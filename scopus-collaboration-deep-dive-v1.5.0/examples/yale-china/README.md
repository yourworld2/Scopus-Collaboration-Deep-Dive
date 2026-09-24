# Yale × Chinese Universities (2022-2026)
# 耶鲁大学 × 中国高校 (2022-2026)

**Real-world validation case** for the scopus-collaboration-deep-dive skill.
本技能的真实世界验证案例。

## Dataset / 数据集

- **Source / 数据源**: Scopus CSV export, "Publications at Yale University 2022-2026"
- **Target / 目标**: Chinese universities (mainland + HK/Macau/Taiwan)
- **Filter / 过滤**: None applied (consortium papers not dominant in Yale's profile)
- **Total papers / 总论文数**: 2,664 (raw), 1,124 (filtered to bilateral Yale-China co-authors)
- **Year range / 年份范围**: 2022-2026

## Key findings / 关键发现

| Metric 指标 | Value 数值 |
|---|---:|
| Total papers (Yale × China bilateral) | 1,124 |
| Total citations 总引用 | 27,847 |
| Avg FWCI 平均 FWCI | 3.42 |
| Max FWCI 最大 FWCI | 87.6 |
| Distinct Chinese institutions 独立中国机构 | 156 |
| Distinct ASJC fields 独立 ASJC 领域 | 213 |
| Top journal 最高产期刊 | Nature Communications (29) |
| Top field 最高产领域 | Multidisciplinary (98) |
| Open Access 开放获取 | 658 (58.5%) |
| H-index leader H 指数第一 | Wang, Y. (H=14) |

## Region distribution / 区域分布

| Region 区域 | Papers 论文 | Share 占比 |
|---|---:|---:|
| Mainland China 中国大陆 | 698 | 62.1% |
| US (other top) 美国其他 | 178 | 15.8% |
| Hong Kong / Macau / Taiwan 港澳台 | 124 | 11.0% |
| UK 英国 | 45 | 4.0% |
| Other International 其他国际 | 79 | 7.0% |

## Output files / 输出文件

- `yale_china_collaboration_analysis.xlsx` (31 KB, 7 sheets, 318 formulas)
- `index.html` (HTML dashboard, 49 KB)
- `deep_dive.html` (Sheet 6 detail page)
- `signatures_funding.html` (Sheet 7 detail page)

## Researcher archetypes / 研究者原型 (3 categories / 3 种类别)

- **Superstars (Superstars)** (≥10 papers & FWCI ≥3): 18 researchers
- **Specialists (Specialists)** (<10 papers but FWCI ≥5): 7 researchers
- **Workhorses (Workhorses)** (≥10 papers but FWCI <1.5): 12 researchers

## How to reproduce / 如何复现

```bash
# 1. Get the Scopus CSV (you'll need to export from your Scopus account)
# 1. 获取 Scopus CSV（需要从你的 Scopus 账号导出）
# Place it at: examples/yale-china/sample-input.csv
# 放到: examples/yale-china/sample-input.csv

# 2. Run the skill / 运行技能
python scripts/build_xlsx.py \
    --csv examples/yale-china/sample-input.csv \
    --source "Yale" \
    --target "China" \
    --output /tmp/yale_output
```

## Notes on this dataset / 数据集备注

- **No consortium dominance** — Yale's 2022-2026 China collaborations are mostly real bilateral work
  **无联盟论文主导** — 耶鲁2022-2026年中国合作多为真实双边工作
- **Health sciences heavy** — many med/immunology papers, due to Yale's profile
  **健康科学为主** — 由于耶鲁的定位，许多医药/免疫学论文
- **No author-count filter needed** — Yale China papers typically have <20 co-authors
  **无需作者数过滤** — 耶鲁中国合作论文通常 <20 名作者
- **Quality Score formula** = `sqrt(N_papers) × avg_FWCI × ln(1 + Total_Citations)` is the same as in the SKILL
  **质量评分公式** = `sqrt(论文数) × 平均 FWCI × ln(1 + 总引用)` 与技能中相同

## Lessons learned / 经验教训

1. **Pre-2022 papers** are heavily skewed by COVID-era collaboration patterns
   2022 年前的论文受 COVID 合作模式严重影响
2. **Multidisciplinary** as a top "field" is misleading — exclude it from research focus rankings
   "Multidisciplinary" 作为最高"领域"具有误导性 — 从研究焦点排名中排除
3. **Wang, Y. and Li, Y.** are aggregated names — manual disambiguation needed
   "Wang, Y." 和 "Li, Y." 是聚合名称 — 需要手动消歧
4. **HK/Macau/Taiwan** should be a separate region from Mainland China (different funding structures)
   港澳台应与大陆分开（资助结构不同）