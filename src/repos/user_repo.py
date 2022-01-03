from . import OpenDB
from config import db_name
from models import User

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
            if self.get_user(user.username):
                raise ValueError("user with such username already exists")
            
            add_user_st = "INSERT INTO users VALUES (NULL, ?, ?, ?, ?)"
            cursor.execute(add_user_st, (user.username, user.first_name, user.last_name, user.password))

user_repo = UserRepo()
