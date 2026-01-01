"""仪表板API路由"""
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import json

from ..core.auth import User, get_current_user, optional_user
from ..core.response import success_response, error_response, ErrorCode
from ..db.session import get_db
from ..db.repo import JobRepository
from ..db.models import JobStatus
from ..core.logging import logger


router = APIRouter(prefix="/dashboard", tags=["仪表板"])


class StatItem(BaseModel):
    """统计项"""
    label: str = Field(..., description="标签")
    value: str = Field(..., description="数值")
    icon: str = Field(..., description="图标名称")
    color: str = Field(..., description="颜色类名")
    bg: str = Field(..., description="背景类名")


class StatsResponse(BaseModel):
    """统计数据响应"""
    stats: List[StatItem]


class ProjectSummary(BaseModel):
    """项目摘要"""
    id: str
    title: str
    thumbnail: str = Field(..., description="封面图URL")
    timestamp: str = Field(..., description="时间描述")
    type: str = Field(..., description="项目类型")
    score: int = Field(..., ge=0, le=100, description="评分")
    status: str = Field(..., description="状态")
    tags: List[str] = Field(default_factory=list, description="标签")
    radarData: Optional[List[dict]] = Field(None, description="雷达图数据")


class ProjectsResponse(BaseModel):
    """项目列表响应"""
    projects: List[ProjectSummary]
    total: int
    page: int
    limit: int


class ScheduleDay(BaseModel):
    """日程热力图日期"""
    day: str = Field(..., description="星期")
    intensity: int = Field(..., ge=0, le=100, description="强度")


class TaskItem(BaseModel):
    """任务项"""
    label: str
    active: bool
    color: str


class ScheduleResponse(BaseModel):
    """日程响应"""
    schedule: List[ScheduleDay]
    tasks: List[TaskItem]


@router.get("/stats")
async def get_stats(current_user: Optional[User] = Depends(optional_user)):
    """
    获取统计数据
    
    返回用户的各项统计指标
    """
    try:
        with get_db() as db:
            job_repo = JobRepository(db)
            
            # 获取统计数据
            total_jobs = job_repo.count_by_status()
            completed_count = total_jobs.get(JobStatus.SUCCEEDED, 0)
            
            # 计算总时长（从已完成的任务中统计）
            total_duration = 0
            jobs = job_repo.list_by_status(JobStatus.SUCCEEDED, limit=1000)
            
            for job in jobs:
                if job.result_json:
                    try:
                        result = json.loads(job.result_json)
                        target = result.get("target", {})
                        segments = target.get("segments", [])
                        if segments:
                            duration_sec = segments[-1].get("end_ms", 0) / 1000
                            total_duration += duration_sec
                    except:
                        pass
            
            # 构建统计数据
            stats = StatsResponse(
                stats=[
                    StatItem(
                        label="已分析视频",
                        value=str(completed_count),
                        icon="FileVideo",
                        color="text-blue-400",
                        bg="bg-blue-400/10"
                    ),
                    StatItem(
                        label="爆款基因库",
                        value=str(completed_count * 15),  # 假设每个视频提取15个基因
                        icon="Zap",
                        color="text-yellow-400",
                        bg="bg-yellow-400/10"
                    ),
                    StatItem(
                        label="节省创作时长",
                        value=f"{int(total_duration / 60)}h",
                        icon="Timer",
                        color="text-green-400",
                        bg="bg-green-400/10"
                    ),
                    StatItem(
                        label="平均分析分",
                        value="88.5",
                        icon="TrendingUp",
                        color="text-purple-400",
                        bg="bg-purple-400/10"
                    )
                ]
            )
            
            return success_response(data=stats.dict())
    
    except Exception as e:
        logger.error(f"获取统计数据失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "获取统计数据失败"
        )


