from models import User
from repos import user_repo

class UserService:
    def get_user(self, username: str) -> User:
        return user_repo.get_user(username)

    def add_user(self, user: User):
        if self.get_user(user.username):
            raise ValueError("User with such username already exists")
        
        return user_repo.add_user(user)

    def delete_user(self, username: str):
        user_repo.delete_user(username)

    def get_all_users(self):
        return user_repo.get_all_users()


user_service = UserService()
