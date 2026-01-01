Local Demo Backend Spec
1. 目标交付（Agent 必须做出来）
必须跑通
1.	本地启动一个 API 服务（FastAPI）
2.	支持 learn / compare 两种 job
3.	可异步执行（不依赖 Celery/Redis）：创建 job → 轮询 job 状态 → 得到结果 JSON
4.	拆解部分实际调用多模态大模型 API（不是纯 mock）
5.	Compare 模式产出：target 拆解 + user 拆解 + mapping + step-by-step improvements
6.	虚拟运镜 preview：走子任务接口，调用图生视频 API（Demo 允许先做 1 种运镜效果，如 push-in）
允许先简化（Demo 阶段）
•	只支持 url 输入（视频链接）或本地文件路径（可选）
•	数据库存 SQLite
•	存储先用本地目录 ./data/（帧、临时文件、结果 JSON）
•	多模态大模型只做：
o	镜头边界（shot boundaries）
o	每段至少 3 个 feature（camera_motion / lighting / color_grading）
•	图生视频只做“运镜 preview”一种或两种 preset
 
2. 本地架构（不使用 Docker / 不依赖队列中间件）
2.1 进程内异步 Job（推荐实现）
•	API 进程内维护一个 JobRunner：
o	用 asyncio.create_task() 或 ThreadPoolExecutor 跑 pipeline
o	job 状态写入 SQLite（避免进程重启丢结果）
•	进度更新：阶段 stage + percent + message
注意：Demo 本地跑 OK；生产再换 Celery/队列也不影响业务逻辑，因为 pipeline & 插件是纯函数式输入输出。
 
3. 项目目录（Agent 直接照抄）
video_ai_demo/
  app/
    main.py
    api/
      routes_jobs.py
      routes_virtual_motion.py
    core/
      config.py
      errors.py
      logging.py
      json_schema.py          # 输出结构校验（强烈建议）
    db/
      session.py              # SQLite
      models.py               # jobs/assets/artifacts
      repo.py
    pipeline/
      orchestrator.py
      steps/
        ingest.py
        extract_frames.py
        mm_llm_decompose.py    # 多模态模型：镜头切分 + 每段分析
        compare_map.py
        improve_steps.py
        artifacts.py
    integrations/
      mm_llm_client.py         # 多模态大模型 API 适配层（可插拔）
      img2video_client.py      # 图生视频 API 适配层（可插拔）
    plugins/
      registry.py
      contracts.py             # 插件接口定义（Segmentation/Analyzer/Improver等）
      llm_decomposer_v1.py     # Demo: “拆解全部交给多模态模型”的实现
      improver_v1.py
      mapper_v1.py
  data/
    .gitkeep
  tests/
    test_contract.py
  requirements.txt
  README.md
 
4. 外部 API 适配层（关键：可扩展、可替换）
你说“拆解调用多模态大模型 API”“运镜改进效果走图生视频 API”，所以必须把外部服务隔离成适配层：
4.1 integrations/mm_llm_client.py（必须）
提供统一方法：
•	decompose_video(frames: List[FrameInput], prompt_config) -> DecomposeResultJSON
其中 frames 不是整段视频，而是抽帧序列（带时间戳），例如：
{
  "ts_ms": 2100,
  "image_path": "./data/jobs/job_x/frames/f_00021.jpg"
}
这样做的好处
•	任何多模态模型都能接（只要支持图片输入）
•	你可以控制成本：抽帧率可调（比如 2fps/1fps）
4.2 integrations/img2video_client.py（可选但建议做）
•	generate_virtual_motion(keyframes_or_images, motion_recipe, out_path) -> PreviewResult
 
