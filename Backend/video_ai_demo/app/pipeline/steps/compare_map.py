"""比对映射步骤"""
from typing import Dict, Any, List, Optional

from ...core.logging import logger


def map_segments(
    target_segments: List[Dict[str, Any]],
    user_segments: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    映射user segments到target segments
    
    策略：基于时长和节奏相似度进行简单映射（Demo版本）
    
    Returns:
        映射列表：
        [
            {
                "user_segment_id": str,
                "target_segment_id": str,
                "confidence": float,
                "reason": str
            }
        ]
    """
    logger.info(f"映射segments: target={len(target_segments)}, user={len(user_segments)}")
    
    mappings = []
    
    # 简单策略：按时长比例映射
    target_total_duration = sum(s["duration_ms"] for s in target_segments)
    user_total_duration = sum(s["duration_ms"] for s in user_segments)
    
    for user_seg in user_segments:
        # 计算user segment在整体中的相对位置
        user_relative_pos = (user_seg["start_ms"] / user_total_duration 
                            if user_total_duration > 0 else 0)
        
        # 找到target中最接近位置的segment
        best_target = None
        best_score = -1
        
        for target_seg in target_segments:
            target_relative_pos = (target_seg["start_ms"] / target_total_duration
                                  if target_total_duration > 0 else 0)
            
            # 位置相似度
            pos_similarity = 1 - abs(user_relative_pos - target_relative_pos)
            
            # 时长相似度
            duration_ratio = min(
                user_seg["duration_ms"] / target_seg["duration_ms"],
                target_seg["duration_ms"] / user_seg["duration_ms"]
            ) if target_seg["duration_ms"] > 0 else 0
            
            # 综合得分
            score = pos_similarity * 0.6 + duration_ratio * 0.4
            
            if score > best_score:
                best_score = score
                best_target = target_seg
        
        if best_target:
            mappings.append({
                "user_segment_id": user_seg["segment_id"],
                "target_segment_id": best_target["segment_id"],
                "confidence": best_score,
                "reason": f"位置和时长相似度: {best_score:.2f}"
            })
    
    logger.info(f"映射完成，共{len(mappings)}个映射关系")
    
    return mappings

