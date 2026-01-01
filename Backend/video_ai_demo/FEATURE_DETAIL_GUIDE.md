# 特征详细描述功能指南

## 功能概述

系统现在支持**两层特征展示**架构：

1. **简洁视图**：时间轴上的特征通道只显示简单特征名称（如"缓慢推镜"、"三点布光"）
2. **详细视图**：点击片段后，右侧详情面板显示完整的专业解读

## 数据结构

### Feature 数据模型

每个特征现在包含一个可选的 `detailed_description` 字段：

```json
{
  "category": "camera_motion",
  "type": "push_in",
  "value": "缓慢推镜",
  "confidence": 0.85,
  "evidence": {
    "time_ranges_ms": [[0, 3500]]
  },
  "detailed_description": {
    "summary": "摄像机以缓慢的速度向拍摄主体推进，焦距逐渐拉近",
    "technical_terms": ["推镜头", "Dolly In", "景深变化"],
    "purpose": "引导观众注意力聚焦到主体，营造逐渐接近、深入的感觉，增强情感张力",
    "parameters": {
      "speed": "缓慢",
      "distance": "中距离推进",
      "focal_length_change": "无明显变化"
    }
  }
}
```

## 详细描述字段说明

### 1. 运镜特征 (camera_motion)

- **summary**: 运镜方式的简要描述
- **technical_terms**: 相关专业术语（中英文）
- **purpose**: 镜头意义和艺术效果
- **parameters**: 技术参数
  - `speed`: 运动速度
  - `distance`: 运动距离
  - `focal_length_change`: 焦距变化
  - 等

**示例：**

```json
{
  "category": "camera_motion",
  "type": "tracking",
  "value": "跟随镜头",
  "confidence": 0.88,
  "detailed_description": {
    "summary": "摄像机跟随移动主体进行同步运动，保持主体在画面中的相对位置",
    "technical_terms": ["跟镜", "Tracking Shot", "运动摄影"],
    "purpose": "营造动态感，让观众与主体共同行进，增强沉浸感和代入感",
    "parameters": {
      "speed": "中等速度",
      "smoothness": "稳定器辅助",
      "subject_position": "画面中心"
    }
  }
}
```

### 2. 光线特征 (lighting)

- **summary**: 光线布局的简要描述
- **technical_terms**: 相关专业术语
- **purpose**: 光线效果和氛围营造
- **parameters**: 光源配置
  - `key_light_position`: 主光位置
  - `fill_light_ratio`: 补光比例
  - `back_light_position`: 轮廓光位置
  - 等
- **diagram**: 光路图示意（使用 emoji 或文字）

**示例：**

```json
{
  "category": "lighting",
  "type": "three_point",
  "value": "三点布光",
  "confidence": 0.90,
  "detailed_description": {
    "summary": "经典的三点布光系统，包含主光、补光和轮廓光",
    "technical_terms": ["Key Light主光", "Fill Light补光", "Back Light轮廓光"],
    "purpose": "塑造人物立体感，突出轮廓，营造专业的影像质感",
    "parameters": {
      "key_light_position": "左前方45度，高于眼平",
      "fill_light_ratio": "1:2（主光与补光比例）",
      "back_light_position": "后上方，勾勒轮廓"
    },
    "diagram": "主光源↗️（左前上） + 补光源➡️（右前方） + 轮廓光⬇️（后上方）"
  }
}
```

### 3. 调色特征 (color_grading)

- **summary**: 调色风格的简要描述
- **technical_terms**: 相关专业术语
- **purpose**: 整体氛围和情感表达
- **parameters**: 调色参数
  - `color_temperature`: 色温
  - `saturation`: 饱和度
  - `contrast`: 对比度
  - `shadow_tint`: 阴影偏移
  - `highlight_tint`: 高光偏移
  - 等

**示例：**

```json
{
  "category": "color_grading",
  "type": "cinematic_teal_orange",
  "value": "电影感橙蓝调",
  "confidence": 0.85,
  "detailed_description": {
    "summary": "经典的橙蓝互补色调色方案，人物肤色呈暖橙色，背景和阴影偏向冷蓝色",
    "technical_terms": ["Orange & Teal", "互补色调色", "好莱坞风格"],
    "purpose": "营造强烈的视觉冲击和电影感，通过冷暖对比突出主体，增强画面层次",
    "parameters": {
      "color_temperature": "分离色温（肤色5800K，背景7000K）",
      "saturation": "中高饱和度（65%）",
      "contrast": "高对比度",
      "shadow_tint": "青蓝色偏移（+15 Cyan）",
      "highlight_tint": "橙黄色偏移（+10 Orange）"
    }
  }
}
```

