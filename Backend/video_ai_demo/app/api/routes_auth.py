"""认证相关API路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from ..core.auth import User, create_access_token
from ..core.response import success_response, error_response, ErrorCode
from ..core.logging import logger


router = APIRouter(prefix="/auth", tags=["认证"])


class LoginRequest(BaseModel):
    """登录请求"""
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    """登录响应数据"""
    user: User
    token: str = Field(..., description="JWT Token")
    expiresIn: int = Field(default=604800, description="过期时间（秒）")


@router.post("/login")
async def login(request: LoginRequest):
    """
    用户登录
    
    返回用户信息和访问令牌
    """
    try:
        # 实际应验证数据库中的用户
        # 这里为演示目的，使用简单的验证逻辑
        if request.password != "123456":
            return error_response(
                ErrorCode.UNAUTHORIZED,
                "邮箱或密码错误"
            )
        
        # 创建用户对象
        user = User(
            id=f"user_{request.email.split('@')[0]}",
            email=request.email,
            name=request.email.split('@')[0].title(),
            avatar=f"https://api.dicebear.com/7.x/avataaars/svg?seed={request.email}",
            subscription="pro"
        )
        
        # 生成token
        token = create_access_token(user)
        
        logger.info(f"用户登录成功: {user.email}")
        
        return success_response(
            data=LoginResponse(
                user=user,
                token=token,
                expiresIn=604800  # 7天
            ).dict(),
            message="登录成功"
        )
    
    except Exception as e:
        logger.error(f"登录失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "登录失败，请稍后重试"
        )


@router.post("/register")
async def register(request: LoginRequest):
    """
    用户注册
    
    创建新用户账户
    """
    try:
        # 检查邮箱是否已存在（实际应查询数据库）
        # 这里为演示目的，简化处理
        
        # 创建用户对象
        user = User(
            id=f"user_{request.email.split('@')[0]}",
            email=request.email,
            name=request.email.split('@')[0].title(),
            avatar=f"https://api.dicebear.com/7.x/avataaars/svg?seed={request.email}",
            subscription="free"
        )
        
        # 生成token
        token = create_access_token(user)
        
        logger.info(f"用户注册成功: {user.email}")
        
        return success_response(
            data=LoginResponse(
                user=user,
                token=token,
                expiresIn=604800
            ).dict(),
            message="注册成功"
        )
    
    except Exception as e:
        logger.error(f"注册失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "注册失败，请稍后重试"
        )


@router.post("/logout")
async def logout():
    """
    用户登出
    
    客户端应删除本地存储的token
    """
    return success_response(message="登出成功")

