import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

from authlib.integrations.flask_client import OAuth

from config import Config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
cors = CORS()
oauth = OAuth()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    oauth.init_app(app)
    

    # Error Blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    # Main Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    # Auth Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    # API Blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/main.log', maxBytes=10240, backupCount=10)

        fmt = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        file_handler.setFormatter(logging.Formatter(fmt=fmt))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler) # pylint: disable=maybe-no-member

        app.logger.setLevel(logging.INFO) # pylint: disable=maybe-no-member
        app.logger.info('Start Logging') # pylint: disable=maybe-no-member
    
    return app

from app import models