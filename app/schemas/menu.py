"""
菜单相关数据验证和序列化模型
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    """菜单基础信息"""
    name: str = Field(..., min_length=1, max_length=50, description="菜单名称", examples=["用户管理", "系统设置", "权限管理"])
    path: Optional[str] = Field(None, max_length=255, description="菜单路径", examples=["/users", "/system", "/permissions"])
    component: Optional[str] = Field(None, max_length=255, description="组件路径", examples=["UserManagement", "SystemSettings", "PermissionManagement"])
    icon: Optional[str] = Field(None, max_length=100, description="菜单图标", examples=["user", "setting", "lock"])
    order_num: int = Field(0, description="排序号", examples=[1, 2, 3])
    parent_id: Optional[int] = Field(None, description="父菜单ID", examples=[1, 2, None])
    menu_type: str = Field("menu", description="菜单类型：menu菜单，button按钮", examples=["menu", "button"])
    permission: Optional[str] = Field(None, max_length=100, description="权限标识", examples=["user:list", "system:config", "permission:assign"])
    is_visible: bool = Field(True, description="是否显示", examples=[True])
    is_active: bool = Field(True, description="是否启用", examples=[True])


class MenuCreate(MenuBase):
    """创建菜单"""
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "用户管理",
                    "path": "/users",
                    "component": "UserManagement",
                    "icon": "user",
                    "order_num": 1,
                    "parent_id": None,
                    "menu_type": "menu",
                    "permission": "user:list",
                    "is_visible": True,
                    "is_active": True
                }
            ]
        }
    }


class MenuUpdate(BaseModel):
    """更新菜单"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="菜单名称", examples=["高级用户管理"])
    path: Optional[str] = Field(None, max_length=255, description="菜单路径", examples=["/advanced-users"])
    component: Optional[str] = Field(None, max_length=255, description="组件路径", examples=["AdvancedUserManagement"])
    icon: Optional[str] = Field(None, max_length=100, description="菜单图标", examples=["user-plus"])
    order_num: Optional[int] = Field(None, description="排序号", examples=[5])
    parent_id: Optional[int] = Field(None, description="父菜单ID", examples=[2])
    menu_type: Optional[str] = Field(None, description="菜单类型：menu菜单，button按钮", examples=["button"])
    permission: Optional[str] = Field(None, max_length=100, description="权限标识", examples=["user:advanced"])
    is_visible: Optional[bool] = Field(None, description="是否显示", examples=[False])
    is_active: Optional[bool] = Field(None, description="是否启用", examples=[False])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "高级用户管理",
                    "path": "/advanced-users",
                    "icon": "user-plus",
                    "order_num": 5,
                    "is_visible": True
                }
            ]
        }
    }


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
    menu_id: int = Field(..., description="菜单ID", examples=[1])
    user_id: int = Field(..., description="用户ID", examples=[1])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "menu_id": 1,
                    "user_id": 1
                }
            ]
        }
    }


# 更新前向引用
MenuTree.model_rebuild()