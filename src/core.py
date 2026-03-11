"""
核心模块
整合解析器和下载器，提供完整的下载功能
"""

import asyncio
import logging
from typing import Optional, List

from .parser import DouyinParser
from .downloader import Downloader, SyncDownloader


 logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DouyinDownloader:
    """抖音下载器主类"""
    
    def __init__(self, async_mode: bool = True):
        """
        初始化下载器

        Args:
            async_mode: 是否使用异步模式（默认 True）
        """
        self.parser = DouyinParser()
        self.async_mode = async_mode
        
        if async_mode:
            self.downloader = Downloader()
        else:
            self.downloader = SyncDownloader()
    
    async def download_video_async(self, url: str) -> str:
        """
        异步下载单个视频

        Args:
            url: 抖音视频 URL

        Returns:
            下载的文件路径
        """
        logger.info(f"正在解析视频 URL: {url}")
        
        # 解析 URL
        info = self.parser.parse_url(url)
        if not info:
            raise ValueError("无法解析抖音 URL")
        
        logger.info(f"解析成功: {info.get('title', '未知')}")
        
        # 下载视频
        async with self.downloader as dl:
            # 注意：实际使用时需要将 info['media_url'] 替换为真实的无水印链接
            # 这里是示例代码
            video_url = info.get('media_url', '')
            if not video_url:
                raise ValueError("未找到视频下载链接")
            
            filepath = await dl.download_video(video_url)
            logger.info(f"下载完成: {filepath}")
            return filepath
    
    def download_video_sync(self, url: str) -> str:
        """
        同步下载单个视频

        Args:
            url: 抖音视频 URL

        Returns:
            下载的文件路径
        """
        logger.info(f"正在解析视频 URL: {url}")
        
        # 解析 URL
        info = self.parser.parse_url(url)
        if not info:
            raise ValueError("无法解析抖音 URL")
        
        logger.info(f"解析成功: {info.get('title', '未知')}")
        
        # 下载视频
        dl = SyncDownloader()
        video_url = info.get('media_url', '')
        if not video_url:
            raise ValueError("未找到视频下载链接")
        
        filepath = dl.download_file(video_url)
        logger.info(f"下载完成: {filepath}")
        return filepath
    
    async def download_image_async(self, url: str) -> str:
        """
        异步下载单个图片

        Args:
            url: 抖音图片 URL

        Returns:
            下载的文件路径
        """
        logger.info(f"正在解析图片 URL: {url}")
        
        # 解析 URL
        info = self.parser.parse_url(url)
        if not info:
            raise ValueError("无法解析抖音 URL")
        
        # 下载图片
        async with self.downloader as dl:
            image_url = info.get('media_url', '')
            if not image_url:
                raise ValueError("未找到图片下载链接")
            
            filepath = await dl.download_image(image_url)
            logger.info(f"下载完成: {filepath}")
            return filepath
    
    def download_image_sync(self, url: str) -> str:
        """
        同步下载单个图片

        Args:
            url: 抖音图片 URL

        Returns:
            下载的文件路径
        """
        logger.info(f"正在解析图片 URL: {url}")
        
        # 解析 URL
        info = self.parser.parse_url(url)
        if not info:
            raise ValueError("无法解析抖音 URL")
        
        # 下载图片
        dl = SyncDownloader()
        image_url = info.get('media_url', '')
        if not image_url:
            raise ValueError("未找到图片下载链接")
        
        filepath = dl.download_file(image_url)
        logger.info(f"下载完成: {filepath}")
        return filepath
    
    async def batch_download_async(self, urls: List[str]) -> List[str]:
        """
        异步批量下载

        Args:
            urls: URL 列表

        Returns:
            下载的文件路径列表
        """
        logger.info(f"开始批量下载 {len(urls)} 个文件")
        
        tasks = []
        for url in urls:
            info = self.parser.parse_url(url)
            if info:
                task_type = info.get('type', 'video')
                if task_type == 'video':
                    tasks.append(self.download_video_async(url))
                else:
                    tasks.append(self.download_image_async(url))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("批量下载完成")
        return results


def quick_download_video(url: str, async_mode: bool = True) -> str:
    """
    快速下载单个视频（便捷函数）

    Args:
        url: 抖音视频 URL
        async_mode: 是否异步

    Returns:
        下载的文件路径
    """
    downloader = DouyinDownloader(async_mode=async_mode)
    
    if async_mode:
        return asyncio.run(downloader.download_video_async(url))
    else:
        return downloader.download_video_sync(url)


def quick_download_image(url: str, async_mode: bool = True) -> str:
    """
    快速下载单个图片（便捷函数）

    Args:
        url: 抖音图片 URL
        async_mode: 是否异步

    Returns:
        下载的文件路径
    """
    downloader = DouyinDownloader(async_mode=async_mode)
    
    if async_mode:
        return asyncio.run(downloader.download_image_async(url))
    else:
        return downloader.download_image_sync(url)
