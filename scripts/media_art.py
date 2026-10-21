"""Isometric illustrations for scripts/make_media.py, drawn as inline SVG (no image files, no network).

Scenes: "chip" (memory chip on a board, falling bars), "deal" (server racks + coin stacks),
"code" (laptop with code + torch), "oil" (barrels + derrick), "rocket" (rocket + car), "gold" (bar stack).
cover_art() combines three scenes on one board.
"""
import math

C30, S30 = math.cos(math.pi / 6), 0.5


def shade(hex_color, f):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f >= 1:
        r, g, b = (int(v + (255 - v) * (f - 1)) for v in (r, g, b))
    else:
        r, g, b = (int(v * f) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


class Iso:
    def __init__(self, scale, cx, cy):
        self.s, self.cx, self.cy, self.out = scale, cx, cy, []

    def p(self, x, y, z):
        return (self.cx + (x - y) * C30 * self.s, self.cy + (x + y) * S30 * self.s - z * self.s)

    def poly(self, pts, fill, extra=""):
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in (self.p(*q) for q in pts))
        self.out.append(f'<polygon points="{d}" fill="{fill}" {extra}/>')

    def box(self, x, y, z, w, d, h, color, extra=""):
        t = z + h
        self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, t), (x, y + d, t)], color, extra)
        self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, t), (x + w, y, t)], shade(color, 0.72), extra)
        self.poly([(x, y, t), (x + w, y, t), (x + w, y + d, t), (x, y + d, t)], shade(color, 1.28), extra)

    def line(self, pts, color, width, extra=""):
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in (self.p(*q) for q in pts))
        self.out.append(f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
                        f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')

    def face_left(self, x, y_front, z_top):
        """SVG transform so content drawn in (u right, t down) grid units lands on a front-left face."""
        ox, oy = self.p(x, y_front, z_top)
        return f"matrix({C30 * self.s:.3f},{S30 * self.s:.3f},0,{self.s:.3f},{ox:.1f},{oy:.1f})"

    def face_top(self, x, y, z):
        ox, oy = self.p(x, y, z)
        return f"matrix({C30 * self.s:.3f},{S30 * self.s:.3f},{-C30 * self.s:.3f},{S30 * self.s:.3f},{ox:.1f},{oy:.1f})"

    def coin_stack(self, x, y, z, n, r=1.1):
        for k in range(n):
            cx, cy = self.p(x, y, z + k * 0.32)
            rx, ry = r * C30 * self.s * 1.15, r * S30 * self.s * 1.15
            self.out.append(f'<rect x="{cx - rx:.1f}" y="{cy - 0.32 * self.s:.1f}" width="{2 * rx:.1f}" height="{0.32 * self.s:.1f}" fill="#c9971c"/>'
                            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#b5850f"/>'
                            f'<ellipse cx="{cx:.1f}" cy="{cy - 0.32 * self.s:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#ffd23f" stroke="#e3a91a" stroke-width="2"/>')
        cx, cy = self.p(x, y, z + n * 0.32)
        self.out.append(f'<text x="{cx:.1f}" y="{cy + 0.28 * self.s:.1f}" text-anchor="middle" font-family="Kanit" font-weight="700" '
                        f'font-size="{0.9 * self.s:.0f}" fill="#9a6b00" transform="scale(1 1)">$</text>')


DEFS = """<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/>
<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="flame" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#e63b2e"/><stop offset=".6" stop-color="#ff8a1f"/><stop offset="1" stop-color="#ffd23f"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient></defs>"""


def _chip(g, ox=0.0, oy=0.0, z=0.8):
    # falling bars behind the chip
    for k, h in enumerate((2.6, 1.8, 1.0)):
        g.box(ox + 7.6, oy + 0.6 + k * 1.0, z, 0.8, 0.7, h, "#e63b2e")
    for k in range(5):
        y = oy + 3.4 + k * 0.75
        g.line([(ox + 3, y, z), (ox + 1.6, y, z), (ox + 0.9, y + 0.5, z)], "#ffd23f", 3, 'filter="url(#glow)" opacity=".9"')
        x = ox + 3.4 + k * 0.75
        g.line([(x, oy + 7, z), (x, oy + 8.6, z), (x + 0.5, oy + 9.3, z)], "#ffd23f", 3, 'filter="url(#glow)" opacity=".9"')
    g.box(ox + 3, oy + 3, z, 4, 4, 0.7, "#1c1c1c")
    g.poly([(ox + 3.6, oy + 3.6, z + 0.71), (ox + 6.4, oy + 3.6, z + 0.71), (ox + 6.4, oy + 6.4, z + 0.71), (ox + 3.6, oy + 6.4, z + 0.71)], "#2f2f2f")
    g.out.append(f'<g transform="{g.face_top(ox + 3.6, oy + 3.6, z + 0.72)}"><text x="1.4" y="1.75" text-anchor="middle" '
                 f'font-family="Kanit" font-weight="700" font-size="1.1" fill="#f4f1ea">RAM</text></g>')
    for k in range(5):
        g.box(ox + 3.25 + k * 0.75, oy + 7, z, 0.35, 0.35, 0.25, "#c8ccd4")
        g.box(ox + 7, oy + 3.25 + k * 0.75, z, 0.35, 0.35, 0.25, "#c8ccd4")


def _deal(g, ox=0.0, oy=0.0, z=0.6):
    for k, h in enumerate((5.2, 4.2, 5.8)):
        x = ox + 0.8 + k * 2.6
        g.box(x, oy + 0.8, z, 2.0, 2.0, h, "#26324f")
        leds = []
        for r in range(int(h / 0.7)):
            t = 0.5 + r * 0.7
            leds.append(f'<rect x="0.25" y="{t:.2f}" width="1.5" height="0.16" rx="0.08" fill="#0d1526"/>'
                        f'<circle cx="{0.4 + (r % 3) * 0.12:.2f}" cy="{t + 0.08:.2f}" r="0.07" fill="{("#38d98f", "#ffd23f", "#38d98f")[r % 3]}"/>')
        g.out.append(f'<g transform="{g.face_left(x, oy + 2.8, z + h)}">{"".join(leds)}</g>')
    g.coin_stack(ox + 7.6, oy + 7.2, z, 6)
    g.coin_stack(ox + 5.6, oy + 8.4, z, 3)


def _code(g, ox=0.0, oy=0.0, z=0.6):
    g.box(ox + 1.5, oy + 2.4, z + 0.25, 5.6, 0.25, 3.8, "#1b1b1b")
    lines, colors = [], ("#ffd23f", "#38d98f", "#6aa8ff", "#e63b2e", "#f4f1ea")
    for r in range(7):
        w = (3.6, 2.4, 4.2, 1.8, 3.0, 2.6, 3.8)[r]
        lines.append(f'<rect x="{0.4 + (r % 3) * 0.35:.2f}" y="{0.45 + r * 0.45:.2f}" width="{w:.2f}" height="0.18" rx="0.09" fill="{colors[r % 5]}"/>')
    g.out.append(f'<g transform="{g.face_left(ox + 1.5, oy + 2.65, z + 4.05)}" filter="url(#glow)">{"".join(lines)}'
                 f'<text x="4.6" y="3.4" font-family="Kanit" font-weight="700" font-size="1.0" fill="#f4f1ea">&lt;/&gt;</text></g>')
    g.box(ox + 1.2, oy + 2.65, z, 6.2, 4.2, 0.25, "#d9dbe0")
    g.poly([(ox + 3.4, oy + 5.4, z + 0.26), (ox + 5.4, oy + 5.4, z + 0.26), (ox + 5.4, oy + 6.4, z + 0.26), (ox + 3.4, oy + 6.4, z + 0.26)], "#bfc3cb")
    g.box(ox + 8.2, oy + 7.4, z, 0.55, 0.55, 2.2, "#7a4a24")
    fx, fy = g.p(ox + 8.47, oy + 7.67, z + 2.2)
    s = g.s
    g.out.append(f'<circle cx="{fx:.1f}" cy="{fy - 0.9 * s:.1f}" r="{1.6 * s:.1f}" fill="url(#halo)"/>'
                 f'<path d="M{fx:.1f} {fy - 2.2 * s:.1f} C{fx + 0.9 * s:.1f} {fy - 1.2 * s:.1f} {fx + 0.7 * s:.1f} {fy:.1f} {fx:.1f} {fy:.1f} '
                 f'C{fx - 0.7 * s:.1f} {fy:.1f} {fx - 0.9 * s:.1f} {fy - 1.0 * s:.1f} {fx:.1f} {fy - 2.2 * s:.1f} Z" fill="url(#flame)" filter="url(#glow)"/>')


def _cylinder(g, x, y, z, r, h, color, top=None):
    cx, cy = g.p(x, y, z)
    tx, ty = g.p(x, y, z + h)
    rx, ry = r * C30 * g.s * 1.15, r * S30 * g.s * 1.15
    g.out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{shade(color, 0.7)}"/>'
                 f'<rect x="{cx - rx:.1f}" y="{ty:.1f}" width="{2 * rx:.1f}" height="{cy - ty:.1f}" fill="{color}"/>'
                 f'<rect x="{cx:.1f}" y="{ty:.1f}" width="{rx:.1f}" height="{cy - ty:.1f}" fill="{shade(color, 0.82)}"/>'
                 f'<ellipse cx="{tx:.1f}" cy="{ty:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{top or shade(color, 1.3)}"/>')
    return tx, ty, rx


