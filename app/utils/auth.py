"""
JWT认证和密码加密工具
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import config
import logging
import os

# 配置日志
logger = logging.getLogger(__name__)

# 密码加密上下文
pwd_context = CryptContext(schemes=config.PWD_CONTEXT_SCHEMES, deprecated="auto")

# 确保使用相同的JWT密钥
# 这是解决问题的关键：直接从.env文件或环境变量获取密钥，绕过可能的配置加载问题
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "aada1213123121a1213")
JWT_ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 加密后的密码
        
    Returns:
        bool: 验证结果
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    获取密码哈希值
    
    Args:
        password: 明文密码
        
    Returns:
        str: 加密后的密码
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间
        
    Returns:
        str: JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    # 使用确定的密钥，确保一致性
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    创建刷新令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间
        
    Returns:
        str: JWT刷新令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=config.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    # 使用确定的密钥，确保一致性
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    验证JWT令牌
    
    Args:
        token: JWT令牌
        
    Returns:
        Optional[Dict[str, Any]]: 解码后的数据，验证失败返回None
    """
    try:
        # 使用相同的直接定义的密钥，而不是从config加载
        # 这样确保编码和解码使用完全相同的密钥
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"Token验证失败: {str(e)}")
        return None


def get_current_user_id(token: str) -> Optional[int]:
    """
    从令牌中获取当前用户ID
    
    Args:
        token: JWT令牌
        
    Returns:
        Optional[int]: 用户ID，获取失败返回None
    """
    payload = verify_token(token)
    if payload:
        user_id: int = payload.get("sub")
        return user_id
    return None