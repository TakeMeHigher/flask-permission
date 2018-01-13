from flask import Flask,Blueprint,render_template,current_app,session
import settings

from auth.auth import Auth
op=Blueprint('index',__name__,static_folder='static')


@op.route('/index')
def index():

    result=session.get(settings.RESULT)
    print(result,'----******')
    return render_template('base.html',result=result)
