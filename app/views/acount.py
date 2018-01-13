from  flask import Flask, Blueprint, request, render_template, redirect, current_app
from app import db, models

count = Blueprint('count', __name__)


@count.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get("name")
        pwd = request.form.get("pwd")

        user = db.session.query(models.User).filter(models.User.username == name, models.User.pwd == pwd).first()

        if user:
            current_app.auth_manager.login(name)
            current_app.auth_manager.permission(user)

            return redirect('/index')