## 前端展示

### 时间轴视图（简洁）

时间轴上的特征块只显示 `value` 字段的简洁名称：

- 运镜：缓慢推镜
- 光线：三点布光
- 调色：暖色调

### 详情面板（详细）

点击片段后，右侧详情面板展示完整信息：

#### 运镜分析 📹
- **特征名称**：缓慢推镜
- **置信度**：85%
- **简要描述**：摄像机以缓慢的速度向拍摄主体推进...
- **专业术语**：推镜头 | Dolly In | 景深变化
- **镜头意义**：引导观众注意力聚焦到主体，营造逐渐接近...
- **技术参数**：
  - speed: 缓慢
  - distance: 中距离推进

#### 光线分析 💡
- **特征名称**：三点布光
- **置信度**：90%
- **简要描述**：经典的三点布光系统...
- **专业术语**：Key Light主光 | Fill Light补光 | Back Light轮廓光
- **光路图**：主光源↗️（左前上） + 补光源➡️（右前方） + 轮廓光⬇️（后上方）
- **光线效果**：塑造人物立体感，突出轮廓...
- **光源配置**：
  - key_light_position: 左前方45度
  - fill_light_ratio: 1:2

#### 调色分析 🎨
- **特征名称**：暖色调
- **置信度**：80%
- **简要描述**：整体画面偏向暖色系...
- **专业术语**：暖色温 | 黄金时段色调
- **整体氛围**：营造温暖、舒适、怀旧或浪漫的氛围...
- **调色参数**：
  - color_temperature: 5500K-6500K
  - saturation: 60-70%
  - contrast: 柔和对比

## 使用示例

### 启动分析

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
      "llm": {
        "enabled_modules": ["camera_motion", "lighting", "color_grading"]
      }
    }
  }'
```

### 返回结果示例

```json
{
  "job_id": "job_abc123",
  "status": "succeeded",
  "result": {
    "target": {
      "segments": [
        {
          "segment_id": "seg_001",
          "start_ms": 0,
          "end_ms": 3500,
          "features": [
            {
              "category": "camera_motion",
              "type": "push_in",
              "value": "缓慢推镜",
              "confidence": 0.85,
              "detailed_description": {
                "summary": "摄像机以缓慢的速度向拍摄主体推进，焦距逐渐拉近",
                "technical_terms": ["推镜头", "Dolly In", "景深变化"],
                "purpose": "引导观众注意力聚焦到主体，营造逐渐接近、深入的感觉，增强情感张力",
                "parameters": {
                  "speed": "缓慢",
                  "distance": "中距离推进"
                }
              }
            }
          ]
        }
      ]
    }
  }
}
```

## 配置 API Key

确保配置了多模态 LLM 的 API Key：

```bash
# 编辑 .env 文件
MM_LLM_API_KEY=你的API密钥
MM_LLM_BASE_URL=https://www.sophnet.com/api/open-apis/v1
MM_LLM_MODEL=Qwen2.5-VL-7B-Instruct
```

## 兼容性说明

- `detailed_description` 字段是**可选的**
- 旧的数据不需要迁移，系统会自动降级到简单展示
- 前端会优先使用详细描述，如果不存在则回退到 `feature-meanings.js` 中的预定义描述

## 最佳实践

1. **提示词优化**：根据实际需求调整 LLM prompt，让模型输出更符合你的专业领域的描述
2. **参数定制**：在 `parameters` 中添加对你的工作流有用的具体参数
3. **光路图创意**：使用 emoji 或 ASCII 艺术创建直观的光路图示意
4. **术语标准化**：建立统一的专业术语词汇表，确保输出一致性

## 未来扩展

- [ ] 支持图片光路图（上传或生成）
- [ ] 支持视频片段预览
- [ ] 支持自定义特征类别
- [ ] 支持导出为 PDF 报告
- [ ] 支持多语言切换

## 问题反馈

如有问题，请在项目中提交 Issue。

