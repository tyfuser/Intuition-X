"""JSON Schema定义和校验"""
import jsonschema
from typing import Dict, Any, List
from .errors import ValidationError


# 特征输出Schema
FEATURE_SCHEMA = {
    "type": "object",
    "required": ["category", "type", "value", "confidence", "evidence"],
    "properties": {
        "category": {
            "type": "string",
            "enum": ["camera_motion", "lighting", "color_grading"]
        },
        "type": {"type": "string"},
        "value": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence": {
            "type": "object",
            "required": ["time_ranges_ms"],
            "properties": {
                "time_ranges_ms": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2,
                        "maxItems": 2
                    }
                }
            }
        },
        "detailed_description": {
            "type": "object",
            "description": "详细特征描述",
            "properties": {
                "summary": {"type": "string"},
                "technical_terms": {"type": "array", "items": {"type": "string"}},
                "purpose": {"type": "string"},
                "parameters": {"type": "object"},
                "diagram": {"type": "string"}
            }
        }
    }
}

# 段落Schema
SEGMENT_SCHEMA = {
    "type": "object",
    "required": ["segment_id", "start_ms", "end_ms", "duration_ms"],
    "properties": {
        "segment_id": {"type": "string"},
        "start_ms": {"type": "number"},
        "end_ms": {"type": "number"},
        "duration_ms": {"type": "number"},
        "features": {
            "type": "array",
            "items": FEATURE_SCHEMA
        }
    }
}

# 拆解结果Schema
DECOMPOSE_RESULT_SCHEMA = {
    "type": "object",
    "required": ["segments"],
    "properties": {
        "segments": {
            "type": "array",
            "items": SEGMENT_SCHEMA
        }
    }
}


def validate_decompose_result(data: Dict[str, Any]) -> None:
    """校验拆解结果"""
    try:
        jsonschema.validate(instance=data, schema=DECOMPOSE_RESULT_SCHEMA)
    except jsonschema.ValidationError as e:
        raise ValidationError(f"拆解结果校验失败: {e.message}", {"path": list(e.path)})
    
    # 额外检查：单特征约束
    _check_single_feature_constraint(data)


def _check_single_feature_constraint(data: Dict[str, Any]) -> None:
    """检查单特征约束：value不应包含连接词"""
    forbidden_words = ["、", "，", "；", " and ", "以及", "/"]
    warnings = []
    
    for segment in data.get("segments", []):
        for feature in segment.get("features", []):
            value = feature.get("value", "")
            for word in forbidden_words:
                if word in value:
                    warnings.append({
                        "segment_id": segment.get("segment_id"),
                        "feature_type": feature.get("type"),
                        "value": value,
                        "issue": f"包含连接词'{word}'，可能违反单特征约束"
                    })
    
    if warnings:
        # Demo阶段只记录警告，不抛异常
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"发现{len(warnings)}个潜在的单特征约束违规: {warnings}")

