"""认证和授权模块"""
from typing import Optional
from fastapi import Header, HTTPException, Depends
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

from .response import ErrorCode, error_response


# JWT配置
SECRET_KEY = "your-secret-key-change-in-production"  # 生产环境应使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7天


class User(BaseModel):
    """用户模型"""
    id: str
    email: str
    name: str
    avatar: str = ""
    subscription: str = "free"  # free, pro, enterprise


class TokenData(BaseModel):
    """Token数据"""
    user_id: str
    email: str
    exp: Optional[datetime] = None


def create_access_token(user: User) -> str:
    """创建访问令牌"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "user_id": user.id,
        "email": user.email,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """验证令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        email: str = payload.get("email")
        if user_id is None or email is None:
            return None
        return TokenData(user_id=user_id, email=email)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None


async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> User:
    """获取当前用户（依赖注入）"""
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail=error_response(ErrorCode.UNAUTHORIZED, "未提供认证信息")
        )
    
    # 解析 Bearer token
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail=error_response(ErrorCode.UNAUTHORIZED, "无效的认证方案")
            )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail=error_response(ErrorCode.UNAUTHORIZED, "无效的Authorization头")
        )
    
    # 验证token
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=401,
            detail=error_response(ErrorCode.INVALID_TOKEN, "Token无效或已过期")
        )
    
    # 返回用户信息（实际应从数据库查询）
    # 这里为了演示，返回模拟数据
    return User(
        id=token_data.user_id,
        email=token_data.email,
        name="演示用户",
        avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=" + token_data.user_id,
        subscription="pro"
    )


async def optional_user(
    authorization: Optional[str] = Header(None)
) -> Optional[User]:
    """可选的用户认证（不强制）"""
    if not authorization:
        return None
    
    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None

