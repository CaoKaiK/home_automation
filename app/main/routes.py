import requests
from flask import jsonify, render_template, session, request


from app.main import bp


@bp.route('/')
def home():
    response = requests.get(request.url_root + '/api/rooms')
    rooms = response.json()['result']

    return render_template('main/home.html', rooms=rooms)
