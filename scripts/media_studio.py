"""Broadcast-style studio for the anchor video in scripts/make_media.py.

A shaded vector news anchor at a desk, an LED wall behind, an opening sting, camera shots that
cut between wide / close-up / split (graphics screen above the anchor), lower-third straps,
subtitles and a ticker. Everything is inline SVG/CSS, driven per frame by render(t, mouth).
"""
import html
import json
import random

RED, YELLOW, BLUE, PAPER, INK = "#e63b2e", "#ffd23f", "#6aa8ff", "#f4f1ea", "#111111"

# Camera shots: screen = graphics screen opacity, tx/ty/s = anchor placement, wall = LED-wall title.
SHOTS = {
    "wide": {"screen": 0, "tx": 0, "ty": 700, "s": 1.1, "wall": 1},
    "close": {"screen": 0, "tx": 0, "ty": 506, "s": 1.4, "wall": 0},
    "split": {"screen": 1, "tx": 0, "ty": 900, "s": 0.85, "wall": 0},
}
# A real presenter photo already shows a desk and studio, so it sits smaller to keep the LED wall visible.
SHOTS_REAL = {
    "wide": {"screen": 0, "tx": 0, "ty": 820, "s": 0.75, "wall": 1},
    "close": {"screen": 0, "tx": 0, "ty": 600, "s": 1.05, "wall": 0},
    "split": {"screen": 1, "tx": 0, "ty": 1000, "s": 0.62, "wall": 0},
}
STRAPS = {"intro": "สรุปข่าว", "disclaimer": "ขอบอกก่อน", "story": "ข่าว", "view": "มุมมอง",
          "market": "ตลาด", "outro": "WWWTrend"}


def esc(text):
    return html.escape(str(text))


