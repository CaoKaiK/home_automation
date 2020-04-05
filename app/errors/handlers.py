from flask import render_template, request, jsonify
from app.errors import bp
from app.api.errors import ApiError
from app.auth.errors import AuthError

# check if json response expected
def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(ApiError)
def api_error(ApiError):
    # Error raised in API
    if wants_json_response():
        return ApiError.to_response()
    
    return render_template(f'errors/{ApiError.status_code}.html'), ApiError.status_code

@bp.app_errorhandler(AuthError)
def auth_error(AuthError):
    # Error raised during Auth
    if wants_json_response():
        return AuthError.to_response()
    
    return render_template(f'errors/{AuthError.status_code}.html'), AuthError.status_code

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

