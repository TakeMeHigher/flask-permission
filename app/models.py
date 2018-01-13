from sqlalchemy import Column, Index, UniqueConstraint, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Menu(db.Model):
    '''
     菜单表
    '''
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32), nullable=True, unique=True)


class Group(db.Model):
    '''
    权限组表
    '''
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32), nullable=True, unique=True)
    menu_id = Column(Integer, ForeignKey("menu.id"))

    menu = relationship('Menu', backref='groups')


class Permission(db.Model):
    '''
    权限表
    '''
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32), nullable=True)
    url = Column(String(64), nullable=True)
    menu_gp_id = Column(Integer, ForeignKey('permission.id'))
    code = Column(String(32), default='list')
    group_id = Column(Integer, ForeignKey('group.id'), default=1)

    goup = relationship('Group', backref='pers')

    menu_gp=relationship('Permission')
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }


class Role(db.Model):
    '''
    角色表
    '''
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32), nullable=True)

    pers = relationship("Permission", secondary='permission2role', backref='roles')


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
    username = Column(String(32), nullable=True, index=True)
    pwd = Column(String(32), nullable=True)

    roles = relationship('Role',secondary='user2role',backref='users')


class User2Role(db.Model):
    '''
    用户角色表
    '''
    __tablename__='user2role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id=Column(Integer,ForeignKey('user.id'))
    role_id=Column(Integer,ForeignKey('role.id'))


