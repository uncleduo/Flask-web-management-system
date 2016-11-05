# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import Required, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from ..models import Student

class EditInfoForm(Form):
    name = StringField(u'姓名', validators=[Length(0,64)])
    major = StringField(u'科研方向', validators=[Length(0,255)])
    email = StringField(u'邮箱', validators=[Length(0,255)])
    telephone = StringField(u'手机or电话', validators=[Length(0,20)])
    info = StringField(u'教师信息', validators=[Length(0, 255)])
    submit = SubmitField(u'提交')


class NoticeForm(Form):
    body = TextAreaField(u'请输入通知', validators=[Required()])
    submit = SubmitField(u'发布')


class ScoreForm(Form):
    regular_score = IntegerField(u'请给平时成绩打分', validators=[NumberRange(0,100,u'必须是0-100的数字')])
    final_score = IntegerField(u'请给期末成绩打分', validators=[NumberRange(0,100,u'必须是0-100的数字')])
    submit = SubmitField(u'打分')


