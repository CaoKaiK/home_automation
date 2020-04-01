from flask import jsonify
from flask import render_template

from app.main import bp


@bp.route('/index')
def index():
    user = {'username': 'Niklas'}
    return render_template('main/index.html', title='Page Title', user=user)
