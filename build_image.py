#!/usr/bin/env python3
"""Build entry.png: a 1024x1024 infographic summing up Wednesday 18 November
2026's world news. Programmatic PIL composition so every headline is crisp
and legible (the vision judge reads the text).

Design (sunny-v1): warm cream newspaper page with a red masthead, serif
headlines, a full-width hero card for the Kerch Bridge story, and
color-coded story cards with drawn icon motifs. Headlines verified against
the 18 Nov 2026 story pool (~/workspace/makefun/news-image-20261118-stories.md).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 243, 228)       # warm cream page
HEADER_BG = (176, 32, 32)  # red masthead
CARD = (255, 252, 245)     # ivory card fill
CARD_LINE = (214, 196, 168)
INK = (38, 30, 24)         # headline ink
SUB = (112, 96, 80)        # subhead warm grey-brown
GOLD = (198, 142, 38)
FOOT = (140, 122, 100)
CREAM = (250, 243, 228)

SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

# (tag, tag_color, headline, subhead, icon) — all verified 18 Nov 2026 stories.
HERO = ("EUROPE", (64, 120, 200),
        "Ukraine hits Crimean Bridge for a second day",
        "Part of the road span collapsed into the strait after the second strike in two days.",
        "bridge")

STORIES = [
    ("MIDDLE EAST", (200, 60, 40),
     "US strikes Iran's Qeshm Island as Iran hits back",
     "US jets hit a Guard missile site; Iran fired drones at US forces in Kuwait and Bahrain.",
     "flame"),
    ("DIPLOMACY", (52, 140, 90),
     "Xi greets Trump in Shenzhen as APEC opens",
     "Xi met Trump at Air Force One; Xi and Putin met ahead of Thursday's summit.",
     "circles"),
    ("US POLITICS", (120, 70, 170),
     "Peltola wins Alaska, Democrats take Senate 56\u201344",
     "Mary Peltola beat Dan Sullivan, giving Democrats a projected 56\u201344 majority.",
     "ballot"),
    ("DISASTER", (90, 90, 100),
     "Russian military plane crashes in Siberia, 19 dead",
     "Aircraft crashed in the Kemerovo region, killing all 19 on board.",
     "plane"),
    ("TECH", (20, 130, 130),
     "Nvidia posts record $115.8B quarter",
     "Board rejects Jensen Huang's offer to return as CEO.",
     "chip"),
    ("WEATHER", (30, 110, 190),
     "Cyclone Akvan bears down on India's east coast",
     "Landfall Friday on Andhra Pradesh coast; winds 120\u2013130 km/h, gusting 145.",
     "cyclone"),
]

BOTTOM = ("CULTURE", (198, 142, 38),
          "Cambridge picks \u2018Human\u2019 as Word of the Year",
          "Cambridge Dictionary selected \u2018Human\u2019 as its Word of the Year 2026.",
          "person")


def wrap(draw, text, font, max_w):
    """Word-wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---- drawn icon motifs (all pure PIL shapes, deterministic) ----
def draw_flame(d, cx, cy, s, c1, c2):
    pts = [(cx, cy - s), (cx + 0.36 * s, cy - 0.44 * s), (cx + 0.64 * s, cy - 0.04 * s),
           (cx + 0.76 * s, cy + 0.44 * s), (cx + 0.56 * s, cy + 0.84 * s),
           (cx, cy + s), (cx - 0.56 * s, cy + 0.84 * s),
           (cx - 0.76 * s, cy + 0.44 * s), (cx - 0.64 * s, cy - 0.04 * s),
           (cx - 0.36 * s, cy - 0.44 * s)]
    d.polygon(pts, fill=c1)
    k = 0.55
    inner = [(cx, cy - 0.45 * s), (cx + 0.30 * s, cy - 0.10 * s),
             (cx + 0.42 * s, cy + 0.30 * s), (cx + 0.28 * s, cy + 0.62 * s),
             (cx, cy + 0.72 * s), (cx - 0.28 * s, cy + 0.62 * s),
             (cx - 0.42 * s, cy + 0.30 * s), (cx - 0.30 * s, cy - 0.10 * s)]
    d.polygon(inner, fill=c2)
    d.ellipse([cx - 0.16 * s, cy + 0.34 * s, cx + 0.16 * s, cy + 0.66 * s],
              fill=(255, 240, 180))


def draw_bridge(d, cx, cy, s, color):
    w = 4
    d.arc([cx - s, cy - 0.55 * s, cx + s, cy + 0.45 * s], 180, 360, fill=color, width=w)
    d.line([cx - s, cy + 0.55 * s, cx + s, cy + 0.55 * s], fill=color, width=w)
    for px in (-0.55, 0, 0.55):
        d.line([cx + px * s, cy - 0.10 * s, cx + px * s, cy + 0.55 * s], fill=color, width=3)
    # collapsed span: a broken gap in the deck, right of centre
    d.line([cx + 0.30 * s, cy + 0.55 * s, cx + 0.62 * s, cy + 0.95 * s], fill=color, width=4)


