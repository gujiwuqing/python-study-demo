"""
角色相关数据验证和序列化模型
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """角色基础信息"""
    name: str = Field(..., min_length=1, max_length=50, description="角色名称", examples=["管理员", "普通用户", "编辑者"])
    code: str = Field(..., min_length=1, max_length=50, description="角色代码", examples=["admin", "user", "editor"])
    description: Optional[str] = Field(None, max_length=255, description="角色描述", examples=["系统管理员，拥有所有权限", "普通用户权限", "内容编辑权限"])
    is_active: bool = Field(True, description="是否启用", examples=[True])


class RoleCreate(RoleBase):
    """创建角色"""
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "管理员",
                    "code": "admin",
                    "description": "系统管理员，拥有所有权限",
                    "is_active": True
                }
            ]
        }
    }


class RoleUpdate(BaseModel):
    """更新角色"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="角色名称", examples=["高级管理员"])
    code: Optional[str] = Field(None, min_length=1, max_length=50, description="角色代码", examples=["super_admin"])
    description: Optional[str] = Field(None, max_length=255, description="角色描述", examples=["高级管理员，拥有更多权限"])
    is_active: Optional[bool] = Field(None, description="是否启用", examples=[False])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "高级管理员",
                    "description": "高级管理员，拥有更多权限",
                    "is_active": True
                }
            ]
        }
    }


class RoleInDBBase(RoleBase):
    """数据库中的角色基础信息"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Role(RoleInDBBase):
    """角色响应模型"""
    pass


class RoleWithMenus(RoleInDBBase):
    """包含菜单的角色信息"""
    menus: List["MenuSimple"] = []


class RoleAssignUsers(BaseModel):
    """角色分配用户"""
    user_ids: List[int] = Field(..., description="用户ID列表", examples=[[1, 2, 3]])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_ids": [1, 2, 3]
                }
            ]
        }
    }


class RoleAssignMenus(BaseModel):
    """角色分配菜单"""
    menu_ids: List[int] = Field(..., description="菜单ID列表", examples=[[1, 2, 3, 4]])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "menu_ids": [1, 2, 3, 4]
                }
            ]
        }
    }


class MenuSimple(BaseModel):
    """简化的菜单信息"""
    id: int
    name: str
    path: Optional[str]
    component: Optional[str]
    icon: Optional[str]
    order_num: int
    parent_id: Optional[int]
    menu_type: str
    permission: Optional[str]
    is_visible: bool
    is_active: bool
    
    class Config:
        from_attributes = True


# 更新前向引用
RoleWithMenus.model_rebuild()