from datetime import timedelta
from flask import Flask
import os
from src.user_manager import user_manager
from src.models.user_db import db
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    
    app= Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_COOKIE_SECURE=False,
            JWT_TOKEN_LOCATION=["cookies"],
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
            JWT_COOKIE_CSRF_PROTECT=True

        )
    else:
        app.config.from_mapping(test_config)    


    db.app=app
    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(user_manager)

    return app    


