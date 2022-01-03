import sqlite3

class OpenDB(object):
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, type, value, traceback):
        self.connection.commit()
        self.connection.close()
