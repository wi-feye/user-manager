from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

app = None
db = None
migrate = None

def create_app():
    global app
    global db
    global migrate

    app = Flask(__name__)
    JWTManager(app)
    app.config.from_object(Config)
    app.config.from_mapping(
        JWT_COOKIE_SECURE=False,
        JWT_TOKEN_LOCATION=["cookies"],
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        JWT_ACCESS_TOKEN_EXPIRES= timedelta(hours=12),
        JWT_COOKIE_CSRF_PROTECT=True
    )

    # env = Environments(app)
    # env.from_object(Config)

    db = SQLAlchemy(
        app=app
    )

    from src.models import User

    migrate = Migrate(
        app=app,
        db=db
    )

    from src import routes

    app.app_context().push()
    db.create_all()


    from src.init_static_db import init_user
    from src.dao.UserManager import UserManager
    from src.dao.manager import Manager
    
    # Manager.delete_all_user()
    if Manager.get_all()==[]:
        init_user()

    return app
    