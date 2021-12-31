from flask import make_response, request, abort, session, Response
from flask_restful import Resource

from src.controllers.utils import get_username_from_request
from src.controllers import main as app
from src.resources.data import users

@app.route("/api/login_verify")
class LoginVerify(Resource):
    def get(self):
        username = request.cookies.get('username')

        if username is None or users.get(username) is None:
            return Response(status=200)
        
        return Response(status=302)


class Verify(Resource):
    def get(self):
        get_username_from_request()
        return Response(status=200)


class Register(Resource):
    def post(self):
        username = request.args.get('username')
        first_name = request.args.get('firstName')
        last_name = request.args.get('lastName')
        password = request.args.get('password')

        if username is None or password is None or first_name is None or last_name is None:
            abort(400)

        if username in users:
            abort(status=401)
        
        users[username] = {"first_name": first_name, "last_name": last_name, "password": password}

        response = make_response()
        # response.set_cookie('username', username)
        # session["username"] = username
        
        return response


# sets cookie value for user
# 400 - username or password missing
# 401 - username or password is incorrect
class Login(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')

        if username is None or password is None:
            abort(400)

        user = users.get(username)
        if user is None or user.get("password") != password:
            abort(status=401)
        
        response = make_response("Login successful")
        response.set_cookie('username', username)
        session["username"] = username

        return response


class Logout(Resource):
    def get(self):
        response = make_response()
        response.set_cookie('username', '')
        return response, 200
