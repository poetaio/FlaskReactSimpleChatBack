from flask import Flask
from flask_socketio import SocketIO
from flask_restful import Api

from controllers import *
from controllers import main as main_blueprint
from services import db_service

app = Flask(__name__)

app.register_blueprint(main_blueprint)
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app, errors=Flask.errorhandler)
api.add_resource(Profile, "/api/profile")
api.add_resource(Users, "/api/users")
api.add_resource(Chats, "/api/chats")
api.add_resource(ChatHistory, "/api/chat-history")
api.add_resource(Login, "/api/login")
api.add_resource(Logout, "/api/logout")
api.add_resource(Register, "/api/register")
api.add_resource(Verify, "/api/verify")
api.add_resource(LoginVerify, "/api/login_verify")

db_service.init_db()

socketio.init_app(app)
socketio.run(app, host="0.0.0.0", port=5000)
