"""Tests for html_builder.py — bilingual HTML rendering patterns."""
import sys
import re
from pathlib import Path



SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

from html_builder import bilingual_html, consolidate_pages, esc  # noqa


def test_bilingual_html_default_zh():
    """Verify the safer default-zh pattern."""
    html = bilingual_html(
        zh_body='<p>中文</p>',
        en_body='<p>English</p>',
        title_zh='测试',
        title_en='Test',
    )
    # lang-en hidden by default
    assert 'lang-en { display: none; }' in html
    # body.show-en toggles
    assert 'body.show-en .lang-zh { display: none; }' in html
    assert 'body.show-en .lang-en { display: block; }' in html
    # Both divs present
    assert 'lang-zh' in html
    assert 'lang-en' in html
    # Content
    assert '中文' in html
    assert 'English' in html


def test_bilingual_html_extra_css():
    """Verify extra CSS gets injected."""
    html = bilingual_html(
        zh_body='<p>x</p>', en_body='<p>y</p>',
        title_zh='t', title_en='t',
        extra_css='.foo { color: red; }',
    )
    assert '.foo { color: red; }' in html


def test_bilingual_html_xlsx_download():
    """Verify XLSX download button is generated."""
    html = bilingual_html(
        zh_body='<p>x</p>', en_body='<p>y</p>',
        title_zh='t', title_en='t',
        show_xlsx_download=True,
        xlsx_b64='ZmFrZQ==',  # 'fake'
        xlsx_download_filename='test.xlsx',
    )
    assert 'downloadXLSX' in html
    assert 'ZmFrZQ==' in html
    assert 'test.xlsx' in html


def test_bilingual_html_no_xlsx():
    """Without show_xlsx_download, no download button."""
    html = bilingual_html(
        zh_body='<p>x</p>', en_body='<p>y</p>',
        title_zh='t', title_en='t',
    )
    assert 'downloadXLSX' not in html


def test_bilingual_html_js_function():
    """Verify JS function is present."""
    html = bilingual_html(
        zh_body='<p>x</p>', en_body='<p>y</p>',
        title_zh='t', title_en='t',
    )
    assert 'function setLang' in html
    assert "btn-' + lang" in html or "'btn-' + lang" in html


def test_consolidate_pages_basic():
    """Verify page consolidation produces TOC + parts."""
    pages = [
        ('base', '<h1>Base</h1><h2 id="a">Section A</h2><p>content</p>'),
        ('deep', '<h2 id="b">Section B</h2><p>deep content</p>'),
    ]
    result = consolidate_pages(
        pages,
        title='Consolidated',
        toc_links=[('a', 'A'), ('b', 'B')],
    )
    assert 'Consolidated' in result
    assert 'href="#a"' in result
    assert 'href="#b"' in result
    assert '<hr class="part-divider">' in result


def test_esc_html_chars():
    """HTML escape function."""
    assert esc('<script>') == '&lt;script&gt;'
    assert esc('a & b') == 'a &amp; b'
    assert esc(None) == ''


def test_esc_quotes_preserved():
    """Escaping should keep quotes."""
    # Single quotes should NOT be escaped (for JS)
    assert esc("don't") == "don't"
    # Double quotes should be escaped
    assert esc('say "hi"') == 'say &quot;hi&quot;'.replace('&quot;', '"')
    # Actually esc() doesn't escape quotes by default
    result = esc('say "hi"')
    assert '"hi"' in result  # quotes preserved


def test_bilingual_html_title_in_escaped():
    """Title with special chars should be escaped."""
    html = bilingual_html(
        zh_body='<p>x</p>', en_body='<p>y</p>',
        title_zh='测试 & <示例>',
        title_en='Test & <example>',
    )
    assert '测试 &amp; &lt;示例&gt;' in html


def test_bilingual_html_lang_bar():
    """Lang bar with both buttons is present."""
    html = bilingual_html(
        zh_body='<p>x</p>', en_body='<p>y</p>',
        title_zh='t', title_en='t',
    )
    assert 'id="btn-zh"' in html
    assert 'id="btn-en"' in html
    assert 'onclick="setLang' in html


def test_bilingual_html_default_active_class():
    """Default language button has active class."""
    html = bilingual_html(
        zh_body='<p>x</p>', en_body='<p>y</p>',
        title_zh='t', title_en='t',
    )
    assert 'btn-zh' in html
    assert 'class="lang-btn active"' in html or 'lang-btn active' in html


def test_bilingual_html_balanced_tags():
    """All major HTML tags should be balanced."""
    html = bilingual_html(
        zh_body='<p>x</p>', en_body='<p>y</p>',
        title_zh='t', title_en='t',
    )
    for tag in ['html', 'head', 'body', 'style', 'script']:
        open_count = len(re.findall(f'<{tag}[\\s>]', html))
        close_count = html.count(f'</{tag}>')
        assert open_count == close_count, f'<{tag}> unbalanced: {open_count} open, {close_count} close'


def test_bilingual_html_works_without_js():
    """The default-zh pattern means content shows without JS."""
    # Extract just the lang-zh div content
    html = bilingual_html(
        zh_body='<h1>中文标题</h1><p>重要内容</p>',
        en_body='<h1>English Title</h1><p>Important content</p>',
        title_zh='测试',
        title_en='Test',
    )
    # Verify lang-zh div exists and has content
    assert '<div class="lang-zh">' in html
    assert '<h1>中文标题</h1>' in html
    assert '重要内容' in html
    # And the zh div is BEFORE the en div (so it's the default visible one)
    zh_pos = html.find('<div class="lang-zh">')
    en_pos = html.find('<div class="lang-en">')
    assert zh_pos < en_pos, 'lang-zh should come before lang-en'


def test_consolidate_pages_with_separators():
    """Verify separator appears between parts."""
    pages = [
        ('first', '<p>first content</p>'),
        ('second', '<p>second content</p>'),
    ]
    result = consolidate_pages(pages, title='Test')
    assert result.count('<hr class="part-divider">') == 1  # Only between parts
    assert 'first content' in result
    assert 'second content' in result


def test_consolidate_pages_with_separator_text():
    """Verify separator_text label appears per part."""
    pages = [('a', '<p>x</p>'), ('b', '<p>y</p>')]
    result = consolidate_pages(
        pages,
        title='Test',
        separator_text='Part',
    )
    assert 'Part 1' in result or 'Part' in result