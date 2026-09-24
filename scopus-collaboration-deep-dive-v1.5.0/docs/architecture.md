# Architecture | 架构

> How `scopus-collaboration-deep-dive` works internally.
> `scopus-collaboration-deep-dive` 内部如何工作。

## High-level flow | 整体流程

```
Scopus CSV/XLSX
    ↓
1. Header detection (skiprows=18-21) | 头部检测
    ↓
2. Author-count filter (if >30% papers have >50 authors)
   作者数过滤（如果 >30% 论文有 >50 作者）
    ↓
3. Paper cache (list of dicts) | 论文缓存
    ↓
4. Compute 10 base topics | 计算 10 个基础主题
    ↓
5. Compute 4 deep-dive topics (optional) | 计算 4 个深度主题（可选）
    ↓
6. Build XLSX XML manually (live formulas) | 手动构建 XLSX XML（活公式）
    ↓
7. xlsx_pack.py → package as XLSX | 打包为 XLSX
    ↓
8. LibreOffice convert (resolves non-sequential rIds)
   LibreOffice 转换（解决 rId 顺序问题）
    ↓
9. Build HTML dashboard (bilingual) | 构建双语 HTML 仪表板
    ↓
10. (Optional) consolidate multiple pages | 合并多页（可选）
    ↓
11. (Optional) website_deploy → public URL | 部署为公网 URL（可选）
```

## Layered design | 分层设计

```
┌──────────────────────────────────────────────────────────┐
│ Skill entry point (SKILL.md — AI consumption)            │
│ 技能入口（SKILL.md — AI 使用）                            │
└──────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│ 10-topic base pipeline (always run)                      │
│ 10 主题基础流程（始终运行）                                │
│   - 5 sheet XLSX                                          │
│   - HTML dashboard                                        │
└──────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│ 4 deep-dive topics (run on request)                      │
│ 4 深度主题（按需运行）                                    │
│   - + Sheet 6 (Deep Dive)                                │
│   - + Sheet 7 (Signatures & Funding)                     │
└──────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│ Reusable scripts/ | 可复用的脚本                          │
│   - filters.py                                           │
│   - region_classifier.py                                 │
│   - clusters.py                                          │
│   - bilingual.py                                         │
│   - html_builder.py |  HTML 构造函数 (NEW v1.4)         │
│   - deploy.py        |  部署助手 (NEW v1.4)              │
│   - build_xlsx.py (CLI entry point) | 命令行入口         │
└──────────────────────────────────────────────────────────┘
```

## Author-count filter rationale | 作者数过滤原理

Scopus exports often include physics consortium papers (ATLAS, CMS, LHCb) and Global Burden of Disease medical cohorts that have hundreds or thousands of co-authors. These papers:
Scopus 导出经常包含物理联盟论文（ATLAS、CMS、LHCb）和全球疾病负担医疗队列论文，这些论文有数百或数千名共同作者：

- Appear at the top of every metric (FWCI, citations, etc.) 出现在每个指标的顶部
- Are not actually bilateral collaborations 实际不是真正的双边合作
- Skew researcher counts (one "consortium paper" may have 3,000 authors) 扭曲研究者计数（一篇"联盟论文"可能有 3,000 名作者）
- Inflate paper counts by 50-60% 论文数虚增 50-60%

**Solution 解决方案:** Filter papers to ≤50 authors. After filtering:
过滤作者数 ≤50 的论文。过滤后：

| Metric 指标 | Before 前 | After 后 | Change 变化 |
|---|---:|---:|---|
| Papers 论文数 | 1,174 | 456 | -61% |
| Avg FWCI 平均 FWCI | 8.85 | 2.79 | -68% (now realistic 现已合理) |
| Max FWCI 最大 FWCI | 927 | 67 | -93% (outliers removed 异常值已移除) |
| Top field 最高领域 | Physics | CS / AI | **Real research focus 真实研究焦点** |

## Region classifier v3 design | v3 区域分类器设计

The earlier v1/v2 classifiers used abbreviations (`"MIT"`, `"NUS"`) which miss many real Scopus entries. v3 uses **explicit full-name matching**:
之前的 v1/v2 分类器用缩写（`"MIT"`、`"NUS"`），漏掉很多实际 Scopus 条目。v3 用**显式全名匹配**：

```python
KEYWORD_RULES = {
    'US (other top)': lambda nm: any(k in nm for k in [
        'massachusetts institute of technology',  # 不只是 "MIT"
        'harvard', 'university of california',
        'columbia', 'cornell', 'yale', ...
    ]),
    ...
}
```

This catches institutions Scopus writes as:
这能匹配 Scopus 的多种写法：

