# 部署说明

## 🚀 快速部署

### 1. 环境准备

```bash
# Python 3.8+
python --version

# 安装依赖
cd video_ai_demo
pip install -r requirements.txt

# 如果使用CV检测功能
./install_cv_deps.sh
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# API配置
API_HOST=0.0.0.0
API_PORT=8000

# 多模态LLM配置
MM_LLM_BASE_URL=https://www.sophnet.com/api/open-apis/v1
MM_LLM_API_KEY=your_api_key_here
MM_LLM_MODEL=Qwen2.5-VL-7B-Instruct

# 认证密钥（生产环境必须修改）
SECRET_KEY=your-very-long-and-secure-secret-key-here

# 数据库
SQLITE_PATH=./data/demo.db
DATA_DIR=./data
```

### 3. 启动服务

#### 开发模式

```bash
# 方式1：直接运行
python -m app.main

# 方式2：使用启动脚本
./start.sh

# 方式3：使用uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 生产模式

```bash
# 使用Gunicorn + Uvicorn Workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

### 4. 验证部署

```bash
# 健康检查
curl http://localhost:8000/health

# 运行测试
python test_api.py
```

---

## 🐳 Docker部署

### 创建Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 构建和运行

```bash
# 构建镜像
docker build -t video-ai-api .

# 运行容器
docker run -d \
  --name video-ai-api \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e MM_LLM_API_KEY=your_api_key \
  -e SECRET_KEY=your_secret_key \
  video-ai-api

# 查看日志
docker logs -f video-ai-api
```

### Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - MM_LLM_API_KEY=${MM_LLM_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - API_HOST=0.0.0.0
      - API_PORT=8000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped
```

启动：

```bash
docker-compose up -d
```

---

## 🌐 Nginx反向代理

### nginx.conf

```nginx
upstream video_ai_api {
    server localhost:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL证书
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # SSL配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 客户端上传限制
    client_max_body_size 500M;

    # API代理
    location /api/ {
        proxy_pass http://video_ai_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # 原有API代理
    location /v1/ {
        proxy_pass http://video_ai_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 文档
    location /docs {
        proxy_pass http://video_ai_api;
        proxy_set_header Host $host;
    }

    # 前端静态文件
    location / {
        root /var/www/frontend;
        try_files $uri $uri/ /index.html;
    }
}
```

---

## 📊 监控和日志

### Systemd服务

创建 `/etc/systemd/system/video-ai-api.service`：

```ini
[Unit]
Description=Video AI API Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/video-ai-api
Environment="PATH=/opt/video-ai-api/venv/bin"
ExecStart=/opt/video-ai-api/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

管理服务：

```bash
# 启动服务
sudo systemctl start video-ai-api

# 设置开机自启
sudo systemctl enable video-ai-api

# 查看状态
sudo systemctl status video-ai-api

# 查看日志
sudo journalctl -u video-ai-api -f
```

### 日志配置

修改 `app/core/logging.py`，添加文件日志：

```python
import logging
from logging.handlers import RotatingFileHandler

# 文件日志
file_handler = RotatingFileHandler(
    'logs/api.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
```

---

## 🔒 安全配置

### 1. 防火墙设置

```bash
# 只开放必要端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. 限制访问

```nginx
# 在nginx.conf中添加
location /api/v1/admin/ {
    allow 192.168.1.0/24;
    deny all;
    proxy_pass http://video_ai_api;
}
```

### 3. Rate Limiting

安装依赖：

```bash
pip install slowapi
```

在 `app/main.py` 中添加：

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 应用到路由
@router.post("/analysis/create")
@limiter.limit("10/minute")
async def create_analysis(request: Request, ...):
    ...
```

---

## 📈 性能调优

### 1. 数据库优化

```sql
-- 添加索引
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_created_at ON jobs(created_at);
CREATE INDEX idx_jobs_user_id ON jobs(user_id);
```

### 2. 连接池配置

```python
# app/db/session.py
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

### 3. 缓存策略

使用Redis缓存：

```python
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(ttl=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

---

## 🔍 健康检查

### 详细健康检查端点

```python
@app.get("/health/detailed")
async def detailed_health_check():
    checks = {
        "api": "healthy",
        "database": check_database(),
        "llm_service": check_llm_service(),
        "disk_space": check_disk_space(),
        "memory": check_memory()
    }
    
    overall = all(v == "healthy" for v in checks.values())
    
    return {
        "status": "healthy" if overall else "degraded",
        "checks": checks,
        "timestamp": datetime.now().isoformat()
    }
```

---

## 📝 维护任务

### 定期清理

```bash
# 清理旧的分析任务（保留30天）
python -c "
from app.db.session import get_db
from app.db.repo import JobRepository
from datetime import datetime, timedelta

with get_db() as db:
    repo = JobRepository(db)
    cutoff = datetime.now() - timedelta(days=30)
    # 实现清理逻辑
"
```

### 备份数据

```bash
# 备份数据库
sqlite3 data/demo.db .dump > backup_$(date +%Y%m%d).sql

# 备份视频文件
tar -czf data_backup_$(date +%Y%m%d).tar.gz data/jobs/
```

---

## 🆘 故障排查

### 常见问题

1. **端口被占用**
   ```bash
   # 查找占用进程
   lsof -i :8000
   # 或
   netstat -tuln | grep 8000
   ```

2. **数据库锁定**
   ```bash
   # SQLite数据库被锁定
   # 检查是否有其他进程在使用
   fuser data/demo.db
   ```

3. **内存不足**
   ```bash
   # 监控内存使用
   free -h
   # 查看进程内存
   ps aux --sort=-%mem | head
   ```

---

## 📞 支持

遇到问题？

1. 查看日志：`sudo journalctl -u video-ai-api -f`
2. 运行测试：`python test_api.py`
3. 查看文档：`/docs` 或 `API_GUIDE.md`
4. 提交Issue：GitHub Issues

---

**部署愉快！** 🎉

