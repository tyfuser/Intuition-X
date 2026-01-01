"""CV场景检测步骤 - 使用传统CV算法进行镜头切分"""
from pathlib import Path
from typing import Dict, Any, List
from scenedetect import open_video, SceneManager, split_video_ffmpeg
from scenedetect.detectors import ContentDetector, ThresholdDetector
from scenedetect.scene_manager import save_images

from ...core.errors import VideoProcessingError
from ...core.logging import logger


def detect_scenes(
    video_path: str,
    output_dir: Path,
    threshold: float = 27.0,
    min_scene_len: int = 15
) -> List[Dict[str, Any]]:
    """
    使用CV算法检测视频场景切换
    
    Args:
        video_path: 视频路径
        output_dir: 输出目录
        threshold: 检测阈值（越低越敏感，默认27）
        min_scene_len: 最小场景长度（帧数，默认15帧约0.5秒）
    
    Returns:
        场景列表：
        [
            {
                "segment_id": "seg_001",
                "start_ms": 0,
                "end_ms": 3500,
                "start_frame": 0,
                "end_frame": 105
            }
        ]
    """
    logger.info(f"开始CV场景检测: threshold={threshold}, min_scene_len={min_scene_len}")
    
    try:
        # 打开视频
        video = open_video(video_path)
        
        # 创建场景管理器
        scene_manager = SceneManager()
        
        # 添加内容检测器（基于帧间差异）
        scene_manager.add_detector(
            ContentDetector(
                threshold=threshold,
                min_scene_len=min_scene_len
            )
        )
        
        # 检测场景
        scene_manager.detect_scenes(video)
        
        # 获取场景列表
        scene_list = scene_manager.get_scene_list()
        
        if not scene_list:
            logger.warning("未检测到场景切换，使用整个视频作为单一场景")
            # 获取视频总帧数和FPS
            fps = video.frame_rate
            total_frames = video.duration.get_frames()
            
            scene_list = [
                (video.base_timecode, video.base_timecode + total_frames)
            ]
        
        # 转换为我们的格式
        segments = []
        fps = video.frame_rate
        
        for i, (start_time, end_time) in enumerate(scene_list):
            start_frame = start_time.get_frames()
            end_frame = end_time.get_frames()
            
            start_ms = (start_frame / fps) * 1000
            end_ms = (end_frame / fps) * 1000
            
            segments.append({
                "segment_id": f"seg_{i+1:03d}",
                "start_ms": start_ms,
                "end_ms": end_ms,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "duration_ms": end_ms - start_ms
            })
        
        logger.info(f"CV场景检测完成，共检测到{len(segments)}个场景")
        
        # 可选：保存关键帧
        if len(segments) > 0 and len(segments) < 50:  # 不要在场景太多时保存
            try:
                keyframes_dir = output_dir / "scene_keyframes"
                keyframes_dir.mkdir(parents=True, exist_ok=True)
                
                save_images(
                    scene_list=scene_list,
                    video=video,
                    num_images=1,  # 每个场景保存1帧
                    output_dir=str(keyframes_dir),
                    image_name_template='$SCENE_NUMBER-keyframe'
                )
                logger.info(f"场景关键帧已保存到: {keyframes_dir}")
            except Exception as e:
                logger.warning(f"保存场景关键帧失败: {str(e)}")
        
        return segments
        
    except Exception as e:
        raise VideoProcessingError(f"CV场景检测失败: {str(e)}")


