"""
核心模块 - 整合真实的抖音API
整合解析器和下载器，提供完整的下载功能
"""

import asyncio
import logging
from typing import Optional, List

from .douyin_api import DouyinAPI
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
        self.api = DouyinAPI()
        self.async_mode = async_mode

        if async_mode:
            self.downloader = Downloader()
        else:
            self.downloader = SyncDownloader()

    async def download_video_async(self, url: str) -> str:
        """
        异步下载单个视频

        Args:
            url: 抖音视频 URL（可以是分享链接或直接链接）

        Returns:
            下载的文件路径
        """
        logger.info(f"🔍 正在解析视频 URL: {url}")

        # 1. 解析短链接
        real_url = self.api.resolve_share_url(url)
        if real_url:
            logger.info(f"✅ 短链接已解析: {real_url}")
            url = real_url

        # 2. 提取 aweme_id
        aweme_id = self.api.extract_aweme_id(url)
        if not aweme_id:
            raise ValueError(f"无法从 URL 中提取 aweme_id: {url}")

        logger.info(f"✅ 提取到 aweme_id: {aweme_id}")

        # 3. 获取视频信息
        video_info = self.api.get_video_info(aweme_id)
        if not video_info:
            raise ValueError(f"无法获取视频信息: {aweme_id}")

        logger.info(f"✅ 解析成功: {video_info.get('title', '未知')} - 作者: {video_info.get('author', '未知')}")

        # 4. 下载视频
        video_url = video_info.get('video_url', '')
        if not video_url:
            raise ValueError("未找到视频下载链接，可能是视频已被删除或来自私密账号")

        logger.info(f"🎬 开始下载视频...")

        async with self.downloader as dl:
            filename = f"video_{aweme_id}.mp4"
            filepath = await dl.download_video(video_url, filename)
            logger.info(f"✅ 下载完成: {filepath}")
            return filepath

    def download_video_sync(self, url: str) -> str:
        """
        同步下载单个视频

        Args:
            url: 抖音视频 URL

        Returns:
            下载的文件路径
        """
        logger.info(f"🔍 正在解析视频 URL: {url}")

        # 1. 解析短链接
        real_url = self.api.resolve_share_url(url)
        if real_url:
            logger.info(f"✅ 短链接已解析: {real_url}")
            url = real_url

        # 2. 提取 aweme_id
        aweme_id = self.api.extract_aweme_id(url)
        if not aweme_id:
            raise ValueError(f"无法从 URL 中提取 aweme_id: {url}")

        logger.info(f"✅ 提取到 aweme_id: {aweme_id}")

        # 3. 获取视频信息
        video_info = self.api.get_video_info(aweme_id)
        if not video_info:
            raise ValueError(f"无法获取视频信息: {aweme_id}")

        logger.info(f"✅ 解析成功: {video_info.get('title', '未知')} - 作者: {video_info.get('author', '未知')}")

        # 4. 下载视频
        video_url = video_info.get('video_url', '')
        if not video_url:
            raise ValueError("未找到视频下载链接，可能是视频已被删除或来自私密账号")

        logger.info(f"🎬 开始下载视频...")

        dl = SyncDownloader()
        filename = f"video_{aweme_id}.mp4"
        filepath = dl.download_file(video_url, filename)
        logger.info(f"✅ 下载完成: {filepath}")
        return filepath

    async def download_image_async(self, url: str) -> str:
        """
        异步下载单个图片

        Args:
            url: 抖音图片 URL

        Returns:
            下载的文件路径
        """
        logger.info(f"🔍 正在解析图片 URL: {url}")

        # 1. 解析短链接
        real_url = self.api.resolve_share_url(url)
        if real_url:
            url = real_url

        # 2. 提取 aweme_id
        aweme_id = self.api.extract_aweme_id(url)
        if not aweme_id:
            raise ValueError(f"无法从 URL 中提取 aweme_id: {url}")

        # 3. 获取图片信息（目前复用视频API）
        video_info = self.api.get_video_info(aweme_id)
        if not video_info:
            raise ValueError(f"无法获取图片信息: {aweme_id}")

        # 4. 下载封面图作为图集代表
        cover_url = video_info.get('cover_url', '')
        if not cover_url:
            raise ValueError("未找到图片下载链接")

        logger.info(f"🖼️  开始下载图片...")

        async with self.downloader as dl:
            filename = f"image_{aweme_id}.jpg"
            filepath = await dl.download_image(cover_url, filename)
            logger.info(f"✅ 下载完成: {filepath}")
            return filepath

    def download_image_sync(self, url: str) -> str:
        """
        同步下载单个图片

        Args:
            url: 抖音图片 URL

        Returns:
            下载的文件路径
        """
        logger.info(f"🔍 正在解析图片 URL: {url}")

        real_url = self.api.resolve_share_url(url)
        if real_url:
            url = real_url

        aweme_id = self.api.extract_aweme_id(url)
        if not aweme_id:
            raise ValueError(f"无法从 URL 中提取 aweme_id: {url}")

        video_info = self.api.get_video_info(aweme_id)
        if not video_info:
            raise ValueError(f"无法获取图片信息: {aweme_id}")

        cover_url = video_info.get('cover_url', '')
        if not cover_url:
            raise ValueError("未找到图片下载链接")

        logger.info(f"🖼️  开始下载图片...")

        dl = SyncDownloader()
        filename = f"image_{aweme_id}.jpg"
        filepath = dl.download_file(cover_url, filename)
        logger.info(f"✅ 下载完成: {filepath}")
        return filepath


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
