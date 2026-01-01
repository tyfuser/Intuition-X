// 特征意义和可视化
// Feature Meanings and Visualizations

// ========== 景别意义 ==========
function getShotMeaning(type) {
    const meanings = {
        'extreme_wide_shot': `
            <strong>艺术效果：</strong>建立场景环境，营造宏大氛围<br>
            <strong>情感传达：</strong>渺小、孤独、壮观<br>
            <strong>常见用途：</strong>电影开场、场景转换、展示地理位置
        `,
        'wide_shot': `
            <strong>艺术效果：</strong>展示人物与环境关系，叙事功能强<br>
            <strong>情感传达：</strong>平衡、舒适、客观<br>
            <strong>常见用途：</strong>展示动作、群像场景、空间关系
        `,
        'medium_shot': `
            <strong>艺术效果：</strong>平衡人物与环境，适合对话<br>
            <strong>情感传达：</strong>亲切、自然、交流<br>
            <strong>常见用途：</strong>对话场景、日常活动、新闻访谈
        `,
        'close_up': `
            <strong>艺术效果：</strong>突出面部表情，强化情感<br>
            <strong>情感传达：</strong>亲密、紧张、强烈<br>
            <strong>常见用途：</strong>情绪特写、关键反应、戏剧高潮
        `,
        'extreme_close_up': `
            <strong>艺术效果：</strong>极致细节，营造压迫感<br>
            <strong>情感传达：</strong>紧张、焦虑、专注<br>
            <strong>常见用途：</strong>悬疑惊悚、物体细节、眼神特写
        `
    };
    return meanings[type] || '';
}

// ========== 运镜方式意义 ==========
function getMovementMeaning(type) {
    const meanings = {
        'push_in': `
            <strong>艺术效果：</strong>引导观众注意力，增强代入感<br>
            <strong>情感传达：</strong>紧张升级、聚焦重点<br>
            <strong>叙事作用：</strong>强调细节、进入内心世界
        `,
        'pull_out': `
            <strong>艺术效果：</strong>揭示更大场景，扩展视野<br>
            <strong>情感传达：</strong>释放、疏离、全局观<br>
            <strong>叙事作用：</strong>场景转换、揭示真相
        `,
        'pan': `
            <strong>艺术效果：</strong>水平扫视，连接不同主体<br>
            <strong>情感传达：</strong>观察、跟随、寻找<br>
            <strong>叙事作用：</strong>展示空间关系、跟随对话
        `,
        'tracking': `
            <strong>艺术效果：</strong>跟随移动，动感流畅<br>
            <strong>情感传达：</strong>参与、陪伴、追逐<br>
            <strong>叙事作用：</strong>强化动作、营造节奏
        `,
        'follow': `
            <strong>艺术效果：</strong>主观视角，身临其境<br>
            <strong>情感传达：</strong>紧密跟随、代入感强<br>
            <strong>叙事作用：</strong>展现角色视角、追踪动作
        `,
        'static': `
            <strong>艺术效果：</strong>稳定客观，聚焦内容<br>
            <strong>情感传达：</strong>平静、观察、冷静<br>
            <strong>叙事作用：</strong>对话场景、静态展示
        `,
        'slow_motion': `
            <strong>艺术效果：</strong>时间延展，细节展现<br>
            <strong>情感传达：</strong>浪漫、梦幻、悲壮<br>
            <strong>叙事作用：</strong>强调瞬间、营造诗意
        `,
        'time_lapse': `
            <strong>艺术效果：</strong>时间压缩，过程展示<br>
            <strong>情感传达：</strong>流逝、变化、规律<br>
            <strong>叙事作用：</strong>时间推进、变化展示
        `
    };
    return meanings[type] || '';
}

