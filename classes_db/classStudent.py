from flask_login import UserMixin
from db import get_db


class Student(UserMixin):
    def __init__(self, name, email, profile_pic, roleID):
        self.name = name
        self.id = email
        self.profile_pic = profile_pic
        self.role = roleID

    @staticmethod
    def get(user_email):
        db = get_db()
        user = db.execute(
            "SELECT * FROM student WHERE email = ?", (user_email,)
        ).fetchone()
        if not user:
            return None
        user = Student(
            name=user[0], email=user[1], profile_pic=user[2], roleID=user[3]
        )
        return user

    @staticmethod
    def create(name, email, profile_pic, roleID):
        db = get_db()
        db.execute(
            "INSERT INTO student (name, email, profile_pic, role)"
            " VALUES (?, ?, ?, ?)",
            (name, email, profile_pic, roleID),
        )
        db.commit()

    @staticmethod
    def get_all():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM student",
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
            ("student_1", "flaskapptest1@gmail.com",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "student"),
            ("student_2", "flaskapptest2@gmail.com",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "student"),
            ("student_3", "flaskapptest3@gmail.com",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "student"),
            ("student_4", "flaskapptest4@gmail.com",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "student"),
            ("student_5", "flaskapptest5@gmail.com",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "student"),
            ("student_6", "flaskapptest6@gmail.com",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "student"),
            ("student_7", "flaskapptest7@gmail.com",
             "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c", "student")

        ]
        cur.executemany(
            "INSERT OR REPLACE INTO student VALUES(?, ?, ?, ?)", data)
        db.commit()
        cur.close()

    def get_list_of_all_students():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT name, email FROM student",
        )
        users = cur.fetchall()
        if not users:
            return None
        users = [[item for item in user] for user in users ]
        cur.close()
        return users

    # def get_email_by_name(student_name):
    #     db = get_db()
    #     cur = db.cursor()
    #     cur.execute("SELECT email FROM student WHERE name = ?", (student_name, ))
    #     student_email_ = cur.fetchone()[0]
    #     cur.close()
    #     return student_email_
