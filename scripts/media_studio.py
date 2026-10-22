"""Newsroom studio (16:9) for the anchor video in scripts/make_media.py.

A real presenter (assets/anchor.jpg, cut out with assets/anchor-alpha.png) sits on the right at a glass
desk, a big angled screen on the left shows the story graphics, and a lower third carries the headline
and subtitles. One steady camera with a slow drift and soft cross-fades only: no wipes or jump cuts.
Everything is HTML/CSS, driven per frame by render(t).
"""
import html
import json
import random

RED, ORANGE, TEAL, NAVY = "#e63b2e", "#ff9a3c", "#3fe0d0", "#0b1a33"
VW, VH = 1920, 1080            # YouTube / Facebook
TW, TH = 1080, 1920            # TikTok / Reels
STRAPS = {"intro": "สรุปข่าว", "disclaimer": "ขอบอกก่อน", "story": "ข่าว", "view": "มุมมอง",
          "market": "ตลาด", "outro": "WWWTrend"}


def esc(text):
    return html.escape(str(text))


def newsroom():
    """Out-of-focus newsroom behind the set: window bays, warm/cool bokeh, a floor glow."""
    rng = random.Random(7)
    bays = "".join(f'<div class="bay" style="left:{x}px;width:{w}px;opacity:{o:.2f}"></div>'
                   for x, w, o in [(0, 150, .5), (190, 220, .8), (450, 200, .6), (700, 260, .9), (1000, 230, .7),
                                   (1270, 210, .55), (1520, 240, .8), (1800, 160, .5)])
    dots = []
    for _ in range(46):
        warm = rng.random() < 0.55
        r = rng.uniform(14, 60)
        dots.append(f'<i class="bk" data-s="{rng.uniform(.2, 1):.2f}" style="left:{rng.uniform(-40, VW):.0f}px;top:{rng.uniform(40, 760):.0f}px;'
                    f'width:{2 * r:.0f}px;height:{2 * r:.0f}px;opacity:{rng.uniform(.18, .55):.2f};'
                    f'background:radial-gradient(circle,{"rgba(255,190,110,.9)" if warm else "rgba(110,170,255,.9)"} 0%,rgba(0,0,0,0) 70%)"></i>')
    return f'<div id="room">{bays}{"".join(dots)}<div id="floor"></div></div>'


def anchor_layer():
    # Cut-out presenter frames (WebP with alpha) are swapped in per frame by make_media.render_video.
    return '<img id="anchorImg" alt="">'


