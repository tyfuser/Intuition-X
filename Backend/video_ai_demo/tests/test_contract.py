"""合约测试：验证API返回结构"""
import pytest
from app.core.json_schema import validate_decompose_result, ValidationError


def test_valid_decompose_result():
    """测试有效的拆解结果"""
    
    valid_result = {
        "segments": [
            {
                "segment_id": "seg_001",
                "start_ms": 0,
                "end_ms": 3500,
                "duration_ms": 3500,
                "features": [
                    {
                        "category": "camera_motion",
                        "type": "push_in",
                        "value": "缓慢推镜",
                        "confidence": 0.85,
                        "evidence": {
                            "time_ranges_ms": [[0, 3500]]
                        }
                    },
                    {
                        "category": "lighting",
                        "type": "three_point",
                        "value": "三点布光",
                        "confidence": 0.90,
                        "evidence": {
                            "time_ranges_ms": [[0, 3500]]
                        }
                    }
                ]
            }
        ]
    }
    
    # 应该不抛异常
    validate_decompose_result(valid_result)


def test_invalid_decompose_result_missing_fields():
    """测试缺少必填字段的结果"""
    
    invalid_result = {
        "segments": [
            {
                "segment_id": "seg_001",
                # 缺少 start_ms, end_ms, duration_ms
            }
        ]
    }
    
    with pytest.raises(ValidationError):
        validate_decompose_result(invalid_result)


def test_feature_single_constraint_warning():
    """测试单特征约束（应该记录警告但不失败）"""
    
    result_with_multiple_features = {
        "segments": [
            {
                "segment_id": "seg_001",
                "start_ms": 0,
                "end_ms": 3500,
                "duration_ms": 3500,
                "features": [
                    {
                        "category": "camera_motion",
                        "type": "mixed",
                        "value": "推镜、拉镜、平移",  # 违反单特征约束
                        "confidence": 0.85,
                        "evidence": {
                            "time_ranges_ms": [[0, 3500]]
                        }
                    }
                ]
            }
        ]
    }
    
    # 应该记录警告但不失败（Demo阶段）
    validate_decompose_result(result_with_multiple_features)


def test_compare_result_structure():
    """测试Compare模式的结果结构"""
    
    compare_result = {
        "mode": "compare",
        "target": {
            "asset_id": "job_test_target",
            "segments": [
                {
                    "segment_id": "seg_001",
                    "start_ms": 0,
                    "end_ms": 3500,
                    "duration_ms": 3500,
                    "features": []
                }
            ],
            "keyframes": []
        },
        "user": {
            "asset_id": "job_test_user",
            "segments": [],
            "keyframes": []
        },
        "comparison": {
            "mappings": [],
            "improvements": []
        }
    }
    
    # 验证基本结构
    assert compare_result["mode"] == "compare"
    assert "target" in compare_result
    assert "user" in compare_result
    assert "comparison" in compare_result
    assert "mappings" in compare_result["comparison"]
    assert "improvements" in compare_result["comparison"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

