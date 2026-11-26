#!/usr/bin/env python3
"""Render a 1024x1024 front-page newspaper image for 26 November 2026.

Usage:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Writes entry.png into $MAKEFUN_OUTPUT_DIR (default /output). The drawing is
fully deterministic: fixed palette, fixed fonts, fixed layout, no network,
no clocks, no randomness. If Pillow, the DejaVu fonts, or hero.png is not
available, the script falls back to copying the shipped entry.png
byte-for-byte so the entry still produces a valid image.
"""

import os
import shutil
import sys

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.png")

WIDTH = 1024
HEIGHT = 1024
MARGIN = 26
CONTENT_W = WIDTH - 2 * MARGIN  # 972

PAPER = (247, 242, 231)
INK = (17, 17, 17)
MUTED = (90, 86, 76)
RED = (163, 22, 33)
LEAD_BG = (252, 250, 244)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

STORIES = [
    ("MIDDLE EAST \u00b7 ENERGY", "Tankers hit by mines in the Strait of Hormuz",
     "Iran says tankers struck naval mines; shipping fears rise."),
    ("MIDDLE EAST \u00b7 GAZA", "Israel strikes Hamas official in Gaza as truce strains",
     "The strike comes as the ceasefire frays and hardship deepens."),
    ("EUROPE \u00b7 WAR", "Ukraine hits Russian oil refineries; Putin vows reply",
     "Kyiv keeps striking Russian energy plants; Moscow vows a reply."),
    ("EUROPE \u00b7 WAR", "Russia's own figures show near 500,000 war dead",
     "Moscow's data points to near half a million lost in the war."),
    ("ASIA \u00b7 INDIA", "India marks 18 years since the 26/11 Mumbai attacks",
     "India also marks Constitution Day, 77 years after adopting it."),
    ("ASIA \u00b7 SPACE", "Pakistan's first astronaut picked for China's station",
     "Muhammad Zeeshan Ali will fly on Shenzhou-24 to Tiangong."),
    ("ASIA \u00b7 ECONOMY", "Bangladesh garment workers win 36% pay rise",
     "Entry-level garment workers' minimum wage rises by a third."),
    ("AMERICAS \u00b7 COLOMBIA", "Police free 20 hostages after 17-hour siege",
     "Officers storm a Cartagena supermarket to end the hostage siege."),
    ("ASIA \u00b7 DISASTER", "Magnitude 5.6 quake hits Nepal near China border",
     "The tremor strikes Koshi Province near the Chinese border."),
    ("SPORT \u00b7 CRICKET", "Sooryavanshi, 15, smashes fastest List A double ton",
     "The teenager hits 204 off 53 balls against the UAE, a world record."),
    ("SPORT \u00b7 CHESS", "Gukesh faces Sindarov at World Chess Championship",
     "India's champion takes on Uzbekistan's Sindarov for the world title."),
    ("ASIA-PACIFIC \u00b7 DIPLOMACY", "Solomon Islands and Australia sign security treaty",
     "The pact deepens defence ties between the Pacific neighbours."),
    ("ASIA \u00b7 KOREA", "North Korea orders Swiss office shut in Pyongyang",
     "Pyongyang tells Bern to close its newly opened diplomatic office."),
    ("AMERICAS \u00b7 TRADE", "US prepares plan for new tariffs on trade partners",
     "Washington readies fresh tariffs on global trading partners."),
    ("ASIA \u00b7 BUSINESS", "Flipkart chief to step down in December",
     "Kalyan Krishnamurthy will leave the Walmart-owned e-commerce group."),
    ("ASIA \u00b7 EDUCATION", "IITs to add 6,000 seats in robotics, AI and space",
     "India's top tech institutes expand in robotics, AI and space tech."),
]

SOURCES_LINE = ("Sources: Rigzone \u00b7 TankerBrief \u00b7 BBC \u00b7 Reuters \u00b7 AP \u00b7 "
                "JagranJosh \u00b7 Observer Voice \u00b7 SelfStudys")


def load_font(name, size):
    from PIL import ImageFont
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def fit_one_line(draw, text, font, max_width):
    """Truncate with an ellipsis so the text fits on one line."""
    if draw.textlength(text, font=font) <= max_width:
        return text
    ellipsis = "\u2026"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if draw.textlength(text[:mid] + ellipsis, font=font) <= max_width:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo].rstrip() + ellipsis


