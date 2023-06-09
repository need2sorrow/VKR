import json
import os
import sqlite3
from flask import Flask, redirect, request, url_for, render_template, session, Blueprint
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
from classes_db.classLesson import Lesson  # from user_role import User_role
import functools
import datetime

bp = Blueprint('api', __name__)  # , url_prefix='/teacher_func')

# **************************---------FOR-TEACHER---------*********************************


@bp.route("/teacher_site", methods=['GET', 'POST'])
def teacher_site():
    return (render_template('teacher_site.html'))


@bp.route("/student_site", methods=['GET', 'POST'])
def student_site():
    teachers = Teacher_Students.get_teachers_of_this_student(current_user.id)
    return (render_template('student_site.html', teachers=teachers))


@bp.route("/add_students", methods=['GET', 'POST'])
def add_students():

    # ПОХИМИЧИТЬ С УДОБСТВОМ ПОИСКА СТУДЕНТА В СПИСКЕ
    form_id = None
    if request.method == 'POST':
        form_id = request.args.get("Form_id", None)
        if form_id == "add":
            choosing_std = request.form.get('choose_student_for_add')
            if not Teacher_Students.get(current_user.id, choosing_std):
                Teacher_Students.create(current_user.id, choosing_std)
        elif form_id == "del":
            choosing_std_for_del = request.form.get('choose_student_for_del')
            Teacher_Students.delete_student(
                current_user.id, choosing_std_for_del)
            Lesson.delete_all_lessons_with_this_student(
                current_user.id, choosing_std_for_del)
    list_of_students = Student.get_list_of_all_students()

    # ????????????????????
    if Teacher_Students.get_students_of_this_teacher(current_user.id):
        for item in Teacher_Students.get_students_of_this_teacher(current_user.id):
            list_of_students.remove(item)
    # это что это куда это зачем (выше)

    students_of_teacher = Teacher_Students.get_students_of_this_teacher(
        current_user.id)
    return (render_template('add_students.html', all_std=list_of_students, students=students_of_teacher, action_type=form_id))

# @bp.route("/del_students", methods=['GET', 'POST'])
# def del_students():

#     # ПОХИМИЧИТЬ С УДОБСТВОМ ПОИСКА СТУДЕНТА В СПИСКЕ

#     if request.method == 'POST':
#         choosing_std_for_del = request.form.get('choose_student_for_del')
#         Teacher_Students.delete_student(current_user.id, choosing_std_for_del)
#         Lesson.delete_all_lessons_with_this_student(current_user.id, choosing_std_for_del)
#     students_of_teacher = Teacher_Students.get_students_of_this_teacher(
#         current_user.id)
#     return (render_template('del_students.html', students=students_of_teacher))


