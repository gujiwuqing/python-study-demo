"""
用户相关业务逻辑服务
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from app.models.user import User, Role
from app.schemas.user import UserCreate, UserUpdate, UserChangePassword
from app.utils.auth import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.utils.response import BusinessException, NotFoundException
from config import config


class UserService:
    """用户服务类"""
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> Dict[str, Any]:
        """
        创建用户
        
        Args:
            db: 数据库会话
            user_data: 用户创建数据
            
        Returns:
            Dict[str, Any]: 创建的用户信息
            
        Raises:
            BusinessException: 用户名或邮箱已存在
        """
        # 检查用户名是否已存在
        existing_user = await UserService.get_user_by_username(db, user_data.username)
        if existing_user:
            raise BusinessException("用户名已存在")
        
        # 检查邮箱是否已存在
        existing_email = await UserService.get_user_by_email(db, user_data.email)
        if existing_email:
            raise BusinessException("邮箱已存在")
        
        # 创建用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            phone=user_data.phone,
            hashed_password=hashed_password,
            real_name=user_data.real_name,
            avatar=user_data.avatar,
            is_active=user_data.is_active
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user.to_dict()
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """
        根据ID获取用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            Optional[User]: 用户对象
        """
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == user_id, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            Optional[User]: 用户对象
        """
        result = await db.execute(
            select(User)
            .where(User.username == username, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        
        Args:
            db: 数据库会话
            email: 邮箱
            
        Returns:
            Optional[User]: 用户对象
        """
        result = await db.execute(
            select(User)
            .where(User.email == email, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
        """
        用户认证
        
        Args:
            db: 数据库会话
            username: 用户名或邮箱
            password: 密码
            
        Returns:
            Optional[User]: 认证成功返回用户对象，否则返回None
        """
        # 尝试用户名登录
        user = await UserService.get_user_by_username(db, username)
        if not user:
            # 尝试邮箱登录
            user = await UserService.get_user_by_email(db, username)
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> Optional[Dict[str, Any]]:
        """
        更新用户信息
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            user_data: 更新数据
            
        Returns:
            Optional[Dict[str, Any]]: 更新后的用户信息
            
        Raises:
            NotFoundException: 用户不存在
            BusinessException: 用户名或邮箱已存在
        """
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("用户不存在")
        
        # 检查用户名是否已被其他用户使用
        if user_data.username and user_data.username != user.username:
            existing_user = await UserService.get_user_by_username(db, user_data.username)
            if existing_user and existing_user.id != user_id:
                raise BusinessException("用户名已存在")
        
        # 检查邮箱是否已被其他用户使用
        if user_data.email and user_data.email != user.email:
            existing_email = await UserService.get_user_by_email(db, user_data.email)
            if existing_email and existing_email.id != user_id:
                raise BusinessException("邮箱已存在")
        
        # 更新字段
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        
        return user.to_dict()
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """
        删除用户（软删除）
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            bool: 删除是否成功
            
        Raises:
            NotFoundException: 用户不存在
        """
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("用户不存在")
        
        user.is_deleted = True
        await db.commit()
        
        return True
    
    @staticmethod
    async def change_password(db: AsyncSession, user_id: int, password_data: UserChangePassword) -> bool:
        """
        修改密码
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            password_data: 密码修改数据
            
        Returns:
            bool: 修改是否成功
            
        Raises:
            NotFoundException: 用户不存在
            BusinessException: 原密码错误
        """
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("用户不存在")
        
        if not verify_password(password_data.old_password, user.hashed_password):
            raise BusinessException("原密码错误")
        
        user.hashed_password = get_password_hash(password_data.new_password)
        await db.commit()
        
        return True
    
    @staticmethod
    async def get_users_paginated(
        db: AsyncSession, 
        page: int = 1, 
        per_page: int = config.DEFAULT_PAGE_SIZE,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分页获取用户列表
        
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
        query = select(User).where(User.is_deleted == False)
        count_query = select(func.count(User.id)).where(User.is_deleted == False)
        
        if search:
            search_filter = or_(
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.real_name.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        # 获取总数
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # 获取分页数据
        query = query.options(selectinload(User.roles)).offset(offset).limit(per_page)
        result = await db.execute(query)
        users = result.scalars().all()
        
        # 转换为字典
        items = [user.to_dict() for user in users]
        
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
    async def assign_roles(db: AsyncSession, user_id: int, role_ids: List[int]) -> bool:
        """
        为用户分配角色
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            role_ids: 角色ID列表
            
        Returns:
            bool: 分配是否成功
            
        Raises:
            NotFoundException: 用户不存在
        """
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException("用户不存在")
        
        # 获取角色对象
        roles_result = await db.execute(
            select(Role).where(Role.id.in_(role_ids), Role.is_deleted == False)
        )
        roles = roles_result.scalars().all()
        
        # 清空现有角色并分配新角色
        user.roles = roles
        await db.commit()
        
        return True
    
    @staticmethod
    async def create_tokens(user: User) -> Dict[str, Any]:
        """
        创建用户令牌
        
        Args:
            user: 用户对象
            
        Returns:
            Dict[str, Any]: 令牌信息
        """
        access_token = create_access_token({"sub": user.id, "username": user.username})
        refresh_token = create_refresh_token({"sub": user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user.to_dict()
        }