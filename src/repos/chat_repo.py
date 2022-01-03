from . import OpenDB
from models import Chat, Message
from config import db_name
from services import user_service

class ChatRepo:
    def add_chat(self, chat: Chat):
        with OpenDB(db_name) as cursor:
            add_chat_st = "INSERT INTO chats VALUES (NULL, ?, ?)"
            cursor.execute(add_chat_st, (chat.user_1, chat.user_2))

            get_chat_id = "SELECT last_insert_rowid()"
            row = cursor.execute(get_chat_id).fetchone()
            
            chat.chat_id = row[0]
            return chat


    def get_chat_by_id(self, chat_id):
        with OpenDB(db_name) as cursor:
            get_chat_st = "SELECT * FROM chats WHERE chat_id=? LIMIT 1"
            row = cursor.execute(get_chat_st, (chat_id,)).fetchone()

            if row:
                return Chat(*row)
            else:
                return None


    def get_chat(self, chat: Chat):
        with OpenDB(db_name) as cursor:
            get_chat_st = "SELECT chat_id FROM chats WHERE user_1=? AND user_2=? LIMIT 1"
            row = cursor.execute(get_chat_st, (chat.user_1, chat.user_2)).fetchone()

            if row:
                chat.chat_id = row[0]
                return chat
            else:
                return None

    def get_all(self):
        with OpenDB(db_name) as cursor:
            get_all_st = "SELECT * FROM chats"
            return [Chat(*row) for row in cursor.execute(get_all_st).fetchall()]
            


chat_repo = ChatRepo()
