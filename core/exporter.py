#!/usr/bin/env python3
from typing import List, Callable
from pathlib import Path
from datetime import datetime
import csv
from .models import Channel

class ResultExporter:
    """结果导出模块，支持导出 M3U、TXT 和 CSV 格式的文件。"""

    def __init__(self, output_dir: str, enable_history: bool, template_path: str, config, matcher):
        """
        初始化导出模块。

        :param output_dir: 输出目录路径。
        :param enable_history: 是否启用历史记录功能。
        :param template_path: 分类模板路径。
        :param config: 配置对象，用于读取文件名配置。
        :param matcher: AutoCategoryMatcher 实例，用于频道名称规范化和排序。
        """
        self.output_dir = Path(output_dir)
        self.enable_history = enable_history
        self.template_path = template_path
        self.config = config
        self.matcher = matcher  # 保存 matcher 实例
        self._ensure_dirs()

    def _ensure_dirs(self):
        """确保输出目录存在，如果不存在则创建。"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, channels: List[Channel], progress_cb: Callable):
        """
        执行导出流程。

        :param channels: 频道列表。
        :param progress_cb: 进度回调函数，用于通知导出进度。
        """
        # 根据模板对频道进行排序
        sorted_channels = self.matcher.sort_channels_by_template(channels)

        # 导出 M3U、TXT 和 CSV 文件
        self._export_m3u(sorted_channels)
        progress_cb(1)
        self._export_txt(sorted_channels)
        progress_cb(1)
        if self.enable_history:
            self._export_csv(sorted_channels)
            progress_cb(1)

    def _export_m3u(self, channels: List[Channel]):
        """
        导出 M3U 文件。

        :param channels: 频道列表。
        """
        m3u_filename = self.config.get('EXPORTER', 'm3u_filename', fallback='all.m3u')
        path = self.output_dir / m3u_filename  # 基于 output_dir 和配置中的文件名生成路径
        epg_url = self.config.get('EXPORTER', 'm3u_epg_url', fallback='')
        logo_url = self.config.get('EXPORTER', 'm3u_logo_url', fallback='')

        with open(path, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")  # M3U 文件头
            if epg_url:
                f.write(f'#EXT-X-EPG:URL="{epg_url}"\n')
            if logo_url:
                f.write(f'#EXT-X-LOGO:URL="{logo_url}"\n')

            seen_urls = set()  # 用于记录已经写入的 URL
            for c in channels:
                if c.status == 'online' and c.url not in seen_urls:
                    # 写入频道信息
                    f.write(f"#EXTINF:-1 group-title=\"{c.category}\",{c.name}\n")
                    if logo_url:
                        f.write(f'#EXTVLCOPT:logo="{logo_url}"\n')
                    f.write(f"{c.url}\n")
                    seen_urls.add(c.url)

    def _export_txt(self, channels: List[Channel]):
        """
        导出 TXT 文件。

        :param channels: 频道列表。
        """
        txt_filename = self.config.get('EXPORTER', 'txt_filename', fallback='all.txt')
        path = self.output_dir / txt_filename  # 基于 output_dir 和配置中的文件名生成路径
        with open(path, 'w', encoding='utf-8') as f:
            seen_urls = set()  # 用于记录已经写入的 URL
            current_category = None

            for c in channels:
                if c.status == 'online' and c.url not in seen_urls:
                    # 如果分类发生变化，写入分类行
                    if c.category != current_category:
                        if current_category is not None:
                            f.write("\n")  # 在分类之间添加空行
                        f.write(f"{c.category},#genre#\n")
                        current_category = c.category

                    # 写入频道信息
                    f.write(f"{c.name},{c.url}\n")
                    seen_urls.add(c.url)

    def _export_csv(self, channels: List[Channel]):
        """
        导出 CSV 文件（历史记录）。

        :param channels: 频道列表。
        """
        if self.enable_history:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 时间戳，增加秒信息
            csv_filename_format = self.config.get('EXPORTER', 'csv_filename_format', fallback='history_{timestamp}.csv')
            path = self.output_dir / csv_filename_format.format(timestamp=timestamp)
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 写入 CSV 文件头
                writer.writerow(['频道名称', '分类', '状态', '响应时间', 'URL'])
                seen_urls = set()  # 用于记录已经写入的 URL
                for c in channels:
                    if c.url not in seen_urls:
                        # 写入频道信息
                        writer.writerow([
                            c.name,
                            c.category,
                            c.status,
                            f"{c.response_time:.2f}s" if c.response_time else 'N/A',
                            c.url
                        ])
                        seen_urls.add(c.url)