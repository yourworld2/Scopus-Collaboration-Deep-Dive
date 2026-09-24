"""HTML builder with bilingual rendering fix.

The bilingual pattern uses 'lang-zh visible by default, lang-en hidden by default'.
This way the page renders even with JS broken or CSS not loading.

Reference: see Stanford × SJTU case (Sep 2026) — previous pattern (both display:none
+ JS toggle) caused empty page on some browsers. New pattern is JS-optional.
"""

from typing import Optional


DEFAULT_LANG_BIDI_CSS = """
.lang-en { display: none; }
body.show-en .lang-zh { display: none; }
body.show-en .lang-en { display: block; }
"""

BILINGUAL_JS = '''
function setLang(lang) {
    document.body.className = '';
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
    var btn = document.getElementById('btn-' + lang);
    if (btn) btn.classList.add('active');
    if (lang === 'en') document.body.classList.add('show-en');
}
'''


def bilingual_html(
    zh_body: str,
    en_body: str,
    title_zh: str,
    title_en: str,
    extra_css: str = '',
    extra_head: str = '',
    extra_js: str = '',
    show_xlsx_download: bool = False,
    xlsx_b64: Optional[str] = None,
    xlsx_download_filename: str = 'analysis.xlsx',
) -> str:
    """Build a complete bilingual HTML page with the safer lang-zh-default pattern.

    Args:
        zh_body: Chinese content (visible by default).
        en_body: English content (hidden by default).
        title_zh: Browser tab title (Chinese).
        title_en: Browser tab title (English).
        extra_css: Extra CSS to inject.
        extra_head: Extra HTML to inject in <head>.
        extra_js: Extra JS to inject before closing </body>.
        show_xlsx_download: Show XLSX download button.
        xlsx_b64: Base64-encoded XLSX for download.
        xlsx_download_filename: Filename for XLSX download.

    Returns:
        Complete HTML string.
    """
    title = f'{title_zh} | {title_en}'
    css = DEFAULT_LANG_BIDI_CSS + extra_css

    js = BILINGUAL_JS
    if show_xlsx_download and xlsx_b64:
        js += f'''
function downloadXLSX() {{
    const b64 = "{xlsx_b64}";
    const bin = atob(b64);
    const arr = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    const blob = new Blob([arr], {{type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "{xlsx_download_filename}";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}}
'''

    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="zh-CN">')
    parts.append('<head>')
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    parts.append(f'<title>{esc(title)}</title>')
    parts.append('<style>')
    parts.append(css)
    parts.append('</style>')
    parts.append(extra_head)
    parts.append('</head>')
    parts.append('<body>')
    parts.append('<div class="lang-bar">')
    parts.append('<button class="lang-btn active" id="btn-zh" onclick="setLang(\'zh\')">中文</button>')
    parts.append('<button class="lang-btn" id="btn-en" onclick="setLang(\'en\')">English</button>')
    if show_xlsx_download:
        parts.append('<button class="lang-btn" onclick="downloadXLSX()">⬇ XLSX</button>')
    parts.append('</div>')

    parts.append('<div class="lang-zh">')
    parts.append(zh_body)
    parts.append('</div>')

    parts.append('<div class="lang-en">')
    parts.append(en_body)
    parts.append('</div>')

    parts.append('<script>')
    parts.append(js)
    parts.append('</script>')
    if extra_js:
        parts.append(extra_js)
    parts.append('</body>')
    parts.append('</html>')

    return '\n'.join(parts)


def consolidate_pages(pages: list, title: str, toc_links: list = None,
                       separator_text: str = None) -> str:
    """Consolidate multiple HTML pages into one.

    Args:
        pages: List of (name, html_content) tuples.
        title: Unified document title.
        toc_links: Optional list of (anchor_id, display_text) for TOC.
        separator_text: Optional text to show at each separator (e.g., "Part N: ...").

    Returns:
        Consolidated HTML string.
    """
    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append(f'<html lang="zh-CN"><head><meta charset="UTF-8">')
    parts.append(f'<title>{esc(title)}</title>')
    parts.append('<style>')
    parts.append(DEFAULT_BIDI_CSS)
    parts.append('</style>')
    parts.append('</head><body>')

    # Unified title
    parts.append(f'<h1>{esc(title)}</h1>')

    # TOC
    if toc_links:
        parts.append('<div class="toc">')
        parts.append('<h3>📑 报告目录 / Table of Contents</h3>')
        parts.append('<ol>')
        for anchor_id, text in toc_links:
            parts.append(f'<li><a href="#{anchor_id}">{esc(text)}</a></li>')
        parts.append('</ol>')
        parts.append('</div>')

    # Pages
    for i, (name, content) in enumerate(pages):
        if i > 0:
            parts.append('<hr class="part-divider">')
            if separator_text:
                parts.append(f'<h2>{esc(separator_text)} {i+1}</h2>')
        parts.append(content)

    parts.append('<div class="footer">')
    parts.append('<p>Consolidated report. Generated by Mavis.</p>')
    parts.append('</div>')
    parts.append('</body></html>')

    return '\n'.join(parts)


def esc(s):
    """HTML-escape a string."""
    if s is None:
        return ''
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


DEFAULT_BIDI_CSS = DEFAULT_LANG_BIDI_CSS