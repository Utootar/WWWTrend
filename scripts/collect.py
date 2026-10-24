"""Daily collector: RSS news + prices -> free-model summaries -> data/ and news/.

Free models only shorten and tag news. They never judge or forecast; Claude
does the analysis later from the files written here (see CLAUDE.md).

    python scripts/collect.py              # full run (needs GEMINI_API_KEY and/or OPENROUTER_API_KEY)
    python scripts/collect.py --no-llm     # fetch only, no summaries (for testing sources)

Repair (run by a daily Claude routine on the owner's subscription, not here):
    python scripts/collect.py --repair-pending /tmp/pending.json   # items the free models failed on
    python scripts/collect.py --repair-apply /tmp/summaries.json   # merge Claude's summaries back
    python scripts/collect.py --review-pending /tmp/review.json    # summaries for Claude to check
    python scripts/collect.py --review-apply /tmp/fixes.json       # apply Claude's corrections

Theme stocks: Claude lists public tickers it found in the news in
config/theme_stocks.yaml; their prices are fetched here so the next analysis
can see them (the analysis sessions cannot reach Yahoo themselves).
"""
import argparse
import calendar
import hashlib
import html
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

import feedparser
import requests
import yaml

from llm import LLMError, Summarizer

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (compatible; WWWTrend/1.0; personal news digest)"}
TEXT_LIMIT = 700
MAX_THEME_STOCKS = 40
THAI_MONTHS = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
               "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]

SYSTEM_PROMPT = """You are a news clerk for a Thai reader. You shorten news; you never analyse.
Rules:
- Use ONLY facts written in the given title/text. No outside knowledge, no guesses.
- No opinions, predictions, advice, or words like "likely", "should", "bullish".
- summary_th: 1-2 short Thai sentences saying what happened (who, what, how much).
  If the text is thin, translate the headline faithfully and stop.
- numbers: copy figures exactly as they appear in the input (e.g. "$4,189", "2.5%"). Empty list if none.
- importance: 3 = moves markets/industry or a big policy/approval/deal; 2 = notable; 1 = minor;
  0 = off-topic for the category, an ad, a listicle, or a how-to.
- tags: 1-4 short English topic tags in lower case (e.g. "fed", "opec", "ai chips", "glp-1").
- entities: companies, people, countries, products named in the input.
Reply with JSON only:
{"items":[{"id":"...","importance":0-3,"summary_th":"...","numbers":[],"tags":[],"entities":[]}]}
Include every id you were given, exactly once."""

REVIEW_PROMPT = """You check Thai news summaries written by a free model against their source title/text.
You fix mistakes; you never analyse.
Fix an item only when its summary_th:
- gets a number, a direction (up/down), a name, a date, or who-did-what wrong versus the title/text;
- adds anything the title/text does not say (outside facts, opinion, prediction, advice);
- mistranslates the headline or misses its main point;
- or its importance is clearly off: 3 = moves markets/industry or a big policy/approval/deal;
  2 = notable; 1 = minor; 0 = off-topic for the category, an ad, a listicle, or a how-to.
Leave correct items alone; wording or style is not a reason to change.
A new summary_th follows the clerk rules: 1-2 short Thai sentences, only facts in the title/text,
figures copied exactly as written in the source (e.g. "$25 billion", "2.5%"), never converted.
Reply with JSON only:
{"checked":["every id you were given"],"fixes":[{"id":"...","reason":"short Thai reason","summary_th":"...","importance":0-3,"numbers":[]}]}
In a fix only id and reason are required; leave out the fields you do not change."""


# ---------- fetching ----------

def clean_text(raw, limit=TEXT_LIMIT):
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    return text[:limit]


def normalize_link(url):
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query) 
             if not k.lower().startswith("utm_") and k.lower() not in ("mod", "cmpid")]
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path, urlencode(query), ""))


def item_id(link):
    return hashlib.sha1(link.encode()).hexdigest()[:12]


def title_key(title):
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()[:90]


def parse_feed(content, feed_name):
    parsed = feedparser.parse(content)
    items = []
    for e in parsed.entries:
        link = e.get("link")
        title = clean_text(e.get("title"), 300)
        if not link or not title:
            continue
        stamp = e.get("published_parsed") or e.get("updated_parsed")
        source = feed_name
        if e.get("source", {}).get("title"):  # Google News: real publisher
            source = e["source"]["title"]
            title = re.sub(r"\s+-\s+" + re.escape(source) + r"$", "", title)
        link = normalize_link(link)
        items.append({
            "id": item_id(link),
            "title": title,
            "link": link,
            "source": source,
            "published": calendar.timegm(stamp) if stamp else None,
            "text": clean_text(e.get("summary") or e.get("description")),
        })
    return items


