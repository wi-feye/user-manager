from flask import Blueprint, request,jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_code import *
import validators
from src.models.user_db import User,db
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity,get_jwt,set_access_cookies
from datetime import datetime, timedelta, timezone

user_manager = Blueprint("user_manager", __name__, url_prefix="/api/v1/auth")

#after every api is called, this function checks if the access_token will expire within the next 30 minutes
#in case it expires, it will use the refresh t
@user_manager.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity()) 
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


#register a new user
@user_manager.post('/register')
def register():
    email= request.json['email']
    password= request.json['password']
    name= request.json['name']
    surname= request.json['surname']

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}),HTTP_400_BAD_REQUEST

    if " " in email:
        return jsonify({'error': "Email is not valid"}),HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email already exists"}),HTTP_409_CONFLICT

    if contains_number(name):
        return jsonify({'error': "the name cannot contain a number"}),HTTP_400_BAD_REQUEST

    if contains_number(surname):
        return jsonify({'error': "the surname cannot contain a number"}),HTTP_400_BAD_REQUEST    

    if len(password)<8:
        return jsonify({'error': "password is too short, it has to be minimum 8 characters"}),HTTP_400_BAD_REQUEST


    pwd_hash=generate_password_hash(password)

    user=User(name=name,password=pwd_hash,email=email,surname=surname)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created successfully",
        'user': {
            'name': name,
            'surname': surname,
            'email': email
        }          

    }),HTTP_201_CREATED


#login user
@user_manager.post('/login')
def login():
    email= request.json.get('email', ' ')
    password = request.json.get('password', ' ')

    user= User.query.filter_by(email=email).first()
    if user:
        is_pass_correct= check_password_hash(user.password, password)

        if is_pass_correct:
            access = create_access_token(identity=user.id)
            
            response= jsonify({
                'user':{
                    'access': access,
                    'name': user.name,
                    'surname': user.surname,
                    'email': user.email,
                }
            })
            set_access_cookies(response, access)
            return response


    return jsonify({
        'message': "Wrong credentials"
    }),HTTP_401_UNAUTHORIZED


#get person information
@user_manager.get('/me')
#only users that have an access_token can access this api
@jwt_required()
def me():

    # get_jwt_identity returns the id of the user
    user_id =get_jwt_identity() 
    user= User.query.filter_by(id=user_id).first()

    return jsonify({
        "email": user.email,
        "name": user.name

    }), HTTP_200_OK


#get all users in the database
@user_manager.get('/all')
def all():
    users= User.query.all()

    allusers=[]

    for user in users:
        allusers.append({
            'id': user.id,
            'password': user.password,
            'email' :user.email,
            'name': user.name,
            'surname': user.name,
            'created_at': user.created_at
        })
    return jsonify({'All_users': allusers}), HTTP_200_OK


def contains_number(string):
    return any(char.isdigit() for char in string)    
              