import time
from flask import Flask, make_response, request, abort
from flask.json import jsonify
from flask.wrappers import Response
from werkzeug.utils import redirect

import threading

from werkzeug.wrappers import response
def setInterval(func, t):
    def period():
        while True:
            time.sleep(t)
            func()
    threading.Thread(target=period).start()


app = Flask(__name__)

users = {
    "poetaio": {
        "name": "ilia",
        "password": "12345"
    },
    "poetamo": {
        "name": "mary",
        "password": "12345"
    },
    "nusya": {
        "name": "den",
        "password": "12345"
    }
}

chat_history = {
    ("poetaio", "poetamo"): [
        ("poetaio", "hello"),
        ("poetaio", "how r u?"),
        ("poetamo", "hey"),
        ("poetamo", "fine"),
        ("poetamo", "u?"),
        ("poetaio", "great!"),
    ], ("nusya", "poetaio"): [
        ("nusya", "hello, ilia"),
        ("nusya", "how r u?"),
        ("poetaio", "hey, n"),
        ("poetaio", "fine"),
        ("poetaio", "u?"),
        ("nusya", "great!"),
    ]
}

@app.route("/api/")
def home():
    return("Init")

# sets cookie value for user
# 400 - username or password missing
# 401 - username or password is incorrect
@app.route("/api/login", methods=["POST", "GET"])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if username is None or password is None:
        abort(400)

    user = users.get(username)
    if user is None or user.get("password") != password:
        abort(status=401)
    
    response = make_response("Login successful")
    response.set_cookie('username', username)

    return response


# returns chat history with the user from url query
# 401 - no token in cookies username or cookies username is invalid
# 400 - no such with_user 
@app.route("/api/chat-history", methods=["GET", "POST"])
def get_chat_history():
    username = request.cookies.get('username')

    if username is None or users.get(username) is None:
        abort(401)
    
    user_with = request.args.get('username')

    if users.get(user_with) is None:
        abort(Response(f"No user exists with username {user_with}", status=400))
    
    chat_history_key = (username, user_with) if username < user_with else (user_with, username)
    users_chat_history = chat_history.get(chat_history_key)

    if request.method == "GET":
        if users_chat_history is None:
            chat_history[chat_history_key] = []
            return jsonify({"chatHistory": []})
        
        return jsonify({"chatHistory": users_chat_history})
    elif request.method == "POST":
        message = request.args.get('message')
        if message is None or message == "":
            abort(400)
        
        users_chat_history.append((username, message))
        
        return Response(status=200)

import redis
red = redis.StrictRedis()

import datetime

@app.route('/post', methods=['POST'])
def post():
    message = request.form['message']
    now = datetime.datetime.now().replace(microsecond=0).time()
    red.publish('chat', u'[%s] %s: %s' % (now.isoformat(), "user", message))
    return Response(status=204)

@app.route("/updater")
def chat_change_event():
    def event_stream():
        pubsub = red.pubsub()
        pubsub.subscribe('chat')
        for message in pubsub.listen():
            print(message)
            yield('data: %s\n\n' % message['data'])

    return Response(event_stream(), mimetype="text/event-stream")
    # resp.headers['Connection'] = 'keep-alive'
    # resp.headers['Content-Type'] = 'text/event-stream'
    # resp.headers['Cache-Control'] = 'no-cache'
    # def func():
    #     resp.
    # Connection: "keep-alive",
    # "Content-Type": "text/event-stream",
    # "Cache-Control": "no-cache",


# returns all users usernames with whom user has chat
# 401 - if username in cookies is missing or invalid
@app.route("/api/chats")
def get_all_chats():
    username = request.cookies.get('username')

    if username is None or users.get(username) is None:
        abort(401)
    
    # user_chats = [
    #     x[1] for x in chat_history 
    #         if x[0] == username 
    #         or
    #         x[1]
    #         if x[0] == username
    # ]

    user_chats = []
    for users_pair in chat_history:
        if users_pair[0] == username:
            user_chats.append(users_pair[1])
        elif users_pair[1] == username:
            user_chats.append(users_pair[0])

    return jsonify({"allChats": user_chats})


app.run("0.0.0.0", port=5000)
