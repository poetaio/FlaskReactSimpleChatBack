from flask_socketio import join_room, leave_room
from flask import request, abort, Response, jsonify, session

from src.controllers import main as app
from src.resources.data import users, chat_history
from src.controllers.utils import get_username_from_request
from src.controllers import socketio

# returns chat history with the user from url query
# 401 - no token in cookies username or cookies username is invalid
# 400 - no such with_user 
@app.route("/api/chat-history", methods=["GET", "POST"])
def get_chat_history():
    username = get_username_from_request()
    
    user_with = request.args.get('username')

    if users.get(user_with) is None:
        abort(Response(f"No user exists with username {user_with}", status=400))
    
    chat_history_key = (username, user_with) if username < user_with else (user_with, username)
    users_chat_history = chat_history.setdefault(chat_history_key, [])

    if request.method == "GET":        
        return jsonify({"chatHistory": users_chat_history})
    elif request.method == "POST":
        message = request.args.get('message')
        if message is None or message == "":
            abort(400)
        
        users_chat_history.append((username, message))
        
        return Response(status=200)


# returns all users usernames with whom user has chat
# 401 - if username in cookies is missing or invalid
@app.route("/api/chats")
def get_all_chats():
    username = get_username_from_request()

    user_chats = []
    for users_pair in chat_history:
        if users_pair[0] == username:
            user_chats.append(users_pair[1])
        elif users_pair[1] == username:
            user_chats.append(users_pair[0])

    return jsonify({"allChats": user_chats})


@socketio.on("connect")
def on_connect():
    print(f"connecting...")


@socketio.on("set_connection")
def set_connection(user_with):
    # todo: check for user_with existence
    # todo add validation

    username = session.get("username")
    user_with = user_with.get("with")

    room = f"{username}:{user_with}" if username < user_with else f"{user_with}:{username}"
    join_room(room)

    session["room"] = room
    session["user_with"] = user_with
    

@socketio.on("message")
def on_message(message):
    username = session.get("username")
    user_with = session.get("user_with")
    room = session.get("room")

    chat_history_key = (username, user_with) if username < user_with else (user_with, username)
    users_chat_history = chat_history.get(chat_history_key, [])
    users_chat_history.append((username, message))
    print(users_chat_history)
    socketio.emit("messages", users_chat_history, room=room)
    
    # print(f"message: {message}, from: {session.get('username')}, to {session.get('user_with')}")


@socketio.on("client_disconnect")
def on_disconnect():
    leave_room(session.get("room"))
