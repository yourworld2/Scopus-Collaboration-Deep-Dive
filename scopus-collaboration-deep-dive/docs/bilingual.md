# Adding bilingual output to new regions

How to add a new language (e.g., French, German, Japanese) to the skill.

## 1. Update `scripts/bilingual.py`

Add a new translation dictionary alongside `REGION_TRANSLATIONS`:

```python
REGION_TRANSLATIONS_FR = {
    'Stanford (source)': 'Stanford (source)',
    'Shanghai Jiao Tong (target)': 'Université de Shanghai Jiao Tong',
    'Mainland China': 'Chine continentale',
    ...
}
```

Add label translations:

```python
LABEL_TRANSLATIONS_FR = {
    'Overview': 'Aperçu',
    'Top 20 Partner Institutions': 'Top 20 institutions partenaires',
    ...
}
```

## 2. Update HTML template

The current pattern uses two divs with class toggle. For 3+ languages, switch to a data-attribute pattern:

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

## 3. Update XLSX labels

Single-column pattern works for any language. Just use the new translations:

```python
B('Overview', 'Aperçu')  # French
B('Total Publications', '总发表数')  # Chinese
B('Total Publications', '총 게재 수')  # Korean
```

## 4. Translation tips

- **Keep sheet names ASCII** — Excel handles non-ASCII sheet names inconsistently across versions
- **Use 「」『』 for Japanese** rather than western quotes (better readability)
- **CJK character sets**: Chinese (Simplified/Traditional), Japanese (Hiragana/Katakana), Korean (Hangul)
- **Right-to-left languages** (Arabic, Hebrew): add `dir="rtl"` to the container div

## 5. Test the new language

After adding a language:

```python
# tests/test_bilingual.py
def test_french_translations():
    from bilingual import REGION_TRANSLATIONS_FR
    assert REGION_TRANSLATIONS_FR['Mainland China'] == 'Chine continentale'
```

```bash
pytest tests/test_bilingual.py -v
```

## 6. Real-world example

For Stanford × SJTU the bilingual translation dictionary includes:

- 14 region names (one for each region category)
- 60+ label translations (sheet titles, column headers, metric names)
- 4 long-form explanations (Quality Score, name disambiguation, AI cluster, filter)
- 4 metric descriptions (FWCI, citations, ASJC, OA)

## Pitfalls

❌ **Don't auto-translate** — machine translation produces awkward results for technical terms

❌ **Don't translate sheet names** — Excel may break with non-ASCII sheet names

❌ **Don't use machine-only verification** — bilingual output is user-facing; manual review needed

❌ **Don't assume same character set** — Chinese (CJK Unified Ideographs) ≠ Japanese (Hiragana/Katakana)

✅ **Do keep technical terms (FWCI, ASJC) untranslated**

✅ **Do provide both languages for important descriptions**

✅ **Do test in actual browser** (some CJK fonts may not render in headless tests)