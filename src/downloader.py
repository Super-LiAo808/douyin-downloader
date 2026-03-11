"""
下载器模块
负责下载视频和图片文件
"""

import os
import asyncio
import aiohttp
from pathlib import Path
from typing import Optional
import logging

from config import DOWNLOAD_DIR, TIMEOUT, USER_AGENTS



class Downloader:
    """异步下载器"""
    
    def __init__(self, download_dir: str = DOWNLOAD_DIR):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def download_file(self, url: str, filename: Optional[str] = None) -> str:
        """
        下载文件

        Args:
            url: 文件 URL
            filename: 保存的文件名（可选）

        Returns:
            下载文件的完整路径
        """
        if not filename:
            # 从 URL 中提取文件名
            filename = url.split('/')[-1].split('?')[0]
        
        filepath = self.download_dir / filename
        
        # 获取 User-Agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.douyin.com/"
        }
        
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                with open(filepath, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024):
                        f.write(chunk)
                return str(filepath)
            else:
                raise Exception(f"下载失败: HTTP {response.status}")
    
    async def download_video(
        self,
        video_url: str,
        filename: Optional[str] = None,
        callback=None
    ) -> str:
        """
        下载视频

        Args:
            video_url: 视频无水印 URL
            filename: 保存的文件名
            callback: 进度回调函数

        Returns:
            下载文件的完整路径
        """
        if not filename:
            filename = f"video_{asyncio.get_event_loop().time()}.mp4"
        
        return await self.download_file(video_url, filename)
    
    async def download_image(
        self,
        image_url: str,
        filename: Optional[str] = None
    ) -> str:
        """
        下载图片

        Args:
            image_url: 图片无水印 URL
            filename: 保存的文件名

        Returns:
            下载文件的完整路径
        """
        if not filename:
            filename = f"image_{asyncio.get_event_loop().time()}.jpg"
        
        return await self.download_file(image_url, filename)
    
    async def batch_download(
        self,
        urls: list,
        prefix: str = "download"
    ) -> list:
        """
        批量下载文件

        Args:
            urls: URL 列表
            prefix: 文件名前缀

        Returns:
            下载文件路径列表
        """
        tasks = []
        for i, url in enumerate(urls):
            ext = "mp4" if "video" in url else "jpg"
            filename = f"{prefix}_{i+1}.{ext}"
            tasks.append(self.download_file(url, filename))
        
        return await asyncio.gather(*tasks, return_exceptions=True)


class SyncDownloader:
    """同步下载器（兼容性版本）"""
    
    def __init__(self, download_dir: str = DOWNLOAD_DIR):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def download_file(self, url: str, filename: Optional[str] = None) -> str:
        """
        同步下载文件

        Args:
            url: 文件 URL
            filename: 保存的文件名

        Returns:
            下载文件的完整路径
        """
        import requests
        
        if not filename:
            filename = url.split('/')[-1].split('?')[0]
        
        filepath = self.download_dir / filename
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.douyin.com/"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return str(filepath)
        else:
            raise Exception(f"下载失败: HTTP {response.status_code}")
