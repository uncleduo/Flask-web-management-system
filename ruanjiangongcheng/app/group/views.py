# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from . import group
from ..models import Student, Group
from .forms import CreateGroup
from app import db


@group.route('/groupInfo/<groupID>')
@login_required
def groupInfo(groupID):
    group = Group.query.filter_by(groupID=groupID).first()
    groupMember = Student.query.filter_by(groupID=groupID).all()
    if groupMember is None:
        abort(404)
    return render_template('groupInfo.html', groupMember=groupMember, group=group)

@group.route('/groupList/<teacherID>')
@login_required
def groupList(teacherID):
    groupList = Group.query.filter_by(teacherID=teacherID).all()
    return render_template('groupList.html', groupList=groupList)

@group.route('createGroup', methods=['GET', 'POST'])
@login_required
def createGroup():
    if current_user.groupID:
        flash(u'你已经有分组啦')
        return redirect(url_for('main.index'))
    if current_user.role:
        flash(u'老师无法创建小组')
        return redirect(url_for('main.index'))
    form = CreateGroup()
    student_now = Student.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        group = Group(
                group_name=form.group_name.data,
                teacherID=current_user.teacherID,
                group_leader=current_user.id)
        db.session.add(group)
        student_now.groupID = Group.query.filter_by(group_leader=current_user.id).first().groupID
        db.session.add(student_now)
        flash(u'小组创建完成')
        return redirect(url_for('main.index'))
    return render_template('createGroup.html', form=form)


@group.route('/joinGroup/<groupID>')
@login_required
def joinGroup(groupID):
    student_now = Student.query.filter_by(studentID=current_user.studentID).first()
    if student_now.groupID :
        flash(u'不许重复选择')
        return redirect(url_for('main.index'))
    student_now.groupID = groupID
    db.session.add(student_now)
    flash(u'您已经加入小组')
    return redirect(url_for('main.index'))



