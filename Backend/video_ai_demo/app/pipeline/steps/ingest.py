"""视频摄取步骤"""
import httpx
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional

from ...core.errors import VideoProcessingError
from ...core.config import settings
from ...core.logging import logger


async def ingest_video(
    source_type: str,
    source_url: Optional[str],
    source_path: Optional[str],
    output_dir: Path
) -> Dict[str, Any]:
    """
    摄取视频：下载或复制到本地
    
    Returns:
        {
            "local_path": str,
            "duration_ms": float,
            "width": int,
            "height": int,
            "fps": float,
            "codec": str
        }
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    local_path = output_dir / "input_video.mp4"
    
    # 下载或复制视频
    if source_type == "url":
        await _download_video(source_url, local_path)
    elif source_type == "file":
        _copy_video(source_path, local_path)
    else:
        raise VideoProcessingError(f"不支持的source_type: {source_type}")
    
    # 获取视频元数据
    metadata = _probe_video(local_path)
    
    return {
        "local_path": str(local_path),
        **metadata
    }


async def _download_video(url: str, output_path: Path):
    """下载视频"""
    logger.info(f"下载视频: {url}")
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                
                with open(output_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
        
        logger.info(f"视频下载完成: {output_path}")
    
    except Exception as e:
        raise VideoProcessingError(f"视频下载失败: {str(e)}")


def _copy_video(source_path: str, output_path: Path):
    """复制本地视频"""
    import shutil
    
    logger.info(f"复制视频: {source_path} -> {output_path}")
    
    source = Path(source_path)
    if not source.exists():
        raise VideoProcessingError(f"源视频不存在: {source_path}")
    
    shutil.copy2(source, output_path)


def _probe_video(video_path: Path) -> Dict[str, Any]:
    """探测视频元数据（使用ffprobe）"""
    logger.info(f"探测视频元数据: {video_path}")
    
    cmd = [
        settings.ffprobe_bin,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(video_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        probe_data = json.loads(result.stdout)
        
        # 提取视频流信息
        video_stream = None
        for stream in probe_data.get("streams", []):
            if stream.get("codec_type") == "video":
                video_stream = stream
                break
        
        if not video_stream:
            raise VideoProcessingError("未找到视频流")
        
        # 提取元数据
        duration_s = float(probe_data.get("format", {}).get("duration", 0))
        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))
        
        # 计算FPS
        fps_str = video_stream.get("r_frame_rate", "0/1")
        if "/" in fps_str:
            num, den = fps_str.split("/")
            fps = float(num) / float(den) if float(den) > 0 else 0
        else:
            fps = float(fps_str)
        
        codec = video_stream.get("codec_name", "unknown")
        
        return {
            "duration_ms": duration_s * 1000,
            "width": width,
            "height": height,
            "fps": fps,
            "codec": codec
        }
    
    except subprocess.CalledProcessError as e:
        raise VideoProcessingError(f"ffprobe执行失败: {e.stderr}")
    except Exception as e:
        raise VideoProcessingError(f"视频元数据提取失败: {str(e)}")