@bp.route("/add_lessons", methods=['GET', 'POST'])
def add_lessons():

    # ДОБАВИТЬ ИЗМЕНЕНИЕ УРОКА (ИЗМЕНИТЬ УЧЕНИКА, ИЗМЕНИТЬ ДАТУВРЕМЯ (ПЕРЕНОС УРОКА), ИЗМЕНИТЬ ТЕМУ)
    date = None
    std = None
    thm = None
    # # students = None
    # themes = None

    bad_auth = ""
    bad_auth2 = ""
    if request.method == 'POST':
        form_id = request.args.get("Form_id", None)

        if form_id == "add":
            choosing_student = request.form.get('choose_student')
            choosing_date = request.form.get('choose_date')
            link = "http://zoom.com/hdfhdflgjrgedfgdl"
            ch_date = datetime.datetime.strptime(choosing_date, '%Y-%m-%dT%H:%M')
            # print(ch_date.strftime('%b %d %Y at %H:%M')) #%I:%M%p'))
            bad_auth = check_possible_time(ch_date)
            if bad_auth == "":
                Lesson.create(current_user.id, choosing_student, str(
                    ch_date.strftime('%Y-%m-%d %H:%M')), link)

        elif form_id == "edit":
            # date = request.args.get("Les_date", None)
            # if not Lesson.get(current_user.id, date):
            #     date = session.get('Date', None)
            new_date = request.form.get('new_date')
            print(new_date)
            new_date = datetime.datetime.strptime(new_date, '%Y-%m-%dT%H:%M')
            bad_auth2 = check_possible_time(new_date)
            new_date = str(new_date.strftime('%Y-%m-%d %H:%M'))
            if date == new_date:
                bad_auth2 = ""
            if bad_auth2 == "":
                Lesson.change_date(current_user.id, date, new_date)
                print("ok")
            if Lesson.get(current_user.id, new_date):
                date = new_date
                # session['Date'] = date
            new_std = request.form.get('new_std')
            print(new_std)
            Lesson.change_student(current_user.id, date, new_std)
            new_thm = request.form.get('new_thm')
            print(new_thm)
            Lesson.change_theme(current_user.id, date, new_thm)

            # date = Lesson.get(current_user.id, date).lesDate
            # std = Lesson.get(current_user.id, date).student_email
            # thm = Lesson.get(current_user.id, date).theme_name
            # # students = Teacher_Students.get_students_of_this_teacher(current_user.id)
            # themes = Theme.get_names(current_user.id)

        elif form_id == "del":
            choosing_date = request.form.get('choose_les')
            Lesson.delete_lesson(current_user.id, choosing_date)

    students_of_this_teacher = Teacher_Students.get_students_of_this_teacher(
        current_user.id)
    list_of_lessons = Lesson.get_lessons_for_a_specific_teacher(
        current_user.id)

    pas_les = Lesson.list_passed_lessons_for_teacher(current_user.id)
    # [[les1][les2]] = [[std, date, theme, passed - 1], [std, date, theme, passed - 2]]
    future_les = Lesson.list_future_lessons_for_teacher(current_user.id)
    if future_les:
        future_les = [tuple(les) for les in future_les] #[[item for item in les] for les in future_les]

    students_future_les = []
    if students_of_this_teacher and future_les:
        for student in students_of_this_teacher:
            # print(student[0], ": ", Lesson.get_all_lessons(current_user.id, student[1]))
            for one_lesson in future_les:
                if student[0] == one_lesson[0]:
                    students_future_les.append(student)
                    break

    students_past_les = []
    if students_of_this_teacher and pas_les:
        for student in students_of_this_teacher:
            for one_lesson in pas_les:
                if student[0] == one_lesson[0]:
                    students_past_les.append(student)
                    break

    if date != None:
        date = Lesson.get(current_user.id, date).lesDate
        std = Lesson.get(current_user.id, date).student_email
        thm = Lesson.get(current_user.id, date).theme_name
    # students = Teacher_Students.get_students_of_this_teacher(current_user.id)
    themes = Theme.get_names(current_user.id)

    i = 0
    # list_les = []
    # if students_of_this_teacher and future_les:
    #     for student in students_of_this_teacher:
    #         print(student)
    #         for one_lesson in future_les:
    #             if student[0] == one_lesson[0]:
    #                 i=i+1
    #             print(one_lesson)
    #         if i>0:
    #             i=0
    #         else:
    #             mes = "С ним пока нет уроков. Добавьте их ниже"
    #             list_les.append([student[0], mes])
    # print(list_les)
    # print([tuple(les) for les in Lesson.get_all_lessons(current_user.id)])
    return (render_template('add_lessons.html', future_students=students_future_les, past_students=students_past_les,
                            students_of_this_teacher=students_of_this_teacher, bad_auth=bad_auth, bad_auth2=bad_auth2, passed_les=pas_les, future_les=future_les,
                            date=date, std=std, thm=thm, themes=themes, enumerate=enumerate))
#  lessons=list_of_lessons, lessons_les=list_les,


