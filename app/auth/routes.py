import json
from flask import jsonify, request, redirect, session, url_for, abort
from app import oauth
import requests


from app.auth import bp
from app.auth.errors import AuthError

from config_auth0 import config_auth0

auth0 = oauth.register(
    'auth0',
    client_id=config_auth0.CLIENT_ID,
    client_secret=config_auth0.CLIENT_SECRET,
    api_base_url=config_auth0.API_BASE_URL,
    access_token_url=config_auth0.ACCES_TOKEN_URL,
    authorize_url=config_auth0.AUTHORIZE_URL,
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@bp.route('/login')
def login():
    # redirect to auth0 url
    return auth0.authorize_redirect(audience=config_auth0.AUDIENCE,redirect_uri='http://127.0.0.1:5000/auth/callback')

    
@bp.route('/callback')
def callback():
    # get token and save in session
    response = auth0.authorize_access_token()
    token = response.get('access_token')
    #print(token)
    session["token"] = token
    return redirect(url_for('main.index'))

@bp.route('/logout')
def logout():
    #clear session
    session.clear()

    params = {
        'client_id': config_auth0.CLIENT_ID
    }

    r = requests.get(config_auth0.API_BASE_URL + '/v2/logout', params=params)

    if not r.status_code==200:
        abort(500)

    return redirect(url_for('main.index'))