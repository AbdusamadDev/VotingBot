import sqlite3

from utils import get_teachers_name


class Database:
    def __init__(self, name: str = "../db.sqlite3") -> None:
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.create_users_table()
        self.create_teachers_table()

    def create_users_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users 
            (id INTEGER, username TEXT, first_name TEXT, telegram_id INTEGER UNIQUE,
            is_voted INTEGER, PRIMARY KEY ('id'))
            """
        )
        self.connection.commit()

    def create_teachers_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS teachers 
            (id INTEGER, fullname TEXT, school TEXT UNIQUE, number_of_votes INTEGER, 
            PRIMARY KEY ('id'))""",
        )
        for school, name in get_teachers_name().items():
            try:
                self.cursor.execute(
                    """INSERT INTO teachers (fullname, school, number_of_votes) 
                    VALUES (?, ?, ?)""",
                    (name, school, 0),
                )
            except sqlite3.IntegrityError:
                continue
        self.connection.commit()

    def add_user(self, username, first_name, telegram_id):
        try:
            self.cursor.execute(
                """INSERT INTO users 
                (username, first_name, telegram_id, is_voted) 
                VALUES (?, ?, ?, ?)""",
                (username, first_name, telegram_id, 0),
            )
        except sqlite3.IntegrityError:
            pass
        self.connection.commit()

    def voting(self, telegram_id, school):
        self.cursor.execute(
            """UPDATE users SET is_voted = 1 WHERE telegram_id = ?;""",
            (telegram_id,),
        )
        number_of_votes = self.cursor.execute(
            """SELECT number_of_votes FROM teachers WHERE school LIKE ?""",
            (school,),
        )
        if number_of_votes and number_of_votes is not None:
            number_of_votes = number_of_votes.fetchone()[0]
        self.cursor.execute(
            """UPDATE teachers SET number_of_votes = ? WHERE school LIKE ?""",
            (number_of_votes + 1, school),
        )
        print(number_of_votes)
        self.connection.commit()

    def is_already_voted(self, telegram_id):
        voted = self.cursor.execute(
            """SELECT is_voted FROM users WHERE telegram_id=?""", (telegram_id,)
        ).fetchone()
        if voted == () or voted is None or len(voted) == 0:
            return False
        return bool(voted[0])

    def get_user_id(self, username):
        user = self.cursor.execute(
            """SELECT telegram_id FROM users WHERE username=?""",
            (username,),
        ).fetchone()
        return user[0] if user else 0

    def get_usernames(self):
        users = self.cursor.execute("""SELECT username FROM users;""")
        return (
            [(user[0], index) for index, user in enumerate(users, start=1)]
            if users
            else []
        )


if __name__ == "__main__":
    database = Database()
    for i in range(20):
        database.add_user(
            "User " + str(i), first_name="Firstname " + str(i), telegram_id=i
        )
    print(database.get_usernames())
