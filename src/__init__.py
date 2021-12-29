from flask import Flask
from flask_socketio import SocketIO

# from src.controllers.main import main as main_blueprint
# from src.controllers.socketio import socketio

from src.controllers import main as main_blueprint, socketio

app = Flask(__name__)

app.register_blueprint(main_blueprint)
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

socketio.init_app(app)
socketio.run(app, host="0.0.0.0", port=5000)
