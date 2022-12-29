from src.models.User import User
from src.dao.UserManager import UserManager
from src import app
from flask import request, jsonify
from src.constants.http_status_code import *
from datetime import datetime, timezone, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
import requests


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

def get_zerynth_prrofile_by_apikey(apikey):
    return requests.get("https://api.login.zerynth.com/v1/auth/profile", headers={"X-API-KEY": apikey})

# Api registration
@app.post("/register/")
def register():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]
    surname = request.json["surname"]
    apikey_zerynth = request.json["apikey_zerynth"]
    zprofile_res = get_zerynth_prrofile_by_apikey(apikey_zerynth)
    if not zprofile_res.ok:
        return (
                jsonify({"error": "the api key is not correct"}),
                zprofile_res.status_code,
            )
    id_zerynth = zprofile_res.json()["uid"]

    user = User(
        name=name,
        password=password,
        email=email,
        surname=surname,
        apikey_zerynth=apikey_zerynth,
        id_zerynth=id_zerynth,
    )
    return UserManager.register(user)


@app.post("/login/")
def login():
    email = request.json["email"]
    password = request.json["password"]
    return UserManager.login(email, password)

# get all users in the database
@app.get("/users/")
def all():
    return UserManager.get_all()

# get data of the user
@app.get("/user")
def get_info_user():
    id= request.args.get('id', type = int)
    if id:
        return UserManager.get_me(id), HTTP_200_OK
    return jsonify({"message":"id not received"}), HTTP_400_BAD_REQUEST           