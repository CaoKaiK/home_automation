from flask import render_template, request, Response
from app.errors import bp
from app.api.errors import error_response as api_error_response

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        url = request.url
        return api_error_response(
            404,
            message=f'Ressource was not found',
            endpoint=url
            )
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(405)
def method_not_allowed(error):
    if wants_json_response():
        method = request.method
        url = request.url
        return api_error_response(
            405,
            message=f'Method {method} is not allowed for this endpoint',
            endpoint=url
            )
    return render_template('errors/404.html') , 405

@bp.app_errorhandler(406)
def not_accepted(error):
    if wants_json_response():
        url = request.url
        content = request.content_type
        return api_error_response(
            406,
            message=f'Header: Content-Type must be "application/json". Header Parameter Content-Type was {content}',
            endpoint=url
            )
    return render_template('errors/404.html') , 406

@bp.app_errorhandler(415)
def accept_not_accepted(error):
    if wants_json_response():
        url = request.url
        accept = request.accept_mimetypes
        return api_error_response(
            406,
            message=f'Header: Accept must allow json. Header Parameter Accept was {accept}',
            endpoint=url
            )
    return render_template('errors/404.html') , 415