# 快速参考卡片 - 视频分析系统后端

## 🚀 一分钟启动

```bash
# 1. 激活环境
conda activate IntuitionX

# 2. 配置API Key
export MM_LLM_API_KEY=sk-your-key

# 3. 启动服务
./start.sh

# 访问: http://localhost:8000/docs
```

---

## 📡 核心API速查

### 视频分析（同步）

```bash
# 上传
POST /api/v1/analysis/upload
FormData: file

# 分析（直接返回完整结果）
POST /api/v1/analysis/create
Body: {"url": "/path/to/video.mp4"}
→ 返回完整VideoAnalysis对象

# 查询状态
GET /api/v1/analysis/{id}/status
→ analysis_xxx格式立即返回completed

# 获取结果
GET /api/v1/analysis/{id}
→ 从缓存读取
```

### Dashboard

```bash
GET /api/v1/stats          # 统计数据
GET /api/v1/projects       # 项目列表
GET /api/v1/schedule       # 日程安排
```

### Knowledge Base

```bash
GET /api/v1/knowledge/items                    # 列表
GET /api/v1/knowledge/items/{id}               # 详情
POST /api/v1/knowledge/items/{id}/bookmark     # 收藏
```

### 认证

```bash
POST /api/v1/auth/login     # 登录
POST /api/v1/auth/register  # 注册
```

---

## 🗂️ 项目结构速查

```
app/
├── main.py              # 入口
├── api/
│   ├── routes_analysis.py    ⭐️ 视频分析
│   ├── routes_dashboard.py   📊 仪表盘
│   └── routes_knowledge.py   📚 知识库
├── core/
│   ├── config.py        # 配置
│   ├── auth.py          # 认证
│   └── response.py      # 响应格式
├── db/
│   ├── models.py        # 数据模型
│   └── repo.py          # 数据仓储
├── pipeline/
│   ├── orchestrator.py  # Pipeline编排
│   └── steps/
│       ├── extract_frames.py    # 提取帧
│       └── format_analysis.py   # 格式化分析
└── integrations/
    └── mm_llm_client.py  # LLM客户端
```

---

## 🔑 环境变量速查

```bash
# 必填
MM_LLM_API_KEY=sk-xxx

# 可选
MM_LLM_BASE_URL=https://api.openai.com/v1
MM_LLM_MODEL=gpt-4o
JWT_SECRET_KEY=your-secret
DEBUG=false
```

---

## 📦 数据结构速查

### VideoAnalysis（分析结果）

```json
{
  "id": "analysis_xxx",
  "analysisId": "analysis_xxx",
  "title": "视频标题",
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
  "hookDetails": {...},
  "editingStyle": {...},
  "audienceResponse": {...}
}
```

### 统一响应格式

```json
{
  "code": 0,
  "message": "成功",
  "data": {...}
}
```

---

## 🐛 常见问题速查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 视频帧提取失败 | 缺少ffmpeg | `brew install ffmpeg` |
| LLM调用失败 | API Key错误 | 检查 `MM_LLM_API_KEY` |
| 端口占用 | 8000被占用 | `lsof -i :8000` 然后 `kill` |
| 数据库锁定 | SQLite并发限制 | 减少并发或换PostgreSQL |
| 分析结果丢失 | 服务重启 | 内存缓存，重启会清空 |

---

## 🔧 开发命令速查

```bash
# 启动
python -m app.main
uvicorn app.main:app --reload  # 热重载

# 测试
pytest tests/
pytest tests/ -v              # 详细输出
pytest --cov=app tests/       # 覆盖率

# 格式化
black app/
isort app/

# 类型检查
mypy app/
```

---

## 📊 性能参数速查

| 项目 | 值 |
|------|------|
| 分析延迟 | 5-15秒 |
| 帧提取 | 每2秒1帧，最多5帧 |
| 缓存时间 | 24小时 |
| 缓存容量 | 最多100个 |
| 推荐workers | 4-8个 |
| 内存占用 | ~200MB |

---

## 📚 文档导航

- [README_BACKEND.md](README_BACKEND.md) - 后端服务说明
- [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) - 完整项目文档
- [API_REANDME.md](../API_REANDME.md) - 前后端API文档
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [VIDEO_ANALYSIS_GUIDE.md](VIDEO_ANALYSIS_GUIDE.md) - 分析指南

---

## 🎯 核心流程速查

### 视频分析流程

```
上传视频
  ↓
POST /api/v1/analysis/upload
  ↓
获得文件路径
  ↓
POST /api/v1/analysis/create
  ↓
提取5帧 → LLM分析 → 格式化 → 缓存
  ↓
立即返回完整结果
```

### 添加新API

```python
# 1. 创建路由文件 app/api/routes_xxx.py
from fastapi import APIRouter
router = APIRouter(prefix="/xxx", tags=["XXX"])

@router.get("/test")
async def test():
    return success_response(data={})

# 2. 注册路由 app/main.py
from .api import routes_xxx
app.include_router(routes_xxx.router, prefix="/api/v1")
```

### 调用LLM

```python
from app.integrations.mm_llm_client import MMHLLMClient, FrameInput

client = MMHLLMClient()
frames = [FrameInput(ts_ms=0, image_path="/path/to/frame.jpg")]
result = await client._call_api(frames=frames, prompt="分析这个视频")
```

---

## 🔐 认证速查

### 可选认证（推荐用于Demo）

```python
from ..core.auth import optional_user

@router.get("/data")
async def get_data(current_user: Optional[User] = Depends(optional_user)):
    # current_user可能为None，无需token即可访问
    pass
```

### 强制认证

```python
from ..core.auth import get_current_user

@router.get("/data")
async def get_data(current_user: User = Depends(get_current_user)):
    # 必须提供有效token
    pass
```

---

**快速查阅 | 最后更新: 2026-01-02**

