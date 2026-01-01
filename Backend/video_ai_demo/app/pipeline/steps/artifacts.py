"""生成产物步骤"""
from pathlib import Path
from typing import Dict, Any, List
import shutil

from ...core.logging import logger


def generate_artifacts(
    segments: List[Dict[str, Any]],
    frames_index: List[Dict[str, Any]],
    output_dir: Path,
    asset_role: str = "target"
) -> Dict[str, Any]:
    """
    生成产物：为每个segment提取关键帧
    
    Returns:
        {
            "keyframes": [
                {
                    "segment_id": str,
                    "keyframe_path": str,
                    "ts_ms": float
                }
            ]
        }
    """
    logger.info(f"生成产物，共{len(segments)}个镜头")
    
    keyframes_dir = output_dir / "keyframes"
    keyframes_dir.mkdir(parents=True, exist_ok=True)
    
    keyframes = []
    
    for segment in segments:
        segment_id = segment["segment_id"]
        start_ms = segment["start_ms"]
        end_ms = segment["end_ms"]
        
        # 选择中间帧作为关键帧
        mid_ms = (start_ms + end_ms) / 2
        
        # 找到最接近的帧
        closest_frame = _find_closest_frame(frames_index, mid_ms)
        
        if closest_frame:
            # 复制为关键帧
            src_path = Path(closest_frame["path"])
            dst_path = keyframes_dir / f"{asset_role}_{segment_id}_key.jpg"
            
            shutil.copy2(src_path, dst_path)
            
            keyframes.append({
                "segment_id": segment_id,
                "keyframe_path": str(dst_path),
                "ts_ms": closest_frame["ts_ms"]
            })
    
    logger.info(f"产物生成完成，共{len(keyframes)}个关键帧")
    
    return {"keyframes": keyframes}


def _find_closest_frame(
    frames_index: List[Dict[str, Any]],
    target_ms: float
) -> Dict[str, Any]:
    """找到最接近目标时间的帧"""
    if not frames_index:
        return None
    
    closest = min(
        frames_index,
        key=lambda f: abs(f["ts_ms"] - target_ms)
    )
    return closest

