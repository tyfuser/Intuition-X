"""
电影分镜标准术语
Cinema Shot Terminology Standards
"""

# 景别分类 (Shot Size)
SHOT_SIZES = {
    "extreme_wide_shot": {
        "name": "全景",
        "name_en": "Extreme Wide Shot / Establishing Shot",
        "abbr": "EWS",
        "description": "展示整个场景环境，人物很小或不可见"
    },
    "wide_shot": {
        "name": "中全景",
        "name_en": "Wide Shot",
        "abbr": "WS",
        "description": "人物全身可见，周围环境清晰"
    },
    "medium_shot": {
        "name": "中景",
        "name_en": "Medium Shot",
        "abbr": "MS",
        "description": "人物腰部以上，表情和动作都能看清"
    },
    "close_up": {
        "name": "近景",
        "name_en": "Close-Up",
        "abbr": "CU",
        "description": "人物肩部以上，突出面部表情"
    },
    "extreme_close_up": {
        "name": "特写",
        "name_en": "Extreme Close-Up",
        "abbr": "ECU",
        "description": "人物面部局部或物体细节"
    }
}

# 拍摄角度 (Camera Angle)
CAMERA_ANGLES = {
    "ground_level": {
        "name": "贴地角度",
        "name_en": "Ground Level / Worm's Eye View",
        "abbr": "GL",
        "description": "摄像机贴近地面向上拍摄"
    },
    "low_angle": {
        "name": "仰拍角度",
        "name_en": "Low Angle",
        "abbr": "LA",
        "description": "摄像机低于视线向上拍摄，显得高大威严"
    },
    "high_angle": {
        "name": "俯拍角度",
        "name_en": "High Angle",
        "abbr": "HA",
        "description": "摄像机高于视线向下拍摄，显得渺小脆弱"
    },
    "birds_eye": {
        "name": "鸟瞰镜头",
        "name_en": "Bird's Eye View / Aerial Shot",
        "abbr": "BEV",
        "description": "从正上方垂直向下拍摄"
    }
}

# 运镜方式 (Camera Movement)
CAMERA_MOVEMENTS = {
    "pan": {
        "name": "摇镜头",
        "name_en": "Pan Shot",
        "abbr": "PAN",
        "description": "摄像机水平左右旋转"
    },
    "tracking": {
        "name": "移镜头",
        "name_en": "Tracking Shot / Dolly Shot",
        "abbr": "TRK",
        "description": "摄像机整体水平移动"
    },
    "push_in": {
        "name": "推镜头",
        "name_en": "Push In / Dolly In",
        "abbr": "PUSH",
        "description": "摄像机向前推进，逐渐靠近主体"
    },
    "pull_out": {
        "name": "拉镜头",
        "name_en": "Pull Out / Dolly Out",
        "abbr": "PULL",
        "description": "摄像机向后拉远，逐渐远离主体"
    },
    "follow": {
        "name": "跟踪镜头",
        "name_en": "Follow Shot",
        "abbr": "FOLLOW",
        "description": "摄像机跟随移动的主体"
    },
    "slow_motion": {
        "name": "升格镜头",
        "name_en": "Slow Motion / High Frame Rate",
        "abbr": "SLO-MO",
        "description": "高帧率拍摄后慢速播放"
    },
    "time_lapse": {
        "name": "降格镜头",
        "name_en": "Time Lapse / Low Frame Rate",
        "abbr": "TL",
        "description": "低帧率拍摄后快速播放"
    },
    "static": {
        "name": "固定镜头",
        "name_en": "Static Shot",
        "abbr": "STATIC",
        "description": "摄像机完全静止"
    }
}

# 组合术语
ALL_SHOT_TYPES = {
    **SHOT_SIZES,
    **CAMERA_ANGLES,
    **CAMERA_MOVEMENTS
}

# 用于LLM提示词的格式化输出
def get_shot_terminology_prompt():
    """生成用于LLM的标准术语提示"""
    
    prompt = """请使用以下标准电影术语：

**景别分类 (Shot Size)**：
"""
    for key, info in SHOT_SIZES.items():
        prompt += f"- {info['name']} ({info['name_en']}): {info['description']}\n"
    
    prompt += """
**拍摄角度 (Camera Angle)**：
"""
    for key, info in CAMERA_ANGLES.items():
        prompt += f"- {info['name']} ({info['name_en']}): {info['description']}\n"
    
    prompt += """
**运镜方式 (Camera Movement)**：
"""
    for key, info in CAMERA_MOVEMENTS.items():
        prompt += f"- {info['name']} ({info['name_en']}): {info['description']}\n"
    
    return prompt


def get_shot_types_list():
    """获取所有镜头类型列表（用于验证）"""
    return {
        "shot_sizes": list(SHOT_SIZES.keys()),
        "camera_angles": list(CAMERA_ANGLES.keys()),
        "camera_movements": list(CAMERA_MOVEMENTS.keys())
    }


def get_chinese_name(key: str) -> str:
    """根据英文key获取中文名称"""
    return ALL_SHOT_TYPES.get(key, {}).get("name", key)


def validate_shot_type(shot_type: str, category: str = None) -> bool:
    """验证镜头类型是否有效"""
    if category:
        if category == "shot_size":
            return shot_type in SHOT_SIZES
        elif category == "camera_angle":
            return shot_type in CAMERA_ANGLES
        elif category == "camera_movement":
            return shot_type in CAMERA_MOVEMENTS
    return shot_type in ALL_SHOT_TYPES


# 导出给前端使用的JSON格式
SHOT_TERMINOLOGY_JSON = {
    "shot_sizes": SHOT_SIZES,
    "camera_angles": CAMERA_ANGLES,
    "camera_movements": CAMERA_MOVEMENTS
}


if __name__ == "__main__":
    # 测试输出
    print(get_shot_terminology_prompt())
    print("\n" + "="*60)
    print("\n所有术语列表:")
    print(get_shot_types_list())

