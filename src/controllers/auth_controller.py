from typing import Any
from flask import make_response, request, abort, session, Response
from flask_restful import Resource, reqparse

from .utils import get_username_from_request
from services import auth_service, user_service
from models import AuthUser, User


class LoginVerify(Resource):
    def get(self):
        username = request.cookies.get('username')

        if not username or not user_service.get_user(username):
            return '', 204
        
        return '', 302


class Verify(Resource):
    def get(self):
        get_username_from_request()
        return '', 204


class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="'username' is required non empty field"
    )
    parser.add_argument('firstName',
        type=str,
        required=True,
        help="'firstName' is required non empty field"
    )
    parser.add_argument('lastName',
        type=str,
        required=True,
        help="'lastName' is required non empty field"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="'password' is required non empty field"
    )

    def post(self):
        data = self.parser.parse_args()

        username = data.get('username')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        password = data.get('password')
        
        try:
            return user_service.add_user(User(None, username, first_name, last_name, password)).to_dict(), 200
        except BaseException as err:
            abort(401)


# sets cookie value for user
# 400 - username or password missing
# 401 - username or password is incorrect
class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="'username' is a required non empty field"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="'password' is  a required non empty field"
    )

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']

        if not auth_service.login(AuthUser(username, password)):
            return "", 401
        
        response = make_response('')
        response.set_cookie('username', username)
        session["username"] = username

        return response


class Logout(Resource):
    def get(self):
        response = make_response('')
        response.set_cookie('username', '')
        response.status = 204
        return response
