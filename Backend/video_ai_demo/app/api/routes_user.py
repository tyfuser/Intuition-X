"""用户管理API路由"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

from ..core.auth import User, get_current_user
from ..core.response import success_response, error_response, ErrorCode
from ..core.logging import logger


router = APIRouter(prefix="/user", tags=["用户管理"])


class SubscriptionInfo(BaseModel):
    """订阅信息"""
    plan: str = Field(..., description="套餐：free, pro, enterprise")
    expiresAt: str = Field(..., description="到期时间")
    features: List[str] = Field(..., description="功能列表")


class UsageQuota(BaseModel):
    """配额使用情况"""
    daily: int = Field(..., description="每日配额")
    remaining: int = Field(..., description="剩余配额")


class UsageInfo(BaseModel):
    """使用情况"""
    videosAnalyzed: int = Field(..., description="已分析视频数")
    scriptsGenerated: int = Field(..., description="已生成脚本数")
    quota: UsageQuota


class UserProfile(BaseModel):
    """用户资料"""
    id: str
    email: str
    name: str
    avatar: str
    subscription: SubscriptionInfo
    usage: UsageInfo
    createdAt: str
    lastLoginAt: str


class UpdateProfileRequest(BaseModel):
    """更新用户信息请求"""
    name: Optional[str] = None
    avatar: Optional[str] = None


class QuotaInfo(BaseModel):
    """配额信息"""
    plan: str
    quota: dict
    features: dict


@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    获取用户信息
    
    返回当前登录用户的完整资料
    """
    try:
        # 构建用户资料
        # 实际应从数据库查询
        profile = UserProfile(
            id=current_user.id,
            email=current_user.email,
            name=current_user.name,
            avatar=current_user.avatar,
            subscription=SubscriptionInfo(
                plan=current_user.subscription,
                expiresAt=(datetime.now().replace(year=datetime.now().year + 1)).isoformat(),
                features=[
                    "无限视频分析",
                    "AI脚本生成",
                    "知识库访问",
                    "导出高清视频",
                    "优先处理队列"
                ] if current_user.subscription == "pro" else [
                    "每日5次视频分析",
                    "基础知识库访问"
                ]
            ),
            usage=UsageInfo(
                videosAnalyzed=128,
                scriptsGenerated=45,
                quota=UsageQuota(
                    daily=100 if current_user.subscription == "pro" else 5,
                    remaining=73 if current_user.subscription == "pro" else 3
                )
            ),
            createdAt="2024-01-01T00:00:00Z",
            lastLoginAt=datetime.now().isoformat()
        )
        
        return success_response(data=profile.dict())
    
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "获取用户信息失败"
        )


@router.patch("/profile")
async def update_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user)
):
    """
    更新用户信息
    
    允许用户更新姓名和头像
    """
    try:
        # 实际应更新数据库
        updated_fields = {}
        
        if request.name:
            updated_fields["name"] = request.name
        
        if request.avatar:
            updated_fields["avatar"] = request.avatar
        
        logger.info(f"用户 {current_user.id} 更新了资料: {updated_fields}")
        
        return success_response(
            data=updated_fields,
            message="更新成功"
        )
    
    except Exception as e:
        logger.error(f"更新用户信息失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "更新用户信息失败"
        )


@router.get("/quota")
async def get_quota(current_user: User = Depends(get_current_user)):
    """
    获取用户配额信息
    
    返回用户的使用配额和功能权限
    """
    try:
        quota_info = QuotaInfo(
            plan=current_user.subscription,
            quota={
                "daily": 100 if current_user.subscription == "pro" else 5,
                "used": 27,
                "remaining": 73 if current_user.subscription == "pro" else 3,
                "resetAt": datetime.now().replace(hour=0, minute=0, second=0).isoformat()
            },
            features={
                "videoAnalysis": True,
                "scriptGeneration": current_user.subscription != "free",
                "slideshow": current_user.subscription != "free",
                "aiChat": current_user.subscription == "enterprise"
            }
        )
        
        return success_response(data=quota_info.dict())
    
    except Exception as e:
        logger.error(f"获取配额信息失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "获取配额信息失败"
        )


@router.post("/upgrade")
async def upgrade_subscription(
    plan: str = "pro",
    current_user: User = Depends(get_current_user)
):
    """
    升级订阅
    
    将用户订阅升级到指定套餐
    """
    try:
        if plan not in ["pro", "enterprise"]:
            return error_response(
                ErrorCode.INVALID_REQUEST,
                "无效的套餐类型"
            )
        
        # 实际应处理支付和订阅逻辑
        logger.info(f"用户 {current_user.id} 升级订阅到 {plan}")
        
        return success_response(
            data={"plan": plan, "upgraded": True},
            message=f"成功升级到 {plan} 套餐"
        )
    
    except Exception as e:
        logger.error(f"升级订阅失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "升级订阅失败"
        )


@router.get("/stats")
async def get_user_stats(current_user: User = Depends(get_current_user)):
    """
    获取用户统计数据
    
    返回用户的各项使用统计
    """
    try:
        stats = {
            "totalVideosAnalyzed": 128,
            "totalScriptsGenerated": 45,
            "totalKnowledgeItems": 67,
            "totalSavedTime": "340h",
            "avgScore": 88.5,
            "weeklyActivity": [
                {"day": "Mon", "count": 12},
                {"day": "Tue", "count": 18},
                {"day": "Wed", "count": 8},
                {"day": "Thu", "count": 22},
                {"day": "Fri", "count": 15},
                {"day": "Sat", "count": 5},
                {"day": "Sun", "count": 10}
            ]
        }
        
        return success_response(data=stats)
    
    except Exception as e:
        logger.error(f"获取用户统计失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "获取用户统计失败"
        )

