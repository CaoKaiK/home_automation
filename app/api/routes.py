from flask import jsonify, request, abort
from app import db
from app.models import Room, Thing

from app.api import bp
from app.api import errors as api_error

@bp.before_request
def check_content_type():
    if request.content_type != 'application/json':
        if request.method == 'GET':
            pass
        else:
            abort(406)

@bp.before_request
def check_accept():
    if request.accept_mimetypes.accept_json:
        pass
    else:
        abort(415)



@bp.route('/status', methods=['GET'])
def health():
    return jsonify({
        'success': True,
        'code': 200
    })

@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify({
        'result': {},

    }), 200
