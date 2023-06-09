import json
import os
import sqlite3
from flask import Flask, redirect, request, url_for, render_template, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from db import init_db_command
from classes_db.classTeacher import Teacher
from classes_db.classStudent import Student
from classes_db.classTeacherStudent import Teacher_Students
from classes_db.classTheme import Theme
from classes_db.classLesson import Lesson
# from user_role import User_role
from classes_db.classEmailPassword import Email_Password

import teachers_functional
import logging
import datetime
import calendar
from werkzeug.security import generate_password_hash, check_password_hash


# Flask App
# set GOOGLE_CLIENT_SECRET=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
# set GOOGLE_CLIENT_ID=120996757294-0tiqc5bhgoqn0pm78o00t8tcluq5s9uo.apps.googleusercontent.com

GOOGLE_CLIENT_ID = "120996757294-0tiqc5bhgoqn0pm78o00t8tcluq5s9uo.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

# new (Flask App 2)
# GOOGLE_CLIENT_ID = "120996757294-mfpmb1nlpelhqqjt611gpkon4t0ojcta.apps.googleusercontent.com"
# GOOGLE_CLIENT_SECRET = "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"

# Configuration
# GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
# GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.register_blueprint(teachers_functional.bp)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


# -------------------------GOOGLE-AUTHORIZATION------------------------------------
# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
# login_manager.login_view = 'login'  # ? добавленная мной строка
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass
except:
    pass


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    if Teacher.get(user_id):
        return Teacher.get(user_id)
    elif Student.get(user_id):
        return Student.get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():

    if current_user.is_authenticated:
        
        Teacher.create_table_with_data()
        Student.create_table_with_data()
        Teacher_Students.create_table_with_data()
        Lesson.create_table_lessons_with_data()
        Lesson.auto_check_passed_lessons()
        # Theme.create_table_with_data()

        if current_user.role == 'teacher':
            # return (render_template('user_page_teacher.html', user_name=current_user.name).format(
            #     current_user.role, current_user.name, current_user.id, current_user.profile_pic
            # )) 
            # return(render_template("index2.html"))
            now = datetime.datetime.now()
            print(now, calendar.day_name[now.weekday()], datetime.date.today())
            # print([tuple(lesson) for lesson in Lesson.get_todays_lessons(current_user.id)])
            todays_lessons = Lesson.get_todays_lessons_teacher(current_user.id)
            if todays_lessons:
                todays_lessons = [tuple(lesson) for lesson in todays_lessons]
            return render_template('user_page_teacher.html', date=datetime.date.today(), day_of_week=calendar.day_name[now.weekday()], t_lessons=todays_lessons) #('start_teacher_page.html')

        if current_user.role == 'student':
            list_of_teachers = Teacher_Students.get_teachers_of_this_student(current_user.id)
            list_of_lessons = Lesson.get_lessons_for_a_specific_student(current_user.id)
                                    
            i = 0
            if list_of_teachers and list_of_lessons:
                for teacher in list_of_teachers:
                    for one_lesson in list_of_lessons:
                        if teacher[0] == one_lesson[0] and one_lesson[3] != "Yes":
                            i = i+1
                    if i > 0:
                        i = 0
                    else:
                        mes = "С ним пока нет уроков. Подождите, пока учитель выставит уроки или напомните ему об этом"
                        list_of_lessons.append([teacher[0], mes])
            pas_les = Lesson.list_passed_lessons_for_std(current_user.id)
            # return (render_template('user_page_student.html', teachers=list_of_teachers, lessons=list_of_lessons,  passed_les=pas_les).format(
            #     current_user.role, current_user.name, current_user.id, current_user.profile_pic
            # ))
            now = datetime.datetime.now()
            todays_lessons = Lesson.get_todays_lessons_student(current_user.id)
            if todays_lessons:
                todays_lessons = [tuple(lesson) for lesson in todays_lessons]
            return (render_template('user_page_student.html', teachers=list_of_teachers, date=datetime.date.today(), day_of_week=calendar.day_name[now.weekday()], t_lessons=todays_lessons))
    else:
        Lesson.auto_check_passed_lessons()

        # если регистрировать гугловскую почту через форму регистрации, то потом можно будет заходить и с помощью логина-пароля
        # и с помощью гугла
        # если регистрироваться через кнопку "войти с помощью гугла", то вход потом только через эту кнопку
        # (через пароль-логин не пустит)

        Email_Password.create_table_with_data()
        if request.method == 'POST':
            Email = request.form.get('Email')  # get data from front
            Password = request.form.get('Password')  # get data from front
           
            if not Email_Password.get(Email):
                return render_template('index.html', bad_auth = "Не зарегистрирован аккаунт с таким логином") # выскакивает надпись, если такого логина нет в БД
            else:
                log = Email_Password.get(Email).email
                hash = Email_Password.get(Email).password
                roleID = Email_Password.get(Email).role

            if not check_password_hash(hash, Password):
                return render_template('index.html', bad_auth = "Неверный логин или пароль") # выскакивает надпись, если такой пары нет в БД

            if roleID == "student":
                user = Student.get(Email)

            if roleID == "teacher":
                user = Teacher.get(Email)
            login_user(user)
            return redirect(url_for("index"))

        return render_template('index.html', bad_auth="")


