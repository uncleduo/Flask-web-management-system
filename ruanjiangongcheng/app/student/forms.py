# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Required, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from ..models import Student


class ScoreForm(Form):
    group_score = IntegerField(u'请给平时成绩打分', validators=[NumberRange(0,100,u'必须是0-100的数字')])
    submit = SubmitField(u'打分')

class LoginForm(Form):
    username = StringField(u'用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'让我一直在线')
    submit = SubmitField(u'登录')


class RegistrationForm(Form):
    username = StringField(u'用户名',  validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名必须是英文开头加数字')])
    studentID = StringField(u'学号', validators=[Required(), Length(1, 20), Regexp('^[0-9]*$', 0, u'学号要是数字哦')])
    password = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message=u'两次密码不一样诶')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'注册')


    def validate_username(self, field):
        if Student.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被占用啦')

    def validate_studentID(self, field):
        if Student.query.filter_by(studentID=field.data).first():
            raise ValidationError(u'这个学号已经被使用了')

class EditInfoForm(Form):
    name = StringField(u'姓名', validators=[Length(0,64)])
    major = StringField(u'班级', validators=[Length(0,255)])
    email = StringField(u'邮箱', validators=[Length(0,255)])
    telephone = StringField(u'手机or电话', validators=[Length(0,20)])
    info = StringField(u'个人信息', validators=[Length(0, 255)])
    submit = SubmitField(u'提交')
