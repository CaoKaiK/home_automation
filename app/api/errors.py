from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None, location=None):
    payload = {
        'error': HTTP_STATUS_CODES.get(status_code, 'Unknown'),
        'code': status_code
        }
    if message:
        payload['message'] = message
    if location:
        payload['location'] = location
    response = jsonify(payload)
    response.status_code = status_code
    return response