"""多模态LLM拆解步骤"""
from typing import Dict, Any, List

from ...integrations.mm_llm_client import MMHLLMClient, FrameInput
from ...core.logging import logger


async def decompose_with_mm_llm(
    frames_index: List[Dict[str, Any]],
    llm_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    使用多模态LLM拆解视频
    
    Args:
        frames_index: 帧索引列表
        llm_config: LLM配置，如 {"provider": "...", "model": "...", "enabled_modules": [...]}
    
    Returns:
        拆解结果：
        {
            "segments": [
                {
                    "segment_id": "seg_001",
                    "start_ms": 0,
                    "end_ms": 3500,
                    "duration_ms": 3500,
                    "features": [...]
                }
            ]
        }
    """
    logger.info(f"使用多模态LLM拆解视频，共{len(frames_index)}帧")
    
    # 准备帧输入
    frame_inputs = [
        FrameInput(ts_ms=frame["ts_ms"], image_path=frame["path"])
        for frame in frames_index
    ]
    
    # 创建LLM客户端
    client = MMHLLMClient(
        model=llm_config.get("model")
    )
    
    # 准备提示词配置
    prompt_config = {
        "enabled_modules": llm_config.get("enabled_modules", [
            "camera_motion", "lighting", "color_grading"
        ])
    }
    
    # 调用拆解
    result = await client.decompose_video(frame_inputs, prompt_config)
    
    logger.info(f"拆解完成，共{len(result['segments'])}个镜头")
    
    return result

