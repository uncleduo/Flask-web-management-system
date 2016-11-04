from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from . import login_manager
#from flask_moment import datetime
from datetime import datetime

class Group(db.Model):
    __tablename__ = 'group'
    groupID = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(64))
    group_leader = db.Column(db.String(64))
    teacherID = db.Column(db.Integer)

class Student(UserMixin,db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    name = db.Column(db.String(64))
    role = db.Column(db.Integer, unique=True, default=0)
    studentID = db.Column(db.Integer, unique=True)
    teacherID = db.Column(db.Integer)
    password = db.Column(db.String(256))
    password_hash = db.Column(db.String(256))
    info = db.Column(db.String(256))
    email = db.Column(db.String(256))
    major = db.Column(db.String(256))
    telephone = db.Column(db.String(256))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    regular_score = db.Column(db.Integer)
    group_score = db.Column(db.Integer)
    final_score = db.Column(db.Integer)
    groupID = db.Column(db.Integer)

    def ping(self):
        self.last_seen = str(datetime.utcnow())[:19]
        db.session.add(self)


    @property
    def password(self):
        raise AttributeError('wrong')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    @login_manager.user_loader
    def load_student(id):
        return Student.query.get(int(id))

    def __repr__(self):
        return '<Student %r>' % self.username
