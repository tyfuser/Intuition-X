# 视频分析系统 - 后端项目文档

## 📋 目录

1. [项目概述](#项目概述)
2. [技术架构](#技术架构)
3. [项目结构](#项目结构)
4. [核心功能](#核心功能)
5. [API文档](#api文档)
6. [数据库设计](#数据库设计)
7. [开发指南](#开发指南)
8. [部署指南](#部署指南)
9. [配置说明](#配置说明)
10. [常见问题](#常见问题)

---

## 项目概述

### 简介

视频分析系统是一个基于AI大模型的短视频内容分析平台，能够自动分析视频的运镜、光影、调色等专业特征，并生成详细的爆款因素分析报告。

### 核心价值

- **智能分析**：利用多模态大模型（LLM）自动识别视频中的专业特征
- **格式化输出**：将分析结果转换为可视化的前端数据格式
- **知识沉淀**：构建短视频创作知识库，提供可复用的创作技巧
- **实时响应**：支持同步分析，快速返回结果

### 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 主要开发语言 |
| FastAPI | 0.104+ | Web框架 |
| SQLAlchemy | 2.0+ | ORM |
| SQLite | 3.x | 数据库 |
| PyJWT | 2.8+ | JWT认证 |
| httpx | 0.25+ | HTTP客户端 |
| opencv-python | 4.8+ | 视频处理 |
| ffmpeg | 4.4+ | 视频帧提取 |

---

## 技术架构

### 整体架构

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (React)                   │
│          Vite + TypeScript + TailwindCSS            │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/REST API
┌──────────────────▼──────────────────────────────────┐
│              FastAPI Application Layer               │
│  ┌────────────┬────────────┬────────────┐          │
│  │  Auth API  │ Analysis  │ Knowledge │          │
│  │            │    API     │    API     │          │
│  └────────────┴────────────┴────────────┘          │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│              Business Logic Layer                    │
│  ┌────────────────────────────────────────────┐    │
│  │  Pipeline Orchestrator                      │    │
│  │  ┌───────┬─────────┬──────────┬──────────┐│    │
│  │  │Ingest │ Extract │  Scene   │   LLM    ││    │
│  │  │       │ Frames  │  Detect  │ Analysis ││    │
│  │  └───────┴─────────┴──────────┴──────────┘│    │
│  └────────────────────────────────────────────┘    │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│                  Data Layer                          │
│  ┌─────────────┬──────────────┬─────────────┐      │
│  │  SQLite DB  │ File Storage │ LLM Client  │      │
│  │  (jobs,     │  (videos,    │  (OpenAI    │      │
│  │   assets)   │   frames)    │   API)      │      │
│  └─────────────┴──────────────┴─────────────┘      │
└─────────────────────────────────────────────────────┘
```

### 分层设计

#### 1. API Layer (`app/api/`)
- 处理HTTP请求和响应
- 参数验证和转换
- 统一响应格式
- 认证鉴权

#### 2. Core Layer (`app/core/`)
- 配置管理
- 日志系统
- 错误处理
- JWT认证
- 响应格式化

#### 3. Business Logic Layer (`app/pipeline/`)
- 视频处理Pipeline
- 场景检测
- LLM分析
- 结果格式化

#### 4. Data Layer (`app/db/`, `app/integrations/`)
- 数据库操作
- 外部服务集成
- 文件存储

---

## 项目结构

```
video_ai_demo/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI应用入口
│   │
│   ├── api/                        # API路由层
│   │   ├── __init__.py
│   │   ├── routes_auth.py         # 认证API
│   │   ├── routes_dashboard.py    # 仪表盘API
│   │   ├── routes_analysis.py     # 视频分析API ⭐️
│   │   ├── routes_knowledge.py    # 知识库API
│   │   ├── routes_user.py         # 用户管理API
│   │   ├── routes_jobs.py         # Job管理API（异步）
│   │   └── routes_terminology.py  # 术语API
│   │
│   ├── core/                       # 核心模块
│   │   ├── __init__.py
│   │   ├── config.py              # 配置管理
│   │   ├── auth.py                # JWT认证
│   │   ├── response.py            # 统一响应格式
│   │   ├── errors.py              # 错误定义
│   │   ├── logging.py             # 日志系统
│   │   └── json_schema.py         # JSON Schema验证
│   │
│   ├── db/                         # 数据库层
│   │   ├── __init__.py
│   │   ├── models.py              # SQLAlchemy模型
│   │   ├── repo.py                # 数据仓储
│   │   └── session.py             # 数据库会话
│   │
│   ├── pipeline/                   # 视频处理Pipeline
│   │   ├── __init__.py
│   │   ├── orchestrator.py        # Pipeline编排器
│   │   └── steps/                 # Pipeline步骤
│   │       ├── ingest.py          # 视频获取
│   │       ├── extract_frames.py  # 帧提取
│   │       ├── scene_detect.py    # 场景检测
│   │       ├── mm_llm_decompose.py # LLM分析
│   │       ├── format_analysis.py  # 格式化分析 ⭐️
│   │       └── artifacts.py       # 产物生成
│   │
│   └── integrations/               # 外部服务集成
│       ├── __init__.py
│       ├── mm_llm_client.py       # 多模态LLM客户端
│       └── img2video_client.py    # 图生视频客户端
│
├── data/                           # 数据存储目录
│   ├── demo.db                    # SQLite数据库
│   ├── jobs/                      # Job数据目录
│   │   └── job_xxx/               # 单个Job目录
│   │       ├── target/            # 目标视频
│   │       ├── frames/            # 提取的帧
│   │       └── frames_index.json  # 帧索引
│   └── uploads/                   # 上传文件目录
│
├── requirements.txt               # Python依赖
├── start.sh                       # 启动脚本
├── PROJECT_DOCUMENTATION.md       # 本文档 ⭐️
└── README.md                      # 项目说明
```

---

## 核心功能

### 1. 视频分析 (Analysis API) ⭐️

#### 工作流程

```
用户上传视频
    ↓
POST /api/v1/analysis/upload
    ↓
返回文件路径
    ↓
POST /api/v1/analysis/create
    ↓
┌─────────────────────────────┐
│  1. 提取视频帧（5帧）       │
│  2. 调用LLM分析画面          │
│  3. 生成格式化报告           │
│  4. 缓存结果                │
└─────────────────────────────┘
    ↓
返回完整的VideoAnalysis对象
    ↓
前端轮询 GET /api/v1/analysis/{id}/status
    ↓
识别同步分析ID，立即返回completed
    ↓
GET /api/v1/analysis/{id}
    ↓
从缓存读取结果
```

#### 核心特性

- **同步分析**：不创建Job，直接返回结果
- **内存缓存**：结果缓存24小时，最多100个
- **快速提取**：每2秒提取1帧，最多5帧
- **智能降级**：LLM失败时返回基础分析

### 2. Dashboard API

从真实的Job数据生成统计信息：

- **统计数据**：总任务数、完成数、总时长、平均分数
- **项目列表**：最近的分析任务列表
- **日程安排**：基于Job创建时间的日程

### 3. Knowledge Base API

提供短视频创作知识库：

- **分类管理**：钩子、叙事、风格、BGM、指纹
- **搜索功能**：支持关键词和标签搜索
- **收藏功能**：用户可以收藏知识条目

### 4. Authentication API

JWT Token认证：

- **登录**：返回access_token和refresh_token
- **注册**：创建新用户（演示版本）
- **可选认证**：大多数API支持无token访问

---

## API文档

### 统一响应格式

#### 成功响应
```json
{
  "code": 0,
  "message": "操作成功",
  "data": { ... }
}
```

#### 错误响应
```json
{
  "code": 1001,
  "message": "错误描述",
  "data": null
}
```

### 错误码

| Code | 含义 |
|------|------|
| 0 | 成功 |
| 1001 | 无效请求 |
| 1002 | 认证失败 |
| 1003 | 权限不足 |
| 1004 | 资源不存在 |
| 1005 | 分析失败 |
| 5000 | 内部错误 |

### 核心API端点

#### 1. 视频分析

##### 上传视频
```http
POST /api/v1/analysis/upload
Content-Type: multipart/form-data

file: [视频文件]
```

响应：
```json
{
  "code": 0,
  "data": {
    "filePath": "/path/to/video.mp4",
    "fileName": "video.mp4",
    "fileSize": 1024000
  }
}
```

##### 创建分析
```http
POST /api/v1/analysis/create
Content-Type: application/json

{
  "url": "/path/to/video.mp4"
}
```

响应：
```json
{
  "code": 0,
  "data": {
    "id": "analysis_20260102123456",
    "analysisId": "analysis_20260102123456",
    "title": "视频分析",
    "duration": 15,
    "hookScore": 85,
    "viralFactors": [
      {
        "category": "视觉呈现",
        "description": "画面构图专业",
        "intensity": 8
      }
    ],
    "rhythmData": [...],
    "radarData": [...],
    "evaluationReport": {...},
    ...
  }
}
```

##### 查询分析状态
```http
GET /api/v1/analysis/{analysis_id}/status
```

响应：
```json
{
  "code": 0,
  "data": {
    "analysisId": "analysis_xxx",
    "status": "completed",
    "progress": 100,
    "message": "分析已完成"
  }
}
```

##### 获取分析结果
```http
GET /api/v1/analysis/{analysis_id}
```

响应：同创建分析的响应

#### 2. Dashboard

##### 获取统计数据
```http
GET /api/v1/stats
```

响应：
```json
{
  "code": 0,
  "data": {
    "totalAnalyses": 42,
    "completedToday": 5,
    "totalDuration": 3600,
    "avgScore": 82.5
  }
}
```

##### 获取项目列表
```http
GET /api/v1/projects?page=1&limit=10
```

#### 3. Knowledge Base

##### 获取知识库列表
```http
GET /api/v1/knowledge/items?category=hooks&page=1&limit=15
```

响应：
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "id": "kb_001",
        "category": "hooks",
        "title": "视觉反差钩子",
        "description": "前0.5秒展示极端对比画面",
        "tags": ["高点击", "强反转"],
        "usageCount": 1240,
        "rating": 4.9
      }
    ],
    "total": 6,
    "page": 1,
    "limit": 15
  }
}
```

#### 4. 认证

##### 登录
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "demo@example.com",
  "password": "123456"
}
```

响应：
```json
{
  "code": 0,
  "data": {
    "accessToken": "eyJ...",
    "refreshToken": "eyJ...",
    "user": {
      "id": "user_001",
      "email": "demo@example.com",
      "name": "Demo User"
    }
  }
}
```

---

## 数据库设计

### Job表 (jobs)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(PK) | Job ID (job_xxx) |
| mode | Enum | learn/compare |
| status | Enum | queued/running/succeeded/failed |
| progress_stage | String | 当前阶段 |
| progress_percent | Float | 进度百分比 |
| progress_message | String | 进度消息 |
| result_json | Text | 最终结果JSON |
| partial_result_json | Text | 部分结果JSON |
| error_message | Text | 错误信息 |
| title | String | AI生成的标题 |
| learning_points_json | Text | 学习要点JSON |
| thumbnail_url | String | 缩略图URL |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| started_at | DateTime | 开始时间 |
| completed_at | DateTime | 完成时间 |

### Asset表 (assets)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(PK) | Asset ID |
| job_id | String(FK) | 关联的Job ID |
| role | Enum | target/reference |
| source_type | Enum | url/file/generated |
| source_url | String | 源URL |
| local_path | String | 本地路径 |
| metadata_json | Text | 元数据JSON |
| created_at | DateTime | 创建时间 |

### Artifact表 (artifacts)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(PK) | Artifact ID |
| job_id | String(FK) | 关联的Job ID |
| artifact_type | Enum | keyframe/segment_video等 |
| file_path | String | 文件路径 |
| metadata_json | Text | 元数据JSON |
| created_at | DateTime | 创建时间 |

---

## 开发指南

### 环境准备

1. **安装Python 3.10+**
```bash
python --version
```

2. **创建虚拟环境**
```bash
conda create -n IntuitionX python=3.10
conda activate IntuitionX
```

3. **安装依赖**
```bash
cd video_ai_demo
pip install -r requirements.txt
```

4. **安装ffmpeg**
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

### 配置环境变量

创建 `.env` 文件：
```bash
# LLM配置
MM_LLM_BASE_URL=https://api.openai.com/v1
MM_LLM_API_KEY=sk-xxx
MM_LLM_MODEL=gpt-4o

# JWT配置
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 启动开发服务器

```bash
# 方式1: 使用start.sh
./start.sh

# 方式2: 直接运行
python -m app.main

# 方式3: 使用uvicorn（支持热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 开发流程

#### 1. 添加新的API端点

1. 在 `app/api/` 创建或编辑路由文件
2. 定义Pydantic模型
3. 实现处理函数
4. 在 `app/main.py` 注册路由

示例：
```python
# app/api/routes_example.py
from fastapi import APIRouter
from pydantic import BaseModel
from ..core.response import success_response

router = APIRouter(prefix="/example", tags=["示例"])

class ExampleRequest(BaseModel):
    name: str

@router.post("/hello")
async def hello(request: ExampleRequest):
    return success_response(
        data={"message": f"Hello, {request.name}!"}
    )
```

```python
# app/main.py
from .api import routes_example

app.include_router(routes_example.router, prefix="/api/v1")
```

#### 2. 添加数据库模型

1. 在 `app/db/models.py` 定义模型
2. 在 `app/db/repo.py` 添加仓储方法
3. 运行数据库迁移（如果需要）

#### 3. 集成外部服务

1. 在 `app/integrations/` 创建客户端类
2. 实现异步方法
3. 添加错误处理和重试逻辑

### 代码规范

- 使用 **Type Hints**
- 遵循 **PEP 8** 编码规范
- API函数添加详细的 **Docstring**
- 使用 **async/await** 处理异步操作
- 错误处理使用统一的 **error_response**

### 测试

```bash
# 运行测试
pytest tests/

# 测试单个文件
pytest tests/test_contract.py -v

# 测试覆盖率
pytest --cov=app tests/
```

---

## 部署指南

### 生产环境部署

#### 1. 使用Gunicorn + Uvicorn

```bash
# 安装
pip install gunicorn

# 启动
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

#### 2. 使用Systemd

创建服务文件 `/etc/systemd/system/video-analysis.service`：
```ini
[Unit]
Description=Video Analysis API
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/video_ai_demo
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable video-analysis
sudo systemctl start video-analysis
```

#### 3. 使用Docker

创建 `Dockerfile`：
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 创建数据目录
RUN mkdir -p data/jobs data/uploads

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：
```bash
docker build -t video-analysis-api .
docker run -d -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e MM_LLM_API_KEY=sk-xxx \
  video-analysis-api
```

#### 4. 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 超时设置
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
    
    # 静态文件
    location /data/ {
        alias /path/to/video_ai_demo/data/;
        autoindex off;
    }
}
```

---

## 配置说明

### 核心配置 (app/core/config.py)

```python
class Settings:
    # 应用配置
    app_name: str = "Video Analysis API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # 数据目录
    data_dir: Path = Path(__file__).parent.parent.parent / "data"
    
    # LLM配置
    mm_llm_base_url: str = "https://api.openai.com/v1"
    mm_llm_api_key: str = ""
    mm_llm_model: str = "gpt-4o"
    
    # JWT配置
    jwt_secret_key: str = "your-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # 数据库配置
    database_url: str = "sqlite:///./data/demo.db"
```

### 环境变量

所有配置项都可以通过环境变量覆盖，格式为大写+下划线：

```bash
export MM_LLM_API_KEY=sk-xxx
export JWT_SECRET_KEY=your-secret-key
export DEBUG=true
```

---

## 常见问题

### 1. 视频分析失败

**问题**：提取视频帧失败

**解决**：
- 检查ffmpeg是否安装：`ffmpeg -version`
- 检查视频文件格式是否支持
- 检查文件路径权限

### 2. LLM调用失败

**问题**：LLM API返回错误

**解决**：
- 检查API Key是否正确
- 检查API余额
- 检查网络连接
- 查看日志中的详细错误信息

### 3. 数据库锁定

**问题**：SQLite database is locked

**解决**：
- SQLite不支持高并发写入
- 考虑使用PostgreSQL或MySQL
- 减少并发请求数

### 4. 内存缓存丢失

**问题**：重启服务后分析结果丢失

**解决**：
- 内存缓存在重启后会清空（设计如此）
- 如需持久化，考虑使用Redis
- 或者将结果存入数据库

### 5. 文件上传失败

**问题**：视频文件过大导致上传失败

**解决**：
- 调整FastAPI的最大上传大小
- 配置Nginx的client_max_body_size
- 考虑使用分片上传

---

## 附录

### A. 项目依赖

详见 `requirements.txt`

### B. 相关文档

- [API_REANDME.md](../API_REANDME.md) - API接口文档
- [QUICKSTART.md](./QUICKSTART.md) - 快速开始指南
- [VIDEO_ANALYSIS_GUIDE.md](./VIDEO_ANALYSIS_GUIDE.md) - 视频分析指南
- [UPGRADE_GUIDE.md](./UPGRADE_GUIDE.md) - 升级指南

### C. 许可证

本项目采用 MIT 许可证

### D. 联系方式

- 项目仓库：[GitHub](https://github.com/your-repo)
- 问题反馈：[Issues](https://github.com/your-repo/issues)

---

**最后更新**: 2026-01-02

**版本**: v1.0.0

