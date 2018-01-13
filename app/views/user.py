from flask import  Flask,session,render_template,redirect,Blueprint,request,session
from app import db,models

import settings
user=Blueprint('user',__name__,static_folder='static')



class BasePagePermission(object):
    def __init__(self,code_list):
        self.code_list=code_list
    def has_add(self):
        if "add" in self.code_list:
            return True

    def has_edit(self):
        if "edit" in self.code_list:
            return True
    def has_del(self):
        if "del" in self.code_list:
            return  True



@user.route('/userlist',methods=['POST','GET'])
def userlist():
    users=db.session.query(models.User).all()
    pagepermission = BasePagePermission(request.permission_code_list)
    result = session.get(settings.RESULT)
    return render_template('userlist.html',users=users,pagepermission=pagepermission,result=result)