def _oil(g, ox=0.0, oy=0.0, z=0.6):
    base = [(ox + 6.2, oy + 1.6), (ox + 8.4, oy + 1.6), (ox + 8.4, oy + 3.8), (ox + 6.2, oy + 3.8)]
    top = (ox + 7.3, oy + 2.7, z + 6.2)
    for bx, by in base:
        g.line([(bx, by, z), top], "#2b2b2b", 4)
    for t in (2.0, 3.8):
        f = t / 6.2
        ring = [(bx + (top[0] - bx) * f, by + (top[1] - by) * f, z + t) for bx, by in base]
        g.line(ring + [ring[0]], "#2b2b2b", 3)
    for k, h in enumerate((2.8, 2.0, 1.2)):
        g.box(ox + 8.2, oy + 5.2 + k * 1.0, z, 0.8, 0.7, h, "#e63b2e")
    for bx, by in ((ox + 2.2, oy + 5.0), (ox + 4.0, oy + 6.2), (ox + 2.4, oy + 7.8)):
        tx, ty, rx = _cylinder(g, bx, by, z, 0.9, 2.2, "#1f2a44", "#2f3d61")
        g.out.append(f'<rect x="{tx - rx:.1f}" y="{ty + 0.6 * g.s:.1f}" width="{2 * rx:.1f}" height="{0.18 * g.s:.1f}" fill="#ffd23f"/>'
                     f'<rect x="{tx - rx:.1f}" y="{ty + 1.5 * g.s:.1f}" width="{2 * rx:.1f}" height="{0.18 * g.s:.1f}" fill="#ffd23f"/>')
    dx, dy = g.p(ox + 4.6, oy + 3.6, z + 2.6)
    g.out.append(f'<path d="M{dx:.1f} {dy:.1f} c{0.9 * g.s:.1f} {1.2 * g.s:.1f} {0.9 * g.s:.1f} {2.0 * g.s:.1f} 0 {2.0 * g.s:.1f} '
                 f'c{-0.9 * g.s:.1f} 0 {-0.9 * g.s:.1f} {-0.8 * g.s:.1f} 0 {-2.0 * g.s:.1f} z" fill="#111" filter="url(#glow)"/>')


