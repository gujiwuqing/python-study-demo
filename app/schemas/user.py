"""
用户相关数据验证和序列化模型
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """用户基础信息"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    is_active: bool = Field(True, description="是否激活")


class UserCreate(UserBase):
    """创建用户"""
    password: str = Field(..., min_length=6, max_length=20, description="密码")


class UserUpdate(BaseModel):
    """更新用户"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    is_active: Optional[bool] = Field(None, description="是否激活")


class UserChangePassword(BaseModel):
    """修改密码"""
    old_password: str = Field(..., description="原密码")
    new_password: str = Field(..., min_length=6, max_length=20, description="新密码")


class UserInDBBase(UserBase):
    """数据库中的用户基础信息"""
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class User(UserInDBBase):
    """用户响应模型"""
    pass


class UserInDB(UserInDBBase):
    """数据库中的用户（包含密码）"""
    hashed_password: str


class UserLogin(BaseModel):
    """用户登录"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")


class UserRegister(BaseModel):
    """用户注册"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=6, max_length=20, description="密码")
    confirm_password: str = Field(..., description="确认密码")


class Token(BaseModel):
    """JWT令牌"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """令牌数据"""
    user_id: Optional[int] = None


class UserWithRoles(UserInDBBase):
    """包含角色的用户信息"""
    roles: List["RoleSimple"] = []


class RoleSimple(BaseModel):
    """简化的角色信息"""
    id: int
    name: str
    code: str
    description: Optional[str]
    
    class Config:
        from_attributes = True


# 更新前向引用
UserWithRoles.model_rebuild()