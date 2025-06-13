"""
数据库关联表定义
"""
from sqlalchemy import Column, Integer, ForeignKey, Table
from app.models.base import BaseModel

# 用户角色关联表
user_role_association = Table(
    'user_roles',
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True, comment="用户ID"),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True, comment="角色ID"),
    comment="用户角色关联表"
)

# 角色菜单关联表
role_menu_association = Table(
    'role_menu_association',
    BaseModel.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True, comment="角色ID"),
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True, comment="菜单ID"),
    comment="角色菜单关联表"
)