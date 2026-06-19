# Deploying to GitHub Pages with the beliveau.io domain

One-time setup. After this, every push to `main` rebuilds and redeploys.

## 1. Push the repo

```bash
cd beliveau-site
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

Naming the repo `<you>.github.io` is optional — a custom domain works with any
repo name.

## 2. Turn on GitHub Pages (Actions deployment)

In the repo: **Settings → Pages → Build and deployment → Source = GitHub Actions**.

The included workflow (`.github/workflows/deploy.yml`) validates the content,
runs `build_pages.py`, and publishes. Watch the first run under the **Actions**
tab. When it finishes you'll get a `*.github.io` URL — confirm the site looks
right there before wiring up the domain.

## 3. Point beliveau.io at GitHub (Namecheap)

In Namecheap: **Domain List → Manage → Advanced DNS**. Remove the existing
records that point at Wix, then add:

| Type  | Host | Value                  |
|-------|------|------------------------|
| A     | @    | 185.199.108.153        |
| A     | @    | 185.199.109.153        |
| A     | @    | 185.199.110.153        |
| A     | @    | 185.199.111.153        |
| CNAME | www  | `<you>.github.io.`     |

(Those four A records are GitHub Pages' published IPs. The `CNAME` host value
should be your GitHub Pages subdomain, with the trailing dot.)

If Namecheap shows a default "URL Redirect / parking" record on `@`, delete it
or the A records won't take effect.

## 4. Set the custom domain in GitHub

**Settings → Pages → Custom domain →** enter `beliveau.io` and save. This
repo already contains a `CNAME` file with `beliveau.io`, so it should populate
automatically. Once DNS resolves (minutes to a few hours), tick
**Enforce HTTPS**.

## 5. Localize images, then cancel Wix — in that order

While Wix is still live:

```bash
python3 scripts/download_images.py
git add images data && git commit -m "Localize images" && git push
```

Verify photos still load on the deployed site, **then** cancel the Wix
subscription. Doing it in this order avoids broken images if the Wix CDN
stops serving the old URLs.

## Troubleshooting

- **Pages build failed in Actions** — open the run log. A failed `validate`
  step means a content problem in `data/`; fix and push again.
- **Domain shows "improperly configured"** — DNS hasn't propagated yet, or a
  leftover Namecheap parking record is still on `@`. Recheck step 3.
- **Images 404 after canceling Wix** — they weren't localized first. Re-run
  `download_images.py` against the JSON (it still has the remote URLs in git
  history if needed).