@app.route("/login")
def login():
    # Find out what URL to hit for Google login

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    if Email_Password.get(users_email):
        role = Email_Password.get(users_email).role

        # Create a user in our db with the information provided
        # by Google
        if role == "teacher":
            user = Teacher(
                name=users_name, email=users_email, profile_pic=picture, roleID=role
            )
        if role == "student":
            user = Student(
                name=users_name, email=users_email, profile_pic=picture, roleID=role
            )
        # Begin user session by logging the user in
        login_user(user)
    else:
        return render_template('index.html', bad_auth="Вы еще не зарегистрированы")

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# -------------------------END-OF-GOOGLE-AUTHORIZATION------------------------------------

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
    if request.method == 'POST':
        Email = request.form.get('Email')
        Password = request.form.get('Password')
        hash = generate_password_hash(Password)
        Role = request.form.get('Role')
        name = request.form.get('Name')
        pic = "https://lh3.googleusercontent.com/a/AEdFTp6JHTykq5NLGHzDv9Hs_n0ZrkfimhDa2m2E0WEr=s96-c"

        if not Email_Password.get(Email):
            Email_Password.create(Email, hash, Role)
        else:
            return render_template('registration.html', bad_auth = "Email is already used")

        if Role == "student":
            user = Student(
            name=name, email=Email, profile_pic=pic, roleID=Role
        )
            if not Student.get(Email) and not Teacher.get(Email):
                Student.create(name, Email, pic, Role)
            else: 
                return render_template('registration.html', bad_auth = "Email is already used")

        if Role == "teacher":
            user = Teacher(
            name=name, email=Email, profile_pic=pic, roleID=Role
        )
            if not Teacher.get(Email) and not Student.get(Email):
                Teacher.create(name, Email, pic, Role)
                Theme.create(Email, "No theme", "--", "--")
            else: 
                return render_template('registration.html', bad_auth = "Email is already used")

        login_user(user)
        return redirect(url_for("index"))
        # return render_template('successregis.html')
    return render_template('registration.html', bad_auth = "")

# **************************---------FOR-STUDENT---------*********************************

@app.route("/page_teacher")
def page_teacher():
    teacher_email = request.args.get("Teach_email", None)
    # ДУМАЛА ПОФИКСИТЬ, НО НЕ ПОНИМАЮ УСЛОВИЯ ВОЗНИКНОВЕНИЯ ЭТОГО ИСКЛЮЧЕНИЯ:
    #   если нет студента такого то вывести сообщение, что его нет в базе 
    return (render_template('page_for_any_teacher.html').format(
            Teacher.get(teacher_email).role, Teacher.get(teacher_email).name, Teacher.get(teacher_email).id, Teacher.get(teacher_email).profile_pic
        ))

