from repos import message_repo


class MessageService:
    def get_messages(self, chat_id):
        from services.chat_service import chat_service
        if not chat_service.get_chat_by_id(chat_id):
            raise ValueError(f"No chat with chat_id={chat_id}")
        
        return message_repo.get_messages(chat_id)

    def add_message(self, chat_id, user_from, message_text):
        message_repo.add_message(chat_id, user_from, message_text)

message_service = MessageService()