def check_possible_time(ch_date):
    bad_auth = ""
    list_of_lessons = Lesson.get_lessons_for_a_specific_teacher(
        current_user.id)
    now = datetime.datetime.now()
    if now > ch_date:
        bad_auth = "Выберите корректные дату и время для будущего урока"
    else:
        if list_of_lessons:
            for start_les in list_of_lessons:
                hour = datetime.timedelta(minutes=59)
                start_les___ = datetime.datetime.strptime(start_les[1], '%Y-%m-%d %H:%M')
                hour_before_start_les = start_les___ - hour
                end_les = start_les___ + hour
                # print(hour_before_start_les, " < ", ch_date, " < ", end_les)
                if start_les___ <= ch_date <= end_les:
                    bad_auth = "Это время занято"
                elif hour_before_start_les <= ch_date <= start_les___:
                    bad_auth = "У вас будет меньше часа на проведение урока. Вы не успеете"
    return bad_auth


@bp.route("/del_lessons", methods=['GET', 'POST'])
def del_lessons():

    # ДОБАВИТЬ ИЗМЕНЕНИЕ УРОКА (ИЗМЕНИТЬ УЧЕНИКА, ИЗМЕНИТЬ ДАТУВРЕМЯ (ПЕРЕНОС УРОКА), ИЗМЕНИТЬ ТЕМУ)

    students_of_this_teacher = Teacher_Students.get_students_of_this_teacher(
        current_user.id)
    # list_of_lessons = [lesson for lesson in Lesson.get_lessons_for_a_specific_teacher(current_user.id) if lesson[3] != "Yes"]
    if request.method == 'POST':
        choosing_date = request.form.get('choose_les')
        Lesson.delete_lesson(current_user.id, choosing_date)

    # students_of_this_teacher = Teacher_Students.get_students_of_this_teacher(current_user.id)
    list_of_lessons = [lesson for lesson in Lesson.get_lessons_for_a_specific_teacher(
        current_user.id) if lesson[3] != "Yes"]

    students = []
    if students_of_this_teacher and list_of_lessons:
        for student in students_of_this_teacher:
            for one_lesson in list_of_lessons:
                if student[0] == one_lesson[0] and one_lesson[3] != "Yes":
                    students.append(student)
                    break
    # , list_lessons_for_choose_del=list_les))
    return (render_template('del_lessons.html',  students=students, lessons=list_of_lessons, all_std=students_of_this_teacher))

# @bp.route("/change_lessons", methods=['GET', 'POST'])
# def change_lessons():

#     # ДОБАВИТЬ ИЗМЕНЕНИЕ УРОКА (ИЗМЕНИТЬ УЧЕНИКА, ИЗМЕНИТЬ ДАТУВРЕМЯ (ПЕРЕНОС УРОКА), ИЗМЕНИТЬ ТЕМУ)

#     students_of_this_teacher = Teacher_Students.get_students_of_this_teacher(current_user.id)
#     list_of_lessons = Lesson.get_lessons_for_a_specific_teacher(current_user.id)

#     students = []
#     if students_of_this_teacher and list_of_lessons:
#         for student in students_of_this_teacher:
#             for one_lesson in list_of_lessons:
#                 if student[0] == one_lesson[0] and one_lesson[3] == "No":
#                     students.append(student)
#                     break
#     return (render_template('change_lessons.html',  students=students, lessons=list_of_lessons))


