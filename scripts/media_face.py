"""Make the lip-synced presenter look alive: eye blinks and small head motion.

Wav2Lip (see make_media.talking_head) only redraws the mouth. This pass runs on its frames:
- blinks: the real upper lid slides down (its lash row moves as is, a thin strip of lid skin
  above it is stretched to fill the gap) for ~0.25 s at natural, slightly irregular intervals;
- head: a small tilt / nod / sway of the head region around the chin, feathered into the
  neck so shoulders and background stay put; it nods a little more while speaking.
Uses OpenCV's bundled Haar cascades only (no downloads), a few ms per frame on a CPU.
"""
import math
import random

import cv2
import numpy as np


def analyze(img):
    """Face box and up to two eye boxes (full-image coords), or None if no face is found."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    ec = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    faces = fc.detectMultiScale(g, 1.1, 5, minSize=(120, 120))
    if len(faces) == 0:
        return None
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    eyes = ec.detectMultiScale(g[y:y + h * 5 // 8, x:x + w], 1.05, 6, minSize=(w // 10, w // 10))
    eyes = sorted(eyes, key=lambda e: -e[2] * e[3])[:2]
    return {"face": (int(x), int(y), int(w), int(h)),
            "eyes": [(int(x + ex), int(y + ey), int(ew), int(eh)) for ex, ey, ew, eh in eyes]}


def _opening(gray, eye):
    """Tight box (x0, x1, top, bottom) of the dark lash/iris band inside a Haar eye box."""
    ex, ey, ew, _ = eye
    r = gray[ey:ey + ew, ex:ex + ew] < 70
    r[:, r.mean(0) > 0.6] = False                         # hair beside the eye is dark in every row
    rows = r.sum(1) >= 0.2 * ew
    best, cur = (0, 0), None
    for i in range(ew // 4, ew):                          # skip the brow at the top of the box
        if rows[i]:
            cur = i if cur is None else cur
            if i - cur > best[1] - best[0]:
                best = (cur, i)
        else:
            cur = None
    t, b = best
    cols = np.nonzero(r[t:b + 1].sum(0) >= 3)[0]
    if b - t < ew // 10 or len(cols) < ew // 3:
        return None
    return ex + int(cols.min()), ex + int(cols.max()), ey + t, ey + b


def _lid_map(shape, op, level):
    """Row lookup that slides the upper lid (lash row + a stretched strip of lid skin) down by `level`."""
    x0, x1, t, b = op
    cx, cy, hw, oh = (x0 + x1) / 2, (t + b) / 2, 0.55 * (x1 - x0), b - t
    X, Y = np.meshgrid(np.arange(shape[1], dtype=np.float32), np.arange(shape[0], dtype=np.float32))
    s = np.clip(1 - ((X - cx) / hw) ** 2, 0, 1) ** 0.75   # almond: full height mid-eye, 0 at corners
    top = cy - 0.5 * oh * s
    d = level * oh * s * 0.97                             # how far the lid edge drops here
    lash = top - 0.42 * oh                                # top of the lash row
    strip = lash - 0.3 * oh                               # skin above it, stretched to fill the gap
    sy = Y.copy()
    skin = (Y >= strip) & (Y < lash + d)
    sy[skin] = (strip + (Y - strip) * (lash - strip) / np.maximum(lash + d - strip, 1))[skin]
    row = (Y >= lash + d) & (Y < top + 0.08 * oh + d)
    sy[row] = (Y - d)[row]
    return X, sy


def blink_curve(n_frames, fps, seed=7):
    """Eye closure 0..1 per frame: blinks every ~2.5-5.5 s, ~0.25 s long, sometimes double."""
    rng, c, t = random.Random(seed), np.zeros(n_frames, np.float32), 1.2
    shape = [0.35, 0.8, 1.0, 1.0, 0.75, 0.45, 0.2]       # close fast, open slower
    while t * fps < n_frames:
        for rep in range(2 if rng.random() < 0.18 else 1):
            start = int((t + rep * 0.35) * fps)
            for i, v in enumerate(np.interp(np.linspace(0, len(shape) - 1, max(4, int(0.25 * fps))),
                                            range(len(shape)), shape)):
                if 0 <= start + i < n_frames:
                    c[start + i] = max(c[start + i], v)
        t += rng.uniform(2.5, 5.5)
    return c


def head_motion(n_frames, fps, speech):
    """(angle deg, dx px, dy px) per frame: slow idle sway plus a nod that follows speech energy."""
    t = np.arange(n_frames) / fps
    win = max(1, int(0.4 * fps))
    s = np.convolve(np.asarray(speech[:n_frames], np.float32), np.ones(win) / win, mode="same")
    s = np.pad(s, (0, max(0, n_frames - len(s))))
    angle = 1.8 * np.sin(2 * np.pi * t / 6.1) + 0.8 * np.sin(2 * np.pi * t / 2.9 + 0.8) + 1.5 * (s - s.mean())
    dx = 5.0 * np.sin(2 * np.pi * t / 7.7)
    dy = 3.0 * np.sin(2 * np.pi * t / 4.3) + 6.0 * s
    return angle, dx, dy


def animate(frame_paths, base_img, fps, speech, alpha=None, width=None):
    """Blink and move the head on every frame. Without `alpha` frames are rewritten in place; with a cut-out
    mask (same size as base_img) each frame becomes a .webp with transparency (the mask moves with the head),
    scaled to `width`. Returns the written paths, or [] if no face was found."""
    info = analyze(base_img)
    if not info:
        return []
    x, y, w, h = info["face"]
    gray = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    ops = [o for o in (_opening(gray, e) for e in info["eyes"]) if o]
    levels = (0.25, 0.5, 0.75, 1.0)                       # lid positions while blinking
    lids = {}
    if len(ops) == 2:
        for lv in levels:
            mx, my0 = _lid_map(base_img.shape, ops[0], lv)
            my1 = _lid_map(base_img.shape, ops[1], lv)[1]
            rows = np.arange(my0.shape[0], dtype=np.float32)[:, None]
            lids[lv] = (mx, my0 + my1 - rows)               # the eyes don't overlap: add both shifts
    head = np.zeros(base_img.shape[:2], np.float32)
    cv2.ellipse(head, (x + w // 2, y + int(h * 0.42)), (int(w * 0.82), int(h * 0.98)), 0, 0, 360, 1.0, -1)
    k = (int(w * 0.35) | 1)
    head = cv2.GaussianBlur(head, (k, k), 0)[..., None]
    pivot = (x + w / 2, y + h * 1.08)                     # chin / neck
    n = len(frame_paths)
    closure, (angle, dx, dy) = blink_curve(n, fps), head_motion(n, fps, speech)
    size = (width, round(base_img.shape[0] * width / base_img.shape[1])) if width else None
    outs = []
    for i, p in enumerate(frame_paths):
        f = cv2.imread(str(p))
        if f is None or f.shape[:2] != base_img.shape[:2]:
            continue
        if closure[i] > 0.12 and lids:
            mx, my = lids[min(levels, key=lambda v: abs(v - closure[i]))]
            f = cv2.remap(f, mx, my, cv2.INTER_LINEAR)
        m = cv2.getRotationMatrix2D(pivot, float(angle[i]), 1.0)
        m[:, 2] += (float(dx[i]), float(dy[i]))
        moved = cv2.warpAffine(f, m, (f.shape[1], f.shape[0]), borderMode=cv2.BORDER_REFLECT)
        f = (moved * head + f * (1 - head)).astype(np.uint8)
        if alpha is None:
            cv2.imwrite(str(p), f, [cv2.IMWRITE_JPEG_QUALITY, 92])
            outs.append(p)
            continue
        a = cv2.warpAffine(alpha, m, (f.shape[1], f.shape[0]))
        a = (a * head[..., 0] + alpha * (1 - head[..., 0])).astype(np.uint8)
        f = np.dstack([f, a])
        if size:
            f = cv2.resize(f, size, interpolation=cv2.INTER_AREA)
        out = p.with_suffix(".webp")
        cv2.imwrite(str(out), f, [cv2.IMWRITE_WEBP_QUALITY, 92])
        p.unlink()
        outs.append(out)
    return outs
