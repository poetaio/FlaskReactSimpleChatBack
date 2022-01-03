from flask_socketio import SocketIO
from flask import Blueprint

socketio = SocketIO()
main = Blueprint('main', __name__)

from .auth_controller import * 
from .chat_controller import *
from .profile_controller import *
from .users_controller import *
