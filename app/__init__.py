import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(congig_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    
    # Error Blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    # Main Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

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