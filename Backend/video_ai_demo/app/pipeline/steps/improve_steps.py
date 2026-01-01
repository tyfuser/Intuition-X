"""改进建议生成步骤"""
from typing import Dict, Any, List, Optional

from ...core.logging import logger


def generate_improvements(
    user_segments: List[Dict[str, Any]],
    target_segments: List[Dict[str, Any]],
    mappings: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    为每个user segment生成step-by-step改进建议
    
    Returns:
        改进建议列表：
        [
            {
                "user_segment_id": str,
                "target_segment_id": str,
                "improvements": [
                    {
                        "step": int,
                        "category": str,
                        "action_type": str,
                        "description": str,
                        "target_value": str,
                        "current_value": str,
                        "priority": str
                    }
                ]
            }
        ]
    """
    logger.info(f"生成改进建议，共{len(mappings)}个映射")
    
    improvements_list = []
    
    # 构建快速查找字典
    user_seg_dict = {s["segment_id"]: s for s in user_segments}
    target_seg_dict = {s["segment_id"]: s for s in target_segments}
    
    for mapping in mappings:
        user_seg_id = mapping["user_segment_id"]
        target_seg_id = mapping["target_segment_id"]
        
        user_seg = user_seg_dict.get(user_seg_id)
        target_seg = target_seg_dict.get(target_seg_id)
        
        if not user_seg or not target_seg:
            continue
        
        improvements = _generate_segment_improvements(
            user_seg,
            target_seg
        )
        
        improvements_list.append({
            "user_segment_id": user_seg_id,
            "target_segment_id": target_seg_id,
            "improvements": improvements
        })
    
    logger.info(f"改进建议生成完成")
    
    return improvements_list


def _generate_segment_improvements(
    user_seg: Dict[str, Any],
    target_seg: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """为单个segment生成改进建议"""
    
    improvements = []
    step = 1
    
    # 按优先级：运镜 -> 打光 -> 调色
    priority_order = ["camera_motion", "lighting", "color_grading"]
    
    user_features = _group_features_by_category(user_seg.get("features", []))
    target_features = _group_features_by_category(target_seg.get("features", []))
    
    for category in priority_order:
        target_feature = target_features.get(category)
        user_feature = user_features.get(category)
        
        if not target_feature:
            continue
        
        # 生成改进建议
        improvement = _create_improvement_action(
            step=step,
            category=category,
            target_feature=target_feature,
            user_feature=user_feature
        )
        
        if improvement:
            improvements.append(improvement)
            step += 1
    
    return improvements


def _group_features_by_category(
    features: List[Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """按category分组features（取第一个）"""
    grouped = {}
    for feature in features:
        category = feature.get("category")
        if category and category not in grouped:
            grouped[category] = feature
    return grouped


def _create_improvement_action(
    step: int,
    category: str,
    target_feature: Dict[str, Any],
    user_feature: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """创建改进动作"""
    
    category_names = {
        "camera_motion": "运镜",
        "lighting": "打光",
        "color_grading": "调色"
    }
    
    target_value = target_feature.get("value", "")
    current_value = user_feature.get("value", "无") if user_feature else "无"
    
    # 如果当前值和目标值相同，不需要改进
    if current_value == target_value:
        return None
    
    # 生成描述
    description = f"将{category_names.get(category, category)}调整为：{target_value}"
    
    # 根据category生成具体action_type
    action_type_map = {
        "camera_motion": "adjust_camera_motion",
        "lighting": "adjust_lighting",
        "color_grading": "adjust_color_grading"
    }
    
    # 运镜改进可以生成虚拟预览
    motion_recipe = None
    if category == "camera_motion":
        motion_recipe = _infer_motion_recipe(target_feature)
    
    improvement = {
        "step": step,
        "category": category,
        "action_type": action_type_map.get(category, "adjust"),
        "description": description,
        "target_value": target_value,
        "current_value": current_value,
        "priority": "high" if step == 1 else "medium",
        "validation": {
            "expected": target_value,
            "confidence_threshold": 0.7
        }
    }
    
    if motion_recipe:
        improvement["motion_recipe"] = motion_recipe
    
    return improvement


def _infer_motion_recipe(target_feature: Dict[str, Any]) -> Dict[str, Any]:
    """从target feature推断运镜配方"""
    
    feature_type = target_feature.get("type", "")
    value = target_feature.get("value", "")
    
    # 简单映射（Demo版本）
    recipe_map = {
        "push_in": {"type": "push_in", "strength": 0.18, "duration_ms": 3000},
        "pull_out": {"type": "pull_out", "strength": 0.18, "duration_ms": 3000},
        "pan_left": {"type": "pan", "direction": "left", "strength": 0.15, "duration_ms": 3000},
        "pan_right": {"type": "pan", "direction": "right", "strength": 0.15, "duration_ms": 3000},
        "tilt_up": {"type": "tilt", "direction": "up", "strength": 0.15, "duration_ms": 3000},
        "tilt_down": {"type": "tilt", "direction": "down", "strength": 0.15, "duration_ms": 3000}
    }
    
    # 尝试从type或value中匹配
    for key, recipe in recipe_map.items():
        if key in feature_type.lower() or key.replace("_", "") in value.lower():
            return recipe
    
    # 默认
    return {"type": "push_in", "strength": 0.18, "duration_ms": 3000}

