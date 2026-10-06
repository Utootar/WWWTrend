import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import collect  # noqa: E402
from llm import LLMError, ModelGone, RateLimited, Summarizer, parse_json  # noqa: E402

NOW = datetime(2026, 10, 7, 0, 5, tzinfo=timezone.utc)  # 07:05 Bangkok
HOUR = 3600

RSS = """<?xml version="1.0"?><rss version="2.0"><channel><title>t</title>
<item><title>Gold hits $4,190 as dollar slips - Reuters</title>
<link>https://example.com/gold?utm_source=x&amp;id=7</link>
<pubDate>Tue, 06 Oct 2026 20:00:00 GMT</pubDate>
<description>&lt;p&gt;Spot gold rose 0.8% to $4,190.30 an ounce.&lt;/p&gt;</description>
<source url="https://reuters.com">Reuters</source></item>
</channel></rss>"""


def item(n, hours_ago, feed="A", title=None):
    link = f"https://news.example/{feed}/{n}"
    return {"id": collect.item_id(link), "title": title or f"{feed} story {n}", "link": link,
            "source": feed, "published": NOW.timestamp() - hours_ago * HOUR,
            "text": f"Text {n} says revenue rose 12% to $3.4 billion."}


def test_parse_feed_strips_tracking_and_uses_publisher():
    [it] = collect.parse_feed(RSS.encode(), "Google News")
    assert it["source"] == "Reuters"
    assert it["title"] == "Gold hits $4,190 as dollar slips"
    assert it["link"] == "https://example.com/gold?id=7"
    assert it["text"] == "Spot gold rose 0.8% to $4,190.30 an ounce."


def test_select_round_robin_dedupes_and_drops_old():
    busy = [item(i, i, "A") for i in range(10)]
    quiet = [item(0, 2, "B"), item(1, 40, "B")]  # second one too old
    dup_title = [item(9, 1, "C", title="A story 0")]
    seen = {busy[1]["id"]: "2026-10-06"}
    out = collect.select_items([busy, quiet, dup_title], NOW.timestamp(), 30, seen, set(), set(), 4)
    assert [it["link"] for it in out] == [
        "https://news.example/A/0", "https://news.example/B/0",
        "https://news.example/A/2", "https://news.example/A/3"]


def test_select_skips_ids_taken_by_earlier_category():
    a = item(0, 1)
    taken = {a["id"]}
    assert collect.select_items([[a]], NOW.timestamp(), 30, {}, taken, set(), 5) == []


def test_verify_numbers_drops_invented_figures():
    src = "Spot gold rose 0.8% to $4,190.30 an ounce."
    assert collect.verify_numbers(["$4,190.30", "0.8%", "$5,000", "up 3%", "record"], src) == \
        ["$4,190.30", "0.8%"]


def test_parse_json_handles_fences_and_chatter():
    assert parse_json('Sure!\n```json\n{"items": []}\n```') == {"items": []}
    with pytest.raises(LLMError):
        parse_json("no json here")


class FakeSummarizer:
    def __init__(self, fail_labels=()):
        self.fail_labels = fail_labels
        self.calls = 0

    def run(self, system, prompt):
        self.calls += 1
        label = prompt.split("\n")[0].removeprefix("Category: ")
        if label in self.fail_labels:
            raise LLMError("down")
        payload = json.loads(prompt.split("News items:\n", 1)[1])
        items = [{"id": p["id"], "importance": 2, "summary_th": f"สรุป {p['title']}",
                  "numbers": ["12%", "$9.9 billion"], "tags": ["Earnings"], "entities": ["X"]}
                 for p in payload]
        items.append({"id": "not-a-real-id", "importance": 3, "summary_th": "แต่งขึ้น"})
        return {"items": items}, "fake/model"


def make_config():
    return {
        "timezone": "Asia/Bangkok", "max_age_hours": 30, "seen_days": 14,
        "llm": {"batch_size": 2},
        "prices": [{"symbol": "GC=F", "label": "ทองคำ"}],
        "categories": [
            {"key": "a", "label": "หมวดเอ", "max_items": 3, "feeds": [{"name": "A", "url": "a"}]},
            {"key": "b", "label": "หมวดบี", "max_items": 3, "feeds": [{"name": "B", "url": "b"}]},
        ],
    }


def fake_fetch(feed, log=print):
    return [item(i, i + 1, feed["name"]) for i in range(3)]


def fake_prices(tickers, log=print):
    return [{"symbol": "GC=F", "label": "ทองคำ", "close": 4190.3, "prev_close": 4156.0,
             "change_pct": 0.83, "as_of": "2026-10-06", "currency": "USD"}]


