from flask import Flask, make_response, request, abort, session
from flask.json import jsonify
from flask.wrappers import Response
from flask_socketio import SocketIO, join_room, leave_room

socketio = SocketIO()


app = Flask(__name__)

users = {
    "poetaio": {
        "first_name": "ilia",
        "last_name": "poeta",
        "password": "12345"
    },
    "poetamo": {
        "first_name": "Mary",
        "last_name": "Jane",
        "password": "12345"
    },
    "markwo": {
        "first_name": "Mark",
        "last_name": "Wolson",
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
    ], ("markwo", "poetaio"): [
        ("markwo", "hello, ilia"),
        ("markwo", "how r u?"),
        ("poetaio", "hey, n"),
        ("poetaio", "fine"),
        ("poetaio", "u?"),
        ("markwo", "great!"),
    ]
}

def get_username_from_request():
    username = request.cookies.get('username')

    if username is None or users.get(username) is None:
        abort(401)
    
    return username



@app.route("/api/profile")
def profile():
    username = session.get("username")
    user = users.get(username)

    return jsonify({
        "username": username,
        "firstName": user.get("first_name"),
        "lastName": user.get("last_name")
    })


@app.route("/api/login_verify")
def login_verify():
    username = request.cookies.get('username')

    if username is None or users.get(username) is None:
        return Response(status=200)
    
    return Response(status=302)


@app.route("/api/verify")
def verify():
    get_username_from_request()
    return Response(status=200)


@app.route("/api/register", methods=["POST"])
def register():
    username = request.args.get('username')
    first_name = request.args.get('firstName')
    last_name = request.args.get('lastName')
    password = request.args.get('password')

    if username is None or password is None or first_name is None or last_name is None:
        abort(400)

    if username in users:
        abort(status=401)
    
    users[username] = {"first_name": first_name, "last_name": last_name, "password": password}

    response = make_response()
    # response.set_cookie('username', username)
    # session["username"] = username
    
    return response

# sets cookie value for user
# 400 - username or password missing
# 401 - username or password is incorrect
@app.route("/api/login", methods=["POST"])
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
    session["username"] = username

    return response


@app.route("/api/logout")
def logout():
    response = make_response()
    response.set_cookie('username', '')
    return response


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
    users_chat_history = chat_history.get(chat_history_key, [])

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
    socketio.emit("messages", users_chat_history, room=room)
    
    # print(f"message: {message}, from: {session.get('username')}, to {session.get('user_with')}")


@socketio.on("client_disconnect")
def on_disconnect():
    leave_room(session.get("room"))


app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
socketio.init_app(app)
socketio.run(app, host="0.0.0.0", port=5000)
