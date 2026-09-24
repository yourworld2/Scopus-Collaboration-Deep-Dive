# Yale × China — Complete Consolidated Report
# 耶鲁 × 中国 — 完整合并报告

**Real-world example** of consolidating 3 separate analysis HTML pages into a single comprehensive report.
**真实世界示例** — 将 3 个独立的分析 HTML 页面合并为单个综合报告。

## Source pages / 源页面

| Source 来源 | Size 大小 | Sheets 工作表 | Topic 主题 |
|---|---|---|---|
| `yale_china_collaboration_summary.html` | 33 KB | 1-5 | Base pipeline (overview, top 20, fields, researchers, trends) |
| `yale_china_deep_dive.html` | 36 KB | 6 | AI cluster, ASJC categories, H-index, US-China position |
| `yale_signatures_funding.html` | 28 KB | 7 | Cluster signatures, funding horizon proxies |

## Consolidated output / 合并后的输出

`yale_china_complete_report.html` (86 KB) — single file containing all 3 reports with:
单个文件包含所有 3 个报告，含：

- **Unified title** / 统一标题 + subtitle 副标题
- **Table of contents** / 目录 with anchor links to 11 sections
- **CSS unification** / CSS 统一 (Yale's blue + orange accent colors)
- **Cross-part dividers** / 部分分隔符 (`<hr class="part-divider">`)
- **Unified footer** / 统一页脚 documenting the consolidation

## How to reproduce / 如何复现

```python
import re
from pathlib import Path

def extract_body(html):
    return re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL).group(1).strip()

def extract_style(html):
    return re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL).group(1).strip()

# 1. Read source pages / 读取源页面
pages = []
for path in ['yale_china_collaboration_summary.html',
             'yale_china_deep_dive.html',
             'yale_signatures_funding.html']:
    content = Path(path).read_text(encoding='utf-8')
    pages.append({
        'body': extract_body(content),
        'style': extract_style(content),
    })

# 2. Unified style (use base + append extras) / 统一样式
unified_style = pages[0]['style']
unified_style += '''
  /* Deep dive extras / 深度分析额外样式 */
  .badge-ai { background: #7c3aed; color: white; }
  ...
'''

# 3. Build consolidated / 构建合并文档
# ... (see docs/consolidation.md for full pattern)
# ... (完整模式见 docs/consolidation.md)
```

## Key features / 主要特性

- ✅ TOC navigation across 11 sections / 11 个章节的目录导航
- ✅ All anchors work (`href="#sec-..."` matches `<h2 id="sec-...">`) / 所有锚点工作正常
- ✅ 15 tables 表格, 14 H2 sections 主章节, 46 H3 subsections 子章节
- ✅ 21 insight cards 洞察卡, 193 rank badges 排名徽章
- ✅ Single file, ~86 KB, no external dependencies / 无外部依赖

## What it shows about the skill / 这个示例展示了什么

This is the **page consolidation pattern** in action — useful when:
这是**页面合并模式**的实际应用 — 在以下场景有用：

- **在以下场景有用**：当你有 3 个独立的视图，想要一个 URL 分享
- **想要完整报告**：避免多个文件链接
- **需要一站式文档**：把所有内容放在一个文档里

See `docs/consolidation.md` for the full pattern reference.
完整模式参考见 `docs/consolidation.md`。