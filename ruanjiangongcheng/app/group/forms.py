# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Student

class CreateGroup(Form):
    group_name = StringField(u'小组名称', validators=[Required(),Length(0,64)])
    submit = SubmitField(u'创建小组')

