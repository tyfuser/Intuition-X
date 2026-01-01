"""抽帧步骤"""
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List

from ...core.errors import VideoProcessingError
from ...core.config import settings
from ...core.logging import logger


def extract_frames(
    video_path: str,
    output_dir: Path,
    fps: float = 2.0,
    max_frames: int = 240
) -> Dict[str, Any]:
    """
    从视频中抽取关键帧
    
    Args:
        video_path: 视频路径
        output_dir: 输出目录
        fps: 抽帧率
        max_frames: 最大帧数
    
    Returns:
        {
            "frames_dir": str,
            "frames_index": List[{"frame_id": str, "ts_ms": float, "path": str}],
            "total_frames": int
        }
    """
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"开始抽帧: fps={fps}, max_frames={max_frames}")
    
    # 使用ffmpeg抽帧
    output_pattern = str(frames_dir / "frame_%05d.jpg")
    
    cmd = [
        settings.ffmpeg_bin,
        "-i", video_path,
        "-vf", f"fps={fps}",
        "-frames:v", str(max_frames),
        "-q:v", "2",  # 高质量JPEG
        output_pattern
    ]
    
    try:
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise VideoProcessingError(f"ffmpeg抽帧失败: {e.stderr}")
    
    # 生成帧索引
    frames_index = _build_frames_index(frames_dir, fps)
    
    # 保存索引文件
    index_file = output_dir / "frames_index.json"
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(frames_index, f, ensure_ascii=False, indent=2)
    
    logger.info(f"抽帧完成，共{len(frames_index)}帧")
    
    return {
        "frames_dir": str(frames_dir),
        "frames_index": frames_index,
        "total_frames": len(frames_index)
    }


def _build_frames_index(frames_dir: Path, fps: float) -> List[Dict[str, Any]]:
    """构建帧索引"""
    frames = sorted(frames_dir.glob("frame_*.jpg"))
    
    index = []
    frame_interval_ms = 1000.0 / fps
    
    for i, frame_path in enumerate(frames):
        index.append({
            "frame_id": f"f_{i:05d}",
            "ts_ms": i * frame_interval_ms,
            "path": str(frame_path)
        })
    
    return index