def fetch_feed(feed, log=print):
    try:
        resp = requests.get(feed["url"], headers=UA, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        log(f"::warning::feed failed {feed['name']}: {e}")
        return []
    return parse_feed(resp.content, feed["name"])


def select_items(per_feed, now_ts, max_age_hours, seen, taken_ids, taken_titles, max_items):
    """Fresh, unseen, de-duplicated items, taken round-robin across feeds
    (newest first within each feed) so one busy feed can't fill the category."""
    queues = []
    for items in per_feed:
        fresh = [it for it in items
                 if it["published"] is not None and now_ts - it["published"] <= max_age_hours * 3600]
        queues.append(sorted(fresh, key=lambda x: x["published"], reverse=True))
    out = []
    while len(out) < max_items and any(queues):
        for q in queues:
            while q:
                it = q.pop(0)
                tk = title_key(it["title"])
                if it["id"] in seen or it["id"] in taken_ids or tk in taken_titles:
                    continue
                taken_ids.add(it["id"])
                taken_titles.add(tk)
                out.append(it)
                break
            if len(out) >= max_items:
                break
    return out


def fetch_prices(tickers, log=print):
    rows = []
    for t in tickers:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t['symbol']}"
        try:
            resp = requests.get(url, params={"range": "10d", "interval": "1d"}, headers=UA, timeout=30)
            resp.raise_for_status()
            result = resp.json()["chart"]["result"][0]
            closes = [(ts, c) for ts, c in zip(result["timestamp"], result["indicators"]["quote"][0]["close"])
                      if c is not None]
            (ts, close), (_, prev) = closes[-1], closes[-2]
        except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as e:
            log(f"::warning::price failed {t['symbol']}: {e}")
            rows.append({"symbol": t["symbol"], "label": t["label"], "close": None})
            continue
        rows.append({
            "symbol": t["symbol"], "label": t["label"],
            "close": round(close, 4), "prev_close": round(prev, 4),
            "change_pct": round((close - prev) / prev * 100, 2),
            "as_of": datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d"),
            "currency": result["meta"].get("currency"),
        })
    return rows


# ---------- summarising ----------

def digits(s):
    return re.findall(r"\d+(?:[.,]\d+)*", s)


def verify_numbers(numbers, source_text):
    """Keep only figures whose digits really appear in the source (free models invent numbers)."""
    src = set(d.replace(",", "") for d in digits(source_text))
    kept = []
    for n in numbers or []:
        ds = [d.replace(",", "") for d in digits(str(n))]
        if ds and all(d in src for d in ds):
            kept.append(str(n))
    return kept


def apply_summaries(batch, reply, model):
    by_id = {it["id"]: it for it in batch}
    for r in reply.get("items", []) if isinstance(reply, dict) else []:
        it = by_id.get(str(r.get("id")))
        if it is None or "summary_th" in it:
            continue
        try:
            importance = max(0, min(3, int(r.get("importance", 1))))
        except (TypeError, ValueError):
            importance = 1
        summary = str(r.get("summary_th") or "").strip()
        if not summary:
            continue
        it.update({
            "summary_th": summary,
            "importance": importance,
            "numbers": verify_numbers(r.get("numbers"), it["title"] + " " + it["text"]),
            "tags": [str(t).lower()[:40] for t in (r.get("tags") or [])][:4],
            "entities": [str(e)[:60] for e in (r.get("entities") or [])][:8],
            "model": model,
        })


def summarize_category(items, label, summarizer, batch_size, log=print):
    failed = 0
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        payload = [{"id": it["id"], "title": it["title"], "source": it["source"], "text": it["text"]}
                   for it in batch]
        prompt = f"Category: {label}\nNews items:\n" + json.dumps(payload, ensure_ascii=False)
        try:
            reply, model = summarizer.run(SYSTEM_PROMPT, prompt)
        except LLMError as e:
            log(f"::warning::summary failed for {label} batch {i // batch_size}: {e}")
            failed += len(batch)
            continue
        apply_summaries(batch, reply, model)
        failed += sum(1 for it in batch if "summary_th" not in it)
    return failed


# ---------- output ----------

def thai_date(d):
    return f"{d.day} {THAI_MONTHS[d.month - 1]} {d.year}"


def fmt_price(p):
    if p.get("close") is None:
        return f"| {p['label']} | ดึงไม่ได้ | |"
    sign = "+" if p["change_pct"] > 0 else ""
    return f"| {p['label']} | {p['close']:,.2f} | {sign}{p['change_pct']:.2f}% |"


