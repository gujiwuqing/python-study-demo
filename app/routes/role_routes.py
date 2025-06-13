"""
角色相关路由
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.database import get_db
from app.utils.dependencies import get_current_user, get_current_superuser
from app.utils.response import ResponseUtil, BusinessException, NotFoundException
from app.services.role_service import RoleService
from app.schemas.role import (
    RoleCreate, RoleUpdate, Role, RoleWithMenus, 
    RoleAssignUsers, RoleAssignMenus
)
from app.models.user import User as UserModel

router = APIRouter(prefix="/api/roles", tags=["角色管理"])


@router.post("", response_model=dict, summary="创建角色")
async def create_role(
    role_data: RoleCreate,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """创建角色（需要超级管理员权限）"""
    try:
        role = await RoleService.create_role(db, role_data)
        response = ResponseUtil.created(role, "角色创建成功")
        return response.to_dict()
        
    except BusinessException as e:
        response = ResponseUtil.bad_request(e.message)
        raise HTTPException(status_code=400, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"创建失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("", response_model=dict, summary="分页获取角色列表")
async def get_roles(
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """分页获取角色列表"""
    try:
        result = await RoleService.get_roles_paginated(db, page, per_page, search)
        response = ResponseUtil.paginated_response(
            result["items"], page, per_page, result["total"], "查询成功"
        )
        return response.to_dict()
        
    except Exception as e:
        response = ResponseUtil.internal_error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("/{role_id}", response_model=dict, summary="获取指定角色信息")
async def get_role_by_id(
    role_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取指定角色信息"""
    try:
        role = await RoleService.get_role_by_id(db, role_id)
        if not role:
            response = ResponseUtil.not_found("角色不存在")
            raise HTTPException(status_code=404, detail=response.to_dict())
        
        role_data = role.to_dict()
        response = ResponseUtil.success(role_data, "查询成功")
        return response.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        response = ResponseUtil.internal_error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.put("/{role_id}", response_model=dict, summary="更新角色信息")
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """更新角色信息（需要超级管理员权限）"""
    try:
        updated_role = await RoleService.update_role(db, role_id, role_data)
        response = ResponseUtil.success(updated_role, "更新成功")
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


@router.delete("/{role_id}", response_model=dict, summary="删除角色")
async def delete_role(
    role_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """删除角色（需要超级管理员权限）"""
    try:
        await RoleService.delete_role(db, role_id)
        result = {"id": role_id, "deleted": True}
        response = ResponseUtil.success(result, "删除成功")
        return response.to_dict()
        
    except NotFoundException as e:
        response = ResponseUtil.not_found(e.message)
        raise HTTPException(status_code=404, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"删除失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.post("/{role_id}/users", response_model=dict, summary="为角色分配用户")
async def assign_role_users(
    role_id: int,
    assign_data: RoleAssignUsers,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """为角色分配用户（需要超级管理员权限）"""
    try:
        await RoleService.assign_users(db, role_id, assign_data.user_ids)
        response = ResponseUtil.success(None, "用户分配成功")
        return response.to_dict()
        
    except NotFoundException as e:
        response = ResponseUtil.not_found(e.message)
        raise HTTPException(status_code=404, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"分配失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.post("/{role_id}/menus", response_model=dict, summary="为角色分配菜单")
async def assign_role_menus(
    role_id: int,
    assign_data: RoleAssignMenus,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """为角色分配菜单（需要超级管理员权限）"""
    try:
        await RoleService.assign_menus(db, role_id, assign_data.menu_ids)
        response = ResponseUtil.success(None, "菜单分配成功")
        return response.to_dict()
        
    except NotFoundException as e:
        response = ResponseUtil.not_found(e.message)
        raise HTTPException(status_code=404, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"分配失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())