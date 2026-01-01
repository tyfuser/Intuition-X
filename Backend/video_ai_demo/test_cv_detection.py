#!/usr/bin/env python3
"""
CV场景检测测试脚本
用于验证CV检测功能是否正常工作
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from app.pipeline.steps.scene_detect import detect_scenes, detect_scenes_simple


def test_cv_detection():
    """测试CV场景检测"""
    
    print("=" * 60)
    print("CV场景检测 - 功能测试")
    print("=" * 60)
    print()
    
    # 检查依赖
    print("1. 检查依赖...")
    try:
        import cv2
        import numpy as np
        from scenedetect import open_video, SceneManager
        from scenedetect.detectors import ContentDetector
        print("   ✅ 所有依赖已安装")
        print(f"   - OpenCV: {cv2.__version__}")
        print(f"   - NumPy: {np.__version__}")
        print(f"   - PySceneDetect: 已安装")
    except ImportError as e:
        print(f"   ❌ 缺少依赖: {e}")
        print()
        print("请运行以下命令安装依赖：")
        print("  bash install_cv_deps.sh")
        print("或：")
        print("  pip install 'scenedetect[opencv]' opencv-python numpy")
        return False
    
    print()
    
    # 检查测试视频
    print("2. 检查测试视频...")
    test_video = Path("./data/test_video.mp4")
    
    if not test_video.exists():
        print(f"   ⚠️  测试视频不存在: {test_video}")
        print()
        print("请提供一个测试视频文件：")
        print("  ./data/test_video.mp4")
        print()
        print("或修改脚本中的 test_video 路径")
        return False
    
    print(f"   ✅ 找到测试视频: {test_video}")
    print()
    
    # 测试CV检测
    print("3. 测试CV场景检测...")
    try:
        output_dir = Path("./data/test_output")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        segments = detect_scenes(
            str(test_video),
            output_dir,
            threshold=27.0,
            min_scene_len=15
        )
        
        print(f"   ✅ 检测成功！")
        print(f"   - 检测到 {len(segments)} 个场景")
        print()
        
        # 显示场景详情
        print("场景列表：")
        print("-" * 60)
        for i, seg in enumerate(segments[:10], 1):  # 最多显示10个
            duration = seg['duration_ms'] / 1000
            print(f"  {i}. {seg['segment_id']}")
            print(f"     时间: {seg['start_ms']:.0f}ms - {seg['end_ms']:.0f}ms")
            print(f"     时长: {duration:.2f}秒")
            print()
        
        if len(segments) > 10:
            print(f"  ... 还有 {len(segments) - 10} 个场景")
            print()
        
        return True
        
    except Exception as e:
        print(f"   ❌ 检测失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_detection():
    """测试简单快速检测"""
    
    print()
    print("=" * 60)
    print("快速场景检测 - 功能测试")
    print("=" * 60)
    print()
    
    test_video = Path("./data/test_video.mp4")
    
    if not test_video.exists():
        print("⚠️  跳过（没有测试视频）")
        return False
    
    print("测试快速检测算法...")
    try:
        output_dir = Path("./data/test_output")
        
        segments = detect_scenes_simple(
            str(test_video),
            output_dir,
            threshold=30.0,
            sample_rate=5
        )
        
        print(f"✅ 快速检测成功！")
        print(f"   - 检测到 {len(segments)} 个场景")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 快速检测失败: {e}")
        return False


def main():
    """主函数"""
    
    print()
    print("🎬 CV场景检测 - 功能测试")
    print()
    
    # 测试标准检测
    result1 = test_cv_detection()
    
    # 测试快速检测
    result2 = test_simple_detection()
    
    print()
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    
    if result1:
        print("✅ CV场景检测：通过")
    else:
        print("❌ CV场景检测：失败")
    
    if result2:
        print("✅ 快速检测：通过")
    else:
        print("⚠️  快速检测：跳过")
    
    print()
    
    if result1:
        print("🎉 恭喜！CV场景检测功能正常工作！")
        print()
        print("下一步：")
        print("  1. 启动服务: uvicorn app.main:app --reload")
        print("  2. 测试API: curl -X POST http://localhost:8000/v1/video-analysis/jobs ...")
        print("  3. 查看文档: http://localhost:8000/docs")
        print()
    else:
        print("⚠️  请先解决上述问题，然后重新运行测试")
        print()


if __name__ == "__main__":
    main()

