# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Student


class CreateTeacher(Form):
    username = StringField(u'用户名',  validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名必须是英文开头加数字')])
    password = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message=u'两次密码不一样诶')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'创建')

