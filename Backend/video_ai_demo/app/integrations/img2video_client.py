"""图生视频客户端适配层"""
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..core.config import settings
from ..core.errors import AppError
from ..core.logging import logger


class Img2VideoClient:
    """图生视频客户端（预留接口）"""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.base_url = base_url or settings.img2video_base_url
        self.api_key = api_key or settings.img2video_api_key
        self.model = model or settings.img2video_model
    
    async def generate_virtual_motion(
        self,
        keyframes: List[str],
        motion_recipe: Dict[str, Any],
        output_path: str
    ) -> Dict[str, Any]:
        """
        生成虚拟运镜preview
        
        Args:
            keyframes: 关键帧图片路径列表
            motion_recipe: 运镜配方，如 {"type": "push_in", "strength": 0.18, "duration_ms": 3000}
            output_path: 输出视频路径
        
        Returns:
            结果字典，包含视频路径等信息
        """
        logger.info(f"生成虚拟运镜: {motion_recipe['type']}")
        
        if not self.api_key:
            logger.warning("未配置图生视频API，返回模拟结果")
            return self._mock_generate(keyframes, motion_recipe, output_path)
        
        # TODO: 实际调用图生视频API
        raise AppError("图生视频API尚未实现")
    
    def _mock_generate(
        self,
        keyframes: List[str],
        motion_recipe: Dict[str, Any],
        output_path: str
    ) -> Dict[str, Any]:
        """模拟生成（Demo阶段）"""
        
        # 创建一个占位文件
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).touch()
        
        logger.info(f"模拟生成视频: {output_path}")
        
        return {
            "success": True,
            "video_path": output_path,
            "motion_type": motion_recipe.get("type"),
            "duration_ms": motion_recipe.get("duration_ms", 3000),
            "message": "Demo阶段：模拟生成（实际未调用图生视频API）"
        }

