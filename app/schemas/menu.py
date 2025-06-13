"""
菜单相关数据验证和序列化模型
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    """菜单基础信息"""
    name: str = Field(..., min_length=1, max_length=50, description="菜单名称")
    path: Optional[str] = Field(None, max_length=255, description="菜单路径")
    component: Optional[str] = Field(None, max_length=255, description="组件路径")
    icon: Optional[str] = Field(None, max_length=100, description="菜单图标")
    order_num: int = Field(0, description="排序号")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    menu_type: str = Field("menu", description="菜单类型：menu菜单，button按钮")
    permission: Optional[str] = Field(None, max_length=100, description="权限标识")
    is_visible: bool = Field(True, description="是否显示")
    is_active: bool = Field(True, description="是否启用")


class MenuCreate(MenuBase):
    """创建菜单"""
    pass


class MenuUpdate(BaseModel):
    """更新菜单"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="菜单名称")
    path: Optional[str] = Field(None, max_length=255, description="菜单路径")
    component: Optional[str] = Field(None, max_length=255, description="组件路径")
    icon: Optional[str] = Field(None, max_length=100, description="菜单图标")
    order_num: Optional[int] = Field(None, description="排序号")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    menu_type: Optional[str] = Field(None, description="菜单类型：menu菜单，button按钮")
    permission: Optional[str] = Field(None, max_length=100, description="权限标识")
    is_visible: Optional[bool] = Field(None, description="是否显示")
    is_active: Optional[bool] = Field(None, description="是否启用")


class MenuInDBBase(MenuBase):
    """数据库中的菜单基础信息"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Menu(MenuInDBBase):
    """菜单响应模型"""
    pass


class MenuTree(MenuInDBBase):
    """菜单树形结构"""
    children: List["MenuTree"] = []


class MenuSimple(BaseModel):
    """简化的菜单信息"""
    id: int
    name: str
    path: Optional[str]
    icon: Optional[str]
    
    class Config:
        from_attributes = True


class MenuPermissionCheck(BaseModel):
    """菜单权限检查"""
    menu_id: int
    user_id: int


# 更新前向引用
MenuTree.model_rebuild()