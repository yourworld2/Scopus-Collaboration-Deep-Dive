"""Public deployment helper for scopus-collaboration-deep-dive outputs.
公网部署助手，用于 scopus-collaboration-deep-dive 输出。

Three deployment patterns:
三种部署模式：

1. Public dashboard (single page) | 公网仪表板（单页）
2. Download link (HTML with landing page) | 下载链接（HTML + 着陆页）
3. ZIP bundle (offline distribution) | ZIP 包（离线分发）

Usage:
用法：
    from deploy import deploy_dashboard, deploy_download, deploy_zip_bundle

    deploy_dashboard(html_path, project_name)
    deploy_download(html_path, project_name)
    deploy_zip_bundle(file_paths, project_name)
"""

import base64
import os
import shutil
import zipfile
from pathlib import Path
from typing import List


DEFAULT_LANDING_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title} | Download | 下载</title>
<style>
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
       margin: 0; padding: 40px; background: #f7f7f7; color: #202028; line-height: 1.6; }}
.container {{ max-width: 720px; margin: 0 auto; background: white; padding: 40px;
              border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
h1 {{ color: #00356b; border-bottom: 3px solid #bd5319; padding-bottom: 12px; margin-top: 0; }}
.btn {{ display: inline-block; background: #00356b; color: white; padding: 12px 24px;
        border-radius: 6px; text-decoration: none; font-weight: 600; margin: 16px 0; }}
.btn:hover {{ background: #2a4a6e; }}
code {{ background: #f0f0f5; padding: 2px 6px; border-radius: 3px;
        font-family: "SF Mono", Menlo, Consolas, monospace; }}
</style>
</head>
<body>
<div class="container">
<h1>📦 {title}</h1>
<p>{description}</p>

<a class="btn" href="./{filename}" download>
  📥 Download 下载 {filename} ({size_kb} KB)
</a>

<p style="font-size: 0.85em; color: #666; margin-top: 8px;">
  Or open directly 直接打开: <a href="./{filename}">view in browser 在浏览器中查看</a>
</p>

<p style="margin-top: 32px; font-size: 0.85em; color: #888;">
Built by Mavis Agent team. Source: Source 数据源 Scopus export.
</p>
</div>
</body>
</html>
'''


def deploy_dashboard(html_path: str, project_name: str, deploy_tool=None):
    """Deploy a single HTML dashboard via website_deploy.
    通过 website_deploy 部署单个 HTML 仪表板。

    Args:
        html_path: Path to HTML file. | HTML 文件路径。
        project_name: Display name for the deployment. | 部署显示名称。
        deploy_tool: website_deploy function (defaults to importing). | website_deploy 函数（默认导入）。

    Returns:
        URL string. | URL 字符串。
    """
    if deploy_tool is None:
        from website_deploy import website_deploy
        deploy_tool = website_deploy

    site_dir = Path('/tmp/deploy_' + project_name.replace(' ', '_'))
    site_dir.mkdir(exist_ok=True)

    shutil.copy(html_path, site_dir / 'index.html')

    result = deploy_tool(
        path=str(site_dir),
        source_path=str(site_dir),
        project_name=project_name,
    )
    return result.url if hasattr(result, 'url') else str(result)


def deploy_download(html_path: str, project_name: str,
                    deploy_tool=None, description: str = ''):
    """Deploy HTML as a download link with a landing page.
    将 HTML 部署为带着陆页的下载链接。

    Args:
        html_path: Path to HTML file. | HTML 文件路径。
        project_name: Display name. | 显示名称。
        deploy_tool: website_deploy function. | website_deploy 函数。
        description: Optional description for landing page. | 着陆页可选描述。

    Returns:
        URL string. | URL 字符串。
    """
    if deploy_tool is None:
        from website_deploy import website_deploy
        deploy_tool = website_deploy

    src = Path(html_path)
    site_dir = Path('/tmp/download_' + project_name.replace(' ', '_'))
    site_dir.mkdir(exist_ok=True)

    filename = src.name
    shutil.copy(html_path, site_dir / filename)

    size_kb = src.stat().st_size / 1024

    landing = DEFAULT_LANDING_TEMPLATE.format(
        title=project_name,
        description=description or 'Self-contained analysis report. | 自包含分析报告。',
        filename=filename,
        size_kb=f'{size_kb:.1f}',
    )
    (site_dir / 'index.html').write_text(landing, encoding='utf-8')

    result = deploy_tool(
        path=str(site_dir),
        source_path=str(site_dir),
        project_name=f'{project_name} (download | 下载)',
    )
    return result.url if hasattr(result, 'url') else str(result)


def deploy_zip_bundle(file_paths: List[str], project_name: str,
                       zip_filename: str = 'bundle.zip',
                       deploy_tool=None):
    """Create a ZIP bundle of multiple files and deploy as download.
    创建包含多个文件的 ZIP 包并部署为下载。

    Args:
        file_paths: List of file paths to include. | 要包含的文件路径列表。
        project_name: Display name. | 显示名称。
        zip_filename: Output ZIP filename. | 输出 ZIP 文件名。
        deploy_tool: website_deploy function. | website_deploy 函数。

    Returns:
        URL string. | URL 字符串。
    """
    if deploy_tool is None:
        from website_deploy import website_deploy
        deploy_tool = website_deploy

    site_dir = Path('/tmp/bundle_' + project_name.replace(' ', '_'))
    site_dir.mkdir(exist_ok=True)

    zip_path = site_dir / zip_filename
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fp in file_paths:
            fp_path = Path(fp)
            if fp_path.is_file():
                zf.write(fp_path, arcname=fp_path.name)
            else:
                print(f'Warning 警告: {fp} not found 未找到, skipping 跳过')

    size_kb = zip_path.stat().st_size / 1024

    landing = DEFAULT_LANDING_TEMPLATE.format(
        title=project_name + ' ZIP',
        description='Offline-ready bundle. Extract to view HTML in browser. | 离线包，解压后用浏览器查看 HTML。',
        filename=zip_filename,
        size_kb=f'{size_kb:.1f}',
    )
    (site_dir / 'index.html').write_text(landing, encoding='utf-8')

    result = deploy_tool(
        path=str(site_dir),
        source_path=str(site_dir),
        project_name=f'{project_name} ZIP',
    )
    return result.url if hasattr(result, 'url') else str(result)


def base64_xlsx(xlsx_path: str) -> str:
    """Read XLSX file and encode as base64 (for embedding in HTML download button).
    读取 XLSX 文件并编码为 base64（用于嵌入 HTML 下载按钮）。"""
    with open(xlsx_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')