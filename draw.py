#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news image.

A clean newspaper front page, drawn with Pillow only: no photos, no
AI-generated faces, so every word stays crisp and legible.
Output: 1024x1024 PNG, well under the 1 MiB limit.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (15, 42, 68)
INK = (18, 24, 32)
GREY = (84, 96, 110)
LIGHT = (234, 241, 248)
CARD = (255, 255, 255)
RED = (178, 34, 34)
BLUE = (24, 90, 160)
TEAL = (14, 122, 110)
PURPLE = (94, 58, 140)
AMBER = (176, 112, 8)
RULE = (200, 210, 220)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured width."""
    words, lines, cur = text.split(), [], ""
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


def para(draw, x, y, text, fnt, color, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text, color):
    f = font(SANS_B, 20)
    draw.text((x, y), text, font=f, fill=color)
    return y + 28


def headline(draw, x, y, text, max_w, size=28, leading=34):
    f = font(SANS_B, size)
    for line in wrap(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=INK)
        y += leading
    return y


def flag(d, x, y, w, h, kind, label):
    """A flat flag swatch with its country name beside it in bold."""
    if kind == "china":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        d.text((x + 16, y + h // 2 - 8), "*", font=font(SANS_B, 26),
               fill=(255, 214, 90))
    elif kind == "usa":
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(178, 34, 34))
        d.rectangle([x, y, x + w, y + 10], fill=(178, 34, 34))
    else:  # russia
        for i, c in enumerate(((255, 255, 255), (0, 57, 166), (213, 0, 50))):
            d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=c)
        d.rectangle([x, y, x + w, y + h], outline=(150, 160, 170), width=2)
    d.text((x + w + 14, y + h // 2 - 13), label, font=font(SANS_B, 22), fill=INK)


def main():
    img = Image.new("RGB", (W, H), (248, 249, 251))
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 158], fill=NAVY)
    d.text((M, 16), "THE WORLD IN ONE DAY  •  WORLD NEWS",
           font=font(SANS_B, 22), fill=(255, 214, 90))
    d.text((M, 48), "FRIDAY 20 NOVEMBER 2026",
           font=font(SERIF, 46), fill=(255, 255, 255))
    d.text((M, 108), "One day. Seven stories. The world, in a single picture.",
           font=font(SANS, 24), fill=(205, 220, 235))
    d.rectangle([0, 158, W, 164], fill=(255, 214, 90))

    # ---------- hero: the Shenzhen trilateral talks ----------
    y0, y1 = 176, 424
    d.rectangle([M, y0, W - M, y1], fill=CARD, outline=RULE, width=2)
    d.rectangle([M, y0, W - M, y0 + 6], fill=RED)
    hx, hy = M + 22, y0 + 18
    hy = kicker(d, hx, hy, "DIPLOMACY  •  APEC, SHENZHEN, CHINA", RED)
    hy = headline(d, hx, hy + 2, "TRUMP, XI AND PUTIN HOLD FIRST THREE-WAY TALKS",
                  max_w=560, size=32, leading=36)
    hy = para(d, hx, hy + 8,
              "A four-point Declaration toward Peace: UN reform, energy, "
              "immunity and nuclear-risk dialogue.",
              font(SANS, 22), INK, 600, 27)
    hy = para(d, hx, hy + 6,
              "Zelensky: no deal without Kyiv. 40 partners pledge "
              "air-defence and energy aid.",
              font(SANS, 22), INK, 600, 27)
    # flags on the right, with the country name beside each swatch
    fx, fy = 668, y0 + 52
    for kind, label in (("china", "CHINA"), ("usa", "USA"), ("russia", "RUSSIA")):
        flag(d, fx, fy, 130, 44, kind, label)
        fy += 54

    # ---------- 2 x 2 grid ----------
    gy0 = 436
    cw, ch, gap = 474, 186, 16
    cells = [
        ("JUSTICE  •  THE HAGUE", RED,
         "ICJ: MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA",
         "The court rules 9-6 on the 2017 crackdown in northern "
         "Rakhine. A landmark verdict for the Rohingya."),
        ("TECHNOLOGY  •  MARKETS", TEAL,
         "ANTHROPIC GOES PUBLIC: SHARES JUMP 17% ON DEBUT",
         "The first frontier AI company to list, on Nasdaq as ANT. "
         "Shares open at $111.50 after an $81.3bn IPO."),
        ("UKRAINE  •  EUROPE", BLUE,
         "KERCH BRIDGE HIT FOR A THIRD TIME",
         "Neptune missiles strike the Crimean Bridge again, briefly "
         "halting trains. Putin vows a far more painful response."),
        ("MIDDLE EAST  •  THE GULF", PURPLE,
         "HOUTHI STRIKE DAMAGES RIYADH'S PIF TOWER",
         "The 80-storey tower's windows are blown out; no injuries. "
         "Strikes claimed on four Saudi targets; Senate rejects "
         "war powers, 51-48."),
    ]
    for i, (kick, color, head, body) in enumerate(cells):
        cx = M + (i % 2) * (cw + gap)
        cy = gy0 + (i // 2) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=RULE, width=2)
        d.rectangle([cx, cy, cx + cw, cy + 6], fill=color)
        tx, ty = cx + 18, cy + 16
        ty = kicker(d, tx, ty, kick, color)
        ty = headline(d, tx, ty + 2, head, max_w=cw - 36, size=24, leading=29)
        para(d, tx, ty + 8, body, font(SANS, 18), INK, cw - 36, 24)

    # ---------- bottom strip: markets, climate, weather ----------
    by0, by1 = 840, 960
    d.rectangle([M, by0, W - M, by1], fill=LIGHT, outline=RULE, width=2)
    strips = [
        ("MARKETS  •  DOW 49,097", RED,
         "Dow falls below 50,000 in an AI selloff; S&P -2.02%, Nasdaq -2.25%."),
        ("CLIMATE  •  COP31", TEAL,
         "Draft drops calls to phase out fossil fuels as talks continue."),
        ("WEATHER  •  AKVAN", AMBER,
         "Storm nears India's east coast; Andhra and Odisha landfall due, trains cancelled."),
    ]
    sw = (W - 2 * M - 2 * 18) // 3
    for i, (kick, color, body) in enumerate(strips):
        sx = M + 18 + i * (sw + 18)
        if i:
            d.line([(sx - 9, by0 + 14), (sx - 9, by1 - 14)], fill=RULE, width=2)
        d.text((sx, by0 + 12), kick, font=font(SANS_B, 19), fill=color)
        para(d, sx, by0 + 42, body, font(SANS, 18), INK, sw - 12, 23)

    # ---------- footer ----------
    d.text((M, 976), "All events reported on Friday 20 November 2026  •  AP, Reuters, IMD",
           font=font(SANS, 18), fill=GREY)
    d.text((W - M - 118, 976), "20 NOV 2026", font=font(SANS_B, 18), fill=NAVY)

    img.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT}: {img.size}")


if __name__ == "__main__":
    main()
