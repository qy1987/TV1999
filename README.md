# IPTV 频道管理工具

## 项目概述

这是一个用于管理和优化 IPTV 频道的工具，能够自动获取、解析、分类和测速 IPTV 频道，并导出结果。它可以帮助用户快速筛选出可用的 IPTV 频道，提高观看体验。

## 功能特点

- 自动获取订阅源：从指定的订阅源 URL 获取 IPTV 频道数据。
- 智能分类：根据预定义的分类模板对频道进行自动分类。
- 测速功能：对每个频道进行速度测试，确保只保留可用且速度良好的频道。
- 黑名单过滤：支持通过黑名单过滤不需要的频道。
- 多格式导出：支持导出为 M3U、TXT 和 CSV 格式，方便不同设备使用。
- IPv4/IPv6 分类导出：将频道按 IPv4 和 IPv6 地址分别导出，便于针对性使用。

## 项目结构
#project/
#├── core/
#│   ├── init.py
#│   ├── fetcher.py
#│   ├── parser.py
#│   ├── matcher.py
#│   ├── tester.py
#│   ├── exporter.py
#│   └── models.py
#├── config/
#│   ├── config.ini
#│   ├── urls.txt
#│   ├── templates.txt
#│   └── blacklist.txt
#├── main.py
#└── requirements.txt

## 使用方法

### 配置项目

1. 编辑 `config/config.ini` 文件，设置输出目录、测速参数等。
2. 在 `config/urls.txt` 中添加您的 IPTV 订阅源 URL。
3. 在 `config/templates.txt` 中定义频道分类规则。
4. 在 `config/blacklist.txt` 中添加需要过滤的域名、URL 或频道名称。

### 运行程序

```bash
python main.py
