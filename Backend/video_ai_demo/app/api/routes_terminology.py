"""
术语API路由
Terminology API Routes
"""
from fastapi import APIRouter
from typing import Dict, Any

from ..core.shot_terminology import (
    SHOT_TERMINOLOGY_JSON,
    get_shot_types_list,
    get_chinese_name,
    ALL_SHOT_TYPES
)

router = APIRouter(prefix="/v1/terminology", tags=["terminology"])


@router.get("/shots")
async def get_shot_terminology() -> Dict[str, Any]:
    """
    获取所有镜头术语
    Get all shot terminology
    """
    return {
        "status": "success",
        "data": SHOT_TERMINOLOGY_JSON
    }


@router.get("/shots/list")
async def get_shot_types() -> Dict[str, Any]:
    """
    获取所有镜头类型列表
    Get all shot types list
    """
    return {
        "status": "success",
        "data": get_shot_types_list()
    }


@router.get("/shots/{shot_key}")
async def get_shot_detail(shot_key: str) -> Dict[str, Any]:
    """
    获取单个镜头术语详情
    Get single shot terminology detail
    """
    shot_info = ALL_SHOT_TYPES.get(shot_key)
    
    if not shot_info:
        return {
            "status": "error",
            "message": f"镜头类型 '{shot_key}' 不存在"
        }
    
    return {
        "status": "success",
        "data": shot_info
    }


@router.get("/shots/translate/{shot_key}")
async def translate_shot_name(shot_key: str) -> Dict[str, Any]:
    """
    翻译镜头类型为中文名称
    Translate shot type to Chinese name
    """
    chinese_name = get_chinese_name(shot_key)
    
    return {
        "status": "success",
        "data": {
            "key": shot_key,
            "chinese_name": chinese_name
        }
    }

