# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Student

class EditInfoForm(Form):
    name = StringField(u'姓名', validators=[Length(0,64)])
    major = StringField(u'科研方向', validators=[Length(0,255)])
    email = StringField(u'邮箱', validators=[Length(0,255)])
    telephone = StringField(u'手机or电话', validators=[Length(0,20)])
    info = StringField(u'教师信息', validators=[Length(0, 255)])
    submit = SubmitField(u'提交')

