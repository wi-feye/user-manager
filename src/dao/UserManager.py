from src.models.User import User
from src.dao.manager import Manager
import validators
from src.constants.http_status_code import *
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt,
    set_access_cookies,
)


class UserManager(Manager):
    @staticmethod
    def add(user: User):
        Manager.create(user=user)

    # @staticmethod
    # def get_all():
    #     users = User.query.all()
    #     users = [user_dict(user) for user in users]
    #     return users

    @staticmethod
    def register(user):
        name = user.name.strip()
        surname = user.surname.strip()
        email = "".join(user.email.split())
        password = user.password.strip()

        if len(password) < 8:
            return (
                jsonify(
                    {
                        "error": "password is too short, it has to be minimum 8 characters"
                    }
                ),
                HTTP_400_BAD_REQUEST,
            )

        if not validators.email(email):
            return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

        if contains_number(name):
            return (
                jsonify({"error": "the name cannot contain a number"}),
                HTTP_400_BAD_REQUEST,
            )

        if contains_number(surname):
            return (
                jsonify({"error": "the surname cannot contain a number"}),
                HTTP_400_BAD_REQUEST,
            )

            

        # TODO get idz from zerinth
        # TODO check if zerynth_api_key for real exists in zerynth cloude

        if Manager.get_user_by_email(email) is not None:
            return jsonify({"error": "Email already exists"}), HTTP_409_CONFLICT

        if Manager.get_user_by_idz(user.idz) is not None:
            return jsonify({"error": "Id zerynth already exists"}), HTTP_409_CONFLICT

        if Manager.get_user_by_idz(user.zerynth_api_key) is not None:
            return jsonify({"error": "zeryntH api key already exists"}), HTTP_409_CONFLICT           


        pwd_hash = generate_password_hash(password)

        user = User(
            name=name,
            password=pwd_hash,
            email=email,
            surname=surname,
            zerynth_api_key=user.zerynth_api_key,
            idz=user.idz,
        )
        UserManager.add(user)

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "user": {
                        "id":user.id,
                        "name": user.name,
                        "surname": user.surname,
                        "email": user.email
                    },
                }
            ),
            HTTP_201_CREATED,
        )

   
    def login(email, password):
        email = email.strip()
        is_pass_correct=False
        user = Manager.get_user_by_email(email)
        if user:
            is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            access = create_access_token(identity=user.id)

            response = jsonify(
                {
                    "user": {
                        "id": user.id,
                        "access": access,
                        "name": user.name,
                        "email": user.email,
                        "surname": user.surname,
                        "zerynth_api_key": user.zerynth_api_key,
                    }
                }
            )
            set_access_cookies(response, access)
            return response

        return jsonify({"message": "Wrong credentials"}), HTTP_401_UNAUTHORIZED

    def get_all():
        users= Manager.get_all()
        allusers = []
        for user in users:
            allusers.append(
                {
                    "id": user.id,
                    "password": user.password,
                    "email": user.email,
                    "name": user.name,
                    "surname": user.surname,
                    "idz": user.idz,
                    "zerynth_api_key": user.zerynth_api_key
                }
            )
        return jsonify({"All_users": allusers}), HTTP_200_OK

    
    
    def get_me(id):
        user = Manager.get_user_by_id(id)
        if user:
             return jsonify({
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "surname": user.surname,
                "idz": user.idz,
                "zerynth_api_key": user.zerynth_api_key
        })
        return jsonify({"message": "User not found"}), HTTP_404_NOT_FOUND




def user_dict(user):
    return {
        "id": user.id,
        "idz": user.idz,
        "zerynth_api_key": user.zerynth_api_key,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "password": user.password,
    }
  


def contains_number(string):
    return any(char.isdigit() for char in string)
