from flask import session

from src.controllers import main as app
from src.resources.data import users, chat_history

from flask.json import jsonify


@app.route("/api/profile")
def profile():
    username = session.get("username")
    user = users.get(username)

    return jsonify({
        "username": username,
        "firstName": user.get("first_name"),
        "lastName": user.get("last_name")
    })
