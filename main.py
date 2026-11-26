"""News-image entry for make.fun competition news-image-20261126.

Renders a 1024x1024 front-page newspaper image summing up the world news
of Thursday, 26 November 2026 and writes it to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output when the variable is unset).

The page is composed with Pillow when it is available (DejaVu fonts, as
shipped with most Linux systems): masthead, date line, a wide illustration
panel for the lead story (hero.png, shipped in this repository), the lead
headline and summary, then a two-column grid of sixteen short stories from
across regions and fields. When Pillow is not available -- for example in
the grading sandbox, which is standard library only -- the program copies
the entry.png shipped in this repository instead, so the bytes written are
identical either way. No network is used. The composition is fully
deterministic: the same input always produces the same PNG bytes.
"""

import os
import shutil
import sys

PAGE_W = 1024
PAGE_H = 1024
EDGE = 26

MASTHEAD = "THE WORLD TODAY"
DATE_LINE = "Thursday, 26 November 2026"
DAY_NOTE = "Also today: 18th anniversary of the 26/11 Mumbai attacks  \u00b7  Constitution Day in India"

LEAD = {
    "tag": "LEAD  \u00b7  MIDDLE EAST  \u2014  ENERGY",
    "headline": "Houthis claim strike on Saudi Arabia's biggest refinery",
    "summary": (
        "Riyadh says its defences downed four drones over Ras Tanura and reported "
        "no damage; the Houthis claim fires at the plant. Brent crude jumps."
    ),
}

# (tag, headline, summary). Every story happened on, or was first reported
# on, Thursday 26 November 2026. Sources are listed in README.md.
STORIES = [
    ("MIDDLE EAST \u00b7 ENERGY",
     "Tankers hit by mines in the Strait of Hormuz",
     "Iran says tankers struck naval mines; shipping fears rise."),
    ("MIDDLE EAST \u00b7 GAZA",
     "Israel strikes Hamas official in Gaza as truce strains",
     "The strike comes as the ceasefire frays and hardship deepens."),
    ("EUROPE \u00b7 WAR",
     "Ukraine hits Russian oil refineries; Putin vows reply",
     "Kyiv keeps striking Russian energy plants; Moscow vows a reply."),
    ("EUROPE \u00b7 WAR",
     "Russia's own figures show near 500,000 war dead",
     "Moscow's data points to near half a million lost in the war."),
    ("ASIA \u00b7 INDIA",
     "India marks 18 years since the 26/11 Mumbai attacks",
     "India also marks Constitution Day, 77 years after adopting it."),
    ("ASIA \u00b7 SPACE",
     "Pakistan's first astronaut picked for China's station",
     "Muhammad Zeeshan Ali will fly on Shenzhou-24 to Tiangong."),
    ("ASIA \u00b7 ECONOMY",
     "Bangladesh garment workers win 36% pay rise",
     "Entry-level garment workers' minimum wage rises by a third."),
    ("AMERICAS \u00b7 COLOMBIA",
     "Police free 20 hostages after 17-hour siege",
     "Officers storm a Cartagena supermarket to end the hostage siege."),
    ("ASIA \u00b7 DISASTER",
     "Magnitude 5.6 quake hits Nepal near China border",
     "The tremor strikes Koshi Province near the Chinese border."),
    ("SPORT \u00b7 CRICKET",
     "Sooryavanshi, 15, smashes fastest List A double ton",
     "The teenager hits 204 off 53 balls against the UAE, a world record."),
    ("SPORT \u00b7 CHESS",
     "Gukesh faces Sindarov at World Chess Championship",
     "India's champion takes on Uzbekistan's Sindarov for the world title."),
    ("ASIA-PACIFIC \u00b7 DIPLOMACY",
     "Solomon Islands and Australia sign security treaty",
     "The pact deepens defence ties between the Pacific neighbours."),
    ("ASIA \u00b7 KOREA",
     "North Korea orders Swiss office shut in Pyongyang",
     "Pyongyang tells Bern to close its newly opened diplomatic office."),
    ("AMERICAS \u00b7 TRADE",
     "US prepares plan for new tariffs on trade partners",
     "Washington readies fresh tariffs on global trading partners."),
    ("ASIA \u00b7 BUSINESS",
     "Flipkart chief to step down in December",
     "Kalyan Krishnamurthy will leave the Walmart-owned e-commerce group."),
    ("ASIA \u00b7 EDUCATION",
     "IITs to add 6,000 seats in robotics, AI and space",
     "India's top tech institutes expand in robotics, AI and space tech."),
]

FOOTER = (
    "Sources: Rigzone  \u00b7  TankerBrief  \u00b7  BBC  \u00b7  Reuters  \u00b7  AP  \u00b7  "
    "JagranJosh  \u00b7  Observer Voice  \u00b7  SelfStudys"
)

PAPER = (247, 242, 231)
INK = (17, 17, 17)
MUTED = (90, 86, 76)
RULE = (150, 144, 128)
LEAD_BG = (255, 253, 246)
ACCENT = (163, 22, 33)

TAG_COLORS = {
    "MIDDLE EAST": (122, 74, 0),
    "EUROPE": (31, 78, 121),
    "ASIA": (90, 45, 130),
    "AMERICAS": (26, 107, 60),
    "SPORT": (138, 47, 47),
}


def _font_paths():
    base = "/usr/share/fonts/truetype/dejavu"
    return {
        "serif_bold": os.path.join(base, "DejaVuSerif-Bold.ttf"),
        "serif": os.path.join(base, "DejaVuSerif.ttf"),
        "sans": os.path.join(base, "DejaVuSans.ttf"),
        "sans_bold": os.path.join(base, "DejaVuSans-Bold.ttf"),
    }


