# Video AI Demo Backend

视频分析与对比系统的本地Demo版本，支持Learn和Compare两种模式。

## 功能特性

- **Learn模式**：分析单个视频，提取镜头切分和影视特征（运镜、打光、调色）
- **Compare模式**：对比两个视频，生成step-by-step改进建议
- **虚拟运镜预览**：基于改进建议生成运镜预览视频（图生视频API）
- **异步执行**：Job异步执行，支持进度查询
- **多模态LLM**：使用Qwen2.5-VL进行视频理解和特征提取

## 技术架构

- **Web框架**：FastAPI
- **数据库**：SQLite
- **异步任务**：asyncio + Task
- **视频处理**：ffmpeg
- **多模态LLM**：Qwen2.5-VL-7B-Instruct (sophnet.com)

## 项目结构

```
video_ai_demo/
├── app/
│   ├── main.py                    # FastAPI主应用
│   ├── api/                       # API路由
│   │   ├── routes_jobs.py         # Job相关API
│   │   └── routes_virtual_motion.py  # 虚拟运镜API
│   ├── core/                      # 核心模块
│   │   ├── config.py              # 配置
│   │   ├── errors.py              # 错误定义
│   │   ├── logging.py             # 日志
│   │   └── json_schema.py         # JSON Schema校验
│   ├── db/                        # 数据库
│   │   ├── session.py             # SQLite会话
│   │   ├── models.py              # 数据模型
│   │   └── repo.py                # 仓储层
│   ├── pipeline/                  # Pipeline编排
│   │   ├── orchestrator.py        # 编排器
│   │   └── steps/                 # Pipeline步骤
│   │       ├── ingest.py          # 视频摄取
│   │       ├── extract_frames.py  # 抽帧
│   │       ├── mm_llm_decompose.py  # 多模态LLM拆解
│   │       ├── artifacts.py       # 产物生成
│   │       ├── compare_map.py     # 对比映射
│   │       └── improve_steps.py   # 改进建议
│   ├── integrations/              # 外部API适配层
│   │   ├── mm_llm_client.py       # 多模态LLM客户端
│   │   └── img2video_client.py    # 图生视频客户端
│   └── plugins/                   # 插件（预留）
├── data/                          # 数据目录
├── tests/                         # 测试
├── requirements.txt               # 依赖
├── .env.example                   # 配置示例
└── README.md                      # 本文件
```

## 安装和启动

### 1. 系统依赖

确保已安装：
- Python 3.9+
- ffmpeg 和 ffprobe

在macOS上安装ffmpeg：
```bash
brew install ffmpeg
```

在Ubuntu上安装ffmpeg：
```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. 安装Python依赖

```bash
cd video_ai_demo
pip install -r requirements.txt
```

### 3. 配置环境变量

复制配置示例：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API密钥：
```bash
# 多模态LLM配置
MM_LLM_BASE_URL=https://www.sophnet.com/api/open-apis/v1
MM_LLM_API_KEY=你的API密钥
MM_LLM_MODEL=Qwen2.5-VL-7B-Instruct

# 图生视频配置（可选，暂未实现）
IMG2VIDEO_BASE_URL=
IMG2VIDEO_API_KEY=
IMG2VIDEO_MODEL=

# 数据存储
DATA_DIR=./data
SQLITE_PATH=./data/demo.db

# FFmpeg
FFMPEG_BIN=ffmpeg
FFPROBE_BIN=ffprobe
```

### 4. 启动服务

```bash
uvicorn app.main:app --reload --port 8000
```

或者直接运行：
```bash
python -m app.main
```

服务将在 `http://localhost:8000` 启动。

访问API文档：`http://localhost:8000/docs`

## API使用示例

### 1. Learn模式：分析单个视频

```bash
curl -X POST "http://localhost:8000/v1/video-analysis/jobs" \
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
        "max_frames": 240
      },
      "analysis": {
        "enabled_modules": ["camera_motion", "lighting", "color_grading"]
      },
      "llm": {
        "provider": "sophnet",
        "model": "Qwen2.5-VL-7B-Instruct"
      }
    }
  }'
```

响应：
```json
{
  "job_id": "job_abc123",
  "status": "queued",
  "status_url": "/v1/video-analysis/jobs/job_abc123"
}
```

### 2. 查询Job状态

```bash
curl "http://localhost:8000/v1/video-analysis/jobs/job_abc123"
```

响应（运行中）：
```json
{
  "job_id": "job_abc123",
  "mode": "learn",
  "status": "running",
  "progress": {
    "stage": "decompose",
    "percent": 60.0,
    "message": "分析视频特征..."
  },
  "created_at": "2026-01-01T10:00:00",
  "updated_at": "2026-01-01T10:02:30"
}
```

响应（成功）：
```json
{
  "job_id": "job_abc123",
  "mode": "learn",
  "status": "succeeded",
  "result": {
    "mode": "learn",
    "target": {
      "asset_id": "job_abc123_target",
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
            }
          ]
        }
      ],
      "keyframes": [...]
    }
  },
  "completed_at": "2026-01-01T10:03:00"
}
```