def test_run_writes_digest_data_state_and_latest(tmp_path):
    summ = FakeSummarizer(fail_labels=("หมวดบี",))
    total, failed = collect.run(tmp_path, make_config(), NOW, summ, fake_fetch, fake_prices, log=lambda m: None)
    assert (total, failed) == (6, 3)
    assert summ.calls == 4  # 2 batches per category

    data = json.loads((tmp_path / "data/2026-10/2026-10-07.json").read_text(encoding="utf-8"))
    a_items = data["categories"][0]["items"]
    assert all(it["summary_th"].startswith("สรุป") for it in a_items)
    assert all(it["numbers"] == ["12%"] for it in a_items)  # invented $9.9 billion dropped
    assert all(it["tags"] == ["earnings"] for it in a_items)
    assert data["summary_failed"] == 3

    md = (tmp_path / "news/2026-10/2026-10-07.md").read_text(encoding="utf-8")
    assert "# ข่าวประจำวัน 7 ต.ค. 2026" in md
    assert "| ทองคำ | 4,190.30 | +0.83% |" in md
    assert "**ย่อไม่สำเร็จ 3 ข่าว**" in md
    assert "B story 0 — [B](https://news.example/B/0)" in md  # raw headline fallback
    assert "แต่งขึ้น" not in md

    seen = json.loads((tmp_path / "data/state/seen.json").read_text(encoding="utf-8"))
    assert len(seen) == 3  # failed category retried tomorrow
    assert "news/2026-10/2026-10-07.md" in (tmp_path / "LATEST.md").read_text(encoding="utf-8")
    assert (tmp_path / "data/prices.csv").read_text(encoding="utf-8").splitlines()[1] == \
        "2026-10-07,GC=F,4190.3,2026-10-06"


def test_theme_stocks_are_loaded_priced_and_rendered(tmp_path):
    f = tmp_path / "theme_stocks.yaml"
    f.write_text("stocks:\n"
                 "  - {symbol: GULF.BK, label: GULF, theme: ไฟฟ้าจาก AI}\n"
                 "  - {symbol: GC=F, label: dup}\n"
                 "  - {symbol: GULF.BK, label: again}\n"
                 "  - {label: no symbol}\n", encoding="utf-8")
    stocks = collect.load_theme_stocks(f, skip={"GC=F"})
    assert stocks == [{"symbol": "GULF.BK", "label": "GULF · ไฟฟ้าจาก AI"}]
    assert collect.load_theme_stocks(tmp_path / "missing.yaml") == []

    def echo_prices(tickers, log=print):
        return [{"symbol": t["symbol"], "label": t["label"], "close": 50.0, "prev_close": 49.0,
                 "change_pct": 2.04, "as_of": "2026-10-06"} for t in tickers]

    config = make_config() | {"theme_stocks": stocks}
    collect.run(tmp_path, config, NOW, None, fake_fetch, echo_prices, log=lambda m: None)
    md = (tmp_path / "news/2026-10/2026-10-07.md").read_text(encoding="utf-8")
    assert "## ราคาหุ้นในธีมที่เจอจากข่าว" in md
    assert "| GULF · ไฟฟ้าจาก AI | 50.00 | +2.04% |" in md
    data = json.loads((tmp_path / "data/2026-10/2026-10-07.json").read_text(encoding="utf-8"))
    assert data["theme_prices"][0]["symbol"] == "GULF.BK"
    assert "2026-10-07,GULF.BK,50.0,2026-10-06" in (tmp_path / "data/prices.csv").read_text(encoding="utf-8")


def test_summarizer_falls_back_and_skips_dead_models():
    calls = []

    def gemini(model, system, prompt, key):
        calls.append(model)
        if model == "g1":
            raise ModelGone("404")
        raise RateLimited("429", 5)

    def openrouter(model, system, prompt, key):
        calls.append(model)
        return '{"items": []}'

    cfg = {"providers": [{"provider": "gemini", "models": ["g1", "g2"]},
                         {"provider": "openrouter", "models": ["o1"]}]}
    s = Summarizer(cfg, env={"GEMINI_API_KEY": "k", "OPENROUTER_API_KEY": "k"},
                   callers={"gemini": gemini, "openrouter": openrouter},
                   sleep=lambda s: None, log=lambda m: None)
    assert s.run("sys", "p") == ({"items": []}, "openrouter/o1")
    assert calls == ["g1", "g2", "g2", "o1"]  # g2 retried once after 429
    calls.clear()
    s.run("sys", "p")
    assert calls[0] == "g2"  # g1 not tried again this run


def test_summarizer_without_keys_is_unavailable():
    cfg = {"providers": [{"provider": "gemini", "models": ["g"]}]}
    assert not Summarizer(cfg, env={}, log=lambda m: None).available