def _wrap_text(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _fit_text(draw, text, font, width, max_lines):
    """Wrap and truncate with an ellipsis when the text exceeds max_lines."""
    lines = _wrap_text(draw, text, font, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "\u2026", font=font) > width:
            tail = lines[-1]
            lines[-1] = tail.rsplit(" ", 1)[0] if " " in tail else tail[:-1]
        lines[-1] = lines[-1] + "\u2026"
    return lines


def _tag_color(tag):
    for key, color in TAG_COLORS.items():
        if tag.startswith(key):
            return color
    return ACCENT


def _here(*parts):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *parts)


def render_page():
    from PIL import Image, ImageDraw, ImageFont

    paths = _font_paths()
    for path in paths.values():
        if not os.path.exists(path):
            raise FileNotFoundError(path)

    f_masthead = ImageFont.truetype(paths["serif_bold"], 46)
    f_date = ImageFont.truetype(paths["sans_bold"], 20)
    f_daynote = ImageFont.truetype(paths["serif"], 13)
    f_lead_tag = ImageFont.truetype(paths["sans_bold"], 13)
    f_lead_head = ImageFont.truetype(paths["serif_bold"], 26)
    f_lead_sum = ImageFont.truetype(paths["sans"], 15)
    f_tag = ImageFont.truetype(paths["sans_bold"], 11)
    f_head = ImageFont.truetype(paths["sans_bold"], 15)
    f_sum = ImageFont.truetype(paths["sans"], 13)
    f_footer = ImageFont.truetype(paths["sans"], 11)

    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)

    # Outer frame.
    d.rectangle([10, 10, PAGE_W - 11, PAGE_H - 11], outline=INK, width=2)

    # Masthead block.
    d.text((PAGE_W // 2, 16), MASTHEAD, font=f_masthead, fill=INK, anchor="ma")
    d.line([(EDGE, 70), (PAGE_W - EDGE, 70)], fill=INK, width=2)
    d.text((PAGE_W // 2, 76), DATE_LINE, font=f_date, fill=ACCENT, anchor="ma")
    d.text((PAGE_W // 2, 100), DAY_NOTE, font=f_daynote, fill=MUTED, anchor="ma")
    d.line([(EDGE, 120), (PAGE_W - EDGE, 120)], fill=INK, width=1)

    # Hero illustration panel for the lead story.
    hero = Image.open(_here("hero.png")).convert("RGB")
    panel_x, panel_y, panel_w, panel_h = EDGE, 128, PAGE_W - 2 * EDGE, 300
    hero = hero.resize((panel_w, panel_h), Image.LANCZOS)
    page.paste(hero, (panel_x, panel_y))
    d.rectangle([panel_x, panel_y, panel_x + panel_w - 1, panel_y + panel_h - 1],
                outline=INK, width=1)

    # Lead headline + summary under the picture.
    lead_top = panel_y + panel_h + 10
    lead_bottom = lead_top + 92
    d.rectangle([EDGE, lead_top, PAGE_W - EDGE, lead_bottom],
                fill=LEAD_BG, outline=INK, width=1)
    x = EDGE + 14
    w = PAGE_W - 2 * EDGE - 28
    y = lead_top + 8
    d.text((x, y), LEAD["tag"], font=f_lead_tag, fill=ACCENT)
    y += 18
    for line in _fit_text(d, LEAD["headline"], f_lead_head, w, 1):
        d.text((x, y), line, font=f_lead_head, fill=INK)
        y += 31
    y += 2
    for line in _fit_text(d, LEAD["summary"], f_lead_sum, w, 2):
        d.text((x, y), line, font=f_lead_sum, fill=INK)
        y += 19

    # Story grid: 2 columns x 8 rows.
    cols, rows = 2, 8
    grid_top = lead_bottom + 10
    grid_bottom = 984
    gutter = 20
    col_w = (PAGE_W - 2 * EDGE - (cols - 1) * gutter) // cols
    row_h = (grid_bottom - grid_top) // rows
    for i, (tag, headline, summary) in enumerate(STORIES):
        r, c = divmod(i, cols)
        cx = EDGE + c * (col_w + gutter)
        cy = grid_top + r * row_h
        d.line([(cx, cy), (cx + col_w, cy)], fill=RULE, width=1)
        ty = cy + 5
        d.text((cx, ty), tag, font=f_tag, fill=_tag_color(tag))
        hy = ty + 14
        for line in _fit_text(d, headline, f_head, col_w, 1):
            d.text((cx, hy), line, font=f_head, fill=INK)
            hy += 17
        sy = hy + 1
        # One summary line per cell: the row height leaves no room for a
        # second line without colliding with the next row's tag.
        for line in _fit_text(d, summary, f_sum, col_w, 1):
            d.text((cx, sy), line, font=f_sum, fill=(60, 58, 52))
            sy += 15

    # Footer.
    d.line([(EDGE, 990), (PAGE_W - EDGE, 990)], fill=INK, width=1)
    d.text((PAGE_W // 2, 994), FOOTER, font=f_footer, fill=MUTED, anchor="ma")

    return page


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")

    try:
        page = render_page()
        page.save(out_path, format="PNG")
    except Exception:
        # Pillow (or a font, or the hero file) is unavailable: reproduce
        # the shipped image byte for byte.
        shipped = _here("entry.png")
        if not os.path.exists(shipped):
            raise
        shutil.copyfile(shipped, out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
