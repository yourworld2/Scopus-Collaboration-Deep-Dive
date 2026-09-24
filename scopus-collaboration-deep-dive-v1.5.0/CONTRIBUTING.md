# Contributing

> 贡献指南 / Contributing Guide

Thanks for considering a contribution to **scopus-collaboration-deep-dive**!

欢迎为 **scopus-collaboration-deep-dive** 提交贡献！

## Most useful contributions / 最有用的贡献

1. **New region classifier rules** — extending `scripts/region_classifier.py` for other countries
   新区域分类规则 — 为其他国家扩展 `scripts/region_classifier.py`

2. **New cluster patterns** — life sciences, physics, materials, etc.
   新集群模式 — 生命科学、物理、材料等

3. **New templated insights** — bibliometric patterns observed in different fields
   新模板化洞察 — 不同领域的文献计量模式

4. **Translation corrections** in bilingual labels
   双语标签的翻译纠正

6. **Bug fixes** — XLSX structural issues, formula errors, CSS rendering bugs
   Bug 修复 — XLSX 结构问题、公式错误、CSS 渲染 bug

## Development setup / 开发环境配置

```bash
git clone https://github.com/minimax/scopus-collaboration-deep-dive.git
cd scopus-collaboration-deep-dive

# Install dependencies / 安装依赖
pip install -r requirements.txt

# Run tests / 运行测试
pytest tests/

# Try on the example CSVs / 在示例 CSV 上试用
python scripts/build_xlsx.py \
    --csv examples/yale-china/sample-input.csv \
    --source "Yale" \
    --target "China" \
    --output /tmp/test_output
```

## Pull request workflow / 提交流程

1. Fork the repo / Fork 仓库
2. Create a feature branch / 创建功能分支 (`git checkout -b feature/new-region-rule`)
3. Make changes (with tests if applicable) / 修改代码（如适用请带测试）
4. Run `pytest tests/` to verify no regressions / 跑测试确认无回归
5. Update [CHANGELOG.md](CHANGELOG.md) under "Unreleased" section / 更新 CHANGELOG.md
6. Open PR with before/after screenshots if visual changes / 提 PR，UI 改动请附前后截图

## Code style / 代码风格

- Python: PEP 8, type hints where possible, docstrings for public functions
  Python 遵循 PEP 8，尽量加类型注解和文档字符串
- XLSX: Live formulas everywhere on derived metrics, never hardcoded ratios
  XLSX：所有派生指标用活公式，不要硬编码比例
- HTML: Self-contained (no external CDN/fonts), bilingual-ready by default
  HTML：自包含（无外部 CDN/字体），默认支持双语
- Comments and descriptions should include both Chinese and English
  注释和描述应该同时包含中文和英文

## Adding a new region classifier / 添加新的区域分类器

To add rules for a new country (e.g., Singapore, Korea, Brazil):
为新加坡、韩国、巴西等国家添加规则：

1. Add keyword lists to `scripts/region_classifier.py`:
   添加关键词列表到 `scripts/region_classifier.py`：
   ```python
   SINGAPORE_KEYWORDS = ['singapore', 'nus ', 'ntu', 'nanyang technological']
   ```
2. Add a check function:
   添加检查函数：
   ```python
   def is_singapore_inst(name):
       nm = name.lower()
       return any(k in nm for k in SINGAPORE_KEYWORDS)
   ```
3. Update `classify_inst_v3()` to add a branch
   更新 `classify_inst_v3()` 添加分支
4. Add a test case in `tests/test_region_classifier.py`
   在 `tests/test_region_classifier.py` 添加测试
5. Update bilingual labels in `examples/*/README.md` if needed
   如需要更新示例 README 中的双语标签

## Adding a new cluster pattern / 添加新的集群模式

To add detection of, say, a Materials Science cluster:
例如添加材料科学集群检测：

1. Add to `scripts/clusters.py`:
   添加到 `scripts/clusters.py`：
   ```python
   def detect_materials_cluster(papers):
       """检测材料科学论文 | Papers with Materials Science ASJC field."""
       return [p for p in papers
               if any('material' in f.lower() for f in p['fields'])]
   ```
2. Add a usage example in `examples/materials-cluster/`
   在 `examples/materials-cluster/` 添加使用示例
3. Document in SKILL.md under "Deep-dive topics" section
   在 SKILL.md 的 "Deep-dive topics" 部分记录

## Testing / 测试

All PRs should pass `pytest tests/`. Add new tests for new functionality.
所有 PR 必须通过 `pytest tests/`。新功能请添加测试。

```python
# tests/test_my_feature.py
def test_author_count_filter():
    from scripts.filters import apply_author_filter
    df = pd.DataFrame(...)
    df_filtered, _ = apply_author_filter(df, max_authors=50)
    assert all(df_filtered['n_authors'] <= 50)
```

## Questions? / 有问题？

Open an issue. We're friendly.
提 issue 即可。我们很友好。