# 魔方 AI - API 使用指南

> **版本**: v1.0.0  
> **最后更新**: 2025-01-02  
> **基础URL**: `http://localhost:8000/api/v1`

---

## 📚 目录

1. [快速开始](#快速开始)
2. [认证说明](#认证说明)
3. [API概览](#api概览)
4. [详细接口文档](#详细接口文档)
5. [错误处理](#错误处理)
6. [示例代码](#示例代码)

---

## 快速开始

### 1. 启动服务

```bash
cd video_ai_demo
python -m app.main
# 或使用
./start.sh
```

服务将在 `http://localhost:8000` 启动

### 2. 查看API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. 第一个API调用

```bash
# 登录获取token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "demo123"
  }'
```

---

## 认证说明

### 登录流程

1. **调用登录接口** 获取 JWT Token
2. **在后续请求中携带 Token**

```http
Authorization: Bearer {your_token_here}
```

### Token 有效期

- 默认7天（604800秒）
- 过期后需要重新登录

### 演示账号

- **邮箱**: 任意邮箱
- **密码**: `demo123`

---

## API概览

### API架构

```
/api/v1/
├── auth/          # 认证相关
├── dashboard/     # 仪表板数据
├── analysis/      # 视频分析
├── knowledge/     # 知识库
└── user/          # 用户管理

/v1/video-analysis/  # 原有视频分析API（保持兼容）
/v1/terminology/     # 术语查询
```

### 统一响应格式

#### 成功响应

```json
{
  "success": true,
  "data": {
    // 实际数据
  },
  "message": "操作成功",
  "timestamp": 1704153600000
}
```

#### 错误响应

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

## 详细接口文档

### 1. 认证模块 (/api/v1/auth)

#### POST /auth/login
**用户登录**

请求体：
```json
{
  "email": "user@example.com",
  "password": "demo123"
}
```

响应：
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_example",
      "email": "user@example.com",
      "name": "Example",
      "avatar": "https://...",
      "subscription": "pro"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresIn": 604800
  }
}
```

#### POST /auth/register
**用户注册**（参数同登录）

#### POST /auth/logout
**用户登出**（客户端删除token即可）

---

### 2. 仪表板模块 (/api/v1/dashboard)

#### GET /dashboard/stats
**获取统计数据**

需要认证：✅

响应：
```json
{
  "success": true,
  "data": {
    "stats": [
      {
        "label": "已分析视频",
        "value": "128",
        "icon": "FileVideo",
        "color": "text-blue-400",
        "bg": "bg-blue-400/10"
      }
    ]
  }
}
```

#### GET /dashboard/projects
**获取项目列表**

需要认证：✅

查询参数：
- `page`: 页码（默认1）
- `limit`: 每页数量（默认10）
- `status`: 筛选状态
- `sortBy`: 排序方式（默认timestamp）

响应：
```json
{
  "success": true,
  "data": {
    "projects": [
      {
        "id": "job_xxx",
        "title": "视频标题",
        "thumbnail": "https://...",
        "timestamp": "10分钟前",
        "type": "视频分析",
        "score": 88,
        "status": "succeeded",
        "tags": ["AI分析"],
        "radarData": [...]
      }
    ],
    "total": 128,
    "page": 1,
    "limit": 10
  }
}
```

#### GET /dashboard/schedule
**获取日程热力图**

需要认证：✅

---

### 3. 视频分析模块 (/api/v1/analysis)

#### POST /analysis/create
**发起视频分析**

需要认证：否（可选）

请求体：
```json
{
  "url": "https://example.com/video.mp4",
  "platform": "auto"
}
```

响应：
```json
{
  "success": true,
  "data": {
    "analysisId": "analysis_20250102120000",
    "status": "queued",
    "estimatedTime": 120
  }
}
```

#### GET /analysis/{analysis_id}
**获取分析结果**

需要认证：否（可选）

响应：完整的视频分析数据（参见 API_REANDME.md）

#### GET /analysis/{analysis_id}/status
**获取分析状态**

需要认证：否（可选）

响应：
```json
{
  "success": true,
  "data": {
    "status": "processing",
    "progress": 65,
    "currentStep": "提取关键帧",
    "message": "正在处理..."
  }
}
```

---

### 4. 知识库模块 (/api/v1/knowledge)

#### GET /knowledge/items
**获取知识库列表**

需要认证：✅

查询参数：
- `category`: 分类筛选（hooks, narrative, style, bgm, fingerprints）
- `search`: 关键词搜索
- `page`: 页码
- `limit`: 每页数量

响应：
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "kb_001",
        "category": "hooks",
        "title": "视觉反差钩子",
        "description": "前0.5秒展示极端对比画面...",
        "tags": ["高点击", "强反转"],
        "usageCount": 1240,
        "rating": 4.9,
        "previewColor": "from-orange-500 to-red-500"
      }
    ],
    "total": 45,
    "page": 1,
    "limit": 15
  }
}
```

#### GET /knowledge/items/{item_id}
**获取知识库条目详情**

需要认证：✅

#### POST /knowledge/items/{item_id}/bookmark
**添加到收藏**

需要认证：✅

#### DELETE /knowledge/items/{item_id}/bookmark
**取消收藏**

需要认证：✅

---

### 5. 用户管理模块 (/api/v1/user)

#### GET /user/profile
**获取用户信息**

需要认证：✅

响应：
```json
{
  "success": true,
  "data": {
    "id": "user_xxx",
    "email": "user@example.com",
    "name": "用户名",
    "avatar": "https://...",
    "subscription": {
      "plan": "pro",
      "expiresAt": "2025-12-31T23:59:59Z",
      "features": ["无限视频分析", ...]
    },
    "usage": {
      "videosAnalyzed": 128,
      "scriptsGenerated": 45,
      "quota": {
        "daily": 100,
        "remaining": 73
      }
    },
    "createdAt": "2024-01-01T00:00:00Z",
    "lastLoginAt": "2025-01-02T12:00:00Z"
  }
}
```

#### PATCH /user/profile
**更新用户信息**

需要认证：✅

请求体：
```json
{
  "name": "新名字",
  "avatar": "https://..."
}
```

#### GET /user/quota
**获取配额信息**

需要认证：✅

#### POST /user/upgrade
**升级订阅**

需要认证：✅

查询参数：
- `plan`: 套餐类型（pro, enterprise）

#### GET /user/stats
**获取用户统计**

需要认证：✅

---

### 6. 原有视频分析API (/v1/video-analysis)

#### POST /v1/video-analysis/jobs
**创建分析任务**

请求体：
```json
{
  "mode": "learn",
  "target_video": {
    "source": {
      "type": "file",
      "path": "/path/to/video.mp4"
    }
  },
  "options": {
    "frame_extract": {
      "fps": 1.0,
      "max_frames": 20
    },
    "llm": {
      "enabled_modules": ["camera_motion", "lighting", "color_grading"]
    }
  }
}
```

响应：
```json
{
  "job_id": "job_xxx",
  "status": "queued",
  "status_url": "/v1/video-analysis/jobs/job_xxx"
}
```

#### GET /v1/video-analysis/jobs/{job_id}
**查询任务状态和结果**

响应：完整的任务信息（包括进度、结果等）

#### GET /v1/video-analysis/history
**获取历史记录**

查询参数：
- `limit`: 返回数量（默认50）

#### DELETE /v1/video-analysis/jobs/{job_id}
**删除任务**

---

## 错误处理

### 常见错误码

| 错误码 | 描述 | HTTP状态码 |
|--------|------|-----------|
| INVALID_URL | 视频链接格式不正确 | 400 |
| UNSUPPORTED_PLATFORM | 不支持的平台 | 400 |
| ANALYSIS_FAILED | 分析失败 | 500 |
| QUOTA_EXCEEDED | 配额已用完 | 429 |
| INVALID_TOKEN | Token无效或过期 | 401 |
| UNAUTHORIZED | 未授权 | 401 |
| FORBIDDEN | 权限不足 | 403 |
| RESOURCE_NOT_FOUND | 资源不存在 | 404 |
| INTERNAL_ERROR | 服务器内部错误 | 500 |

### 错误处理示例

```javascript
try {
  const response = await fetch('/api/v1/dashboard/stats', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const result = await response.json();
  
  if (!result.success) {
    // 处理错误
    console.error(result.error.code, result.error.message);
    
    if (result.error.code === 'INVALID_TOKEN') {
      // 跳转到登录页
      window.location.href = '/login';
    }
  } else {
    // 处理成功数据
    console.log(result.data);
  }
} catch (error) {
  console.error('请求失败:', error);
}
```

---

## 示例代码

### JavaScript/TypeScript

#### 创建API客户端

```javascript
class APIClient {
  constructor(baseURL = 'http://localhost:8000/api/v1') {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('token');
  }
  
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    const response = await fetch(url, {
      ...options,
      headers
    });
    
    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.error.message);
    }
    
    return result.data;
  }
  
  async login(email, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    
    this.token = data.token;
    localStorage.setItem('token', data.token);
    return data;
  }
  
  async getDashboardStats() {
    return this.request('/dashboard/stats');
  }
  
  async getProjects(page = 1, limit = 10) {
    return this.request(`/dashboard/projects?page=${page}&limit=${limit}`);
  }
  
  async createAnalysis(url, platform = 'auto') {
    return this.request('/analysis/create', {
      method: 'POST',
      body: JSON.stringify({ url, platform })
    });
  }
  
  async getKnowledgeItems(category = null, search = null, page = 1) {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search);
    params.append('page', page);
    
    return this.request(`/knowledge/items?${params}`);
  }
}

// 使用示例
const api = new APIClient();

// 登录
await api.login('demo@example.com', 'demo123');

// 获取统计数据
const stats = await api.getDashboardStats();
console.log(stats);

// 获取项目列表
const projects = await api.getProjects(1, 10);
console.log(projects);
```

### Python

```python
import requests
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def request(self, endpoint: str, method: str = "GET", 
                data: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        result = response.json()
        
        if not result.get("success"):
            raise Exception(result["error"]["message"])
        
        return result["data"]
    
    def login(self, email: str, password: str) -> Dict:
        data = self.request("/auth/login", "POST", {
            "email": email,
            "password": password
        })
        self.token = data["token"]
        return data
    
    def get_dashboard_stats(self) -> Dict:
        return self.request("/dashboard/stats")
    
    def get_projects(self, page: int = 1, limit: int = 10) -> Dict:
        return self.request(f"/dashboard/projects?page={page}&limit={limit}")
    
    def create_analysis(self, url: str, platform: str = "auto") -> Dict:
        return self.request("/analysis/create", "POST", {
            "url": url,
            "platform": platform
        })

# 使用示例
api = APIClient()

# 登录
login_data = api.login("demo@example.com", "demo123")
print(f"登录成功: {login_data['user']['name']}")

# 获取统计数据
stats = api.get_dashboard_stats()
print(f"统计数据: {stats}")

# 获取项目列表
projects = api.get_projects(page=1, limit=10)
print(f"项目总数: {projects['total']}")
```

---

## 开发建议

### 1. 环境配置

```bash
# .env 文件
MM_LLM_BASE_URL=https://www.sophnet.com/api/open-apis/v1
MM_LLM_API_KEY=your_api_key_here
MM_LLM_MODEL=Qwen2.5-VL-7B-Instruct

API_HOST=0.0.0.0
API_PORT=8000
```

### 2. 调试技巧

- 使用 Swagger UI (`/docs`) 进行API测试
- 查看日志输出了解请求处理流程
- 使用浏览器开发者工具监控网络请求

### 3. 性能优化

- 使用分页加载大量数据
- 缓存常用的API响应
- 使用WebSocket或轮询获取实时进度

### 4. 安全建议

- **生产环境必须修改** `SECRET_KEY`（在 `app/core/auth.py`）
- 使用HTTPS传输
- 定期更新token
- 验证用户输入

---

## 常见问题

### Q: Token过期怎么办？
A: 捕获401错误，重定向到登录页重新获取token

### Q: 如何批量处理视频？
A: 循环调用 `/v1/video-analysis/jobs` 创建多个任务，然后轮询状态

### Q: 如何获取分析进度？
A: 轮询 `/analysis/{analysis_id}/status` 或使用 `/v1/video-analysis/jobs/{job_id}` 获取详细进度

### Q: 支持哪些视频格式？
A: MP4, MOV, AVI等常见格式

---

## 更新日志

### v1.0.0 (2025-01-02)
- ✅ 完整的认证系统
- ✅ 仪表板统计API
- ✅ 视频分析API（整合现有功能）
- ✅ 知识库管理API
- ✅ 用户管理API
- ✅ 统一响应格式
- ✅ 完整的API文档

---

## 联系方式

- **GitHub**: https://github.com/your-repo
- **Email**: dev@example.com
- **问题反馈**: GitHub Issues

---

**Happy Coding! 🚀**

