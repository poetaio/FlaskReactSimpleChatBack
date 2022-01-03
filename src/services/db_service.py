from repos import OpenDB
from config import db_name

# TODO: replace with admin service???
class DBService:
    def __create_users(self):
        add_user = "INSERT INTO users VALUES (NULL, ?, ?, ?, ?)"
        self.cursor.execute(add_user, ("poetaio", "ilia", "poeta", "12345"))
        self.cursor.execute(add_user, ("markwo", "mark", "wotson", "12345"))
        self.cursor.execute(add_user, ("mj", "mary", "jane", "12345"))

    def __create_chats_table(self):
        # TODO: replace usernames with user ids
        create_chats_table_st = "CREATE TABLE IF NOT EXISTS chats (chat_id INTEGER PRIMARY KEY, user_1 text, user_2 text)"
        self.cursor.execute(create_chats_table_st)

    def __create_messages_table(self):
        create_messages_table_st = "CREATE TABLE IF NOT EXISTS messages (message_id INTEGER PRIMARY KEY, chat_id INTEGER, user_from text, message_text text)"
        self.cursor.execute(create_messages_table_st)

    def init_db(self):
        with OpenDB(db_name) as cursor:
            self.cursor = cursor
            create_table = "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username text, first_name text, last_name text, password text)"
            self.cursor.execute(create_table)

            self.__create_users()

            self.__create_chats_table()
            self.__create_messages_table()


db_service = DBService()
