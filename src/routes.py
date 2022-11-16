from src.models.User import User
from src.dao.UserManager import UserManager
from src import app
from flask import request,jsonify
import validators
from src.constants.http_status_code import *
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone, timedelta
from flask_jwt_extended import jwt_required, create_access_token,create_refresh_token,get_jwt_identity,get_jwt,set_access_cookies,set_refresh_cookies


#  It checks after every call to the apis if the token is expiring, in case is expiring it refreshs it
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity()) 
        return response
    except (RuntimeError, KeyError):
        return response


# Api registration
@app.post('/register')
def register():
    email= request.json['email']
    password= request.json['password']
    name= request.json['name']
    surname= request.json['surname']
    zerynth_api_key = request.json['zerynth_api_key']
    idz = request.json['idz']
    # idz= TODO get id from zerinth

    if len(password)<8:
        return jsonify({'error': "password is too short, it has to be minimum 8 characters"}),HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}),HTTP_400_BAD_REQUEST

    # if contains_number(name):
    #     return jsonify({'error': "the name cannot contain a number"}),HTTP_400_BAD_REQUEST

    # if contains_number(surname):
    #     return jsonify({'error': "the surname cannot contain a number"}),HTTP_400_BAD_REQUEST
    
    # def contains_number(string):
    #     return any(char.isdigit() for char in string)     

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email already exists"}),HTTP_409_CONFLICT

    #TODO Check if zerynth_api_key exists in zerynth cloud

    pwd_hash=generate_password_hash(password)

    user=User(name=name, password=pwd_hash, email=email, surname=surname,zerynth_api_key=zerynth_api_key, idz=idz)
    UserManager.add(user)

    return jsonify({
        'message': "User created successfully",
        'user': {
            'name': name,
            'surname': surname,
            'email': email
        }          

    }),HTTP_201_CREATED


@app.post('/login')
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
                    'email': user.email,
                    'surname':user.surname,
                    'zerynth_api_key':user.zerynth_api_key

                }
            })
            set_access_cookies(response, access)
            return response


    return jsonify({
        'message': "Wrong credentials"
    }),HTTP_401_UNAUTHORIZED
        


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/")
def api():
    return "<p>API Handle</p>"

@app.route("/push/")
def push():
    user = User()
    user.idz = 'zidprova2'
    user.zerynth_api_key = 'zerynth_api_key2'
    user.email = 'prov2a@gmail.com'
    user.name = 'Dav2ide'
    user.surname = 'Fi2orini'
    user.password = 'pro2222va1234567890'
    UserManager.add(user)
    return "<p>Data pushed</p>"

@app.route("/pull/")
def pull():
    raws = UserManager.get_all()
    return raws


#get all users in the database
@app.get('/all')
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
        })
    return jsonify({'All_users': allusers}), HTTP_200_OK    