from flask import jsonify, render_template, session


from app.main import bp


@bp.route('/index')
def index():
    user = {'username': 'Niklas'}
    
    return render_template('main/index.html', title='Page Title', user=user)