@bp.route("/change_les_parameters", methods=['GET', 'POST'])
def change_les_parameters():
    date = request.args.get("Les_date", None)
    bad_auth = ""
    if request.method == 'POST':

        if not Lesson.get(current_user.id, date):
            date = session.get('Date', None)
        new_date = request.form.get('new_date')
        new_date = datetime.datetime.strptime(new_date, '%Y-%m-%dT%H:%M')
        bad_auth = check_possible_time(new_date)
        new_date = str(new_date.strftime('%Y-%m-%d %H:%M'))
        if date == new_date:
            bad_auth = ""
        if bad_auth == "":
            Lesson.change_date(current_user.id, date, new_date)
        if Lesson.get(current_user.id, new_date):
            date = new_date
            session['Date'] = date
        new_std = request.form.get('new_std')
        Lesson.change_student(current_user.id, date, new_std)
        new_thm = request.form.get('new_thm')
        Lesson.change_theme(current_user.id, date, new_thm)

    date = Lesson.get(current_user.id, date).lesDate
    std = Lesson.get(current_user.id, date).student_email
    thm = Lesson.get(current_user.id, date).theme_name
    students = Teacher_Students.get_students_of_this_teacher(current_user.id)
    themes = Theme.get_names(current_user.id)
    return render_template('change_les_parameters.html', date=date, std=std, thm=thm, students=students, themes=themes, bad_auth=bad_auth)
    # СОРТИРОВКА СПИСКА СТУДЕНТОВ ПО СТУДЕНТАМ
    # ДОБАВИТЬ ИЗМЕНЕНИЕ УРОКА ( ИЗМЕНИТЬ ДАТУВРЕМЯ (ПЕРЕНОС УРОКА), ИЗМЕНИТЬ ТЕМУ)


@bp.route("/add_theme_start", methods=['GET', 'POST'])
def add_theme1():

    students_of_this_teacher = Teacher_Students.get_students_of_this_teacher(
        current_user.id)

    if request.method == 'POST':
        choosing_lesson = request.args.get("Les", None)
        choosing_theme = request.form.get('choose_theme')
        Lesson.change_theme(current_user.id, choosing_lesson, choosing_theme)
    lessons = [lesson for lesson in Lesson.get_lessons_for_a_specific_teacher(
        current_user.id) if lesson[3] == "No"]  # None
    # if Lesson.get_lessons_for_a_specific_teacher(current_user.id):
    #     lessons_for_std = [lesson for lesson in Lesson.get_lessons_for_a_specific_teacher(
    #         current_user.id) if (lesson[3] == "No" and lesson[0] == std)]

    themes = Theme.get_names(current_user.id)
    return (render_template('add_theme1.html', students=students_of_this_teacher, lessons=lessons, themes=themes, enumerate=enumerate, get_lessons_for_student_and_teacher=Lesson.get_list_of_lessons_for_student_and_teacher_with_themes))


@bp.route("/add_theme_finish", methods=['GET', 'POST'])
def add_theme2():

    std = session.get('Stud', None)

    if request.method == 'POST':
        choosing_lesson = request.form.get('choose_lesson')
        choosing_theme = request.form.get('choose_theme')
        Lesson.change_theme(current_user.id, choosing_lesson, choosing_theme)

    lessons_for_std = None
    if Lesson.get_lessons_for_a_specific_teacher(current_user.id):
        lessons_for_std = [lesson for lesson in Lesson.get_lessons_for_a_specific_teacher(
            current_user.id) if (lesson[3] == "No" and lesson[0] == std)]

    themes = Theme.get_names(current_user.id)
    return (render_template('add_theme2.html', std=std, lessons_for_std=lessons_for_std, list_of_themes=themes))


@bp.route("/page_student")
def page_student():
    student_email = request.args.get("Stud_email", None)
    return (render_template('page_for_any_student.html', name=Student.get(student_email).name, email=Student.get(student_email).id))


@bp.route("/page_theme")
def page_theme():
    theme_name = request.args.get("Theme_name", None)
    if current_user.role == "student":
        teach_email = request.args.get("Teach_email", None)
    else:
        teach_email = current_user.id
    return (render_template('page_for_any_theme.html', name=Theme.get(teach_email, theme_name).name, mat=Theme.get(teach_email, theme_name).materials, hw=Theme.get(teach_email, theme_name).homework))