// ========== 拍摄角度意义 ==========
function getAngleMeaning(type) {
    const meanings = {
        'ground_level': `
            <strong>艺术效果：</strong>从地面仰视，夸张高度<br>
            <strong>情感传达：</strong>威压、震撼、渺小<br>
            <strong>叙事作用：</strong>强化力量对比、营造紧张感
        `,
        'low_angle': `
            <strong>艺术效果：</strong>仰拍主体，显得高大<br>
            <strong>情感传达：</strong>威严、力量、优越<br>
            <strong>叙事作用：</strong>塑造强者形象、建立权威
        `,
        'high_angle': `
            <strong>艺术效果：</strong>俯拍主体，显得渺小<br>
            <strong>情感传达：</strong>脆弱、无助、卑微<br>
            <strong>叙事作用：</strong>弱化角色、营造同情
        `,
        'birds_eye': `
            <strong>艺术效果：</strong>上帝视角，全局视野<br>
            <strong>情感传达：</strong>客观、冷静、命运感<br>
            <strong>叙事作用：</strong>场景概览、空间关系
        `
    };
    return meanings[type] || '';
}

// ========== 景别可视化 ==========
function getShotVisual(type) {
    const visuals = {
        'extreme_wide_shot': `
            <div class="shot-visual" style="text-align: center; margin-top: 12px;">
                <div style="font-size: 11px; color: #888; margin-bottom: 8px;">视野范围示意</div>
                <div style="border: 2px solid #666; padding: 20px; border-radius: 8px; background: linear-gradient(180deg, #1a1a1a 0%, #2a2a2a 100%);">
                    <div style="font-size: 10px;">🏔️ 环境 🏔️</div>
                    <div style="margin-top: 8px; font-size: 8px; opacity: 0.6;">人物</div>
                </div>
            </div>
        `,
        'wide_shot': `
            <div class="shot-visual" style="text-align: center; margin-top: 12px;">
                <div style="font-size: 11px; color: #888; margin-bottom: 8px;">视野范围示意</div>
                <div style="border: 2px solid #666; padding: 16px; border-radius: 8px; background: linear-gradient(180deg, #1a1a1a 0%, #2a2a2a 100%);">
                    <div style="font-size: 10px;">🌳 环境 🌳</div>
                    <div style="margin-top: 6px; font-size: 12px;">🧍 人物全身</div>
                </div>
            </div>
        `,
        'medium_shot': `
            <div class="shot-visual" style="text-align: center; margin-top: 12px;">
                <div style="font-size: 11px; color: #888; margin-bottom: 8px;">视野范围示意</div>
                <div style="border: 2px solid #666; padding: 12px; border-radius: 8px; background: linear-gradient(180deg, #1a1a1a 0%, #2a2a2a 100%);">
                    <div style="font-size: 14px; line-height: 1.6;">
                        👤<br>腰部以上
                    </div>
                </div>
            </div>
        `,
        'close_up': `
            <div class="shot-visual" style="text-align: center; margin-top: 12px;">
                <div style="font-size: 11px; color: #888; margin-bottom: 8px;">视野范围示意</div>
                <div style="border: 2px solid #666; padding: 10px; border-radius: 8px; background: linear-gradient(180deg, #1a1a1a 0%, #2a2a2a 100%);">
                    <div style="font-size: 20px;">😊</div>
                    <div style="font-size: 10px; margin-top: 4px;">肩部以上</div>
                </div>
            </div>
        `,
        'extreme_close_up': `
            <div class="shot-visual" style="text-align: center; margin-top: 12px;">
                <div style="font-size: 11px; color: #888; margin-bottom: 8px;">视野范围示意</div>
                <div style="border: 2px solid #666; padding: 8px; border-radius: 8px; background: linear-gradient(180deg, #1a1a1a 0%, #2a2a2a 100%);">
                    <div style="font-size: 24px;">👁️</div>
                    <div style="font-size: 10px; margin-top: 2px;">局部特写</div>
                </div>
            </div>
        `
    };
    return visuals[type] || '';
}

// ========== 光线意义 ==========
function getLightingMeaning(type) {
    const meanings = {
        'natural': `
            <strong>艺术效果：</strong>真实自然，柔和舒适<br>
            <strong>情感传达：</strong>真实、温暖、生活化<br>
            <strong>适用场景：</strong>日常生活、现实题材、温馨场景
        `,
        'three_point': `
            <strong>艺术效果：</strong>经典布光，层次丰富<br>
            <strong>情感传达：</strong>专业、立体、清晰<br>
            <strong>适用场景：</strong>访谈、人物特写、正式拍摄
        `,
        'low_key': `
            <strong>艺术效果：</strong>高对比度，戏剧性强<br>
            <strong>情感传达：</strong>神秘、紧张、悬疑<br>
            <strong>适用场景：</strong>黑色电影、惊悚片、艺术摄影
        `,
        'high_key': `
            <strong>艺术效果：</strong>明亮柔和，阴影少<br>
            <strong>情感传达：</strong>欢快、轻松、纯净<br>
            <strong>适用场景：</strong>喜剧、广告、梦幻场景
        `
    };
    return meanings[type] || `
        <strong>艺术效果：</strong>独特的光线处理<br>
        <strong>情感传达：</strong>根据具体效果而定<br>
        <strong>适用场景：</strong>特定主题表达
    `;
}