@router.get("/projects")
async def get_projects(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="筛选状态"),
    sortBy: str = Query("timestamp", description="排序方式"),
    current_user: Optional[User] = Depends(optional_user)
):
    """
    获取项目列表
    
    返回用户的视频分析项目
    """
    try:
        with get_db() as db:
            job_repo = JobRepository(db)
            
            # 获取任务列表
            offset = (page - 1) * limit
            jobs = job_repo.list_history(limit=limit, offset=offset)
            total = job_repo.count_all()
            
            # 转换为项目摘要
            projects = []
            for job in jobs:
                # 解析结果
                segment_count = 0
                duration_sec = 0
                
                if job.result_json:
                    try:
                        result = json.loads(job.result_json)
                        target = result.get("target", {})
                        segments = target.get("segments", [])
                        segment_count = len(segments)
                        if segments:
                            duration_sec = segments[-1].get("end_ms", 0) / 1000
                    except:
                        pass
                
                # 计算时间描述
                time_diff = datetime.now() - job.created_at
                if time_diff.days > 0:
                    timestamp = f"{time_diff.days}天前"
                elif time_diff.seconds > 3600:
                    timestamp = f"{time_diff.seconds // 3600}小时前"
                elif time_diff.seconds > 60:
                    timestamp = f"{time_diff.seconds // 60}分钟前"
                else:
                    timestamp = "刚刚"
                
                # 计算评分（基于segments数量和特征完整性）
                score = min(100, 60 + segment_count * 5)
                
                project = ProjectSummary(
                    id=job.id,
                    title=job.title or "未命名视频",
                    thumbnail=job.thumbnail_url or f"/data/jobs/{job.id}/target/scene_keyframes/001-keyframe.jpg",
                    timestamp=timestamp,
                    type="视频分析" if job.mode.value == "learn" else "视频对比",
                    score=score,
                    status=job.status.value,
                    tags=["AI分析", job.mode.value],
                    radarData=[
                        {"subject": "钩子强度", "value": score - 10, "fullMark": 100},
                        {"subject": "情绪张力", "value": score - 20, "fullMark": 100},
                        {"subject": "视觉冲击", "value": score, "fullMark": 100},
                        {"subject": "叙事逻辑", "value": score - 15, "fullMark": 100},
                        {"subject": "转化潜力", "value": score - 5, "fullMark": 100},
                        {"subject": "创新指数", "value": score - 10, "fullMark": 100}
                    ]
                )
                
                projects.append(project)
            
            response = ProjectsResponse(
                projects=projects,
                total=total,
                page=page,
                limit=limit
            )
            
            return success_response(data=response.dict())
    
    except Exception as e:
        logger.error(f"获取项目列表失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "获取项目列表失败"
        )


@router.get("/schedule")
async def get_schedule(current_user: Optional[User] = Depends(optional_user)):
    """
    获取日程热力图
    
    返回用户的任务日程（基于最近7天的真实数据）
    """
    try:
        with get_db() as db:
            job_repo = JobRepository(db)
            
            # 获取过去7天的所有任务
            now = datetime.now()
            seven_days_ago = now - timedelta(days=7)
            
            # 统计每天的任务数量
            day_counts = defaultdict(int)
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            
            # 获取所有任务
            all_jobs = job_repo.list_history(limit=1000)
            
            # 统计过去7天每天的任务数
            for job in all_jobs:
                if job.created_at and job.created_at >= seven_days_ago:
                    day_of_week = job.created_at.weekday()  # 0=Monday, 6=Sunday
                    day_counts[day_of_week] += 1
            
            # 找出最大值用于归一化
            max_count = max(day_counts.values()) if day_counts else 1
            
            # 构建日程数据
            schedule_data = []
            for i, day_name in enumerate(day_names):
                count = day_counts.get(i, 0)
                # 归一化到0-100
                intensity = int((count / max_count) * 100) if max_count > 0 else 0
                schedule_data.append(ScheduleDay(day=day_name, intensity=intensity))
            
            # 统计不同状态的任务数量
            status_counts = job_repo.count_by_status()
            queued_count = status_counts.get(JobStatus.QUEUED, 0)
            running_count = status_counts.get(JobStatus.RUNNING, 0)
            succeeded_count = status_counts.get(JobStatus.SUCCEEDED, 0)
            
            # 构建任务列表
            tasks = []
            if queued_count > 0:
                tasks.append(TaskItem(
                    label=f"待解析: {queued_count}个视频",
                    active=True,
                    color="bg-indigo-500"
                ))
            if running_count > 0:
                tasks.append(TaskItem(
                    label=f"分析中: {running_count}个视频",
                    active=True,
                    color="bg-green-500"
                ))
            if succeeded_count > 0:
                tasks.append(TaskItem(
                    label=f"已完成: {succeeded_count}个视频",
                    active=False,
                    color="bg-gray-500"
                ))
            
            # 如果没有任何任务，显示提示
            if not tasks:
                tasks.append(TaskItem(
                    label="暂无任务",
                    active=False,
                    color="bg-gray-400"
                ))
            
            schedule = ScheduleResponse(
                schedule=schedule_data,
                tasks=tasks
            )
            
            return success_response(data=schedule.dict())
    
    except Exception as e:
        logger.error(f"获取日程失败: {str(e)}")
        return error_response(
            ErrorCode.INTERNAL_ERROR,
            "获取日程失败"
        )

