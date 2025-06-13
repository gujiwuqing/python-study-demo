"""
FastAPI 后端管理系统主入口文件
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import traceback

from config import config
from app.utils.database import init_db, close_db
from app.utils.response import ResponseUtil, CustomException
from app.routes.user_routes import router as user_router

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("FastAPI 应用启动中...")
    try:
        await init_db()
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise e
    
    yield
    
    # 关闭时执行
    logger.info("FastAPI 应用关闭中...")
    try:
        await close_db()
        logger.info("数据库连接已关闭")
    except Exception as e:
        logger.error(f"数据库关闭失败: {e}")


# 创建FastAPI应用实例
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description="基于FastAPI的后端管理系统，包含用户、角色、菜单管理功能",
    docs_url="/docs" if config.DEBUG else None,
    redoc_url="/redoc" if config.DEBUG else None,
    lifespan=lifespan
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS,
)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    """自定义异常处理器"""
    response = exc.to_response()
    return JSONResponse(
        status_code=exc.code,
        content=response.to_dict()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    # 如果detail已经是字典格式（来自我们的统一响应），直接返回
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    
    # 否则包装成统一格式
    response = ResponseUtil.error(exc.status_code, str(exc.detail))
    return JSONResponse(
        status_code=exc.status_code,
        content=response.to_dict()
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"未处理的异常: {exc}")
    logger.error(f"异常堆栈: {traceback.format_exc()}")
    
    response = ResponseUtil.internal_error("服务器内部错误")
    return JSONResponse(
        status_code=500,
        content=response.to_dict()
    )


# 注册路由
app.include_router(user_router)

# 根路径
@app.get("/", summary="根路径")
async def root():
    """根路径接口"""
    response = ResponseUtil.success({
        "app_name": config.APP_NAME,
        "version": config.APP_VERSION,
        "status": "running"
    }, "服务运行正常")
    return response.to_dict()


# 健康检查接口
@app.get("/health", summary="健康检查")
async def health_check():
    """健康检查接口"""
    response = ResponseUtil.success({
        "status": "healthy",
        "timestamp": ResponseUtil.success().timestamp
    }, "服务健康")
    return response.to_dict()


if __name__ == "__main__":
    import uvicorn
    
    # 启动应用
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG,
        log_level="info" if config.DEBUG else "warning"
    )