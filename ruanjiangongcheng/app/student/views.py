# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from . import student
from ..models import Student
from .forms import LoginForm, RegistrationForm, EditInfoForm
from app import db

@student.route('/secret')
@login_required
def secret():
    return u'没登录不准看！'

@student.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()

@student.route('/edit-info', methods=['GET', 'POST'])
@login_required
def edit_info():
    form = EditInfoForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.major = form.major.data
        current_user.telephone = form.telephone.data
        current_user.info = form.info.data
        current_user.email = form.email.data
        db.session.add(current_user)
        flash(u'你的信息已经更新')
        return redirect(url_for('.studentInfo', id=current_user.id))
    form.name.data = current_user.name
    form.major.data = current_user.major
    form.telephone.data = current_user.telephone
    form.info.data = current_user.info
    form.email.data = current_user.email
    return render_template('edit_info.html', form=form)


@student.route('/addTeacher/<teacherID>')
@login_required
def addTeacher(teacherID):
    student_now = Student.query.filter_by(studentID=current_user.studentID).first()
    if student_now.teacherID :
        flash(u'不许重复选择')
        return redirect(url_for('main.index'))
    student_now.teacherID = teacherID
    db.session.add(student_now)
    flash(u'您已经选择老师')
    return redirect(url_for('main.index'))

@student.route('/chooseTeacher')
@login_required
def chooseTeacher():
    teacherList = Student.query.filter_by(role=1).all()
    return render_template('chooseTeacher.html', teacherList=teacherList)

@student.route('/studentInfo/<id>')
@login_required
def studentInfo(id):
    user = Student.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    return render_template('studentInfo.html', user=user)

@student.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username = form.username.data).first()
        if student is not None and student.verify_password(form.password.data):
            login_user(student, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名密码不匹配')
    return render_template('login.html', form=form)


@student.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Student(username=form.username.data,
                       studentID=form.studentID.data,
                       password=form.password.data)
        db.session.add(user)
        flash(u'你可以登录了')
        return redirect(url_for('student.login'))
    return render_template('register.html', form=form)


@student.route('/logut')
@login_required
def logout():
    logout_user()
    flash(u'您刚刚登出了本系统')
    return redirect(url_for('main.index'))