@app.route("/go_to_the_lesson", methods=['GET', 'POST'])
def go_to_the_lesson():
    if current_user.role == "student":
        teach_email = request.args.get("Teach_email", None)
    else:
        teach_email = current_user.id
    date = request.args.get("Date", None)
    note = Lesson.get(teach_email, date).note
    print("before: ", note)
    link = Lesson.get(teach_email, date).link
    if request.method == 'POST':
        notes = request.form.get('les_notes')
        print("after: ", notes)
        Lesson.change_note(teach_email, date, notes)
        print("after: ", notes)
        # Lesson.make_lesson_passed(teach_email, date)
        return redirect(url_for('index'))
    note = Lesson.get(teach_email, date).note
    return (render_template('go_to_the_lesson.html', link=link, note=note))

# @app.route('/upd_notes', methods = ['POST'])
# def upd_notes():
#     if current_user.role == "student":
#         teach_email = request.args.get("Teach_email", None)
#     else:
#         teach_email = current_user.id
#     date = request.args.get("Date", None)
#     note = Lesson.get(teach_email, date).note
#     if request.method == 'POST':
#         new_note = request.form.get('les_notes')

#     return (render_template('go_to_the_lesson.html', ))

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    app.logger.info(jsdata)
    if current_user.role == "student":
        teach_email = request.args.get("Teach_email", None)
    else:
        teach_email = current_user.id
    date = request.args.get("Date", None)
    Lesson.change_note(teach_email, date, jsdata)
    return json.loads(jsdata)[0]

@app.route("/passed_lessons_for_std")
def passed_lessons_for_std():
    list_of_teachers = Teacher_Students.get_teachers_of_this_student(current_user.id)
    list_of_passed_lessons = Lesson.list_passed_lessons_for_std(current_user.id)
    teachers = []
    if list_of_teachers and list_of_passed_lessons: 
        for student in list_of_teachers:
            for one_lesson in list_of_passed_lessons:
                if student[0] == one_lesson[0] and one_lesson[3] == "Yes":
                    teachers.append(student)
                    break

    return render_template('passed_lessons_for_std.html', teachers=list_of_teachers, lessons=list_of_passed_lessons)


@app.route("/les_materials")
def les_materials():
    list_of_teachers = Teacher_Students.get_teachers_of_this_student(current_user.id)
    list_of_passed_lessons = Lesson.list_passed_lessons_for_std(current_user.id)
    teachers = []
    if list_of_teachers and list_of_passed_lessons: 
        for teacher in list_of_teachers:
            for one_lesson in list_of_passed_lessons:
                if teacher[0] == one_lesson[0] and one_lesson[3] == "Yes":
                    teachers.append(teacher)
                    break
    return render_template('les_materials.html', teachers=teachers, lessons=list_of_passed_lessons, gett=Theme.get)


@app.route("/les_homeworks")
def les_homeworks():
    list_of_teachers = Teacher_Students.get_teachers_of_this_student(current_user.id)
    list_of_passed_lessons = Lesson.list_passed_lessons_for_std(current_user.id)
    teachers = []
    if list_of_teachers and list_of_passed_lessons: 
        for teacher in list_of_teachers:
            for one_lesson in list_of_passed_lessons:
                if teacher[0] == one_lesson[0] and one_lesson[3] == "Yes":
                    teachers.append(teacher)
                    break
    return render_template('les_homeworks.html', teachers=teachers, lessons=list_of_passed_lessons, gett=Theme.get)


@app.route("/les_notes")
def les_notes():
    list_of_teachers = Teacher_Students.get_teachers_of_this_student(current_user.id)
    list_of_passed_lessons = Lesson.list_passed_lessons_for_std(current_user.id)
    teachers = []
    if list_of_teachers and list_of_passed_lessons: 
        for teacher in list_of_teachers:
            for one_lesson in list_of_passed_lessons:
                if teacher[0] == one_lesson[0] and one_lesson[3] == "Yes":
                    teachers.append(teacher)
                    break
    # print(Lesson.get())
    return render_template('les_notes.html', teachers=teachers, lessons=list_of_passed_lessons, gett=Lesson.get)


@app.route("/students_schedule")
def students_schedule():
    list_of_teachers = Teacher_Students.get_teachers_of_this_student(current_user.id)
    lessons = Lesson.list_future_lessons_for_std(current_user.id)
    return (render_template('student_schedule.html', teachers=list_of_teachers, day_of_week=calendar.day_name, lessons=lessons, date__=datetime.datetime.strptime))

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
