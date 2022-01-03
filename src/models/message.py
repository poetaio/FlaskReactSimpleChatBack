class Message:
    def __init__(self, message_id, chat_id, user_from, message):
        self.message_id = message_id
        self.chat_id = chat_id
        self.user_from = user_from
        self.message = message

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "chat_id": self.chat_id,
            "user_from": self.user_from,
            "message": self.message
        }
