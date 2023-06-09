from flask_login import UserMixin
from db import get_db


class Theme(UserMixin):
    def __init__(self, name, teacher_email, materials, homework):
        self.name = name
        self.teacherEmail = teacher_email
        self.materials = materials
        self.homework = homework

    @staticmethod
    def get(teacheremail, name):
        db = get_db()
        theme = db.execute(
            "SELECT * FROM theme WHERE teacher_email = ? AND name = ?", (teacheremail, name)
        ).fetchone()
        if not theme:
            return None
        theme = Theme(
            name=theme[0], teacher_email=theme[1], materials=theme[2], homework=theme[3]
        )
        return theme

    @staticmethod
    def create(teacheremail, name, materials, homework):
        db = get_db()
        db.execute(
            "INSERT INTO theme (name, teacher_email, materials, homework)"
            "VALUES (?, ?, ?, ?)",
            (name, teacheremail, materials, homework),
        )
        db.commit() 

    # def get_themes(teacher_email):
    #     db = get_db()
    #     cur = db.cursor()
    #     cur.execute(
    #         "SELECT name, materials, homework FROM theme WHERE teacher_email = ?", (teacher_email,)
    #     )
    #     themes = cur.fetchall()
    #     if not themes:
    #         return None
    #     themes = [[item for item in theme] for theme in themes] #[[item] for theme in themes for item in theme]
    #     cur.close()
    #     return themes       

    def get_names(teacher_email):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT name, materials, homework FROM theme WHERE teacher_email = ?", (teacher_email,)
        )
        themes = cur.fetchall()
        if not themes:
            return None
        themes = [[item for item in theme] for theme in themes] #[[item] for theme in themes for item in theme]
        cur.close()
        return themes

    def create_table_with_data():
        db = get_db()
        cur = db.cursor()
        data = [
            ("theme_1", "flaskapptest22@gmail.com", "fail", "homework"), 
            ("theme_2", "flaskapptest22@gmail.com", "", ""), 
            ("theme_3", "flaskapptest22@gmail.com", "", ""), 
            ("theme_4", "flaskapptest22@gmail.com", "", ""), 
            ("theme_5", "flaskapptest22@gmail.com", "", ""), 
            ("theme_6", "flaskapptest22@gmail.com", "", ""), 
            ("theme_7", "flaskapptest22@gmail.com", "", ""), 
            ("theme_8", "flaskapptest22@gmail.com", "", ""), 
            ("theme_9", "flaskapptest22@gmail.com", "", ""), 
            ("theme_11", "flaskapptest22@gmail.com", "", ""), 
            ("Без темы", "flaskapptest22@gmail.com", "", ""),
            ("Без темы", "flaskapptest@gmail.com", "", ""),
            ("Без темы", "flaskapptest222@gmail.com", "", ""),
            ("Без темы", "1", "", ""),
            ("Без темы", "2", "", "")
        ]
        cur.executemany(
            "INSERT OR REPLACE INTO theme(name, teacher_email) VALUES(?, ?)", data)
        db.commit()
        cur.close()
    
    def get_all():
        db = get_db()
        themes = db.execute(
            "SELECT * FROM theme",
        ).fetchall()
        if not themes:
            return None
        themes = [thm for theme in themes for thm in theme]
        return themes

    # def add_theme(teacher_email, date, theme):
    #     db = get_db()
    #     db.execute(
    #         "UPDATE lesson SET theme_name = ? WHERE teacher_email = ? AND lesDate = ?",
    #         (theme, teacher_email, date,),
    #     )
    #     db.commit()

    def change_name(teacheremail, name, new_name):
        db = get_db()
        db.execute(
            "UPDATE theme SET name = ? WHERE teacher_email = ? AND name = ?",
            (new_name, teacheremail, name),
        )
        db.commit() 

    def change_materials(teacheremail, name, new_materials):
        db = get_db()
        db.execute(
            "UPDATE theme SET materials = ? WHERE teacher_email = ? AND name = ?",
            (new_materials, teacheremail, name),
        )
        db.commit()

    def change_homework(teacheremail, name, new_homework):
        db = get_db()
        db.execute(
            "UPDATE theme SET homework = ? WHERE teacher_email = ? AND name = ?",
            (new_homework, teacheremail, name),
        )
        db.commit()

    def del_theme(teacheremail, name):
        db = get_db()
        db.execute(
            "DELETE FROM theme WHERE teacher_email = ? AND name = ?",
            (teacheremail, name),
        )
        db.commit()

