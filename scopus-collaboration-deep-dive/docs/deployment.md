# Deployment guide

How to share your XLSX + HTML dashboard publicly.

## Option 1: Public URL via `website_deploy`

```python
# 1. Build the deliverable in a self-contained directory
mkdir -p /tmp/share
cp output.html /tmp/share/index.html
cp output.xlsx /tmp/share/

# 2. Use the Mavis tool
website_deploy(
    path="/tmp/share",
    source_path="/tmp/share",
    project_name="Yale × China 2022-2026"
)
# Returns: https://xyz.space.mcode.cn
```

The deployed URL is publicly accessible. Use only when the data is meant to be shared publicly.

## Option 2: Offline ZIP package

For no-internet viewing (e.g., internal team on a flight):

```bash
mkdir -p output_bundle
cp output.html output_bundle/index.html
cp output.xlsx output_bundle/
cp intermediate.json output_bundle/

cd output_bundle
zip -r ../output_bundle.zip .
```

The HTML file is self-contained — no external CSS/JS/fonts. Opens in any browser.

## Option 3: Email-ready XLSX only

For just sharing the spreadsheet:

```bash
# Single XLSX with all sheets
cp output.xlsx ~/Downloads/
```

XLSX size is typically 25-30 KB for 7 sheets — well within email attachment limits.

## Option 4: GitHub Pages / Vercel / Netlify

For long-term hosting with custom domain:

1. Create a new GitHub repo
2. Push the `output_bundle/` contents to `docs/` or root
3. Enable GitHub Pages
4. Access via `https://username.github.io/repo-name/`

## Deployment checklist

Before deploying publicly, verify:

- [ ] No PII (emails, phone numbers) in deliverable
- [ ] No internal-only data (employee IDs, restricted research)
- [ ] License allows public sharing (Scopus data is OK for derived analyses)
- [ ] Get user confirmation
- [ ] Bilingual version verified in browser

## ⚠️ Important caveats

**Public deployment is just that — public.** Anyone with the URL can view the data. Make sure the user wants this before deploying.

**Source archive is uploaded too.** When using `website_deploy`, both the built site and the source directory are saved. Don't include secrets in either.

## URL formats

| Pattern | Use Case |
|---|---|
| `https://xyz.space.mcode.cn` | Default Mavis-hosted deployment |
| `https://username.github.io/repo` | GitHub Pages (custom domain possible) |
| `https://project-name.vercel.app` | Vercel deployment |
| Local file:// | Offline / no internet |

## When NOT to deploy

- When the data is confidential or proprietary
- When the user explicitly says "don't share" / "keep private"
- When the dataset includes sensitive PII
- When the publication list is embargoed (e.g., pre-publication)

## Real-world examples from this skill

| Deployment | URL | Type |
|---|---|---|
| Yale × China (signatures) | `huhqumk08ghal.space.mcode.cn/signatures_funding.html` | Public XLSX sheet view |
| Stanford × SJTU dashboard | `d2qor2at6wdha.space.mcode.cn` | Bilingual EN+中文 |
| Stanford × SJTU offline | `tf10itfi1x347.space.mcode.cn` | Self-contained + ZIP download |