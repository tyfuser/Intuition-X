# 历史记录功能指南

## 功能概述

将原来的 **Compare** 模式替换为 **History** 模式，提供完整的历史记录管理功能。

### 核心特性

1. **自动总结**：每次分析完成后，AI 自动生成任务标题和学习要点
2. **历史列表**：卡片式展示所有历史记录，包含缩略图、标题、学习要点
3. **快速查看**：点击历史记录即可查看完整的分析结果
4. **独立界面**：Learn 和 History 两个界面完全独立，互不干扰

---

## 数据库变更

### 新增字段

在 `jobs` 表中添加了三个新字段：

| 字段名 | 类型 | 说明 |
|-------|------|------|
| `title` | TEXT | AI生成的任务标题（10-20字） |
| `learning_points_json` | TEXT | 学习要点JSON数组（3-5个要点） |
| `thumbnail_url` | TEXT | 缩略图URL（可选，暂未实现） |

### 迁移脚本

```bash
cd /Users/tang/GitProj/Intuition-X/video_ai_demo
python migrate_add_summary_fields.py
```

---

## 后端改动

### 1. LLM 总结方法

**文件**: `app/integrations/mm_llm_client.py`

新增方法：
```python
async def summarize_video_analysis(
    segments: List[Dict[str, Any]],
    duration_ms: float
) -> Dict[str, Any]:
    """
    总结视频分析结果
    返回: {"title": "...", "learning_points": [...]}
    """
```

**Prompt 设计**：
- 输入：片段列表、时长、特征统计
- 输出：简洁标题 + 3-5个学习要点
- 格式：JSON

### 2. 数据模型扩展

**文件**: `app/db/models.py`

```python
class Job(Base):
    # ... 原有字段 ...
    
    # 新增总结字段
    title = Column(String)
    learning_points_json = Column(Text)
    thumbnail_url = Column(String)
```

### 3. Repository 方法

**文件**: `app/db/repo.py`

新增方法：
```python
def update_summary(job_id, title, learning_points) -> Job:
    """更新Job总结信息"""

def list_history(limit=50) -> List[Job]:
    """获取历史记录列表"""
```

### 4. Pipeline 集成

**文件**: `app/pipeline/orchestrator.py`

在任务完成时自动调用总结：

```python
async def _run_job(job_id, orchestrator):
    result = await orchestrator.execute()
    
    # 生成总结
    summary = await orchestrator._generate_summary(result)
    
    # 保存总结
    job_repo.update_summary(
        job_id,
        title=summary.get("title"),
        learning_points=summary.get("learning_points")
    )
```

### 5. API 路由

**文件**: `app/api/routes_jobs.py`

新增端点：
```python
@router.get("/history", response_model=List[HistoryItem])
async def get_history(limit: int = 50):
    """获取历史记录列表"""
```

响应模型：
```python
class HistoryItem(BaseModel):
    job_id: str
    title: Optional[str]
    status: str
    learning_points: List[str]
    segment_count: Optional[int]
    duration_sec: Optional[float]
    thumbnail_url: Optional[str]
    created_at: datetime
```

---

## 前端改动

### 1. 导航栏

**文件**: `frontend/index.html`

```html
<div class="nav-center">
    <button class="nav-tab active" data-mode="learn">Learn</button>
    <button class="nav-tab" data-mode="history">History</button>
</div>
```

### 2. 模式切换逻辑

**文件**: `frontend/js/app.js`

```javascript
function handleModeSwitch(mode) {
    if (mode === 'learn') {
        // 显示Learn界面
        // 恢复之前的状态
    } else if (mode === 'history') {
        // 显示History界面
        showHistoryView();
    }
}
```

### 3. 历史记录界面

**核心函数**：

```javascript
// 显示历史记录视图
async function showHistoryView()

// 加载历史记录数据
async function loadHistory()

// 渲染历史记录列表
function renderHistory(history)

// 加载历史任务详情
async function loadHistoryJob(jobId)

// 格式化时间显示
function formatDate(dateString)
```

**界面结构**：
```
┌─────────────────────────────────────────┐
│ 📚 分析历史              [🔄 刷新]      │
├─────────────────────────────────────────┤
│ ┌─────────────┐  ┌─────────────┐       │
│ │  [缩略图]   │  │  [缩略图]   │       │
│ │             │  │             │       │
│ │  标题       │  │  标题       │       │
│ │  ✓ 完成     │  │  ⟳ 进行中   │       │
│ │  📹 5镜头   │  │  📹 3镜头   │       │
│ │  ⏱️ 12.5s   │  │  ⏱️ 8.2s    │       │
│ │  📅 2小时前 │  │  📅 刚刚     │       │
│ │             │  │             │       │
│ │  💡学习要点 │  │  💡学习要点 │       │
│ │  • 要点1    │  │  • 要点1    │       │
│ │  • 要点2    │  │  • 要点2    │       │
│ └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────┘
```

