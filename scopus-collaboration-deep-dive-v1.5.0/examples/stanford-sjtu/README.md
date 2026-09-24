# Stanford × Shanghai Jiao Tong University (2022-2026)
# 斯坦福 × 上海交通大学 (2022-2026)

**Real-world validation case** with author-count filtering and bilingual output.
**真实世界验证案例** — 含作者数过滤和双语输出。

## Dataset / 数据集

- **Source / 数据源**: Scopus CSV export, "Publications at Stanford University 2022-2026"
- **Target / 目标**: Shanghai Jiao Tong University
- **Filter / 过滤**: ≤50 authors applied (61% papers removed — dominated by ATLAS/CMS/GBD)
- **Total papers / 总论文数**: 1,174 (raw) → 456 (filtered to bilateral Stanford-SJTU co-authors)
- **Year range / 年份范围**: 2022-2026

## Why the filter matters / 为什么过滤很重要

| Metric 指标 | Before 前 | After 后 | Insight 洞察 |
|---|---:|---:|---|
| Papers 论文数 | 1,174 | 456 | 61% removed 移除 |
| Avg FWCI 平均 FWCI | 8.85 | 2.79 | Real research focus 真实研究方向 |
| Max FWCI 最大 FWCI | 927 | 67 | Outliers were physics 异常值是物理 |
| Top field 最高领域 | Physics | CS / AI | Real research profile 真实研究画像 |

**Without the filter** 没有过滤, Stanford-SJTU looks like a physics consortium.
看起来像物理联盟。

**With the filter** 有过滤, you see the real bilateral AI/CS/health collaboration.
你看到真实的双边 AI/CS/健康合作。

## Key findings / 关键发现

| Metric 指标 | Value 数值 |
|---|---:|
| Total papers 论文数 | 456 |
| Total citations 总引用 | 8,989 |
| Avg FWCI 平均 FWCI | 2.79 |
| Distinct institutions 独立机构 | 187 |
| Distinct ASJC fields 独立领域 | 207 |
| Top journal 最高产期刊 | Nature Communications (17) |
| Top field 最高产领域 | Computer Science Applications (43) |
| Open Access 开放获取 | 215 (47.1%) |
| Multi-sector papers 多区域论文 | 409 (89.7%) |

## Region distribution (after classifier v3) / 区域分布 (v3 分类器后)

| Region 区域 | Papers 论文 | Share 占比 |
|---|---:|---:|
| Stanford (source) 斯坦福（源）| 455 | 13.6% |
| Shanghai Jiao Tong (target) 上海交大（目标）| 410 | 12.3% |
| Mainland China 中国大陆 | 391 | 11.7% |
| US (other top) 美国其他顶级 | 387 | 11.6% |
| Hong Kong / Macau / Taiwan 港澳台 | 60 | 1.8% |
| US (Federal/DOE) 美国联邦 | 60 | 1.8% |
| Germany / Switzerland 德/瑞 | 56 | 1.7% |
| UK 英国 | 50 | 1.5% |
| Singapore 新加坡 | 47 | 1.4% |
| Other International 其他国际 | 1,308 | 39.3% |

## AI / ML cluster / AI 机器学习集群

- **Detection 检测**: Co-authors whose surnames match top CS/AI Chinese names (Wang/Li/Liu/Zhang/Ma/Zhao/Chen/Tang/Sun/Cai/Hu)
  **检测方法**: 合著者姓氏匹配最常见的 CS/AI 中文学者姓名
- **123 papers match** (27% of dataset) — **123 篇论文匹配**（占 27%）
- **Top researchers 顶级研究者**: Zhang Y. (32), Li Y. (30), Wang Y. (28)
- **Yearly trend 年度趋势**: 22 (2022) → 26 (2025), FWCI peaked at 3.10 (2024)

## Output files / 输出文件

- `stanford_sjtu_filtered_analysis.xlsx` (27 KB, 7 sheets, 56 formulas, bilingual EN+中文)
- `index.html` (110 KB, self-contained, bilingual with toggle)
- `stanford_sjtu_offline_bundle.zip` (80 KB, full package)
- Deployed URLs:
  - Dashboard 仪表板: https://d2qor2at6wdha.space.mcode.cn
  - Offline 离线: https://tf10itfi1x347.space.mcode.cn

## Bilingual features / 双语特性

- All 60+ labels in `English | 中文` format
  所有 60+ 标签用 `English | 中文` 格式
- Region names translated (`中国大陆（其他）`, `斯坦福（源）`, etc.)
  区域名已翻译
- HTML with toggle button (default: 中文 visible)
  HTML 含切换按钮（默认显示中文）
- Top 1% papers highlighted in both languages
  Top 1% 论文中英文双语突出
- Quality Score formula explained in both languages
  质量评分公式双语说明

## Lessons learned / 经验教训

1. **Always check `should_apply_filter()`** — physics consortium papers silently inflate metrics
   **务必检查 `should_apply_filter()`** — 物理联盟论文会悄悄抬高指标
2. **Region classifier v3 (full names)** is critical — `MIT` vs `Massachusetts Institute of Technology` produce very different results
   **v3 区域分类器（全名）** 至关重要 — `MIT` 与 `Massachusetts Institute of Technology` 结果差异很大
3. **Bilingual output** doubles the work but vastly improves usability for international teams
   **双语输出** 工作量翻倍但大幅提升国际团队使用体验
4. **Multi-US profile** (43.9% papers include Stanford + SJTU + ≥1 other US university) is a key insight for bilateral analysis
   **多美画像** (43.9% 论文含斯坦福+交大+≥1 所其他美国大学) 是双边分析的关键洞察
5. **AI cluster detection** by Chinese surname pattern reveals the AI/ML collaboration depth
   **通过中文学者姓氏模式检测 AI 集群** 揭示 AI/ML 合作深度

## How to reproduce / 如何复现

```bash
# Get the Scopus CSV from your account, place at:
# 获取 Scopus CSV，放在：
# examples/stanford-sjtu/sample-input.csv

python scripts/build_xlsx.py \
    --csv examples/stanford-sjtu/sample-input.csv \
    --source "Stanford" \
    --target "Shanghai Jiao Tong" \
    --output /tmp/stanford_output
```