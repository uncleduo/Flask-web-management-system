# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from . import teacher
from ..models import Student, Notice, Group
from .forms import EditInfoForm, NoticeForm, ScoreForm
from app import db


@teacher.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@teacher.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if current_user.role == 0:
        flash(u'这是老师的功能，你走错啦')
        return redirect(url_for('main.index'))
    myStudentList = Student.query.filter_by(teacherID=current_user.id).all()

    return render_template('attendance.html', myStudentList=myStudentList)


@teacher.route('/isLate/<id>')
def isLate(id):
    student = Student.query.filter_by(id=id).first()
    if student.absent_count == None:
        student.absent_count = 0
    if student.late_count == None:
        student.late_count = 0
    if student.teacherID == current_user.id:
        if student.absent_count == 0:
            flash(u'他没有缺勤，不能记一次迟到')
        else:
            student.absent_count -=1
            student.late_count +=1
            db.session.add(student)
        return redirect(url_for('.attendance'))
    else:
        flash(u'乖，不是老师不要乱给别人加未到哦')
        return redirect(url_for('main.index'))

@teacher.route('/addAbsent/<id>')
def addAbsent(id):
    student = Student.query.filter_by(id=id).first()
    if student.absent_count == None:
        student.absent_count = 0
    if student.teacherID == current_user.id:
        student.absent_count += 1
        db.session.add(student)
        return redirect(url_for('.attendance'))
    else:
        flash(u'乖，不是老师不要乱给别人加未到哦')
        return redirect(url_for('main.index'))

@teacher.route('/deleteNotice/<id>')
def deleteNotice(id):
    notice = Notice.query.filter_by(id=id).first()
    if notice.teacherID == current_user.id:
        db.session.delete(notice)
        flash(u'已经删除该通知')
        return redirect(url_for('.createNotice'))
    else:
        flash(u'你不可以删除哦')
        return redirect(url_for('main.index'))


@teacher.route('/edit_score/<id>', methods=['GET', 'POST'])
def edit_score(id):
    form = ScoreForm()
    this_teacherID = Student.query.filter_by(id=id).first().teacherID
    student = Student.query.filter_by(id=id).first()
    if current_user.id==this_teacherID:
        if form.validate_on_submit():
            student.regular_score = form.regular_score.data
            student.final_score = form.final_score.data
            db.session.add(student)
            return redirect(url_for('student.studentInfo', id=student.id))
    else:
        flash(u'不是老师不要乱打分哦')
        return redirect(url_for('main.index'))
    form.regular_score.data = student.regular_score
    form.final_score.data = student.final_score
    return render_template('edit_score.html', form=form, student=student)


@teacher.route('/createNotice', methods=['GET', 'POST'])
def createNotice():
    if current_user.role == 0:
        flash(u'这是老师的功能，你走错啦')
        return redirect(url_for('main.index'))
    form = NoticeForm()
    if current_user.role and form.validate_on_submit():
        notice = Notice(body=form.body.data,
                            teacherID=current_user.id)
        db.session.add(notice)
        return redirect(url_for('teacher.createNotice'))
    notices = Notice.query.filter_by(teacherID=current_user.id).order_by(Notice.timestamp.desc()).all()
    return render_template('createNotice.html', form=form, notices=notices)


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
    if user.role == 0:
        flash(u'这是老师信息，你走错啦')
        return redirect(url_for('main.index'))
    if user is None:
        abort(404)
    return render_template('teacherInfo.html', user=user)

@teacher.route('/myStudent')
@login_required
def myStudent():
    if current_user.role == 0:
        flash(u'这是老师的功能，你走错啦')
        return redirect(url_for('main.index'))
    myStudentList = Student.query.filter_by(teacherID=current_user.id).all()
    return render_template('myStudent.html', myStudentList=myStudentList)