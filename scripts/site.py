#!/usr/bin/env python3
"""
site.py — content management CLI for the Beliveau Lab website.

All content lives in data/*.json. Edit it through this tool (or by hand),
then run `python3 scripts/build_pages.py` to regenerate the HTML.

Usage:
  python3 scripts/site.py add-member   --name "..." --role "..." [options]
  python3 scripts/site.py move-to-alumni --name "..." [--after "..."] [--dates "..."]
  python3 scripts/site.py remove-member --name "..."
  python3 scripts/site.py add-news     --month "October 2025" --item "..." [--item "..."]
  python3 scripts/site.py add-pub      --title "..." --authors "..." --venue "..." [options]
  python3 scripts/site.py list         [team|news|pubs]
  python3 scripts/site.py validate

Run with no args, or `-h`, for help.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TEAM = os.path.join(DATA, "team.json")
NEWS = os.path.join(DATA, "news.json")
PUBS = os.path.join(DATA, "publications.json")

WIX_HOST = "static.wixstatic.com"

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


# ---------- io helpers ----------

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")

def slug(name):
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")

def info(msg):
    print(msg)

def die(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


# ---------- team ----------

def cmd_add_member(args):
    team = load(TEAM)
    if any(m["name"].lower() == args.name.lower() for m in team["current"]):
        die(f'"{args.name}" is already a current member.')

    rec = {"name": args.name, "role": args.role}
    if args.pi:
        rec["pi"] = True
    if args.degree:
        rec["degree"] = args.degree
    if args.program:
        rec["program"] = args.program
    if args.pronouns:
        rec["pronouns"] = args.pronouns
    if args.email:
        rec["email"] = args.email
    if args.joined:
        rec["joined"] = args.joined
    if args.joint:
        rec["joint"] = args.joint
    if args.social_label and args.social_url:
        rec["social"] = {"label": args.social_label, "url": args.social_url}
    ext = os.path.splitext(args.photo_url)[1].lower() if args.photo_url else ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        ext = ".jpg"
    rec["photo"] = f"images/team/{slug(args.name)}{ext}"
    if args.photo_url:
        rec["photo_remote"] = args.photo_url

    # PI stays first; everyone else appended.
    if args.pi:
        team["current"].insert(0, rec)
    else:
        team["current"].append(rec)
    save(TEAM, team)
    info(f'Added current member "{args.name}". '
         f'Drop a photo at {rec["photo"]} (or run download_images.py if --photo-url was set).')


def cmd_move_to_alumni(args):
    team = load(TEAM)
    idx = next((i for i, m in enumerate(team["current"])
                if m["name"].lower() == args.name.lower()), None)
    if idx is None:
        die(f'"{args.name}" not found among current members.')
    m = team["current"].pop(idx)

    alum = {"name": m["name"], "role": m.get("role", "")}
    if args.dates:
        alum["dates"] = args.dates
    elif m.get("joined"):
        alum["dates"] = f'{m["joined"]} \u2013 {datetime.now().year}'
    if args.after:
        alum["after"] = args.after
    # repoint photo into the alumni folder, keep remote fallback
    if m.get("photo"):
        fn = os.path.basename(m["photo"])
        alum["photo"] = f"images/alumni/{fn}"
    if m.get("photo_remote"):
        alum["photo_remote"] = m["photo_remote"]

    team["alumni"].insert(0, alum)
    save(TEAM, team)
    info(f'Moved "{m["name"]}" to alumni. '
         f'If a photo exists at images/team/, move it to {alum.get("photo","images/alumni/")}.')


def cmd_remove_member(args):
    team = load(TEAM)
    for bucket in ("current", "alumni"):
        idx = next((i for i, m in enumerate(team[bucket])
                    if m["name"].lower() == args.name.lower()), None)
        if idx is not None:
            team[bucket].pop(idx)
            save(TEAM, team)
            info(f'Removed "{args.name}" from {bucket}.')
            return
    die(f'"{args.name}" not found.')


# ---------- news ----------

def _month_key(label):
    """Sort key for a 'Month YYYY' string; unknown formats sort last."""
    parts = label.split()
    if len(parts) == 2 and parts[0] in MONTHS:
        return (int(parts[1]), MONTHS.index(parts[0]))
    return (-1, -1)

def cmd_add_news(args):
    news = load(NEWS)
    items = [s for s in (args.item or []) if s.strip()]
    if not items:
        die("provide at least one --item.")
    entry = next((m for m in news if m["month"].lower() == args.month.lower()), None)
    if entry:
        if args.top:
            entry["items"] = items + entry["items"]
        else:
            entry["items"].extend(items)
        info(f'Appended {len(items)} item(s) to "{args.month}".')
    else:
        news.insert(0, {"month": args.month, "items": items})
        info(f'Created news month "{args.month}" with {len(items)} item(s).')
    # keep reverse-chronological order
    news.sort(key=lambda m: _month_key(m["month"]), reverse=True)
    save(NEWS, news)


# ---------- publications ----------

def cmd_add_pub(args):
    pubs = load(PUBS)
    if args.preprint:
        rec = {"title": args.title, "authors": args.authors, "venue": args.venue}
        if args.link:
            rec["links"] = [_parse_link(x) for x in args.link]
        pubs["preprints"].insert(0, rec)
        info(f'Added preprint "{args.title[:50]}...".')
    else:
        nums = [p.get("num", 0) for p in pubs["papers"]]
        nxt = (max(nums) + 1) if nums else 1
        year = args.year or datetime.now().year
        rec = {"num": nxt, "year": int(year),
               "title": args.title, "authors": args.authors, "venue": args.venue}
        if args.link:
            rec["links"] = [_parse_link(x) for x in args.link]
        pubs["papers"].insert(0, rec)
        pubs["papers"].sort(key=lambda p: (p.get("year", 0), p.get("num", 0)), reverse=True)
        info(f'Added paper #{nxt} ({year}) "{args.title[:50]}...".')
    save(PUBS, pubs)

def _parse_link(s):
    """Accept 'Label=https://url' or just a bare URL."""
    if "=" in s:
        label, url = s.split("=", 1)
        return {"label": label.strip(), "url": url.strip()}
    return {"label": "Link", "url": s.strip()}


# ---------- list / validate ----------

def cmd_list(args):
    what = args.what or "team"
    if what == "team":
        team = load(TEAM)
        print(f"CURRENT ({len(team['current'])}):")
        for m in team["current"]:
            print(f"  - {m['name']} — {m.get('role','')}")
        print(f"\nALUMNI ({len(team['alumni'])}):")
        for m in team["alumni"]:
            print(f"  - {m['name']} — {m.get('role','')}")
    elif what == "news":
        for m in load(NEWS):
            print(f"{m['month']}: {len(m['items'])} item(s)")
    elif what == "pubs":
        pubs = load(PUBS)
        print(f"Preprints: {len(pubs['preprints'])}")
        print(f"Papers: {len(pubs['papers'])}")
    else:
        die(f"unknown list target '{what}'")

def cmd_validate(args):
    problems = []
    warnings = []

    team = load(TEAM)
    pis = [m for m in team["current"] if m.get("pi")]
    if len(pis) != 1:
        problems.append(f"expected exactly 1 PI in current, found {len(pis)}")
    # A person may legitimately appear more than once with distinct
    # appointments (e.g. rotation -> RA -> grad student), so key on the
    # full (name, role, dates) tuple rather than name alone.
    seen = set()
    wix_count = 0
    for bucket in ("current", "alumni"):
        for m in team[bucket]:
            if "name" not in m or "role" not in m:
                problems.append(f"{bucket} entry missing name/role: {m}")
            key = (bucket, m.get("name", "").lower(),
                   m.get("role", ""), m.get("dates", ""), m.get("joined", ""))
            if key in seen:
                problems.append(f"exact duplicate {bucket} entry: "
                                f'{m.get("name")} ({m.get("role")})')
            seen.add(key)
            if m.get("photo_remote") and WIX_HOST in m["photo_remote"]:
                wix_count += 1
    if wix_count:
        warnings.append(f"{wix_count} member photo(s) still point at the Wix CDN; "
                        f"localize them before canceling Wix")

    news = load(NEWS)
    for m in news:
        if "month" not in m or "items" not in m:
            problems.append(f"news entry malformed: {m}")
        if not isinstance(m.get("items"), list) or not m["items"]:
            problems.append(f"news month '{m.get('month')}' has no items")

    pubs = load(PUBS)
    nums = [p.get("num") for p in pubs["papers"]]
    if len(nums) != len(set(nums)):
        problems.append("duplicate publication numbers")
    for p in pubs["papers"]:
        if not all(k in p for k in ("num", "year", "title", "authors", "venue")):
            problems.append(f"paper missing fields: {p.get('title','?')[:40]}")

    if warnings:
        print(f"{len(warnings)} warning(s):")
        for w in warnings:
            print("  ! " + w)
        print()
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  x " + p)
        sys.exit(1)
    print("All content valid.")


# ---------- argparse ----------

def build_parser():
    p = argparse.ArgumentParser(
        prog="site.py",
        description="Manage Beliveau Lab website content (data/*.json). "
                    "Run build_pages.py afterward to regenerate HTML.")
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("add-member", help="add a current lab member")
    a.add_argument("--name", required=True)
    a.add_argument("--role", required=True, help='e.g. "Postdoctoral Researcher"')
    a.add_argument("--degree")
    a.add_argument("--program", help="e.g. graduate program")
    a.add_argument("--pronouns")
    a.add_argument("--email")
    a.add_argument("--joined", help='e.g. "Sept 2026"')
    a.add_argument("--joint", help="joint-lab affiliation note")
    a.add_argument("--photo-url", dest="photo_url", help="remote image URL")
    a.add_argument("--social-label", dest="social_label")
    a.add_argument("--social-url", dest="social_url")
    a.add_argument("--pi", action="store_true", help="mark as PI (pins to top)")
    a.set_defaults(func=cmd_add_member)

    a = sub.add_parser("move-to-alumni", help="move a current member to alumni")
    a.add_argument("--name", required=True)
    a.add_argument("--after", help="where they went next")
    a.add_argument("--dates", help='override dates, e.g. "2022 \u2013 2026"')
    a.set_defaults(func=cmd_move_to_alumni)

    a = sub.add_parser("remove-member", help="delete a member entirely")
    a.add_argument("--name", required=True)
    a.set_defaults(func=cmd_remove_member)

    a = sub.add_parser("add-news", help="add a news item")
    a.add_argument("--month", required=True, help='e.g. "October 2025"')
    a.add_argument("--item", action="append", required=True,
                   help="news text (HTML <a> ok); repeat for multiple")
    a.add_argument("--top", action="store_true", help="prepend within the month")
    a.set_defaults(func=cmd_add_news)

    a = sub.add_parser("add-pub", help="add a publication")
    a.add_argument("--title", required=True)
    a.add_argument("--authors", required=True)
    a.add_argument("--venue", required=True)
    a.add_argument("--year", type=int)
    a.add_argument("--link", action="append",
                   help='"Label=https://url" or a bare URL; repeat for multiple')
    a.add_argument("--preprint", action="store_true")
    a.set_defaults(func=cmd_add_pub)

    a = sub.add_parser("list", help="list current content")
    a.add_argument("what", nargs="?", choices=["team", "news", "pubs"])
    a.set_defaults(func=cmd_list)

    a = sub.add_parser("validate", help="check all JSON for problems")
    a.set_defaults(func=cmd_validate)
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "func", None):
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
