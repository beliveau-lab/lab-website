# Beliveau Lab website

The lab site (https://beliveau.io), rebuilt as a static site for GitHub Pages.
All content lives in `data/*.json`; the HTML pages are generated from it.

## How it works

- **`data/`** — the content. Three files: `team.json`, `news.json`,
  `publications.json`. This is the only thing you normally edit.
- **`scripts/site.py`** — a small CLI for editing that content safely
  (add a member, move someone to alumni, post news, add a paper, validate).
- **`scripts/build_pages.py`** — regenerates every `.html` file from the JSON
  plus the shared nav/footer chrome.
- **`css/`, `js/`** — styling and the client-side renderers that read the JSON.
- **GitHub Actions** rebuilds the HTML and deploys on every push to `main`,
  so you only ever commit JSON.

## Editing content

Use the CLI rather than hand-editing JSON where you can:

```bash
# add a new lab member
python3 scripts/site.py add-member \
  --name "Jane Doe" --role "Postdoctoral Researcher" \
  --joined "Sept 2026" --email "jdoe@uw.edu" \
  --photo-url "https://.../jane.jpg"

# graduate / move someone to alumni
python3 scripts/site.py move-to-alumni --name "Jane Doe" \
  --after "Now an Assistant Professor at ..."

# post a news item (HTML links are fine)
python3 scripts/site.py add-news --month "September 2026" \
  --item 'Our SABER-FISH paper is out in <a href="https://...">Nature Methods</a>!'

# add a publication
python3 scripts/site.py add-pub \
  --title "..." --authors "Doe, J., Beliveau, B.J." \
  --venue "Nature Methods 23, 1 (2026)" --year 2026 \
  --link "Journal=https://..." --link "PubMed=https://..."

# add a preprint instead
python3 scripts/site.py add-pub --preprint \
  --title "..." --authors "..." --venue "bioRxiv (2026)" \
  --link "bioRxiv=https://..."

# see what you have / check for problems
python3 scripts/site.py list team
python3 scripts/site.py validate
```

Then preview and rebuild:

```bash
python3 scripts/build_pages.py          # regenerate the HTML
python3 -m http.server 8000             # preview at http://localhost:8000
```

> Previewing needs a local server (the pages `fetch()` the JSON, which the
> browser blocks over `file://`). `python3 -m http.server` is enough.

Commit and push `main`; the Action rebuilds and deploys automatically.

## Images

Team and news photos currently load from the old Wix CDN as a fallback so the
site renders identically right away. **Before canceling Wix**, localize them:

```bash
python3 scripts/download_images.py      # downloads into images/, repoints JSON
git add images data && git commit -m "Localize images" && git push
```

See `DEPLOY.md` for first-time GitHub Pages + Namecheap DNS setup.

## Layout

```
data/            content (edit this)
scripts/         site.py, build_pages.py, download_images.py
css/  js/        presentation + JSON renderers
images/          team/ alumni/ news/ research/
*.html           generated — do not hand-edit
CNAME            custom domain (beliveau.io)
.github/workflows/deploy.yml   build + deploy on push
```