def detect_scenes_with_optical_flow(
    video_path: str,
    output_dir: Path,
    flow_threshold: float = 30.0
) -> List[Dict[str, Any]]:
    """
    使用光流法检测场景切换（更精确但更慢）
    
    Args:
        video_path: 视频路径
        output_dir: 输出目录
        flow_threshold: 光流阈值
    
    Returns:
        场景列表
    """
    import cv2
    import numpy as np
    
    logger.info(f"开始光流法场景检测: threshold={flow_threshold}")
    
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # 读取第一帧
        ret, prev_frame = cap.read()
        if not ret:
            raise VideoProcessingError("无法读取视频第一帧")
        
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        
        # 检测场景切换点
        scene_changes = [0]  # 起始帧
        frame_idx = 1
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 计算光流
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray, None,
                pyr_scale=0.5,
                levels=3,
                winsize=15,
                iterations=3,
                poly_n=5,
                poly_sigma=1.2,
                flags=0
            )
            
            # 计算光流幅度
            mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            mean_mag = np.mean(mag)
            
            # 如果光流突变，认为是场景切换
            if mean_mag > flow_threshold:
                scene_changes.append(frame_idx)
                logger.debug(f"检测到场景切换: 帧{frame_idx}, 光流={mean_mag:.2f}")
            
            prev_gray = gray
            frame_idx += 1
            
            # 进度提示
            if frame_idx % 100 == 0:
                logger.debug(f"光流检测进度: {frame_idx}/{total_frames}")
        
        scene_changes.append(total_frames - 1)  # 结束帧
        cap.release()
        
        # 转换为段落格式
        segments = []
        for i in range(len(scene_changes) - 1):
            start_frame = scene_changes[i]
            end_frame = scene_changes[i + 1]
            
            start_ms = (start_frame / fps) * 1000
            end_ms = (end_frame / fps) * 1000
            
            segments.append({
                "segment_id": f"seg_{i+1:03d}",
                "start_ms": start_ms,
                "end_ms": end_ms,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "duration_ms": end_ms - start_ms
            })
        
        logger.info(f"光流法检测完成，共检测到{len(segments)}个场景")
        return segments
        
    except Exception as e:
        raise VideoProcessingError(f"光流法场景检测失败: {str(e)}")


def detect_scenes_simple(
    video_path: str,
    output_dir: Path,
    threshold: float = 30.0,
    sample_rate: int = 5
) -> List[Dict[str, Any]]:
    """
    简单快速的场景检测（基于直方图差异）
    
    Args:
        video_path: 视频路径
        output_dir: 输出目录
        threshold: 相似度阈值（0-100，越大越严格）
        sample_rate: 采样率（每N帧检测一次）
    
    Returns:
        场景列表
    """
    import cv2
    import numpy as np
    
    logger.info(f"开始快速场景检测: threshold={threshold}, sample_rate={sample_rate}")
    
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # 读取第一帧
        ret, prev_frame = cap.read()
        if not ret:
            raise VideoProcessingError("无法读取视频第一帧")
        
        prev_hist = _calculate_histogram(prev_frame)
        
        scene_changes = [0]
        frame_idx = 1
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 采样检测
            if frame_idx % sample_rate == 0:
                curr_hist = _calculate_histogram(frame)
                
                # 计算直方图相似度
                similarity = cv2.compareHist(
                    prev_hist, curr_hist, cv2.HISTCMP_CORREL
                )
                
                # 相似度低于阈值，认为是场景切换
                if similarity < (1 - threshold / 100):
                    scene_changes.append(frame_idx)
                    logger.debug(f"检测到场景切换: 帧{frame_idx}, 相似度={similarity:.3f}")
                    prev_hist = curr_hist
            
            frame_idx += 1
        
        scene_changes.append(total_frames - 1)
        cap.release()
        
        # 转换格式
        segments = []
        for i in range(len(scene_changes) - 1):
            start_frame = scene_changes[i]
            end_frame = scene_changes[i + 1]
            
            start_ms = (start_frame / fps) * 1000
            end_ms = (end_frame / fps) * 1000
            
            # 过滤太短的片段（小于0.5秒）
            if end_ms - start_ms < 500:
                continue
            
            segments.append({
                "segment_id": f"seg_{i+1:03d}",
                "start_ms": start_ms,
                "end_ms": end_ms,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "duration_ms": end_ms - start_ms
            })
        
        logger.info(f"快速场景检测完成，共检测到{len(segments)}个场景")
        return segments
        
    except Exception as e:
        raise VideoProcessingError(f"快速场景检测失败: {str(e)}")


def _calculate_histogram(frame):
    """计算帧的颜色直方图"""
    import cv2
    
    # 转换为HSV色彩空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 计算直方图
    hist = cv2.calcHist(
        [hsv], [0, 1], None, [50, 60], [0, 180, 0, 256]
    )
    
    # 归一化
    cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    return hist

