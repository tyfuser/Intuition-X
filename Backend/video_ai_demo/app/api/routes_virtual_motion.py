"""虚拟运镜相关API路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
import json
import asyncio

from ..db.session import get_db
from ..db.repo import JobRepository, VirtualMotionJobRepository
from ..db.models import VirtualMotionJob, JobStatus
from ..integrations.img2video_client import Img2VideoClient
from ..core.config import settings
from ..core.logging import logger


router = APIRouter(prefix="/v1/video-analysis/virtual-motion", tags=["virtual-motion"])


# ===== 请求模型 =====

class MotionRecipe(BaseModel):
    """运镜配方"""
    type: str = Field(..., description="push_in, pull_out, pan, tilt等")
    strength: float = Field(default=0.18, ge=0.0, le=1.0)
    duration_ms: int = Field(default=3000, ge=1000, le=10000)
    direction: Optional[str] = None  # pan/tilt的方向


class VirtualMotionOptions(BaseModel):
    """虚拟运镜选项"""
    provider: str = "default"
    model: Optional[str] = None


class CreateVirtualMotionJobRequest(BaseModel):
    """创建虚拟运镜Job请求"""
    parent_job_id: str
    asset_role: str = Field(..., description="target 或 user")
    segment_id: str
    motion_recipe: MotionRecipe
    options: VirtualMotionOptions = Field(default_factory=VirtualMotionOptions)


class CreateVirtualMotionJobResponse(BaseModel):
    """创建虚拟运镜Job响应"""
    subtask_id: str
    status: str
    status_url: str


# ===== 响应模型 =====

class VirtualMotionJobResponse(BaseModel):
    """虚拟运镜Job响应"""
    subtask_id: str
    parent_job_id: str
    status: str
    asset_role: str
    segment_id: str
    motion_recipe: Dict[str, Any]
    result_video_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None


# ===== 路由处理 =====

@router.post("/jobs", response_model=CreateVirtualMotionJobResponse)
async def create_virtual_motion_job(request: CreateVirtualMotionJobRequest):
    """创建虚拟运镜子任务"""
    
    logger.info(f"创建虚拟运镜Job: parent={request.parent_job_id}, segment={request.segment_id}")
    
    # 校验parent job存在
    with get_db() as db:
        job_repo = JobRepository(db)
        parent_job = job_repo.get(request.parent_job_id)
        
        if not parent_job:
            raise HTTPException(status_code=404, detail=f"父Job {request.parent_job_id} 不存在")
        
        if parent_job.status != JobStatus.SUCCEEDED:
            raise HTTPException(status_code=400, detail="父Job尚未完成")
    
    # 生成子任务ID
    subtask_id = f"vm_{uuid.uuid4().hex[:12]}"
    
    # 创建虚拟运镜Job记录
    with get_db() as db:
        vm_repo = VirtualMotionJobRepository(db)
        
        vm_job = VirtualMotionJob(
            id=subtask_id,
            parent_job_id=request.parent_job_id,
            status=JobStatus.QUEUED,
            asset_role=request.asset_role,
            segment_id=request.segment_id,
            motion_recipe_json=json.dumps(request.motion_recipe.dict(), ensure_ascii=False)
        )
        
        vm_repo.create(vm_job)
    
    # 异步执行
    asyncio.create_task(_run_virtual_motion_job(
        subtask_id,
        request.parent_job_id,
        request.asset_role,
        request.segment_id,
        request.motion_recipe.dict()
    ))
    
    return CreateVirtualMotionJobResponse(
        subtask_id=subtask_id,
        status="queued",
        status_url=f"/v1/video-analysis/virtual-motion/jobs/{subtask_id}"
    )


@router.get("/jobs/{subtask_id}", response_model=VirtualMotionJobResponse)
async def get_virtual_motion_job(subtask_id: str):
    """查询虚拟运镜Job状态"""
    
    with get_db() as db:
        vm_repo = VirtualMotionJobRepository(db)
        vm_job = vm_repo.get(subtask_id)
        
        if not vm_job:
            raise HTTPException(status_code=404, detail=f"虚拟运镜Job {subtask_id} 不存在")
        
        motion_recipe = {}
        if vm_job.motion_recipe_json:
            try:
                motion_recipe = json.loads(vm_job.motion_recipe_json)
            except json.JSONDecodeError:
                pass
        
        return VirtualMotionJobResponse(
            subtask_id=vm_job.id,
            parent_job_id=vm_job.parent_job_id,
            status=vm_job.status.value,
            asset_role=vm_job.asset_role,
            segment_id=vm_job.segment_id,
            motion_recipe=motion_recipe,
            result_video_path=vm_job.result_video_path,
            error_message=vm_job.error_message,
            created_at=vm_job.created_at,
            updated_at=vm_job.updated_at,
            completed_at=vm_job.completed_at
        )


# ===== 后台任务 =====

async def _run_virtual_motion_job(
    subtask_id: str,
    parent_job_id: str,
    asset_role: str,
    segment_id: str,
    motion_recipe: Dict[str, Any]
):
    """运行虚拟运镜Job（后台任务）"""
    
    logger.info(f"开始执行虚拟运镜Job {subtask_id}")
    
    try:
        # 更新状态为running
        with get_db() as db:
            vm_repo = VirtualMotionJobRepository(db)
            vm_repo.update_status(subtask_id, JobStatus.RUNNING)
        
        # 获取父Job的结果，找到对应的keyframes
        keyframes = await _get_segment_keyframes(parent_job_id, asset_role, segment_id)
        
        if not keyframes:
            raise Exception(f"未找到segment {segment_id} 的关键帧")
        
        # 准备输出路径
        output_dir = settings.data_dir / "jobs" / parent_job_id / "previews"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / f"{subtask_id}.mp4")
        
        # 调用图生视频API
        client = Img2VideoClient()
        result = await client.generate_virtual_motion(
            keyframes,
            motion_recipe,
            output_path
        )
        
        # 更新状态为succeeded
        with get_db() as db:
            vm_repo = VirtualMotionJobRepository(db)
            vm_repo.update_status(
                subtask_id,
                JobStatus.SUCCEEDED,
                result_video_path=result.get("video_path")
            )
        
        logger.info(f"虚拟运镜Job {subtask_id} 完成")
    
    except Exception as e:
        logger.error(f"虚拟运镜Job {subtask_id} 失败: {str(e)}", exc_info=True)
        
        with get_db() as db:
            vm_repo = VirtualMotionJobRepository(db)
            vm_repo.update_status(
                subtask_id,
                JobStatus.FAILED,
                error_message=str(e)
            )


async def _get_segment_keyframes(
    parent_job_id: str,
    asset_role: str,
    segment_id: str
) -> list:
    """获取segment的关键帧"""
    
    with get_db() as db:
        job_repo = JobRepository(db)
        parent_job = job_repo.get(parent_job_id)
        
        if not parent_job or not parent_job.result_json:
            return []
        
        try:
            result = json.loads(parent_job.result_json)
            
            # 从结果中提取keyframes
            asset_data = result.get(asset_role, {})
            keyframes = asset_data.get("keyframes", [])
            
            # 找到匹配的keyframe
            matching_keyframes = [
                kf["keyframe_path"]
                for kf in keyframes
                if kf["segment_id"] == segment_id
            ]
            
            return matching_keyframes
        
        except json.JSONDecodeError:
            return []

