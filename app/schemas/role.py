"""
角色相关数据验证和序列化模型
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """角色基础信息"""
    name: str = Field(..., min_length=1, max_length=50, description="角色名称")
    code: str = Field(..., min_length=1, max_length=50, description="角色代码")
    description: Optional[str] = Field(None, max_length=255, description="角色描述")
    is_active: bool = Field(True, description="是否启用")


class RoleCreate(RoleBase):
    """创建角色"""
    pass


class RoleUpdate(BaseModel):
    """更新角色"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="角色名称")
    code: Optional[str] = Field(None, min_length=1, max_length=50, description="角色代码")
    description: Optional[str] = Field(None, max_length=255, description="角色描述")
    is_active: Optional[bool] = Field(None, description="是否启用")


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
    user_ids: List[int] = Field(..., description="用户ID列表")


class RoleAssignMenus(BaseModel):
    """角色分配菜单"""
    menu_ids: List[int] = Field(..., description="菜单ID列表")


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