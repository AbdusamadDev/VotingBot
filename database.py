import sqlite3


class Database:
    def __init__(self, name: str = "db.sqlite3") -> None:
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.create_users_table()
        self.create_teachers_table()

    def create_users_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users 
            (id INTEGER, username TEXT, first_name TEXT, telegram_id INTEGER,
            is_voted INTEGER, PRIMARY KEY ('id'))
            """
        )
        self.connection.commit()

    def create_teachers_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS teachers 
            (id INTEGER, fullname TEXT, school TEXT, number_of_votes INTEGER, 
            PRIMARY KEY ('id'))""",
        )
        for details in get_teachers_name():
            
        self.connection.commit()

    def add_user(self, username, first_name, telegram_id):
        self.cursor.execute(
            """INSERT INTO users 
            (username, first_name, telegram_id, is_voted) 
            VALUES (?, ?, ?, ?)""",
            (username, first_name, telegram_id, 0),
        )
        self.connection.commit()

    def voting(self, telegram_id, boolean, school):
        self.cursor.execute(
            """UPDATE users SET is_voted = ? WHERE telegram_id = ?;""",
            (boolean, telegram_id),
        )
        number_of_votes = self.cursor.execute(
            """SELECT number_of_votes FROM teachers WHERE school LIKE ?""",
            (school,),
        )
        if number_of_votes:
            number_of_votes = number_of_votes.fetchone()
        # self.cursor.execute(
        #     """UPDATE teachers SET number_of_votes = ? WHERE school = ?""", ()
        # )
        print(number_of_votes)
        self.connection.commit()


if __name__ == "__main__":
    database = Database()
    database.voting(2003049919, 1, "1 - maktab")
