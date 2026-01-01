"""统一的API响应格式"""
from typing import Optional, Any, TypeVar, Generic
from pydantic import BaseModel, Field
from datetime import datetime


T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """API统一响应格式"""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"key": "value"},
                "message": "操作成功",
                "timestamp": 1704153600000
            }
        }


class ErrorDetail(BaseModel):
    """错误详情"""
    code: str = Field(..., description="错误码")
    message: str = Field(..., description="错误描述")
    details: Optional[Any] = Field(None, description="详细信息")


class ErrorResponse(BaseModel):
    """错误响应"""
    success: bool = False
    error: ErrorDetail
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": {
                    "code": "INVALID_URL",
                    "message": "视频链接格式不正确",
                    "details": None
                },
                "timestamp": 1704153600000
            }
        }


def success_response(data: Any = None, message: Optional[str] = None) -> dict:
    """创建成功响应"""
    return {
        "success": True,
        "data": data,
        "message": message,
        "timestamp": int(datetime.now().timestamp() * 1000)
    }


def error_response(code: str, message: str, details: Any = None) -> dict:
    """创建错误响应"""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details
        },
        "timestamp": int(datetime.now().timestamp() * 1000)
    }


# 常见错误码
class ErrorCode:
    """错误码定义"""
    INVALID_URL = "INVALID_URL"
    UNSUPPORTED_PLATFORM = "UNSUPPORTED_PLATFORM"
    ANALYSIS_FAILED = "ANALYSIS_FAILED"
    QUOTA_EXCEEDED = "QUOTA_EXCEEDED"
    INVALID_TOKEN = "INVALID_TOKEN"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    GENERATION_FAILED = "GENERATION_FAILED"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
    INVALID_REQUEST = "INVALID_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INTERNAL_ERROR = "INTERNAL_ERROR"

