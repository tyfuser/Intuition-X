# 视频分析系统 - 后端服务

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于AI大模型的短视频智能分析平台后端服务

[功能特性](#功能特性) • [快速开始](#快速开始) • [API文档](#api文档) • [完整文档](PROJECT_DOCUMENTATION.md)

</div>

---

## 📖 项目简介

视频分析系统后端服务提供完整的短视频AI分析能力，通过多模态大模型自动识别视频中的专业特征（运镜、光影、调色等），生成详细的爆款因素分析报告。

### 核心能力

- 🎬 **智能视频分析** - 基于LLM的多模态视频内容理解
- 📊 **格式化输出** - 结构化的分析报告，可直接用于可视化
- 💾 **知识库管理** - 短视频创作技巧的知识沉淀
- ⚡ **快速响应** - 同步分析，秒级返回结果
- 🔐 **可选认证** - 支持JWT认证，也支持无token访问

---

## ✨ 功能特性

### 1. 视频分析 API

```python
# 同步分析流程
上传视频 → 提取关键帧 → LLM分析 → 返回完整报告
```

**特点**：
- 每2秒提取1帧，最多5帧（快速模式）
- 内存缓存24小时，最多100个结果
- 智能降级，LLM失败时返回基础分析
- 支持本地文件和URL

### 2. Dashboard API

基于真实Job数据的统计仪表盘：
- 总任务数、完成率、总时长
- 平均分数、最近项目列表
- 日程安排

### 3. Knowledge Base API

短视频创作知识库：
- 5大分类：钩子、叙事、风格、BGM、指纹
- 支持搜索和筛选
- 收藏功能

### 4. Authentication API

JWT Token认证：
- 登录/注册
- Token刷新
- 可选认证（大多数API无需token）

---

## 🚀 快速开始

### 前置要求

- Python 3.10+
- ffmpeg
- Conda（推荐）或 venv

### 1. 克隆项目

```bash
git clone <repo-url>
cd video_ai_demo
```

### 2. 创建虚拟环境

```bash
conda create -n IntuitionX python=3.10
conda activate IntuitionX
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

### 5. 配置环境变量

创建 `.env` 文件：

```bash
# LLM配置（必填）
MM_LLM_BASE_URL=https://api.openai.com/v1
MM_LLM_API_KEY=sk-your-api-key-here
MM_LLM_MODEL=gpt-4o

# JWT配置（可选）
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
```

### 6. 启动服务

```bash
# 方式1: 使用启动脚本
./start.sh

# 方式2: 直接运行
python -m app.main

# 方式3: 开发模式（热重载）
uvicorn app.main:app --reload
```

访问：
- API服务：http://localhost:8000
- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

---

## 📡 API文档

### 统一响应格式

#### 成功
```json
{
  "code": 0,
  "message": "操作成功",
  "data": { ... }
}
```

#### 失败
```json
{
  "code": 1001,
  "message": "错误描述",
  "data": null
}
```

### 核心端点

#### 视频分析

```bash
# 1. 上传视频
curl -X POST http://localhost:8000/api/v1/analysis/upload \
  -F "file=@video.mp4"

# 2. 分析视频（同步返回完整结果）
curl -X POST http://localhost:8000/api/v1/analysis/create \
  -H "Content-Type: application/json" \
  -d '{"url": "/path/to/video.mp4"}'

# 3. 查询状态（可选，同步分析会立即返回completed）
curl http://localhost:8000/api/v1/analysis/{analysis_id}/status

# 4. 获取结果（从缓存读取）
curl http://localhost:8000/api/v1/analysis/{analysis_id}
```

#### Dashboard

```bash
# 获取统计数据
curl http://localhost:8000/api/v1/stats

# 获取项目列表
curl http://localhost:8000/api/v1/projects?page=1&limit=10

# 获取日程
curl http://localhost:8000/api/v1/schedule
```

#### Knowledge Base

```bash
# 获取知识库列表
curl http://localhost:8000/api/v1/knowledge/items?category=hooks

# 获取单个条目
curl http://localhost:8000/api/v1/knowledge/items/kb_001

# 收藏
curl -X POST http://localhost:8000/api/v1/knowledge/items/kb_001/bookmark
```

#### 认证

```bash
# 登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "123456"
  }'
