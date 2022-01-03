from repos import chat_repo
from models import Chat

class ChatService:
    def get_chat_by_id(self, chat_id) -> Chat:
        return chat_repo.get_chat_by_id(chat_id)
    
    def get_chat(self, user_1, user_2) -> Chat:
        if (user_1 == user_2):
            raise ValueError("Circular chat!!!")

        users_tuple = (user_1, user_2) if user_1 < user_2 else (user_2, user_1)

        # TODO: avoid creating chat but throw error instead
        chat = Chat(None, *users_tuple)
        res_chat = chat_repo.get_chat(chat)
        if not res_chat:
            res_chat = chat_repo.add_chat(chat)

        return res_chat

    def get_all(self):
        return chat_repo.get_all()


chat_service = ChatService()
