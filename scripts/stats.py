"""Tag/entity counts for the radar: this window vs the window before it.

    python scripts/stats.py --end 2026-10-11 --days 7

Prints a Markdown table Claude pastes into the Sunday analysis. Counts only
items the free model tagged with importance >= 1.
"""
import argparse
import json
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_items(root, start, end):
    items, d = [], start
    while d <= end:
        path = root / "data" / d.strftime("%Y-%m") / f"{d}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            for cat in data["categories"]:
                items += [dict(it, category=cat["key"]) for it in cat["items"] if it.get("importance", 1) > 0]
        d += timedelta(days=1)
    return items


def count(items, field):
    c = Counter()
    for it in items:
        for v in set(x.lower() for x in it.get(field, [])):
            c[v] += 1
    return c


def risers(now, before, top=20, min_count=3):
    rows = []
    for k, n in now.items():
        if n < min_count:
            continue
        prev = before.get(k, 0)
        rows.append((k, n, prev, (n + 1) / (prev + 1)))
    rows.sort(key=lambda r: (-r[3], -r[1]))
    return rows[:top]


def table(title, rows):
    out = [f"### {title}", "", "| หัวข้อ | สัปดาห์นี้ | ก่อนหน้า | เท่า |", "|---|---:|---:|---:|"]
    out += [f"| {k} | {n} | {p} | {r:.1f} |" for k, n, p, r in rows]
    return "\n".join(out + [""])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--end", type=date.fromisoformat, default=date.today())
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args(argv)

    start = args.end - timedelta(days=args.days - 1)
    now = load_items(args.root, start, args.end)
    before = load_items(args.root, start - timedelta(days=args.days), start - timedelta(days=1))
    print(f"ข่าว {start} ถึง {args.end}: {len(now)} ชิ้น · ช่วงก่อนหน้า: {len(before)} ชิ้น\n")
    print(table("แท็กที่ถูกพูดถึงเพิ่มเร็ว", risers(count(now, "tags"), count(before, "tags"))))
    print(table("ชื่อบริษัท/คน/ประเทศที่ถูกพูดถึงเพิ่มเร็ว", risers(count(now, "entities"), count(before, "entities"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
