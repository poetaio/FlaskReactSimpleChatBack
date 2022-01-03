from flask import session, jsonify
from flask_restful import Resource

from services import user_service

class Users(Resource):
    def get(self):
        return [{
            "value": user.username, 
            "name": f"{user.first_name} {user.last_name}"
            }
            for user in user_service.get_all_users()
            if user.username != session.get("username")
        ]