def wrap_lines(draw, text, font, max_width, max_lines):
    """Greedy word wrap, capped at max_lines (last line gets an ellipsis)."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
            if len(lines) == max_lines:
                break
    if len(lines) < max_lines and current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    if len(lines) == max_lines and draw.textlength(lines[-1], font=font) > max_width:
        lines[-1] = fit_one_line(draw, lines[-1], font, max_width)
    return lines


def render():
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    serif_bold = load_font("DejaVuSerif-Bold.ttf", 46)
    serif = load_font("DejaVuSerif.ttf", 15)
    sans_bold_20 = load_font("DejaVuSans-Bold.ttf", 20)
    sans_bold_15 = load_font("DejaVuSans-Bold.ttf", 15)
    sans_bold_13 = load_font("DejaVuSans-Bold.ttf", 13)
    sans_bold_11 = load_font("DejaVuSans-Bold.ttf", 11)
    sans_15 = load_font("DejaVuSans.ttf", 15)
    sans_13 = load_font("DejaVuSans.ttf", 13)
    serif_bold_26 = load_font("DejaVuSerif-Bold.ttf", 26)
    sans_bold_12 = load_font("DejaVuSans-Bold.ttf", 12)

    # Outer frame.
    draw.rectangle([8, 8, WIDTH - 9, HEIGHT - 9], outline=INK, width=3)

    y = 20
    # Masthead.
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=serif_bold)
    draw.text(((WIDTH - tw) / 2, y), title, font=serif_bold, fill=INK)
    y += 54
    # Thin rule under the masthead.
    draw.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=INK, width=2)
    y += 8
    # Date line.
    date_line = "Thursday, 26 November 2026"
    dw = draw.textlength(date_line, font=sans_bold_20)
    draw.text(((WIDTH - dw) / 2, y), date_line, font=sans_bold_20, fill=RED)
    y += 26
    # Daynote.
    daynote = ("Also today: 18th anniversary of the 26/11 Mumbai attacks "
               "\u00b7 Constitution Day in India")
    nw = draw.textlength(daynote, font=serif)
    draw.text(((WIDTH - nw) / 2, y), daynote, font=serif, fill=MUTED)
    y += 24

    # Hero illustration panel.
    hero = Image.open(os.path.join(REPO_DIR, "hero.png")).convert("RGB")
    if hero.size != (CONTENT_W, 300):
        hero = hero.resize((CONTENT_W, 300))
    img.paste(hero, (MARGIN, y))
    draw.rectangle([MARGIN, y, MARGIN + CONTENT_W - 1, y + 299],
                   outline=INK, width=2)
    y += 300 + 12

    # Lead box.
    lead_top = y
    lead_h = 94
    draw.rectangle([MARGIN, lead_top, WIDTH - MARGIN - 1, lead_top + lead_h - 1],
                   fill=LEAD_BG, outline=INK, width=2)
    lx = MARGIN + 14
    lw = CONTENT_W - 28
    ly = lead_top + 9
    draw.text((lx, ly), "LEAD \u00b7 MIDDLE EAST \u2014 ENERGY",
              font=sans_bold_12, fill=RED)
    ly += 17
    headline = "Houthis claim strike on Saudi Arabia's biggest refinery"
    headline = fit_one_line(draw, headline, serif_bold_26, lw)
    draw.text((lx, ly), headline, font=serif_bold_26, fill=INK)
    ly += 32
    summary = ("Riyadh says its defences downed four drones over Ras Tanura "
               "and reported no damage; the Houthis claim fires at the "
               "plant. Brent crude jumps.")
    for line in wrap_lines(draw, summary, sans_15, lw, 2):
        draw.text((lx, ly), line, font=sans_15, fill=INK)
        ly += 19
    y = lead_top + lead_h + 12

    # Story grid: 2 columns x 8 rows.
    gutter = 20
    col_w = (CONTENT_W - gutter) // 2
    grid_top = y
    grid_bottom = HEIGHT - 38  # leave room for the footer line
    row_h = (grid_bottom - grid_top) // 8
    for idx, (tag, headline, summary) in enumerate(STORIES):
        row = idx // 2
        col = idx % 2
        cx = MARGIN + col * (col_w + gutter)
        cy = grid_top + row * row_h
        # Thin divider above each row after the first, placed in the gap
        # below the previous row's summary line so it never crosses text.
        if row > 0:
            draw.line([(MARGIN, cy - 2), (WIDTH - MARGIN, cy - 2)],
                      fill=(200, 195, 182), width=1)
        ty = cy + 1
        draw.text((cx, ty), tag, font=sans_bold_11, fill=RED)
        ty += 14
        headline = fit_one_line(draw, headline, sans_bold_15, col_w)
        draw.text((cx, ty), headline, font=sans_bold_15, fill=INK)
        ty += 18
        summary = fit_one_line(draw, summary, sans_13, col_w)
        draw.text((cx, ty), summary, font=sans_13, fill=MUTED)

    # Footer sources line.
    fy = HEIGHT - 30
    draw.line([(MARGIN, fy - 8), (WIDTH - MARGIN, fy - 8)], fill=INK, width=1)
    sw = draw.textlength(SOURCES_LINE, font=sans_13)
    draw.text(((WIDTH - sw) / 2, fy), SOURCES_LINE, font=sans_13, fill=MUTED)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img.save(OUTPUT_PATH, format="PNG")
    return OUTPUT_PATH


def fallback_copy():
    """Copy the shipped entry.png byte-for-byte to the output path."""
    shipped = os.path.join(REPO_DIR, "entry.png")
    if not os.path.isfile(shipped):
        raise RuntimeError("fallback entry.png is missing from the repo")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(shipped, OUTPUT_PATH)
    return OUTPUT_PATH


def main():
    try:
        path = render()
    except Exception:
        # Pillow, fonts, or hero.png unavailable: ship the pre-rendered image.
        path = fallback_copy()
    print("wrote " + path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