@bp.route("/passed_lessons_for_teacher")
def passed_lessons_for_teacher():
    list_of_students = Teacher_Students.get_students_of_this_teacher(
        current_user.id)
    list_of_passed_lessons = Lesson.list_passed_lessons_for_teacher(
        current_user.id)
    students = []
    if list_of_students and list_of_passed_lessons:
        for student in list_of_students:
            for one_lesson in list_of_passed_lessons:
                if student[0] == one_lesson[0] and one_lesson[3] == "Yes":
                    students.append(student)
                    break

    return render_template('passed_lessons_for_teacher.html', students=students, lessons=list_of_passed_lessons)


@bp.route("/new_theme", methods=['GET', 'POST'])
def new_theme():
    bad_auth = ""
    if request.method == 'POST':
        form_id = request.args.get("Form_id", None)
        if form_id == "add":
            choosing_name_of_theme = request.form.get('enter_name_of_theme')
            mat = request.form.get('materials')
            hw = request.form.get('homework')
            if not Theme.get(current_user.id, choosing_name_of_theme):
                Theme.create(current_user.id, choosing_name_of_theme, mat, hw)
                bad_auth = ""
            else:
                bad_auth = "Тема с таким названием уже существует, придумайте другое"
        elif form_id == "edit":
            theme_name = request.args.get("Theme_name", None)
            # if not Theme.get(current_user.id, theme_name):
            #     theme_name = session.get('Th_name', None)
            new_name = request.form.get('new_name')
            Theme.change_name(current_user.id, theme_name, new_name)
            # mat = Theme.get(current_user.id, theme_name).materials
            if Theme.get(current_user.id, new_name):
                theme_name = new_name
                # session['Th_name'] = theme_name
            new_mat = request.form.get('new_mat')
            Theme.change_materials(current_user.id, theme_name, new_mat)
            new_hw = request.form.get('new_hw')
            Theme.change_homework(current_user.id, theme_name, new_hw)
    #         real_name_of_theme = Theme.get(current_user.id, theme_name).name
    # mat = Theme.get(current_user.id, theme_name).materials
    # hw = Theme.get(current_user.id, theme_name).homework
        elif form_id == "del":
            choosing_name_of_theme = request.form.get('choose_theme')
            Theme.del_theme(current_user.id, choosing_name_of_theme)
    list_of_themes = Theme.get_names(current_user.id)
    for item in list_of_themes:
        if item[0] == "No theme":
            list_of_themes.remove(item)
    # print(list_of_themes)
    return (render_template('new_theme.html', themes=list_of_themes, bad_auth=bad_auth, enumerate=enumerate))


@bp.route("/edit_theme")
def edit_theme():
    list_of_themes = Theme.get_names(current_user.id)
    list_of_themes.remove("No theme")
    return render_template('change_theme.html', themes=list_of_themes)


@bp.route("/edit_theme_parameters", methods=['GET', 'POST'])
def edit_theme_parameters():
    theme_name = request.args.get("Theme_name", None)

    if request.method == 'POST':

        if not Theme.get(current_user.id, theme_name):
            theme_name = session.get('Th_name', None)
            mat = Theme.get(current_user.id, theme_name).materials
        new_name = request.form.get('new_name')
        Theme.change_name(current_user.id, theme_name, new_name)
        if Theme.get(current_user.id, new_name):
            theme_name = new_name
            session['Th_name'] = theme_name
        new_mat = request.form.get('new_mat')
        Theme.change_materials(current_user.id, theme_name, new_mat)
        new_hw = request.form.get('new_hw')
        Theme.change_homework(current_user.id, theme_name, new_hw)

    real_name_of_theme = Theme.get(current_user.id, theme_name).name
    mat = Theme.get(current_user.id, theme_name).materials
    hw = Theme.get(current_user.id, theme_name).homework
    return render_template('change_theme_parameters.html', name=real_name_of_theme, mat=mat, hw=hw)


@bp.route("/delete_theme", methods=['GET', 'POST'])
def delete_theme():
    if request.method == 'POST':
        choosing_name_of_theme = request.form.get('choose_theme')
        Theme.del_theme(current_user.id, choosing_name_of_theme)
    list_of_themes = Theme.get_names(current_user.id)
    list_of_themes.remove("No theme")
    return render_template('del_theme.html', themes=list_of_themes)