STUDIO_CSS = f"""
body{{width:{VW}px;height:{VH}px;position:relative;background:#040913;color:#fff;overflow:hidden}}
#stage{{position:absolute;inset:0;transform-origin:62% 45%}}
#room{{position:absolute;inset:0;background:linear-gradient(180deg,#0a1830 0%,#0c1f3d 45%,#081325 70%,#050b16 100%);overflow:hidden}}
.bay{{position:absolute;top:60px;height:640px;background:linear-gradient(180deg,rgba(120,170,230,.16),rgba(60,110,180,.05));
  filter:blur(14px);border-radius:6px}}
.bk{{position:absolute;border-radius:50%;filter:blur(6px)}}
#floor{{position:absolute;left:0;right:0;bottom:0;height:420px;background:radial-gradient(ellipse at 55% 0%,rgba(63,224,208,.10),rgba(0,0,0,0) 60%),
  linear-gradient(180deg,rgba(4,9,19,0),#040913 80%)}}
#pillar{{position:absolute;left:1180px;top:0;width:8px;height:820px;background:linear-gradient(180deg,rgba(63,224,208,0),{TEAL},rgba(63,224,208,0));
  filter:blur(2px);opacity:.55}}
#wrap{{position:absolute;left:70px;top:112px;width:1090px;height:648px;perspective:2200px}}
#screen{{position:absolute;inset:0;border-radius:18px;transform:rotateY(10deg);transform-origin:0 50%;
  background:linear-gradient(160deg,#0f2448,#081631 60%,#061127);border:3px solid rgba(63,224,208,.85);
  box-shadow:0 0 50px rgba(63,224,208,.35),0 30px 80px rgba(0,0,0,.6);overflow:hidden}}
#screen:after{{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.07),rgba(255,255,255,0) 40%);pointer-events:none}}
#stand{{position:absolute;left:180px;top:770px;width:860px;height:14px;border-radius:50%;background:rgba(63,224,208,.35);filter:blur(12px)}}
.panel{{position:absolute;inset:0;padding:40px 48px;display:flex;flex-direction:column;opacity:0}}
.pill{{display:inline-block;border-radius:999px;padding:4px 16px;font-weight:600;line-height:1.3}}
#anchorImg{{position:absolute;left:1150px;top:170px;width:760px;height:auto;-webkit-mask-image:linear-gradient(180deg,#000 70%,transparent 75%)}}
#desk{{position:absolute;left:1000px;top:792px;width:1000px;height:130px;
  background:linear-gradient(180deg,rgba(190,225,255,.35),rgba(120,170,220,.16) 18%,rgba(20,40,70,.85) 60%,#07101f);
  border-top:2px solid rgba(220,240,255,.75);box-shadow:0 -10px 40px rgba(120,190,255,.18);border-radius:6px 0 0 0}}
#desk:before{{content:"";position:absolute;left:0;right:0;top:0;height:6px;background:linear-gradient(90deg,rgba(63,224,208,0),{TEAL},rgba(63,224,208,0));opacity:.7}}
#bug{{position:absolute;left:52px;top:34px;display:flex;align-items:stretch;font-weight:700;box-shadow:0 6px 20px rgba(0,0,0,.4)}}
#bug b{{background:{RED};padding:4px 16px;font-size:26px;border-radius:8px 0 0 8px}}
#bug span{{background:#fff;color:{NAVY};padding:4px 16px;font-size:24px;border-radius:0 8px 8px 0;display:flex;align-items:center}}
#date{{position:absolute;right:52px;top:36px;font-size:24px;font-weight:600;background:rgba(10,20,40,.7);border:1px solid rgba(255,255,255,.3);
  padding:4px 18px;border-radius:999px}}
#lower{{position:absolute;left:52px;right:52px;top:856px}}
#tag{{display:inline-flex;align-items:center;gap:12px;background:rgba(6,14,30,.92);padding:6px 20px;font-size:24px;font-weight:600;
  border-left:6px solid {RED};letter-spacing:.5px}}
#tag em{{font-style:normal;color:{TEAL}}}
#head{{position:relative;margin-top:2px;height:76px;background:linear-gradient(90deg,#0c2350 0%,#123a7a 55%,rgba(18,58,122,.85));
  border-top:2px solid rgba(255,255,255,.35);box-shadow:0 10px 30px rgba(0,0,0,.5);overflow:hidden}}
#head div{{position:absolute;left:24px;right:24px;top:0;line-height:76px;font-size:42px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
#cap{{margin-top:8px;min-height:50px;font-size:28px;line-height:1.35;font-weight:600;color:#fff;background:rgba(0,0,0,.62);padding:7px 22px;border-radius:6px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
#fade{{position:absolute;inset:0;background:#000;pointer-events:none;z-index:30}}
#logo{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;z-index:31;font-size:130px;font-weight:700;letter-spacing:-2px;opacity:0}}
"""

# 9:16 for TikTok: same set stacked, screen on top, presenter below, and the bottom ~260 px left plain
# because TikTok draws its caption and buttons there.
TALL_CSS = f"""
body{{width:{TW}px;height:{TH}px}}
#stage{{transform-origin:50% 40%}}
#room{{right:auto;bottom:auto;width:{VW}px;height:{VH}px;left:-420px;transform:scale(1.78);transform-origin:50% 0}}
#pillar,#stand{{display:none}}
#wrap{{left:40px;top:150px;transform:scale(.917);transform-origin:0 0}}
#screen{{transform:none}}
#anchorImg{{left:90px;top:760px;width:900px}}
#desk{{left:0;top:1471px;width:{TW}px;border-radius:0}}
#bug{{left:30px;top:60px}}#date{{right:30px;top:62px}}
#lower{{left:30px;right:30px;top:1500px}}
#head{{height:70px}}#head div{{line-height:70px;font-size:38px}}
#cap{{-webkit-line-clamp:3;font-size:29px}}
#logo{{font-size:110px}}
"""


