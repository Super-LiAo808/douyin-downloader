"""
抖音 API 实现模块
使用多种方法尝试获取视频信息
"""

import re
import json
import requests
from typing import Dict, Any, Optional


class DouyinAPI:
    """抖音 API 客户端"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://www.douyin.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    def resolve_share_url(self, share_url: str) -> Optional[str]:
        """
        解析短链接，获取真实 URL

        Args:
            share_url: 抖音分享链接

        Returns:
            真实 URL
        """
        try:
            response = self.session.get(share_url, allow_redirects=False, timeout=10)
            if response.status_code in [301, 302]:
                redirect_url = response.headers.get('Location', '')
                # 清理 URL 中的参数
                base_url = redirect_url.split('?')[0]
                return base_url
        except Exception as e:
            print(f"⚠️ 解析短链接失败: {e}")
        return None

    def extract_aweme_id(self, url: str) -> Optional[str]:
        """从 URL 中提取 aweme_id"""
        match = re.search(r'(\d{19})', url)
        if match:
            return match.group(1)

        if '/share/video/' in url:
            match = re.search(r'/share/video/(\d{19})', url)
            if match:
                return match.group(1)

        return None

    def get_video_info(self, aweme_id: str) -> Optional[Dict[str, Any]]:
        """
        尝试多种方法获取视频信息

        Args:
            aweme_id: 视频 ID

        Returns:
            视频信息字典
        """
        # 方法1: 直接 API（可能被风控）
        result = self._try_api_method(aweme_id)
        if result:
            return result

        # 方法2: 爬取页面解析
        result = self._try_scrape_method(aweme_id)
        if result:
            return result

        # 方法3: 使用第三方 API (备用方案)
        result = self._try_thirdparty_api(aweme_id)
        if result:
            return result

        return None

    def _try_api_method(self, aweme_id: str) -> Optional[Dict[str, Any]]:
        """尝试使用官方 API"""
        api_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={aweme_id}&aid=1128"

        try:
            response = self.session.get(api_url, timeout=15)
            data = response.json()

            if data.get('aweme_detail'):
                return self._parse_video_data(data['aweme_detail'])
        except Exception as e:
            pass

        return None

    def _try_scrape_method(self, aweme_id: str) -> Optional[Dict[str, Any]]:
        """尝试爬取页面"""
        share_url = f"https://www.iesdouyin.com/share/video/{aweme_id}"

        try:
            response = self.session.get(share_url, timeout=15)
            html = response.text

            # 查找 JSON 数据
            patterns = [
                r'<script[^>]*RENDER_DATA[^>]*>(.*?)</script>',
                r'<script[^>]*id=\"__NEXT_DATA__\"[^>]*>(.*?)</script>',
                r'<script[^>]*type=\"application/json\"[^>]*>(.*?)</script>',
            ]

            for pattern in patterns:
                match = re.search(pattern, html, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    # 尝试解码
                    try:
                        from urllib.parse import unquote
                        decoded = unquote(json_str)
                        data = json.loads(decoded)
                        return self._parse_render_data(data)
                    except:
                        # 直接解析
                        try:
                            data = json.loads(json_str)
                            return self._parse_render_data(data)
                        except:
                            pass
        except Exception as e:
            pass

        return None

    def _try_thirdparty_api(self, aweme_id: str) -> Optional[Dict[str, Any]]:
        """
        尝试使用第三方 API (备用方案)
        注意: 这里需要用户自己提供可用的第三方 API
        """
        # 示例: 使用公开的无水印解析接口
        # 这个接口可能随时失效，需要用户更换

        # 第三方API列表（示例）:
        third_party_apis = [
            # 用户可以在这里配置自己发现的可用接口
            # "https://api.example.com/douyin",
        ]

        print("⚠️ 官方API和页面爬取都失败了")
        print("💡 建议:")
        print("   1. 配置 Cookie 并使用 Evil0ctal/Douyin_TikTok_Download_API")
        print("   2. 使用第三方 API 服务")
        print("   3. 直接克隆成熟项目: https://github.com/Evil0ctal/Douyin_TikTok_Download_API")

        return {
            "aweme_id": aweme_id,
            "title": "视频名（需要Cookie才能获取）",
            "author": "未知",
            "video_url": "",
            "cover_url": "",
            "type": "video",
            "note": "抖音API需要Cookie才能访问，请参考 https://github.com/Evil0ctal/Douyin_TikTok_Download_API"
        }

    def _parse_video_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """解析 API 返回的数据"""
        return {
            "aweme_id": data.get("aweme_id"),
            "title": data.get("desc", "无标题"),
            "author": data.get("author", {}).get("nickname", "未知"),
            "video_url": self._extract_no_watermark_url(data),
            "cover_url": data.get("video", {}).get("cover", {}).get("url_list", [""])[0],
            "type": "video",
        }

    def _parse_render_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """解析 RENDER_DATA"""
        try:
            # 尝试多种路径
            paths = [
                data.get("app", {}).get("videoDetail", {}),
                data.get("props", {}).get("pageProps", {}).get("video", {}),
                data.get("videoDetail", {}),
            ]

            for app_data in paths:
                if app_data:
                    return {
                        "aweme_id": app_data.get("awemeId") or app_data.get("aweme_id"),
                        "title": app_data.get("desc") or app_data.get("title", "无标题"),
                        "author": app_data.get("author", {}).get("nickname", "未知"),
                        "video_url": self._extract_from_data(app_data),
                        "cover_url": app_data.get("video", {}).get("cover", ""),
                        "type": "video",
                    }
        except:
            pass

        return None

    def _extract_from_data(self, data: Dict[str, Any]) -> str:
        """从数据中提取视频URL"""
        video = data.get("video", {})

        # 尝试多个字段
        for key in ["play_addr", "download_addr", "bit_rate", "video"]:
            if key in video:
                addr = video[key]
                if isinstance(addr, dict):
                    url_list = addr.get("url_list", [])
                    if url_list:
                        url = url_list[0]
                        url = url.replace("playwm", "play")  # 去水印
                        return url
                elif isinstance(addr, list):
                    if addr:
                        return addr[0]

        return ""

    def _extract_no_watermark_url(self, data: Dict[str, Any]) -> str:
        """提取无水印URL"""
        return self._extract_from_data(data)
