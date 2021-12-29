from flask import session, jsonify

from src.controllers import main as app
from src.resources.data import users, chat_history

@app.route("/api/users")
def get_users():
    return jsonify([{"value": username, "name": f"{user['first_name']} {user['last_name']}"} 
        for username, user in users.items()
        if username != session.get("username")
    ])