def load_theme_stocks(path, skip=()):
    """Tickers Claude picked from the news (config/theme_stocks.yaml), minus ones already in prices."""
    if not path.exists():
        return []
    stocks = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("stocks") or []
    out, taken = [], set(skip)
    for s in stocks:
        sym = str(s.get("symbol", "")).strip()
        if sym and sym not in taken:
            taken.add(sym)
            label = s.get("label") or sym
            out.append({"symbol": sym, "label": f"{label} · {s['theme']}" if s.get("theme") else label})
    return out[:MAX_THEME_STOCKS]


def render_markdown(day, collected_at, prices, categories, models, failed, theme_prices=(), title="ข่าวประจำวัน"):
    total = sum(len(c["items"]) for c in categories)
    lines = [
        f"# {title} {thai_date(day)}",
        "",
        f"เก็บเมื่อ {collected_at.strftime('%H:%M')} น. เวลาไทย · ข่าว {total} ชิ้น"
        + (f" · ย่อโดย {', '.join(sorted(models))}" if models else ""),
        "",
        "> ไฟล์นี้คือข่าวย่อโดยโมเดลฟรี ยังไม่ใช่บทวิเคราะห์ ตัวเลขสำคัญให้กดลิงก์เช็คต้นทางก่อนใช้ตัดสินใจ",
        "",
    ]
    if failed:
        lines += [f"> **ย่อไม่สำเร็จ {failed} ข่าว** แสดงเป็นหัวข่าวภาษาอังกฤษแทน", ""]
    if prices:
        lines += ["## ราคาปิดล่าสุด", "", "| รายการ | ราคา | เปลี่ยน |", "|---|---:|---:|"]
        lines += [fmt_price(p) for p in prices]
        lines.append("")
    if theme_prices:
        lines += ["## ราคาหุ้นในธีมที่เจอจากข่าว", "",
                  "| หุ้น · ธีม | ราคา | เปลี่ยน |", "|---|---:|---:|"]
        lines += [fmt_price(p) for p in theme_prices]
        lines.append("")
    for cat in categories:
        shown = [it for it in cat["items"] if it.get("importance", 1) > 0]
        shown.sort(key=lambda it: (-it.get("importance", 1), -(it["published"] or 0)))
        lines += [f"## {cat['label']} ({len(shown)})", ""]
        if not shown:
            lines += ["ไม่มีข่าวใหม่", ""]
            continue
        for it in shown:
            stars = "★" * it.get("importance", 1)
            body = it.get("summary_th") or it["title"]
            extra = f" · ตัวเลข: {', '.join(it['numbers'])}" if it.get("numbers") else ""
            fixed = " · แก้โดย Claude" if it.get("fixed_by") else ""
            lines.append(f"- {stars} {body} — [{it['source']}]({it['link']}){extra}{fixed}")
        lines.append("")
    return "\n".join(lines)


def latest_file(folder, pattern):
    files = sorted(folder.glob(pattern)) if folder.exists() else []
    return files[-1] if files else None


def write_latest(root):
    news = latest_file(root / "news", "*/*.md")
    analysis = latest_file(root / "analysis", "*/*.md")
    rel = lambda p: p.relative_to(root).as_posix()
    lines = ["# ล่าสุด", ""]
    lines.append(f"- ข่าวประจำวัน: [{news.stem}]({rel(news)})" if news else "- ข่าวประจำวัน: ยังไม่มี")
    lines.append(f"- บทวิเคราะห์: [{analysis.stem}]({rel(analysis)})" if analysis else "- บทวิเคราะห์: ยังไม่มี")
    if (root / "ai" / "LATEST.md").exists():
        lines.append("- ข่าว AI (โฟลเดอร์แยก): [ai/LATEST.md](ai/LATEST.md)")
    lines += ["", "ย้อนดู: [ข่าวทั้งหมด](news/) · [บทวิเคราะห์ทั้งหมด](analysis/)", ""]
    (root / "LATEST.md").write_text("\n".join(lines), encoding="utf-8")


def append_price_history(path, day, prices):
    new = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        if new:
            f.write("date,symbol,close,as_of\n")
        for p in prices:
            if p.get("close") is not None:
                f.write(f"{day},{p['symbol']},{p['close']},{p['as_of']}\n")


# ---------- main ----------

