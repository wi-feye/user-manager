from src.models.User import User
from src.dao.UserManager import UserManager
from src import app
from flask import request, jsonify
from src.constants.http_status_code import *
from datetime import datetime, timezone, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt


#  It checks after every call to the apis if the token is expiring, in case is expiring it refreshs it
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access = create_access_token(identity=get_jwt_identity())
        return response
    except (RuntimeError, KeyError):
        return response


# Api registration
@app.post("/register/")
def register():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]
    surname = request.json["surname"]
    zerynth_api_key = request.json["zerynth_api_key"]
    idz = request.json["idz"]

    user = User(
        name=name,
        password=password,
        email=email,
        surname=surname,
        zerynth_api_key=zerynth_api_key,
        idz=idz,
    )
    return UserManager.register(user)


@app.post("/login/")
def login():
    email = request.json.get("email", " ")
    password = request.json.get("password", " ")

    return UserManager.login(email, password)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/")
def api():
    return "<p>API Handle</p>"


@app.route("/push/")
def push():
    user = User()
    user.idz = "zidprova2"
    user.zerynth_api_key = "zerynth_api_key2"
    user.email = "prov2a@gmail.com"
    user.name = "Dav2ide"
    user.surname = "Fi2orini"
    user.password = "pro2222va1234567890"
    UserManager.add(user)
    return "<p>Data pushed</p>"


@app.route("/pull/")
def pull():
    raws = UserManager.get_all()
    return raws


# get all users in the database
@app.get("/users/")
def all():
    return UserManager.get_all()


# get data of the user
@app.get("/user")
def get_info_user():
    id= request.args.get('id', type = int)
    if id:
        return UserManager.get_me(id)
    return jsonify({"message":"id not received"}), HTTP_400_BAD_REQUEST           