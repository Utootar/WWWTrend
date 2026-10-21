"""Render a draft infographic (PNG) and a talking-anchor news video (MP4) from a content file.

Claude picks the stories and writes media/YYYY-MM-DD/content.json (facts and links
copied from news/ and data/ only, plus the narration text); this script only draws
and voices them. Drafts stay in media/ until the owner approves; nothing posts anywhere.

    python scripts/make_media.py media/2026-10-20/content.json
    python scripts/make_media.py media/2026-10-20/content.json --only poster

Needs: pip install playwright numpy edge-tts, a Chromium (CHROME env, else /opt/pw-browsers,
else Playwright's own) and ffmpeg. The Thai voice (edge-tts) needs internet, so the video is
rendered by .github/workflows/media-video.yml; render only the poster in sandboxes without it.
Fonts: assets/fonts (Kanit, OFL).
"""
import argparse
import base64
import html
import json
import os
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

from media_art import cover_art, scene_svg

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
DEFAULT_CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FPS = 30
W, H = 1080, 1920
GAP = 0.45          # silence between narration segments (seconds)
THAI_VOICE = os.environ.get("MEDIA_VOICE", "th-TH-NiwatNeural")   # edge-tts neural Thai voice
ESPEAK = ["espeak-ng", "-v", "th", "-s", "190", "-p", "42"]       # offline fallback, only with MEDIA_TTS=espeak

INK, PAPER, RED, YELLOW, TEAL = "#111111", "#f4f1ea", "#e63b2e", "#ffd23f", "#0f4a4a"
CARD_STYLES = [(TEAL, "#ffffff", YELLOW), (YELLOW, INK, RED), ("#ffffff", INK, TEAL)]
ART_BG = ["rgba(255,255,255,.14)", "#ffffff", YELLOW]


def esc(text):
    return html.escape(str(text))


def fmt_pct(p):
    return f"{'+' if p > 0 else '−' if p < 0 else ''}{abs(p):.2f}%"


def font_css():
    faces = [("Kanit-Light", 300), ("Kanit-Regular", 400), ("Kanit-SemiBold", 600), ("Kanit-Bold", 700)]
    # Embedded as data URIs: pages loaded with set_content cannot read file:// fonts.
    return "\n".join(
        f"@font-face{{font-family:Kanit;font-weight:{w};src:url(data:font/ttf;base64,"
        f"{base64.b64encode((FONTS / (n + '.ttf')).read_bytes()).decode()})}}"
        for n, w in faces)


def page(body, css=""):
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{font_css()}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Kanit,sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}}
{css}</style></head><body>{body}</body></html>"""


# ---------- drawings (inline SVG, no external images) ----------

def icon_svg(kind, fg, bg, size=150):
    shapes = {
        "chip": f"""<rect x="45" y="45" width="60" height="60" rx="8" fill="{fg}"/>
<g stroke="{fg}" stroke-width="6" stroke-linecap="round">{''.join(
            f'<line x1="{x}" y1="30" x2="{x}" y2="42"/><line x1="{x}" y1="108" x2="{x}" y2="120"/>'
            f'<line x1="30" y1="{x}" x2="42" y2="{x}"/><line x1="108" y1="{x}" x2="120" y2="{x}"/>'
            for x in (58, 75, 92))}</g>
<text x="75" y="83" text-anchor="middle" font-size="20" font-weight="700" fill="{bg}" font-family="Kanit">RAM</text>
<path d="M118 92 v26 m-10 -10 l10 12 l10 -12" stroke="{RED}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>""",
        "deal": f"""<g fill="{fg}"><rect x="34" y="42" width="56" height="18" rx="5"/><rect x="34" y="66" width="56" height="18" rx="5"/>
<rect x="34" y="90" width="56" height="18" rx="5"/></g><g fill="{bg}"><circle cx="46" cy="51" r="3.5"/><circle cx="46" cy="75" r="3.5"/><circle cx="46" cy="99" r="3.5"/></g>
<circle cx="104" cy="96" r="24" fill="{YELLOW}" stroke="{fg}" stroke-width="5"/>
<text x="104" y="106" text-anchor="middle" font-size="28" font-weight="700" fill="{INK}" font-family="Kanit">$</text>""",
        "code": f"""<path d="M58 50 L34 75 L58 100 M92 50 L116 75 L92 100" stroke="{fg}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M75 40 C88 58 70 64 80 80 C70 76 64 66 75 40 Z M70 92 h10 v20 h-10 z" fill="{RED}"/>""",
    }
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 150 150"><circle cx="75" cy="75" r="75" fill="{bg}"/>{shapes[kind]}</svg>"""