def _rocket(g, ox=0.0, oy=0.0, z=0.6):
    g.box(ox + 1.8, oy + 1.8, z, 3.0, 3.0, 0.3, "#9aa1ad")
    tx, ty, rx = _cylinder(g, ox + 3.3, oy + 3.3, z + 0.3, 0.85, 5.6, "#f4f1ea", "#ffffff")
    g.out.append(f'<path d="M{tx - rx:.1f} {ty:.1f} Q{tx:.1f} {ty - 2.6 * g.s:.1f} {tx + rx:.1f} {ty:.1f} Z" fill="#e63b2e"/>'
                 f'<circle cx="{tx:.1f}" cy="{ty + 1.4 * g.s:.1f}" r="{0.4 * g.s:.1f}" fill="#6aa8ff" stroke="#1f2a44" stroke-width="2"/>')
    bx, by = g.p(ox + 3.3, oy + 3.3, z + 0.3)
    g.out.append(f'<path d="M{bx - rx:.1f} {by - 1.4 * g.s:.1f} l{-0.8 * g.s:.1f} {1.6 * g.s:.1f} l{0.8 * g.s:.1f} {-0.2 * g.s:.1f} Z '
                 f'M{bx + rx:.1f} {by - 1.4 * g.s:.1f} l{0.8 * g.s:.1f} {1.6 * g.s:.1f} l{-0.8 * g.s:.1f} {-0.2 * g.s:.1f} Z" fill="#e63b2e"/>')
    g.box(ox + 5.6, oy + 6.4, z, 3.6, 1.8, 0.7, "#e63b2e")
    g.box(ox + 6.4, oy + 6.6, z + 0.7, 1.9, 1.4, 0.6, "#1f2a44")
    for wx in (6.2, 8.6):
        cx, cy = g.p(ox + wx, oy + 8.2, z + 0.15)
        g.out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{0.42 * g.s:.1f}" ry="{0.5 * g.s:.1f}" fill="#111"/>')
    g.line([(ox + 5.4, oy + 4.8, z + 0.05), (ox + 5.4, oy + 6.0, z + 0.05)], "#ffd23f", 5, 'filter="url(#glow)"')