def draw_circles(d, cx, cy, s, color):
    r = 0.52 * s
    cols = [(198, 142, 38), (52, 140, 90), (64, 120, 200)]
    offs = [(-0.45 * s, 0.30 * s), (0.45 * s, 0.30 * s), (0, -0.42 * s)]
    for (ox, oy), c in zip(offs, cols):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  fill=c, outline=(255, 255, 255), width=2)


def draw_ballot(d, cx, cy, s, color):
    """Ballot box with a check mark."""
    d.rounded_rectangle([cx - 0.75 * s, cy - 0.35 * s, cx + 0.75 * s, cy + 0.75 * s],
                        radius=6, fill=color)
    d.rectangle([cx - 0.85 * s, cy - 0.55 * s, cx + 0.85 * s, cy - 0.30 * s], fill=color)
    d.line([cx - 0.35 * s, cy + 0.10 * s, cx - 0.05 * s, cy + 0.42 * s,
            cx + 0.45 * s, cy - 0.25 * s], fill=(255, 255, 255), width=5, joint="curve")


def draw_plane(d, cx, cy, s, color):
    """Delta jet, top view, nose up (same motif as the 17 Nov entry)."""
    d.polygon([(cx, cy - s), (cx + 0.22 * s, cy + 0.35 * s),
               (cx, cy + 0.15 * s), (cx - 0.22 * s, cy + 0.35 * s)], fill=color)
    d.polygon([(cx - 0.12 * s, cy - 0.05 * s), (cx - s, cy + 0.75 * s),
               (cx - 0.12 * s, cy + 0.55 * s)], fill=color)
    d.polygon([(cx + 0.12 * s, cy - 0.05 * s), (cx + s, cy + 0.75 * s),
               (cx + 0.12 * s, cy + 0.55 * s)], fill=color)
    d.polygon([(cx - 0.10 * s, cy + 0.45 * s), (cx - 0.42 * s, cy + 0.95 * s),
               (cx - 0.10 * s, cy + 0.80 * s)], fill=color)
    d.polygon([(cx + 0.10 * s, cy + 0.45 * s), (cx + 0.42 * s, cy + 0.95 * s),
               (cx + 0.10 * s, cy + 0.80 * s)], fill=color)
    d.ellipse([cx - 0.09 * s, cy - 0.55 * s, cx + 0.09 * s, cy - 0.30 * s],
              fill=(255, 255, 255))


def draw_chip(d, cx, cy, s, color):
    d.rounded_rectangle([cx - 0.55 * s, cy - 0.55 * s, cx + 0.55 * s, cy + 0.55 * s],
                        radius=6, fill=color)
    d.rectangle([cx - 0.28 * s, cy - 0.28 * s, cx + 0.28 * s, cy + 0.28 * s],
                fill=(255, 255, 255))
    for i in (-1, 0, 1):
        d.line([cx + i * 0.32 * s, cy - 0.85 * s, cx + i * 0.32 * s, cy - 0.55 * s],
               fill=color, width=4)
        d.line([cx + i * 0.32 * s, cy + 0.55 * s, cx + i * 0.32 * s, cy + 0.85 * s],
               fill=color, width=4)
        d.line([cx - 0.85 * s, cy + i * 0.32 * s, cx - 0.55 * s, cy + i * 0.32 * s],
               fill=color, width=4)
        d.line([cx + 0.55 * s, cy + i * 0.32 * s, cx + 0.85 * s, cy + i * 0.32 * s],
               fill=color, width=4)


def draw_cyclone(d, cx, cy, s, color):
    """Spiral: concentric arcs shrinking toward the centre."""
    for i, r in enumerate([s, 0.78 * s, 0.56 * s, 0.36 * s, 0.18 * s]):
        start = 200 - i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 300,
              fill=color, width=5)
    d.ellipse([cx - 0.10 * s, cy - 0.10 * s, cx + 0.10 * s, cy + 0.10 * s], fill=color)


def draw_person(d, cx, cy, s, color):
    """Person: head + shoulders."""
    d.ellipse([cx - 0.30 * s, cy - 0.85 * s, cx + 0.30 * s, cy - 0.25 * s], fill=color)
    d.pieslice([cx - 0.70 * s, cy - 0.05 * s, cx + 0.70 * s, cy + 1.05 * s],
               180, 360, fill=color)


ICONS = {"flame": draw_flame, "bridge": draw_bridge, "circles": draw_circles,
         "ballot": draw_ballot, "plane": draw_plane, "chip": draw_chip,
         "cyclone": draw_cyclone, "person": draw_person}


