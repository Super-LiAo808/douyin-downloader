# 抖音爬虫 + 无水印下载工具

基于 Python 的抖音爬虫和视频/图片无水印下载工具。

## 功能特点

- ✅ 抖音视频无水印下载
- ✅ 抖音图片无水印下载
- ✅ 批量下载支持
- ✅ 命令行工具
- ✅ 异步高性能
- ✅ 简单易用

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 下载单个视频

```bash
python main.py -v <抖音视频URL>
```

### 下载单个图片

```bash
python main.py -i <抖音图片URL>
```

### 批量下载

```bash
python main.py -b <包含URL的文件>
```

## 项目结构

```
douyin-downloader/
├── src/
│   ├── core.py           # 核心下载逻辑
│   ├── parser.py         # URL解析
│   └── downloader.py     # 下载器
├── config.py             # 配置文件
├── main.py               # 主入口
├── requirements.txt      # 依赖
└── README.md            # 说明文档
```

## 参考项目

- [Evil0ctal/Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API)
- [xiyaowong/spiders](https://github.com/xiayaowong/spiders)

## 许可证

MIT License
