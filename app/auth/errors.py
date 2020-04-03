from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

class AuthError(Exception):
    def __init__(self, status_code, message=None):
        Exception.__init__(self)
        self.status_code = status_code
        self.message = message
    
    def to_response(self):
        payload = {}
        payload['error'] = HTTP_STATUS_CODES.get(self.status_code, 'Unknown')
        if self.message:
            payload['message'] = self.message

        response = jsonify(payload)
        response.status_code = self.status_code
        return response