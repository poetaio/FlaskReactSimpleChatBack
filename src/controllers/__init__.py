from flask_socketio import SocketIO
from flask import Blueprint


socketio = SocketIO()
main = Blueprint('main', __name__)

from . import auth_controller, chat_controller, profile_controller, users_controller, main, socketio
