from . import OpenDB
from config import db_name
from models import Message

class MessageRepo:
    def get_messages(self, chat_id):
        with OpenDB(db_name) as cursor:
            get_messages_st = "SELECT * FROM messages where chat_id=?"
            messages_rows = cursor.execute(get_messages_st, (chat_id,)).fetchall()

            return [Message(*row) for row in messages_rows]

    def add_message(self, chat_id, user_from, message_text):
        with OpenDB(db_name) as cursor:
            add_message_st = "INSERT INTO messages VALUES (NULL, ?, ?, ?)"
            cursor.execute(add_message_st, (chat_id, user_from, message_text))


message_repo = MessageRepo()
