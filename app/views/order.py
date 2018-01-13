from flask import Flask,render_template,redirect,Blueprint,request


from  app import  db,models
order=Blueprint('order',__name__)

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
@order.route('/orderlist')
def orderlist():
    orders=db.session.query(models.Order).all()
    pagepermission = BasePagePermission(request.permission_code_list)
    return render_template('orderlist.html',orders=orders,pagepermission=pagepermission)