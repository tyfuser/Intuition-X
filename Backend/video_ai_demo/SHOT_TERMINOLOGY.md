# 🎬 电影分镜标准术语

## 📋 术语分类

### 1. 景别 (Shot Size)

景别是指被摄主体在画面中所占的比例大小。

| 中文名 | 英文名 | 缩写 | 描述 |
|--------|--------|------|------|
| 全景 | Extreme Wide Shot / Establishing Shot | EWS | 展示整个场景环境，人物很小或不可见 |
| 中全景 | Wide Shot | WS | 人物全身可见，周围环境清晰 |
| 中景 | Medium Shot | MS | 人物腰部以上，表情和动作都能看清 |
| 近景 | Close-Up | CU | 人物肩部以上，突出面部表情 |
| 特写 | Extreme Close-Up | ECU | 人物面部局部或物体细节 |

### 2. 拍摄角度 (Camera Angle)

拍摄角度指摄像机与被摄主体之间的垂直关系。

| 中文名 | 英文名 | 缩写 | 描述 |
|--------|--------|------|------|
| 贴地角度 | Ground Level / Worm's Eye View | GL | 摄像机贴近地面向上拍摄 |
| 仰拍角度 | Low Angle | LA | 摄像机低于视线向上拍摄，显得高大威严 |
| 俯拍角度 | High Angle | HA | 摄像机高于视线向下拍摄，显得渺小脆弱 |
| 鸟瞰镜头 | Bird's Eye View / Aerial Shot | BEV | 从正上方垂直向下拍摄 |

### 3. 运镜方式 (Camera Movement)

运镜方式指摄像机的移动方式。

| 中文名 | 英文名 | 缩写 | 描述 |
|--------|--------|------|------|
| 摇镜头 | Pan Shot | PAN | 摄像机水平左右旋转 |
| 移镜头 | Tracking Shot / Dolly Shot | TRK | 摄像机整体水平移动 |
| 推镜头 | Push In / Dolly In | PUSH | 摄像机向前推进，逐渐靠近主体 |
| 拉镜头 | Pull Out / Dolly Out | PULL | 摄像机向后拉远，逐渐远离主体 |
| 跟踪镜头 | Follow Shot | FOLLOW | 摄像机跟随移动的主体 |
| 升格镜头 | Slow Motion / High Frame Rate | SLO-MO | 高帧率拍摄后慢速播放 |
| 降格镜头 | Time Lapse / Low Frame Rate | TL | 低帧率拍摄后快速播放 |
| 固定镜头 | Static Shot | STATIC | 摄像机完全静止 |

## 🔑 术语键值对应

### JSON中的type字段使用英文key：

```json
{
  "景别": {
    "extreme_wide_shot": "全景",
    "wide_shot": "中全景",
    "medium_shot": "中景",
    "close_up": "近景",
    "extreme_close_up": "特写"
  },
  "拍摄角度": {
    "ground_level": "贴地角度",
    "low_angle": "仰拍角度",
    "high_angle": "俯拍角度",
    "birds_eye": "鸟瞰镜头"
  },
  "运镜方式": {
    "pan": "摇镜头",
    "tracking": "移镜头",
    "push_in": "推镜头",
    "pull_out": "拉镜头",
    "follow": "跟踪镜头",
    "slow_motion": "升格镜头",
    "time_lapse": "降格镜头",
    "static": "固定镜头"
  }
}
```

## 📝 使用示例

### API返回格式

```json
{
  "segments": [
    {
      "segment_id": "seg_001",
      "start_ms": 0,
      "end_ms": 3500,
      "features": [
        {
          "category": "camera_motion",
          "type": "medium_shot",
          "value": "中景 - 人物腰部以上",
          "confidence": 0.90
        },
        {
          "category": "camera_motion",
          "type": "push_in",
          "value": "推镜头 - 缓慢向前推进",
          "confidence": 0.85
        },
        {
          "category": "camera_motion",
          "type": "low_angle",
          "value": "仰拍角度 - 向上仰拍",
          "confidence": 0.82
        }
      ]
    }
  ]
}
```

### LLM分析要求

LLM在分析视频时，必须使用以上标准术语，并且对于camera_motion类别，至少识别：
1. **景别**：1个（全景/中全景/中景/近景/特写）
2. **运镜方式**：1个（摇镜头/移镜头/推镜头/拉镜头等）
3. **拍摄角度**：1个（贴地/仰拍/俯拍/鸟瞰）

## 🌐 API端点

### 获取所有术语

```bash
GET /v1/terminology/shots
```

响应：
```json
{
  "status": "success",
  "data": {
    "shot_sizes": {...},
    "camera_angles": {...},
    "camera_movements": {...}
  }
}
```

### 获取术语列表

```bash
GET /v1/terminology/shots/list
```

### 获取单个术语详情

```bash
GET /v1/terminology/shots/medium_shot
```

响应：
```json
{
  "status": "success",
  "data": {
    "name": "中景",
    "name_en": "Medium Shot",
    "abbr": "MS",
    "description": "人物腰部以上，表情和动作都能看清"
  }
}
```

### 翻译术语

```bash
GET /v1/terminology/shots/translate/push_in
```

响应：
```json
{
  "status": "success",
  "data": {
    "key": "push_in",
    "chinese_name": "推镜头"
  }
}
```

## 📚 前端集成

前端可以通过API获取所有术语，用于：
1. **下拉选择**：提供标准术语选择
2. **结果展示**：将英文key翻译为中文
3. **术语说明**：显示术语描述和示例

## 🎯 最佳实践

### 1. 景别优先级
- 先识别景别（全景→近景→特写）
- 景别决定了画面的基本框架

### 2. 运镜组合
- 可以有多个运镜方式组合
- 例如："推镜头 + 摇镜头"

### 3. 角度与景别
- 角度与景别可以同时存在
- 例如："中景 + 仰拍角度"

### 4. 置信度标准
- 0.9-1.0：非常明显
- 0.8-0.9：比较明显
- 0.7-0.8：基本可以识别
- <0.7：不确定

## 🔄 术语更新流程

1. 修改 `app/core/shot_terminology.py`
2. 更新术语字典
3. 重启服务
4. 前端调用API获取最新术语

## 📖 参考资料

- [电影镜头语言](https://en.wikipedia.org/wiki/Shot_(filmmaking))
- [摄影机运动](https://en.wikipedia.org/wiki/Camera_movement)
- [电影拍摄角度](https://en.wikipedia.org/wiki/Camera_angle)

---

**标准化术语使分析结果更专业、更统一！** 🎬✨