def anchor_svg():
    return """<svg id="anchor" viewBox="0 0 1080 1100" width="1080" height="1100">
<defs>
<radialGradient id="skinG" cx="45%" cy="38%" r="70%"><stop offset="0" stop-color="#f7d7bb"/><stop offset=".6" stop-color="#eebf98"/><stop offset="1" stop-color="#d69d76"/></radialGradient>
<linearGradient id="hairG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b2b21"/><stop offset="1" stop-color="#160f0b"/></linearGradient>
<linearGradient id="suitG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3a5e"/><stop offset="1" stop-color="#0f1729"/></linearGradient>
<linearGradient id="tieG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff6a58"/><stop offset="1" stop-color="#a8231a"/></linearGradient>
<radialGradient id="irisG"><stop offset="0" stop-color="#7a5539"/><stop offset="1" stop-color="#2a1a10"/></radialGradient>
<linearGradient id="deskTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b5180"/><stop offset="1" stop-color="#22325a"/></linearGradient>
<linearGradient id="deskFront" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18243f"/><stop offset="1" stop-color="#070d1a"/></linearGradient>
</defs>
<g id="body">
<path d="M170 1100 C185 880 300 800 432 770 L540 840 L648 770 C780 800 895 880 910 1100 Z" fill="url(#suitG)"/>
<path d="M470 765 L540 905 L610 765 Z" fill="#f5f5f5"/>
<path d="M470 765 L512 832 L540 800 Z M610 765 L568 832 L540 800 Z" fill="#dfe2e8"/>
<path d="M522 800 L558 800 L552 836 L528 836 Z" fill="#b3271d"/>
<path d="M528 836 L552 836 L568 965 L540 995 L512 965 Z" fill="url(#tieG)"/>
<path d="M436 770 L522 884 L470 972 L392 842 Z M644 770 L558 884 L610 972 L688 842 Z" fill="#17223d"/>
<path d="M436 770 L522 884 M644 770 L558 884" stroke="rgba(255,255,255,.18)" stroke-width="3" fill="none"/>
<circle cx="626" cy="900" r="9" fill="#0b0b0b"/><rect x="622" y="908" width="8" height="18" rx="3" fill="#0b0b0b"/>
<path d="M486 500 L594 500 L600 782 Q540 826 480 782 Z" fill="#e2ad87"/>
<path d="M486 560 Q540 640 594 560 L596 640 Q540 690 484 640 Z" fill="#c08560" opacity=".45"/>
<g id="head">
<ellipse cx="388" cy="380" rx="26" ry="44" fill="#e6b28c"/><ellipse cx="692" cy="380" rx="26" ry="44" fill="#e6b28c"/>
<ellipse cx="392" cy="382" rx="12" ry="24" fill="#cf946f"/><ellipse cx="688" cy="382" rx="12" ry="24" fill="#cf946f"/>
<path d="M392 330 C392 190 470 150 540 150 C610 150 688 190 688 330 C688 452 640 560 540 582 C440 560 392 452 392 330 Z" fill="url(#skinG)"/>
<path d="M384 342 C366 200 440 120 545 117 C662 115 718 200 699 346 C691 300 677 262 652 240 C602 264 520 264 470 245 C438 262 404 292 384 342 Z" fill="url(#hairG)"/>
<path d="M430 250 C470 190 560 176 660 232 C620 214 560 214 520 236 C490 226 455 234 430 250 Z" fill="#2c1f17"/>
<path d="M470 160 C520 138 600 148 642 186" stroke="rgba(255,255,255,.2)" stroke-width="8" fill="none" stroke-linecap="round"/>
<path d="M396 360 C400 470 450 552 540 576 C470 540 428 470 410 362 Z M684 360 C680 470 630 552 540 576 C610 540 652 470 670 362 Z" fill="#c98b66" opacity=".35"/>
<path d="M448 318 Q479 300 512 318 M568 318 Q601 300 632 318" stroke="#c98b66" stroke-width="3" fill="none" opacity=".7"/>
<path d="M530 440 L534 466 M550 440 L546 466" stroke="#d79c78" stroke-width="3" opacity=".6"/>
<g id="brows" fill="#24180f">
<path d="M440 292 Q478 272 518 288 L516 300 Q478 287 442 303 Z"/><path d="M640 292 Q602 272 562 288 L564 300 Q602 287 638 303 Z"/></g>
<g id="eyes">
<path d="M446 334 Q479 310 513 334 Q479 352 446 334 Z" fill="#fff"/><path d="M567 334 Q601 310 634 334 Q601 352 567 334 Z" fill="#fff"/>
<circle cx="480" cy="333" r="13" fill="url(#irisG)"/><circle cx="600" cy="333" r="13" fill="url(#irisG)"/>
<circle cx="480" cy="333" r="6" fill="#0d0806"/><circle cx="600" cy="333" r="6" fill="#0d0806"/>
<circle cx="485" cy="328" r="3.5" fill="#fff"/><circle cx="605" cy="328" r="3.5" fill="#fff"/>
<path d="M443 333 Q479 305 516 331 M564 331 Q601 305 637 333" stroke="#24180f" stroke-width="5" fill="none" stroke-linecap="round"/></g>
<path d="M540 342 C534 382 524 410 528 421 C534 429 548 429 554 421" stroke="#c18560" stroke-width="5" fill="none" stroke-linecap="round"/>
<ellipse cx="528" cy="423" rx="7" ry="4" fill="#b2754f" opacity=".6"/><ellipse cx="552" cy="423" rx="7" ry="4" fill="#b2754f" opacity=".6"/>
<ellipse cx="452" cy="420" rx="30" ry="16" fill="#ef9d88" opacity=".22"/><ellipse cx="628" cy="420" rx="30" ry="16" fill="#ef9d88" opacity=".22"/>
<g id="mouth">
<ellipse id="mouthIn" cx="540" cy="484" rx="34" ry="2" fill="#4f1717"/>
<rect id="teeth" x="516" y="476" width="48" height="9" rx="3" fill="#fbfbfb" opacity="0"/>
<path d="M500 479 Q520 467 540 474 Q560 467 580 479 Q540 487 500 479 Z" fill="#b25d55"/>
<path id="lowLip" d="M504 485 Q540 503 576 485 Q540 495 504 485 Z" fill="#c46c62"/></g>
<ellipse cx="540" cy="556" rx="58" ry="12" fill="#d29a73" opacity=".35"/>
</g></g>
<path d="M200 930 C240 990 330 1000 420 990 L430 1030 L250 1040 Z M880 930 C840 990 750 1000 660 990 L650 1030 L830 1040 Z" fill="url(#suitG)"/>
<path d="M60 958 L1020 958 L1044 1004 L36 1004 Z" fill="url(#deskTop)"/>
<path d="M60 958 L1020 958" stroke="rgba(255,255,255,.35)" stroke-width="3"/>
<path d="M468 946 L612 946 L630 984 L450 984 Z" fill="#f4f1ea"/><path d="M490 958 L590 958 M486 968 L596 968" stroke="#c9c4b8" stroke-width="3"/>
<ellipse cx="440" cy="984" rx="48" ry="20" fill="#e2ad87"/><ellipse cx="640" cy="984" rx="48" ry="20" fill="#e2ad87"/>
<path d="M36 1004 L1044 1004 L1004 1100 L76 1100 Z" fill="url(#deskFront)"/>
<rect x="400" y="1030" width="280" height="44" rx="8" fill="rgba(230,59,46,.9)"/>
<text x="540" y="1062" text-anchor="middle" font-family="Kanit" font-weight="700" font-size="30" fill="#fff">WWWTrend</text>
</svg>"""


