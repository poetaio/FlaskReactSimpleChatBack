class User:
    def __init__(self, id, username, first_name, last_name, password):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        
    def to_dict(self):
        return {
            "username": self.username,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "password": self.password
        }