// ========== 光路图 ==========
function getLightingDiagram(type) {
    const diagrams = {
        'three_point': `
            <div class="lighting-diagram-container" style="margin-top: 12px; padding: 16px; background: #1a1a1a; border-radius: 8px;">
                <div style="text-align: center; font-size: 11px; color: #888; margin-bottom: 12px;">三点布光示意图</div>
                <div style="position: relative; height: 120px;">
                    <div style="position: absolute; top: 10px; left: 20%; width: 40px; height: 40px; background: radial-gradient(circle, #ffeb3b 0%, transparent 70%); border-radius: 50%;"></div>
                    <div style="position: absolute; top: 10px; left: 20%; font-size: 10px; margin-top: 45px;">💡 主光</div>
                    
                    <div style="position: absolute; top: 10px; right: 20%; width: 30px; height: 30px; background: radial-gradient(circle, #90caf9 0%, transparent 70%); border-radius: 50%;"></div>
                    <div style="position: absolute; top: 10px; right: 20%; font-size: 10px; margin-top: 35px;">💡 补光</div>
                    
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 24px;">👤</div>
                    
                    <div style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); width: 30px; height: 30px; background: radial-gradient(circle, #fff 0%, transparent 70%); border-radius: 50%;"></div>
                    <div style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); font-size: 10px; margin-top: 35px;">💡 轮廓光</div>
                </div>
            </div>
        `,
        'natural': `
            <div class="lighting-diagram-container" style="margin-top: 12px; padding: 16px; background: #1a1a1a; border-radius: 8px;">
                <div style="text-align: center; font-size: 11px; color: #888; margin-bottom: 12px;">自然光示意图</div>
                <div style="position: relative; height: 100px; text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 8px;">☀️</div>
                    <div style="font-size: 10px; color: #888;">自然光源</div>
                    <div style="margin-top: 12px; font-size: 20px;">👤</div>
                    <div style="margin-top: 8px; font-size: 10px; opacity: 0.6;">柔和漫射</div>
                </div>
            </div>
        `,
        'low_key': `
            <div class="lighting-diagram-container" style="margin-top: 12px; padding: 16px; background: #000; border-radius: 8px;">
                <div style="text-align: center; font-size: 11px; color: #888; margin-bottom: 12px;">低调光示意图</div>
                <div style="position: relative; height: 100px;">
                    <div style="position: absolute; top: 20px; left: 30%; width: 50px; height: 50px; background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, transparent 60%); border-radius: 50%;"></div>
                    <div style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size: 24px; text-shadow: 2px 2px 8px rgba(255,255,255,0.3);">👤</div>
                    <div style="position: absolute; bottom: 20px; right: 30%; width: 80px; height: 80px; background: radial-gradient(circle, rgba(0,0,0,0.95) 0%, transparent 60%); border-radius: 50%;"></div>
                    <div style="position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); font-size: 10px; color: #666;">高对比度</div>
                </div>
            </div>
        `,
        'high_key': `
            <div class="lighting-diagram-container" style="margin-top: 12px; padding: 16px; background: #f0f0f0; border-radius: 8px; color: #333;">
                <div style="text-align: center; font-size: 11px; color: #666; margin-bottom: 12px;">高调光示意图</div>
                <div style="position: relative; height: 100px;">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at 50% 20%, rgba(255,255,255,1) 0%, rgba(255,255,255,0.3) 70%);"></div>
                    <div style="position: relative; text-align: center; padding-top: 30px;">
                        <div style="font-size: 24px;">👤</div>
                        <div style="margin-top: 8px; font-size: 10px; color: #666;">明亮柔和</div>
                    </div>
                </div>
            </div>
        `
    };
    return diagrams[type] || `
        <div style="margin-top: 12px; padding: 16px; background: #1a1a1a; border-radius: 8px; text-align: center;">
            <div style="font-size: 11px; color: #888;">光线效果</div>
            <div style="margin-top: 8px; font-size: 20px;">💡</div>
        </div>
    `;
}

