from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

class ApiError(Exception):
    def __init__(self, status_code, message=None, endpoint=None):
        Exception.__init__(self)
        self.status_code = status_code
        self.message = message
        self.endpoint = endpoint
    
    def to_response(self):
        payload = {}
        payload['error'] = HTTP_STATUS_CODES.get(self.status_code, 'Unknown')
        if self.message:
            payload['message'] = self.message
        if self.endpoint:
            payload['endpoint'] = self.endpoint

        response = jsonify(payload)
        response.status_code = self.status_code
        return response

