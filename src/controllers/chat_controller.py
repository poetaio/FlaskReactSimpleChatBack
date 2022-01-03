import re
from flask_restful import Resource, reqparse
from flask_socketio import join_room, leave_room
from flask import request, abort, Response, jsonify, session

from services import user_service, chat_service, message_service

from . import socketio, get_username_from_request

# returns chat history with the user from url query
# 401 - no token in cookies username or cookies username is invalid
# 400 - no such with_user 
class ChatHistory(Resource):
    def get_chat_history(self):
        username = get_username_from_request()
        
        user_with = request.args.get('username')

        if not user_service.get_user(user_with):
            abort(Response(f"No user exists with username {user_with}", status=400))
        
        users_tuple = (username, user_with) if username < user_with else (user_with, username)
        # TODO: move everything to service
        chat_id = chat_service.get_chat(*users_tuple).chat_id
        
        return username, [m.to_dict() for m in message_service.get_messages(chat_id)]

    def get(self):
        # TODO: split in two controllers: Messages (list all messages, or the last one)
        # and Chat(only chat info, description in future)
        _, users_chat_history = self.get_chat_history()
        return {"chatHistory": users_chat_history}
        
    def post(self):
        # TODO: replace with json
        message = request.args.get('message')
        if message is None or message == "":
            abort(400)

        username = get_username_from_request()
        user_with = request.args.get('username')
        users_tuple = (username, user_with) if username < user_with else (user_with, username)

        # TODO: save chat_id in session
        chat = chat_service.get_chat(users_tuple)
        
        message_service.add_message(chat.chat_id, username, message)
        
        return Response(status=200)


# returns all users usernames with whom user has chat
# 401 - if username in cookies is missing or invalid
class Chats(Resource):
    def get(self):
        username = get_username_from_request()

        user_chats = []
        # TODO: replace with chat.service.get_user_chats(username)
        for chat in chat_service.get_all():
            if chat.user_1 == username:
                user_chats.append(chat.user_2)
            elif chat.user_2 == username:
                user_chats.append(chat.user_1)

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

    # TODO: remove .chat_id()
    room = chat_service.get_chat(username, user_with).chat_id
    join_room(room)

    session["room"] = room
    session["user_with"] = user_with
    

@socketio.on("message")
def on_message(message):
    username = session.get("username")
    room = session.get("room")

    message_service.add_message(room, username, message)
    users_chat_history = [m.to_dict() for m in message_service.get_messages(room)]
    # new_message = {
    #     "from": username,
    #     ""
    # }

    socketio.emit("messages", users_chat_history, room=room)
    

@socketio.on("client_disconnect")
def on_disconnect():
    leave_room(session.get("room"))
