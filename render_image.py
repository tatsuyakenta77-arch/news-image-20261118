#!/usr/bin/env python3
"""Render the news-image-20261118 entry: a one-page newspaper front page
summing up world news of Wednesday 18 November 2026.

Run:  python3 render_image.py [out.png]
Output: 1024x1024 PNG, well under the 1 MiB gate limit.
Everything is drawn with Pillow from the facts researched on 18 Nov 2026
(see SOURCES in the README). No network, no external images.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (11, 31, 58)
NAVY2 = (18, 48, 88)
RED = (178, 34, 34)
GOLD = (232, 184, 75)
GREY = (90, 90, 86)
RULE = (200, 192, 175)
CARD = (255, 255, 255)
TINTS = {
    "red": (246, 226, 222),
    "navy": (222, 231, 242),
    "gold": (247, 236, 205),
    "green": (226, 240, 226),
    "purple": (236, 226, 242),
    "teal": (220, 240, 238),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def draw_icon(draw, kind, cx, cy, r, color):
    """Small abstract pictogram, centred at (cx, cy), radius r."""
    if kind == "strike":  # explosion burst over the strait
        for a in range(0, 360, 30):
            x2 = cx + r * 1.0 * math.cos(math.radians(a))
            y2 = cy + r * 1.0 * math.sin(math.radians(a))
            draw.line([(cx, cy), (x2, y2)], fill=color, width=4)
        draw.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
                     fill=(226, 84, 44))
        draw.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3],
                     fill=(255, 255, 255))
    elif kind == "bridge":  # arch bridge, one span dropped
        draw.arc([cx - r, cy - r * 0.4, cx + r, cy + r * 1.2], 180, 360,
                 fill=color, width=6)
        draw.line([(cx - r, cy + r * 0.4), (cx + r, cy + r * 0.4)],
                  fill=color, width=6)
        draw.line([(cx - r * 0.7, cy + r * 0.4), (cx - r * 0.7, cy - r * 0.1)],
                  fill=color, width=4)
        draw.line([(cx + r * 0.7, cy + r * 0.4), (cx + r * 0.7, cy - r * 0.1)],
                  fill=color, width=4)
        draw.line([(cx + r * 0.1, cy + r * 0.4), (cx + r * 0.45, cy + r * 0.9)],
                  fill=RED, width=5)
    elif kind == "summit":  # three leaders / globe
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
        draw.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 360,
                 fill=color, width=3)
        draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=3)
        for dx, c in ((-r * 0.55, RED), (0, GOLD), (r * 0.55, NAVY2)):
            draw.ellipse([cx + dx - 7, cy - r - 14, cx + dx + 7, cy - r],
                         fill=c)
    elif kind == "chip":
        draw.rectangle([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6],
                       outline=color, width=6)
        draw.rectangle([cx - r * 0.25, cy - r * 0.25, cx + r * 0.25, cy + r * 0.25],
                       fill=color)
        for i in (-1, 0, 1):
            draw.line([(cx + i * r * 0.4, cy - r * 0.6),
                       (cx + i * r * 0.4, cy - r * 0.95)], fill=color, width=4)
            draw.line([(cx + i * r * 0.4, cy + r * 0.6),
                       (cx + i * r * 0.4, cy + r * 0.95)], fill=color, width=4)
            draw.line([(cx - r * 0.6, cy + i * r * 0.4),
                       (cx - r * 0.95, cy + i * r * 0.4)], fill=color, width=4)
            draw.line([(cx + r * 0.6, cy + i * r * 0.4),
                       (cx + r * 0.95, cy + i * r * 0.4)], fill=color, width=4)
    elif kind == "virus":
        draw.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
                     fill=color)
        for a in range(0, 360, 30):
            x1 = cx + r * 0.55 * math.cos(math.radians(a))
            y1 = cy + r * 0.55 * math.sin(math.radians(a))
            x2 = cx + r * 0.95 * math.cos(math.radians(a))
            y2 = cy + r * 0.95 * math.sin(math.radians(a))
            draw.line([(x1, y1), (x2, y2)], fill=color, width=4)
            draw.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=color)
    elif kind == "cyclone":
        for k in range(3):
            r0 = r * (0.25 + 0.25 * k)
            draw.arc([cx - r0, cy - r0, cx + r0, cy + r0],
                     20 + 40 * k, 300 + 40 * k, fill=color, width=5)
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)
    elif kind == "ebola":
        draw.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7],
                     outline=color, width=6)
        draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=4)
        for dx in (-r * 0.5, 0, r * 0.5):
            draw.ellipse([cx + dx - 5, cy - r * 0.45, cx + dx + 5, cy - r * 0.45 + 10],
                         fill=color)
            draw.ellipse([cx + dx - 5, cy + r * 0.45 - 10, cx + dx + 5, cy + r * 0.45],
                         fill=color)


def card(draw, x, y, w, h, kicker, kcolor, headline, body, icon, tint,
         hsize=26, bsize=18):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=kcolor)
    pad = 16
    ix = x + pad + 34
    iy = y + 52
    draw.ellipse([x + pad, y + 18, x + pad + 68, y + 86], fill=tint)
    draw_icon(draw, icon, ix, iy, 24, kcolor)
    tx = x + pad + 84
    tw = w - pad - 84 - pad
    draw.text((tx, y + 14), kicker, font=font(SANS_B, 17), fill=kcolor)
    hl = wrap(draw, headline, font(SERIF, hsize), tw)
    yy = draw_lines(draw, hl, tx, y + 38, font(SERIF, hsize), INK, hsize + 5)
    bl = wrap(draw, body, font(SANS, bsize), tw)
    draw_lines(draw, bl, tx, yy + 4, font(SANS, bsize), (60, 60, 58), bsize + 4)
    return y + h


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.text((28, 14), "THE WORLD  ·  IN ONE IMAGE",
           font=font(SANS_B, 21), fill=GOLD)
    d.text((28, 40), "WORLD NEWS", font=font(SERIF, 62), fill=(255, 255, 255))
    d.text((700, 52), "ONE DAY — ONE IMAGE", font=font(SANS_B, 20), fill=(180, 195, 215))
    d.text((700, 82), "THE DAY IN ONE PAGE", font=font(SANS, 18), fill=(180, 195, 215))
    d.text((28, 108), "WEDNESDAY,  18  NOVEMBER  2026",
           font=font(SANS_B, 33), fill=GOLD)
    d.rectangle([0, 150, W, 158], fill=RED)

    # ---- Lead story: the Gulf ----
    lx, ly, lw, lh = 28, 174, 968, 224
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=RULE, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 6], fill=RED)
    d.text((lx + 20, ly + 16), "LEAD STORY  —  THE GULF IN FLAMES",
           font=font(SANS_B, 20), fill=RED)
    hl = wrap(d, "U.S. Jets Strike Iran as Gulf Tankers Burn",
              font(SERIF, 44), 660)
    yy = draw_lines(d, hl, lx + 20, ly + 44, font(SERIF, 44), INK, 50)
    body = ("American jets hit a Revolutionary Guard missile site on Qeshm "
            "Island after Iran fired drones at U.S. bases in Bahrain and "
            "Kuwait. Tankers burn in the Strait of Hormuz.")
    bl = wrap(d, body, font(SANS, 20), 660)
    draw_lines(d, bl, lx + 20, yy + 6, font(SANS, 20), (60, 60, 58), 26)
    # icon panel
    ix0, iy0 = lx + 700, ly + 18
    d.rectangle([ix0, iy0, lx + lw - 18, ly + lh - 18], fill=NAVY2)
    draw_icon(d, "strike", ix0 + 125, iy0 + 82, 52, GOLD)
    d.text((ix0 + 18, iy0 + 148), "QESHM ISLAND  ·  HORMUZ",
           font=font(SANS_B, 15), fill=(255, 255, 255))

    # ---- Grid: 4 stories, 2 x 2 ----
    gx, gy = 28, 412
    cw, ch, gap = 476, 176, 16
    stories = [
        ("UKRAINE  ·  WAR", NAVY2, "Kerch Bridge Falls — Again",
         "Ukraine hit the Crimea bridge for a second day; part of its road "
         "span dropped into the strait.", "bridge", TINTS["navy"]),
        ("CHINA  ·  APEC SUMMIT", RED, "Xi, Putin and Trump Meet in Shenzhen",
         "Xi opens the APEC summit and urges free trade and AI cooperation "
         "as the three leaders gather.", "summit", TINTS["red"]),
        ("MARKETS  ·  TECH", (23, 110, 60), "Nvidia Doubles Its Revenue",
         "$115.8bn in a quarter, up 103%. The board rules out bringing "
         "back founder Jensen Huang as CEO.", "chip", TINTS["green"]),
        ("HEALTH  ·  USA", (110, 45, 130), "America Loses Its Measles-Free Status",
         "5,400 cases in 2026 end 26 years of elimination. Health chiefs "
         "warn the virus is back.", "virus", TINTS["purple"]),
    ]
    for i, (kick, kc, head, body, icon, tint) in enumerate(stories):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        card(d, cx, cy, cw, ch, kick, kc, head, body, icon, tint)

    # ---- Second row: Ebola + Cyclone ----
    ry = gy + 2 * ch + gap + 14  # 794
    card(d, gx, ry, cw, 146, "HEALTH  ·  AFRICA", (140, 60, 20),
         "Ebola in DR Congo More Than Doubles",
         "Over 11,000 cases and 5,400 deaths in three months; children "
         "hardest hit.", "ebola", TINTS["gold"], hsize=24, bsize=17)
    card(d, gx + cw + gap, ry, cw, 146, "WEATHER  ·  INDIA", (0, 110, 110),
         "Cyclone Akvan Bears Down on Andhra",
         "Landfall expected Friday near Nellore as the storm strengthens.",
         "cyclone", TINTS["teal"], hsize=24, bsize=17)

    # ---- Ticker ----
    ty = ry + 146 + 10  # 950
    d.rectangle([0, ty, W, H], fill=NAVY)
    d.text((28, ty + 10), "ALSO TODAY",
           font=font(SANS_B, 19), fill=GOLD)
    tick = ("Peltola flips Alaska — Democrats 56   •   Siberia crash "
            "kills 19   •   146,000 march in France")
    tl = wrap(d, tick, font(SANS, 17), 968 - 170)
    draw_lines(d, tl, 28 + 150, ty + 14, font(SANS, 17),
               (235, 235, 235), 23)
    d.text((28, H - 22), "Sources: wire reports of 18 November 2026  ·  Wednesday 18 November 2026",
           font=font(SANS, 13), fill=(150, 165, 185))

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {img.size}")
    import os
    print("bytes:", os.path.getsize(out))


if __name__ == "__main__":
    main()
