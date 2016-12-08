# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, abort, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
from . import group
from ..models import Student, Group, GroupDoc
from .forms import CreateGroup
from werkzeug.utils import secure_filename
from app import db, config
import os, time


@group.route('/showGroupDoc/<int:groupID>', methods=('GET', 'POST'))
@login_required
def showGroupDoc(groupID):
    doc_list = GroupDoc.query.filter_by(groupID=groupID).order_by(GroupDoc.upload_time.desc()).all()
    return render_template('showGroupDoc.html', doc_list=doc_list, groupID=groupID)


@group.route("/downloadGroupDoc/<int:docID>/<int:groupID>")
@login_required
def downloadGroupDoc(docID, groupID):
    filename = GroupDoc.query.filter_by(docID=docID).first().file_name
    user_dir = config['default'].UPLOAD_FOLDER + 'Group' + str(groupID)
    return send_from_directory(user_dir, filename, as_attachment=True)


@group.route('/groupInfo/<groupID>')
@login_required
def groupInfo(groupID):
    group = Group.query.filter_by(groupID=groupID).first()
    leader = Group.query.filter_by(groupID=groupID).first().group_leader
    groupMember = Student.query.filter_by(groupID=groupID).all()
    if groupMember is None:
        abort(404)
    return render_template('groupInfo.html', groupMember=groupMember, group=group, groupID=groupID, leader=leader)


@group.route('/uploadGroupFile', methods=('GET', 'POST'))
@login_required
def uploadGroupFile():
    if current_user.groupID == None:
        flash(u'你没有加入组')
        return redirect(url_for('main.index'))
    if request.method == 'GET':
        return render_template('uploadGroupDoc.html')
    if request.method == "POST":
        t_file = request.files["file"]
        info = request.form["info"]
        user_dir = config['default'].UPLOAD_FOLDER + 'Group' + str(current_user.groupID)
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)
        ext_name = secure_filename(t_file.filename.split(".")[-1])
        if ext_name == '':
            flash(u'不要上传空文件')
            return redirect(url_for('group.groupInfo'))
        new_filename = str(abs(hash(t_file.filename))) + str(time.time())[:10] + "." + ext_name
        file_path = os.path.join(user_dir, new_filename)
        # ToDo
        file_record = GroupDoc(groupID=current_user.groupID, file_name=new_filename, doc_name=info)
        try:
            db.session.add(file_record)
            t_file.save(file_path)
        except:
            db.session.rollback()
            return "fail", 500
        db.session.commit()
        flash(u'上传成功')
    return redirect(url_for('group.groupInfo', groupID=current_user.groupID))


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
        db.session.commit()
        flash(u'小组创建完成')
        return redirect(url_for('main.index'))
    return render_template('createGroup.html', form=form)


@group.route('/refuseJoinGroup/<id>')
def refuseJoinGroup(id):
    student = Student.query.filter_by(id=id).first()
    group = Group.query.filter_by(groupID=student.groupID).first()
    if group.group_leader != current_user.id:
        flash(u'你没有权限')
        return redirect(url_for('group.groupInfo', groupID=current_user.groupID))
    student.groupID = None
    db.session.add(student)
    db.session.commit()
    flash(u'已经拒绝')
    return redirect(url_for('group.groupInfo', groupID=current_user.groupID))


@group.route('/allowJoinGroup/<id>')
def allowJoinGroup(id):
    student = Student.query.filter_by(id=id).first()
    group = Group.query.filter_by(groupID=student.groupID).first()
    if group.group_leader != current_user.id:
        flash(u'你没有权限')
        return redirect(url_for('group.groupInfo', groupID=current_user.groupID))
    student.group_state = 1
    db.session.add(student)
    db.session.commit()
    flash(u'已经通过')
    return redirect(url_for('group.groupInfo', groupID=current_user.groupID))


@group.route('/joinGroup/<groupID>')
@login_required
def joinGroup(groupID):
    student_now = Student.query.filter_by(studentID=current_user.studentID).first()
    if student_now.groupID :
        flash(u'不许重复选择')
        return redirect(url_for('main.index'))
    student_now.groupID = groupID
    student_now.group_state = -1
    db.session.add(student_now)
    db.session.commit()
    flash(u'您已经加入小组')
    return redirect(url_for('main.index'))



