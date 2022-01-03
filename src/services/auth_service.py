from repos import user_repo
from models import AuthUser

class AuthService:
    def login(self, auth_user: AuthUser):
        user = user_repo.get_user(auth_user.username)
        print(user.username, user.password)
        if not user:
            return False
            # raise ValueError("No such user")
        
        if auth_user.password != user.password:
            return False
            # raise ValueError("Incorrect password")
        
        return True

    def register(self):
        pass


auth_service = AuthService()
