"""
数据库连接和会话管理
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import config

# 创建异步数据库引擎
async_engine = create_async_engine(
    config.DATABASE_URL,
    echo=config.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

# 创建异步会话
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 创建基础模型类
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    获取数据库会话
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """
    初始化数据库
    """
    async with async_engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    关闭数据库连接
    """
    await async_engine.dispose()