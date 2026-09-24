# Changelog | 变更日志

> All notable changes to this project are documented here.
> 本项目的所有重要变更都记录在这里。

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

## [1.5.0] - 2026-09-24 | 2026年9月24日

### Changed / 变更
- **All documentation bilingualized** | **所有文档双语化** — Every markdown file (README, SKILL.md, CHANGELOG, CONTRIBUTING, docs/, examples/) now has Chinese + English content
  每个 Markdown 文件（README、SKILL.md、CHANGELOG、CONTRIBUTING、docs/、examples/）现在都有中英文双语
- **YAML frontmatter** updated with bilingual description and bilingual keywords | YAML frontmatter 更新双语描述和双语关键词
- **`SKILL.md` body** rewritten with parallel Chinese/English sections | **`SKILL.md` 正文** 重写为中英文并行

### Added / 新增
- **`CHANGELOG.md` bilingual header** | **`CHANGELOG.md` 双语标题**
- **`CONTRIBUTING.md` bilingual guide** | **`CONTRIBUTING.md` 双语指南**
- **`README.md` bilingual headers, tables, footers** | **`README.md` 双语标题、表格、页脚**
- **`docs/architecture.md` bilingual** | **`docs/architecture.md` 双语**
- **`docs/bilingual.md` bilingual** | **`docs/bilingual.md` 双语**
- **`docs/consolidation.md` bilingual** | **`docs/consolidation.md` 双语**
- **`docs/deployment.md` bilingual** | **`docs/deployment.md` 双语**
- **`docs/html-pitfalls.md` bilingual** | **`docs/html-pitfalls.md` 双语**
- **`examples/yale-china/README.md` bilingual** | **`examples/yale-china/README.md` 双语**
- **`examples/stanford-sjtu/README.md` bilingual** | **`examples/stanford-sjtu/README.md` 双语**
- **`examples/yale-china-complete/README.md` bilingual** | **`examples/yale-china-complete/README.md` 双语**

### Philosophy | 设计理念
> Skill descriptions should be **immediately understandable by both English and Chinese speakers**.
> Bilingual content reflects international research collaboration work and serves the global academic community.
> 技能描述应**对中英文使用者都能立即理解**。
> 双语内容反映了国际研究合作工作，服务全球学术社区。

## [1.4.0] - 2026-09-24 | 2026年9月24日

### Added | 新增
- **`scripts/html_builder.py`** — bilingual HTML builder with default-zh pattern
  **`scripts/html_builder.py`** — 双语 HTML 构造函数，默认中文模式
- **`scripts/deploy.py`** — public deployment helper (3 patterns: dashboard / download / ZIP)
  **`scripts/deploy.py`** — 公网部署助手（3 种模式）
- **`docs/html-pitfalls.md`** — HTML generation gotchas (f-string escapes, CSS bugs, deployment issues)
  **`docs/html-pitfalls.md`** — HTML 生成陷阱
- **`docs/consolidation.md`** — page consolidation pattern (3-page → 1-page)
  **`docs/consolidation.md`** — 页面合并模式
- **`examples/yale-china-complete/`** — real-world consolidation example
  **`examples/yale-china-complete/`** — 真实合并示例

### Improved | 改进
- Bilingual CSS pattern (lang-zh visible by default) | 双语 CSS 模式
- Decision matrix updates | 决策矩阵更新

### Validated on | 验证案例
- Yale × Chinese Universities (2,664 papers, 7 sheets, 318 formulas, 31 KB) | 耶鲁 × 中国大学
- Stanford × Shanghai Jiao Tong University (456 papers, 7 sheets, 56 formulas, bilingual) | 斯坦福 × 上海交大
- Yale consolidated report (3 pages → 1 page, 86 KB) | 耶鲁合并报告

## [1.0.0] - 2026-09-24 | 2026年9月24日

### Added | 新增
- **Author-count filter** | 作者数过滤 — automatic detection of consortium mega-papers
- **Region classifier v3** | v3 区域分类器 — 50+ explicit university names
- **Bilingual output** | 双语输出 — EN + 中文 in single column
- **5-sheet base pipeline** | 5 工作表基础流程 covering 10 default topics
- **Extended 7-sheet pipeline** | 7 工作表扩展流程
- **HTML dashboard** | HTML 仪表板 with EN/中文 toggle
- **Public deployment** support via `website_deploy` | 公网部署支持
- **Offline package** | 离线包 — self-contained HTML
- **Live formulas** throughout | 公式覆盖派生指标

## [0.9.0] - 2026-09-20 (pre-release) | 2026年9月20日 (预发布)

### Added | 新增
- Initial SKILL.md with 9-step procedure | 初始 SKILL.md（9 步流程）
- 11-code-snippet analysis-cookbook | 11 个代码片段
- 8 templated insight patterns | 8 个洞察模式
- 3 worked examples | 3 个示例

[1.5.0]: https://github.com/minimax/scopus-collaboration-deep-dive/releases/tag/v1.5.0
[1.4.0]: https://github.com/minimax/scopus-collaboration-deep-dive/releases/tag/v1.4.0
[1.0.0]: https://github.com/minimax/scopus-collaboration-deep-dive/releases/tag/v1.0.0
[0.9.0]: https://github.com/minimax/scopus-collaboration-deep-dive/releases/tag/v0.9.0