from flask_login import UserMixin
from db import get_db


class Teacher(UserMixin):
    def __init__(self, name, email, profile_pic, roleID):
        self.name = name
        self.id = email
        self.profile_pic = profile_pic
        self.role = roleID

    @staticmethod
    def get(user_email):
        db = get_db()
        user = db.execute(
            "SELECT * FROM teacher WHERE email = ?", (user_email,)
        ).fetchone()
        if not user:
            return None

        user = Teacher(
            name=user[0], email=user[1], profile_pic=user[2], roleID=user[3]
        )
        return user

    @staticmethod
    def create(name, email, profile_pic, roleID):
        db = get_db()
        db.execute(
            "INSERT INTO teacher (name, email, profile_pic, role)"
            " VALUES (?, ?, ?, ?)",
            (name, email, profile_pic, roleID),
        )
        db.commit()

    @staticmethod
    def get_all():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM teacher",
        )
        users = cur.fetchall()
        if not users:
            return None
        users = [item for user in users for item in user]
        cur.close()
        return users

    def create_table_with_data():
        db = get_db()
        cur = db.cursor()
        data = [
            ("Flask_teacher_1", "flaskapptest@gmail.com",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "teacher"),
            ("Flask_teacher_2", "flaskapptest222@gmail.com",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "teacher"),
            ("teacher1", "1",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "teacher"),
            ("teacher2", "2",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "teacher")
        ]
        cur.executemany(
            "INSERT OR REPLACE INTO teacher VALUES(?, ?, ?, ?)", data)
        db.commit()
        cur.close()