// ========== 调色意义 ==========
function getColorMeaning(type) {
    const meanings = {
        'warm_tone': `
            <strong>色彩心理：</strong>温暖、热情、亲切<br>
            <strong>情感传达：</strong>幸福、怀旧、温馨<br>
            <strong>常见用途：</strong>日落场景、温馨回忆、浪漫氛围
        `,
        'cool_tone': `
            <strong>色彩心理：</strong>冷静、理性、科技<br>
            <strong>情感传达：</strong>冷漠、孤独、神秘<br>
            <strong>常见用途：</strong>科幻片、悬疑片、冬季场景
        `,
        'desaturated': `
            <strong>色彩心理：</strong>平淡、压抑、真实<br>
            <strong>情感传达：</strong>沉重、回忆、纪实<br>
            <strong>常见用途：</strong>战争片、纪录片、现实主义
        `,
        'high_contrast': `
            <strong>色彩心理：</strong>强烈、冲击、戏剧<br>
            <strong>情感传达：</strong>紧张、激烈、鲜明<br>
            <strong>常见用途：</strong>动作片、时尚片、艺术片
        `
    };
    return meanings[type] || `
        <strong>色彩心理：</strong>独特的视觉风格<br>
        <strong>情感传达：</strong>根据具体调色而定<br>
        <strong>常见用途：</strong>特定主题表达
    `;
}

// ========== 调色参数 ==========
function getColorParameters(type) {
    const params = {
        'warm_tone': {
            color_temp: '3200K - 4000K',
            tint: '+10 ~ +20',
            saturation: '+5 ~ +15',
            highlights: '-5 ~ +5',
            shadows: '+10 ~ +20'
        },
        'cool_tone': {
            color_temp: '6500K - 8000K',
            tint: '-10 ~ -20',
            saturation: '-5 ~ +5',
            highlights: '+5 ~ +15',
            shadows: '-10 ~ -5'
        },
        'desaturated': {
            color_temp: '5000K - 5500K',
            tint: '0',
            saturation: '-20 ~ -40',
            highlights: '0 ~ -10',
            shadows: '+5 ~ +10'
        },
        'high_contrast': {
            color_temp: '4500K - 6000K',
            tint: '±5',
            saturation: '+10 ~ +25',
            highlights: '+15 ~ +25',
            shadows: '-15 ~ -25'
        }
    };
    
    const param = params[type] || {
        color_temp: '5500K',
        tint: '0',
        saturation: '0',
        highlights: '0',
        shadows: '0'
    };
    
    return `
        <div class="color-params-container" style="margin-top: 12px; padding: 12px; background: #1a1a1a; border-radius: 8px;">
            <div style="font-size: 11px; color: #888; margin-bottom: 12px;">调色参数</div>
            <div class="param-row" style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 12px; color: #ccc;">色温</span>
                <span style="font-size: 12px; font-weight: 600; color: #ff9800;">${param.color_temp}</span>
            </div>
            <div class="param-row" style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 12px; color: #ccc;">色调</span>
                <span style="font-size: 12px; font-weight: 600; color: #2196f3;">${param.tint}</span>
            </div>
            <div class="param-row" style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 12px; color: #ccc;">饱和度</span>
                <span style="font-size: 12px; font-weight: 600; color: #4caf50;">${param.saturation}</span>
            </div>
            <div class="param-row" style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-size: 12px; color: #ccc;">高光</span>
                <span style="font-size: 12px; font-weight: 600; color: #ffeb3b;">${param.highlights}</span>
            </div>
            <div class="param-row" style="display: flex; justify-content: space-between;">
                <span style="font-size: 12px; color: #ccc;">阴影</span>
                <span style="font-size: 12px; font-weight: 600; color: #9c27b0;">${param.shadows}</span>
            </div>
        </div>
    `;
}

