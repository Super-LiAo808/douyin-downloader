# 使用说明

## 当前状态

本项目的核心框架已完成，但由于抖音的反爬策略，直接访问需要：

1. **配置 Cookie** - 从浏览器获取 Douyin 网站的 Cookie
2. **X-Bogus 签名算法** - 用于绕过风控

## 快速使用方案（推荐）

### 方案A: 直接使用成熟项目

```bash
git clone https://github.com/Evil0ctal/Douyin_TikTok_Download_API
cd Douyin_TikTok_Download_API
pip install -r requirements.txt
python3 main.py
```

### 方案B: 使用第三方 API

如果只是想快速下载，可以使用在线解析服务：

```python
import requests

def download_douyin(share_url):
    # 使用第三方 API
    api_url = f"https://api.example.com/douyin?url={share_url}"
    response = requests.get(api_url)
    data = response.json()

    if data.get('video_url'):
        # 下载视频
        video_url = data['video_url']
        response = requests.get(video_url)
        with open('video.mp4', 'wb') as f:
            f.write(response.content)
```

## 本项目的使用

本项目的意义在于：

1. ✅ **学习抖音爬虫的原理**
2. ✅ **理解 URL 解析和数据提取**
3. ✅ **掌握异步下载技术的实现**
4. ✅ **可以作为其他项目的参考框架**

## 技术要点

```
分享链接解析:
  v.douyin.com/xxx → iesdouyin.com/share/video/{aweme_id}

视频获取方法:
  1. API 请求 (需要 X-Bogus 签名)
  2. 页面爬取 (需要 Cookie)
  3. 第三方 API (依赖外部服务)

去水印原理:
  playwm.xx.com → play.xx.com
```

## 参考资源

- [Evil0ctal/Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API)
- 抖音 Web API 文档（暗网）
- X-Bogus 算法源码

## 许可证

MIT License - 仅供学习使用，请勿用于商业用途
