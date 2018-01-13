class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/fpe?charset=utf8"
    SQLALCHEMY_POOL_SIZE = 2
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = -1

    # 追踪对象的修改并且发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False


#权限相关
PERMISSIONS_URL_DICT_KEY="permission_dict_url"

PERMISSIONS_MENU_KEY='PERMISSIONS_MENU_KEY'
RESULT='result'
