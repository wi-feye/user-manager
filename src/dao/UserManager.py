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

        if Manager.get_user_by_email(email) is not None:
            return jsonify({"error": "Email already exists"}), HTTP_409_CONFLICT

        if Manager.get_user_by_id_zerynth(user.id_zerynth) is not None:
            return jsonify({"error": "Id zerynth already exists"}), HTTP_409_CONFLICT

        if Manager.get_user_by_apikey_zerynth(user.apikey_zerynth) is not None:
            return jsonify({"error": "apikey zerynth already exists"}), HTTP_409_CONFLICT           

        pwd_hash = generate_password_hash(password)

        user = User(
            name=name,
            password=pwd_hash,
            email=email,
            surname=surname,
            apikey_zerynth=user.apikey_zerynth,
            id_zerynth=user.id_zerynth,
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
                        "email": user.email,
                        "id_zerynth": user.id_zerynth,
                        "apikey_zerynth": user.apikey_zerynth
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
                        "id_zerynth": user.id_zerynth,
                        "apikey_zerynth": user.apikey_zerynth
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
                    "email": user.email,
                    "name": user.name,
                    "surname": user.surname,
                    "id_zerynth": user.id_zerynth,
                    "apikey_zerynth": user.apikey_zerynth
                }
            )
        return jsonify(allusers), HTTP_200_OK

    def get_me(id):
        user = Manager.get_user_by_id(id)
        if user:
             return jsonify({
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "surname": user.surname,
                "id_zerynth": user.id_zerynth,
                "apikey_zerynth": user.apikey_zerynth
        })
        return jsonify({"message": "User not found"}), HTTP_404_NOT_FOUND


def user_dict(user):
    return {
        "id": user.id,
        "id_zerynth": user.id_zerynth,
        "apikey_zerynth": user.apikey_zerynth,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "password": user.password,
    }


def contains_number(string):
    return any(char.isdigit() for char in string)