def hero_svg(scale=1.0):
    # Black-and-white "architecture" style: a giant chip block with a hard diagonal shadow.
    return f"""<svg viewBox="0 0 420 560" width="{420 * scale:.0f}" height="{560 * scale:.0f}">
<defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2f2f2"/><stop offset="1" stop-color="#9a9a9a"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a3a3a"/><stop offset="1" stop-color="#0d0d0d"/></linearGradient></defs>
<rect width="420" height="560" fill="#1b1b1b"/>
<polygon points="0,560 0,330 250,140 420,140 420,560" fill="#0b0b0b"/>
<polygon points="90,180 300,120 360,170 150,230" fill="url(#g1)"/>
<polygon points="150,230 360,170 360,400 150,460" fill="url(#g2)"/>
<polygon points="90,180 150,230 150,460 90,410" fill="#d8d8d8"/>
<g stroke="#bdbdbd" stroke-width="7" stroke-linecap="round">{''.join(
        f'<line x1="{150 + 42 * k}" y1="{230 - 12 * k + 40}" x2="{150 + 42 * k + 34}" y2="{230 - 12 * k + 30}"/>' for k in range(5))}</g>
<text x="255" y="330" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="54" fill="#f4f1ea" transform="rotate(-16 255 330)">CHIP</text>
<path d="M330 380 v120 m-34 -36 l34 40 l34 -40" stroke="{RED}" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def torn(color_top, color_bottom, flip=False):
    pts, x = [], 0
    rng = np.random.default_rng(7 if not flip else 11)
    while x <= W:
        pts.append(f"{x},{20 + rng.integers(-16, 17)}")
        x += int(rng.integers(18, 42))
    pts.append(f"{W},{20}")
    poly = " ".join(pts)
    return f"""<svg width="{W}" height="44" viewBox="0 0 {W} 44" style="display:block;background:{color_top}">