- "Massachusetts Institute of Technology" ✓
- "MIT Computer Science and Artificial Intelligence Laboratory" ✓
- "MIT, Department of Biology" ✓

## XLSX construction approach | XLSX 构建方法

We don't use `openpyxl.write()` directly because:
我们不直接用 `openpyxl.write()`，因为：

1. **Live formulas**: openpyxl can write formulas but not always parse them back
   **活公式**: openpyxl 能写公式但不一定能解析回来
2. **Non-sequential rIds**: openpyxl-created XLSX often breaks in LibreOffice
   **rId 顺序问题**: openpyxl 创建的 XLSX 在 LibreOffice 经常坏
3. **Color/style precision**: We need exact cell-by-cell color control (blue=input, black=formula, green=cross-sheet)
   **颜色/样式精度**: 我们需要逐格的精确颜色控制

**Pattern 模式:** Build XLSX XML directly, then post-process with LibreOffice:
直接构建 XLSX XML，然后用 LibreOffice 后处理：

```python
# 1. Build XML | 构建 XML
import openpyxl
wb = openpyxl.Workbook()
# ... add sheets, formulas, styles
wb.save('/tmp/build.xlsx')

# 2. Pack (using minimax-xlsx skill) | 打包
python xlsx_pack.py /tmp/build.xlsx /tmp/final.xlsx

# 3. LibreOffice convert (fixes rIds) | 转换
libreoffice --headless --convert-to xlsx /tmp/final.xlsx --outdir /tmp/

# 4. Copy back | 复制回去
cp /tmp/final.xlsx ./output.xlsx
```

## Bilingual architecture | 双语架构

Two patterns based on deliverable:
根据交付物不同有两种模式：

**HTML** — toggleable visibility (default-zh pattern):
HTML — 切换可见性（默认中文模式）：

```html
<div class="lang-zh"><!-- 默认可见 --></div>
<div class="lang-en"><!-- 默认隐藏 --></div>
```
```css
.lang-en { display: none; }
body.show-en .lang-zh { display: none; }
body.show-en .lang-en { display: block; }
```

**XLSX** — single column, both languages:
XLSX — 单列双语：

```
English | 中文
Total Papers | 总论文数
```

Why this pattern: XLSX doesn't natively support per-cell language toggle, so a single column with both languages is the cleanest approach.
为什么用这个模式：XLSX 本身不支持单元格级语言切换，所以单列双语是最简洁的方案。

## Deployment options | 部署选项

| Need 需求 | Solution 解决方案 |
|---|---|
| Quick share 快速分享 | `website_deploy` → `https://xyz.space.mcode.cn` |
| Download link 下载链接 | HTML with landing page (see `scripts/deploy.py`) |
| Offline viewing 离线查看 | Self-contained HTML with embedded data + XLSX |
| Mass distribution 批量分发 | ZIP bundle with HTML + XLSX + JSON |
| Email-ready 邮件分享 | Small XLSX only (single sheet) |

See `scripts/deploy.py` for the deployment helper.
部署助手见 `scripts/deploy.py`。

## Performance | 性能

| Phase 阶段 | Time 时间 | Notes 备注 |
|---|---|---|
| CSV parsing CSV 解析 | <1s | pandas |
| Author filter 作者过滤 | <1s | vectorized 向量化 |
| Paper cache 论文缓存 | <1s | dict construction |
| 10 topics 10 主题 | ~5s | mostly pandas operations |
| 4 deep-dive topics 4 深度主题 | ~3s | AI cluster + H-index |
| XLSX build 构建 | ~10s | XML construction |
| LibreOffice convert 转换 | ~20s | headless conversion |
| HTML build 构建 | ~1s | string templates |
| **Total (default 5 sheets) 默认 5 工作表** | **~40s** | |
| **Total (full 7 sheets + bilingual HTML) 完整 7 工作表 + 双语** | **~2min** | |

## Validation | 验证

After each run, verify:
每次运行后验证：

```bash
# 1. XLSX opens and formulas calculate | XLSX 能打开且公式计算
libreoffice --headless --calc --convert-to xlsx output.xlsx

# 2. HTML renders both languages | HTML 两种语言都能渲染
python3 -c "
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('output.html').read())
zh = soup.find('div', class_='lang-zh')
en = soup.find('div', class_='lang-en')
assert len(zh.text) > 1000, 'lang-zh content too small | lang-zh 内容太少'
assert len(en.text) > 1000, 'lang-en content too small | lang-en 内容太少'
print('✓ Both languages have substantial content')
print('✓ 两种语言都有实质内容')
"
```