def anchor_img():
    # Real presenter: Wav2Lip frames of assets/anchor.jpg, swapped in per frame by make_media.render_video.
    return ('<img id="anchorImg" style="width:1080px;height:1100px;object-fit:cover;object-position:50% 18%;'
            'border-radius:30px;box-shadow:0 30px 90px rgba(0,0,0,.6);border:3px solid rgba(255,255,255,.35)">')


def wall_chart():
    rng = random.Random(21)
    bars, x, y = [], 0, 380
    while x < 2400:
        o = y
        y = max(160, min(600, y + rng.uniform(-60, 60)))
        hi, lo = min(o, y) - rng.uniform(10, 40), max(o, y) + rng.uniform(10, 40)
        c = "#38d98f" if y < o else "#ff6b5e"
        bars.append(f'<line x1="{x + 9}" y1="{hi:.0f}" x2="{x + 9}" y2="{lo:.0f}" stroke="{c}" stroke-width="3" opacity=".55"/>'
                    f'<rect x="{x}" y="{min(o, y):.0f}" width="18" height="{max(4, abs(o - y)):.0f}" fill="{c}" opacity=".55"/>')
        x += 40
    grid = "".join(f'<line x1="0" y1="{gy}" x2="2400" y2="{gy}" stroke="rgba(106,168,255,.12)"/>' for gy in range(80, 760, 80))
    return f'<svg id="wallChart" width="2400" height="760" style="position:absolute;left:0;top:0">{grid}{"".join(bars)}</svg>'


STUDIO_CSS = f"""
body{{width:1080px;height:1920px;position:relative;background:#050a14;color:#fff;overflow:hidden}}
#bg{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 85%,#1d3a6e 0%,#0a1630 45%,#050a14 80%)}}
.beam{{position:absolute;top:-200px;width:420px;height:1500px;background:linear-gradient(180deg,rgba(150,190,255,.18),rgba(150,190,255,0));filter:blur(18px)}}
#wall{{position:absolute;left:40px;right:40px;top:150px;height:780px;border-radius:26px;overflow:hidden;
  background:linear-gradient(180deg,#0f2550,#07132a);border:2px solid rgba(106,168,255,.35);box-shadow:0 0 80px rgba(106,168,255,.25)}}
#wallText{{position:absolute;inset:0;padding:70px 64px;display:flex;flex-direction:column;justify-content:center}}
#anchorWrap{{position:absolute;left:0;top:0;width:1080px;height:1100px;transform-origin:540px 400px}}
#screen{{position:absolute;left:48px;right:48px;top:150px;height:780px;border-radius:30px;background:{PAPER};color:{INK};overflow:hidden;
  box-shadow:0 30px 90px rgba(0,0,0,.6);border:3px solid rgba(255,255,255,.6)}}
.panel{{position:absolute;inset:0;padding:50px 56px;display:flex;flex-direction:column;opacity:0}}
.pill{{display:inline-block;border-radius:999px;padding:6px 18px;font-weight:600;line-height:1.3}}
#bug{{position:absolute;left:48px;top:52px;display:flex;align-items:stretch;font-weight:700;box-shadow:0 8px 24px rgba(0,0,0,.4)}}
#bug b{{background:{RED};padding:8px 18px;font-size:34px;border-radius:10px 0 0 10px}}
#bug span{{background:#fff;color:{INK};padding:8px 18px;font-size:30px;border-radius:0 10px 10px 0;display:flex;align-items:center}}
#date{{position:absolute;right:48px;top:60px;font-size:30px;font-weight:600;background:rgba(0,0,0,.45);padding:8px 18px;border-radius:10px}}
#strap{{position:absolute;left:0;top:1470px;display:flex;align-items:stretch;max-width:1020px;box-shadow:0 10px 30px rgba(0,0,0,.5)}}
#strap b{{background:{RED};padding:12px 22px 12px 48px;font-size:32px;white-space:nowrap}}
#strap span{{background:#fff;color:{INK};padding:12px 26px;font-size:34px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
#cap{{position:absolute;left:48px;right:48px;top:1572px;min-height:120px;background:rgba(0,0,0,.8);border-left:10px solid {YELLOW};
  border-radius:14px;padding:18px 26px;font-size:33px;line-height:1.4;font-weight:600}}
#tick{{position:absolute;left:0;right:0;bottom:0;height:86px;background:#0d1526;overflow:hidden;display:flex;align-items:center;border-top:4px solid {RED}}}
#tick b{{position:absolute;left:0;top:0;bottom:0;z-index:2;background:{RED};font-size:30px;padding:0 24px;display:flex;align-items:center}}
#tk{{white-space:nowrap;font-size:30px;font-weight:600;position:absolute;left:0}}
#sting{{position:absolute;inset:0;z-index:20;pointer-events:none}}
#sting i{{position:absolute;left:-1400px;width:1400px;height:260px;transform:skewY(-12deg)}}
#sting div{{position:absolute;left:0;right:0;top:820px;text-align:center;font-size:120px;font-weight:700;letter-spacing:-2px;opacity:0}}
"""


