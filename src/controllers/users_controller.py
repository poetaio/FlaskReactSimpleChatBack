from flask import session, jsonify
from flask_restful import Resource

from src.resources.data import users

class Users(Resource):
    def get(self):
        return [{
            "value": username, 
            "name": f"{user['first_name']} {user['last_name']}"
            } 
            for username, user in users.items()
            if username != session.get("username")
        ]

