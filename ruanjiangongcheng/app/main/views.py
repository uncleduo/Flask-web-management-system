from datetime import datetime
from flask import render_template, sessions,redirect, url_for

from . import main
#from . forms import NameForm
from .. import db
#from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/onCoding')
def onCoding():
    return render_template('onCoding.html')


@main.route('/lessonLearned')
def lessonLearned():
    return render_template('lessonLearned.html')

@main.route('/gameInfo')
def gameInfo():
    return render_template('gameInfo.html')
