from sqlite3.dbapi2 import Error
from typing import Any
from . import OpenDB
from config import db_name
from models import User

# v = list['User']

class UserRepo:
    def get_user(self, username: str) -> User:
        # TODO: split for login select / profile select maybe
        # to avoid returning password each time
        with OpenDB(db_name) as cursor:
            get_user_st = "SELECT * FROM users WHERE username=?"
            res = cursor.execute(get_user_st, (username,))
            row = res.fetchone()
            
            if row:
                return User(row[0], row[1], row[2], row[3], row[4])

    def add_user(self, user: User):
        with OpenDB(db_name) as cursor:            
            add_user_st = "INSERT INTO users VALUES (NULL, ?, ?, ?, ?)"
            cursor.execute(add_user_st, (user.username, user.first_name, user.last_name, user.password))

            get_user_id = "SELECT last_insert_rowid()"
            row_id = cursor.execute(get_user_id).fetchone()
            user.id = row_id[0]

            return user

    def delete_user(self, username: str):
        with OpenDB(db_name) as cursor:
            delete_user_st = "DELETE FROM users WHERE username=?"
            cursor.execute(delete_user_st, (username,))

    def get_all_users(self):
        with OpenDB(db_name) as cursor:
            get_all_st = "SELECT * FROM users"
            return [User(*row) for row in cursor.execute(get_all_st).fetchall()]


user_repo = UserRepo()
