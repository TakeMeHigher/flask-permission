import re

from flask import session,request,redirect
from app import db,models
import settings

class Auth(object):
    def __init__(self,app):
        self.app=app
        if self.app:
            self.init_app(app)


    def init_app(self,app):
        app.auth_manager=self

        app.before_request(self.check_login)
        app.before_request(self.check_permission)
        app.context_processor(self.auth_context_processor)



    def auth_context_processor(self):
        name = session.get('user')
        return dict(current_user=name)


    def check_login(self):

        if request.path=='/login':
            return None

        if session.get('user'):
            return None
        return redirect('/login')


    def check_permission(self):
        current_url=request.path

        permission_url_dict = session.get(settings.PERMISSIONS_URL_DICT_KEY)
        if not permission_url_dict:
            return redirect('/login')

        flag=False
        for group_id,code_url in permission_url_dict.items():

            for url in code_url.get('urls'):
                regex='^{}$'.format(url)

                if re.match(regex,current_url):
                    request.permission_code_list=code_url.get('codes')
                    flag=True
                    break


            if flag:
                break
        if not flag:
            return '无权访问'





    def permission(self,user):
        roles = db.session.query(models.User2Role.role_id).filter(models.User2Role.user_id == user.id).all()
        per_ids = None
        for role_id in roles:
            per_ids = db.session.query(models.Permission2Role.permission_id).filter(
                models.Permission2Role.role_id == role_id[0]).distinct().all()

        # 获取用户所有的权限id lsit
        per_id_list = []
        for per_id_tuple in per_ids:
            per_id_list.append(per_id_tuple[0])

        permission_list = []
        for per_id in per_id_list:
            dic = {}

            per_list = db.session.query(models.Permission.title, models.Permission.url, models.Permission.code,
                                        models.Permission.menu_gp_id, models.Permission.group_id).filter(
                models.Permission.id == per_id).all()

            for per_tuple in per_list:
                dic['permission_id'] = per_id
                dic['permission_name'] = per_tuple[0]
                dic['permission_url'] = per_tuple[1]
                dic['permission_code'] = per_tuple[2]
                dic['permission_menu_gp_id'] = per_tuple[3]
                dic['permission_group_id'] = per_tuple[4]

                group = db.session.query(models.Group).filter(models.Group.id == per_tuple[4]).first()
                dic['permission_menu_id'] = group.menu_id
                dic['permission_menu_title'] = group.menu.title
                permission_list.append(dic)


        #权限相关
        result={}

        for item in permission_list:
            group_id=item['permission_group_id']
            permission_url=item['permission_url']
            permission_code=item['permission_code']


            if group_id in result:
                result[group_id]['codes'].append(permission_code)
                result[group_id]['urls'].append(permission_url)
            else:
                result[group_id]={
                    'codes':[permission_code,],
                    'urls':[permission_url,]
                }

        session[settings.PERMISSIONS_URL_DICT_KEY]=result


    def login(self,data):
        session['user'] = data
