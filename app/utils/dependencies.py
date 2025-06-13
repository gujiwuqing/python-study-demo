"""
FastAPI依赖注入
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.database import get_db
from app.utils.auth import verify_token
from app.services.user_service import UserService
from app.models.user import User

# JWT令牌认证
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    
    Args:
        credentials: JWT凭证
        db: 数据库会话
        
    Returns:
        User: 用户对象
        
    Raises:
        HTTPException: 认证失败
    """
    # 验证令牌
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户ID
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户信息
    user = await UserService.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        User: 活跃用户对象
        
    Raises:
        HTTPException: 用户未激活
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未激活"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前超级管理员用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        User: 超级管理员用户对象
        
    Raises:
        HTTPException: 权限不足
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    获取可选的当前用户（用于可选认证的接口）
    
    Args:
        credentials: JWT凭证（可选）
        db: 数据库会话
        
    Returns:
        Optional[User]: 用户对象或None
    """
    if not credentials:
        return None
    
    try:
        # 验证令牌
        payload = verify_token(credentials.credentials)
        if not payload:
            return None
        
        # 获取用户ID
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        
        # 这里需要同步方式获取用户，在实际使用中可能需要调整
        return None  # 简化处理
    except:
        return None