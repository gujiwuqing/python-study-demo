"""
用户相关路由
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.database import get_db
from app.utils.dependencies import get_current_user, get_current_superuser
from app.utils.response import ResponseUtil, BusinessException, NotFoundException
from app.services.user_service import UserService
from app.schemas.user import (
    UserCreate, UserUpdate, UserChangePassword, UserLogin, UserRegister,
    User, Token, UserWithRoles
)
from app.models.user import User as UserModel

router = APIRouter(prefix="/api/users", tags=["用户管理"])


@router.post("/register", response_model=dict, summary="用户注册")
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """用户注册"""
    try:
        # 验证确认密码
        if user_data.password != user_data.confirm_password:
            response = ResponseUtil.bad_request("两次密码输入不一致")
            raise HTTPException(status_code=400, detail=response.to_dict())
        
        # 创建用户数据
        create_data = UserCreate(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        
        # 创建用户
        user = await UserService.create_user(db, create_data)
        response = ResponseUtil.created(user, "注册成功")
        return response.to_dict()
        
    except BusinessException as e:
        response = ResponseUtil.bad_request(e.message)
        raise HTTPException(status_code=400, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"注册失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.post("/login", response_model=dict, summary="用户登录")
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """用户登录"""
    try:
        # 验证用户
        user = await UserService.authenticate_user(db, login_data.username, login_data.password)
        if not user:
            response = ResponseUtil.bad_request("用户名或密码错误")
            raise HTTPException(status_code=400, detail=response.to_dict())
        
        # 创建令牌
        token_data = await UserService.create_tokens(user)
        response = ResponseUtil.success(token_data, "登录成功")
        return response.to_dict()
        
    except BusinessException as e:
        response = ResponseUtil.bad_request(e.message)
        raise HTTPException(status_code=400, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"登录失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("/me", response_model=dict, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user)
):
    """获取当前用户信息"""
    try:
        user_data = current_user.to_dict()
        response = ResponseUtil.success(user_data, "获取成功")
        return response.to_dict()
        
    except Exception as e:
        response = ResponseUtil.internal_error(f"获取用户信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.put("/me", response_model=dict, summary="更新当前用户信息")
async def update_current_user_info(
    user_data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新当前用户信息"""
    try:
        updated_user = await UserService.update_user(db, current_user.id, user_data)
        response = ResponseUtil.success(updated_user, "更新成功")
        return response.to_dict()
        
    except BusinessException as e:
        response = ResponseUtil.bad_request(e.message)
        raise HTTPException(status_code=400, detail=response.to_dict())
    except NotFoundException as e:
        response = ResponseUtil.not_found(e.message)
        raise HTTPException(status_code=404, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"更新失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.put("/me/password", response_model=dict, summary="修改当前用户密码")
async def change_current_user_password(
    password_data: UserChangePassword,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改当前用户密码"""
    try:
        await UserService.change_password(db, current_user.id, password_data)
        response = ResponseUtil.success(None, "密码修改成功")
        return response.to_dict()
        
    except BusinessException as e:
        response = ResponseUtil.bad_request(e.message)
        raise HTTPException(status_code=400, detail=response.to_dict())
    except NotFoundException as e:
        response = ResponseUtil.not_found(e.message)
        raise HTTPException(status_code=404, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"密码修改失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("", response_model=dict, summary="分页获取用户列表")
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """分页获取用户列表（需要超级管理员权限）"""
    try:
        result = await UserService.get_users_paginated(db, page, per_page, search)
        response = ResponseUtil.paginated_response(
            result["items"], page, per_page, result["total"], "查询成功"
        )
        return response.to_dict()
        
    except Exception as e:
        response = ResponseUtil.internal_error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.post("", response_model=dict, summary="创建用户")
async def create_user(
    user_data: UserCreate,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """创建用户（需要超级管理员权限）"""
    try:
        user = await UserService.create_user(db, user_data)
        response = ResponseUtil.created(user, "创建成功")
        return response.to_dict()
        
    except BusinessException as e:
        response = ResponseUtil.bad_request(e.message)
        raise HTTPException(status_code=400, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"创建失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("/{user_id}", response_model=dict, summary="获取指定用户信息")
async def get_user_by_id(
    user_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """获取指定用户信息（需要超级管理员权限）"""
    try:
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            response = ResponseUtil.not_found("用户不存在")
            raise HTTPException(status_code=404, detail=response.to_dict())
        
        user_data = user.to_dict()
        response = ResponseUtil.success(user_data, "查询成功")
        return response.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        response = ResponseUtil.internal_error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.put("/{user_id}", response_model=dict, summary="更新指定用户信息")
async def update_user_by_id(
    user_id: int,
    user_data: UserUpdate,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """更新指定用户信息（需要超级管理员权限）"""
    try:
        updated_user = await UserService.update_user(db, user_id, user_data)
        response = ResponseUtil.success(updated_user, "更新成功")
        return response.to_dict()
        
    except BusinessException as e:
        response = ResponseUtil.bad_request(e.message)
        raise HTTPException(status_code=400, detail=response.to_dict())
    except NotFoundException as e:
        response = ResponseUtil.not_found(e.message)
        raise HTTPException(status_code=404, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"更新失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.delete("/{user_id}", response_model=dict, summary="删除用户")
async def delete_user_by_id(
    user_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """删除用户（需要超级管理员权限）"""
    try:
        await UserService.delete_user(db, user_id)
        result = {"id": user_id, "deleted": True}
        response = ResponseUtil.success(result, "删除成功")
        return response.to_dict()
        
    except NotFoundException as e:
        response = ResponseUtil.not_found(e.message)
        raise HTTPException(status_code=404, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"删除失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.post("/{user_id}/roles", response_model=dict, summary="为用户分配角色")
async def assign_user_roles(
    user_id: int,
    role_ids: List[int],
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """为用户分配角色（需要超级管理员权限）"""
    try:
        await UserService.assign_roles(db, user_id, role_ids)
        response = ResponseUtil.success(None, "角色分配成功")
        return response.to_dict()
        
    except NotFoundException as e:
        response = ResponseUtil.not_found(e.message)
        raise HTTPException(status_code=404, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"角色分配失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())