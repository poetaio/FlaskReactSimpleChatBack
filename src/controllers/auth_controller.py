from flask import make_response, request, abort, session, Response
from flask_restful import Resource, reqparse

from .utils import get_username_from_request
from data import users
from services import auth_service
from models import AuthUser


class LoginVerify(Resource):
    def get(self):
        username = request.cookies.get('username')

        if username is None or users.get(username) is None:
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

        if username is None or password is None or first_name is None or last_name is None:
            abort(400)

        if username in users:
            abort(status=401)
        
        users[username] = {"first_name": first_name, "last_name": last_name, "password": password}

        response = make_response('')
        # response.set_cookie('username', username)
        # session["username"] = username
        
        return response


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
