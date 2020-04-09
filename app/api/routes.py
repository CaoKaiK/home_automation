from datetime import datetime
from flask import jsonify, request, abort
from app import db
from app.models import Room, Thing
from app.models import RoomSchema, ThingSchema

from app.api import bp
from app.api.errors import ApiError

from app.auth.auth import requires_auth

# init schemas
room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)

thing_schema = ThingSchema()
things_schema = ThingSchema(many=True)


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

# check for content type json / ignore for GET and DELETE requests
@bp.before_request
def check_content_type():
    if request.content_type != 'application/json':
        if request.method in ['GET', 'DELETE']:
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
    room.patch()

    return {
        'success': True,
        'result': room_schema.dump(room)
    }

@bp.route('/rooms/<int:id>', methods=['DELETE'])
@requires_auth('delete:rooms')
def delete_room(payload, id):
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
    location = request.args.get('room', None)
    if location:
        things = Thing.query.filter_by(room_id=location).all()
    else:
        things = Thing.query.all()
    return {
        'success': True,
        'result': things_schema.dump(things)
    }

@bp.route('/things', methods=['POST'])
def post_thing():
    json_data = validate_content(request, ['name', 'room_id'])
    name = json_data['name']
    room_id = json_data['room_id']

    room = Room.query.filter_by(id=room_id).one_or_none()
    # 404 - if room does not exist
    if not room:
        raise ApiError(404, 'The requested room was not found', request.url)
    
    thing = Thing(name=name, room_id=room_id)
    thing.insert()
    return {
        'success': True,
        'result': thing_schema.dump(thing)
    }

@bp.route('/things/<int:id>', methods=['GET'])
def get_thing(id):
    thing = Thing.query.filter_by(id=id).one_or_none()
    # 404 - if thing does not exist
    if not thing:
        raise ApiError(404, 'The requested thing was not found', request.url)

    return {
        'success': True,
        'result': thing_schema.dump(thing)
    }


@bp.route('/things/<int:id>', methods=['PATCH'])
def rename_thing(id):
    json_data = validate_content(request, ['name'])
    name = json_data['name']

    thing = Thing.query.filter_by(id=id).one_or_none()
    # 404 - if thing does not exist
    if not thing:
        raise ApiError(404, 'The requested thing was not found', request.url)
    
    thing.name = name
    thing.patch()

    return {
        'success': True,
        'result': thing_schema.dump(thing)
    }

@bp.route('/things/<int:id>', methods=['DELETE'])
@requires_auth('delete:things')
def delete_thing(payload, id):
    thing = Thing.query.filter_by(id=id).one_or_none()
    # 404 - if thing does not exist
    if not thing:
        raise ApiError(404, 'The requested thing was not found', request.url)
    
    name = thing.name
    thing.delete()

    return {
        'success': True,
        'result': {},
        'message': f'Thing {name} was deleted'
    }

@bp.route('things/<int:id>/flip', methods=['PATCH'])
@requires_auth('flip:things')
def flip_a_thing(payload, id):
    thing = Thing.query.filter_by(id=id).one_or_none()
    # 404 - if thing does not exist
    if not thing:
        raise ApiError(404, 'The requested thing was not found', request.url)
    
    # flip and save flipping time
    if thing.status:
        thing.status = False
    else:
        thing.status = True
    thing.last_switched = datetime.utcnow()

    thing.patch()

    return {
        'success': True,
        'result': thing_schema.dump(thing)
    }