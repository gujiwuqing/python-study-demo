"""
菜单相关数据库模型
"""
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.associations import role_menu_association


class Menu(BaseModel):
    """菜单模型"""
    __tablename__ = "menus"
    
    name = Column(String(50), nullable=False,unique=True, comment="菜单名称")
    path = Column(String(255), nullable=True,unique=True, comment="菜单路径")
    component = Column(String(255), nullable=True, comment="组件路径")
    icon = Column(String(100), nullable=True, comment="菜单图标")
    order_num = Column(Integer, default=0, comment="排序号")
    parent_id = Column(Integer, ForeignKey('menus.id'), nullable=True, comment="父菜单ID")
    menu_type = Column(String(20), default='menu', comment="菜单类型：menu菜单，button按钮")
    permission = Column(String(100), nullable=True, comment="权限标识")
    is_visible = Column(Boolean, default=True, comment="是否显示")
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    # 自关联：父子菜单关系 - 使用 lambda 表达式修复自引用问题
    children = relationship("Menu", backref="parent", remote_side=lambda: [Menu.id])
    # 关联角色
    roles = relationship("Role", secondary=role_menu_association, back_populates="menus")
    
    def __repr__(self):
        return f"<Menu(id={self.id}, name='{self.name}', path='{self.path}')>"
    
    def to_tree_dict(self) -> dict:
        """转换为树形结构字典"""
        data = self.to_dict()
        data['children'] = [child.to_tree_dict() for child in self.children if child.is_active and not child.is_deleted]
        return data
