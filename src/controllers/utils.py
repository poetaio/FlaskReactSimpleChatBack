from src.resources.data import users
from flask import request, abort

def get_username_from_request():
    username = request.cookies.get('username')

    if username is None or users.get(username) is None:
        abort(401)
    
    return username
