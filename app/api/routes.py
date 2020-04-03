from flask import jsonify, request, abort
from app import db
from app.models import Room, Thing
from app.models import RoomSchema, ThingSchema

from app.api import bp
from app.api.errors import ApiError

def validate_content(request, params=[]):
    json_data = request.get_json(silent=True)
    # 406 - if content empty or not parsable
    if not json_data:
        raise ApiError(406, 'Content was empty or could not be parsed', request.url)
    
    # 400 - if param is missing
    for param in params:
        val = json_data.get(param, None)
        if not val:
            raise ApiError(400, f'Parameter {param} is missing', request.url)

    return json_data

# init schemas
room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)

thing_schema = ThingSchema()
things_schema = ThingSchema(many=True)

# check for content type json / ignore for GET and DELETE requests
@bp.before_request
def check_content_type():
    if request.content_type != 'application/json':
        if request.method == 'GET' or 'DELETE':
            pass
        else:
            content = request.content_type
            message=f'Header: Content-Type must be "application/json". Header Parameter Content-Type was {content}'
            raise ApiError(406, message, request.url)

# check for accept type json
@bp.before_request
def check_accept():
    if request.accept_mimetypes.accept_json:
        pass
    else:
        accept = request.accept_mimetypes
        message=f'Header: Accept must allow json. Header Parameter Accept was {accept}'
        raise ApiError(415, message, request.url)

# API Status Endpoint
@bp.route('/status', methods=['GET', 'POST'])
def health():
    return jsonify({
        'success': True,
        'code': 200
    })


### Room ###
@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return {
        'success': True,
        'result': rooms_schema.dump(rooms)
    }, 200

@bp.route('/rooms', methods=['POST'])
def post_room():
    json_data = validate_content(request, ['name'])
    name = json_data['name']
    
    # 409 - if room already exists
    if Room.query.filter_by(name=name).one_or_none():
        raise ApiError(409, f'Room with name {name} already exists', request.url)
    
    room = Room(name=name)
    room.insert()
    return {
        'success': True,
        'result': room_schema.dump(room)
    }

@bp.route('/rooms/<int:id>', methods=['GET'])
def get_room(id):
    room = Room.query.filter_by(id=id).one_or_none()
    # 404 - if room does not exist
    if not room:
        raise ApiError(404, 'The requested room was not found', request.url)

    return {
        'success': True,
        'result': room_schema.dump(room)
    }

@bp.route('/rooms/<int:id>', methods=['PATCH'])
def patch_room(id):
    json_data = validate_content(request, ['name'])
    name = json_data['name']

    room = Room.query.filter_by(id=id).one_or_none()
    # 404 - if room does not exist
    if not room:
        raise ApiError(404, 'The requested room was not found', request.url)
    
    room.name = name
    room.patch

    return {
        'success': True,
        'result': room_schema.dump(room)
    }

@bp.route('/rooms/<int:id>', methods=['DELETE'])
def delete_room(id):
    room = Room.query.filter_by(id=id).one_or_none()
    # 404 - if room does not exist
    if not room:
        raise ApiError(404, 'The requested room was not found', request.url)
    
    name = room.name
    room.delete()

    return {
        'success': True,
        'result': {},
        'message': f'Room {name} was deleted'
    }



### Thing ###
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
    if not thing:
        raise ApiError(404, 'The requested thing was not found', request.url)

    thing_schema = ThingSchema()
    return {
        'success': True,
        'result': thing_schema.dump(thing)
    }
