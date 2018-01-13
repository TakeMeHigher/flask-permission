from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
from auth.auth import Auth
from .models import *
from .views import acount
from .views import operate
from .views import user
from .views import order

def create_app():
    app=Flask(__name__)
    app.debug=True
    #session秘钥
    app.secret_key='ctz12345'


    #配置文件
    app.config.from_object('settings.BaseConfig')

    #注册蓝图
    app.register_blueprint(acount.count)
    app.register_blueprint(operate.op)
    app.register_blueprint(user.user)
    app.register_blueprint(order.order)

    #注册Auth组件
    Auth(app)

    #注册flask_sqlalchemy
    db.init_app(app)


    return app


