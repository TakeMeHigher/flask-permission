import re

from flask import session,request,redirect,render_template,current_app
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
        #app.before_request(self.check_permission)
        # app.before_request(self.view_menu)
        app.context_processor(self.auth_context_processor)



    def auth_context_processor(self):
        name = session.get('user')
        return dict(current_user=name)


    def check_login(self):

        if request.path=='/login':
            return None

        if session.get('user'):
            self.check_permission()
            self.view_menu()
            return None

        return redirect('/login')


    def check_permission(self):
        current_url=request.path

        if request.path=='/login':
            return None
        if request.path=='/index':
            return None

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


    def view_menu(self):
        menu_list = session.get(settings.PERMISSIONS_MENU_KEY)
        #print(menu_list)
        currenturl = request.path
        #print(menu_list)
        menu_dict = {}
        for item in menu_list:
            if not item["menu_gp_id"]:
                menu_dict[item["id"]] = item
        for item in menu_list:
            regex = "^{0}$".format(item["url"])
            if re.match(regex, currenturl):
                menu_gp_id = item["menu_gp_id"]
                if not menu_gp_id:
                    menu_dict[item["id"]]["active"] = True
                else:
                    menu_dict[item["menu_gp_id"]]["active"] = True
        print(111111111)
        '''
        menu_dict={
        1: {'id': 1, 'title': '用户列表', 'url': '/userinfo/', 'menu_gp_id': None, 'menu_id': 1, 'menu_title': '菜单管理', 'active': True},
        5: {'id': 5, 'title': '订单列表', 'url': '/order/', 'menu_gp_id': None, 'menu_id': 2, 'menu_title': '菜单2'}}
        '''
        #print(menu_dict, "11111111111111111111111111111111111111111111")
        result = {}
        for item in menu_dict.values():
            menu_id = item["menu_id"]
            menu_title = item["menu_title"]
            active = item.get("active")
            url = item["url"]
            title = item["title"]
            #print(active)
            if menu_id in result:
                result[menu_id]["children"].append({"title": title, "url": url, "active": active})
                if active:
                    result[menu_id]["active"] = True
            else:
                result[menu_id] = {
                    "menu_id": menu_id,
                    "menu_title": menu_title,
                    "active": active,
                    "children": [
                        {"title": title, "url": url, "active": active},
                    ]

                }
        session[settings.RESULT]=result
        return result

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


        #菜单相关



        menu_list = []
        for item in permission_list:
            tpl = {
                "id": item["permission_id"],
                "title": item["permission_name"],
                "menu_title": item["permission_menu_title"],
                "url": item["permission_url"],
                "menu_id": item["permission_menu_id"],
                "menu_gp_id": item["permission_menu_gp_id"],
            }
            menu_list.append(tpl)

        session[settings.PERMISSIONS_MENU_KEY] = menu_list


    def login(self,data):
        session['user'] = data
