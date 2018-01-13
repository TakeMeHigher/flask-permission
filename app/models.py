from sqlalchemy import Column, Index, UniqueConstraint, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Menu(db.Model):
    '''
     菜单表
    '''
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32), unique=True)

    def __str__(self):
        return self.title


class Group(db.Model):
    '''
    权限组表
    '''
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32),  unique=True)
    menu_id = Column(Integer, ForeignKey("menu.id"))

    menu = relationship('Menu', backref='groups')


    def __str__(self):
        return self.title


class Permission(db.Model):
    '''
    权限表
    '''
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32) )
    url = Column(String(64))
    menu_gp_id = Column(Integer, ForeignKey('permission.id'),nullable=True)
    code = Column(String(32), default='list')
    group_id = Column(Integer, ForeignKey('group.id'), default=1)

    goup = relationship('Group', backref='pers')

    menu_gp=relationship('Permission')
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }


    def __str__(self):
        return self.title



class Role(db.Model):
    '''
    角色表
    '''
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32))

    pers = relationship("Permission", secondary='permission2role', backref='roles')



    def __str__(self):
        return self.title


class Permission2Role(db.Model):
    '''
    角色权限表
    '''
    __tablename__ = 'permission2role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    permission_id = Column(Integer, ForeignKey('permission.id'))





class User(db.Model):
    '''
    用户表
    '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32),index=True)
    pwd = Column(String(32))

    roles = relationship('Role',secondary='user2role',backref='users')



    def __str__(self):
        return self.username


class User2Role(db.Model):
    '''
    用户角色表
    '''
    __tablename__='user2role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id=Column(Integer,ForeignKey('user.id'))
    role_id=Column(Integer,ForeignKey('role.id'))



class Order(db.Model):
    '''
    订单表
    '''
    id=Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String(64))

    user_id=Column(Integer,ForeignKey('user.id'))

    user=relationship('User',backref='orders')






