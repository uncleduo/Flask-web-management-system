from flask import Flask, render_template
from flask_bootstrap import  Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from config import config
from flask_login import LoginManager, login_required


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'student.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .student import student as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/student')

    from .teacher import teacher as teacher_blueprint
    app.register_blueprint(teacher_blueprint, url_prefix='/teacher')

    from .group import group as group_blueprint
    app.register_blueprint(group_blueprint, url_prefix='/group')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app