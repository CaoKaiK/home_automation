from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None, endpoint=None):
    payload = {
        'error': HTTP_STATUS_CODES.get(status_code, 'Unknown'),
        }
    if message:
        payload['message'] = message
    if endpoint:
        payload['endpoint'] = endpoint
    response = jsonify(payload)
    response.status_code = status_code
    return response

