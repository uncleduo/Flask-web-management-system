# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import Required, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from ..models import Student

