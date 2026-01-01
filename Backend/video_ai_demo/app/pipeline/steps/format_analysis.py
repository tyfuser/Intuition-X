"""格式化分析结果 - 生成前端所需的完整报告"""
from typing import List, Dict, Any
from ...integrations.mm_llm_client import MMHLLMClient
from ...core.logging import logger


async def generate_formatted_analysis(segments: List[Dict[str, Any]], job_id: str) -> Dict[str, Any]:
    """
    使用LLM生成视频分析报告（前端格式）
    
    Args:
        segments: 视频片段数据（包含features）
        job_id: 任务ID
    
    Returns:
        格式化的分析数据，包含:
        - viralFactors: 爆款因素列表
        - narrativeStructure: 叙事结构
        - hookScore: 钩子分数
        - coreStrengths: 核心优势
        - reusablePoints: 可复用点
        - visualHook: 视觉钩子
        - editingPacing: 剪辑节奏
        - colorPalette: 调色风格
        - audienceSentiment: 受众情绪
        - keyTriggers: 关键触发点
    """
    llm_client = MMHLLMClient()
    
    # 准备prompt
    segments_summary = []
    for i, seg in enumerate(segments[:10], 1):  # 最多分析前10个片段
        features_text = []
        for f in seg.get("features", []):
            features_text.append(f"{f.get('category')}: {f.get('type')} - {f.get('value')}")
        
        segments_summary.append(f"""
片段{i} ({seg.get('start_ms', 0)/1000:.1f}s - {seg.get('end_ms', 0)/1000:.1f}s):
- 时长: {seg.get('duration_ms', 0)/1000:.1f}秒
- 特征: {', '.join(features_text) if features_text else '无'}
""")
    
    prompt = f"""你是一位专业的短视频分析师。请基于以下视频片段数据，生成一份详细的视频分析报告。

视频信息:
- 总片段数: {len(segments)}
- 总时长: {segments[-1].get('end_ms', 0)/1000:.1f}秒

片段详情:
{''.join(segments_summary)}

请以JSON格式返回分析结果，包含以下字段:

{{
  "viralFactors": [
    {{"category": "分类名", "description": "描述（50字内）", "intensity": 1-10}}
  ],
  "narrativeStructure": "叙事结构分析（30字内）",
  "hookScore": 0-100,
  "coreStrengths": ["优势1", "优势2", "优势3"],
  "reusablePoints": ["可复用点1", "可复用点2", "可复用点3"],
  "visualHook": "视觉钩子描述（30字内）",
  "editingPacing": "节奏描述（20字内）",
  "colorPalette": "调色风格（15字内）",
  "audienceSentiment": "受众情绪（10字内）",
  "keyTriggers": ["触发点1", "触发点2"]
}}

要求:
1. viralFactors提取5-8个关键因素，按重要性排序
2. hookScore基于节奏、多样性、专业度综合评分
3. 所有描述简洁专业，符合字数限制
4. 只返回JSON，不要其他说明文字"""

    try:
        # 调用LLM API
        logger.info(f"开始为Job {job_id} 生成格式化分析报告")
        messages = [{"role": "user", "content": prompt}]
        response_text = await llm_client._call_api(messages, image_urls=[])
        
        # 解析JSON响应
        llm_result = llm_client._extract_json_from_text(response_text)
        
        if llm_result:
            logger.info(f"Job {job_id} 格式化分析报告生成成功")
            return llm_result
        else:
            raise ValueError("无法从LLM响应中提取JSON")
    
    except Exception as e:
        logger.error(f"Job {job_id} LLM分析失败: {str(e)}")
        # 返回基础分析（降级方案）
        return _generate_fallback_analysis(segments)


def _generate_fallback_analysis(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成降级分析报告（当LLM调用失败时）
    
    基于segments的features进行简单分析
    """
    # 统计特征
    feature_count = {}
    for seg in segments:
        for f in seg.get("features", []):
            category = f.get("category", "other")
            feature_count[category] = feature_count.get(category, 0) + 1
    
    # 生成爆款因素
    viral_factors = []
    if feature_count.get("camera_motion", 0) > 2:
        viral_factors.append({
            "category": "运镜技巧",
            "description": f"运用了多种运镜方式，共{feature_count['camera_motion']}个镜头",
            "intensity": min(10, feature_count['camera_motion'])
        })
    
    if feature_count.get("lighting", 0) > 2:
        viral_factors.append({
            "category": "光影效果",
            "description": f"丰富的光影变化，共{feature_count['lighting']}处",
            "intensity": min(10, feature_count['lighting'])
        })
    
    if feature_count.get("color_grading", 0) > 2:
        viral_factors.append({
            "category": "调色风格",
            "description": f"专业的调色处理，共{feature_count['color_grading']}处",
            "intensity": min(10, feature_count['color_grading'])
        })
    
    # 如果没有足够的特征，添加基础因素
    if len(viral_factors) < 3:
        viral_factors.append({
            "category": "内容呈现",
            "description": "清晰的内容展示",
            "intensity": 6
        })
    
    return {
        "viralFactors": viral_factors,
        "narrativeStructure": f"共{len(segments)}个场景片段，结构清晰",
        "hookScore": min(100, max(50, len(viral_factors) * 15)),
        "coreStrengths": ["镜头流畅", "画面清晰", "内容完整"],
        "reusablePoints": ["镜头语言", "节奏把控"],
        "visualHook": "画面呈现自然",
        "editingPacing": "节奏平稳",
        "colorPalette": "自然色调",
        "audienceSentiment": "平稳观看",
        "keyTriggers": ["视觉内容"]
    }