def studio_css(tall=False):
    return STUDIO_CSS + (TALL_CSS if tall else "")


def studio_html(c, segs, panel_html, gap):
    panels = "".join(f'<div class="panel" data-start="{s["start"]:.3f}" data-end="{s["end"] + gap:.3f}">{panel_html(s, c)}</div>'
                     for s in segs)
    lows = []
    for s in segs:
        k = s["kind"]
        if k == "story":
            tag, text = f'ข่าว {s["index"] + 1} · {s["story"]["source"]}', s["story"]["short"]
        elif k == "view":
            tag, text = "มุมมองจากบทวิเคราะห์ · ไม่ใช่ข้อเท็จจริง", s["story"]["short"]
        elif k == "market":
            tag, text = "ตลาด", c["market"]["title"]
        else:
            tag, text = STRAPS[k], {"intro": f"สรุปข่าวเด่น {c['date_th']}", "disclaimer": "เล่าข่าวตามที่ข่าวรายงาน",
                                    "outro": "ขอบคุณที่ติดตาม"}[k]
        lows.append([s["start"], s["end"] + gap, tag, text, s["caption"]])
    end = segs[-1]["end"] + gap
    data = json.dumps({"lows": lows, "end": end}, ensure_ascii=False)
    return f"""<div id="stage">{newsroom()}<div id="pillar"></div>
<div id="wrap"><div id="screen">{panels}</div></div><div id="stand"></div>
{anchor_layer()}<div id="desk"></div></div>
<div id="bug"><b>WWWTrend</b><span>สรุปข่าว</span></div><div id="date">WWWTrend · {esc(c['date_th'])}</div>
<div id="lower"><div id="tag"><span id="tagT"></span><em>WWWTrend</em></div><div id="head"><div id="headT"></div></div><div id="cap"></div></div>
<div id="fade"></div><div id="logo">WWW<span style="color:{RED}">Trend</span></div>
<script>
const D = {data};
const clamp = x => Math.min(Math.max(x, 0), 1);
const smooth = x => {{ x = clamp(x); return x * x * (3 - 2 * x); }};
const $ = id => document.getElementById(id);
const bk = [...document.querySelectorAll('.bk')];
// opacity of something shown from a to b: soft in, soft out
const span = (t, a, b, i, o) => Math.min(smooth((t - a) / i), smooth((b - t) / o));
function render(t) {{
  // one camera, slow drift: no cuts
  const z = 1.035 + 0.025 * Math.sin(t / 9.0), x = 10 * Math.sin(t / 13.0), y = 5 * Math.sin(t / 7.3);
  $('stage').style.transform = `translate(${{x}}px,${{y}}px) scale(${{z}})`;
  bk.forEach((el, n) => el.style.transform = `translateX(${{Math.sin(t / 6 + n) * 14 * el.dataset.s}}px)`);
  document.querySelectorAll('.panel').forEach(p => {{
    const a = +p.dataset.start, b = +p.dataset.end, q = span(t, a - 0.25, b + 0.25, 0.5, 0.5);
    p.style.opacity = q;
    p.style.transform = `scale(${{0.985 + 0.015 * q}})`;
    if (q > 0) p.querySelectorAll('.bar').forEach((el, n) => el.style.width = (+el.dataset.w * smooth((t - a - 0.4 - n * 0.25) / 0.9)) + '%');
  }});
  const lo = D.lows.find(l => t >= l[0] - 0.25 && t < l[1] - 0.25) || D.lows[0];
  const q = span(t, lo[0] - 0.25, lo[1] - 0.25, 0.35, 0.3);
  $('tagT').textContent = lo[2]; $('headT').textContent = lo[3]; $('cap').textContent = lo[4];
  $('headT').style.opacity = q; $('cap').style.opacity = q; $('tagT').style.opacity = q;
  $('fade').style.opacity = Math.max(1 - smooth(t / 0.9), smooth((t - (D.end - 0.8)) / 0.8));
  const lg = $('logo');
  lg.style.opacity = t < 1.6 ? span(t, 0.1, 1.5, 0.4, 0.5) : 0;
  lg.style.transform = `scale(${{0.94 + 0.06 * smooth(t / 1.5)}})`;
}}
</script>"""
