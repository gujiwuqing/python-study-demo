"""
用户相关数据验证和序列化模型
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """用户基础信息"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名", examples=["testuser", "admin", "zhang_san"])
    email: EmailStr = Field(..., description="邮箱", examples=["test@example.com", "admin@company.com", "user@domain.com"])
    phone: Optional[str] = Field(None, max_length=20, description="手机号", examples=["13888888888", "15912345678", None])
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名", examples=["张三", "李四", "王五"])
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL", examples=["https://example.com/avatar.jpg", "https://cdn.example.com/user1.png", None])
    is_active: bool = Field(True, description="是否激活", examples=[True])


class UserCreate(UserBase):
    """创建用户"""
    password: str = Field(..., min_length=6, max_length=20, description="密码", examples=["123456", "password123", "mySecret2024"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "123456",
                    "phone": "13888888888",
                    "real_name": "张三",
                    "avatar": "https://example.com/avatar.jpg",
                    "is_active": True
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """更新用户"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名", examples=["new_username"])
    email: Optional[EmailStr] = Field(None, description="邮箱", examples=["newemail@example.com"])
    phone: Optional[str] = Field(None, max_length=20, description="手机号", examples=["13999999999"])
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名", examples=["新姓名"])
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL", examples=["https://example.com/new-avatar.jpg"])
    is_active: Optional[bool] = Field(None, description="是否激活", examples=[False])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "real_name": "张三丰",
                    "phone": "13999999999",
                    "avatar": "https://example.com/new-avatar.jpg"
                }
            ]
        }
    }


class UserChangePassword(BaseModel):
    """修改密码"""
    old_password: str = Field(..., description="原密码", examples=["123456"])
    new_password: str = Field(..., min_length=6, max_length=20, description="新密码", examples=["newPassword123"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "old_password": "123456",
                    "new_password": "newPassword123"
                }
            ]
        }
    }


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
    username: str = Field(..., description="用户名或邮箱", examples=["testuser", "test@example.com", "admin"])
    password: str = Field(..., description="密码", examples=["123456", "password123"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "testuser",
                    "password": "123456"
                }
            ]
        }
    }


class UserRegister(BaseModel):
    """用户注册"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名", examples=["newuser", "zhangsan", "testuser"])
    email: EmailStr = Field(..., description="邮箱", examples=["newuser@example.com", "register@test.com"])
    password: str = Field(..., min_length=6, max_length=20, description="密码", examples=["123456", "myPassword123"])
    confirm_password: str = Field(..., description="确认密码", examples=["123456", "myPassword123"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "123456",
                    "confirm_password": "123456"
                }
            ]
        }
    }


class Token(BaseModel):
    """JWT令牌"""
    access_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    refresh_token: str = Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field(default="bearer", examples=["bearer"])


class TokenData(BaseModel):
    """令牌数据"""
    user_id: Optional[int] = Field(None, examples=[1, 2, 3])


class UserWithRoles(UserInDBBase):
    """包含角色的用户信息"""
    roles: List["RoleSimple"] = []


class RoleSimple(BaseModel):
    """简化的角色信息"""
    id: int = Field(..., examples=[1, 2, 3])
    name: str = Field(..., examples=["管理员", "普通用户", "编辑者"])
    code: str = Field(..., examples=["admin", "user", "editor"])
    description: Optional[str] = Field(None, examples=["系统管理员", "普通用户权限", "内容编辑权限"])
    
    class Config:
        from_attributes = True


# 更新前向引用
UserWithRoles.model_rebuild()