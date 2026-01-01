# 快速入门指南

## 5分钟快速上手

### 1. 安装依赖

```bash
cd video_ai_demo
pip install -r requirements.txt

# 安装CV场景检测依赖（推荐）
bash install_cv_deps.sh
```

### 2. 配置API密钥

复制配置示例：
```bash
cp .env.example .env
```

编辑 `.env` 文件，修改API密钥：
```bash
MM_LLM_API_KEY=你的实际API密钥
```

### 3. 启动服务

使用启动脚本：
```bash
./start.sh
```

或手动启动：
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. 访问API文档

浏览器打开：http://localhost:8000/docs

你会看到交互式API文档，可以直接在浏览器中测试API。

### 5. 测试API

#### 方式1：使用Swagger UI（推荐）

1. 访问 http://localhost:8000/docs
2. 找到 `POST /v1/video-analysis/jobs`
3. 点击 "Try it out"
4. 输入请求数据（见下方示例）
5. 点击 "Execute"

#### 方式2：使用curl

创建一个Learn Job：
```bash
curl -X POST "http://localhost:8000/v1/video-analysis/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "learn",
    "target_video": {
      "source": {
        "type": "url",
        "url": "https://example.com/test.mp4"
      }
    },
    "options": {
      "frame_extract": {
        "fps": 1,
        "max_frames": 30
      }
    }
  }'
```

会返回：
```json
{
  "job_id": "job_abc123456",
  "status": "queued",
  "status_url": "/v1/video-analysis/jobs/job_abc123456"
}
```

查询Job状态：
```bash
curl "http://localhost:8000/v1/video-analysis/jobs/job_abc123456"
```

#### 方式3：使用示例脚本

```bash
./examples/curl_examples.sh
```

## 本地测试（不需要真实视频）

如果你想先测试系统是否能运行，可以：

1. **使用本地视频文件**：
```json
{
  "mode": "learn",
  "target_video": {
    "source": {
      "type": "file",
      "path": "/path/to/your/local/video.mp4"
    }
  }
}
```

2. **准备测试视频**：
   - 随便找一个短视频（10-30秒）
   - 放到可访问的URL或本地路径

3. **调整抽帧参数**（减少API调用）：
```json
{
  "options": {
    "frame_extract": {
      "fps": 0.5,
      "max_frames": 10
    }
  }
}
```

## 完整的Learn模式示例

### 推荐：CV检测 + LLM分析（混合方案）

```bash
curl -X POST "http://localhost:8000/v1/video-analysis/jobs" \
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
        "threshold": 27.0
      },
      "frame_extract": {
        "fps": 1,
        "max_frames": 30
      },
      "llm": {
        "enabled_modules": ["camera_motion", "lighting", "color_grading"]
      }
    }
  }'
```

**优势**：
- ✅ CV精准检测镜头切换（不漏检）
- ✅ LLM准确分析特征（运镜、光线、调色）
- ✅ 速度快、成本低、结果稳定

### 传统：纯LLM检测（不推荐）

```bash
curl -X POST "http://localhost:8000/v1/video-analysis/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "learn",
    "target_video": {
      "source": {
        "type": "url",
        "url": "https://example.com/demo.mp4"
      }
    },
    "options": {
      "scene_detection": {
        "use_cv": false
      },
      "frame_extract": {
        "fps": 2,
        "max_frames": 120
      }
    }
  }'
```

## 完整的Compare模式示例

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
        "fps": 1.5,
        "max_frames": 100
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

## 常见问题

### Q: 启动时提示找不到ffmpeg

**A:** 需要安装ffmpeg：
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg`
- Windows: 从 https://ffmpeg.org/download.html 下载

### Q: Job一直处于running状态

**A:** 可能的原因：
1. 视频下载慢（检查网络）
2. LLM API调用慢（正常，耐心等待）
3. 查看终端日志，看具体在哪个步骤

### Q: Job失败了，如何查看错误？

**A:** 查询Job详情会返回error信息：
```bash
curl "http://localhost:8000/v1/video-analysis/jobs/job_xxx"
```

查看 `error.message` 和 `error.details` 字段。

### Q: 如何减少API费用？

**A:** 调整抽帧参数：
- 降低 `fps`（如0.5表示每2秒1帧）
- 降低 `max_frames`（如30表示最多30帧）
- 使用短视频测试

### Q: 数据存储在哪里？

**A:** 所有数据在 `./data/` 目录：
- `demo.db` - SQLite数据库
- `jobs/job_xxx/` - 每个Job的工作目录

可以随时删除清理空间。

### Q: 如何重启服务？

**A:** 
1. 按 Ctrl+C 停止服务
2. 再次运行 `./start.sh` 或 `uvicorn` 命令

数据会保留在数据库中。

## 下一步

- 查看 [README.md](README.md) 了解完整文档
- 查看 [API文档](http://localhost:8000/docs) 了解所有接口
- 查看 `data/jobs/` 目录了解生成的文件结构
- 修改 `app/` 目录的代码进行二次开发

## 获取帮助

如有问题：
1. 查看终端日志
2. 查看 `data/demo.db` 数据库内容
3. 提交Issue

祝使用愉快！ 🎬