```

完整API文档：http://localhost:8000/docs

---

## 🏗️ 项目架构

```
┌─────────────────┐
│   Frontend      │  React + Vite + TypeScript
└────────┬────────┘
         │ REST API
┌────────▼────────┐
│  FastAPI Layer  │  routes_*.py
└────────┬────────┘
         │
┌────────▼────────┐
│ Business Logic  │  Pipeline + LLM Client
└────────┬────────┘
         │
┌────────▼────────┐
│   Data Layer    │  SQLite + File Storage
└─────────────────┘
```

### 目录结构

```
video_ai_demo/
├── app/
│   ├── main.py              # FastAPI入口
│   ├── api/                 # API路由层
│   │   ├── routes_analysis.py    ⭐️ 核心分析API
│   │   ├── routes_dashboard.py
│   │   └── routes_knowledge.py
│   ├── core/                # 核心模块
│   │   ├── config.py
│   │   ├── auth.py
│   │   └── response.py
│   ├── db/                  # 数据库
│   │   ├── models.py
│   │   └── repo.py
│   ├── pipeline/            # 视频处理
│   │   ├── orchestrator.py
│   │   └── steps/
│   └── integrations/        # 外部服务
│       └── mm_llm_client.py
├── data/                    # 数据存储
│   ├── demo.db
│   ├── jobs/
│   └── uploads/
└── requirements.txt
```

---

## 🔧 配置说明

### 环境变量

| 变量 | 说明 | 默认值 | 必填 |
|------|------|--------|------|
| `MM_LLM_BASE_URL` | LLM API地址 | https://api.openai.com/v1 | 否 |
| `MM_LLM_API_KEY` | LLM API密钥 | - | ✅ |
| `MM_LLM_MODEL` | LLM模型名称 | gpt-4o | 否 |
| `JWT_SECRET_KEY` | JWT密钥 | - | 推荐 |
| `DEBUG` | 调试模式 | false | 否 |

### 数据库

默认使用SQLite，数据库文件：`data/demo.db`

生产环境推荐使用PostgreSQL或MySQL。

---

## 📊 性能指标

- **视频分析延迟**：5-15秒（取决于LLM响应时间）
- **并发处理**：建议4-8 workers
- **内存占用**：~200MB（基础）+ 缓存
- **缓存策略**：内存缓存，24小时过期，最多100个

---

## 🐛 故障排查

### 1. 视频帧提取失败

```bash
# 检查ffmpeg
ffmpeg -version

# 检查视频文件
ffmpeg -i your_video.mp4
```

### 2. LLM调用失败

```bash
# 检查API Key
echo $MM_LLM_API_KEY

# 测试连接
curl -H "Authorization: Bearer $MM_LLM_API_KEY" \
  https://api.openai.com/v1/models
```

### 3. 端口被占用

```bash
# 查找占用8000端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

---

## 📚 扩展阅读

- [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) - 完整项目文档
- [API_REANDME.md](../API_REANDME.md) - 前后端API接口文档
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [VIDEO_ANALYSIS_GUIDE.md](VIDEO_ANALYSIS_GUIDE.md) - 视频分析详细指南

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发流程

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范

- 遵循PEP 8
- 使用Type Hints
- 添加详细的Docstring
- 单元测试覆盖率 > 80%

---

## 📝 更新日志

### v1.0.0 (2026-01-02)

- ✨ 初始版本发布
- 🎬 支持同步视频分析
- 📊 Dashboard统计功能
- 📚 知识库管理
- 🔐 JWT认证

---

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证

---

## 💬 联系方式

- 问题反馈：[GitHub Issues](https://github.com/your-repo/issues)
- 邮箱：your-email@example.com

---

<div align="center">

**[⬆ 回到顶部](#视频分析系统---后端服务)**

Made with ❤️ by Your Team

</div>

