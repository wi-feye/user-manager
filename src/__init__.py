from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = None
db = None
migrate = None

def create_app():
    global app
    global db
    global migrate

    app = Flask(__name__)
    app.config.from_object(Config)

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

    return app
    