<polygon points="0,44 {poly} {W},44" fill="{color_bottom}"/></svg>"""


# ---------- poster ----------

POSTER_CSS = f"""
body{{width:{W}px;background:{PAPER};color:{INK}}}
.mast{{display:flex;justify-content:space-between;align-items:center;padding:34px 56px 26px;border-bottom:5px solid {INK}}}
.logo{{font-size:46px;font-weight:700;letter-spacing:-1px}}
.tabs{{display:flex;gap:30px;font-size:24px;font-weight:600}}
.tabs b{{border-bottom:4px solid {RED};color:{RED}}}
.label{{display:inline-block;background:{RED};color:#fff;font-size:22px;font-weight:600;letter-spacing:1px;padding:6px 16px}}
.card{{padding:34px 36px 32px 42px;display:grid;grid-template-columns:1fr 220px;gap:18px;align-items:center}}
.k{{font-size:20px;font-weight:600;letter-spacing:1px;opacity:.7;margin-bottom:4px}}
.pill{{display:inline-block;border-radius:999px;padding:6px 18px;font-size:21px;font-weight:600}}
"""


def card_html(s, i):
    bg, fg, accent = CARD_STYLES[i % 3]
    radius = "64px 64px 64px 14px" if i % 2 == 0 else "64px 14px 64px 64px"
    big_size = 92 if len(s["big"]) <= 6 else 58
    return f"""<div class="card" style="background:{bg};color:{fg};border-radius:{radius}">
<div><div style="display:flex;align-items:center;gap:16px"><span style="font-size:24px;font-weight:700;border:3px solid currentColor;border-radius:999px;padding:0 14px">0{i + 1}</span>
<div style="font-size:42px;font-weight:700;line-height:1.2">{esc(s['short'])}</div></div>
<div class="k" style="margin-top:16px">เกิดอะไรขึ้น</div>
<div style="font-size:25px;line-height:1.45">{esc(s['what'])}</div>
<div style="display:flex;align-items:baseline;gap:18px;margin-top:16px;flex-wrap:wrap">
<div style="font-size:{big_size}px;font-weight:700;line-height:1;color:{RED if bg != TEAL else YELLOW}">{esc(s['big'])}</div>
<div style="font-size:22px;opacity:.8">{esc(s['big_label'])}</div></div>
<div style="margin-top:16px;display:flex;gap:12px;flex-wrap:wrap;align-items:center">
<span class="pill" style="background:{fg};color:{bg}">สถานะ: {esc(s['status'])}</span>
<span style="font-size:21px;opacity:.8">ที่มา <b>{esc(s['source'])}</b></span></div></div>
<div style="align-self:start">{scene_svg(s['icon'], 220, ART_BG[i % 3])}</div>
{details_html(s, fg) if s.get('details') else ''}{views_html(s, fg) if s.get('views') else ''}
{theme_html(s, fg, bg) if s.get('theme') else ''}</div>"""


def conf_pill(v, size=18):
    label = "บันทึก" if v["confidence"] in ("", "—") else f"มั่นใจ {v['confidence']}"
    return f'<span class="pill" style="background:{RED};color:#fff;font-size:{size}px;white-space:nowrap">{esc(label)}</span>'


def view_sources(views):
    return " · ".join(dict.fromkeys(v["from"].split("/")[-1].removesuffix(".md") for v in views))


def views_html(s, fg):
    items = "".join(f'<div style="display:flex;gap:12px;align-items:flex-start;padding:6px 0">{conf_pill(v)}'
                    f'<div style="font-size:23px;line-height:1.45">{esc(v["text"])}</div></div>' for v in s["views"])
    return f"""<div style="grid-column:1/-1;border:3px dashed {fg}88;border-radius:26px;padding:14px 22px;margin-top:8px">
<div class="k">มุมมองจากบทวิเคราะห์ · ไม่ใช่ข้อเท็จจริง <span style="font-weight:400">({esc(view_sources(s['views']))})</span></div>{items}</div>"""


def pct_color(p, bg):
    if bg == TEAL:
        return "#7dffb8" if p >= 0 else "#ffb3a8"
    return "#1f9d63" if p >= 0 else RED


def theme_html(s, fg, bg):
    t = s["theme"]
    chips = "".join(f'<span style="background:{fg}1f;border-radius:999px;padding:5px 16px;font-size:21px;font-weight:600">'
                    f'{esc(x["label"])} <span style="color:{pct_color(x["pct"], bg)}">{fmt_pct(x["pct"])}</span></span>'
                    for x in t["stocks"])
    return f"""<div style="grid-column:1/-1;margin-top:10px"><div class="k">หุ้นในธีม: {esc(t['name'])} · ราคาปิดล่าสุด (ไม่ใช่คำแนะนำซื้อขาย)</div>
<div style="display:flex;gap:10px;flex-wrap:wrap">{chips}</div>
<div style="font-size:19px;opacity:.8;margin-top:8px">ความเสี่ยงของธีม: {esc(t['risk'])}</div></div>"""


def details_html(s, fg):
    rows = "".join(f"""<div style="display:grid;grid-template-columns:30px 1fr;gap:6px;padding:12px 0;border-top:2px solid {fg}33">
<div style="font-size:24px;font-weight:700">•</div><div style="font-size:24px;line-height:1.45">{esc(d['text'])}
<span style="font-size:19px;font-weight:600;opacity:.75;white-space:nowrap"> · {esc(d['source'])}</span></div></div>"""
                   for d in s["details"])
    return f"""<div style="grid-column:1/-1;margin-top:6px"><div class="k">ความเป็นมา · ข่าวที่เกี่ยวข้อง</div>{rows}</div>"""


def market_html(m):
    tiles = "".join(f"""<div style="flex:1 1 28%;background:#1c1c1c;border-radius:22px;padding:22px 24px">
<div style="font-size:22px;color:#bbb">{esc(it['label'])}</div>
<div style="font-size:42px;font-weight:700;color:{'#38d98f' if it['pct'] >= 0 else '#ff6b5e'}">{esc(it.get('value') or fmt_pct(it['pct']))}</div>
{f'<div style="font-size:19px;color:#999">{fmt_pct(it["pct"])}</div>' if it.get('value') else ''}</div>"""
                    for it in m["items"])
    return f"""<div style="color:#fff;font-size:30px;font-weight:700;margin-top:14px">{esc(m['title'])} <span style="font-size:21px;color:#999;font-weight:400">% เทียบวันก่อน · {esc(m['source_note'])}</span></div>
<div style="display:flex;gap:16px;flex-wrap:wrap">{tiles}</div>"""


def watch_html(m):
    rows = "".join(f'<div style="font-size:24px;line-height:1.45;padding:10px 0;border-top:2px solid #333;color:#eee">• {esc(w["text"])} '
                   f'<span style="color:#999;font-size:19px">· {esc(w["source"])}</span></div>' for w in m.get("watch", []))
    return f'<div style="color:#fff;font-size:30px;font-weight:700">จับตาต่อ <span style="font-size:21px;color:#999;font-weight:400">จากบทวิเคราะห์ล่าสุด</span></div>{rows}' if rows else ""


def mast_html(c, page_no=""):
    return f"""<div class="mast"><div class="logo">WWWTrend</div>
<div class="tabs"><span>หุ้น</span><span>เศรษฐกิจ</span><b>เทค</b></div>
<div style="font-size:24px;font-weight:600">{esc(c['date_th'])}{f' · {page_no}' if page_no else ''}</div></div>"""


def footer_html(c):
    return f"""<div style="padding:26px 56px 44px;display:flex;justify-content:space-between;align-items:center;gap:24px">
<div style="font-size:21px;line-height:1.5;color:#444">{esc(c['footer'])}<br>ที่มา: {esc(' · '.join(dict.fromkeys(s['source'] for s in c['stories'])))}</div>
<div class="logo" style="font-size:30px">WWWTrend</div></div>"""


def band(inner):
    return f"""<div style="background:{INK};padding:32px 56px 36px;display:flex;flex-direction:column;gap:22px;flex:1">{inner}</div>"""


def closing_html():
    checks = "".join(f'<div style="font-size:24px;padding:7px 0;border-top:2px solid {INK}">✓ {t}</div>' for t in (
        "ตัวเลขทุกตัวมาจากหัวข่าวหรือตารางราคาในไฟล์ข่าว",
        "ตัวเลขสำคัญ กดลิงก์ต้นทางเช็คก่อนใช้ (ลิงก์ครบใน sources.md)",
        "เรานำข่าวมาเล่าให้ฟังเท่านั้น"))
    return f"""<div style="background:{YELLOW};color:{INK};border-radius:64px 14px 64px 64px;padding:24px 40px 22px">
<div style="font-size:24px;font-weight:600;color:{RED}">ก่อนปิดชุดนี้</div>
<div style="font-size:50px;font-weight:700;line-height:1.1;margin:4px 0 12px">เช็คก่อนใช้ข้อมูล</div>{checks}</div>"""


def band_title(text):
    return f"""<div style="color:#fff;font-size:34px;font-weight:700">{text}</div>"""


def hero_html(c, compact=False):
    head = "<br>".join(esc(x) for x in c["headline"])
    scale = 0.72 if compact else 1.0
    return f"""<div style="display:grid;grid-template-columns:1fr {420 * scale:.0f}px;gap:34px;padding:{'34px 56px 36px' if compact else '44px 56px 54px'}">
<div><span class="label">ข่าวเด่นวันนี้ · {len(c['stories'])} เรื่อง</span>
<div style="font-size:{76 if compact else 88}px;font-weight:700;line-height:1.08;letter-spacing:-2px;margin-top:22px">{head}</div>
<div style="font-size:28px;line-height:1.5;margin-top:26px;color:#333">{esc(c['dek'])}</div>
<div style="display:flex;align-items:center;gap:16px;margin-top:30px">
<div style="width:46px;height:46px;background:{INK}"></div>
<div style="font-size:20px;font-weight:600;letter-spacing:1px;line-height:1.4">เล่าข่าวโดย WWWTrend<br><span style="color:{RED}">นำข่าวมาเล่าตามที่ข่าวรายงาน</span></div></div></div>
<div style="align-self:center">{cover_art(int(420 * scale), int(560 * scale), [s['icon'] for s in c['stories']])}</div></div>"""


def poster_html(c):
    """One long image: everything stacked."""
    cards = "".join(card_html(s, i) for i, s in enumerate(c["stories"]))
    return (mast_html(c) + hero_html(c) + torn(PAPER, INK)
            + band(band_title(f'สรุปให้ทีละเรื่อง <span style="color:{YELLOW}">· อ่านแค่ตรงนี้ก็รู้เรื่อง</span>')
                   + cards + market_html(c["market"]))
            + torn(INK, PAPER, True) + footer_html(c))


def carousel_html(c):
    """Swipeable set of 1080x1350 slides: cover, one slide per story, then market + closing."""
    stories = list(enumerate(c["stories"]))
    total = len(stories) + 2
    topics = "".join(f'<div style="color:#fff;font-size:40px;font-weight:600;padding:16px 0;border-top:2px solid #333">'
                     f'<span style="color:{YELLOW}">0{i + 1}</span> · {esc(s["short"])}</div>' for i, s in stories)
    pages = [mast_html(c, f"1/{total}") + hero_html(c, compact=True) + torn(PAPER, INK)
             + band(band_title(f'ในชุดนี้ <span style="color:{YELLOW}">· ปัดเพื่ออ่านต่อ →</span>') + topics)
             + footer_html(c)]
    for i, s in stories:
        pages.append(mast_html(c, f"{i + 2}/{total}")
                     + band(card_html(s, i))
                     + footer_html(c))
    pages.append(mast_html(c, f"{total}/{total}")
                 + band(band_title(f'สรุปตลาด <span style="color:{YELLOW}">· ก่อนปิดชุดนี้</span>')
                        + f'<div style="display:flex;flex-direction:column;gap:22px">{market_html(c["market"]) + (f'<div style="color:#fff">{views_html(c["market"], "#ffffff")}</div>' if c["market"].get("views") else "") + watch_html(c["market"]) + ("" if c["market"].get("watch") else closing_html())}</div>')
                 + footer_html(c))
    return pages


# ---------- talking-anchor video ----------

def anchor_svg():
    skin, hair, suit = "#f1c6a0", "#2b2118", "#1f2a44"
    return f"""<svg id="anchor" viewBox="0 0 1080 760" width="1080" height="760" style="position:absolute;left:0;top:1000px">
<g id="body">
<path d="M250 760 C260 560 360 520 540 520 C720 520 820 560 830 760 Z" fill="{suit}"/>
<path d="M470 520 L540 640 L610 520 Z" fill="#fff"/>
<path d="M528 548 L552 548 L560 660 L540 690 L520 660 Z" fill="{RED}"/>
<path d="M470 520 L540 640 L430 600 Z M610 520 L540 640 L650 600 Z" fill="#162036"/>
<rect x="505" y="440" width="70" height="95" rx="24" fill="{skin}"/>
<g id="head">
<ellipse cx="392" cy="330" rx="26" ry="40" fill="{skin}"/><ellipse cx="688" cy="330" rx="26" ry="40" fill="{skin}"/>
<ellipse cx="540" cy="320" rx="150" ry="172" fill="{skin}"/>
<path d="M388 300 C380 160 470 118 552 120 C650 122 712 180 694 300 C676 236 640 214 590 206 C540 236 456 238 414 228 C400 250 394 270 388 300 Z" fill="{hair}"/>
<g id="brows" fill="{hair}"><rect x="450" y="262" width="62" height="13" rx="6"/><rect x="568" y="262" width="62" height="13" rx="6"/></g>
<g id="eyes"><ellipse cx="481" cy="315" rx="22" ry="20" fill="#fff"/><ellipse cx="599" cy="315" rx="22" ry="20" fill="#fff"/>
<circle cx="484" cy="318" r="12" fill="#2a1d14"/><circle cx="602" cy="318" r="12" fill="#2a1d14"/>
<circle cx="488" cy="313" r="4" fill="#fff"/><circle cx="606" cy="313" r="4" fill="#fff"/></g>
<path d="M540 330 C532 365 528 378 542 382" stroke="#d9a07c" stroke-width="6" fill="none" stroke-linecap="round"/>
<ellipse cx="450" cy="390" rx="26" ry="14" fill="#f2a08c" opacity=".55"/><ellipse cx="630" cy="390" rx="26" ry="14" fill="#f2a08c" opacity=".55"/>
<g id="mouth"><ellipse id="lip" cx="540" cy="418" rx="40" ry="6" fill="#8a2e2e"/>
<rect id="teeth" x="514" y="410" width="52" height="8" rx="3" fill="#fff"/></g>
</g></g>
<rect x="60" y="640" width="960" height="120" rx="18" fill="#0d1526"/>
<rect x="60" y="640" width="960" height="10" fill="{RED}"/>
</svg>"""


VIDEO_CSS = f"""
body{{width:{W}px;height:{H}px;position:relative;background:#0b1424;color:#fff}}
.studio{{position:absolute;inset:0;background:radial-gradient(circle at 50% 70%,#24406e 0%,#0b1424 60%)}}
.studio:before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.035) 0 2px,transparent 2px 120px)}}
.bug{{position:absolute;left:56px;top:56px;display:flex;align-items:center;gap:14px;font-size:38px;font-weight:700}}
.bug i{{background:{RED};font-style:normal;font-size:24px;padding:4px 14px;border-radius:6px}}
.screen{{position:absolute;left:56px;right:56px;top:150px;height:820px;border-radius:36px;background:{PAPER};color:{INK};overflow:hidden;
  box-shadow:0 30px 80px rgba(0,0,0,.5)}}
.panel{{position:absolute;inset:0;padding:56px 60px;display:flex;flex-direction:column;opacity:0}}
.cap{{position:absolute;left:56px;right:56px;top:1610px;min-height:150px;background:rgba(0,0,0,.82);border-left:10px solid {YELLOW};
  border-radius:16px;padding:20px 28px;font-size:34px;line-height:1.4;font-weight:600}}
.pill{{display:inline-block;border-radius:999px;padding:6px 18px;font-weight:600;line-height:1.3}}
.tick{{position:absolute;left:0;right:0;bottom:0;height:86px;background:{RED};overflow:hidden;display:flex;align-items:center}}
.tick div{{white-space:nowrap;font-size:32px;font-weight:600;position:absolute;left:0}}
"""


def panel_html(seg, c):
    kind = seg["kind"]
    if kind == "intro":
        items = "".join(f'<div style="font-size:40px;font-weight:600;padding:14px 0;border-top:3px solid {INK}">0{i + 1} · {esc(s["short"])}</div>'
                        for i, s in enumerate(c["stories"]))
        return f"""<div style="display:flex;justify-content:space-between"><span style="background:{RED};color:#fff;font-size:28px;font-weight:600;padding:6px 18px">สรุปข่าวเด่น</span>
<span style="font-size:30px;font-weight:600">{esc(c['date_th'])}</span></div>
<div style="font-size:96px;font-weight:700;line-height:1.08;letter-spacing:-2px;margin:40px 0">{'<br>'.join(esc(x) for x in c['headline'])}</div>
<div style="margin-top:auto">{items}</div>"""
    if kind in ("disclaimer", "outro"):
        return f"""<div style="margin:auto 0"><div style="font-size:34px;font-weight:600;color:{RED}">{'ขอบอกก่อน' if kind == 'disclaimer' else 'ก่อนจากกัน'}</div>
<div style="font-size:110px;font-weight:700;line-height:1.1;letter-spacing:-2px;margin:24px 0">{'เล่าข่าว<br>ตามที่<br>ข่าวรายงาน' if kind == 'disclaimer' else 'เช็ค<br>ก่อนใช้<br>ข้อมูล'}</div>
<div style="font-size:38px;line-height:1.45">{'เราแค่นำข่าวมาเล่าให้ฟัง ตามที่ข่าวรายงาน' if kind == 'disclaimer' else 'ตัวเลขสำคัญ กดลิงก์ต้นทางเช็คก่อน · ลิงก์ครบใน sources.md'}</div></div>"""
    if kind == "view":
        s, i = seg["story"], seg["index"]
        items = "".join(f'<div style="display:flex;gap:18px;align-items:flex-start;padding:16px 0;border-top:3px solid {INK}">{conf_pill(v, 26)}'
                        f'<div style="font-size:38px;line-height:1.4">{esc(v["text"])}</div></div>' for v in s["views"])
        t = s.get("theme")
        chips = "".join(f'<span style="background:#e2ddd2;border-radius:999px;padding:8px 20px;font-size:28px;font-weight:600">{esc(x["label"])} '
                        f'<span style="color:{pct_color(x["pct"], PAPER)}">{fmt_pct(x["pct"])}</span></span>' for x in t["stocks"]) if t else ""
        return f"""<span style="background:{RED};color:#fff;font-size:28px;font-weight:600;padding:6px 18px;align-self:flex-start">มุมมองจากบทวิเคราะห์ · ไม่ใช่ข้อเท็จจริง</span>
<div style="font-size:60px;font-weight:700;line-height:1.15;margin:26px 0 20px">ข่าว {i + 1}: {esc(s['short'])}</div>{items}
{f'<div style="font-size:28px;font-weight:600;margin-top:24px">หุ้นในธีม {esc(t["name"])}</div><div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:12px">{chips}</div>' if t else ''}
<div style="margin-top:auto;font-size:24px;color:#555">จาก {esc(view_sources(s['views']))}</div>"""
    if kind == "market":
        m = c["market"]
        peak = max(abs(i["pct"]) for i in m["items"]) or 1
        rows = "".join(f"""<div style="display:grid;grid-template-columns:260px 1fr 170px;gap:20px;align-items:center">
<div style="font-size:36px;font-weight:600">{esc(it['label'])}</div>
<div style="height:34px;background:#e2ddd2;border-radius:17px;position:relative">
<div class="bar" data-w="{abs(it['pct']) / peak * 100:.1f}" style="position:absolute;left:0;top:0;bottom:0;width:0;border-radius:17px;background:{'#1f9d63' if it['pct'] >= 0 else RED}"></div></div>
<div style="font-size:42px;font-weight:700;text-align:right;color:{'#1f9d63' if it['pct'] >= 0 else RED}">{esc(it.get('value') or fmt_pct(it['pct']))}</div></div>"""
                       for it in m["items"])
        return f"""<span style="background:{INK};color:#fff;font-size:28px;font-weight:600;padding:6px 18px;align-self:flex-start">ตลาด</span>
<div style="font-size:84px;font-weight:700;margin:30px 0 40px">{esc(m['title'])}</div>
<div style="display:flex;flex-direction:column;gap:44px">{rows}</div>
<div style="margin-top:auto;font-size:26px;color:#555">% เทียบวันก่อน · {esc(m['source_note'])}</div>"""
    s, i = seg["story"], seg["index"]
    bg, fg, accent = CARD_STYLES[i % 3]
    return f"""<div style="font-size:30px;font-weight:600;color:{RED}">ข่าว {i + 1}/{len(c['stories'])} · ที่มา {esc(s['source'])}</div>
<div style="font-size:58px;font-weight:700;line-height:1.15">{esc(s['short'])}</div>
<div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px">
<div><div style="font-size:{140 if len(s['big']) <= 6 else 76}px;font-weight:700;line-height:1;color:{RED};letter-spacing:-3px">{esc(s['big'])}</div>
<div style="font-size:30px;color:#555;margin-top:10px">{esc(s['big_label'])}</div></div>
{scene_svg(s['icon'], 330, ART_BG[(i + 1) % 3] if i % 3 != 2 else YELLOW)}</div>
<div style="font-size:36px;line-height:1.45;margin-top:18px">{esc(s['what'])}</div>
<div style="margin-top:auto"><span style="display:inline-block;background:{INK};color:#fff;border-radius:999px;padding:10px 26px;font-size:28px;font-weight:600">สถานะ: {esc(s['status'])}</span></div>"""


def video_segments(c):
    segs = [{"kind": "intro", **c["intro"]}, {"kind": "disclaimer", **c["disclaimer"]}]
    for i, s in enumerate(c["stories"]):
        segs.append({"kind": "story", "story": s, "index": i, "say": s["say"], "caption": s["caption"]})
        if s.get("view_say"):
            segs.append({"kind": "view", "story": s, "index": i, "say": s["view_say"], "caption": s["view_caption"]})
    segs += [{"kind": "market", "say": c["market"]["say"], "caption": c["market"]["caption"]},
             {"kind": "outro", **c["outro"]}]
    return segs


def tts(text, wav):
    """Thai speech to a mono 16-bit wav. Default edge-tts (needs internet, runs in GitHub Actions);
    espeak-ng only when MEDIA_TTS=espeak because it cannot really read Thai."""
    if os.environ.get("MEDIA_TTS") == "espeak":
        subprocess.run(ESPEAK + ["-w", str(wav), text], check=True)
        return
    mp3 = wav.with_suffix(".mp3")
    # Separate process: Playwright's sync API already runs an event loop in this one.
    r = subprocess.run([sys.executable, "-m", "edge_tts", "--voice", THAI_VOICE, "--rate=+8%",
                        "--text", text, "--write-media", str(mp3)], capture_output=True, text=True)
    if r.returncode or not mp3.exists():
        sys.exit(f"Thai voice failed ({(r.stderr or '').strip()[-300:]}). The video needs edge-tts with internet: "
                 "push content.json and let the 'Render media video' workflow make it.")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-ac", "1", "-ar", "24000",
                    "-c:a", "pcm_s16le", str(wav)], check=True)


def synth(segs, tmp):
    """Voice each segment; return mono samples, rate, and segment start/end times."""
    chunks, rate, t = [], None, 0.0
    for k, seg in enumerate(segs):
        f = tmp / f"seg{k}.wav"
        tts(seg["say"], f)
        with wave.open(str(f)) as w:
            rate = w.getframerate()
            data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        seg["start"], seg["end"] = t, t + len(data) / rate
        chunks += [data, np.zeros(int(GAP * rate), dtype=np.int16)]
        t = seg["end"] + GAP
    return np.concatenate(chunks), rate


def mouth_curve(samples, rate, frames):
    hop = rate / FPS
    rms = np.array([np.sqrt(np.mean(samples[int(n * hop):int((n + 1) * hop)].astype(np.float64) ** 2) or 0)
                    for n in range(frames)])
    level = np.clip(rms / (np.percentile(rms[rms > 0], 90) if (rms > 0).any() else 1), 0, 1)
    return np.convolve(level, [0.25, 0.5, 0.25], mode="same")


def write_audio(samples, rate, path):
    raw = path.with_suffix(".raw.wav")
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(samples.tobytes())
    dur = len(samples) / rate
    # Soft pad under the voice (A minor triad, slow swell) so the clip is not dead quiet.
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                    "-f", "lavfi", "-t", f"{dur:.2f}", "-i",
                    "aevalsrc=0.05*(sin(2*PI*220*t)+sin(2*PI*261.63*t)+sin(2*PI*329.63*t))*(0.6+0.4*sin(2*PI*0.1*t)):s=44100",
                    "-filter_complex",
                    "[0]aresample=44100,highpass=f=90,lowpass=f=7000,acompressor,volume=1.8[v];"
                    "[1]lowpass=f=900,volume=0.35[m];[v][m]amix=inputs=2:duration=first:normalize=0",
                    "-c:a", "pcm_s16le", str(path)], check=True)
    raw.unlink()


def video_html(c, segs):
    panels = "".join(f'<div class="panel" data-start="{s["start"]:.3f}" data-end="{s["end"] + GAP:.3f}">{panel_html(s, c)}</div>'
                     for s in segs)
    caps = json.dumps([[s["start"], s["end"] + GAP, s["caption"]] for s in segs], ensure_ascii=False)
    ticker = esc(f"  WWWTrend นำข่าวมาเล่าให้ฟัง  ·  {c['footer']}  ·  ") * 4
    return f"""<div class="studio"></div>
<div class="bug">WWWTrend <i>สรุปข่าว</i></div>
<div class="screen">{panels}</div>
{anchor_svg()}
<div class="cap" id="cap"></div>
<div class="tick"><div id="tk">{ticker}</div></div>
<script>
const caps = {caps};
const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3);
function render(t, m) {{
  document.querySelectorAll('.panel').forEach(p => {{
    const a = +p.dataset.start, b = +p.dataset.end, on = t >= a && t < b;
    const k = ease((t - a) / 0.5);
    p.style.opacity = on ? k : 0;
    p.style.transform = 'translateX(' + (1 - k) * 80 + 'px)';
    if (on) p.querySelectorAll('.bar').forEach((el, i) => el.style.width = (+el.dataset.w * ease((t - a - 0.4 - i * 0.35) / 0.8)) + '%');
  }});
  const cap = caps.find(x => t >= x[0] && t < x[1]);
  document.getElementById('cap').textContent = cap ? cap[2] : '';
  document.getElementById('lip').setAttribute('ry', 6 + 30 * m);
  document.getElementById('lip').setAttribute('rx', 40 - 8 * m);
  document.getElementById('teeth').style.opacity = m > 0.25 ? 1 : 0;
  const blink = (t % 3.7) < 0.12 ? 0.1 : 1;
  document.getElementById('eyes').setAttribute('transform', 'translate(0 ' + 315 * (1 - blink) + ') scale(1 ' + blink + ')');
  document.getElementById('brows').setAttribute('transform', 'translate(0 ' + (-6 * m) + ')');
  document.getElementById('head').setAttribute('transform', 'rotate(' + (Math.sin(t * 1.3) * 2.2 + m * 1.5) + ' 540 480)');
  document.getElementById('body').setAttribute('transform', 'translate(0 ' + Math.sin(t * 1.7) * 4 + ')');
  const tk = document.getElementById('tk');
  tk.style.transform = 'translateX(' + (-(t * 140) % (tk.scrollWidth / 4)) + 'px)';
}}
</script>"""


def launch(p):
    exe = os.environ.get("CHROME") or (DEFAULT_CHROME if Path(DEFAULT_CHROME).exists() else None)
    return p.chromium.launch(executable_path=exe, args=["--no-sandbox"])


def render_poster(browser, c, out_dir, date):
    outs = [out_dir / f"infographic-{date}.png"]
    pg = browser.new_page(viewport={"width": W, "height": 1000})
    pg.set_content(page(poster_html(c), POSTER_CSS))
    pg.evaluate("document.fonts.ready")
    pg.screenshot(path=str(outs[0]), full_page=True)
    pg.close()
    css = POSTER_CSS + "body{height:1350px;display:flex;flex-direction:column}"
    for n, body in enumerate(carousel_html(c), 1):
        outs.append(out_dir / f"slide-{date}-{n}.png")
        pg = browser.new_page(viewport={"width": W, "height": 1350})
        pg.set_content(page(body, css))
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(outs[-1]))
        pg.close()
    return outs


def render_video(browser, c, out):
    segs = video_segments(c)
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        samples, rate = synth(segs, tmp)
        frames = int(len(samples) / rate * FPS)
        mouth = mouth_curve(samples, rate, frames)
        audio = tmp / "voice.wav"
        write_audio(samples, rate, audio)
        pg = browser.new_page(viewport={"width": W, "height": H})
        pg.set_content(page(video_html(c, segs), VIDEO_CSS))
        pg.evaluate("document.fonts.ready")
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
                               "-i", "-", "-i", str(audio), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                               "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out)],
                              stdin=subprocess.PIPE)
        for n in range(frames):
            pg.evaluate(f"render({n / FPS}, {mouth[n]:.3f})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=90))
        ff.stdin.close()
        if ff.wait():
            sys.exit("ffmpeg failed")
        pg.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content", type=Path)
    ap.add_argument("--only", choices=["poster", "video"])
    args = ap.parse_args()
    c = json.loads(args.content.read_text(encoding="utf-8"))
    out_dir, date = args.content.parent, c["date"]
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = launch(p)
        if args.only != "video":
            for f in render_poster(browser, c, out_dir, date):
                print(f)
        if args.only != "poster":
            render_video(browser, c, out_dir / f"video-{date}.mp4")
            print(out_dir / f"video-{date}.mp4")
        browser.close()


if __name__ == "__main__":
    main()