5. Pipeline（本地 Demo 的实际执行步骤）
Learn 模式（mode=learn）
1.	ingest：下载视频到 ./data/jobs/{job_id}/input/target.mp4；ffprobe 获取 meta
2.	extract_frames：按固定 fps 抽帧（建议 1~2fps），生成 frames/*.jpg，并生成 frames_index.json
3.	mm_llm_decompose：把帧序列喂给多模态 LLM，让它输出：
o	镜头切分 segments[]（按镜头切换）
o	每个 segment 的 analysis.features[]（单特征字段）
4.	artifacts：为每段生成 keyframes（直接从抽帧里选）、可选导出 zip
5.	persist：写入 job.result_json
Compare 模式（mode=compare）
1.	target 跑 Learn 全流程 → 得到 target_result
2.	user 跑 Learn 全流程 → 得到 user_result
3.	mapper_v1：对齐 user segments 到 target segments（先简单规则：按时长/节奏/feature 相似）
4.	improver_v1：为每个 user segment 生成 step-by-step 建议（先运镜，再打光，再调色）
5.	persist
虚拟运镜 preview（子任务）
•	从 improvements 中某一步（camera_motion）拿到 motion_recipe
•	取该 segment 的 1~3 张关键帧，调用图生视频 API，生成 preview mp4
•	存储到 ./data/jobs/{job_id}/previews/{subtask_id}.mp4
 
6. 多模态 LLM 的“拆解输出”强约束（避免模型胡写）
你最在意的：每个 JSON 字段只包含一个特征，所以必须做两层约束：
6.1 输出 JSON Schema（强烈建议）
在 core/json_schema.py 定义 DecomposeResult 的 JSON Schema，并在拿到模型输出后做校验：
•	不通过 → 自动让模型“修正输出”（一次重试）或返回 job failed（带 details）
6.2 两段式提示词（建议）
•	第一段：只让模型输出 shot boundaries（segments）
•	第二段：基于 segments，再输出每段 features（单特征）
这样比“一次性让模型输出全部”稳定很多，也方便 debug 成本与质量。
 
7. API 合约（前端调用长相不变，但 demo 支持本地）
7.1 创建 Job
POST /v1/video-analysis/jobs
Learn
{
  "mode": "learn",
  "target_video": { "source": { "type": "url", "url": "https://..." } },
  "user_video": null,
  "options": {
    "frame_extract": { "fps": 2, "max_frames": 240 },
    "analysis": { "enabled_modules": ["camera_motion","lighting","color_grading"] },
    "llm": { "provider": "YOUR_MM_LLM", "model": "MODEL_NAME" }
  }
}
Compare
{
  "mode": "compare",
  "target_video": { "source": { "type": "url", "url": "https://target.mp4" } },
  "user_video": { "source": { "type": "url", "url": "https://user.mp4" } },
  "options": {
    "frame_extract": { "fps": 2, "max_frames": 240 },
    "compare": { "enabled": true, "virtual_camera_motion": { "enabled": true } },
    "llm": { "provider": "YOUR_MM_LLM", "model": "MODEL_NAME" }
  }
}
响应：
{
  "job_id": "job_xxx",
  "status": "queued",
  "status_url": "/v1/video-analysis/jobs/job_xxx"
}
7.2 查询 Job
GET /v1/video-analysis/jobs/{job_id}
•	running：progress
•	succeeded：result（包含 segments/features/improvements 等）
•	failed：error
7.3 虚拟运镜子任务
POST /v1/video-analysis/virtual-motion/jobs
请求：
{
  "parent_job_id": "job_xxx",
  "asset_role": "user",
  "segment_id": "u_s003",
  "motion_recipe": { "type": "push_in", "strength": 0.18, "duration_ms": 3000 },
  "options": {
    "provider": "YOUR_IMG2VIDEO",
    "model": "MODEL_NAME"
  }
}
响应：
{
  "subtask_id": "sub_vm_001",
  "status_url": "/v1/video-analysis/virtual-motion/jobs/sub_vm_001"
}
 
8. 本地运行方式（Agent 必须写入 README）
8.1 requirements（建议）
•	fastapi, uvicorn
•	pydantic
•	sqlalchemy
•	httpx / requests
•	python-dotenv
•	jsonschema
•	ffmpeg（系统依赖）
8.2 启动
pip install -r requirements.txt
export MM_LLM_API_KEY=...
export IMG2VIDEO_API_KEY=...
uvicorn app.main:app --reload --port 8000
 
9. 配置（.env）
Demo 用 .env：
•	MM_LLM_BASE_URL=...
•	MM_LLM_API_KEY=...
•	MM_LLM_MODEL=...
•	IMG2VIDEO_BASE_URL=...
•	IMG2VIDEO_API_KEY=...
•	IMG2VIDEO_MODEL=...
•	DATA_DIR=./data
•	SQLITE_PATH=./data/demo.db
•	FFMPEG_BIN=ffmpeg
 
10. 插件扩展点（未来可加功能不用改主流程）
10.1 Decomposer 插件（你现在要的“拆解走多模态 LLM”就是一种实现）
llm_decomposer_v1 负责产出：
•	segments（镜头切分）
•	features（运镜/打光/调色，单特征）
未来如果你换成“传统镜头检测 + LLM 做解释”，只要新增一个 decomposer 插件，不动 orchestrator。
10.2 Improver 插件
improver_v1 负责把：
•	user 当前 feature
•	target 特征经验
变成 step-by-step actions + validation
未来你要扩展“对每个特征都提供具体改进步骤”，就往 actions 里加新的 action_type，不破坏前端。
10.3 Virtual Motion Generator
图生视频 API 换供应商时，只替换 img2video_client.py。
 
11. Demo 质量保障（Agent 必须做的校验）
1.	多模态 LLM 输出 JSON 必须通过 schema 校验
2.	每个 feature 必须包含：
•	category, type, value, confidence, evidence.time_ranges_ms
3.	每个 feature 只能表达一个特征：
建议做一个简单规则检查（demo 阶段）：
•	value 不允许包含 “、/，/；/and/以及”等连接词（命中则降置信度并记录 warning 或触发重写）
4.	所有不认识的字段放 extensions，前端可忽略
 
12. Agent 实施步骤（你可以直接转发）
1.	初始化 FastAPI + SQLite（jobs/assets/artifacts 表）
2.	实现 job runner（asyncio/task + DB 持久化）
3.	实现 ffmpeg 抽帧 step（fps/max_frames 可配置）
4.	实现 mm_llm_client.decompose_video()：
o	组装 frames（带 ts_ms）
o	两段式调用：先 segments 再 features（更稳）
o	schema 校验 + 失败重试一次
5.	实现 compare：mapper_v1 + improver_v1（先简单规则）
6.	实现虚拟运镜子任务：调用 img2video API（最少 push-in）
7.	写 contract 测试：learn/compare 返回结构必备字段齐全
8.	写 README：本地安装、启动、curl 示例

