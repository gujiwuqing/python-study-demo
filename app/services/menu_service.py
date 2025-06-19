"""
菜单相关业务逻辑服务
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from app.models.menu import Menu
from app.models.user import User, Role
from app.schemas.menu import MenuCreate, MenuUpdate
from app.utils.response import BusinessException, NotFoundException
from config import config


class MenuService:
    """菜单服务类"""
    
    @staticmethod
    async def create_menu(db: AsyncSession, menu_data: MenuCreate) -> Dict[str, Any]:
        """
        创建菜单
        
        Args:
            db: 数据库会话
            menu_data: 菜单创建数据
            
        Returns:
            Dict[str, Any]: 创建的菜单信息
            
        Raises:
            BusinessException: 父菜单不存在或菜单名称/路径重复
        """
        # 如果有父菜单ID，检查父菜单是否存在
        if menu_data.parent_id:
            parent_menu = await MenuService.get_menu_by_id(db, menu_data.parent_id)
            if not parent_menu:
                raise BusinessException("父菜单不存在")
        
        # 检查菜单名称是否重复
        name_result = await db.execute(
            select(Menu).where(Menu.name == menu_data.name, Menu.is_deleted == False).limit(1)
        )
        existing_name_menu = name_result.scalar_one_or_none()
        if existing_name_menu:
            raise BusinessException("菜单名称已存在")
        
        # 检查菜单路径是否重复（如果路径不为空）
        if menu_data.path:
            path_result = await db.execute(
                select(Menu).where(Menu.path == menu_data.path, Menu.is_deleted == False).limit(1)
            )
            existing_path_menu = path_result.scalar_one_or_none()
            if existing_path_menu:
                raise BusinessException("菜单路径已存在")
        
        # 创建菜单
        db_menu = Menu(**menu_data.model_dump())
        
        db.add(db_menu)
        await db.commit()
        await db.refresh(db_menu)
        
        return db_menu.to_dict()
    
    @staticmethod
    async def get_menu_by_id(db: AsyncSession, menu_id: int) -> Optional[Menu]:
        """
        根据ID获取菜单
        
        Args:
            db: 数据库会话
            menu_id: 菜单ID
            
        Returns:
            Optional[Menu]: 菜单对象
        """
        result = await db.execute(
            select(Menu)
            .options(selectinload(Menu.children), selectinload(Menu.roles))
            .where(Menu.id == menu_id, Menu.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_menu(db: AsyncSession, menu_id: int, menu_data: MenuUpdate) -> Optional[Dict[str, Any]]:
        """
        更新菜单信息
        
        Args:
            db: 数据库会话
            menu_id: 菜单ID
            menu_data: 更新数据
            
        Returns:
            Optional[Dict[str, Any]]: 更新后的菜单信息
            
        Raises:
            NotFoundException: 菜单不存在
            BusinessException: 父菜单不存在或不能设置自己为父菜单或菜单名称/路径重复
        """
        menu = await MenuService.get_menu_by_id(db, menu_id)
        if not menu:
            raise NotFoundException("菜单不存在")
        
        # 如果更新父菜单ID，需要验证
        if menu_data.parent_id is not None:
            if menu_data.parent_id == menu_id:
                raise BusinessException("不能设置自己为父菜单")
            
            if menu_data.parent_id != 0:  # 0表示顶级菜单
                parent_menu = await MenuService.get_menu_by_id(db, menu_data.parent_id)
                if not parent_menu:
                    raise BusinessException("父菜单不存在")
        
        # 检查菜单名称是否重复（如果要更新名称）
        if menu_data.name is not None:
            name_result = await db.execute(
                select(Menu).where(
                    Menu.name == menu_data.name, 
                    Menu.is_deleted == False, 
                    Menu.id != menu_id
                ).limit(1)
            )
            existing_name_menu = name_result.scalar_one_or_none()
            if existing_name_menu:
                raise BusinessException("菜单名称已存在")
        
        # 检查菜单路径是否重复（如果要更新路径且路径不为空）
        if menu_data.path is not None and menu_data.path:
            path_result = await db.execute(
                select(Menu).where(
                    Menu.path == menu_data.path, 
                    Menu.is_deleted == False, 
                    Menu.id != menu_id
                ).limit(1)
            )
            existing_path_menu = path_result.scalar_one_or_none()
            if existing_path_menu:
                raise BusinessException("菜单路径已存在")
        
        # 更新字段
        update_data = menu_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(menu, field, value)
        
        await db.commit()
        await db.refresh(menu)
        
        return menu.to_dict()
    
    @staticmethod
    async def delete_menu(db: AsyncSession, menu_id: int) -> bool:
        """
        删除菜单（软删除）
        
        Args:
            db: 数据库会话
            menu_id: 菜单ID
            
        Returns:
            bool: 删除是否成功
            
        Raises:
            NotFoundException: 菜单不存在
            BusinessException: 存在子菜单，不能删除
        """
        menu = await MenuService.get_menu_by_id(db, menu_id)
        if not menu:
            raise NotFoundException("菜单不存在")
        
        # 检查是否有子菜单
        children_result = await db.execute(
            select(Menu).where(Menu.parent_id == menu_id, Menu.is_deleted == False)
        )
        children = children_result.scalars().all()
        
        if children:
            raise BusinessException("存在子菜单，不能删除")
        
        menu.is_deleted = True
        await db.commit()
        
        return True
    
    @staticmethod
    async def get_menus_paginated(
        db: AsyncSession, 
        page: int = 1, 
        per_page: int = config.DEFAULT_PAGE_SIZE,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分页获取菜单列表
        
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
        query = select(Menu).where(Menu.is_deleted == False)
        count_query = select(func.count(Menu.id)).where(Menu.is_deleted == False)
        
        if search:
            search_filter = or_(
                Menu.name.ilike(f"%{search}%"),
                Menu.path.ilike(f"%{search}%"),
                Menu.component.ilike(f"%{search}%"),
                Menu.permission.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        # 获取总数
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # 获取分页数据
        query = query.options(selectinload(Menu.children), selectinload(Menu.roles)).offset(offset).limit(per_page).order_by(Menu.order_num)
        result = await db.execute(query)
        menus = result.scalars().all()
        
        # 转换为字典
        items = [menu.to_dict() for menu in menus]
        
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
    async def get_menu_tree(db: AsyncSession) -> List[Dict[str, Any]]:
        """
        获取菜单树形结构
        
        Args:
            db: 数据库会话
            
        Returns:
            List[Dict[str, Any]]: 菜单树
        """
        # 获取所有激活的菜单
        result = await db.execute(
            select(Menu)
            .where(Menu.is_deleted == False, Menu.is_active == True)
            .order_by(Menu.order_num)
        )
        all_menus = result.scalars().all()
        
        # 构建菜单树
        menu_dict = {menu.id: menu.to_dict() for menu in all_menus}
        tree = []
        
        for menu in all_menus:
            menu_data = menu_dict[menu.id]
            menu_data['children'] = []
            
            if menu.parent_id is None or menu.parent_id == 0:
                # 顶级菜单
                tree.append(menu_data)
            else:
                # 子菜单
                parent = menu_dict.get(menu.parent_id)
                if parent:
                    parent['children'].append(menu_data)
        
        return tree
    
    @staticmethod
    async def get_user_menus(db: AsyncSession, user_id: int) -> List[Dict[str, Any]]:
        """
        获取用户可访问的菜单
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            List[Dict[str, Any]]: 用户菜单树
        """
        # 获取用户信息和角色
        user_result = await db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.menus))
            .where(User.id == user_id, User.is_deleted == False)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            return []
        
        # 如果是超级管理员，返回所有菜单
        if user.is_superuser:
            return await MenuService.get_menu_tree(db)
        
        # 获取用户角色关联的所有菜单ID
        menu_ids = set()
        for role in user.roles:
            if role.is_active:
                for menu in role.menus:
                    if menu.is_active and not menu.is_deleted:
                        menu_ids.add(menu.id)
        
        if not menu_ids:
            return []
        
        # 获取菜单详情
        menus_result = await db.execute(
            select(Menu)
            .where(
                Menu.id.in_(menu_ids),
                Menu.is_deleted == False,
                Menu.is_active == True,
                Menu.is_visible == True
            )
            .order_by(Menu.order_num)
        )
        user_menus = menus_result.scalars().all()
        
        # 构建菜单树
        menu_dict = {menu.id: menu.to_dict() for menu in user_menus}
        tree = []
        
        for menu in user_menus:
            menu_data = menu_dict[menu.id]
            menu_data['children'] = []
            
            if menu.parent_id is None or menu.parent_id == 0:
                # 顶级菜单
                tree.append(menu_data)
            else:
                # 子菜单
                parent = menu_dict.get(menu.parent_id)
                if parent:
                    parent['children'].append(menu_data)
        
        return tree
    
    @staticmethod
    async def check_user_menu_permission(db: AsyncSession, user_id: int, menu_id: int) -> bool:
        """
        检查用户是否有菜单权限
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            menu_id: 菜单ID
            
        Returns:
            bool: 是否有权限
        """
        # 获取用户信息
        user_result = await db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(Role.menus))
            .where(User.id == user_id, User.is_deleted == False)
        )
        user = user_result.scalar_one_or_none()
        
        if not user or not user.is_active:
            return False
        
        # 超级管理员有所有权限
        if user.is_superuser:
            return True
        
        # 检查角色权限
        for role in user.roles:
            if role.is_active:
                for menu in role.menus:
                    if menu.id == menu_id and menu.is_active and not menu.is_deleted:
                        return True
        
        return False
    
    @staticmethod
    async def get_all_menus(db: AsyncSession) -> List[Dict[str, Any]]:
        """
        获取所有可用菜单
        
        Args:
            db: 数据库会话
            
        Returns:
            List[Dict[str, Any]]: 菜单列表
        """
        result = await db.execute(
            select(Menu)
            .where(Menu.is_deleted == False, Menu.is_active == True)
            .order_by(Menu.order_num)
        )
        menus = result.scalars().all()
        return [menu.to_dict() for menu in menus]
