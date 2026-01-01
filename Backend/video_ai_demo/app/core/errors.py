"""错误定义"""
from typing import Optional, Dict, Any


class AppError(Exception):
    """应用基础错误"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class JobNotFoundError(AppError):
    """Job不存在"""
    pass


class JobExecutionError(AppError):
    """Job执行错误"""
    pass


class VideoProcessingError(AppError):
    """视频处理错误"""
    pass


class LLMAPIError(AppError):
    """LLM API调用错误"""
    pass


class ValidationError(AppError):
    """数据校验错误"""
    pass


class ConfigurationError(AppError):
    """配置错误"""
    pass

