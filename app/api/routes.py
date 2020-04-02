from flask import jsonify, request, abort
from app import db
from app.models import Room, Thing
from app.models import RoomSchema, ThingSchema

from app.api import bp
from app.api import errors as api_error

# check for content type json / ignore for GET-requests
@bp.before_request
def check_content_type():
    if request.content_type != 'application/json':
        if request.method == 'GET':
            pass
        else:
            abort(406)

# check for accept type json
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
    rooms_schema = RoomSchema(many=True)
    return {
        'success': True,
        'result': rooms_schema.dump(rooms)
    }, 200

@bp.route('/rooms/<int:id>', methods=['GET'])
def get_room(id):
    room = Room.query.filter_by(id=id).one_or_none()
    room_schema = RoomSchema()
    return {
        'success': True,
        'result': room_schema.dump(room)
    }

@bp.route('/things', methods=['GET'])
def get_things():
    things = Thing.query.all()
    things_schema = ThingSchema(many=True)
    return {
        'success': True,
        'result': things_schema.dump(things)
    }

@bp.route('/things/<int:id>', methods=['GET'])
def get_thing(id):
    thing = Thing.query.filter_by(id=id).one_or_none()
    thing_schema = ThingSchema()
    return {
        'success': True,
        'result': thing_schema.dump(thing)
    }
