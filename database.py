import sqlite3


class Database:
    def __init__(self, name: str = "db.sqlite3") -> None:
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.create_users_table()

    def create_users_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users 
            (id INTEGER, username TEXT, first_name TEXT, telegram_id INTEGER,
            is_voted INTEGER, PRIMARY KEY ('id'))
            """
        )
        self.connection.commit()

    def add_user(self, username, first_name, telegram_id):
        self.cursor.execute(
            """INSERT INTO users 
            (username, first_name, telegram_id, is_voted) 
            VALUES (?, ?, ?, ?)""",
            (username, first_name, telegram_id, 0),
        )
        self.connection.commit()

    def voting(self, telegram_id):
        self.cursor.execute(
            """UPDATE users SET is_voted = 1 WHERE telegram_id = ?;""",
            (telegram_id,),
        )
        self.connection.commit()
