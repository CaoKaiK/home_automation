from flask import render_template, request, jsonify
from app.errors import bp
from app.api.errors import ApiError

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(ApiError)
def api_error(ApiError):
    # Error raised in API
    # check if json response expected
    if wants_json_response():
        return ApiError.to_response()
    
    return render_template(f'errors/{ApiError.status_code}.html'), ApiError.status_code

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(405)
def method_not_allowed(error):
    if wants_json_response():
        method = request.method
        message = f'Method {method} is not allowed for this endpoint'
        error = ApiError(status_code=405, message=message, endpoint=request.url)        
        return error.to_response()
    return render_template('errors/404.html') , 405

@bp.app_errorhandler(406)
def not_accepted(error):
    if wants_json_response():
        content = request.content_type
        message=f'Header: Content-Type must be "application/json". Header Parameter Content-Type was {content}'
        error = ApiError(status_code=406, message=message, endpoint=request.url)
        return error.to_response()
    return render_template('errors/404.html') , 406

@bp.app_errorhandler(415)
def accept_not_accepted(error):
    if wants_json_response():
        accept = request.accept_mimetypes
        message=f'Header: Accept must allow json. Header Parameter Accept was {accept}'
        error = ApiError(status_code=415, message=message, endpoint=request.url)
        return error.to_response()
    return render_template('errors/404.html') , 415