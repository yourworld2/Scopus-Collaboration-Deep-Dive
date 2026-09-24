# Page consolidation | 页面合并

> Combine multiple HTML pages into one comprehensive document.
> 将多个 HTML 页面合并成一个综合文档。

## When to use | 使用场景

- **English:** User has multiple analysis views (base + deep dive + signatures), says "merge" / "consolidate" / "合并" / "all in one"
  用户有多个分析视图（基础 + 深度 + 代表性），说"merge" / "合并" / "all in one"

- **中文：** 用户需要把多个分析页面合并成一个 URL 分享
  Want to share a complete report without multiple file URLs

- **English:** Need a single comprehensive document
  需要一份综合文档

## Pattern (7-step) | 7 步模式

```python
import re
from pathlib import Path

def extract_body(html):
    """Extract body content. | 提取 body 内容。"""
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL)
    return m.group(1).strip() if m else ''

def extract_style(html):
    """Extract style content. | 提取 style 内容。"""
    m = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    return m.group(1).strip() if m else ''

# 1. Read all pages / 读取所有页面
pages_html = []
for path in ['base.html', 'deep_dive.html', 'signatures.html']:
    pages_html.append(open(path).read())

# 2. Extract styles and bodies / 提取样式和内容
styles = [extract_style(p) for p in pages_html]
bodies = [extract_body(p) for p in pages_html]

# 3. Build unified CSS — use base style + add extras from others
#    构建统一样式 — 用基础样式 + 其他样式的额外部分
unified_style = styles[0]  # base style / 基础样式
for s in styles[1:]:
    # Add classes that don't exist in unified yet
    # 添加统一样式中还没有的类
    # (manual: identify extras and append)
    # (手动：识别额外部分并追加)
    pass

# 4. Strip duplicate <h1> and subtitle from each body
#    从每个 body 移除重复的 <h1> 和副标题
def remove_h1_subtitle(body):
    body = re.sub(r'<h1[^>]*>.*?</h1>', '', body, count=1, flags=re.DOTALL)
    body = re.sub(r'<div class="subtitle">.*?</div>', '', body, count=1, flags=re.DOTALL)
    return body

bodies = [remove_h1_subtitle(b) for b in bodies]

# 5. Add anchor IDs to top-level <h2>s
#    给顶层 <h2> 加锚点 ID
def add_anchor(body, anchors):
    for pattern, anchor_id in anchors:
        body = re.sub(pattern, f'<h2 id="{anchor_id}">', body, count=1)
    return body

# 6. Build consolidated HTML / 构建合并的 HTML
parts = ['<!DOCTYPE html><html><head><meta charset="UTF-8">']
parts.append('<title>Consolidated Report</title>')
parts.append('<style>' + unified_style + '</style>')
parts.append('</head><body>')

# Unified title / 统一标题
parts.append('<h1>Consolidated Report</h1>')
parts.append('<div class="subtitle">All pages merged</div>')

# TOC / 目录
parts.append('<div class="toc">')
parts.append('<h3>📑 Table of Contents</h3><ol>')
for anchor_id, label in toc_links:
    parts.append(f'<li><a href="#{anchor_id}">{label}</a></li>')
parts.append('</ol></div>')

# Each part with separator / 每个部分加分隔符
for i, (label, body) in enumerate(zip(part_labels, bodies)):
    if i > 0:
        parts.append('<hr class="part-divider">')
    parts.append(f'<h2 style="color: var(--accent);">{label}</h2>')
    parts.append(body)

parts.append('<div class="footer">Consolidated by Mavis</div>')
parts.append('</body></html>')

consolidated = '\n'.join(parts)
```

## Stylistic unification | 样式统一

Different pages may use slightly different colors / spacing. To unify:
不同页面可能用略有不同的颜色/间距。统一方法：

1. **Pick a primary color** — Yale's `#00356b` deep blue works well
   **选主色** — 耶鲁的 `#00356b` 深蓝就很好

2. **Pick an accent color** — `#bd5319` warm orange
   **选强调色** — `#bd5319` 暖橙

3. **Standardize font stack** — `-apple-system + PingFang SC + Microsoft YaHei`
   **统一字体栈** — 中英文都要照顾

4. **Container widths** — `max-width: 1280px` for full reports, `720px` for summaries
   **容器宽度** — 完整报告 1280px，摘要 720px

5. **Card border-lefts** — colored bar matching section context (blue/AI/med/etc.)
   **卡片左边色条** — 跟章节语境配色（蓝/AI/医学等）

## Real-world example: Yale complete report | 真实案例: 耶鲁完整报告

| Source 来源 | Size 大小 | Sheets 工作表 | Topic 主题 |
|---|---|---|---|
| `yale_china_collaboration_summary.html` | 33 KB | 5 | Base pipeline 基础流程 |
| `yale_china_deep_dive.html` | 36 KB | 6 | Deep dive 深度分析 |
| `yale_signatures_funding.html` | 28 KB | 7 | Signatures & funding 代表性论文与资助前瞻 |
| **Consolidated 合并后** | **86 KB** | **all 7** | **All-in-one 一站式** |

Output: `/workspace/analysis/yale_china_complete_report.html`

## Common issues | 常见问题

### Duplicate H1 after merge | 合并后 H1 重复

If you forget to strip `<h1>` from bodies, you'll have multiple H1s.
忘了从 body 移除 `<h1>` 就会多个 H1。

**Fix** 修复: Always run `remove_h1_subtitle()` on each body.
始终对每个 body 跑 `remove_h1_subtitle()`。

### Mismatched CSS selectors | CSS 选择器不匹配

Different pages may have different class names for the same concept.
不同页面对同一概念用不同的类名。

**Fix** 修复: Audit classes first, then add `unified` versions to the master style.
先审计类，然后把统一版本加到主样式。

### TOC links don't jump | TOC 链接不跳转

Anchors in H2s must match `href="#..."` exactly.
H2 里的锚点必须跟 `href="#..."` 完全匹配。

**Fix** 修复: Use `id="..."` attribute (not `name=""`), verify with `grep 'id='`.
用 `id="..."` 属性（不用 `name=""`），用 `grep 'id='` 验证。

### File gets too large | 文件太大

If 5+ pages combined, HTML exceeds 200 KB.
如果合并 5+ 页面，HTML 会超过 200 KB。

**Fix** 修复: Either split back into 2-3 page sets, or use ZIP distribution.
要么拆回 2-3 页，要么用 ZIP 分发。

```python
if len(consolidated) > 200_000:
    print('Warning: HTML > 200 KB, consider ZIP distribution')
    print('警告: HTML > 200 KB，考虑 ZIP 分发')
```