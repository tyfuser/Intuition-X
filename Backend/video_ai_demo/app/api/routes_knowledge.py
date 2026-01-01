"""知识库API路由"""
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

from ..core.auth import User, get_current_user, optional_user
from ..core.response import success_response, error_response, ErrorCode
from ..core.logging import logger


router = APIRouter(prefix="/knowledge", tags=["知识库"])


class KBCategory(str, Enum):
    """知识库分类"""
    HOOKS = "hooks"
    NARRATIVE = "narrative"
    STYLE = "style"
    BGM = "bgm"
    FINGERPRINTS = "fingerprints"


class KBItem(BaseModel):
    """知识库条目"""
    id: str
    category: KBCategory
    title: str
    description: str
    tags: List[str]
    usageCount: int = Field(..., description="使用次数")
    rating: float = Field(..., ge=0, le=5, description="评分")
    previewColor: Optional[str] = Field(None, description="预览卡片渐变色")
    content: Optional[str] = Field(None, description="详细内容")
    examples: Optional[List[str]] = Field(None, description="示例列表")


class KBItemsResponse(BaseModel):
    """知识库列表响应"""
    items: List[KBItem]
    total: int
    page: int
    limit: int


# 模拟知识库数据
MOCK_KB_ITEMS = [
    KBItem(
        id="kb_001",
        category=KBCategory.HOOKS,
        title="视觉反差钩子",
        description="前0.5秒展示极端对比画面，迅速建立视觉张力",
        tags=["高点击", "强反转", "生活"],
        usageCount=1240,
        rating=4.9,
        previewColor="from-orange-500 to-red-500",
        content="通过前后画面的强烈对比（黑白vs彩色、简陋vs豪华等）瞬间抓住观众注意力。适用于改造类、对比类内容。",
        examples=[
            "改造前：破旧老房 → 改造后：现代豪宅",
            "素颜 → 化妆后",
            "普通食材 → 精致料理"
        ]
    ),
    KBItem(
        id="kb_002",
        category=KBCategory.HOOKS,
        title="悬念设置钩子",
        description="开场抛出问题或悬念，激发观众好奇心",
        tags=["高完播", "强互动"],
        usageCount=980,
        rating=4.7,
        previewColor="from-purple-500 to-pink-500",
        content="通过设置悬念、抛出问题的方式，让观众产生'想知道答案'的心理，从而提高完播率。",
        examples=[
            "你绝对想不到最后发生了什么...",
            "这个方法让我月入3万,但90%的人都不知道",
            "千万别在晚上做这件事..."
        ]
    ),
    KBItem(
        id="kb_003",
        category=KBCategory.NARRATIVE,
        title="AIDA营销结构",
        description="Attention → Interest → Desire → Action",
        tags=["营销", "转化"],
        usageCount=756,
        rating=4.8,
        previewColor="from-blue-500 to-cyan-500",
        content="经典的营销叙事结构：注意力吸引 → 兴趣培养 → 欲望激发 → 行动号召。适合带货、引流类视频。",
        examples=[
            "开场：展示产品效果（Attention）",
            "中段：讲解产品特点（Interest）",
            "高潮：展示使用场景（Desire）",
            "结尾：限时优惠引导（Action）"
        ]
    ),
    KBItem(
        id="kb_004",
        category=KBCategory.STYLE,
        title="快节奏剪辑",
        description="高频率镜头切换，保持观众注意力",
        tags=["短视频", "抖音"],
        usageCount=1456,
        rating=4.6,
        previewColor="from-green-500 to-teal-500",
        content="通过快速的镜头切换（0.5-2秒一切）、卡点配乐、特效转场等手法，营造紧张刺激的观看体验。",
        examples=[
            "每0.5秒切换一个场景",
            "配合音乐节奏进行卡点剪辑",
            "使用快速缩放、旋转等转场效果"
        ]
    ),
    KBItem(
        id="kb_005",
        category=KBCategory.BGM,
        title="史诗级氛围音乐",
        description="适合大场面、震撼内容的背景音乐",
        tags=["震撼", "大气"],
        usageCount=892,
        rating=4.5,
        previewColor="from-yellow-500 to-orange-500",
        content="使用交响乐、电影配乐等史诗感强的音乐，配合大场面画面，营造震撼效果。",
        examples=[
            "Two Steps From Hell - Victory",
            "Hans Zimmer - Time",
            "Audiomachine - Guardians at the Gate"
        ]
    ),
    KBItem(
        id="kb_006",
        category=KBCategory.FINGERPRINTS,
        title="网红滤镜风格",
        description="统一的调色风格，形成个人IP标识",
        tags=["IP", "辨识度"],
        usageCount=1123,
        rating=4.4,
        previewColor="from-pink-500 to-rose-500",
        content="通过固定的调色方案（如复古胶片、赛博朋克、日系小清新等），让观众一眼认出你的视频。",
        examples=[
            "复古胶片：降低饱和度、增加颗粒感",
            "赛博朋克：高饱和度蓝紫色调",
            "日系小清新：高亮度、柔和色调"
        ]
    )
]


