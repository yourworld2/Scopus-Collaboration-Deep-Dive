# Adding bilingual output to new regions | 为新区域添加双语输出

> How to add a new language (e.g., French, German, Japanese) to the skill.
> 如何为技能添加新的语言（如法语、德语、日语）。

## 1. Update `scripts/bilingual.py` | 更新 `scripts/bilingual.py`

Add a new translation dictionary alongside `REGION_TRANSLATIONS`:
在 `REGION_TRANSLATIONS` 旁边添加新的翻译字典：

```python
REGION_TRANSLATIONS_FR = {
    'Stanford (source)': 'Stanford (source)',
    'Shanghai Jiao Tong (target)': 'Université de Shanghai Jiao Tong',
    'Mainland China': 'Chine continentale',
    ...
}
```

Add label translations:
添加标签翻译：

```python
LABEL_TRANSLATIONS_FR = {
    'Overview': 'Aperçu',
    'Top 20 Partner Institutions': 'Top 20 institutions partenaires',
    ...
}
```

## 2. Update HTML template | 更新 HTML 模板

The current pattern uses two divs with class toggle. For 3+ languages, switch to a data-attribute pattern:
当前模式用两个 div + 类切换。3+ 种语言用 data-attribute 模式：

```html
<div class="lang lang-zh"><!-- 中文 --></div>
<div class="lang lang-en"><!-- English --></div>
<div class="lang lang-fr"><!-- Français --></div>
```

```css
.lang { display: none; }
body[lang="zh"] .lang-zh { display: block; }
body[lang="en"] .lang-en { display: block; }
body[lang="fr"] .lang-fr { display: block; }
```

```javascript
function setLang(lang) {
    document.body.setAttribute('lang', lang);
}
```

## 3. Update XLSX labels | 更新 XLSX 标签

Single-column pattern works for any language. Just use the new translations:
单列模式适合任何语言。直接用新翻译：

```python
B('Overview', 'Aperçu')  # French | 法语
B('Total Publications', '总发表数')  # Chinese | 中文
B('Total Publications', '총 게재 수')  # Korean | 韩语
```

## 4. Translation tips | 翻译技巧

- **Keep sheet names ASCII** — Excel handles non-ASCII sheet names inconsistently across versions
  **工作表名保持 ASCII** — Excel 对非 ASCII 工作表名处理不一致

- **Use 「」『』 for Japanese** rather than western quotes (better readability)
  **日文用 「」『』** 而不是西方引号（可读性更好）

- **CJK character sets**: Chinese (Simplified/Traditional), Japanese (Hiragana/Katakana), Korean (Hangul)
  **CJK 字符集**：中文（简/繁）、日文（平假名/片假名）、韩文（韩字）

- **Right-to-left languages** (Arabic, Hebrew): add `dir="rtl"` to the container div
  **从右到左语言**（阿拉伯语、希伯来语）：给容器 div 加 `dir="rtl"`

## 5. Test the new language | 测试新语言

After adding a language:
添加新语言后：

```python
# tests/test_bilingual.py
def test_french_translations():
    from bilingual import REGION_TRANSLATIONS_FR
    assert REGION_TRANSLATIONS_FR['Mainland China'] == 'Chine continentale'
```

```bash
pytest tests/test_bilingual.py -v
```

## 6. Real-world example | 真实示例

For Stanford × SJTU the bilingual translation dictionary includes:
斯坦福 × SJTU 的双语翻译字典包括：

- **14 region names** / 14 个区域名 (one for each region category / 每种区域一个)
- **60+ label translations** / 60+ 标签翻译 (sheet titles, column headers, metric names / 工作表名、列头、指标名)
- **4 long-form explanations** / 4 个详细说明 (Quality Score, name disambiguation, AI cluster, filter)
- **4 metric descriptions** / 4 个指标描述 (FWCI, citations, ASJC, OA)

## Pitfalls | 注意事项

❌ **Don't auto-translate** — machine translation produces awkward results for technical terms
**不要自动翻译** — 机器翻译对术语产生尴尬结果

❌ **Don't translate sheet names** — Excel may break with non-ASCII sheet names
**不翻译工作表名** — Excel 对非 ASCII 工作表名会出错

❌ **Don't use machine-only verification** — bilingual output is user-facing; manual review needed
**不要只用机器验证** — 双语输出面向用户，需要人工审查

❌ **Don't assume same character set** — Chinese (CJK Unified Ideographs) ≠ Japanese (Hiragana/Katakana)
**不要假设同字符集** — 中文（CJK 统一汉字）≠ 日文（平假名/片假名）

✅ **Do keep technical terms (FWCI, ASJC) untranslated**
**保留技术术语 (FWCI, ASJC) 不翻译**

✅ **Do provide both languages for important descriptions**
**重要描述提供两种语言**

✅ **Do test in actual browser** (some CJK fonts may not render in headless tests)
**在真实浏览器测试**（无头浏览器可能不渲染 CJK 字体）