"""
项目配置文件
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """基础配置类"""
    
    # 应用基础配置
    APP_NAME = "FastAPI 后端管理系统"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # 数据库配置
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "fengweihui1998")
    MYSQL_DB = os.getenv("MYSQL_DB", "demo")
    
    # 数据库URL
    DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here-please-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 7))
    
    # 密码加密配置
    PWD_CONTEXT_SCHEMES = ["bcrypt"]
    
    # 分页配置
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    
    # 跨域配置
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    MYSQL_DB = "fastapi_admin_test"
    DATABASE_URL = f"mysql+aiomysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/fastapi_admin_test"


# 根据环境变量选择配置
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

# 获取当前环境配置
env = os.getenv("ENVIRONMENT", "development")
config = config_map.get(env, DevelopmentConfig)