@router.get("/items")
async def get_knowledge_items(
    category: Optional[KBCategory] = Query(None, description="筛选分类"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(15, ge=1, le=50, description="每页数量"),
    current_user: Optional[User] = Depends(optional_user)
):
    """
    获取知识库条目列表
    
    支持分类筛选和关键词搜索
    """
    try:
        # 筛选
        items = MOCK_KB_ITEMS
        
        if category:
            items = [item for item in items if item.category == category]
        
        if search:
            search_lower = search.lower()
            items = [
                item for item in items
                if search_lower in item.title.lower() 
                or search_lower in item.description.lower()
                or any(search_lower in tag.lower() for tag in item.tags)
            ]
        
        # 分页
        total = len(items)
        start = (page - 1) * limit
        end = start + limit
        items = items[start:end]
        
        response = KBItemsResponse(
            items=items,
            total=total,
            page=page,
            limit=limit
        )
        
        return success_response(data=response.dict())
    
    except Exception as e:
        logger.error(f"获取知识库列表失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "获取知识库列表失败"
        )


@router.get("/items/{item_id}")
async def get_knowledge_item(
    item_id: str,
    current_user: Optional[User] = Depends(optional_user)
):
    """
    获取单个知识库条目详情
    
    返回完整的条目信息，包括详细内容和示例
    """
    try:
        # 查找条目
        item = next((item for item in MOCK_KB_ITEMS if item.id == item_id), None)
        
        if not item:
            return error_response(
                ErrorCode.RESOURCE_NOT_FOUND,
                f"知识库条目 {item_id} 不存在"
            )
        
        return success_response(data=item.dict())
    
    except Exception as e:
        logger.error(f"获取知识库条目失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "获取知识库条目失败"
        )


@router.post("/items/{item_id}/bookmark")
async def bookmark_item(
    item_id: str,
    current_user: Optional[User] = Depends(optional_user)
):
    """
    添加到收藏
    
    将知识库条目添加到用户的收藏夹
    """
    try:
        # 检查条目是否存在
        item = next((item for item in MOCK_KB_ITEMS if item.id == item_id), None)
        
        if not item:
            return error_response(
                ErrorCode.RESOURCE_NOT_FOUND,
                f"知识库条目 {item_id} 不存在"
            )
        
        # 实际应该保存到数据库
        # 这里为演示，直接返回成功
        
        user_id = current_user.id if current_user else "anonymous"
        logger.info(f"用户 {user_id} 收藏了知识库条目 {item_id}")
        
        return success_response(
            data={"bookmarked": True, "item_id": item_id},
            message="收藏成功"
        )
    
    except Exception as e:
        logger.error(f"收藏失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "收藏失败"
        )


@router.delete("/items/{item_id}/bookmark")
async def unbookmark_item(
    item_id: str,
    current_user: Optional[User] = Depends(optional_user)
):
    """
    取消收藏
    
    从用户的收藏夹中移除知识库条目
    """
    try:
        user_id = current_user.id if current_user else "anonymous"
        logger.info(f"用户 {user_id} 取消收藏知识库条目 {item_id}")
        
        return success_response(
            data={"bookmarked": False, "item_id": item_id},
            message="已取消收藏"
        )
    
    except Exception as e:
        logger.error(f"取消收藏失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "取消收藏失败"
        )

