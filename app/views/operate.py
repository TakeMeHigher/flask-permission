from flask import Flask,Blueprint,render_template

op=Blueprint('index',__name__)


@op.route('/index')
def index():
    return render_template('index.html')