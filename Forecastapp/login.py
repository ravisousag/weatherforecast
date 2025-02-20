import sqlite3

from user import User


class SytemLogin:
    def __init__(self, db_path="forecast.db"):
        self.__db_path = db_path
        self.__create_table_users()

    def __create_table_users(self):
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL
                )
                """
            )
            conn.commit()

    def insert_user(self, user: User):
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
                    (
                        user.name,
                        user.username,
                        user.password,
                    ),
                )
                conn.commit()
                return True
            except Exception as exc:
                conn.rollback()
                return exc

    def autentication(self, username, password):
        with sqlite3.connect(self.__db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (
                    username,
                    password,
                ),
            )
            result = cursor.fetchone()
            try:
                if result[2] == username and result[3] == password:
                    return True
            except Exception:
                return False
