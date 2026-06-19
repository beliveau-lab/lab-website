#!/usr/bin/env python3
"""
download_images.py — localize images off the Wix CDN.

Run this LOCALLY (it needs internet access to static.wixstatic.com).
It walks data/*.json, downloads every `photo_remote` / news `photos[]`
URL into the right images/ subfolder, and points the JSON at the local
copy.

  *** Run this BEFORE you cancel your Wix subscription. ***
  Once Wix is gone, the static.wixstatic.com URLs may stop working and
  the photos would 404. Localizing first makes the site self-contained.

Usage:
  python3 scripts/download_images.py            # download everything
  python3 scripts/download_images.py --dry-run  # show what would happen
  python3 scripts/download_images.py --keep-remote   # keep photo_remote as a fallback

By default a successfully-downloaded photo_remote is removed (the local
file is authoritative). Use --keep-remote to leave it in as a fallback.
"""

import argparse
import json
import os
import sys
import urllib.request
from urllib.error import URLError, HTTPError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TEAM = os.path.join(DATA, "team.json")
NEWS = os.path.join(DATA, "news.json")

UA = "Mozilla/5.0 (beliveau-site image localizer)"


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def save(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")

def ext_from_url(url, default=".jpg"):
    # wix urls look like .../b8abaf_xxx~mv2.jpg/v1/.../file.jpg
    base = url.split("?")[0]
    for token in reversed(base.split("/")):
        for e in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            if token.lower().endswith(e):
                return e
    return default

def fetch(url, dest, dry):
    if dry:
        print(f"  would download -> {dest}")
        return True
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        with open(dest, "wb") as f:
            f.write(data)
        print(f"  saved {len(data)//1024} KB -> {os.path.relpath(dest, ROOT)}")
        return True
    except (URLError, HTTPError, TimeoutError) as e:
        print(f"  FAILED {url}\n         {e}", file=sys.stderr)
        return False


def do_team(args):
    team = load(TEAM)
    ok = fail = 0
    for bucket in ("current", "alumni"):
        for m in team[bucket]:
            url = m.get("photo_remote")
            if not url:
                continue
            local = m.get("photo")
            if not local:
                local = f"images/{'team' if bucket=='current' else 'alumni'}/" \
                        f"{m['name'].lower().replace(' ', '_')}{ext_from_url(url)}"
                m["photo"] = local
            dest = os.path.join(ROOT, local)
            if os.path.exists(dest) and not args.force and not args.dry_run:
                print(f"  exists, skip -> {local}")
                continue
            print(f"{m['name']}:")
            if fetch(url, dest, args.dry_run):
                ok += 1
                if not args.keep_remote and not args.dry_run:
                    m.pop("photo_remote", None)
            else:
                fail += 1
    if not args.dry_run:
        save(TEAM, team)
    return ok, fail


def do_news(args):
    news = load(NEWS)
    ok = fail = 0
    os.makedirs(os.path.join(ROOT, "images", "news"), exist_ok=True)
    for m in news:
        urls = m.get("photos")
        if not urls:
            continue
        local_paths = []
        for i, url in enumerate(urls):
            stem = m["month"].lower().replace(" ", "_")
            local = f"images/news/{stem}_{i+1}{ext_from_url(url)}"
            dest = os.path.join(ROOT, local)
            print(f"{m['month']} [{i+1}]:")
            if os.path.exists(dest) and not args.force and not args.dry_run:
                print(f"  exists, skip -> {local}")
                local_paths.append(local)
                continue
            if fetch(url, dest, args.dry_run):
                ok += 1
                local_paths.append(local)
            else:
                fail += 1
                local_paths.append(url)  # fall back to remote on failure
        if not args.dry_run and not args.keep_remote:
            m["photos_local"] = local_paths
    if not args.dry_run:
        save(NEWS, news)
    return ok, fail


def main():
    ap = argparse.ArgumentParser(description="Localize Wix CDN images.")
    ap.add_argument("--dry-run", action="store_true", help="show actions, change nothing")
    ap.add_argument("--force", action="store_true", help="re-download even if local file exists")
    ap.add_argument("--keep-remote", action="store_true",
                    help="keep photo_remote URLs as a fallback")
    args = ap.parse_args()

    print("== team photos ==")
    t_ok, t_fail = do_team(args)
    print("\n== news photos ==")
    n_ok, n_fail = do_news(args)

    print(f"\nDone. {t_ok + n_ok} downloaded, {t_fail + n_fail} failed.")
    if t_fail + n_fail:
        print("Some downloads failed — those entries still reference the Wix CDN. "
              "Re-run before canceling Wix.")
        sys.exit(1)


if __name__ == "__main__":
    main()
