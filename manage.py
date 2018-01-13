#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
被毙掉了
    # 5. 创建和删除表
    以后执行db.create_all()
    以后执行db.drop_all()
新第5步：
    安装 pip3 install Flask-Migrate
"""

import os
from flask_script import Manager, Server
# 5.1 导入
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app()
manager = Manager(app)
# 5.2 创建migrate示例
migrate = Migrate(app, db)


@manager.command
def custom(arg):
    """
    自定义命令
    python manage.py custom 123
    :param arg:
    :return:
    """
    print(arg)


@manager.option('-n', '--name', dest='name')
@manager.option('-u', '--url', dest='url')
def cmd(name, url):
    """
    自定义命令
    执行： python manage.py  cmd -n wupeiqi -u http://www.oldboyedu.com
    :param name:
    :param url:
    :return:
    """
    print(name, url)


@manager.command
def import_news(path):
    """
    批量导入
    :param name:
    :param url:
    :return:
    """
    #


"""
# 数据库迁移命名
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
"""
# 5.3 创建db命令
manager.add_command('db', MigrateCommand)

"""
# 自定义命令
    python manage.py runserver 
"""
manager.add_command("runserver", Server())

"""
生成当前环境的所有依赖： requirements.txt
    pip3 freeze > requirements.txt

生成当前程序的所有依赖： requirements.txt
    pip3 install pipreqs
    pipreqs ./

"""

if __name__ == "__main__":
    manager.run()
