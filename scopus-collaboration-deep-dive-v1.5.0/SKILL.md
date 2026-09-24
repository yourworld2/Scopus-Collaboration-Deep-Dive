---
name: scopus-collaboration-deep-dive
version: 1.5.0
description: Analyze a Scopus CSV export of one university's co-authorship papers with a target region and produce a multi-sheet XLSX with live formulas + a bilingual HTML dashboard. | 分析某大学与目标地区的 Scopus 合著者论文 CSV 导出，生成多工作表活公式 XLSX + 双语 HTML 仪表板。Use when the user uploads a Scopus CSV/XLSX and asks to "analyze collaborations", "compare partner universities", "identify research clusters", "rank researchers", "trend analysis", "deep dive", or wants a bibliometric partnership report. Do NOT use for: single-paper summarization, full Scopus search/exports, journal-impact-factor queries, or general XLSX building.
github_url: https://github.com/minimax/scopus-collaboration-deep-dive
license: MIT
authors:
  - name: Mavis Agent Team
    email: support@mavis.ai
keywords:
  - bibliometric | 文献计量
  - scopus | Scopus
  - collaboration | 合作分析
  - h-index | H 指数
  - FWCI | 学科归一化引用
  - ASJC | 学科分类
  - XLSX | Excel
  - bilingual | 双语
  - research-analytics | 研究分析
  - offline-html | 离线 HTML
  - page-consolidation | 页面合并
  - public-deployment | 公网部署
---

# scopus-collaboration-deep-dive | Scopus 合作深度挖掘

> A skill that turns a Scopus CSV export into a 5-7 sheet XLSX with live formulas + bilingual HTML dashboard, with optional consolidation and public deployment.
> 把 Scopus CSV 导出转成 5-7 工作表活公式 XLSX + 双语 HTML 仪表板，可选合并与公网部署。

## 🎯 When to use | 使用场景

User uploads a Scopus CSV/XLSX export and asks any of:
用户上传 Scopus CSV/XLSX 导出并询问：

- "Analyze collaborations" / "compare partner universities" | "分析合作" / "比较合作机构"
- "Identify research clusters" / "rank researchers" | "识别研究集群" / "研究者排名"
- "Trend analysis" / "deep dive" / "detailed report" | "趋势分析" / "深度分析" / "详细报告"
- "Bilateral cooperation" / "who are they working with" | "双边合作" / "合作对象"