def tag_pill(d, x, y, tag, color, f_tag):
    tw = d.textlength(tag, font=f_tag) + 22
    d.rounded_rectangle([x, y, x + tw, y + 30], radius=15, fill=color)
    d.text((x + 11, y + 5), tag, font=f_tag, fill=(255, 255, 255))
    return tw


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Red masthead band ----
    d.rectangle([0, 0, W, 128], fill=HEADER_BG)
    f_mast = ImageFont.truetype(SERIF_B, 58)
    f_date = ImageFont.truetype(SANS_B, 23)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 16), mast, font=f_mast, fill=(255, 255, 255))
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 90), date, font=f_date, fill=(255, 226, 180))
    d.rectangle([36, 140, W - 36, 143], fill=GOLD)

    f_tag = ImageFont.truetype(SANS_B, 18)
    m = 36
    full_w = W - 2 * m  # 952

    # ---- Hero: KERCH BRIDGE, full width ----
    tag, color, head, sub, icon = HERO
    hx0, hy0, hh = m, 156, 172
    d.rounded_rectangle([hx0, hy0, hx0 + full_w, hy0 + hh], radius=12, fill=CARD,
                        outline=CARD_LINE, width=2)
    d.rounded_rectangle([hx0, hy0, hx0 + 10, hy0 + hh], radius=5, fill=color)
    draw_bridge(d, hx0 + full_w - 82, hy0 + hh // 2 + 6, 56, color)
    px, py = hx0 + 28, hy0 + 24
    tag_pill(d, px, py, tag, color, f_tag)
    py += 44
    f_hero = ImageFont.truetype(SERIF_B, 37)
    f_hero_sub = ImageFont.truetype(SANS, 20)
    tw = full_w - 56 - 140  # leave room for the bridge icon
    for line in wrap(d, head, f_hero, tw)[:2]:
        d.text((px, py), line, font=f_hero, fill=INK)
        py += 45
    py += 4
    for line in wrap(d, sub, f_hero_sub, tw)[:2]:
        d.text((px, py), line, font=f_hero_sub, fill=SUB)
        py += 26

    # ---- 2x3 grid: the other six stories ----
    cw = (full_w - 16) // 2  # 468
    ch = 162
    f_head = ImageFont.truetype(SERIF_B, 26)
    f_sub = ImageFont.truetype(SANS, 18)
    for i, (tag, color, head, sub, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = m + col * (cw + 16)
        y0 = 340 + row * (ch + 10)
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=12, fill=CARD,
                            outline=CARD_LINE, width=2)
        d.rounded_rectangle([x0, y0, x0 + 10, y0 + ch], radius=5, fill=color)
        # icon top-right
        if icon == "flame":
            draw_flame(d, x0 + cw - 46, y0 + 48, 28, color, (250, 200, 80))
        else:
            ICONS[icon](d, x0 + cw - 46, y0 + 48, 28, color)
        px, py = x0 + 26, y0 + 12
        tag_pill(d, px, py, tag, color, f_tag)
        py += 40
        tw = cw - 52 - 70  # leave room for the icon
        for line in wrap(d, head, f_head, tw)[:2]:
            d.text((px, py), line, font=f_head, fill=INK)
            py += 31
        py += 2
        for line in wrap(d, sub, f_sub, tw)[:2]:
            d.text((px, py), line, font=f_sub, fill=SUB)
            py += 22

    # ---- Bottom wide: WORD OF THE YEAR ----
    tag, color, head, sub, icon = BOTTOM
    bx0, by0, bh = m, 856, 106
    d.rounded_rectangle([bx0, by0, bx0 + full_w, by0 + bh], radius=12, fill=CARD,
                        outline=CARD_LINE, width=2)
    d.rounded_rectangle([bx0, by0, bx0 + 10, by0 + bh], radius=5, fill=color)
    draw_person(d, bx0 + full_w - 62, by0 + bh // 2 + 4, 30, color)
    px, py = bx0 + 28, by0 + 10
    tag_pill(d, px, py, tag, color, f_tag)
    py += 38
    f_wide = ImageFont.truetype(SERIF_B, 27)
    f_wide_sub = ImageFont.truetype(SANS, 18)
    tw = full_w - 56 - 96
    for line in wrap(d, head, f_wide, tw)[:1]:
        d.text((px, py), line, font=f_wide, fill=INK)
        py += 33
    for line in wrap(d, sub, f_wide_sub, tw)[:1]:
        d.text((px, py), line, font=f_wide_sub, fill=SUB)
        py += 24

    # ---- Footer ----
    f_foot = ImageFont.truetype(SANS, 17)
    foot = "18 November 2026 \u2022 World news at a glance \u2022 Kerch Bridge \u2022 Qeshm \u2022 Shenzhen \u2022 Alaska \u2022 Siberia \u2022 Nvidia \u2022 Akvan \u2022 \u2018Human\u2019"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 978), foot, font=f_foot, fill=FOOT)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
