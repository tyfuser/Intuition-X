"""日志配置"""
import logging
import sys
from typing import Optional


def setup_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """设置日志记录器"""
    logger = logging.getLogger(name or __name__)
    logger.setLevel(level)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    # 控制台handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger


# 全局logger
logger = setup_logger("video_ai_demo", logging.INFO)

