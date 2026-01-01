# 🎬 分镜术语 - 快速参考

## 景别 (Shot Size)

| 术语 | 英文Key | 说明 |
|------|---------|------|
| 全景 | `extreme_wide_shot` | 展示整个场景，人物很小 |
| 中全景 | `wide_shot` | 人物全身，环境清晰 |
| 中景 | `medium_shot` | 人物腰部以上 |
| 近景 | `close_up` | 人物肩部以上 |
| 特写 | `extreme_close_up` | 面部局部或物体细节 |

## 拍摄角度 (Camera Angle)

| 术语 | 英文Key | 说明 |
|------|---------|------|
| 贴地角度 | `ground_level` | 贴近地面向上拍 |
| 仰拍角度 | `low_angle` | 低于视线向上拍 |
| 俯拍角度 | `high_angle` | 高于视线向下拍 |
| 鸟瞰镜头 | `birds_eye` | 正上方垂直向下 |

## 运镜方式 (Camera Movement)

| 术语 | 英文Key | 说明 |
|------|---------|------|
| 摇镜头 | `pan` | 水平左右旋转 |
| 移镜头 | `tracking` | 整体水平移动 |
| 推镜头 | `push_in` | 向前推进靠近 |
| 拉镜头 | `pull_out` | 向后拉远离开 |
| 跟踪镜头 | `follow` | 跟随移动主体 |
| 升格镜头 | `slow_motion` | 慢动作播放 |
| 降格镜头 | `time_lapse` | 快速播放 |
| 固定镜头 | `static` | 摄像机静止 |

## 使用方法

### API调用

```bash
# 获取所有术语
curl http://localhost:8000/v1/terminology/shots

# 获取单个术语
curl http://localhost:8000/v1/terminology/shots/push_in

# 翻译术语
curl http://localhost:8000/v1/terminology/shots/translate/medium_shot
```

### JSON格式

```json
{
  "category": "camera_motion",
  "type": "push_in",
  "value": "推镜头 - 缓慢向前推进",
  "confidence": 0.85
}
```

---

**标准术语，专业分析！** 🎬

