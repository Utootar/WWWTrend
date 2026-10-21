"""Make the lip-synced presenter look alive: eye blinks and small head motion.

Wav2Lip (see make_media.talking_head) only redraws the mouth. This pass runs on its frames:
- blinks: a closed-eye patch (eyelid skin stretched over the eye + lash line) faded in
  for ~0.25 s at natural, slightly irregular intervals;
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


def _closed_eye(img, eye, level=1.0):
    """Image with the upper lid lowered over the top `level` of one eye, and a feathered mask for it."""
    ex, ey, ew, _ = eye
    cx, cy = ex + ew / 2, ey + ew / 2 + 0.03 * ew
    ow, oh = int(0.70 * ew), int(0.30 * ew)              # eye opening
    x0, y0 = int(cx - ow / 2), int(cy - oh / 2)
    out = img.copy()
    skin = img[y0 + oh + 2:y0 + oh + 2 + max(4, int(0.5 * oh)), x0:x0 + ow]   # plain under-eye skin
    if skin.size == 0:
        return out, np.zeros(img.shape[:2], np.float32)
    lid_h = max(2, int(oh * level))
    lid = cv2.GaussianBlur(cv2.resize(cv2.flip(skin, 0), (ow, lid_h)), (7, 7), 0).astype(np.float32)
    ring = np.concatenate([img[y0 - oh // 2:y0, x0:x0 + ow].reshape(-1, 3), skin.reshape(-1, 3)]).astype(np.float32)
    lid *= ring.mean(0) / np.maximum(lid.reshape(-1, 3).mean(0), 1)         # match the lid's tone
    out[y0:y0 + lid_h, x0:x0 + ow] = np.clip(lid, 0, 255).astype(np.uint8)
    edge = y0 + lid_h - (0 if level >= 1 else 2)
    pts = np.array([[x0 + i * ow / 12, edge + math.sin(math.pi * i / 12) * 0.16 * oh * level]
                    for i in range(13)], np.int32)
    lash = out.copy()
    cv2.polylines(lash, [pts], False, (34, 26, 24), max(2, ew // 55), cv2.LINE_AA)
    out = cv2.addWeighted(lash, 0.8, out, 0.2, 0)
    mask = np.zeros(img.shape[:2], np.float32)
    cv2.ellipse(mask, (int(cx), int(y0 + lid_h / 2 + 1)), (int(ow * 0.5), int(lid_h * 0.62 + 3)), 0, 0, 360, 1.0, -1)
    k = max(5, (ew // 6) | 1)
    return out, cv2.GaussianBlur(mask, (k, k), 0)


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
    angle = 1.3 * np.sin(2 * np.pi * t / 6.1) + 0.6 * np.sin(2 * np.pi * t / 2.9 + 0.8) + 1.1 * (s - s.mean())
    dx = 3.0 * np.sin(2 * np.pi * t / 7.7)
    dy = 2.0 * np.sin(2 * np.pi * t / 4.3) + 5.0 * s
    return angle, dx, dy


def animate(frame_paths, base_img, fps, speech):
    """Blink and move the head on every frame in place. Returns False if no face was found."""
    info = analyze(base_img)
    if not info:
        return False
    x, y, w, h = info["face"]
    levels = (0.35, 0.7, 1.0)                             # lid positions while blinking
    eyes = {lv: [_closed_eye(base_img, e, lv) for e in info["eyes"]] for lv in levels} \
        if len(info["eyes"]) == 2 else {}
    head = np.zeros(base_img.shape[:2], np.float32)
    cv2.ellipse(head, (x + w // 2, y + int(h * 0.42)), (int(w * 0.82), int(h * 0.98)), 0, 0, 360, 1.0, -1)
    k = (int(w * 0.35) | 1)
    head = cv2.GaussianBlur(head, (k, k), 0)[..., None]
    pivot = (x + w / 2, y + h * 1.08)                     # chin / neck
    n = len(frame_paths)
    closure, (angle, dx, dy) = blink_curve(n, fps), head_motion(n, fps, speech)
    for i, p in enumerate(frame_paths):
        f = cv2.imread(str(p))
        if f is None or f.shape[:2] != base_img.shape[:2]:
            continue
        if closure[i] > 0.15 and eyes:
            lv = min(levels, key=lambda v: abs(v - closure[i]))
            for closed, mask in eyes[lv]:
                a = mask[..., None]
                f = (f * (1 - a) + closed * a).astype(np.uint8)
        m = cv2.getRotationMatrix2D(pivot, float(angle[i]), 1.0)
        m[:, 2] += (float(dx[i]), float(dy[i]))
        moved = cv2.warpAffine(f, m, (f.shape[1], f.shape[0]), borderMode=cv2.BORDER_REFLECT)
        f = (moved * head + f * (1 - head)).astype(np.uint8)
        cv2.imwrite(str(p), f, [cv2.IMWRITE_JPEG_QUALITY, 92])
    return True
