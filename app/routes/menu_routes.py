"""
菜单相关路由
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.database import get_db
from app.utils.dependencies import get_current_user, get_current_superuser
from app.utils.response import ResponseUtil, BusinessException, NotFoundException
from app.services.menu_service import MenuService
from app.schemas.menu import (
    MenuCreate, MenuUpdate, Menu, MenuTree, MenuPermissionCheck
)
from app.models.user import User as UserModel

router = APIRouter(prefix="/api/menus", tags=["菜单管理"])


@router.post("", response_model=dict, summary="创建菜单")
async def create_menu(
    menu_data: MenuCreate,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """创建菜单（需要超级管理员权限）"""
    try:
        menu = await MenuService.create_menu(db, menu_data)
        response = ResponseUtil.created(menu, "菜单创建成功")
        return response.to_dict()
        
    except BusinessException as e:
        response = ResponseUtil.bad_request(e.message)
        raise HTTPException(status_code=400, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"创建失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("", response_model=dict, summary="分页获取菜单列表")
async def get_menus(
    page: int = Query(1, ge=1, description="页码"),
    per_page: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """分页获取菜单列表"""
    try:
        result = await MenuService.get_menus_paginated(db, page, per_page, search)
        response = ResponseUtil.paginated_response(
            result["items"], page, per_page, result["total"], "查询成功"
        )
        return response.to_dict()
        
    except Exception as e:
        response = ResponseUtil.internal_error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("/tree", response_model=dict, summary="获取菜单树形结构")
async def get_menu_tree(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取菜单树形结构"""
    try:
        tree = await MenuService.get_menu_tree(db)
        response = ResponseUtil.success(tree, "查询成功")
        return response.to_dict()
        
    except Exception as e:
        response = ResponseUtil.internal_error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("/user/{user_id}", response_model=dict, summary="获取用户可访问的菜单")
async def get_user_menus(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户可访问的菜单"""
    try:
        # 检查权限：只允许查看自己的菜单或超级管理员查看任何人的菜单
        if current_user.id != user_id and not current_user.is_superuser:
            response = ResponseUtil.forbidden("无权限查看其他用户的菜单")
            raise HTTPException(status_code=403, detail=response.to_dict())
        
        menus = await MenuService.get_user_menus(db, user_id)
        response = ResponseUtil.success(menus, "查询成功")
        return response.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        response = ResponseUtil.internal_error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("/me", response_model=dict, summary="获取当前用户可访问的菜单")
async def get_current_user_menus(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户可访问的菜单"""
    try:
        menus = await MenuService.get_user_menus(db, current_user.id)
        response = ResponseUtil.success(menus, "查询成功")
        return response.to_dict()
        
    except Exception as e:
        response = ResponseUtil.internal_error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.get("/{menu_id}", response_model=dict, summary="获取指定菜单信息")
async def get_menu_by_id(
    menu_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取指定菜单信息"""
    try:
        menu = await MenuService.get_menu_by_id(db, menu_id)
        if not menu:
            response = ResponseUtil.not_found("菜单不存在")
            raise HTTPException(status_code=404, detail=response.to_dict())
        
        menu_data = menu.to_dict()
        response = ResponseUtil.success(menu_data, "查询成功")
        return response.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        response = ResponseUtil.internal_error(f"查询失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())


@router.put("/{menu_id}", response_model=dict, summary="更新菜单信息")
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """更新菜单信息（需要超级管理员权限）"""
    try:
        updated_menu = await MenuService.update_menu(db, menu_id, menu_data)
        response = ResponseUtil.success(updated_menu, "更新成功")
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


@router.delete("/{menu_id}", response_model=dict, summary="删除菜单")
async def delete_menu(
    menu_id: int,
    current_user: UserModel = Depends(get_current_superuser),
    db: AsyncSession = Depends(get_db)
):
    """删除菜单（需要超级管理员权限）"""
    try:
        await MenuService.delete_menu(db, menu_id)
        result = {"id": menu_id, "deleted": True}
        response = ResponseUtil.success(result, "删除成功")
        return response.to_dict()
        
    except BusinessException as e:
        response = ResponseUtil.bad_request(e.message)
        raise HTTPException(status_code=400, detail=response.to_dict())
    except NotFoundException as e:
        response = ResponseUtil.not_found(e.message)
        raise HTTPException(status_code=404, detail=response.to_dict())
    except Exception as e:
        response = ResponseUtil.internal_error(f"删除失败: {str(e)}")
        raise HTTPException(status_code=500, detail=response.to_dict())