def run(root, config, now, summarizer=None, fetch=fetch_feed, prices_fn=fetch_prices, log=print):
    tz = ZoneInfo(config.get("timezone", "Asia/Bangkok"))
    local_now = now.astimezone(tz)
    day = local_now.date()
    now_ts = now.timestamp()

    state_path = root / "data" / "state" / "seen.json"
    seen = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}

    taken_ids, taken_titles, categories = set(), set(), []
    for cat in config["categories"]:
        per_feed = [fetch(feed, log=log) for feed in cat["feeds"]]
        items = select_items(per_feed, now_ts, config.get("max_age_hours", 30), seen,
                             taken_ids, taken_titles, cat.get("max_items", 20))
        log(f"{cat['key']}: {sum(map(len, per_feed))} fetched, {len(items)} kept")
        categories.append({"key": cat["key"], "label": cat["label"], "items": items})

    failed = 0
    if summarizer is not None:
        batch = config["llm"].get("batch_size", 20)
        for cat in categories:
            failed += summarize_category(cat["items"], cat["label"], summarizer, batch, log=log)

    prices = prices_fn(config.get("prices", []), log=log)
    theme_prices = prices_fn(config["theme_stocks"], log=log) if config.get("theme_stocks") else []
    models = {it["model"] for c in categories for it in c["items"] if it.get("model")}

    month = day.strftime("%Y-%m")
    data_path = root / "data" / month / f"{day}.json"
    news_path = root / "news" / month / f"{day}.md"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    news_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "date": str(day),
        "collected_at": local_now.isoformat(timespec="seconds"),
        "models": sorted(models),
        "summary_failed": failed,
        "prices": prices,
        "theme_prices": theme_prices,
        "categories": categories,
        "title": config.get("title", "ข่าวประจำวัน"),
    }
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    news_path.write_text(render_markdown(day, local_now, prices, categories, models, failed, theme_prices,
                                         data["title"]), encoding="utf-8")
    append_price_history(root / "data" / "prices.csv", day, prices + theme_prices)

    # Only remember items that were summarised, so failed ones get retried tomorrow.
    keep_after = str(day - timedelta(days=config.get("seen_days", 14)))
    seen = {k: v for k, v in seen.items() if v > keep_after}
    for c in categories:
        for it in c["items"]:
            if summarizer is None or "summary_th" in it:
                seen[it["id"]] = str(day)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(seen, indent=0, sort_keys=True), encoding="utf-8")

    write_latest(root)
    total = sum(len(c["items"]) for c in categories)
    log(f"wrote {news_path.relative_to(root)}: {total} items, {failed} not summarised, models={sorted(models)}")
    return total, failed


# ---------- repair: fill summaries the free models missed ----------

def day_paths(root, day):
    month = day.strftime("%Y-%m")
    return root / "data" / month / f"{day}.json", root / "news" / month / f"{day}.md"