**Auto-trigger** for any Scopus CSV/XLSX upload (don't ask first — just run the base pipeline).
**自动触发** 任何 Scopus CSV/XLSX 上传（不用先问 —— 直接跑基础流程）。

**Ask first** before:
**部署前先确认** 关于：

- Public deployment to `space.mcode.cn` | 公网部署
- Deep-dive Sheet 6/7 | 深度工作表
- Consolidating multiple pages into one HTML | 合并多页为一个 HTML

## 🚦 Decision matrix | 决策矩阵

| Trigger 触发条件 | Action 操作 |
|---|---|
| Scopus CSV/XLSX uploaded | Auto-run 5-sheet base pipeline |
| User says "deep dive" / "all topics" | Add Sheets 6 (Deep Dive) + 7 (Signatures & Funding) |
| User says "publish" / "deploy" / "link" | Ask confirmation, then `website_deploy` |
| User says "bilingual" / "中文" / "EN+ZH" | Add bilingual EN+中文 labels |
| User says "offline" / "no internet" | Generate self-contained HTML package |
| User says "consolidate" / "合并" / "merge pages" | Run consolidation pipeline |
| User asks for a "download link" | Deploy as public URL with HTML download |

## 📋 The 10-topic base pipeline | 10 主题基础流程

Default 5-sheet XLSX covers these 10 topics:
默认 5 工作表 XLSX 覆盖这 10 个主题：

1. **Overview** | 概览 — totals, year window, top journal
2. **Top 20 Partner Institutions** | Top 20 合作机构 — with live share formulas
3. **Top 10 Research Fields** | Top 10 研究领域 — FWCI averages
4. **Top 10 Researchers** | Top 10 研究者 — primary institution + core field enrichment
5. **Trends & Patterns** | 趋势与模式 — YoY trends, topic evolution, HHI concentration, region breakdown, 3 archetypes, top journals + Funding Horizon proxies

Extended 7-sheet adds:
扩展 7 工作表新增：

6. **Deep Dive** | 深度分析 — ASJC major categories (5 buckets), AI cluster, H-index, multi-region profile
7. **Signatures & Funding** | 代表性论文与资助 — Top 1%/5%/10%, multi-sector, OA, document types

## 🚨 Critical: Author-count filter | 关键: 作者数过滤

> **Always check whether the dataset is dominated by consortium papers before processing.**
> **处理前务必检查数据集是否被联盟论文主导。**

If >30% of papers have >50 authors, the dataset is dominated by mega-author consortium papers (ATLAS/CMS/LHCb physics, GBD medical cohorts). These inflate all metrics and obscure real bilateral collaboration patterns.
如果 >30% 论文有 >50 作者，数据集被大型联盟论文主导（ATLAS/CMS/LHCb 物理，GBD 医疗队列）。这些论文抬高所有指标，模糊真正的双边合作模式。

**Apply filter 应用过滤:**
```python
from filters import apply_author_filter, should_apply_filter

if should_apply_filter(df, threshold_pct=30.0):
    df_filtered, _ = apply_author_filter(df, max_authors=50)
```

**Real impact on Stanford × SJTU (2022-2026):**
**对斯坦福 × SJTU (2022-2026) 的实际影响:**

- 1,174 papers → 456 papers (61% removed) | 论文 1,174 → 456（移除 61%）
- Avg FWCI: 8.85 → 2.79 (still high but no longer dominated by ATLAS/CMS) | 平均 FWCI: 8.85 → 2.79
- Max FWCI: 927 → 67 (real outliers surface) | 最大 FWCI: 927 → 67

## 🌍 Region classifier v3 | v3 区域分类器

Maps each institution name to one of 14 categories (see `scripts/region_classifier.py`):
将每个机构名称映射到 14 个分类之一：

- Stanford (source) / Yale (source) — match your target source | 匹配你的源学校
- Shanghai Jiao Tong (target) / China (target) — match your target region | 匹配你的目标区域
- Mainland China | 中国大陆
- Hong Kong / Macau / Taiwan | 港澳台
- US (Federal/DOE), US (National Labs), US (other top) | 美国联邦/国家实验室/其他顶级
- Germany / Switzerland, UK, Singapore, Japan, Korea | 德/瑞、英、新、日、韩
- Europe (physics labs), Other International | 欧洲物理实验室、其他国际

**Why explicit full-name matching 为什么用全名匹配:** Scopus writes institution names in varied forms (e.g., "Massachusetts Institute of Technology" vs "MIT"). v3 uses full-name patterns for 50+ US/international universities.
Scopus 机构名写法多样（如 "Massachusetts Institute of Technology" vs "MIT"）。v3 用全名模式覆盖 50+ 美/国际大学。

## 🌐 Bilingual output | 双语输出

**HTML — use the default-zh CSS pattern (NOT both-hidden + JS-toggle):**
**HTML — 用默认中文 CSS 模式（不要双隐 + JS 切换）：**

```html
<div class="lang-zh">中文内容 (visible by default) | 默认可见</div>
<div class="lang-en">English content (hidden by default) | 默认隐藏</div>
```

```css
.lang-en { display: none; }                      /* EN hidden by default */
body.show-en .lang-zh { display: none; }         /* switch to EN */
body.show-en .lang-en { display: block; }
```

```javascript
function setLang(lang) {
    document.body.className = '';
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
    if (lang === 'en') document.body.classList.add('show-en');
    // Chinese is default visible — no class needed
    // 中文默认可见 —— 无需 class
}
```

**Why this pattern (vs both-hidden + JS):** If JS fails or className doesn't propagate, the previous pattern (both `display: none`) leaves the page empty. The new pattern has Chinese visible by default — works even with JS broken.
**为什么用这个模式（旧模式问题）:** 如果 JS 不跑或 className 没生效，旧模式两个 div 都 `display: none`，页面就空了。新模式中文默认可见 —— 即使 JS 坏掉也行。

**XLSX**: Single column with `English | 中文` labels:
**XLSX**: 单列双语标签：

```
Total Papers | 总论文数
```

## 📄 Page consolidation pattern | 页面合并模式

When the user has multiple analysis pages (e.g., a base summary + deep dive + signatures), consolidate them into a single HTML document:
当用户有多个分析页面（如基础汇总 + 深度 + 代表性），合并成单个 HTML：

1. Read each HTML file's `<style>` and `<body>` separately
   分别读取每个 HTML 的 `<style>` 和 `<body>`
2. Merge all CSS (watch for duplicate selectors — keep base + add extras from others)
   合并所有 CSS（注意重复选择器 —— 保留基础 + 添加其他额外）
3. Strip duplicate `<h1>` and subtitle (use unified title)
   去掉重复 `<h1>` 和副标题（用统一标题）
4. Add anchor IDs to top-level `<h2>` for TOC navigation
   给顶层 `<h2>` 加锚点 ID 用于目录跳转
5. Insert a table-of-contents div with anchor links at the top
   在顶部插入目录 div 配锚点链接
6. Add separator `<hr>` between parts
   部分间加 `<hr>` 分隔符
7. Add a unified footer noting the consolidation
   加统一页脚说明合并

Reference implementation: see `examples/yale-china-complete/` (3 pages → 1 page, 86 KB output).
参考实现：见 `examples/yale-china-complete/`（3 页 → 1 页，86 KB 输出）。

## 🚀 Public deployment + download link | 公网部署 + 下载链接

Three patterns to share outputs:
三种分享模式：

**Pattern 1: Public dashboard via website_deploy**
**模式 1: 公网仪表板**
```python
website_deploy(
    path="/tmp/share",                # dir with index.html
    source_path="/tmp/share",
    project_name="Yale × China 2022-2026"
)
# Returns: https://xyz.space.mcode.cn
```

**Pattern 2: Download link with landing page**
**模式 2: 着陆页 + 下载链接**
```bash
mkdir -p /workspace/analysis/download_site
cp analysis.html /workspace/analysis/download_site/
cat > /workspace/analysis/download_site/index.html <<'EOF'
<!-- landing with link to ./analysis.html -->
EOF
website_deploy(path="/workspace/analysis/download_site", ...)
```

Or use the helper:
或用助手：
```python
from scripts.deploy import deploy_download
deploy_download(html_path='./analysis.html', project_name='My Report')
```

**Pattern 3: ZIP bundle for offline distribution**
**模式 3: 离线 ZIP 包**
```bash
mkdir -p /workspace/analysis/bundle
cp analysis.html analysis.xlsx *.json /workspace/analysis/bundle/
zip -r /workspace/analysis/bundle.zip /workspace/analysis/bundle/
```

Or:
```python
from scripts.deploy import deploy_zip_bundle
deploy_zip_bundle(file_paths=['./analysis.html'], project_name='My Report')
```

**Verification after deploy 部署后验证:** `curl -s -w "Status: %{http_code}, Size: %{size_download}\n" URL`

## ⚠️ HTML generation pitfalls (lessons learned) | HTML 生成陷阱

| Pitfall 陷阱 | Solution 解决方案 |
|---|---|
| `f"..."` with `}}` literal braces \| f-string 字面 `}}` | Use string concatenation `'\n'.join([...])` instead \| 用字符串拼接代替 |
| `display: none` on both lang divs + JS toggle \| 双隐 + JS 切换 | Default ONE lang visible (no JS needed) \| 默认一种语言可见 |
| Spaces in `class="rank"` causing attribute error \| 计数 `class="rank"` 反斜杠错误 | Use `q1 = 'class="rank'` with `count(q1)` \| 用变量存搜索串 |
| Empty rendered page \| 渲染空白页 | Verify lang-zh div has content; check CSS rule fires \| 验证 lang-zh 内容 |
| External CDN/font dependency \| 外部 CDN/字体依赖 | Use system fonts only \| 只用系统字体 |
| Embedded data exceeds 200 KB \| 嵌入数据超 200 KB | Use ZIP bundle pattern for big datasets \| 大数据集用 ZIP 包 |

## 🛠️ Tech stack | 技术栈

- Python 3.10+
- pandas — CSV parsing & analysis | CSV 解析分析
- openpyxl + custom XML — XLSX construction | XLSX 构建
- LibreOffice headless — post-process (fixes non-sequential rIds) | 后处理
- Standard library — XML, json
- Mavis `website_deploy` — public deployment | 公网部署

## ⚙️ Implementation pattern | 实现模式

For full production implementation see the minimax-xlsx skill. The standalone scripts in `scripts/` provide working reference implementations:
完整生产实现见 minimax-xlsx 技能。`scripts/` 提供可工作的参考实现：

```bash
python scripts/build_xlsx.py --csv path/to/scopus.csv \
    --source "Yale" --target "China" --output ./output
```

For full XLSX + HTML, use the production workflow:
完整 XLSX + HTML 生产流程：

1. Read CSV with `pd.read_csv(skiprows=18)` (or 19/20/21)
2. Apply `apply_author_filter(df, max_authors=50)` if >30% are consortium
3. Build paper cache (list of dicts)
4. Compute 10 base topics + (optional) 4 deep-dive topics
5. Build XLSX XML manually (formula-by-formula) using minimax-xlsx pattern
6. `xlsx_pack.py` to package
7. LibreOffice convert for final XLSX
8. Build HTML dashboard with bilingual toggle (use the safer CSS pattern)
9. Optional: consolidate multiple pages
10. Optional: `website_deploy` for public URL

## 📊 Insight patterns | 洞察模式

8 reusable patterns (each producing 1+ table or chart):
8 个可复用模式（每个产出 1+ 表格或图表）：

1. **Top 20 partner institutions** with concentration (HHI) | 合作机构 Top 20 + HHI
2. **YoY trends** with year-over-year growth | 同比趋势
4. **Topic evolution** by year | 主题年度演变
5. **Region breakdown** with international collaboration profile | 区域分布
6. **Researcher archetypes** (Superstar/Specialist/Workhorse) | 研究者原型
7. **Top 20 high-impact journals** | Top 20 高影响期刊
8. **Funding Horizon proxies** (Top 1%/5%/10% papers, OA, multi-sector) | 资助前瞻
9. **Multi-region partnership** profile (200 papers = bilateral + US) | 多区域合作
10. **AI cluster detection** by Chinese surname pattern | AI 集群检测
11. **Consortium signature** (FWCI >100 flag for physics papers) | 联盟特征

## 📚 Reference documentation | 参考文档

- `references/analysis-cookbook.md` — 16 reusable code snippets | 16 个代码片段
- `docs/architecture.md` — internal architecture | 内部架构
- `docs/bilingual.md` — adding bilingual to new regions | 添加新语言
- `docs/deployment.md` — public deployment guide | 部署指南
- `docs/html-pitfalls.md` — HTML generation gotchas (NEW v1.4) | HTML 陷阱
- `docs/consolidation.md` — page consolidation pattern (NEW v1.4) | 页面合并
- Examples: `examples/yale-china/`, `examples/stanford-sjtu/`, `examples/yale-china-complete/` (NEW v1.4)

## ✅ Validation | 验证

Self-validation patterns:
自验证模式：

- Open XLSX in LibreOffice — verify all formulas calculate | XLSX 公式能算
- Open HTML in browser — verify both languages toggle (test with JS disabled) | 双语切换
- Check FWCI distribution — verify not skewed by single mega-paper | FWCI 分布
- Verify `should_apply_filter()` triggers correctly on ATLAS/CMS datasets | 过滤器触发
- Check HTML renders even when JS is disabled (lang-zh visible by default) | 关 JS 也能渲染

## 📝 Changelog | 变更日志

See [CHANGELOG.md](CHANGELOG.md).

## 📝 License | 许可

MIT — see [LICENSE](LICENSE).

## 👤 Author | 作者

Mavis Agent team, Sep 2026. Inspired by real-world bibliometric consulting work.
灵感来自真实的文献计量咨询工作。