def _gold(g, ox=0.0, oy=0.0, z=0.6):
    for k, h in enumerate((1.2, 2.0, 2.8)):
        g.box(ox + 8.0, oy + 0.8 + k * 1.0, z, 0.8, 0.7, h, "#e63b2e")
    for row, (n, zz) in enumerate(((3, 0.0), (2, 0.6), (1, 1.2))):
        for k in range(n):
            g.box(ox + 1.6 + row * 1.3 + k * 2.6, oy + 4.2, z + zz, 2.4, 1.3, 0.6, "#e3a91a")
    for k in range(2):
        g.box(ox + 2.2 + k * 2.6, oy + 6.6, z, 2.4, 1.3, 0.6, "#e3a91a")
    _cylinder(g, ox + 7.6, oy + 7.6, z, 1.0, 0.35, "#c9971c", "#ffd23f")


SCENES = {"chip": (_chip, "#13584f", 0.8), "deal": (_deal, "#1d2b4f", 0.6), "code": (_code, "#0f4a4a", 0.6),
          "oil": (_oil, "#5b4636", 0.6), "rocket": (_rocket, "#1d2b4f", 0.6), "gold": (_gold, "#13584f", 0.6)}


def scene_svg(kind, size=300, bg=None):
    draw, slab, z = SCENES[kind]
    sc = size / 19
    g = Iso(sc, size / 2, 6.9 * sc)
    g.box(0, 0, 0, 10, 10, z, slab)
    draw(g, z=z)
    back = f'<circle cx="{size / 2}" cy="{size / 2}" r="{size / 2}" fill="{bg}"/>' if bg else ""
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">{DEFS}{back}{"".join(g.out)}</svg>'


def cover_art(w=440, h=560, kinds=("chip", "deal", "code")):
    sc = w / 25
    g = Iso(sc, w / 2, (h - 21 * sc) / 2 + 1.5 * sc)
    g.box(0, 0, 0, 20, 20, 0.9, "#13584f")
    for k in range(1, 4):
        g.line([(k * 5, 0.5, 0.9), (k * 5, 19.5, 0.9)], "#1f7a6d", 2)
        g.line([(0.5, k * 5, 0.9), (19.5, k * 5, 0.9)], "#1f7a6d", 2)
    kinds = (list(kinds) + ["chip", "deal", "code"])[:3]
    SCENES[kinds[1]][0](g, 10, 0, 0.9)
    SCENES[kinds[0]][0](g, 0, 4, 0.9)
    SCENES[kinds[2]][0](g, 10, 10, 0.9)
    return f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}
<rect width="{w}" height="{h}" fill="#111"/>
<g opacity=".18" stroke="#f4f1ea">{''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w, 40))}{''.join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h, 40))}</g>
{"".join(g.out)}</svg>"""
