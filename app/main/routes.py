from flask import jsonify, render_template, session


from app.main import bp


@bp.route('/')
def home():
    
    
    return render_template('main/home.html')
