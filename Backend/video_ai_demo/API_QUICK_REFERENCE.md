# API 快速参考卡

## 🔐 认证

```bash
# 登录
POST /api/v1/auth/login
Body: {"email": "demo@example.com", "password": "demo123"}

# 后续请求携带Token
Authorization: Bearer {token}
```

---

## 📊 仪表板

```bash
# 统计数据
GET /api/v1/dashboard/stats

# 项目列表
GET /api/v1/dashboard/projects?page=1&limit=10

# 日程
GET /api/v1/dashboard/schedule
```

---

## 🎬 视频分析

```bash
# 创建分析（新接口）
POST /api/v1/analysis/create
Body: {"url": "https://...", "platform": "auto"}

# 获取分析结果
GET /api/v1/analysis/{analysis_id}

# 获取分析状态
GET /api/v1/analysis/{analysis_id}/status

# --- 原有接口 ---

# 创建任务（原接口）
POST /v1/video-analysis/jobs
Body: {
  "mode": "learn",
  "target_video": {
    "source": {"type": "file", "path": "/path/to/video.mp4"}
  },
  "options": {
    "frame_extract": {"fps": 1.0, "max_frames": 20}
  }
}

# 查询任务
GET /v1/video-analysis/jobs/{job_id}

# 历史记录
GET /v1/video-analysis/history?limit=50

# 删除任务
DELETE /v1/video-analysis/jobs/{job_id}
```

---

## 📚 知识库

```bash
# 列表
GET /api/v1/knowledge/items?category=hooks&search=视觉&page=1&limit=15

# 详情
GET /api/v1/knowledge/items/{item_id}

# 收藏
POST /api/v1/knowledge/items/{item_id}/bookmark

# 取消收藏
DELETE /api/v1/knowledge/items/{item_id}/bookmark
```

---

## 👤 用户

```bash
# 用户信息
GET /api/v1/user/profile

# 更新信息
PATCH /api/v1/user/profile
Body: {"name": "新名字", "avatar": "https://..."}

# 配额信息
GET /api/v1/user/quota

# 升级订阅
POST /api/v1/user/upgrade?plan=pro

# 统计数据
GET /api/v1/user/stats
```

---

## 📖 术语查询

```bash
# 所有术语
GET /v1/terminology/shots

# 术语列表
GET /v1/terminology/shots/list

# 单个术语
GET /v1/terminology/shots/{shot_key}

# 翻译
GET /v1/terminology/shots/translate/{shot_key}
```

---

## 🎯 知识库分类

- `hooks` - 钩子技巧
- `narrative` - 叙事结构
- `style` - 剪辑风格
- `bgm` - 背景音乐
- `fingerprints` - 个人标识

---

## ⚠️ 错误码

| 错误码 | 描述 |
|--------|------|
| INVALID_URL | 视频链接格式不正确 |
| INVALID_TOKEN | Token无效或过期 |
| UNAUTHORIZED | 未授权 |
| RESOURCE_NOT_FOUND | 资源不存在 |
| QUOTA_EXCEEDED | 配额已用完 |
| INTERNAL_ERROR | 服务器错误 |

---

## 📝 响应格式

### 成功
```json
{
  "success": true,
  "data": {...},
  "message": "操作成功",
  "timestamp": 1704153600000
}
```

### 失败
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": null
  },
  "timestamp": 1704153600000
}
```

---

## 🚀 快速开始

```bash
# 1. 启动服务
cd video_ai_demo
python -m app.main

# 2. 访问文档
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc

# 3. 测试API
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123"}'
```

---

## 📦 演示账号

- **邮箱**: 任意邮箱
- **密码**: `demo123`
- **套餐**: Pro（演示）

---

## 🔗 相关文档

- [完整API文档](./API_GUIDE.md)
- [原始需求文档](./API_REANDME.md)
- [项目README](./README.md)

