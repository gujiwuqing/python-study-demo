"""
用户相关数据库模型
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

# 用户角色关联表
user_role_association = Table(
    'user_roles',
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True, comment="用户ID"),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True, comment="角色ID"),
    comment="用户角色关联表"
)


class User(BaseModel):
    """用户模型"""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    phone = Column(String(20), unique=True, index=True, nullable=True, comment="手机号")
    hashed_password = Column(String(100), nullable=False, comment="加密密码")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    avatar = Column(String(255), nullable=True, comment="头像URL")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_superuser = Column(Boolean, default=False, comment="是否超级管理员")
    
    # 关联角色
    roles = relationship("Role", secondary=user_role_association, back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self, include_password: bool = False) -> dict:
        """转换为字典，默认不包含密码"""
        data = super().to_dict()
        if not include_password:
            data.pop('hashed_password', None)
        return data


class Role(BaseModel):
    """角色模型"""
    __tablename__ = "roles"
    
    name = Column(String(50), unique=True, index=True, nullable=False, comment="角色名称")
    code = Column(String(50), unique=True, index=True, nullable=False, comment="角色代码")
    description = Column(String(255), nullable=True, comment="角色描述")
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    # 关联用户
    users = relationship("User", secondary=user_role_association, back_populates="roles")
    # 关联菜单权限
    menus = relationship("Menu", secondary="role_menu_association", back_populates="roles")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}', code='{self.code}')>"