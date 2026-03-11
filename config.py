# 抖音爬虫配置文件

# 下载设置
DOWNLOAD_DIR = "./downloads"  # 下载目录
MAX_CONCURRENT = 5  # 最大并发数
TIMEOUT = 30  # 请求超时时间（秒）

# 视频设置
VIDEO_QUALITY = "high"  # high, medium, low
VIDEO_FORMAT = "mp4"  # 输出格式

# 图片设置
IMAGE_FORMAT = "jpg"  # 输出格式
IMAGE_QUALITY = 100  # 图片质量 1-100

# 代理设置（可选）
# PROXY = "http://127.0.0.1:7890"

# User-Agent 池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
]
