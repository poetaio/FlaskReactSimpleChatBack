from flask import request, abort
from services import user_service

def get_username_from_request():
    username = request.cookies.get('username')

    if not username or not user_service.get_user(username):
        abort(401)
    
    return username
