import sqlite3

class Database:

    def __init__(self, database_pathname="setup/twitter.db"):
        self.connection = sqlite3.connect(database_pathname, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        if self.connection:
            if self.cursor:
                self.connection.commit()
                self.cursor.close()
            self.connection.close()