from flask_login import UserMixin
from db import get_db


class Email_Password(UserMixin):
    def __init__(self, email, password, roleID):
        self.email = email
        self.password = password
        self.role = roleID

    @staticmethod
    def get(email):
        db = get_db()
        user = db.execute(
            "SELECT * FROM email_password WHERE email = ?", (email,)
        ).fetchone()
        if not user:
            return None

        user = Email_Password(
            email=user[0], password=user[1], roleID=user[2]
        )
        return user

    @staticmethod
    def create(email, password, roleID):
        db = get_db()
        db.execute(
            "INSERT INTO email_password (email, password, role)"
            "VALUES (?, ?, ?)",
            (email, password, roleID),
        )
        db.commit()

    @staticmethod
    def get_all():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM email_password",
        )
        users = cur.fetchall()
        if not users:
            return None
        users = [[item for item in user] for user in users ]
        cur.close()
        return users

    def create_table_with_data():
        db = get_db()
        cur = db.cursor()
        data = [
            ("1", "111", "teacher"),
            ("2", "2", "teacher")
        ]
        cur.executemany(
            "INSERT OR REPLACE INTO email_password VALUES(?, ?, ?)", data)
        db.commit()
        cur.close()