def write_pending(root, day, out):
    """Write the day's unsummarised items plus the clerk rules; return how many."""
    data_path, _ = day_paths(root, day)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    items = [{"id": it["id"], "category": c["label"], "title": it["title"], "source": it["source"],
              "text": it["text"]}
             for c in data["categories"] for it in c["items"] if "summary_th" not in it]
    out.write_text(json.dumps({"date": str(day), "rules": SYSTEM_PROMPT, "items": items},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    return len(items)


def save_day(root, day, data):
    """Write the day's data and re-render its digest from it."""
    data_path, news_path = day_paths(root, day)
    data_path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    news_path.write_text(render_markdown(day, datetime.fromisoformat(data["collected_at"]),
                                         data["prices"], data["categories"], set(data["models"]),
                                         data["summary_failed"], data.get("theme_prices", []),
                                         data.get("title", "ข่าวประจำวัน")), encoding="utf-8")


def apply_repair(root, day, reply, model="claude/routine"):
    """Merge summaries into the day's data, re-render the digest, mark items seen.

    Same checks as free-model replies (verify_numbers, tag/entity limits).
    Returns (fixed, still_missing).
    """
    data_path, news_path = day_paths(root, day)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    every = [it for c in data["categories"] for it in c["items"]]
    before = sum(1 for it in every if "summary_th" not in it)
    apply_summaries(every, reply, model)
    missing = sum(1 for it in every if "summary_th" not in it)
    data["summary_failed"] = missing
    data["models"] = sorted({it["model"] for it in every if it.get("model")})
    save_day(root, day, data)

    state_path = root / "data" / "state" / "seen.json"
    seen = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    for it in every:
        if "summary_th" in it:
            seen.setdefault(it["id"], str(day))
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(seen, indent=0, sort_keys=True), encoding="utf-8")
    return before - missing, missing


# ---------- review: Claude checks the free models' summaries against their source ----------

def write_review(root, day, out):
    """Write the day's summarised items not yet checked by Claude, plus the review rules; return how many."""
    data_path, _ = day_paths(root, day)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    items = [{"id": it["id"], "category": c["label"], "title": it["title"], "source": it["source"],
              "text": it["text"], "summary_th": it["summary_th"], "importance": it.get("importance", 1),
              "numbers": it.get("numbers", [])}
             for c in data["categories"] for it in c["items"]
             if "summary_th" in it and not it.get("checked_by") and not str(it.get("model", "")).startswith("claude/")]
    out.write_text(json.dumps({"date": str(day), "rules": REVIEW_PROMPT, "items": items},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    return len(items)


def apply_review(root, day, reply, model="claude/review"):
    """Apply Claude's corrections and mark the checked items; return (fixed, rejected).

    A new summary is rejected when it carries a figure that is not in the source (same rule as verify_numbers).
    """
    data = json.loads(day_paths(root, day)[0].read_text(encoding="utf-8"))
    by_id = {it["id"]: it for c in data["categories"] for it in c["items"] if "summary_th" in it}
    reply = reply if isinstance(reply, dict) else {}
    fixed = rejected = 0
    for f in reply.get("fixes") or []:
        it = by_id.get(str(f.get("id")))
        if it is None:
            continue
        source = it["title"] + " " + it["text"]
        changed = False
        summary = str(f.get("summary_th") or "").strip()
        if summary:
            if verify_numbers(digits(summary), source) != digits(summary):
                rejected += 1
                continue
            changed |= summary != it["summary_th"]
            it["summary_th"] = summary
        if "importance" in f:
            try:
                imp = max(0, min(3, int(f["importance"])))
                changed |= imp != it.get("importance")
                it["importance"] = imp
            except (TypeError, ValueError):
                pass
        if "numbers" in f:
            it["numbers"] = verify_numbers(f["numbers"], source)
        if changed:
            it["fixed_by"], it["fix_reason"] = model, str(f.get("reason") or "")[:200]
            fixed += 1
    for i in list(reply.get("checked") or []) + [f.get("id") for f in reply.get("fixes") or []]:
        if str(i) in by_id:
            by_id[str(i)]["checked_by"] = model
    save_day(root, day, data)
    return fixed, rejected


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-llm", action="store_true", help="fetch only, skip free-model summaries")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--config", type=Path, default=ROOT / "config" / "sources.yaml")
    ap.add_argument("--latest-only", action="store_true", help="just refresh LATEST.md (after writing an analysis)")
    ap.add_argument("--repair-pending", type=Path, metavar="OUT", help="write unsummarised items of --date to OUT")
    ap.add_argument("--repair-apply", type=Path, metavar="IN", help="merge summaries JSON from IN into --date")
    ap.add_argument("--review-pending", type=Path, metavar="OUT", help="write summarised items of --date for Claude to check")
    ap.add_argument("--review-apply", type=Path, metavar="IN", help="apply Claude's corrections JSON from IN to --date")
    ap.add_argument("--date", help="YYYY-MM-DD for --repair-*/--review-* (default: today, Thai time)")
    args = ap.parse_args(argv)

    if args.latest_only:
        write_latest(args.root)
        return 0
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    if args.repair_pending or args.repair_apply or args.review_pending or args.review_apply:
        tz = ZoneInfo(config.get("timezone", "Asia/Bangkok"))
        day = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else datetime.now(tz).date()
        if not day_paths(args.root, day)[0].exists():
            print(f"no data for {day} yet")
            return 3
        if args.review_pending:
            print(f"{write_review(args.root, day, args.review_pending)} items to check")
        elif args.review_apply:
            fixed, rejected = apply_review(args.root, day, json.loads(args.review_apply.read_text(encoding="utf-8")))
            print(f"corrected {fixed}, rejected {rejected} (figure not in the source)")
        elif args.repair_pending:
            print(f"{write_pending(args.root, day, args.repair_pending)} items need a summary")
        else:
            reply = json.loads(args.repair_apply.read_text(encoding="utf-8"))
            fixed, missing = apply_repair(args.root, day, reply)
            print(f"fixed {fixed}, still missing {missing}")
        return 0
    config["theme_stocks"] = load_theme_stocks(args.config.parent / "theme_stocks.yaml",
                                               skip={p["symbol"] for p in config.get("prices", [])})
    summarizer = None
    if not args.no_llm:
        summarizer = Summarizer(config["llm"])
        if not summarizer.available:
            print("::error::no GEMINI_API_KEY or OPENROUTER_API_KEY env; check repo secrets GEMINI / OPENROUTER")
            return 2
    total, failed = run(args.root, config, datetime.now().astimezone(), summarizer)
    if total and failed == total:
        print("::error::every summary failed; news saved as raw headlines")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
