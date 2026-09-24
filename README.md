# Scopus Collaboration Deep Dive
# Scopus 合作深度挖掘

> Analyze a Scopus CSV export of one university's co-authorship papers with a target region and produce a multi-sheet XLSX with live formulas + a bilingual HTML dashboard.
> 分析某大学与目标地区的 Scopus 合著者论文 CSV 导出，生成多工作表活公式 XLSX + 双语 HTML 仪表板。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Mavis Skill](https://img.shields.io/badge/Mavis-skill-blueviolet)](SKILL.md)
[![Examples](https://img.shields.io/badge/examples-3-success)](#examples)
[![Version](https://img.shields.io/badge/version-1.5.0-blue)](#changelog)

## ✨ What it does | 功能

Turn a Scopus export like `yale_china_2022_2026.csv` into:
把 Scopus 导出转成：

- **5-sheet XLSX** (default) or **7-sheet XLSX** (extended) with **live formulas** — no hardcoded ratios
  **5/7 工作表活公式 XLSX** —— 无硬编码比例
- **Bilingual HTML dashboard** (English + 中文) with toggle button — works even with JS disabled
  **双语 HTML 仪表板** —— 即使 JS 禁用也能显示
- **Single consolidated HTML** combining multiple analysis views
  **单页合并 HTML** —— 多视图合一
- **Public deployment** to `space.mcode.cn` URLs (dashboard or download link)
  **公网部署** —— 仪表板或下载链接
- **ZIP bundle** for offline distribution
  **ZIP 包** —— 离线分发

All in ~2 minutes, no manual data wrangling.
约 2 分钟，无需手动数据处理。

## 🚀 Quick start | 快速开始

### As a Mavis skill | 作为 Mavis 技能

The skill auto-loads for relevant tasks. Just describe what you want:
技能自动加载相关任务。直接描述需求：

```
"分析 Yale × 中国高校 2022-2026 合作情况"
"Analyze Stanford × Shanghai Jiao Tong co-authorship data"
```

### Standalone Python usage | 独立 Python 使用

```bash
# Install | 安装
pip install -r requirements.txt

# Run on a Scopus CSV | 在 Scopus CSV 上运行
python scripts/build_xlsx.py \
    --csv path/to/scopus_export.csv \
    --source "Yale" \
    --target "China" \
    --output ./output

# Deploy output as public download link | 部署为公网下载链接
python -c "
from scripts.deploy import deploy_download
deploy_download('./output.html', 'My Analysis')
"

# Consolidate multiple pages into one | 多页合并为一页
python -c "
from scripts.html_builder import consolidate_pages
print(consolidate_pages([...]))
"
```

## 📊 What you get | 输出

### XLSX structure (default base = 5 sheets) | XLSX 结构 (默认 5 工作表)

| Sheet 工作表 | Content 内容 |
|---|---|
| Overview 概览 | Total stats, year window, top journal |
| Top 20 Partner Institutions Top 20 合作机构 | With live share formulas |
| Top 10 Research Fields Top 10 研究领域 | With FWCI averages |
| Top 10 Researchers Top 10 研究者 | Primary institution + core field enrichment |
| Trends & Patterns 趋势与模式 | YoY trends, topic evolution, HHI, region, archetypes, journals + Funding |

### Extended (7 sheets, on request) | 扩展 (7 工作表，按需)

| Sheet 工作表 | Content 内容 |
|---|---|
| Deep Dive 深度分析 | ASJC major categories (5 buckets), AI cluster detection, H-index, multi-region partnership profile |
| Signatures & Funding 代表性论文与资助 | Top 1%/5%/10% papers, multi-sector collaboration, OA status, document types |

### HTML dashboard | HTML 仪表板

- Bilingual EN/中文 toggle (default-zh pattern — works even with JS disabled)
  双语 EN/中文 切换（默认中文 —— JS 禁用也能用）
- Self-contained (no external CDN/fonts) | 自包含
- Embedded data option (offline-ready, single file) | 嵌入数据离线可用
- Includes XLSX download button | 含 XLSX 下载按钮
- Deployable to public URL | 可公网部署

## 🚨 Critical: Author-count filter | 关键: 作者数过滤

> If >30% of papers have >50 authors, apply the filter to remove mega-author consortium papers (ATLAS/CMS/GBD).
> 如果 >30% 论文有 >50 作者，过滤掉大型联盟论文（ATLAS/CMS/GBD）。

```python
from scripts.filters import should_apply_filter, apply_author_filter

if should_apply_filter(df, threshold_pct=30.0):
    df, _ = apply_author_filter(df, max_authors=50)
```

**Real impact on Stanford × SJTU:** **对斯坦福 × SJTU 实际影响:**
- 1,174 papers → 456 papers (61% removed) | 论文 1,174 → 456（移除 61%）
- Avg FWCI: 8.85 → 2.79 (still high but no longer dominated by ATLAS/CMS) | 平均 FWCI: 8.85 → 2.79

## 📋 Features | 特性

- **Author-count filter** | 作者数过滤 — automatically detects & removes consortium papers
- **Region classifier v3** | v3 区域分类器 — handles 50+ US/international university names explicitly
- **Bilingual labels** | 双语标签 — single XLSX column with `English | 中文` format
- **Live formulas** | 活公式 — all percentages are computed by Excel, not pre-baked
- **HTML builder with default-zh pattern** | 默认中文 HTML 构造函数 — pages render even with JS broken
- **Page consolidation** | 页面合并 — merge multiple views into one comprehensive HTML
- **Public deployment** | 公网部署 — `deploy.py` with 3 patterns (dashboard / download / ZIP)
- **Production-tested** | 生产验证 — used in 3 real-world cases

## 📦 Examples | 示例

- [examples/yale-china/](examples/yale-china/) — 2,664 papers, 7 sheets, 318 formulas
- [examples/stanford-sjtu/](examples/stanford-sjtu/) — 456 papers (after filter), 7 sheets, 56 formulas, bilingual EN+中文
- [examples/yale-china-complete/](examples/yale-china-complete/) — 3 pages → 1 consolidated page, 86 KB

## 🛠️ Tech stack | 技术栈

- Python 3.10+
- pandas — CSV parsing & analysis | CSV 解析分析
- openpyxl + custom XML — XLSX construction | XLSX 构建
- LibreOffice headless — post-process (fixes non-sequential rIds) | 后处理
- Standard library — XML, json
- Mavis `website_deploy` — public deployment | 公网部署

## 🤝 Contributing | 贡献

See [CONTRIBUTING.md](CONTRIBUTING.md). Most useful contributions:
最有用贡献：

- New region classifier rules for other countries | 其他国家新分类规则
- New cluster patterns (life sciences, physics, etc.) | 新集群模式
- New pattern templates (citation lag, topic shift, etc.) | 新模式模板
- Translation corrections in bilingual labels | 双语标签翻译纠正
- New HTML builder patterns | 新 HTML 模式

## 📝 License | 许可

MIT — see [LICENSE](LICENSE).

## 📚 Documentation | 文档

- [SKILL.md](SKILL.md) — main skill specification (for Mavis AI consumption) | 主技能规范
- [docs/architecture.md](docs/architecture.md) — how it works internally | 内部架构
- [docs/bilingual.md](docs/bilingual.md) — adding bilingual output to new regions | 添加新语言
- [docs/deployment.md](docs/deployment.md) — how to deploy publicly | 部署指南
- [docs/html-pitfalls.md](docs/html-pitfalls.md) — HTML generation gotchas (NEW v1.4) | HTML 陷阱
- [docs/consolidation.md](docs/consolidation.md) — page consolidation pattern (NEW v1.4) | 页面合并
- [references/analysis-cookbook.md](references/analysis-cookbook.md) — 16 reusable code snippets | 16 个代码片段
- [CHANGELOG.md](CHANGELOG.md) — version history | 版本历史

## 👤 Author | 作者

Built by **Mavis** (Mavis Agent team), Sep 2026.
由 **Mavis**（Mavis Agent 团队）于 2026 年 9 月构建。

Validated on Yale × Chinese Universities (2,664 papers) and Stanford × SJTU (456 papers after filter).
在耶鲁 × 中国大学（2,664 篇论文）和斯坦福 × SJTU（过滤后 456 篇）上验证。

## 📊 Stats | 性能指标

- 5-sheet XLSX: ~10 seconds | 5 工作表 XLSX: 约 10 秒
- 7-sheet XLSX + bilingual HTML: ~2 minutes | 7 工作表 + 双语 HTML: 约 2 分钟
- 100% formula coverage on derived metrics (no hardcoded ratios) | 派生指标 100% 公式覆盖
- 0 formula errors on all validation runs | 所有验证运行 0 公式错误
