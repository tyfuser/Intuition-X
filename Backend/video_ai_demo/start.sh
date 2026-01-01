#!/bin/bash

# 启动脚本

echo "==================================="
echo "Video AI Demo Backend"
echo "==================================="
echo ""

# 检查.env文件
if [ ! -f .env ]; then
    echo "警告: .env 文件不存在，正在从 .env.example 复制..."
    cp .env.example .env
    echo "请编辑 .env 文件，填入你的API密钥"
    echo ""
fi

# 检查依赖
echo "检查依赖..."
python -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "依赖未安装，正在安装..."
    pip install -r requirements.txt
fi

# 检查ffmpeg
which ffmpeg >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "错误: 未找到 ffmpeg，请先安装："
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu: sudo apt install ffmpeg"
    exit 1
fi

# 创建数据目录
mkdir -p data

echo ""
echo "启动服务..."
echo "访问 http://localhost:8000 查看服务"
echo "访问 http://localhost:8000/docs 查看API文档"
echo ""

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

