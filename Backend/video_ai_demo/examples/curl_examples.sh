#!/bin/bash

# API调用示例

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "Video AI Demo - API调用示例"
echo "=========================================="
echo ""

# 1. 健康检查
echo "1. 健康检查"
echo "-------------------------------------------"
curl -s "$BASE_URL/health" | python -m json.tool
echo ""
echo ""

# 2. Learn模式 - 分析单个视频
echo "2. Learn模式 - 创建Job"
echo "-------------------------------------------"
LEARN_JOB=$(curl -s -X POST "$BASE_URL/v1/video-analysis/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "learn",
    "target_video": {
      "source": {
        "type": "url",
        "url": "https://example.com/video.mp4"
      }
    },
    "options": {
      "frame_extract": {
        "fps": 2,
        "max_frames": 100
      },
      "analysis": {
        "enabled_modules": ["camera_motion", "lighting", "color_grading"]
      }
    }
  }')

echo "$LEARN_JOB" | python -m json.tool
JOB_ID=$(echo "$LEARN_JOB" | python -c "import sys, json; print(json.load(sys.stdin)['job_id'])")
echo ""
echo "Job ID: $JOB_ID"
echo ""
echo ""

# 3. 查询Job状态
echo "3. 查询Job状态"
echo "-------------------------------------------"
curl -s "$BASE_URL/v1/video-analysis/jobs/$JOB_ID" | python -m json.tool
echo ""
echo ""

# 4. Compare模式 - 对比两个视频
echo "4. Compare模式 - 创建Job"
echo "-------------------------------------------"
COMPARE_JOB=$(curl -s -X POST "$BASE_URL/v1/video-analysis/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "compare",
    "target_video": {
      "source": {
        "type": "url",
        "url": "https://example.com/target.mp4"
      }
    },
    "user_video": {
      "source": {
        "type": "url",
        "url": "https://example.com/user.mp4"
      }
    },
    "options": {
      "frame_extract": {
        "fps": 1,
        "max_frames": 60
      }
    }
  }')

echo "$COMPARE_JOB" | python -m json.tool
COMPARE_JOB_ID=$(echo "$COMPARE_JOB" | python -c "import sys, json; print(json.load(sys.stdin)['job_id'])")
echo ""
echo "Compare Job ID: $COMPARE_JOB_ID"
echo ""
echo ""

# 5. 虚拟运镜预览
echo "5. 虚拟运镜预览 - 创建子任务（需要先有成功的Compare Job）"
echo "-------------------------------------------"
echo "示例（需要替换实际的job_id和segment_id）："
echo ""
cat << 'EOF'
curl -X POST "$BASE_URL/v1/video-analysis/virtual-motion/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_job_id": "job_abc123",
    "asset_role": "user",
    "segment_id": "seg_001",
    "motion_recipe": {
      "type": "push_in",
      "strength": 0.18,
      "duration_ms": 3000
    }
  }'
EOF

echo ""
echo ""

# 7. CV场景检测（推荐）
echo "7. CV场景检测 + LLM特征分析"
echo "-------------------------------------------"
echo "使用CV算法精准检测镜头切换，LLM分析特征"
curl -X POST "$BASE_URL/v1/video-analysis/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "learn",
    "target_video": {
      "source": {
        "type": "file",
        "path": "/path/to/video.mp4"
      }
    },
    "options": {
      "scene_detection": {
        "use_cv": true,
        "threshold": 27.0,
        "min_scene_len": 15
      },
      "frame_extract": {
        "fps": 1,
        "max_frames": 30
      },
      "llm": {
        "enabled_modules": ["camera_motion", "lighting", "color_grading"]
      }
    }
  }' | python -m json.tool
echo ""
echo ""

# 8. 纯LLM检测（对比）
echo "8. 纯LLM场景检测（不推荐）"
echo "-------------------------------------------"
curl -X POST "$BASE_URL/v1/video-analysis/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "learn",
    "target_video": {
      "source": {
        "type": "file",
        "path": "/path/to/video.mp4"
      }
    },
    "options": {
      "scene_detection": {
        "use_cv": false
      },
      "frame_extract": {
        "fps": 2,
        "max_frames": 100
      }
    }
  }' | python -m json.tool
echo ""
echo ""

# 9. 高灵敏度检测（适合快节奏视频）
echo "9. 高灵敏度CV检测 - 适合MV、广告"
echo "-------------------------------------------"
curl -X POST "$BASE_URL/v1/video-analysis/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "learn",
    "target_video": {
      "source": {
        "type": "file",
        "path": "/path/to/music_video.mp4"
      }
    },
    "options": {
      "scene_detection": {
        "use_cv": true,
        "threshold": 20.0,
        "min_scene_len": 10
      }
    }
  }' | python -m json.tool
echo ""
echo ""

# 10. 低灵敏度检测（适合慢节奏视频）
echo "10. 低灵敏度CV检测 - 适合纪录片、访谈"
echo "-------------------------------------------"
curl -X POST "$BASE_URL/v1/video-analysis/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "learn",
    "target_video": {
      "source": {
        "type": "file",
        "path": "/path/to/documentary.mp4"
      }
    },
    "options": {
      "scene_detection": {
        "use_cv": true,
        "threshold": 35.0,
        "min_scene_len": 30
      }
    }
  }' | python -m json.tool
echo ""
echo ""

echo "=========================================="
echo "完成！"
echo "=========================================="
echo ""
echo "💡 提示："
echo "  - CV检测默认启用，更准确、更快速"
echo "  - threshold: 15-40，越低越敏感"
echo "  - 详见: CV_SCENE_DETECTION.md"
echo ""

