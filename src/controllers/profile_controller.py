from flask import session
from flask.json import jsonify
from flask_restful import Resource

from src.controllers import main as app
from src.resources.data import users, chat_history
    
class Profile(Resource):
    def get(self):
        username = session.get("username")
        user = users.get(username)

        return {
            "username": username,
            "firstName": user.get("first_name"),
            "lastName": user.get("last_name")
        }
