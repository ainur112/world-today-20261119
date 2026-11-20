#!/usr/bin/env python3
"""Render 'The World Today — Thursday 19 November 2026' front page to entry.png.

Build-time renderer (Pillow). The submitted entry program (main.py) only copies
the produced entry.png to /output/entry.png, per the bounty's simplest-entry rule.
All artwork is drawn here from primitives; all facts are sourced in SOURCES.md.
Deterministic: no clock, no randomness, no network.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 26                      # page margin
CW = W - 2 * M              # content width

# Newsprint palette
PAPER = (247, 243, 232)
INK = (26, 26, 26)
FAINT = (120, 114, 100)
RED = (179, 38, 30)
BLUE = (29, 78, 137)
GOLD = (191, 148, 40)
TEAL = (23, 107, 100)
CREAM = (252, 249, 240)
NAVY = (18, 28, 48)
GREEN = (38, 122, 68)
SKIN = (222, 184, 150)

FONT_DIR = "fonts/"
_fcache = {}


def font(name, size, weight=None):
    key = (name, size, weight)
    if key not in _fcache:
        f = ImageFont.truetype(FONT_DIR + name, size)
        if weight is not None:
            try:
                f.set_variation_by_axes([weight])
            except Exception:
                pass
        _fcache[key] = f
    return _fcache[key]


def masthead_font(size):
    return font("PlayfairDisplay.ttf", size, 900)


def head(size):
    return font("Lato-Black.ttf", size)


def bold(size):
    return font("Lato-Bold.ttf", size)


def body(size):
    return font("PT_Serif-Web-Regular.ttf", size)


def bodyb(size):
    return font("PT_Serif-Web-Bold.ttf", size)


def ital(size):
    return font("Lato-Italic.ttf", size)


def mono(size):
    return font("IBMPlexMono-Medium.ttf", size)


def kicker(size=12):
    return font("ArchivoBlack-Regular.ttf", size)


def bebas(size):
    return font("BebasNeue-Regular.ttf", size)


def tw(d, text, f):
    return d.textlength(text, font=f)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, maxw, fill=INK, leading=None):
    leading = leading or int(f.size * 1.32)
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def headline(d, x, y, text, size, maxw, fill=INK, leading=None):
    f = head(size)
    leading = leading or int(size * 1.08)
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def kick(d, x, y, text, fill=RED, size=12):
    d.text((x, y), text.upper(), font=kicker(size), fill=fill)
    return y + size + 6


def rule(d, x, y, w, fill=INK, width=1):
    d.rectangle([x, y, x + w - 1, y + width - 1], fill=fill)


def vrule(d, x, y, h, fill=(180, 174, 158), width=1):
    d.rectangle([x, y, x + width - 1, y + h - 1], fill=fill)


def chip(d, x, y, text, bg=INK, fg=CREAM, size=12, pad=5):
    f = mono(size)
    w = int(tw(d, text, f)) + 2 * pad
    h = size + 2 * pad - 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + pad, y + pad - 2), text, font=f, fill=fg)
    return w


# ---------------------------------------------------------------- illustrations
def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 240, 235))
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7 - 1], fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.45, y + h * 0.54], fill=(60, 70, 120))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy, r = x + w * 0.22, y + h * 0.3, h * 0.16
    star(d, cx, cy, r, (255, 222, 0))
    for dx, dy in [(0.42, 0.12), (0.5, 0.26), (0.5, 0.44), (0.42, 0.58)]:
        star(d, x + w * dx, y + h * dy, h * 0.055, (255, 222, 0))


def flag_ru(d, x, y, w, h):
    for i, c in enumerate([(240, 240, 240), (0, 57, 166), (213, 43, 30)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3 - 1], fill=c)


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def bust(d, cx, base_y, s, suit, tie, hair=(40, 32, 26)):
    # simple statesman silhouette: shoulders, head, hair, tie. s = head radius
    d.polygon([(cx - 2.6 * s, base_y), (cx - 2.2 * s, base_y - 2.6 * s),
               (cx - 0.9 * s, base_y - 3.3 * s), (cx + 0.9 * s, base_y - 3.3 * s),
               (cx + 2.2 * s, base_y - 2.6 * s), (cx + 2.6 * s, base_y)], fill=suit)
    d.polygon([(cx - 0.55 * s, base_y - 3.2 * s), (cx + 0.55 * s, base_y - 3.2 * s),
               (cx + 0.3 * s, base_y - 1.2 * s), (cx, base_y - 0.9 * s),
               (cx - 0.3 * s, base_y - 1.2 * s)], fill=(245, 243, 236))
    d.polygon([(cx - 0.16 * s, base_y - 3.0 * s), (cx + 0.16 * s, base_y - 3.0 * s),
               (cx + 0.12 * s, base_y - 1.4 * s), (cx, base_y - 1.1 * s),
               (cx - 0.12 * s, base_y - 1.4 * s)], fill=tie)
    d.ellipse([cx - s, base_y - 5.4 * s, cx + s, base_y - 3.2 * s], fill=SKIN)
    d.ellipse([cx - s * 1.02, base_y - 5.5 * s, cx + s * 1.02, base_y - 4.3 * s], fill=hair)


def il_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    # Shenzhen skyline
    sky = (150, 168, 188)
    towers = [(0.04, 0.42), (0.10, 0.62), (0.16, 0.50), (0.22, 0.78), (0.28, 0.55),
              (0.34, 0.66), (0.42, 0.95), (0.50, 0.60), (0.56, 0.72), (0.62, 0.52),
              (0.70, 0.82), (0.78, 0.58), (0.84, 0.68), (0.92, 0.46)]
    for fx, fh in towers:
        tx, th = x + fx * w, fh * h * 0.52
        d.rectangle([tx, y + h * 0.52 - th, tx + w * 0.045, y + h * 0.52], fill=sky)
    d.polygon([(x + 0.42 * w, y + h * 0.52 - 0.95 * h * 0.52),
               (x + 0.42 * w + w * 0.0225, y + h * 0.52 - 0.95 * h * 0.52 - h * 0.07),
               (x + 0.42 * w + w * 0.045, y + h * 0.52 - 0.95 * h * 0.52)], fill=sky)
    d.rectangle([x, y + h * 0.52, x + w, y + h], fill=(206, 214, 222))
    # flags on poles
    for fx, fl in [(0.16, flag_us), (0.475, flag_cn), (0.79, flag_ru)]:
        px = x + fx * w
        d.rectangle([px - 1, y + h * 0.10, px + 1, y + h * 0.62], fill=(90, 96, 104))
        fl(d, px + 2, y + h * 0.11, w * 0.075, h * 0.16)
    # table
    d.ellipse([x + w * 0.10, y + h * 0.70, x + w * 0.90, y + h * 0.94], fill=(120, 86, 54))
    d.ellipse([x + w * 0.12, y + h * 0.68, x + w * 0.88, y + h * 0.88], fill=(150, 110, 72))
    # three leaders behind table
    s = h * 0.052
    bust(d, x + w * 0.26, y + h * 0.74, s, (30, 36, 52), (178, 34, 52), hair=(120, 90, 50))
    bust(d, x + w * 0.50, y + h * 0.72, s, (28, 28, 32), (160, 30, 30), hair=(22, 20, 18))
    bust(d, x + w * 0.74, y + h * 0.74, s, (34, 38, 50), (60, 80, 140), hair=(150, 140, 130))
    # name plates
    for fx, name in [(0.26, "TRUMP"), (0.50, "XI"), (0.74, "PUTIN")]:
        f = bold(int(h * 0.075))
        d.text((x + fx * w - tw(d, name, f) / 2, y + h * 0.80), name, font=f, fill=CREAM)


def il_berlin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 226, 232))
    # circle of stars (EU) above gate
    cx, cy, r = x + w * 0.5, y + h * 0.30, h * 0.20
    for i in range(12):
        a = i * math.pi / 6
        star(d, cx + r * math.cos(a), cy + r * math.sin(a), h * 0.035, GOLD)
    # Brandenburg gate
    gx, gy, gw, gh = x + w * 0.28, y + h * 0.50, w * 0.44, h * 0.42
    d.rectangle([gx, gy, gx + gw, gy + gh * 0.18], fill=(110, 116, 126))
    for i in range(5):
        cxp = gx + gw * (0.08 + i * 0.21)
        d.rectangle([cxp, gy + gh * 0.18, cxp + gw * 0.07, gy + gh], fill=(130, 136, 146))
    d.rectangle([gx + gw * 0.36, gy - gh * 0.16, gx + gw * 0.64, gy], fill=(100, 106, 116))
    d.rectangle([gx + gw * 0.44, gy - gh * 0.26, gx + gw * 0.56, gy - gh * 0.16], fill=(90, 96, 106))
    # small leader silhouettes in front
    for i, fx in enumerate([0.14, 0.22, 0.78, 0.86]):
        bust(d, x + w * fx, y + h * 0.97, h * 0.030, (40, 44, 56), RED if i % 2 else BLUE)
    d.rectangle([x, y + h * 0.94, x + w, y + h], fill=(180, 186, 194))


def il_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # grid
    for i in range(1, 4):
        d.line([x + 8, y + i * h / 4, x + w - 8, y + i * h / 4], fill=(40, 52, 78), width=1)
    # ANT line: pop then pare
    pts = [(0.02, 0.72), (0.10, 0.70), (0.16, 0.30), (0.22, 0.16), (0.30, 0.34),
           (0.40, 0.40), (0.52, 0.38), (0.64, 0.44), (0.78, 0.42), (0.98, 0.46)]
    pp = [(x + fx * w, y + fy * h) for fx, fy in pts]
    for i in range(len(pp) - 1):
        col = GREEN if pp[i + 1][1] < pp[i][1] else (214, 69, 56)
        d.line([pp[i], pp[i + 1]], fill=col, width=3)
    d.ellipse([pp[3][0] - 4, pp[3][1] - 4, pp[3][0] + 4, pp[3][1] + 4], fill=(255, 210, 80))
    d.text((x + 10, y + 6), "ANT", font=bebas(int(h * 0.34)), fill=(255, 255, 255))
    d.text((x + 10 + tw(d, "ANT", bebas(int(h * 0.34))) + 8, y + 10),
           "NASDAQ DEBUT", font=mono(int(h * 0.11)), fill=(150, 170, 200))
    d.text((x + w - 118, y + 6), "$83 → $111.50", font=mono(int(h * 0.12)), fill=(255, 210, 80))
    d.text((x + w - 118, y + h - 20), "OPEN +34%", font=mono(int(h * 0.12)), fill=(120, 220, 150))


def il_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    cx = x + w * 0.5
    # scales of justice
    d.rectangle([cx - 2, y + h * 0.16, cx + 2, y + h * 0.80], fill=(90, 74, 40))
    d.rectangle([cx - w * 0.16, y + h * 0.80, cx + w * 0.16, y + h * 0.86], fill=(90, 74, 40))
    d.line([cx - w * 0.26, y + h * 0.24, cx + w * 0.26, y + h * 0.24], fill=(90, 74, 40), width=3)
    for sx in (-1, 1):
        px = cx + sx * w * 0.26
        d.line([px, y + h * 0.24, px - w * 0.07, y + h * 0.48], fill=(90, 74, 40), width=2)
        d.line([px, y + h * 0.24, px + w * 0.07, y + h * 0.48], fill=(90, 74, 40), width=2)
        d.pieslice([px - w * 0.085, y + h * 0.42, px + w * 0.085, y + h * 0.58], 0, 180, fill=GOLD)
    star(d, cx, y + h * 0.12, h * 0.06, GOLD)
    d.text((x + 12, y + h - 24), "THE HAGUE", font=mono(int(h * 0.12)), fill=FAINT)
    chip(d, x + w - 64, y + h - 28, "9–6", bg=INK, size=int(h * 0.12))


def il_gta(d, x, y, w, h):
    # Vice City sunset
    for i in range(h):
        t = i / h
        c = (int(255 - 90 * t), int(105 + 60 * t), int(150 - 60 * t)) if t < 0.55 else \
            (int(165 - 100 * (t - 0.55)), int(165 - 120 * (t - 0.55)), int(90 + 60 * (t - 0.55)))
        d.line([x, y + i, x + w, y + i], fill=c)
    # sun with scanlines
    scx, scy, sr = x + w * 0.5, y + h * 0.52, h * 0.30
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=(255, 190, 90))
    for i in range(4):
        yy = scy + sr * (0.15 + i * 0.22)
        d.rectangle([scx - sr, yy, scx + sr, yy + 2 + i], fill=(230, 90, 130))
    # palms
    for px, ph, lean in [(0.10, 0.72, 1), (0.90, 0.62, -1)]:
        bx, by = x + px * w, y + h
        tx, ty = bx + lean * w * 0.03, by - ph * h
        d.line([bx, by, tx, ty], fill=(30, 20, 40), width=4)
        for a in range(7):
            ang = -math.pi / 2 + (a - 3) * 0.42
            d.line([tx, ty, tx + math.cos(ang) * w * 0.075, ty + math.sin(ang) * h * 0.16 + h * 0.05],
                   fill=(30, 20, 40), width=3)
    # neon VI
    f = bebas(int(h * 0.52))
    t = "VI"
    d.text((x + w * 0.5 - tw(d, t, f) / 2 + 1, y + h * 0.16 + 1), t, font=f, fill=(255, 60, 160))
    d.text((x + w * 0.5 - tw(d, t, f) / 2, y + h * 0.16), t, font=f, fill=(255, 235, 245))
    d.text((x + 8, y + h - 18), "VICE CITY · LEONIDA", font=mono(int(h * 0.10)), fill=(255, 220, 235))


def il_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 62, 100))
    # sea texture
    for i in range(6):
        d.arc([x - 20 + i * 60, y + h * 0.7, x + 40 + i * 60, y + h * 1.1], 200, 340, fill=(36, 80, 124), width=2)
    # coast on right
    d.polygon([(x + w * 0.82, y), (x + w, y), (x + w, y + h), (x + w * 0.74, y + h),
               (x + w * 0.80, y + h * 0.5)], fill=(196, 178, 140))
    d.polygon([(x + w * 0.82, y), (x + w * 0.86, y), (x + w * 0.84, y + h * 0.5),
               (x + w * 0.78, y + h), (x + w * 0.74, y + h), (x + w * 0.80, y + h * 0.5)], fill=(150, 160, 120))
    # spiral storm
    cx, cy = x + w * 0.38, y + h * 0.52
    for arm in range(2):
        pts = []
        for i in range(60):
            t = i / 60
            ang = arm * math.pi + t * 3.6 * math.pi
            r = h * 0.06 + t * h * 0.40
            pts.append((cx + r * math.cos(ang) * 1.25, cy + r * math.sin(ang) * 0.8))
        d.line(pts, fill=(235, 240, 245), width=max(2, int(h * 0.05)))
    d.ellipse([cx - h * 0.055, cy - h * 0.045, cx + h * 0.055, cy + h * 0.045], fill=(16, 44, 74))
    # forecast arrow to coast
    d.line([cx + h * 0.3, cy, x + w * 0.76, y + h * 0.42], fill=(255, 210, 80), width=2)
    d.polygon([(x + w * 0.78, y + h * 0.40), (x + w * 0.72, y + h * 0.38),
               (x + w * 0.74, y + h * 0.48)], fill=(255, 210, 80))
    d.text((x + 8, y + 6), "BAY OF BENGAL", font=mono(int(h * 0.10)), fill=(170, 200, 230))
    d.text((x + w * 0.80, y + h - 18), "ANDHRA", font=mono(int(h * 0.09)), fill=INK)


def il_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 208, 196))
    # ruined skyline
    rub = (140, 134, 124)
    for fx, fw, fh in [(0.02, 0.10, 0.45), (0.14, 0.08, 0.62), (0.24, 0.12, 0.38),
                       (0.40, 0.09, 0.55), (0.52, 0.11, 0.42), (0.66, 0.08, 0.60), (0.78, 0.12, 0.35)]:
        bx, bw, bh = x + fx * w, fw * w, fh * h * 0.6
        d.rectangle([bx, y + h * 0.62 - bh, bx + bw, y + h * 0.62], fill=rub)
        d.polygon([(bx, y + h * 0.62 - bh), (bx + bw * 0.4, y + h * 0.62 - bh - h * 0.05),
                   (bx + bw * 0.7, y + h * 0.62 - bh), (bx + bw, y + h * 0.62 - bh + h * 0.03)], fill=rub)
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(190, 182, 168))
    # tents
    for fx, s in [(0.12, 1.0), (0.30, 0.8), (0.50, 1.1), (0.70, 0.85), (0.86, 0.95)]:
        tx, ty, ts = x + fx * w, y + h * 0.92, h * 0.16 * s
        d.polygon([(tx - ts, ty), (tx, ty - ts * 1.1), (tx + ts, ty)], fill=(235, 232, 222), outline=(120, 114, 100))
        d.line([tx, ty - ts * 1.1, tx, ty], fill=(120, 114, 100), width=1)
    # yellow line
    for i in range(12):
        d.rectangle([x + i * w / 12, y + h * 0.66, x + i * w / 12 + w / 24, y + h * 0.66 + 2], fill=(212, 175, 55))
    d.text((x + 8, y + 6), "CEASEFIRE 'YELLOW LINE'", font=mono(int(h * 0.10)), fill=(110, 100, 70))


def il_venezuela(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 230, 224))
    # oil derrick
    dx, dy = x + w * 0.78, y + h * 0.9
    d.polygon([(dx - w * 0.07, dy), (dx - w * 0.02, y + h * 0.18), (dx + w * 0.02, y + h * 0.18),
               (dx + w * 0.07, dy)], outline=(60, 60, 60), width=2)
    for i in range(4):
        yy = y + h * (0.3 + i * 0.15)
        d.line([dx - w * 0.05 + i, yy, dx + w * 0.05 - i, yy], fill=(60, 60, 60), width=2)
    # handshake: two sleeves + clasped hands
    hy = y + h * 0.58
    d.rectangle([x + w * 0.10, hy - h * 0.07, x + w * 0.34, hy + h * 0.09], fill=(30, 36, 52))
    d.rectangle([x + w * 0.52, hy - h * 0.07, x + w * 0.66, hy + h * 0.09], fill=(120, 40, 40))
    d.ellipse([x + w * 0.30, hy - h * 0.10, x + w * 0.46, hy + h * 0.10], fill=SKIN)
    d.ellipse([x + w * 0.40, hy - h * 0.10, x + w * 0.56, hy + h * 0.10], fill=(200, 160, 126))
    flag_us(d, x + w * 0.08, y + h * 0.12, w * 0.10, h * 0.18)
    d.rectangle([x + w * 0.22, y + h * 0.12, x + w * 0.32, y + h * 0.30], fill=(250, 200, 50))
    d.rectangle([x + w * 0.22, y + h * 0.18, x + w * 0.32, y + h * 0.24], fill=(0, 60, 150))
    d.rectangle([x + w * 0.22, y + h * 0.24, x + w * 0.32, y + h * 0.30], fill=(200, 40, 40))
    d.text((x + 8, y + h - 18), "CARACAS", font=mono(int(h * 0.10)), fill=FAINT)


# ------------------------------------------------------------------- small icons
def icon(d, kind, x, y, s, fill=INK):
    c = fill
    if kind == "bridge":
        d.line([x, y + s * 0.7, x + s, y + s * 0.7], fill=c, width=2)
        d.arc([x + s * 0.1, y + s * 0.2, x + s * 0.9, y + s * 1.2], 180, 360, fill=c, width=2)
        d.line([x + s * 0.3, y + s * 0.42, x + s * 0.3, y + s * 0.7], fill=c, width=1)
        d.line([x + s * 0.7, y + s * 0.42, x + s * 0.7, y + s * 0.7], fill=c, width=1)
    elif kind == "ice":
        d.polygon([(x + s * 0.2, y + s * 0.7), (x + s * 0.45, y + s * 0.15), (x + s * 0.6, y + s * 0.45),
                   (x + s * 0.8, y + s * 0.7)], fill=c)
        d.line([x, y + s * 0.75, x + s, y + s * 0.75], fill=BLUE, width=2)
    elif kind == "gavel":
        d.rectangle([x + s * 0.15, y + s * 0.15, x + s * 0.6, y + s * 0.4], fill=c)
        d.line([x + s * 0.4, y + s * 0.4, x + s * 0.85, y + s * 0.85], fill=c, width=2)
    elif kind == "tower":
        d.polygon([(x + s * 0.35, y + s * 0.85), (x + s * 0.45, y + s * 0.1), (x + s * 0.55, y + s * 0.1),
                   (x + s * 0.65, y + s * 0.85)], fill=c)
        d.line([x + s * 0.1, y + s * 0.3, x + s * 0.4, y + s * 0.42], fill=RED, width=2)
    elif kind == "capitol":
        d.rectangle([x + s * 0.15, y + s * 0.5, x + s * 0.85, y + s * 0.85], fill=c)
        d.pieslice([x + s * 0.25, y + s * 0.15, x + s * 0.75, y + s * 0.65], 180, 360, fill=c)
        d.line([x + s * 0.5, y + s * 0.05, x + s * 0.5, y + s * 0.2], fill=c, width=2)
    elif kind == "shield":
        d.polygon([(x + s * 0.2, y + s * 0.15), (x + s * 0.8, y + s * 0.15), (x + s * 0.8, y + s * 0.55),
                   (x + s * 0.5, y + s * 0.9), (x + s * 0.2, y + s * 0.55)], outline=c, width=2)
        d.line([x + s * 0.5, y + s * 0.3, x + s * 0.5, y + s * 0.6], fill=RED, width=2)
    elif kind == "atom":
        d.ellipse([x + s * 0.42, y + s * 0.42, x + s * 0.58, y + s * 0.58], fill=RED)
        for ang in (0, 60, 120):
            d.ellipse([x + s * 0.1, y + s * 0.3, x + s * 0.9, y + s * 0.7], outline=c, width=1)
        d.arc([x + s * 0.1, y + s * 0.25, x + s * 0.9, y + s * 0.75], 0, 360, fill=c, width=1)
    elif kind == "ball":
        d.ellipse([x + s * 0.15, y + s * 0.15, x + s * 0.85, y + s * 0.85], outline=c, width=2)
        d.line([x + s * 0.15, y + s * 0.5, x + s * 0.85, y + s * 0.5], fill=c, width=1)
        d.arc([x + s * 0.05, y + s * 0.2, x + s * 0.6, y + s * 0.8], 270, 90, fill=c, width=1)
    elif kind == "leaf":
        d.pieslice([x + s * 0.15, y + s * 0.15, x + s * 0.85, y + s * 0.85], 90, 270, fill=TEAL)
        d.line([x + s * 0.5, y + s * 0.2, x + s * 0.5, y + s * 0.85], fill=PAPER, width=1)
    elif kind == "scales":
        d.line([x + s * 0.5, y + s * 0.15, x + s * 0.5, y + s * 0.85], fill=c, width=2)
        d.line([x + s * 0.15, y + s * 0.3, x + s * 0.85, y + s * 0.3], fill=c, width=2)
        d.pieslice([x + s * 0.05, y + s * 0.35, x + s * 0.35, y + s * 0.6], 0, 180, fill=c)
        d.pieslice([x + s * 0.65, y + s * 0.35, x + s * 0.95, y + s * 0.6], 0, 180, fill=c)
    elif kind == "chip":
        d.rectangle([x + s * 0.25, y + s * 0.25, x + s * 0.75, y + s * 0.75], outline=c, width=2)
        for t in (0.35, 0.5, 0.65):
            d.line([x + s * t, y + s * 0.1, x + s * t, y + s * 0.25], fill=c, width=1)
            d.line([x + s * t, y + s * 0.75, x + s * t, y + s * 0.9], fill=c, width=1)
    elif kind == "flag":
        d.line([x + s * 0.25, y + s * 0.1, x + s * 0.25, y + s * 0.9], fill=c, width=2)
        d.polygon([(x + s * 0.25, y + s * 0.12), (x + s * 0.85, y + s * 0.25), (x + s * 0.25, y + s * 0.45)], fill=RED)


# ------------------------------------------------------------------- page build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # faint paper fibre (deterministic)
    for i in range(0, W, 7):
        d.line([i, 0, i + 40, H], fill=(243, 239, 227), width=1)

    # ---- masthead
    rule(d, M, 16, CW, INK, 2)
    t = "The World Today"
    f = masthead_font(60)
    mx = W / 2 - tw(d, t, f) / 2
    d.text((mx, 12), t, font=f, fill=INK)
    assert d.textbbox((mx, 12), t, font=f)[3] <= 90, "masthead descender hits double rule"
    d.text((M, 40), "SPECIAL EDITION", font=kicker(11), fill=RED)
    rt = "ONE IMAGE · 22 STORIES"
    d.text((W - M - tw(d, rt, kicker(11)), 40), rt, font=kicker(11), fill=RED)
    rule(d, M, 92, CW, INK, 1)
    rule(d, M, 95, CW, INK, 3)
    date = "THURSDAY, 19 NOVEMBER 2026"
    fd = head(24)
    d.text((W / 2 - tw(d, date, fd) / 2, 102), date, font=fd, fill=INK)
    d.text((M, 108), "WORLD NEWS · ONE DAY", font=mono(11), fill=FAINT)
    rt2 = "APEC · IPO · ICJ · GTA VI"
    d.text((W - M - tw(d, rt2, mono(11)), 108), rt2, font=mono(11), fill=FAINT)
    rule(d, M, 132, CW, INK, 1)

    # ---- hero: Shenzhen (left) / Berlin (right)
    hy = 142
    lw = 596
    rx = M + lw + 24
    rw = CW - lw - 24
    y = kick(d, M, hy, "APEC · Shenzhen · first-ever trilateral")
    il_summit(d, M, y, lw, 140)
    y += 146
    y = headline(d, M, y, "TRUMP, XI & PUTIN ISSUE 'PEACE DECLARATION' AT FIRST THREE-WAY SUMMIT", 26, lw)
    y += 4
    y = para(d, M, y, "In 80 minutes at Kylin Villa: nuclear war 'cannot be won and must never be "
             "fought'; more refined-oil supply; UN reform; a curb on the ICC. No Ukraine "
             "breakthrough. Trump calls Putin 'my friend'.", body(14), lw)
    vrule(d, M + lw + 11, hy, 278)
    y2 = kick(d, rx, hy, "Berlin · the same day", BLUE)
    il_berlin(d, rx, y2, rw, 100)
    y2 += 106
    y2 = headline(d, rx, y2, "EUROPE COUNTERS: 30+ LEADERS MEET ZELENSKY IN BERLIN", 19, rw)
    y2 += 3
    y2 = para(d, rx, y2, "'Coalition of the Willing' hosts US envoys Witkoff & Kushner: air defence, "
              "energy aid, and Europe's seat at any peace deal.", body(13), rw)
    y2 += 2
    d.text((rx, y2), "Tusk, on the 'friendship':", font=ital(12), fill=FAINT)
    y2 += 16
    d.text((rx, y2), "“God, protect us from such friends.”", font=bodyb(13), fill=RED)
    rule(d, M, 428, CW, INK, 1)

    # ---- row 2: business / justice / culture
    ry = 436
    colw = (CW - 48) // 3
    xs = [M, M + colw + 24, M + 2 * (colw + 24)]
    for x in xs[1:]:
        vrule(d, x - 13, ry, 214)

    # business
    x = xs[0]
    y = kick(d, x, ry, "Business · Wall Street")
    il_ipo(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "RECORD $81B ANTHROPIC IPO: +34% OPEN, THEN A SELLOFF", 18, colw)
    y += 3
    y = para(d, x, y, "ANT opens $111.50 vs $83 priced — the largest IPO ever, ~$1.5T. Gains pare "
             "to +17% as stocks sink at the debut. Walmart beats and raises its outlook.",
             body(13), colw)
    chip(d, x, y + 2, "DOW −2.2%", bg=RED, size=11)
    chip(d, x + 92, y + 2, "S&P −2.0%", bg=RED, size=11)
    chip(d, x + 184, y + 2, "ANT +17%", bg=GREEN, size=11)

    # justice
    x = xs[1]
    y = kick(d, x, ry, "Justice · The Hague", BLUE)
    il_icj(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "ICJ: MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA", 18, colw)
    y += 3
    jt = ("9–6: the 2017 crackdown killed ~10,000, drove 730,000 into Bangladesh. "
          "The Gambia's case: first state held responsible under the 1948 convention.")
    ye = para(d, x, y, jt, body(13), colw)
    assert ye - 17 + d.textbbox((0, 0), wrap(d, jt, body(13), colw)[-1], font=body(13))[3] <= 654, "justice body hits row rule"

    # culture
    x = xs[2]
    y = kick(d, x, ry, "Culture · gaming", (150, 40, 110))
    il_gta(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "GTA VI IS OUT: $1B+ PRE-ORDERS, VICE CITY AWAITS", 18, colw)
    y += 3
    y = para(d, x, y, "Lucia & Jason arrive on PS5/Xbox after 13 years. Take-Two guides $3.35–3.5B "
             "this quarter; 'GTA flu' leave requests ran 13% high.", body(13), colw)
    rule(d, M, 656, CW, INK, 1)

    # ---- row 3: weather / mideast / americas
    ry = 664
    for x in xs[1:]:
        vrule(d, x - 13, ry, 200)

    x = xs[0]
    y = kick(d, x, ry, "Weather · Bay of Bengal", BLUE)
    il_cyclone(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "AKVAN 'VERY SEVERE': LANDFALL FORECAST FRIDAY NOON", 18, colw)
    y += 3
    y = para(d, x, y, "120–130 km/h gusting 145; waves over 14 m; rain over 21 cm. Andhra–Yanam "
             "coast, Nellore to Visakhapatnam. Red alerts; evacuations under way.", body(13), colw)

    x = xs[1]
    y = kick(d, x, ry, "Middle East · Gaza")
    il_gaza(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "ISRAEL HOLDS TWO-THIRDS OF GAZA AFTER LINE PUSH", 18, colw)
    y += 3
    y = para(d, x, y, "Tanks cross the ceasefire 'Yellow Line'; thousands flee again. 1,600+ killed "
             "since October's truce. Dr Abu Safiya's detention extended 6 months.", body(13), colw)

    x = xs[2]
    y = kick(d, x, ry, "Americas · Caracas", TEAL)
    il_venezuela(d, x, y, colw, 72)
    y += 78
    y = headline(d, x, y, "US–VENEZUELA MILITARY TIES RESTORED, WITH OIL DEAL", 18, colw)
    y += 3
    y = para(d, x, y, "Hegseth in Caracas: training, intel sharing, border security — first since "
             "Maduro's seizure. Colombia rebuffs joint anti-cartel operations.", body(13), colw)
    rule(d, M, 872, CW, INK, 1)

    # ---- briefs: 8 in 4 x 2
    by = 880
    d.text((M, by), "ALSO TODAY", font=kicker(13), fill=INK)
    rule(d, M + 104, by + 7, CW - 104, (180, 174, 158), 1)
    briefs = [
        ("bridge", "UKRAINE", "Crimean Bridge struck a 3rd time this week, Russia says; rail halted."),
        ("ice", "ARCTIC", "Denmark approves a Greenland–US deal: more American bases."),
        ("gavel", "SOUTH KOREA", "Court overturns ex-PM Han's martial-law conviction."),
        ("tower", "IRAN WAR", "Houthi missile hits Riyadh's PIF Tower; Trump weighs a strike."),
        ("capitol", "US POLITICS", "Jeffries nominated speaker, 251–11 — a first Black speaker."),
        ("shield", "CYBER", "CISA: patch Java now — a no-password server-takeover flaw."),
        ("atom", "NORTH KOREA", "IAEA: Yongbyon enrichment site expanding, Grossi says."),
        ("ball", "NBA", "Giannis' Bucks return: 27-14-9, but the Heat win 137–130."),
    ]
    bw = (CW - 3 * 18) // 4
    brief_bottom = 0
    for i, (ic, reg, txt) in enumerate(briefs):
        r, c = divmod(i, 4)
        bx = M + c * (bw + 18)
        byy = by + 20 + r * 40
        icon(d, ic, bx, byy + 2, 16)
        d.text((bx + 22, byy), reg, font=kicker(9), fill=RED)
        ye = para(d, bx + 22, byy + 12, txt, body(11), bw - 22, leading=12)
        last = wrap(d, txt, body(11), bw - 22)[-1]
        brief_bottom = max(brief_bottom, ye - 12 + d.textbbox((0, 0), last, font=body(11))[3])
    # self-check: the closing rule must clear the briefs' descenders
    assert brief_bottom + 2 <= 982, f"briefs collide with footer rule: bottom={brief_bottom}"
    rule(d, M, 982, CW, INK, 1)

    # ---- footer ticker
    tick = "COP31 UNDERWAY IN ANTALYA  ·  RIO TINTO: $250M FOR BOUGAINVILLE MINE LEGACY  ·  HAITI: SANON GUILTY IN MOÏSE PLOT  ·  JAPAN: TAKAICHI–PUTIN TALKS"
    tick2 = "NIKE: AIR FORCE 1s FOR EVERY US VALEDICTORIAN  ·  MUSK CALLS HIS $446M MAGA SPENDING 'FOOLISH'"
    cr = "Drawn by an AI agent · sources: BBC, AP, Reuters, DW, CNBC, IMD, Democracy Now"
    assert tw(d, tick, mono(10)) <= CW and tw(d, tick2, mono(10)) <= CW, "ticker runs off page"
    assert W - M - tw(d, cr, mono(9)) >= M, "credit runs off page"
    assert 1012 + d.textbbox((0, 0), cr, font=mono(9))[3] <= H, "credit clipped at bottom"
    d.text((M, 988), tick, font=mono(10), fill=FAINT)
    d.text((M, 1001), tick2, font=mono(10), fill=FAINT)
    d.text((W - M - tw(d, cr, mono(9)), 1012), cr, font=mono(9), fill=(160, 154, 140))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
