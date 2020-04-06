import json
import requests
from flask import request
from functools import wraps
from jose import jwt

from app.auth.errors import AuthError

AUTH0_DOMAIN = 'caokai.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'home_automation'

# Auth Header
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    # 401 - No Auth in Header
    if not auth:
        raise AuthError(401, 'Authorization Header required')

    header_parts = auth.split()

    # 401 - If not Bearer Token
    if len(header_parts) != 2:
        raise AuthError(401, 'Authorization Header must be Bearer Token')
    elif header_parts[0].lower() != 'bearer':
        raise AuthError(401, 'Authorization Header must be Bearer Token')
    
    return header_parts[1]


def check_permissions(permission, payload):
    # 401 - Permissions not in JWT
    if 'permissions' not in payload:
        raise AuthError(401, 'No permissions in JWT')
    
    # 403 - Required permission not in JWT
    if permission not in payload['permissions']:
        raise AuthError(403, 'Required permission not in JWT')

    return True


def verify_decode_jwt(token):
    # auth0 public key for RS256
    url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    r = requests.get(url)

    keys = r.json().get('keys', None)
    
    # 401
    if not keys:
        raise AuthError(401, 'Auth0 public key not found')

    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    key = keys[0]

    if key['kid'] == unverified_header['kid']:
        rsa_key = {
            'kty': key['kty'],  # RSA
            'kid': key['kid'],  # Key Id
            'use': key['use'],  # sig Signature
            'n': key['n'],  # (n, e) public key
            'e': key['e']
        }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


