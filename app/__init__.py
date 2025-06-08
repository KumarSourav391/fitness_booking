from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import get_config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)

    from .routes.booking_routes import booking_bp
    app.register_blueprint(booking_bp)

    from .routes.class_routes import classes_bp
    app.register_blueprint(classes_bp)

    with app.app_context():
        from . import models
        db.create_all()

    return app