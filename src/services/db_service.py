from repos import OpenDB
from config import db_name

class DBService:
    def __add_users(self):
        add_user = "INSERT INTO users VALUES (NULL, ?, ?, ?, ?)"
        self.cursor.execute(add_user, ("poetaio", "ilia", "poeta", "12345"))
        self.cursor.execute(add_user, ("markwo", "mark", "wotson", "12345"))
        self.cursor.execute(add_user, ("mj", "mary", "jane", "12345"))

    def init_db(self):
        with OpenDB(db_name) as cursor:
            self.cursor = cursor
            create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, first_name text, last_name text, password text)"
            self.cursor.execute(create_table)

            self.__add_users()


db_service = DBService()