# <li class="list-group-item">{{ lesson[1] }}
#     (<a class="button" href="{{ url_for('go_to_the_lesson', Date=lesson[1]) }}">Перейти к уроку</a>)
# </li>


# <!-- <div class="card mb-1">
#                                     <div class="card-header p-0" id="heading{{student[0]}}">
#                                         <h2 class="mb-0 row">
#                                             <button
#                                                 class="btn btn-link btn-block text-left collapsed text-decoration-none"
#                                                 type="button" data-toggle="collapse"
#                                                 data-target="#collapse{{student[0]}}" aria-expanded="false"
#                                                 aria-controls="collapse{{student[0]}}">
#                                                 {{student[0]}}
#                                             </button>
#                                         </h2>
#                                     </div>
#                                     <div id="collapse{{student[0]}}" class="collapse"
#                                         aria-labelledby="heading{{student[0]}}" data-parent="#accordionExample">
#                                         <div class="card-body">
#                                             <div class="d-flex align-items-start">
#                                                 <div class="nav flex-column nav-pills me-3"
#                                                 id="v-pills-tab{{student[1]}}" role="tablist"
#                                                 aria-orientation="vertical">
#                                                     {% if lessons_for_std %}
#                                                         <p> Ваши уроки с <a class="button"
#                                                                 href="{{ url_for('api.page_student', Stud_name=student[0]) }}"> {{
#                                                                 student[0] }} </a>: </p>
#                                                         {% for i, lesson in enumerate(lessons_for_std) %}
#                                                         {% if student[0] == lesson[0] %}
#                                                             <button class="nav-link" id="tab-{{i}}" data-bs-toggle="pill"
#                                                             data-bs-target="#{{i}}" type="button" role="tab"
#                                                             aria-controls="{{i}}">
#                                                             {{ lesson[1] }} - {{ lesson[2] }}
#                                                             </button>
#                                                         {% endif %}
#                                                         {% endfor %}
#                                                     {% else %}
#                                                         <p>Для этого ученика пока не выставлено ни одного урока. Сначала
#                                                             добавьте уроки</p>
#                                                         <a class="button" href="/add_lessons">Выставить уроки</a>
#                                                     {% endif %}
#                                                 </div>
#                                                 <div class="tab-content mx-auto" id="v-pills-tabContent">
#                                                     {% for i, lesson in enumerate(lessons_for_std) %}
#                                                     {% if student[0] == lesson[0] %}
#                                                     <div class="tab-pane fade" id="{{i}}" role="tabpanel"
#                                                         aria-labelledby="tab-{{i}}" tabindex="0">
#                                                         <form action=""
#                                                             method="POST" class="form-inline">
#                                                             <div class="mb-2">
#                                                                 <label for="selecter" class="form-label"> New theme:
#                                                                 </label>
#                                                                 <select id="selecter" type="search"
#                                                                     defaultValue="{{lesson[2]}}" list="character"
#                                                                     name="new_theme" required
#                                                                     class="form-select border border-warning border-opacity-50 mx-auto">
#                                                                     <datalist id="character">
#                                                                         {% for theme in themes %}
#                                                                         <option value="{{ theme[0] }}" {% if
#                                                                             theme[0]==lesson[2] %} selected="selected" {%
#                                                                             endif %}>
#                                                                             {{ theme[0] }}</option>
#                                                                         {% endfor %}
#                                                                     </datalist>
#                                                                 </select>
#                                                             </div>

#                                                             <input type="submit" class="btn btn-signin w-50 mt-2"
#                                                                 value="Изменить">
#                                                         </form>
#                                                     </div>
#                                                     {% endif %}
#                                                     {% endfor %}
#                                                 </div>
#                                             </div>
#                                         </div>
#                                     </div>
#                                 </div> -->
