"""
角色相关业务逻辑服务
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from app.models.user import Role, User
from app.models.menu import Menu
from app.schemas.role import RoleCreate, RoleUpdate
from app.utils.response import BusinessException, NotFoundException
from config import config


class RoleService:
    """角色服务类"""
    
    @staticmethod
    async def create_role(db: AsyncSession, role_data: RoleCreate) -> Dict[str, Any]:
        """
        创建角色
        
        Args:
            db: 数据库会话
            role_data: 角色创建数据
            
        Returns:
            Dict[str, Any]: 创建的角色信息
            
        Raises:
            BusinessException: 角色名称或代码已存在
        """
        # 检查角色名称是否已存在
        existing_name = await RoleService.get_role_by_name(db, role_data.name)
        if existing_name:
            raise BusinessException("角色名称已存在")
        
        # 检查角色代码是否已存在
        existing_code = await RoleService.get_role_by_code(db, role_data.code)
        if existing_code:
            raise BusinessException("角色代码已存在")
        
        # 创建角色
        db_role = Role(**role_data.model_dump())
        
        db.add(db_role)
        await db.commit()
        await db.refresh(db_role)
        
        return db_role.to_dict()
    
    @staticmethod
    async def get_role_by_id(db: AsyncSession, role_id: int) -> Optional[Role]:
        """
        根据ID获取角色
        
        Args:
            db: 数据库会话
            role_id: 角色ID
            
        Returns:
            Optional[Role]: 角色对象
        """
        result = await db.execute(
            select(Role)
            .options(selectinload(Role.users), selectinload(Role.menus))
            .where(Role.id == role_id, Role.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_role_by_name(db: AsyncSession, name: str) -> Optional[Role]:
        """
        根据名称获取角色
        
        Args:
            db: 数据库会话
            name: 角色名称
            
        Returns:
            Optional[Role]: 角色对象
        """
        result = await db.execute(
            select(Role)
            .where(Role.name == name, Role.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_role_by_code(db: AsyncSession, code: str) -> Optional[Role]:
        """
        根据代码获取角色
        
        Args:
            db: 数据库会话
            code: 角色代码
            
        Returns:
            Optional[Role]: 角色对象
        """
        result = await db.execute(
            select(Role)
            .where(Role.code == code, Role.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_role(db: AsyncSession, role_id: int, role_data: RoleUpdate) -> Optional[Dict[str, Any]]:
        """
        更新角色信息
        
        Args:
            db: 数据库会话
            role_id: 角色ID
            role_data: 更新数据
            
        Returns:
            Optional[Dict[str, Any]]: 更新后的角色信息
            
        Raises:
            NotFoundException: 角色不存在
            BusinessException: 角色名称或代码已存在
        """
        role = await RoleService.get_role_by_id(db, role_id)
        if not role:
            raise NotFoundException("角色不存在")
        
        # 检查角色名称是否已被其他角色使用
        if role_data.name and role_data.name != role.name:
            existing_name = await RoleService.get_role_by_name(db, role_data.name)
            if existing_name and existing_name.id != role_id:
                raise BusinessException("角色名称已存在")
        
        # 检查角色代码是否已被其他角色使用
        if role_data.code and role_data.code != role.code:
            existing_code = await RoleService.get_role_by_code(db, role_data.code)
            if existing_code and existing_code.id != role_id:
                raise BusinessException("角色代码已存在")
        
        # 更新字段
        update_data = role_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(role, field, value)
        
        await db.commit()
        await db.refresh(role)
        
        return role.to_dict()
    
    @staticmethod
    async def delete_role(db: AsyncSession, role_id: int) -> bool:
        """
        删除角色（软删除）
        
        Args:
            db: 数据库会话
            role_id: 角色ID
            
        Returns:
            bool: 删除是否成功
            
        Raises:
            NotFoundException: 角色不存在
        """
        role = await RoleService.get_role_by_id(db, role_id)
        if not role:
            raise NotFoundException("角色不存在")
        
        role.is_deleted = True
        await db.commit()
        
        return True
    
    @staticmethod
    async def get_roles_paginated(
        db: AsyncSession, 
        page: int = 1, 
        per_page: int = config.DEFAULT_PAGE_SIZE,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分页获取角色列表
        
        Args:
            db: 数据库会话
            page: 页码
            per_page: 每页数量
            search: 搜索关键词
            
        Returns:
            Dict[str, Any]: 分页结果
        """
        # 限制每页最大数量
        per_page = min(per_page, config.MAX_PAGE_SIZE)
        offset = (page - 1) * per_page
        
        # 构建查询条件
        query = select(Role).where(Role.is_deleted == False)
        count_query = select(func.count(Role.id)).where(Role.is_deleted == False)
        
        if search:
            search_filter = or_(
                Role.name.ilike(f"%{search}%"),
                Role.code.ilike(f"%{search}%"),
                Role.description.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        # 获取总数
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # 获取分页数据
        query = query.options(selectinload(Role.users), selectinload(Role.menus)).offset(offset).limit(per_page)
        result = await db.execute(query)
        roles = result.scalars().all()
        
        # 转换为字典
        items = [role.to_dict() for role in roles]
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
            "has_next": page * per_page < total,
            "has_prev": page > 1
        }
    
    @staticmethod
    async def assign_users(db: AsyncSession, role_id: int, user_ids: List[int]) -> bool:
        """
        为角色分配用户
        
        Args:
            db: 数据库会话
            role_id: 角色ID
            user_ids: 用户ID列表
            
        Returns:
            bool: 分配是否成功
            
        Raises:
            NotFoundException: 角色不存在
        """
        role = await RoleService.get_role_by_id(db, role_id)
        if not role:
            raise NotFoundException("角色不存在")
        
        # 获取用户对象
        users_result = await db.execute(
            select(User).where(User.id.in_(user_ids), User.is_deleted == False)
        )
        users = users_result.scalars().all()
        
        # 清空现有用户并分配新用户
        role.users = users
        await db.commit()
        
        return True
    
    @staticmethod
    async def assign_menus(db: AsyncSession, role_id: int, menu_ids: List[int]) -> bool:
        """
        为角色分配菜单权限
        
        Args:
            db: 数据库会话
            role_id: 角色ID
            menu_ids: 菜单ID列表
            
        Returns:
            bool: 分配是否成功
            
        Raises:
            NotFoundException: 角色不存在
        """
        role = await RoleService.get_role_by_id(db, role_id)
        if not role:
            raise NotFoundException("角色不存在")
        
        # 获取菜单对象
        menus_result = await db.execute(
            select(Menu).where(Menu.id.in_(menu_ids), Menu.is_deleted == False)
        )
        menus = menus_result.scalars().all()
        
        # 清空现有菜单并分配新菜单
        role.menus = menus
        await db.commit()
        
        return True
    
    @staticmethod
    async def get_all_roles(db: AsyncSession) -> List[Dict[str, Any]]:
        """
        获取所有可用角色
        
        Args:
            db: 数据库会话
            
        Returns:
            List[Dict[str, Any]]: 角色列表
        """
        result = await db.execute(
            select(Role)
            .where(Role.is_deleted == False, Role.is_active == True)
            .order_by(Role.name)
        )
        roles = result.scalars().all()
        return [role.to_dict() for role in roles]