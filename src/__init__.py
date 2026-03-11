"""
抖音下载器
抖音爬虫 + 视频/图片无水印下载工具
"""

__version__ = "1.0.0"
__author__ = "liao"

from .core import DouyinDownloader, quick_download_video, quick_download_image
from .parser import DouyinParser
from .downloader import Downloader, SyncDownloader

__all__ = [
    "DouyinDownloader",
    "quick_download_video",
    "quick_download_image",
    "DouyinParser",
    "Downloader",
    "SyncDownloader",
]
