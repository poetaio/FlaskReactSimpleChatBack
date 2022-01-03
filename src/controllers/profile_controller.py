from flask import session
from flask.json import jsonify
from flask_restful import Resource

from services import user_service


    
class Profile(Resource):
    def get(self):
        username = session.get("username")
        user = user_service.get_user(username)

        return {
            "username": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name
        }