### 3. Compare模式：对比两个视频

```bash
curl -X POST "http://localhost:8000/v1/video-analysis/jobs" \
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
        "fps": 2,
        "max_frames": 240
      },
      "compare": {
        "enabled": true,
        "virtual_camera_motion": {
          "enabled": true
        }
      }
    }
  }'
```

结果包含：
- `target`：目标视频的拆解结果
- `user`：用户视频的拆解结果
- `comparison.mappings`：片段映射关系
- `comparison.improvements`：step-by-step改进建议

### 4. 虚拟运镜预览

基于Compare模式的改进建议，生成运镜预览：

```bash
curl -X POST "http://localhost:8000/v1/video-analysis/virtual-motion/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_job_id": "job_abc123",
    "asset_role": "user",
    "segment_id": "u_seg_003",
    "motion_recipe": {
      "type": "push_in",
      "strength": 0.18,
      "duration_ms": 3000
    },
    "options": {
      "provider": "default"
    }
  }'
```

响应：
```json
{
  "subtask_id": "vm_xyz789",
  "status": "queued",
  "status_url": "/v1/video-analysis/virtual-motion/jobs/vm_xyz789"
}
```

查询虚拟运镜Job：
```bash
curl "http://localhost:8000/v1/video-analysis/virtual-motion/jobs/vm_xyz789"
```

## 输出结构说明

### Feature（特征）

每个特征只包含一个单一属性：

```json
{
  "category": "camera_motion",  // 类别：camera_motion/lighting/color_grading
  "type": "push_in",            // 类型
  "value": "缓慢推镜",           // 值（单一特征，不能包含连接词）
  "confidence": 0.85,           // 置信度 (0-1)
  "evidence": {
    "time_ranges_ms": [[0, 3500]]  // 证据时间范围
  }
}
```

### Improvement（改进建议）

```json
{
  "step": 1,
  "category": "camera_motion",
  "action_type": "adjust_camera_motion",
  "description": "将运镜调整为：缓慢推镜",
  "target_value": "缓慢推镜",
  "current_value": "固定机位",
  "priority": "high",
  "motion_recipe": {
    "type": "push_in",
    "strength": 0.18,
    "duration_ms": 3000
  },
  "validation": {
    "expected": "缓慢推镜",
    "confidence_threshold": 0.7
  }
}
```

## 数据存储

所有数据存储在 `./data/` 目录：

```
data/
├── demo.db              # SQLite数据库
└── jobs/
    └── job_abc123/      # Job工作目录
        ├── target/      # Target视频相关
        │   ├── input_video.mp4
        │   ├── frames/
        │   └── keyframes/
        ├── user/        # User视频相关
        │   ├── input_video.mp4
        │   ├── frames/
        │   └── keyframes/
        └── previews/    # 虚拟运镜预览视频
            └── vm_xyz789.mp4
```

## 扩展性设计

### 1. 多模态LLM适配层

`app/integrations/mm_llm_client.py` 提供统一接口，可替换不同的多模态模型：

- 当前支持：Qwen2.5-VL (sophnet.com)
- 可扩展：GPT-4V, Claude Vision等

### 2. 图生视频适配层

`app/integrations/img2video_client.py` 提供图生视频接口：

- 当前状态：Mock实现（返回占位文件）
- 可扩展：接入真实的图生视频API

### 3. Pipeline插件化

所有Pipeline步骤都是独立模块，可以：
- 替换拆解算法（传统CV + LLM解释）
- 扩展新的特征分析模块
- 自定义改进建议生成逻辑

## 质量保障

1. **JSON Schema校验**：所有LLM输出都经过Schema校验
2. **单特征约束**：检测feature.value中的连接词，确保单一特征
3. **错误处理**：完善的错误处理和日志记录
4. **数据持久化**：Job状态和结果持久化到SQLite

## 注意事项

1. **API费用**：多模态LLM调用会产生费用，注意控制抽帧率和数量
2. **处理时间**：视频处理是异步的，大视频可能需要几分钟
3. **存储空间**：抽帧和产物会占用磁盘空间，定期清理
4. **Demo限制**：
   - 图生视频功能为Mock实现
   - 映射和改进算法为简化版本
   - 建议生产环境使用消息队列（如Celery）

## 开发和测试

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio

# 运行测试
pytest tests/
```

### 查看日志

日志输出到控制台，包含详细的执行信息。

### 调试

1. 启动服务时添加 `--reload` 参数实现热重载
2. 访问 `/docs` 查看交互式API文档
3. 检查 `./data/demo.db` 查看数据库内容
4. 查看 `./data/jobs/` 目录下的中间文件

## 生产部署建议

1. 使用消息队列（Celery + Redis/RabbitMQ）替代内存任务
2. 使用PostgreSQL替代SQLite
3. 使用对象存储（S3/OSS）存储视频和产物
4. 添加认证和授权
5. 添加速率限制
6. 配置日志聚合（ELK/Loki）
7. 添加监控和告警

## 许可证

MIT License

## 联系方式

如有问题，请提交Issue。

