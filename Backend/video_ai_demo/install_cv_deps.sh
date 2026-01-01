#!/bin/bash

# CV场景检测依赖安装脚本

echo "🎬 安装CV场景检测依赖..."

pip install 'scenedetect[opencv]' opencv-python numpy -i https://pypi.tuna.tsinghua.edu.cn/simple

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功！"
    echo ""
    echo "已安装："
    echo "  - scenedetect (PySceneDetect库)"
    echo "  - opencv-python (OpenCV)"
    echo "  - numpy (数值计算)"
    echo ""
    echo "现在可以使用CV场景检测功能了！"
else
    echo "❌ 安装失败，请手动安装："
    echo "  pip install 'scenedetect[opencv]' opencv-python numpy"
fi

