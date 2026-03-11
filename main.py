#!/usr/bin/env python3
"""
抖音下载器 - 命令行入口
"""

import argparse
import sys
from pathlib import Path

from src.core import quick_download_video, quick_download_image


def main():
    parser = argparse.ArgumentParser(
        description="抖音爬虫 + 视频/图片无水印下载工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 下载单个视频
  python main.py -v "https://www.douyin.com/video/1234567890123456789"

  # 下载单个图片
  python main.py -i "https://www.douyin.com/photo/1234567890123456789"

  # 批量下载
  python main.py -b urls.txt

注意:
  - 获取无水印视频链接需要实际调用抖音 API（本示例为框架代码）
  - 请勿用于商业用途，仅供学习参考
        """
    )
    
    parser.add_argument(
        '-v', '--video',
        type=str,
        help='抖音视频 URL'
    )
    
    parser.add_argument(
        '-i', '--image',
        type=str,
        help='抖音图片 URL'
    )
    
    parser.add_argument(
        '-b', '--batch',
        type=str,
        help='包含 URL 列表的文件路径'
    )
    
    parser.add_argument(
        '--sync',
        action='store_true',
        help='使用同步模式（默认异步）'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='./downloads',
        help='下载目录（默认: ./downloads）'
    )
    
    args = parser.parse_args()
    
    # 创建输出目录
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 下载单个视频
        if args.video:
            print(f"🎬 正在下载视频: {args.video[:50]}...")
            filepath = quick_download_video(args.video, async_mode=not args.sync)
            print(f"✅ 下载成功: {filepath}")
        
        # 下载单个图片
        elif args.image:
            print(f"🖼️  正在下载图片: {args.image[:50]}...")
            filepath = quick_download_image(args.image, async_mode=not args.sync)
            print(f"✅ 下载成功: {filepath}")
        
        # 批量下载
        elif args.batch:
            print(f"📁 正在读取文件: {args.batch}")
            with open(args.batch, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            print(f"🚀 开始批量下载 {len(urls)} 个文件...")
            # 这里需要实现批量下载逻辑
            print(f"✅ 批量下载完成（示例）")
        
        # 没有参数，显示帮助
        else:
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
