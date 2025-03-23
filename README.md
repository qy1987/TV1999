IPTV 频道管理工具
项目概述
这是一个用于管理和优化 IPTV 频道的工具，能够自动获取、解析、分类和测速 IPTV 频道，并导出结果。它可以帮助用户快速筛选出可用的 IPTV 频道，提高观看体验。
功能特点
自动获取订阅源：从指定的订阅源 URL 获取 IPTV 频道数据。
智能分类：根据预定义的分类模板对频道进行自动分类。
测速功能：对每个频道进行速度测试，确保只保留可用且速度良好的频道。
黑名单过滤：支持通过黑名单过滤不需要的频道。
多格式导出：支持导出为 M3U、TXT 和 CSV 格式，方便不同设备使用。
IPv4/IPv6 分类导出：将频道按 IPv4 和 IPv6 地址分别导出，便于针对性使用。
project/
├── core/
│   ├── __init__.py
│   ├── fetcher.py
│   ├── parser.py
│   ├── matcher.py
│   ├── tester.py
│   ├── exporter.py
│   └── models.py
├── config/
│   ├── config.ini
│   ├── urls.txt
│   ├── templates.txt
│   └── blacklist.txt
├── main.py
└── requirements.txt
使用方法
配置项目：
编辑 config/config.ini 文件，设置输出目录、测速参数等。
在 config/urls.txt 中添加您的 IPTV 订阅源 URL。
在 config/templates.txt 中定义频道分类规则。
在 config/blacklist.txt 中添加需要过滤的域名、URL 或频道名称。
[MAIN]
output_dir = outputs  # 输出目录
prefer_ip_version = 1  # 1: 按原始顺序排列, ipv6: 优先 IPv6, ipv4: 优先 IPv4

[FETCHER]
timeout = 15  # 请求超时时间（秒）
concurrency = 5  # 并发请求数

[TESTER]
timeout = 10  # 测速超时时间（秒）
concurrency = 5  # 并发测速数
max_attempts = 1  # 最大尝试次数
min_download_speed = 0.2  # 最小下载速度（KB/s）
enable_logging = True  # 是否启用日志输出

[EXPORTER]
enable_history = False  # 是否启用历史记录功能
m3u_filename = all.m3u  # M3U 文件名称
txt_filename = all.txt  # TXT 文件名称
csv_filename_format = history_{timestamp}.csv  # CSV 文件名称格式
m3u_epg_url = http://epg.51zmt.top:8000/cc.xml  # M3U 文件的 EPG 地址
m3u_logo_url = http://example.com/logo.png  # M3U 文件的图标 URL

[BLACKLIST]
blacklist_path = config/blacklist.txt  # 黑名单文件路径
show_progress = True  # 是否在过滤黑名单时显示进度条

[PATHS]
urls_path = config/urls.txt  # 订阅源文件路径
templates_path = config/templates.txt  # 分类模板文件路径
failed_urls_path = config/failed_urls.txt  # 无效连接储存路径
ipv4_output_path = ipv4.txt  # IPv4 地址存储路径
ipv6_output_path = ipv6.txt  # IPv6 地址存储路径

[PROGRESS]
update_interval_fetch = 10  # 获取源数据的进度条刷新间隔
update_interval_parse = 40  # 解析频道的进度条刷新间隔
update_interval_classify = 1000  # 分类频道的进度条刷新间隔
update_interval_speedtest = 500  # 测速测试的进度条刷新间隔
update_interval_export = 1  # 导出结果的进度条刷新间隔
update_interval_blacklist = 100  # 过滤黑名单的进度条刷新间隔
