from flask_login import UserMixin
from db import get_db
from datetime import datetime, timedelta, date
from operator import itemgetter
from itertools import groupby


class Lesson(UserMixin):
    def __init__(self, teacherEmail, studentEmail, date_of_lesson, themeName, link, note, passed):
        self.teacher_email = teacherEmail
        self.student_email = studentEmail
        self.lesDate = date_of_lesson
        self.theme_name = themeName
        self.link = link
        self.note = note
        self.passed = passed

    @staticmethod
    def get(teacher_email, date):
        db = get_db()
        lesson = db.execute("""
            SELECT *
            FROM lesson
            WHERE (teacher_email = ? AND lesDate = ?)""", (teacher_email, date, )
        ).fetchone()
        if not lesson:
            return None
        lesson = Lesson(
            teacherEmail=lesson[0], studentEmail=lesson[1], date_of_lesson=lesson[2], themeName=lesson[3], link=lesson[4], note=lesson[5], passed=lesson[6]
        )
        return lesson

    
    # def print_info_for_one_lesson(teacher_id, date):
    #     db = get_db()
    #     lesson = db.execute("""
    #         SELECT teacher.name, student.name, lesson.lesDate, theme.name, lesson.link
    #         FROM lesson, teacher, student, theme
    #         WHERE (teacher.id = lesson.teacher_id AND
    #             student.id = lesson.student_id AND theme.name = lesson.theme_name AND 
    #             teacher.id = ? AND lesson.lesDate = ?)""", (teacher_id, date, )
    #     ).fetchone()
    #     if not lesson:
    #         return None
    #     lesson = [item for item in lesson]
    #     return lesson

    @staticmethod
    def create(teacherEmail, studentEmail, data_of_lesson, link):
        themeName = "Без темы"
        note = ""
        passed = "No"

        db = get_db()
        db.execute(
            "INSERT INTO lesson (teacher_email, student_email, lesDate, theme_name, link, note, passed)"
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (teacherEmail, studentEmail, data_of_lesson, themeName, link, note, passed),
        )
        db.commit()

    def create_table_lessons_with_data():
        db = get_db()
        cur = db.cursor()
        data = [
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-30 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "No"),
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-29 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "No"),
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-28 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "No"),
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-27 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "No"),
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-26 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "No"),
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-25 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "No"),
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-23 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "No"),
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-22 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "No"),
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-21 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "No"),
            ("flaskapptest22@gmail.com", "flaskapptest1@gmail.com",
             "2020-12-20 10:58", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "Yes"),
            ("flaskapptest22@gmail.com", "flaskapptest22std@gmail.com",
             "2023-01-18 18:00", "Без темы", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "Yes"),
             ("flaskapptest22@gmail.com", "flaskapptest22std@gmail.com",
             "2023-01-18 18:00", "Present Simple Tense", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "Yes"),
             ("flaskapptest22@gmail.com", "flaskapptest22std@gmail.com",
             "2023-01-18 18:00", "lalalal", "https://python-school.ru/blog/sqlite-database-in-python-2/", "", "Yes")
        ]
        cur.executemany(
            "INSERT OR REPLACE INTO lesson VALUES(?, ?, ?, ?, ?, ?, ?)", data)
        db.commit()
        cur.close()

    def get_all_lessons(teacher_email):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM lesson WHERE teacher_email = ? AND passed = 'No'", (teacher_email,))
        lessons = cur.fetchall()
        if not lessons:
            return None
        lessons = [tuple(les) for les in lessons] #[[item for item in lesson] for lesson in lessons ]
        cur.close()
        return lessons

    def get_lessons_for_a_specific_teacher(teacher_email):
        db = get_db()
        lesson = db.execute("""
            SELECT student.name, lesDate, theme.name, passed 
            FROM teacher, student, lesson, theme
            WHERE (teacher.email = lesson.teacher_email AND
                student.email = lesson.student_email AND theme.name = lesson.theme_name AND teacher.email = ?)
        """, (teacher_email, )).fetchall()
        if not lesson:
            return None
        # lesson.sort(key=itemgetter(0))
        # y = groupby(lesson, itemgetter(0))
        list_les = [[item for item in les] for les in lesson] #
        return list_les

    def get_lessons_for_a_specific_student(student_email):
        db = get_db()
        lesson = db.execute("""
            SELECT teacher.name, lesDate, theme.name, passed 
            FROM teacher, student, lesson, theme
            WHERE (teacher.email = lesson.teacher_email AND
                student.email = lesson.student_email AND theme.name = lesson.theme_name AND student.email = ?)
        """, (student_email, )).fetchall()
        if not lesson:
            return None
        les = [[item for item in les] for les in lesson]
        return les

    def get_list_of_lessons_for_student_and_teacher_with_themes(teacher_email, student_email):
        db = get_db()
        lesson = db.execute("""
            SELECT lesson.lesDate, theme.name, passed
            FROM teacher, student, lesson, theme
            WHERE (teacher.email = lesson.teacher_email AND
                student.email = lesson.student_email AND theme.name = lesson.theme_name AND 
                teacher.email = ? AND student.email = ? AND passed = "No")
        """, (teacher_email, student_email, )).fetchall()
        if not lesson:
            return None

        lesson = [[item for item in les] for les in lesson ]
        return lesson

    # def get_list_of_lessons_for_student_and_teacher(teacher_email, student_email):
    #     db = get_db()
    #     lesson = db.execute("""
    #         SELECT lesson.lesDate
    #         FROM teacher, student, lesson, theme
    #         WHERE (teacher.email = lesson.teacher_email AND
    #             student.email = lesson.student_email AND theme.name = lesson.theme_name AND 
    #             teacher.email = ? AND student.email = ?)
    #     """, (teacher_email, student_email, )).fetchall()
    #     if not lesson:
    #         return None

    #     lesson = [item  for les in lesson for item in les]
    #     return lesson

    def change_student(teacher_email, date, std):
        db = get_db()
        db.execute(
            "UPDATE lesson SET student_email = ? WHERE teacher_email = ? AND lesDate = ?",
            (std, teacher_email, date,),
        )
        db.commit()

    def change_date(teacher_email, date_before, date_after):
        db = get_db()
        db.execute(
            "UPDATE lesson SET lesDate = ? WHERE teacher_email = ? AND lesDate = ?",
            (date_after, teacher_email, date_before,),
        )
        db.commit()

    def change_theme(teacher_email, date, theme):
        db = get_db()
        db.execute(
            "UPDATE lesson SET theme_name = ? WHERE teacher_email = ? AND lesDate = ?",
            (theme, teacher_email, date,),
        )
        db.commit()

    def change_note(teacher_email, date, note):
        db = get_db()
        db.execute(
            "UPDATE lesson SET note = ? WHERE teacher_email = ? AND lesDate = ?",
            (note, teacher_email, date,),
        )
        db.commit()

    def delete_lesson(teacher_email, date):
        db = get_db()
        db.execute("""
            DELETE FROM lesson WHERE teacher_email = ? AND lesDate = ?
        """, (teacher_email, date, ))
        db.commit()

    def delete_all_lessons_with_this_student(teacher_email, student_email):
        db = get_db()
        db.execute("""
            DELETE FROM lesson WHERE teacher_email = ? AND student_email = ?
        """, (teacher_email, student_email, ))
        db.commit()

    def make_lesson_passed(teacher_email, date):
        db = get_db()
        db.execute(
            "UPDATE lesson SET passed = 'Yes' WHERE teacher_email = ? AND lesDate = ?",
            (teacher_email, date,),
        )
        db.commit()

    def list_future_lessons_for_teacher(teacher_id):
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT student.name, lesDate, theme.name
            FROM teacher, student, lesson, theme, teacher_students
            WHERE (teacher.email = teacher_students.teacher_email AND teacher_students.teacher_email = lesson.teacher_email AND 
                student.email = teacher_students.student_email AND teacher_students.student_email = lesson.student_email AND 
                passed = "No" AND theme.name = lesson.theme_name AND teacher.email = ?)
        """, (teacher_id, ))
        lessons = cur.fetchall()
        
        # print("lessons: ", [tuple(les) for les in lessons]) #{tuple(les) for les in lessons}
        # print(lessons)
        # print(tuple(lessons))
        # print([tuple(les)[1] for les in lessons])
        list_les =  [tuple(les) for les in lessons] #[item for les in lessons for item in les]
        print(list_les)
        # lessons = []
        # lessons.append(db.execute("""
        #     SELECT student.name, lesDate, theme.name, passed 
        #     FROM teacher, student, lesson, theme
        #     WHERE (teacher.email = lesson.teacher_email AND student.email = lesson.student_email AND 
        #     passed = "No" AND theme.name = lesson.theme_name AND teacher.email = ?)
        # """, (teacher_id, )).fetchall()[0]) 
        # list_les = [[item for item in les] for les in lessons] # 
        if not lessons:
            return None
        cur.close()
        return lessons
        # lessons = Lesson.get_lessons_for_a_specific_teacher(teacher_id)
        # res = []
        # if lessons:
        #     for les in lessons:
        #         if les[3] == "No":
        #             res.append(les) #[[les1][les2]] = [[std, date, theme, passed - 1], [std, date, theme, passed - 2]]
        # if not res:
        #     return None
        # res = [les for les in res]
        # return res

    def list_future_lessons_for_std(student_id):
        lessons = Lesson.get_lessons_for_a_specific_student(student_id)
        res = []
        if lessons:
            for les in lessons:
                if les[3] == "No":
                    res.append(les)
        if not res:
            return None
        return res

    def list_passed_lessons_for_teacher(teacher_id):
        lessons = Lesson.get_lessons_for_a_specific_teacher(teacher_id)
        res = []
        if lessons:
            for les in lessons:
                if les[3] == "Yes":
                    res.append(les)
        if not res:
            return None
        return res

    def list_passed_lessons_for_std(student_id):
        lessons = Lesson.get_lessons_for_a_specific_student(student_id)
        res = []
        if lessons:
            for les in lessons:
                if les[3] == "Yes":
                    res.append(les)
        if not res:
            return None
        return res

    def auto_check_passed_lessons():
        now = datetime.now()
        time_change = timedelta(minutes=60)
        # now_plus_lesson = now + time_change
        # print(now_plus_lesson)
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT email FROM teacher",
        )
        teachers = cur.fetchall()
        teachers = [teach for teacher in teachers for teach in teacher]
        cur.close()
        for teacher in teachers:
            lessons = Lesson.get_lessons_for_a_specific_teacher(teacher)
            if lessons:
                for lesson in lessons:
                    les = datetime.strptime(lesson[1], '%Y-%m-%d %H:%M')
                    les_plus_hour = les + time_change
                    if now > les_plus_hour:
                        Lesson.make_lesson_passed(teacher, lesson[1])
        db.commit()

    def get_todays_lessons_teacher(teacher_id):
        today = str(date.today())
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT student.name, lesDate, theme.name
            FROM teacher, student, lesson, theme, teacher_students
            WHERE (teacher.email = teacher_students.teacher_email AND teacher_students.teacher_email = lesson.teacher_email AND 
                student.email = teacher_students.student_email AND teacher_students.student_email = lesson.student_email AND 
                passed = "No" AND theme.name = lesson.theme_name AND teacher.email = ? AND lesDate LIKE ?)
        """, (teacher_id, '%'+today+'%', ))
        lessons = cur.fetchall()
        list_les =  [tuple(les) for les in lessons] 
        if not lessons:
            return None
        cur.close()
        return lessons
    
    def get_todays_lessons_student(student_id):
        today = str(date.today())
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT teacher.name, lesDate, theme.name, teacher.email
            FROM teacher, student, lesson, theme, teacher_students
            WHERE (teacher.email = teacher_students.teacher_email AND teacher_students.teacher_email = lesson.teacher_email AND 
                student.email = teacher_students.student_email AND teacher_students.student_email = lesson.student_email AND 
                passed = "No" AND theme.name = lesson.theme_name AND student.email = ? AND lesDate LIKE ?)
        """, (student_id, '%'+today+'%', ))
        lessons = cur.fetchall()
        list_les =  [tuple(les) for les in lessons] 
        if not lessons:
            return None
        cur.close()
        return lessons



