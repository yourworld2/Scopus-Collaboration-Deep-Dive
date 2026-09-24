# Deployment guide | 部署指南

> How to share your XLSX + HTML dashboard publicly.
> 如何将你的 XLSX + HTML 仪表板公开分享。

## Option 1: Public URL via `website_deploy` | 通过 `website_deploy` 获取公网 URL

```python
# 1. Build the deliverable in a self-contained directory
# 1. 在自包含目录构建交付物
mkdir -p /tmp/share
cp output.html /tmp/share/index.html
cp output.xlsx /tmp/share/

# 2. Use the Mavis tool | 2. 使用 Mavis 工具
website_deploy(
    path="/tmp/share",
    source_path="/tmp/share",
    project_name="Yale × China 2022-2026"
)
# Returns: https://xyz.space.mcode.cn
```

The deployed URL is publicly accessible. Use only when the data is meant to be shared publicly.
部署后的 URL 可公开访问。仅在数据可以公开分享时使用。

## Option 2: Offline ZIP package | 离线 ZIP 包

For no-internet viewing (e.g., internal team on a flight):
无网络环境下查看（如内部团队在飞机上）：

```bash
mkdir -p output_bundle
cp output.html output_bundle/index.html
cp output.xlsx output_bundle/
cp intermediate.json output_bundle/

cd output_bundle
zip -r ../output_bundle.zip .
```

The HTML file is self-contained — no external CSS/JS/fonts. Opens in any browser.
HTML 文件自包含 — 无外部 CSS/JS/字体。任意浏览器都能打开。

Or use `scripts/deploy.py` for an automated workflow:
或用 `scripts/deploy.py` 自动工作流：

```python
from scripts.deploy import deploy_zip_bundle
deploy_zip_bundle(
    file_paths=['./output.html', './output.xlsx'],
    project_name='Yale × China',
)
```

## Option 3: Email-ready XLSX only | 仅邮件附件 XLSX

For just sharing the spreadsheet:
只分享数据表：

```bash
# Single XLSX with all sheets | 包含所有工作表的单个 XLSX
cp output.xlsx ~/Downloads/
```

XLSX size is typically 25-30 KB for 7 sheets — well within email attachment limits.
XLSX 通常 25-30 KB（7 个工作表）— 远低于邮件附件限制。

## Option 4: GitHub Pages / Vercel / Netlify | GitHub Pages / Vercel / Netlify

For long-term hosting with custom domain:
长期托管与自定义域名：

1. Create a new GitHub repo | 创建新的 GitHub 仓库
2. Push the `output_bundle/` contents to `docs/` or root | 推送 `output_bundle/` 到 `docs/` 或根目录
3. Enable GitHub Pages | 启用 GitHub Pages
4. Access via `https://username.github.io/repo-name/` | 通过 `https://username.github.io/repo-name/` 访问

## Option 5 (NEW v1.4): Download link with landing page | 下载链接 + 着陆页

For sharing via a single URL that has a landing page + download button:
通过单一 URL 分享（含着陆页 + 下载按钮）：

```python
from scripts.deploy import deploy_download
deploy_download(
    html_path='./output.html',
    project_name='Yale × China Report',
    description='Self-contained analysis report | 自包含分析报告',
)
```

The user lands on a friendly page with a "Download" button + the file size + a direct link.
用户进入友好的页面，看到"下载"按钮、文件大小和直链。

## Deployment checklist | 部署检查清单

Before deploying publicly, verify:
公开部署前确认：

- [ ] No PII (emails, phone numbers) in deliverable | 无 PII（邮箱、电话）
- [ ] No internal-only data (employee IDs, restricted research) | 无仅限内部数据
- [ ] License allows public sharing (Scopus data is OK for derived analyses) | 许可允许公开分享
- [ ] Get user confirmation | 获得用户确认
- [ ] Bilingual version verified in browser | 浏览器验证双语版本
- [ ] Test with `curl` after deploy | 部署后用 `curl` 测试

## ⚠️ Important caveats | 重要警告

**Public deployment is just that — public.** Anyone with the URL can view the data. Make sure the user wants this before deploying.
**公网部署就是公开的。** 任何有 URL 的人都能看到数据。部署前确认用户同意。

**Source archive is uploaded too.** When using `website_deploy`, both the built site and the source directory are saved. Don't include secrets in either.
**源文件也会上传。** 用 `website_deploy` 时，构建站点和源目录都会保存。两个都不要包含密钥。

## URL formats | URL 格式

| Pattern 模式 | Use Case 用途 |
|---|---|
| `https://xyz.space.mcode.cn` | Default Mavis-hosted deployment 默认 Mavis 部署 |
| `https://username.github.io/repo` | GitHub Pages (custom domain possible 支持自定义域名) |
| `https://project-name.vercel.app` | Vercel deployment Vercel 部署 |
| Local file:// | Offline / no internet 离线 / 无网 |

## When NOT to deploy | 何时不部署

- **English:** When the data is confidential or proprietary
  当数据是机密或专有时

- **中文：** 用户明确说"不要分享" / "保密"
  When the user explicitly says "don't share" / "keep private"

- **English:** When the dataset includes sensitive PII
  当数据集包含敏感 PII

- **中文：** 出版受限（如预发表）
  When the publication list is embargoed (e.g., pre-publication)

## Real-world examples from this skill | 本技能的真实案例

| Deployment 部署 | URL | Type 类型 |
|---|---|---|
| Yale × China (signatures) 耶鲁代表性论文 | `huhqumk08ghal.space.mcode.cn/signatures_funding.html` | Public XLSX sheet view 公网 XLSX 工作表视图 |
| Stanford × SJTU dashboard 斯坦福交大仪表板 | `d2qor2at6wdha.space.mcode.cn` | Bilingual EN+中文 |
| Stanford × SJTU offline 斯坦福交大离线 | `tf10itfi1x347.space.mcode.cn` | Self-contained + ZIP download 自包含 + ZIP 下载 |
| Yale consolidated report 耶鲁合并报告 | `7cgmihmr0q8ue.space.mcode.cn` | Single page 一页式 |
| Yale consolidated download 耶鲁合并下载 | `ie01qseh6o98f.space.mcode.cn` | Landing page + download 着陆页 + 下载 |