#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page as a PNG.

Every story on the page comes from the 20 November research slate:
the Shenzhen trilateral talks, the ICJ Rohingya ruling, the Anthropic
IPO, the third Kerch Bridge strike, the Riyadh PIF tower attack, and
the market / climate / cyclone strip. Only Pillow is used, and the
page is drawn from flat shapes and text, so the words stay sharp.
The output is a 1024x1024 PNG under the 1 MiB limit.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 30
OUT_PATH = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"

NAVY = "#0f2a44"
INK = "#121820"
MUTED = "#54606e"
PAPER = "#f8f9fb"
CARD_BG = "#ffffff"
PALE = "#eaf1f8"
GOLD = "#ffd65a"
CRIMSON = "#b22222"
AZURE = "#185aa0"
TEAL = "#0e7a6e"
VIOLET = "#5e3a8c"
OCHRE = "#b07008"
EDGE = "#c8d2dc"


def load_font(bold, size, serif=False):
    path = SERIF_BOLD if serif else (SANS_BOLD if bold else SANS)
    return ImageFont.truetype(path, size)


def wrap_text(canvas, text, font, width):
    """Split text into lines that fit width, measured with the font."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if canvas.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(canvas, x, y, text, size, colour, width, gap, bold=False):
    """Draw a wrapped paragraph; return the y below its last line."""
    face = load_font(bold, size)
    for line in wrap_text(canvas, text, face, width):
        canvas.text((x, y), line, font=face, fill=colour)
        y += gap
    return y


def section_label(canvas, x, y, text, colour):
    canvas.text((x, y), text, font=load_font(True, 20), fill=colour)
    return y + 28


def story_title(canvas, x, y, text, width, size=24, gap=29):
    face = load_font(True, size)
    for line in wrap_text(canvas, text, face, width):
        canvas.text((x, y), line, font=face, fill=INK)
        y += gap
    return y


def flag_chip(canvas, x, y, kind, name):
    """Flat flag swatch, 130x44, with the country name beside it."""
    w, h = 130, 44
    if kind == "china":
        canvas.rectangle([x, y, x + w, y + h], fill="#de2910")
        canvas.text((x + 16, y + h // 2 - 8), "*",
                    font=load_font(True, 26), fill=GOLD)
    elif kind == "usa":
        canvas.rectangle([x, y, x + w, y + h], fill=NAVY)
        canvas.rectangle([x, y, x + w, y + 10], fill=CRIMSON)
        canvas.rectangle([x, y + h - 10, x + w, y + h], fill=CRIMSON)
    else:
        for i, shade in enumerate(("#ffffff", "#0039a6", "#d50032")):
            canvas.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3],
                             fill=shade)
        canvas.rectangle([x, y, x + w, y + h], outline="#96a0aa", width=2)
    canvas.text((x + w + 14, y + h // 2 - 13), name,
                font=load_font(True, 22), fill=INK)


def masthead(canvas):
    canvas.rectangle([0, 0, PAGE, 158], fill=NAVY)
    canvas.text((MARGIN, 16), "THE WORLD IN ONE DAY  •  WORLD NEWS",
                font=load_font(True, 22), fill=GOLD)
    canvas.text((MARGIN, 48), "FRIDAY 20 NOVEMBER 2026",
                font=load_font(True, 46, serif=True), fill="#ffffff")
    canvas.text((MARGIN, 108), "One day. Seven stories. The world, in a single picture.",
                font=load_font(False, 24), fill="#cddceb")
    canvas.rectangle([0, 158, PAGE, 164], fill=GOLD)


def hero(canvas):
    top, bottom = 176, 424
    canvas.rectangle([MARGIN, top, PAGE - MARGIN, bottom],
                     fill=CARD_BG, outline=EDGE, width=2)
    canvas.rectangle([MARGIN, top, PAGE - MARGIN, top + 6], fill=CRIMSON)
    x, y = MARGIN + 22, top + 18
    y = section_label(canvas, x, y, "DIPLOMACY  •  APEC, SHENZHEN, CHINA", CRIMSON)
    y = story_title(canvas, x, y + 2,
                    "TRUMP, XI AND PUTIN HOLD FIRST THREE-WAY TALKS",
                    560, size=32, gap=36)
    y = text_block(canvas, x, y + 8,
                   "A four-point Declaration toward Peace: UN reform, energy, "
                   "immunity and nuclear-risk dialogue.",
                   22, INK, 600, 27)
    text_block(canvas, x, y + 6,
               "Zelensky: no deal without Kyiv. 40 partners pledge "
               "air-defence and energy aid.",
               22, INK, 600, 27)
    fx, fy = 668, top + 52
    for kind, name in (("china", "CHINA"), ("usa", "USA"), ("russia", "RUSSIA")):
        flag_chip(canvas, fx, fy, kind, name)
        fy += 54


def grid(canvas):
    top = 436
    cell_w, cell_h, gap = 474, 186, 16
    stories = [
        ("JUSTICE  •  THE HAGUE", CRIMSON,
         "ICJ: MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA",
         "The court rules 9-6 on the 2017 crackdown in northern "
         "Rakhine. A landmark verdict for the Rohingya."),
        ("TECHNOLOGY  •  MARKETS", TEAL,
         "ANTHROPIC GOES PUBLIC: SHARES JUMP 17% ON DEBUT",
         "The first frontier AI company to list, on Nasdaq as ANT. "
         "Shares open at $111.50 after an $81.3bn IPO."),
        ("UKRAINE  •  EUROPE", AZURE,
         "KERCH BRIDGE HIT FOR A THIRD TIME",
         "Neptune missiles strike the Crimean Bridge again, briefly "
         "halting trains. Putin vows a far more painful response."),
        ("MIDDLE EAST  •  THE GULF", VIOLET,
         "HOUTHI STRIKE DAMAGES RIYADH'S PIF TOWER",
         "The 80-storey tower's windows are blown out; no injuries. "
         "Strikes claimed on four Saudi targets; Senate rejects "
         "war powers, 51-48."),
    ]
    for i, (label, colour, title, body) in enumerate(stories):
        cx = MARGIN + (i % 2) * (cell_w + gap)
        cy = top + (i // 2) * (cell_h + gap)
        canvas.rectangle([cx, cy, cx + cell_w, cy + cell_h],
                         fill=CARD_BG, outline=EDGE, width=2)
        canvas.rectangle([cx, cy, cx + cell_w, cy + 6], fill=colour)
        tx, ty = cx + 18, cy + 16
        ty = section_label(canvas, tx, ty, label, colour)
        ty = story_title(canvas, tx, ty + 2, title, cell_w - 36)
        text_block(canvas, tx, ty + 8, body, 18, INK, cell_w - 36, 24)


def strip(canvas):
    top, bottom = 840, 960
    canvas.rectangle([MARGIN, top, PAGE - MARGIN, bottom],
                     fill=PALE, outline=EDGE, width=2)
    items = [
        ("MARKETS  •  DOW 49,097", CRIMSON,
         "Dow falls below 50,000 in an AI selloff; S&P -2.02%, Nasdaq -2.25%."),
        ("CLIMATE  •  COP31", TEAL,
         "Draft drops calls to phase out fossil fuels as talks continue."),
        ("WEATHER  •  AKVAN", OCHRE,
         "Storm nears India's east coast; Andhra and Odisha landfall due, trains cancelled."),
    ]
    col_w = (PAGE - 2 * MARGIN - 2 * 18) // 3
    for i, (label, colour, body) in enumerate(items):
        sx = MARGIN + 18 + i * (col_w + 18)
        if i:
            canvas.line([(sx - 9, top + 14), (sx - 9, bottom - 14)],
                        fill=EDGE, width=2)
        canvas.text((sx, top + 12), label, font=load_font(True, 19), fill=colour)
        text_block(canvas, sx, top + 42, body, 18, INK, col_w - 12, 23)


def footer(canvas):
    canvas.text((MARGIN, 976),
                "All events reported on Friday 20 November 2026  •  AP, Reuters, IMD",
                font=load_font(False, 18), fill=MUTED)
    canvas.text((PAGE - MARGIN - 118, 976), "20 NOV 2026",
                font=load_font(True, 18), fill=NAVY)


def main():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    canvas = ImageDraw.Draw(page)
    masthead(canvas)
    hero(canvas)
    grid(canvas)
    strip(canvas)
    footer(canvas)
    page.save(OUT_PATH, "PNG", optimize=True)
    print(f"saved {OUT_PATH}: {page.size}")


if __name__ == "__main__":
    main()
