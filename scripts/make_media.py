"""Render a draft infographic (PNG) and short vertical video (MP4) from a content file.

Claude picks the stories and writes media/YYYY-MM-DD/content.json (facts and links
copied from news/ and data/ only); this script only draws them. Drafts stay in
media/ until the owner approves; nothing here posts anywhere.

    python scripts/make_media.py media/2026-10-20/content.json
    python scripts/make_media.py media/2026-10-20/content.json --only poster

Needs: pip install playwright, a Chromium (CHROME env, else /opt/pw-browsers, else
Playwright's own), and ffmpeg on PATH. Fonts: assets/fonts (Kanit, OFL).
"""
import argparse
import base64
import html
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
DEFAULT_CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FPS = 30
POSTER_W, POSTER_H = 1080, 1620
DISCLAIMER = "ไม่ใช่คำแนะนำการลงทุน"
COLORS = {"red": "#ff5d6c", "gold": "#ffc24b", "green": "#34e0a1", "blue": "#6aa8ff"}

# Video timeline in seconds: intro, one scene per story, market, outro.
INTRO, STORY, MARKET, OUTRO = 3.0, 5.0, 4.0, 3.5


def esc(text):
    return html.escape(str(text))


def color(name):
    return COLORS.get(name or "", "#f3f6fc")


def fmt_pct(p):
    return f"{'+' if p > 0 else '−' if p < 0 else ''}{abs(p):.2f}%"


def font_css():
    faces = [("Kanit-Light", 300), ("Kanit-Regular", 400), ("Kanit-SemiBold", 600), ("Kanit-Bold", 700)]
    return "\n".join(
        # Embedded as data URIs: pages loaded with set_content cannot read file:// fonts.
        f"@font-face{{font-family:Kanit;font-weight:{w};src:url(data:font/ttf;base64,"
        f"{base64.b64encode((FONTS / (n + '.ttf')).read_bytes()).decode()})}}"
        for n, w in faces)


BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#070b16;overflow:hidden}
body{font-family:Kanit,sans-serif;color:#f3f6fc;-webkit-font-smoothing:antialiased}
.bg{position:absolute;inset:0;overflow:hidden;background:#070b16}
.bg:before{content:"";position:absolute;inset:0;
  background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),
  linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:54px 54px}
.glow{position:absolute;border-radius:50%;filter:blur(120px);opacity:.38}
.brand{font-size:30px;font-weight:700;letter-spacing:.5px;display:flex;align-items:center;gap:12px}
.brand i{width:14px;height:14px;border-radius:4px;background:linear-gradient(135deg,#ffc24b,#ff5d6c);display:inline-block}
.brand span{font-weight:300;color:#8b97b5}
.chip{display:inline-flex;align-items:center;gap:10px;border:1px solid rgba(255,255,255,.14);
  border-radius:999px;padding:6px 20px;font-size:24px;color:#c3cce0;background:rgba(255,255,255,.04)}
.tag{font-size:24px;font-weight:600;letter-spacing:.3px}
.muted{color:#8b97b5}
.card{border-radius:34px;border:1px solid rgba(255,255,255,.09);background:rgba(255,255,255,.035);position:relative;overflow:hidden}
.big{font-weight:700;line-height:1;letter-spacing:-2px}
.src{font-size:22px;color:#8b97b5;display:flex;align-items:center;gap:10px}
.src b{color:#dfe5f2;font-weight:600}
.disc{border:1.5px solid #ffc24b;color:#ffc24b;border-radius:999px;padding:6px 20px;font-weight:600;white-space:nowrap}
.bar-row{display:grid;grid-template-columns:220px 1fr 130px;align-items:center;gap:18px}
.track{position:relative;height:26px;border-radius:13px;background:rgba(255,255,255,.05)}
.track:after{content:"";position:absolute;left:50%;top:-6px;bottom:-6px;width:2px;background:rgba(255,255,255,.25)}
.bar{position:absolute;top:0;bottom:0;border-radius:13px}
"""


def title_html(parts):
    return "".join(f'<span style="color:{color(p.get("color"))}">{esc(p["text"])}</span>' for p in parts)


def stars(n):
    return "★" * int(n or 0)


def bars_html(items, animate):
    peak = max(abs(i["pct"]) for i in items) or 1
    rows = []
    for k, it in enumerate(items):
        p = it["pct"]
        c = COLORS["green"] if p >= 0 else COLORS["red"]
        width = abs(p) / peak * 48
        side = "left:50%" if p >= 0 else "right:50%"
        anim = f' data-grow="{width:.2f}" data-delay="{0.5 + 0.25 * k}"' if animate else ""
        rows.append(f"""<div class="bar-row" data-in="{0.3 + 0.25 * k}">
<div style="font-size:28px">{esc(it['label'])}</div>
<div class="track"><div class="bar" style="{side};width:{0 if animate else width:.2f}%;background:{c};box-shadow:0 0 24px {c}66"{anim}></div></div>
<div style="font-size:32px;font-weight:600;color:{c};text-align:right">{fmt_pct(p)}</div></div>""")
    return "\n".join(rows)


def poster_html(c):
    s = c["stories"]
    hero, rest = s[0], s[1:3]
    hc = color(hero.get("color"))
    small = "".join(f"""<div class="card" style="flex:1;padding:30px 32px;border-color:{color(x.get('color'))}55;
background:linear-gradient(160deg,{color(x.get('color'))}22,rgba(255,255,255,.02) 60%)">
<div class="tag" style="color:{color(x.get('color'))}">{stars(x.get('stars'))} {esc(x['tag'])}</div>
<div class="big" style="font-size:{86 if len(x['big']) <= 5 else 66}px;color:{color(x.get('color'))};margin:18px 0 16px">{esc(x['big'])}</div>
<div style="font-size:28px;font-weight:600;line-height:1.35">{esc(x['headline'])}</div>
<div style="font-size:21px;line-height:1.45;margin-top:10px" class="muted">{esc(x['note'])}</div>
<div class="src" style="margin-top:14px">ที่มา <b>{esc(x['source'])}</b></div></div>""" for x in rest)
    m = c["market"]
    return f"""<div class="bg"><div class="glow" style="width:620px;height:620px;left:-180px;top:-200px;background:{hc}"></div>
<div class="glow" style="width:560px;height:560px;right:-220px;bottom:-160px;background:#6aa8ff"></div></div>
<div style="position:absolute;inset:0;padding:56px 60px;display:flex;flex-direction:column;gap:26px">
<div style="display:flex;justify-content:space-between;align-items:center">
<div class="brand"><i></i>WWWTrend <span>· สรุปข่าวเด่น</span></div><div class="chip">{esc(c['date_th'])}</div></div>
<div style="font-size:54px;font-weight:700;line-height:1.2">{title_html(c['title'])}</div>
<div class="card" style="padding:34px 38px;display:flex;gap:34px;align-items:center;border-color:{hc}66;
background:linear-gradient(135deg,{hc}2e,rgba(255,255,255,.02) 65%)">
<div class="big" style="font-size:168px;color:{hc};text-shadow:0 0 60px {hc}88">{esc(hero['big'])}</div>
<div style="flex:1"><div class="tag" style="color:{hc}">{stars(hero.get('stars'))} {esc(hero['tag'])}</div>
<div style="font-size:33px;font-weight:600;line-height:1.35;margin:10px 0">{esc(hero['headline'])}</div>
<div style="font-size:22px;line-height:1.45" class="muted">{esc(hero['note'])}</div>
<div class="src" style="margin-top:12px">ที่มา <b>{esc(hero['source'])}</b></div></div></div>
<div style="display:flex;gap:22px">{small}</div>
<div class="card" style="padding:28px 36px;display:flex;flex-direction:column;gap:16px">
<div style="display:flex;justify-content:space-between;align-items:baseline">
<div style="font-size:28px;font-weight:600">{esc(m['title'])}</div><div class="muted" style="font-size:20px">% เทียบวันก่อน</div></div>
{bars_html(m['items'], False)}
<div class="muted" style="font-size:19px">{esc(m['caption'])}</div></div>
<div style="margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:20px">
<div class="muted" style="font-size:20px;line-height:1.4">{esc(c['footer'])}</div><div class="disc" style="font-size:22px">{DISCLAIMER}</div></div>
</div>"""


def video_html(c):
    stories = c["stories"]
    scenes, t = [], 0.0

    def add(dur, body, glow):
        nonlocal t
        scenes.append(f"""<section class="scene" data-start="{t}" data-end="{t + dur}">
<div class="glow" data-drift="1" style="width:900px;height:900px;left:-260px;top:-260px;background:{glow}"></div>
<div style="position:absolute;inset:0;padding:150px 84px 170px;display:flex;flex-direction:column">{body}</div></section>""")
        t += dur

    add(INTRO, f"""<div data-in="0.1" class="chip" style="align-self:flex-start;font-size:30px">{esc(c['date_th'])}</div>
<div style="margin-top:auto;margin-bottom:auto">
<div data-in="0.3" style="font-size:44px;color:#8b97b5;font-weight:300">WWWTrend · สรุปข่าวเด่น</div>
<div data-in="0.55" style="font-size:112px;font-weight:700;line-height:1.15;margin-top:20px">{len(stories)} ข่าว<br>ที่ต้องรู้วันนี้</div>
<div data-in="0.9" style="font-size:40px;line-height:1.4;margin-top:36px">{title_html(c['title'])}</div></div>""", COLORS["blue"])

    for i, s in enumerate(stories):
        sc = color(s.get("color"))
        cnt = s.get("count")
        big_attr = (f' data-count="{cnt["to"]}" data-prefix="{esc(cnt.get("prefix", ""))}" data-suffix="{esc(cnt.get("suffix", ""))}"'
                    if cnt else "")
        size = 300 if len(s["big"]) <= 5 else 200
        add(STORY, f"""<div data-in="0.1" class="tag" style="color:{sc};font-size:36px">ข่าว {i + 1}/{len(stories)} · {stars(s.get('stars'))} {esc(s['tag'])}</div>
<div style="margin-top:auto;margin-bottom:auto">
<div data-in="0.25" class="big" style="font-size:{size}px;color:{sc};text-shadow:0 0 90px {sc}88"{big_attr}>{esc(s['big'])}</div>
<div data-in="0.7" style="font-size:62px;font-weight:600;line-height:1.3;margin-top:50px">{esc(s['headline'])}</div>
<div data-in="1.1" style="font-size:36px;line-height:1.45;margin-top:30px" class="muted">{esc(s['note'])}</div></div>
<div data-in="1.4" class="src" style="font-size:34px">ที่มา <b>{esc(s['source'])}</b> · ลิงก์ใน sources.md</div>""", sc)

    m = c["market"]
    add(MARKET, f"""<div data-in="0.1" class="tag" style="font-size:36px;color:#6aa8ff">ตลาด</div>
<div style="margin-top:auto;margin-bottom:auto;display:flex;flex-direction:column;gap:46px">
<div data-in="0.2" style="font-size:84px;font-weight:700">{esc(m['title'])}</div>
<div style="display:flex;flex-direction:column;gap:40px;zoom:1.35">{bars_html(m['items'], True)}</div>
<div data-in="1.4" class="muted" style="font-size:30px;line-height:1.45">{esc(m['caption'])}</div></div>""", COLORS["blue"])

    add(OUTRO, f"""<div style="margin-top:auto;margin-bottom:auto">
<div data-in="0.1" class="disc" style="display:inline-block;font-size:72px;padding:18px 48px;border-width:3px">{DISCLAIMER}</div>
<div data-in="0.5" style="font-size:44px;line-height:1.5;margin-top:56px">{esc(c['footer'])}</div>
<div data-in="0.8" style="font-size:36px;margin-top:30px" class="muted">ตัวเลขสำคัญ กดลิงก์ต้นทางเช็คก่อนใช้ตัดสินใจ</div></div>""", COLORS["gold"])

    segs = "".join(f'<div class="seg"><div class="fill" data-s="{k}"></div></div>' for k in range(len(scenes)))
    return f"""<div class="bg"></div>{''.join(scenes)}
<div style="position:absolute;left:84px;right:84px;top:70px;display:flex;gap:12px">{segs}</div>
<div style="position:absolute;left:84px;right:84px;bottom:70px;display:flex;justify-content:space-between;align-items:center">
<div class="brand" style="font-size:30px"><i></i>WWWTrend</div><div class="disc" style="font-size:28px">{DISCLAIMER}</div></div>
<style>.scene{{position:absolute;inset:0;opacity:0}} .seg{{flex:1;height:8px;border-radius:4px;background:rgba(255,255,255,.18);overflow:hidden}}
.fill{{height:100%;width:0;background:#f3f6fc}}</style>
<script>
const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3);
function render(t) {{
  document.querySelectorAll('.scene').forEach((sc, k) => {{
    const a = +sc.dataset.start, b = +sc.dataset.end, l = t - a;
    const on = t >= a && t < b + 1e-6;
    sc.style.opacity = on ? Math.min(1, l / 0.35, (b - t) / 0.35 + (k === {len(scenes) - 1} ? 1 : 0)) : 0;
    const f = document.querySelector('.fill[data-s="' + k + '"]');
    f.style.width = (t >= b ? 100 : t <= a ? 0 : (l / (b - a)) * 100) + '%';
    if (!on) return;
    sc.querySelectorAll('[data-in]').forEach(el => {{
      const p = ease((l - +el.dataset.in) / 0.6);
      el.style.opacity = p; el.style.transform = 'translateY(' + (1 - p) * 50 + 'px)';
    }});
    sc.querySelectorAll('[data-count]').forEach(el => {{
      const p = ease((l - 0.25) / 1.3), v = Math.round(+el.dataset.count * p);
      el.textContent = (v < 0 ? '−' : '') + el.dataset.prefix + Math.abs(v) + el.dataset.suffix;
    }});
    sc.querySelectorAll('[data-grow]').forEach(el => {{
      el.style.width = (+el.dataset.grow * ease((l - +el.dataset.delay) / 0.9)) + '%';
    }});
    sc.querySelectorAll('[data-drift]').forEach(el => {{
      el.style.transform = 'translate(' + l * 40 + 'px,' + l * 30 + 'px)';
    }});
  }});
}}
</script>""", t


def page(body, w, h):
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{font_css()}{BASE_CSS}
body{{width:{w}px;height:{h}px;position:relative}}</style></head><body>{body}</body></html>"""


def launch(p):
    exe = os.environ.get("CHROME") or (DEFAULT_CHROME if Path(DEFAULT_CHROME).exists() else None)
    return p.chromium.launch(executable_path=exe, args=["--no-sandbox"])


def render_poster(browser, c, out):
    pg = browser.new_page(viewport={"width": POSTER_W, "height": POSTER_H})
    pg.set_content(page(poster_html(c), POSTER_W, POSTER_H))
    pg.evaluate("document.fonts.ready")
    pg.screenshot(path=str(out))
    pg.close()


def render_video(browser, c, out):
    body, total = video_html(c)
    pg = browser.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(page(body, 1080, 1920))
    pg.evaluate("document.fonts.ready")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                           "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    for n in range(int(total * FPS)):
        pg.evaluate(f"render({n / FPS})")
        ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
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
            render_poster(browser, c, out_dir / f"infographic-{date}.png")
            print(out_dir / f"infographic-{date}.png")
        if args.only != "poster":
            render_video(browser, c, out_dir / f"video-{date}.mp4")
            print(out_dir / f"video-{date}.mp4")
        browser.close()


if __name__ == "__main__":
    main()
