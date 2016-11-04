# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from . import teacher
from ..models import Student
from .forms import EditInfoForm
from app import db


@teacher.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()

@teacher.route('/edit-info', methods=['GET', 'POST'])
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
        return redirect(url_for('.teacherInfo', id=current_user.id))
    form.name.data = current_user.name
    form.major.data = current_user.major
    form.telephone.data = current_user.telephone
    form.info.data = current_user.info
    form.email.data = current_user.email
    return render_template('edit_info.html', form=form)


@teacher.route('/teacherInfo/<id>')
@login_required
def teacherInfo(id):
    user = Student.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    return render_template('teacherInfo.html', user=user)

@teacher.route('/myStudent')
@login_required
def myStudent():
    myStudentList = Student.query.filter_by(teacherID=current_user.id).all()
    return render_template('myStudent.html', myStudentList=myStudentList)