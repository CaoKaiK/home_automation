from flask import jsonify, request
from app import db
from app.models import Room, Thing

from app.api import bp

@bp.route('/status', methods=['GET'])
def health():
    return jsonify({
        'success': True,
        'code': 200
    })
