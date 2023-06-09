from flask_login import UserMixin
from db import get_db


class Teacher_Students(UserMixin):
    def __init__(self, teacher_email, student_email):
        self.teacherEmail = teacher_email
        self.studentEmail = student_email

    @staticmethod
    def create(teacher_email, student_email):
        db = get_db()
        db.execute(
            "INSERT INTO teacher_students (teacher_email, student_email)"
            " VALUES (?, ?)",
            (teacher_email, student_email),
        )
        db.commit()

    def get(teacher_email, student_email):
        db = get_db()
        couple = db.execute(
            "SELECT * FROM teacher_students WHERE teacher_email = ? AND student_email = ?", (teacher_email, student_email,)
        ).fetchone()
        if not couple:
            return None

        couple = Teacher_Students(
            teacher_email=couple[0], student_email=couple[1]
        )
        return couple

    def get_students_of_this_teacher(teacher_email):
        db = get_db()
        cur = db.cursor()
        students = cur.execute("""
            SELECT student.name, student.email
            FROM teacher, student, teacher_students
            WHERE (teacher.email = teacher_students.teacher_email AND
                student.email = teacher_students.student_email AND teacher.email = ?)
        """, (teacher_email, )).fetchall()
        students = [[item for item in student] for student in students]
        if not students:
            return None
        cur.close()
        return students

    def get_teachers_of_this_student(student_email):
        db = get_db()
        cur = db.cursor()
        teachers = cur.execute("""
            SELECT teacher.name, teacher.email
            FROM teacher, student, teacher_students
            WHERE (teacher.email = teacher_students.teacher_email AND
                student.email = teacher_students.student_email AND student.email = ?)
        """, (student_email, )).fetchall()
        teachers = [[item for item in teacher] for teacher in teachers]
        if not teachers:
            return None
        cur.close()
        return teachers

    def create_table_with_data():
        db = get_db()
        cur = db.cursor()
        data = [
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com"),
            ("flaskapptest22@gmail.com", "flaskapptest2@gmail.com"),
            ("flaskapptest22@gmail.com", "flaskapptest3@gmail.com"),
            ("flaskapptest@gmail.com", "flaskapptest22std@gmail.com"),
            ("flaskapptest22@gmail.com", "flaskapptest22std@gmail.com")
        ]
        cur.executemany("INSERT OR REPLACE INTO teacher_students VALUES(?, ?)", data)
        db.commit()
        cur.close()

    def delete_student(teacher_email, student_email):
        db = get_db()
        db.execute("""
            DELETE FROM teacher_students WHERE teacher_email = ? AND student_email = ?
        """, (teacher_email, student_email, ))
        db.commit()