### 4. 样式

**文件**: `frontend/css/style.css`

新增样式类：
- `.history-container` - 历史记录容器
- `.history-list` - 网格布局列表
- `.history-item` - 历史记录卡片
- `.history-thumbnail` - 缩略图区域
- `.status-badge` - 状态徽章
- `.learning-points-preview` - 学习要点预览

---

## 使用流程

### 1. 分析视频

```bash
# 上传视频进行分析
POST /v1/video-analysis/jobs
{
  "mode": "learn",
  "target_video": {...}
}
```

### 2. 自动总结

任务完成后，系统自动：
1. 调用 LLM 分析所有特征
2. 生成简洁标题（如"暖色调推镜头短片"）
3. 提取 3-5 个学习要点
4. 保存到数据库

### 3. 查看历史

点击 **History** 标签：
- 加载所有历史记录
- 卡片式展示
- 显示标题、状态、学习要点

### 4. 查看详情

点击任意历史记录：
- 自动切换回 Learn 模式
- 加载完整的分析结果
- 显示时间轴和详细特征

---

## 示例数据

### 总结示例

```json
{
  "title": "暖色调人物特写镜头分析",
  "learning_points": [
    "使用缓慢推镜头营造情感张力，引导观众关注人物表情",
    "采用三点布光塑造人物立体感，主光位于左前方45度",
    "暖色调调色（5500K-6500K）营造温暖舒适的氛围"
  ]
}
```

### 历史记录响应

```json
[
  {
    "job_id": "job_abc123",
    "title": "暖色调人物特写镜头分析",
    "status": "succeeded",
    "learning_points": [
      "使用缓慢推镜头营造情感张力...",
      "采用三点布光塑造人物立体感...",
      "暖色调调色营造温暖舒适的氛围"
    ],
    "segment_count": 5,
    "duration_sec": 12.5,
    "thumbnail_url": null,
    "created_at": "2026-01-01T18:30:00"
  }
]
```

---

## 技术亮点

### 1. 界面独立性

- Learn 和 History 完全独立
- 切换不影响后台任务
- 可以在分析进行中查看历史

### 2. 智能总结

- 基于所有特征的统计分析
- 自动提取关键技术点
- 生成专业且易懂的描述

### 3. 用户体验

- 卡片式布局，视觉清晰
- 状态徽章，一目了然
- 时间格式化，人性化显示
- 悬停动画，交互友好

### 4. 性能优化

- 历史记录分页加载
- 缩略图懒加载（预留）
- 网格布局自适应

---

## 配置说明

### API Key

确保配置了 MM_LLM_API_KEY：

```bash
# .env
MM_LLM_API_KEY=你的API密钥
```

### 数据库迁移

首次使用需要运行迁移脚本：

```bash
python migrate_add_summary_fields.py
```

---

## 故障排除

### 问题1：历史记录为空

**原因**：数据库中没有已完成的任务

**解决**：先完成至少一次视频分析

### 问题2：总结字段为空

**原因**：
- API Key 未配置
- LLM 调用失败
- 旧任务没有总结

**解决**：
1. 检查 `.env` 中的 `MM_LLM_API_KEY`
2. 查看服务日志确认 LLM 调用
3. 重新分析视频生成新记录

### 问题3：点击历史记录无反应

**原因**：JavaScript 错误

**解决**：
1. 打开浏览器开发者工具（F12）
2. 查看 Console 错误信息
3. 确认 `loadHistoryJob` 函数正常

---

## 未来扩展

- [ ] 缩略图自动生成（提取关键帧）
- [ ] 历史记录搜索和筛选
- [ ] 导出历史记录为 PDF
- [ ] 历史记录对比功能
- [ ] 收藏夹功能
- [ ] 标签和分类

---

## 总结

历史记录功能提供了完整的任务管理体验：

✅ **自动总结**：AI 生成标题和学习要点  
✅ **独立界面**：Learn 和 History 互不干扰  
✅ **快速查看**：一键加载历史分析结果  
✅ **美观易用**：卡片式布局，交互友好  

现在就开始使用吧！

