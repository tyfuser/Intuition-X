# 视频分析使用指南

## 📹 支持的视频来源

### ✅ 推荐方式：上传本地视频文件

最稳定可靠的方式是上传本地视频文件：

```javascript
// 步骤1: 上传视频文件
const formData = new FormData();
formData.append('file', videoFile);  // videoFile 是用户选择的文件

const uploadResponse = await fetch('/api/v1/analysis/upload', {
  method: 'POST',
  body: formData
});

const uploadResult = await uploadResponse.json();
// 返回: { filePath: "/path/to/uploaded/video.mp4", fileName: "...", fileSize: 123456 }

// 步骤2: 使用上传后的文件路径创建分析任务
const analysisResponse = await fetch('/api/v1/analysis/create', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    url: uploadResult.data.filePath,  // 使用上传返回的路径
    platform: 'auto'
  })
});

const analysisResult = await analysisResponse.json();
// 返回: { analysisId: "job_xxx", status: "queued", estimatedTime: 120 }
```

### ⚠️ 使用本地文件路径

如果视频已经在服务器上，可以直接使用文件路径：

```javascript
const response = await fetch('/api/v1/analysis/create', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    url: '/Users/username/Videos/my_video.mp4',  // 绝对路径
    platform: 'auto'
  })
});
```


```

