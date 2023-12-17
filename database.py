import sqlite3


class Database:
    def __init__(self, name: str = "db.sqlite3") -> None:
        seconnection = sqlite3.connect(name)
        self.cursor = connection.cursor()

    def create_users_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users 
            (id INTEGER, username TEXT, first_name TEXT, telegram_id INTEGER,
            PRIMARY KEY ('id'))
            """
        )
        