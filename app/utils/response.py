"""
统一响应封装工具类
"""
import json
from typing import Any, Dict, Optional
from datetime import datetime


class ApiCode:
    """API响应状态码常量"""
    SUCCESS = 200          # 成功
    CREATED = 200          # 创建成功
    BAD_REQUEST = 400      # 请求参数错误
    UNAUTHORIZED = 401     # 未授权
    FORBIDDEN = 403        # 禁止访问
    NOT_FOUND = 404        # 资源不存在
    INTERNAL_ERROR = 500   # 服务器内部错误


class ApiResponse:
    """API响应基类"""
    
    def __init__(self, code: int, message: str, data: Any = None):
        """
        初始化响应对象
        
        Args:
            code: 响应状态码
            message: 响应消息
            data: 响应数据
        """
        self.code = code
        self.message = message
        self.data = data
        self.timestamp = int(datetime.now().timestamp() * 1000)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, default=str)


class PaginationInfo:
    """分页信息类"""
    
    def __init__(self, page: int, per_page: int, total: int):
        """
        初始化分页信息
        
        Args:
            page: 当前页码
            per_page: 每页数量
            total: 总记录数
        """
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = (total + per_page - 1) // per_page  # 总页数
        self.has_next = page < self.pages
        self.has_prev = page > 1
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "page": self.page,
            "per_page": self.per_page,
            "total": self.total,
            "pages": self.pages,
            "has_next": self.has_next,
            "has_prev": self.has_prev
        }


class ResponseUtil:
    """响应工具类"""
    
    @staticmethod
    def success(data: Any = None, message: str = "操作成功") -> ApiResponse:
        """成功响应"""
        return ApiResponse(ApiCode.SUCCESS, message, data)
    
    @staticmethod
    def created(data: Any = None, message: str = "创建成功") -> ApiResponse:
        """创建成功响应"""
        return ApiResponse(ApiCode.CREATED, message, data)
    
    @staticmethod
    def error(code: int, message: str, data: Any = None) -> ApiResponse:
        """错误响应"""
        return ApiResponse(code, message, data)
    
    @staticmethod
    def not_found(message: str = "资源不存在") -> ApiResponse:
        """资源不存在响应"""
        return ApiResponse(ApiCode.NOT_FOUND, message)
    
    @staticmethod
    def bad_request(message: str = "请求参数错误", errors: Any = None) -> ApiResponse:
        """请求参数错误响应"""
        data = {"errors": errors} if errors else None
        return ApiResponse(ApiCode.BAD_REQUEST, message, data)
    
    @staticmethod
    def unauthorized(message: str = "未授权访问") -> ApiResponse:
        """未授权响应"""
        return ApiResponse(ApiCode.UNAUTHORIZED, message)
    
    @staticmethod
    def forbidden(message: str = "禁止访问") -> ApiResponse:
        """禁止访问响应"""
        return ApiResponse(ApiCode.FORBIDDEN, message)
    
    @staticmethod
    def internal_error(message: str = "服务器内部错误") -> ApiResponse:
        """服务器内部错误响应"""
        return ApiResponse(ApiCode.INTERNAL_ERROR, message)
    
    @staticmethod
    def paginated_response(
        items: list, 
        page: int, 
        per_page: int, 
        total: int, 
        message: str = "查询成功"
    ) -> ApiResponse:
        """分页响应"""
        pagination = PaginationInfo(page, per_page, total)
        data = {
            "items": items,
            "pagination": pagination.to_dict()
        }
        return ApiResponse(ApiCode.SUCCESS, message, data)


class CustomException(Exception):
    """自定义异常基类"""
    
    def __init__(self, code: int, message: str, data: Any = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)
    
    def to_response(self) -> ApiResponse:
        """转换为响应对象"""
        return ApiResponse(self.code, self.message, self.data)


class BusinessException(CustomException):
    """业务异常"""
    
    def __init__(self, message: str, data: Any = None):
        super().__init__(ApiCode.BAD_REQUEST, message, data)


class AuthException(CustomException):
    """认证异常"""
    
    def __init__(self, message: str = "未授权访问"):
        super().__init__(ApiCode.UNAUTHORIZED, message)


class PermissionException(CustomException):
    """权限异常"""
    
    def __init__(self, message: str = "权限不足"):
        super().__init__(ApiCode.FORBIDDEN, message)


class NotFoundException(CustomException):
    """资源不存在异常"""
    
    def __init__(self, message: str = "资源不存在"):
        super().__init__(ApiCode.NOT_FOUND, message)