def studio_html(c, segs, panel_html, gap, real=False):
    panels = "".join(f'<div class="panel" data-start="{s["start"]:.3f}" data-end="{s["end"] + gap:.3f}">{panel_html(s, c)}</div>'
                     for s in segs)
    caps = [[s["start"], s["end"] + gap, s["caption"]] for s in segs]
    shots, straps = [], []
    for s in segs:
        k = s["kind"]
        if k == "story":
            shots += [[s["start"], "close"], [s["start"] + 1.4, "split"]]
            label, text = f'{STRAPS[k]} {s["index"] + 1}', s["story"]["short"]
        elif k == "view":
            shots.append([s["start"], "split"])
            label, text = STRAPS[k], "จากบทวิเคราะห์ · ไม่ใช่ข้อเท็จจริง"
        elif k == "market":
            shots.append([s["start"], "split"])
            label, text = STRAPS[k], c["market"]["title"]
        else:
            shots.append([s["start"], {"intro": "wide", "disclaimer": "close", "outro": "wide"}[k]])
            label, text = STRAPS[k], {"intro": f"สรุปข่าวเด่น {c['date_th']}", "disclaimer": "เล่าข่าวตามที่ข่าวรายงาน",
                                      "outro": "ขอบคุณที่ติดตาม"}[k]
        straps.append([s["start"], s["end"] + gap, label, text])
    heads = "".join(f'<div style="font-size:52px;font-weight:700;line-height:1.25;padding:10px 0;border-top:2px solid rgba(255,255,255,.2)">'
                    f'<span style="color:{YELLOW}">0{i + 1}</span> {esc(s["short"])}</div>' for i, s in enumerate(c["stories"]))
    ticker = esc(f"  WWWTrend นำข่าวมาเล่าให้ฟัง  ·  {c['footer']}  ·  " + "  ·  ".join(s["short"] for s in c["stories"]) + "  ·  ") * 4
    data = json.dumps({"caps": caps, "shots": shots, "straps": straps, "P": SHOTS_REAL if real else SHOTS}, ensure_ascii=False)
    return f"""<div id="bg"></div><div class="beam" style="left:-60px;transform:rotate(18deg)"></div><div class="beam" style="right:-60px;transform:rotate(-18deg)"></div>
<div id="wall">{wall_chart()}<div id="wallText" style="opacity:0">
<div style="font-size:34px;font-weight:600;color:{YELLOW}">WWWTrend · {esc(c['date_th'])}</div>
<div style="font-size:92px;font-weight:700;line-height:1.1;margin:18px 0 30px">{len(c['stories'])} ข่าวที่ต้องรู้วันนี้</div>{heads}</div></div>
<div id="anchorWrap">{anchor_img() if real else anchor_svg()}</div>
<div id="screen">{panels}</div>
<div id="bug"><b>WWWTrend</b><span>สรุปข่าว</span></div><div id="date">{esc(c['date_th'])}</div>
<div id="strap"><b id="strapL"></b><span id="strapT"></span></div>
<div id="cap"></div>
<div id="tick"><b>WWWTrend</b><div id="tk">{ticker}</div></div>
<div id="sting"><i style="top:620px;background:{RED}"></i><i style="top:900px;background:{BLUE}"></i><i style="top:1180px;background:#fff"></i>
<div>WWW<span style="color:{RED}">Trend</span></div></div>
<script>
const D = {data};
const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3);
const lerp = (a, b, k) => a + (b - a) * k;
const $ = id => document.getElementById(id);
function render(t, m) {{
  let i = 0; D.shots.forEach((s, j) => {{ if (t >= s[0]) i = j; }});
  const cur = D.P[D.shots[i][1]], prev = D.P[D.shots[Math.max(0, i - 1)][1]];
  const k = ease((t - D.shots[i][0]) / 0.7), P = {{}};
  for (const key in cur) P[key] = lerp(prev[key], cur[key], k);
  const push = 1 + 0.025 * Math.min(1, (t - D.shots[i][0]) / 6);
  $('anchorWrap').style.transform = 'translate(' + P.tx + 'px,' + P.ty + 'px) scale(' + (P.s * push) + ')';
  $('screen').style.opacity = P.screen;
  $('screen').style.transform = 'translateY(' + (1 - P.screen) * -60 + 'px) scale(' + (0.96 + 0.04 * P.screen) + ')';
  $('wallText').style.opacity = P.wall;
  $('wallChart').style.transform = 'translateX(' + (-(t * 40) % 1200) + 'px)';
  document.querySelectorAll('.panel').forEach(p => {{
    const a = +p.dataset.start, b = +p.dataset.end, on = t >= a && t < b;
    const q = ease((t - a - 0.3) / 0.5);
    p.style.opacity = on ? q : 0;
    p.style.transform = 'translateX(' + (1 - q) * 80 + 'px)';
    if (on) p.querySelectorAll('.bar').forEach((el, n) => el.style.width = (+el.dataset.w * ease((t - a - 0.6 - n * 0.35) / 0.8)) + '%');
  }});
  const cap = D.caps.find(x => t >= x[0] && t < x[1]);
  $('cap').textContent = cap ? cap[2] : '';
  const st = D.straps.find(x => t >= x[0] && t < x[1]);
  if (st) {{ $('strapL').textContent = st[2]; $('strapT').textContent = st[3]; }}
  $('strap').style.transform = 'translateX(' + (st ? (1 - ease((t - st[0]) / 0.5)) * -700 : -1100) + 'px)';
  if ($('mouthIn')) {{
  $('mouthIn').setAttribute('cy', 482 + 12 * m);
  $('mouthIn').setAttribute('ry', 3 + 13 * m);
  $('lowLip').setAttribute('transform', 'translate(0 ' + 22 * m + ')');
  $('teeth').style.opacity = m > 0.2 ? 1 : 0;
  const bt = t % 4.1, blink = (bt < 0.12 || (bt > 0.3 && bt < 0.4 && Math.floor(t / 4.1) % 3 === 0)) ? 0.08 : 1;
  $('eyes').setAttribute('transform', 'translate(0 ' + 333 * (1 - blink) + ') scale(1 ' + blink + ')');
  $('brows').setAttribute('transform', 'translate(0 ' + (-7 * m) + ')');
  $('head').setAttribute('transform', 'rotate(' + (Math.sin(t * 1.1) * 1.8 + Math.sin(t * 2.7) * m * 1.4) + ' 540 640) translate(0 ' + (m * 3) + ')');
  $('body').setAttribute('transform', 'translate(0 ' + Math.sin(t * 1.6) * 3 + ')');
  }}
  const tk = $('tk');
  tk.style.transform = 'translateX(' + (220 - (t * 130) % (tk.scrollWidth / 4)) + 'px)';
  const sg = $('sting');
  sg.style.display = t < 1.6 ? 'block' : 'none';
  if (t < 1.6) {{
    sg.querySelectorAll('i').forEach((el, n) => el.style.transform = 'skewY(-12deg) translateX(' + ease((t - n * 0.08) / 0.5) * (t < 1.1 ? 1400 : 1400 + (t - 1.1) * 6000) + 'px)');
    const lg = sg.querySelector('div'), q = ease((t - 0.35) / 0.4);
    lg.style.opacity = t < 1.2 ? q : Math.max(0, 1 - (t - 1.2) / 0.3);
    lg.style.transform = 'scale(' + (0.8 + 0.2 * q) + ')';
  }}
}}
</script>"""
