# HTML generation pitfalls | HTML 生成陷阱

> Real-world debugging notes from the scopus-collaboration-deep-dive skill.
> 来自 scopus-collaboration-deep-dive 技能的真实调试笔记。

## 🚨 Bug #1: Empty page after deploy | 部署后页面空白

**Symptom** 症状: Deployed HTML page shows nothing — looks blank. Verified locally that HTML has content.
部署后的 HTML 页面显示为空白 — 本地验证 HTML 有内容。

**Root cause** 根本原因:
```css
/* Dangerous pattern — both lang divs hidden by default */
/* 危险模式 — 两个语言 div 默认都被隐藏 */
.lang-zh, .lang-en { display: none; }
body.lang-zh .lang-zh { display: block; }
body.lang-en .lang-en { display: block; }
```

If JS doesn't run (CSP issue, browser quirk, slow connection), `body` never gets a class — **both divs stay `display: none`**.
如果 JS 不跑（CSP 问题、浏览器怪癖、网络慢），`body` 永远不会获得 class — **两个 div 都保持 `display: none`**。

**Fix** 修复:
```css
/* Safe pattern — zh visible by default */
/* 安全模式 — 中文默认可见 */
.lang-en { display: none; }
body.show-en .lang-zh { display: none; }
body.show-en .lang-en { display: block; }
```

Now even without JS, the Chinese version is visible.
即使没有 JS，中文版也是可见的。

## 🚫 Bug #2: f-string with `}}` literals | f-string 包含字面 `}}`

**Symptom** 症状: Python `SyntaxError: f-string: unmatched '['` or `SyntaxError: f-string expression part cannot include a backslash`.
Python 语法错误。

**Root cause** 根本原因: f-strings have limitations:
f-string 有以下限制：

1. Can't have backslashes in expressions: `f"{value['key']}"` 表达式不能有反斜杠
2. Can't have nested same-type quotes: `f"{... 'key' inside ...}"` 不能嵌套同类型引号
3. `}}` is an escape for `}` — easy to get wrong with CSS `}}` 是 `}` 的转义 — 写 CSS 时容易搞错

**Fix** 修复: Use string concatenation instead:
改用字符串拼接：
```python
# Instead of / 而不是:
html = f'<style>.badge {{ color: {color}; }}</style>'

# Use / 使用:
html = '<style>.badge {\n' + \
       '  color: ' + color + ';\n' + \
       '</style>'
```

Or use `.format()` with explicit escapes:
或用 `.format()` 加显式转义：
```python
html = '<style>.badge {{ color: {}; }}</style>'.format(color)
```

Best for complex HTML: build a list and `'\n'.join(parts)`.
复杂 HTML 的最佳做法：构建列表再 `'\n'.join(parts)`。

## 🚫 Bug #3: `class="rank"` count in Python | 在 Python 中统计 `class="rank"`

**Symptom** 症状: `SyntaxError: f-string expression part cannot include a backslash` when counting tag occurrences.
统计标签出现次数时报语法错误。

**Root cause** 根本原因:
```python
# This fails / 这样会失败:
print(f"Rank badges: {content.count('class=\"rank\"')}")
```

**Fix** 修复: Store the search string in a variable first:
先把搜索字符串存到变量里：
```python
q1 = 'class="rank'
print(f"Rank badges: {content.count(q1)}")
```

## 🚫 Bug #4: Empty `<div class="lang-zh">` | 空的 lang-zh div

**Symptom** 症状: User reports "both public URL and local HTML appear empty". HTML structure is correct, but content div is empty.
用户报告"公网 URL 和本地 HTML 都空白"。HTML 结构正确，但内容 div 是空的。

**Root cause** 根本原因: Loop variable shadowing or logic error — when building rows dynamically, sometimes the loop runs against the wrong variable.
循环变量遮蔽或逻辑错误 — 动态构建行时，有时循环跑错了变量。

**Debug** 调试: Count chars in each section:
统计每节的字符数：
```python
zh_start = content.find('<div class="lang-zh">')
en_start = content.find('<div class="lang-en">')
print(f"lang-zh content: {en_start - zh_start} chars")
# If this is 0 or tiny, you have a bug
# 如果接近 0 或很小，你有 bug
```

## 🚫 Bug #5: Platform-injected content | 平台注入内容

**Symptom** 症状: Deployed URL has slightly larger HTML than local file. Some pages appear different from local.
部署的 URL 比本地文件稍大一些。有些页面看起来跟本地不同。

**Root cause** 根本原因: Some deployment platforms (e.g., space.mcode.cn) inject analytics widgets or footer scripts. This is normal and not a bug — verify locally first.
某些部署平台（如 space.mcode.cn）会注入分析 widget 或底部脚本。这是正常的，不是 bug —— 先在本地验证。

**Verify** 验证:
```bash
curl -s -w "Size: %{size_download}\n" https://your-deployed-url/
# Compare to local file size
# 跟本地文件大小比较
```

A 5-10% size difference is normal. A 50%+ difference means something's wrong.
5-10% 的大小差异是正常的。50%+ 差异表示有问题。

## ✅ Defensive patterns | 防御性模式

1. **Always default one language visible** — don't require JS for content
   **始终默认一种语言可见** — 内容不依赖 JS

2. **Use string concatenation for complex HTML** — avoid f-string edge cases
   **复杂 HTML 用字符串拼接** — 避免 f-string 边界情况

3. **Verify with `curl` after deploy** — confirm size and status
   **部署后用 `curl` 验证** — 确认大小和状态

4. **Test with JS disabled** — open in browser DevTools with JS off
   **关掉 JS 测试** — 在浏览器 DevTools 关 JS 后打开

5. **Use a search variable for repeated strings** — avoid backslash escapes
   **重复字符串用搜索变量** — 避免反斜杠转义

## 🧪 Validation script | 验证脚本

```python
def validate_html(html_path):
    """Validate HTML structure for common bugs. | 验证 HTML 结构中的常见 bug。"""
    content = open(html_path).read()

    # Check bilingual pattern / 检查双语模式
    if 'lang-zh' in content:
        # Verify default visibility / 验证默认可见性
        if '.lang-en { display: none' not in content:
            print('⚠️  lang-en might not be hidden by default')
            print('⚠️  lang-en 可能未默认隐藏')
        if 'body.show-en .lang-zh' not in content:
            print('⚠️  No toggle for showing lang-en')
            print('⚠️  没有切换到 lang-en 的逻辑')

    # Check balanced tags / 检查标签平衡
    import re
    for tag in ['html', 'head', 'body', 'style']:
        open_count = len(re.findall(f'<{tag}[\\s>]', content))
        close_count = content.count(f'</{tag}>')
        if open_count != close_count:
            print(f'⚠️  <{tag}> unbalanced: {open_count} open, {close_count} close')
            print(f'⚠️  <{tag}> 不平衡: {open_count} 开, {close_count} 闭')

    # Check content size / 检查内容大小
    zh_start = content.find('<div class="lang-zh">')
    en_start = content.find('<div class="lang-en">')
    if zh_start > 0 and en_start > zh_start:
        zh_chars = en_start - zh_start
        if zh_chars < 1000:
            print(f'⚠️  lang-zh content too small ({zh_chars} chars)')
            print(f'⚠️  lang-zh 内容太少 ({zh_chars} 字符)')
```

Run this after every HTML generation to catch issues early.
每次生成 HTML 后运行这个脚本，及早发现问题。