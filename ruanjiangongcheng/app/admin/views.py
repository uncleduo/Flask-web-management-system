# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from . import admin
from ..models import Student, Group
from .forms import CreateTeacher
from app import db


@admin.route('/secret')
@login_required
def secret():
    return u'没登录不准看！'


@admin.route('/teacherList', methods=['GET', 'POST'])
@login_required
def teacherList():
    if current_user.role != 2:
        flash(u'这是管理员的功能，你走错啦')
        return redirect(url_for('main.index'))
    teacherList = Student.query.filter_by(role=1).all()
    return render_template('teacherList.html', teacherList=teacherList)


@admin.route('/createTeacher', methods=['GET', 'POST'])
def createTeacher():
    form = CreateTeacher()
    if form.validate_on_submit():
        user = Student(username=form.username.data,
                       password=form.password.data,
                       role = 1)
        db.session.add(user)
        flash(u'老师账号已经创建')
        return redirect(url_for('main.index'))
    return render_template('createTeacher.html', form=form)

