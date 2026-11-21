#!/usr/bin/env python3
"""Render the front page for Saturday 21 November 2026.

Build-time only: draws "The World in One Page" -- a 1024x1024 newspaper
front page summing up the day's world news -- and saves it as entry.png
next to this script. Requires Pillow. The shipped entry program
(main.py) is stdlib-only and simply copies entry.png to /output.

The day's reporting (21 November 2026) behind the page:
- Hero: Russian missiles and a drone came down in Poland during a
  barrage of about 100 missiles on Ukraine; Warsaw called it a
  deliberate provocation, NATO a grave violation of its airspace.
- Panels: the Trump-Xi-Putin Shenzhen trilateral summit wraps; Wall
  Street slides into correction as AI stocks plunge.
- Briefs and the numbers strip draw on the same day's reporting.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 36
RIGHT = W - MARGIN
CONTENT_W = RIGHT - MARGIN

PAPER = (247, 243, 233)
PANEL_BG = (238, 231, 214)
INK = (26, 23, 19)
FAINT = (96, 88, 74)
RED = (164, 32, 28)
NAVY = (18, 28, 54)
DARK = (18, 18, 22)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap(draw, s, fnt, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, s, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, s, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, x0=MARGIN, x1=RIGHT, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- art panel

def draw_hero_art(img, box):
    """Night sky over a border town: missile trails arc down, bursts bloom."""
    x0, y0, x1, y1 = box
    art = Image.new("RGB", (x1 - x0, y1 - y0), NAVY)
    d = ImageDraw.Draw(art)
    aw, ah = art.size

    top, bot = (8, 12, 30), (52, 62, 102)
    for i in range(ah):
        t = i / max(ah - 1, 1)
        d.line([(0, i), (aw, i)], fill=tuple(
            int(top[c] + (bot[c] - top[c]) * t) for c in range(3)))

    rng = random.Random(20261121)
    for _ in range(90):  # stars
        sx, sy = rng.randrange(aw), rng.randrange(int(ah * 0.62))
        r = rng.choice([1, 1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(210, 216, 235))

    d.ellipse([aw - 74, 22, aw - 30, 66], fill=(232, 230, 214))
    d.ellipse([aw - 86, 16, aw - 44, 58], fill=(16, 22, 46))

    ground_y = int(ah * 0.84)
    impacts = [(int(aw * 0.24), ground_y), (int(aw * 0.52), ground_y + 4),
               (int(aw * 0.78), ground_y)]

    def trail(sx, sy, ex, ey, bend):
        pts = []
        for i in range(41):
            t = i / 40
            mx = (sx + ex) / 2 + bend
            my = min(sy, ey) - 46
            px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t ** 2 * ex
            py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * my + t ** 2 * ey
            pts.append((px, py))
        d.line(pts, fill=(146, 44, 34), width=7)
        d.line(pts, fill=(255, 176, 102), width=3)
        hx, hy = pts[-1]
        d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=(255, 226, 170))

    trail(int(aw * 0.06), 8, impacts[0][0], impacts[0][1], -30)
    trail(int(aw * 0.38), 2, impacts[1][0], impacts[1][1], 18)
    trail(int(aw * 0.66), 14, impacts[2][0], impacts[2][1], 34)

    d.rectangle([0, ground_y, aw, ah], fill=(10, 10, 16))
    for bx, bw, bh in [(18, 52, 26), (86, 38, 18), (150, 60, 32),
                       (236, 44, 20), (300, 56, 28)]:
        d.rectangle([bx, ground_y - bh, bx + bw, ground_y], fill=(10, 10, 16))
        d.polygon([(bx - 3, ground_y - bh), (bx + bw + 3, ground_y - bh),
                   (bx + bw // 2, ground_y - bh - 12)], fill=(10, 10, 16))
    for wx, wy in [(30, ground_y - 16), (168, ground_y - 20),
                   (318, ground_y - 18), (250, ground_y - 10)]:
        d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 196, 92))

    for ex, ey in impacts:
        for ang in range(0, 360, 30):
            r1 = 16 + (ang % 90) // 6
            d.line([(ex, ey), (ex + r1 * math.cos(math.radians(ang)),
                               ey - abs(r1 * math.sin(math.radians(ang))))],
                   fill=(255, 150, 60), width=3)
        d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 214, 130))

    img.paste(art, (x0, y0))
    d2 = ImageDraw.Draw(img)
    d2.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    cap = "MISSILE TRAILS OVER POLAND — NATO'S EASTERN FLANK"
    cap_size = 13
    cf = font(SANS_B, cap_size)
    while text_w(d2, cap, cf) > (x1 - x0) - 12 and cap_size > 8:
        cap_size -= 1
        cf = font(SANS_B, cap_size)
    cw = text_w(d2, cap, cf)
    d2.rectangle([x0, y1 - 26, x1, y1], fill=(10, 10, 16))
    d2.text((x0 + (x1 - x0 - cw) / 2, y1 - 20), cap, font=cf,
            fill=(238, 234, 220))


def draw_chart(draw, box):
    """A plunging market line for the markets panel."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(24, 24, 30))
    pts = [(0.04, 0.30), (0.20, 0.24), (0.36, 0.38), (0.50, 0.34),
           (0.64, 0.52), (0.78, 0.62), (0.96, 0.86)]
    xy = [(x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)) for fx, fy in pts]
    for gx in (0.25, 0.5, 0.75):
        draw.line([(x0 + gx * (x1 - x0), y0 + 4),
                   (x0 + gx * (x1 - x0), y1 - 4)], fill=(52, 52, 62), width=1)
    draw.line(xy, fill=(232, 84, 60), width=4)
    for px, py in xy:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 170, 140))
    draw.text((x0 + 10, y0 + 6), "S&P 500  -3.7%", font=font(SANS_B, 17),
              fill=(255, 205, 180))


# ---------------------------------------------------------------- the page

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([MARGIN, 30, RIGHT, H - 30], outline=INK, width=2)
    f_mast = font(SERIF_B, 55)
    title = "THE WORLD IN ONE PAGE"
    d.text(((W - text_w(d, title, f_mast)) / 2, 44), title,
           font=f_mast, fill=INK)
    rule(d, 118, width=3)
    rule(d, 124, width=1)
    f_date = font(SANS_B, 17)
    d.text((MARGIN + 6, 134), "SATURDAY 21 NOVEMBER 2026", font=f_date,
           fill=INK)
    tag = "THE DAY'S WORLD NEWS IN A SINGLE IMAGE"
    d.text((RIGHT - 6 - text_w(d, tag, f_date), 134), tag, font=f_date,
           fill=FAINT)
    rule(d, 162, width=2)

    # ---- hero (text left, art right)
    hero_x1 = 606
    d.text((MARGIN + 6, 174), "WAR IN EUROPE — ESCALATION",
           font=font(SANS_B, 19), fill=RED)
    f_head = font(SERIF_B, 57)
    while (text_w(d, "RUSSIAN MISSILES", f_head) > hero_x1 - MARGIN - 10
           and f_head.size > 30):
        f_head = font(SERIF_B, f_head.size - 1)
    d.text((MARGIN + 4, 200), "RUSSIAN MISSILES", font=f_head, fill=INK)
    d.text((MARGIN + 4, 200 + f_head.size + 8), "FALL ON POLAND",
           font=f_head, fill=INK)
    deck = ("Two Russian missiles and a suspected drone came down on "
            "Polish soil during an overnight barrage of some 100 "
            "missiles on Ukraine. Warsaw called it a deliberate "
            "provocation; NATO, a grave violation of its airspace.")
    draw_wrapped(d, (MARGIN + 6, 336), deck, font(SANS, 20), INK,
                 hero_x1 - MARGIN - 12, 27)
    draw_hero_art(img, (622, 174, RIGHT - 6, 472))
    rule(d, 486, width=2)

    # ---- two panels
    py, ph = 498, 148
    mid = (MARGIN + RIGHT) // 2
    for x0, x1 in [(MARGIN + 4, mid - 8), (mid + 8, RIGHT - 4)]:
        d.rectangle([x0, py, x1, py + ph], fill=PANEL_BG)
        d.rectangle([x0, py, x1, py + ph], outline=INK, width=1)

    d.text((MARGIN + 18, py + 10), "SHENZHEN — THE SUMMIT",
           font=font(SANS_B, 17), fill=NAVY)
    chips = [("US", (46, 62, 110)), ("CHINA", (178, 40, 34)),
             ("RUSSIA", (90, 104, 140))]
    cx = MARGIN + 18
    for label, col in chips:
        cf = font(SANS_B, 13)
        wch = text_w(d, label, cf) + 16
        d.rectangle([cx, py + 36, cx + wch, py + 58], fill=col)
        d.text((cx + 8, py + 40), label, font=cf, fill=(245, 242, 232))
        cx += wch + 8
    summit = ("Trump, Xi and Putin end the first US–China–Russia summit "
              "with pledges on UN reform, oil and nuclear-risk talks — "
              "few concrete results. Trump then phones European allies "
              "about Ukraine.")
    draw_wrapped(d, (MARGIN + 18, py + 68), summit, font(SANS, 15), INK,
                 mid - 8 - MARGIN - 34, 20)

    d.text((mid + 26, py + 10), "MARKETS — THE SLIDE",
           font=font(SANS_B, 17), fill=RED)
    draw_chart(d, (mid + 26, py + 38, mid + 206, py + 132))
    markets = ("AI and chip stocks plunge; S&P 500 and Dow enter "
               "correction, dollar at a 19-month high — Anthropic's "
               "$119.5B record IPO lands mid-sell-off.")
    draw_wrapped(d, (mid + 220, py + 37), markets, font(SANS, 14), INK,
                 RIGHT - 4 - (mid + 220) - 10, 19)
    rule(d, py + ph + 14, width=2)

    # ---- briefs
    by = py + ph + 28
    d.text((MARGIN + 6, by), "THE REST OF THE DAY — IN BRIEF",
           font=font(SANS_B, 18), fill=INK)
    by += 32
    briefs = [
        ("THE HAGUE", "World Court finds Myanmar committed genocide "
         "against the Rohingya."),
        ("BRUSSELS", "Britain and the EU sign food, carbon and "
         "youth-mobility deals."),
        ("HORMUZ", "Iran war nears month nine; Trump in no hurry, IEA "
         "sees a lasting energy shock."),
        ("RIYADH", "Saudi defences intercept three Houthi ballistic "
         "missiles fired at Riyadh."),
        ("KYIV", "Ukraine destroys three Russian missile launchers; "
         "EU sends €1bn in air defence."),
        ("HEALTH", "A pill is hailed as a breakthrough against "
         "pancreatic cancer."),
        ("LOS ANGELES", "Jury convicts the man who started the "
         "Palisades Fire."),
        ("WASHINGTON", "Nationwide air-traffic outage grounds "
         "thousands of US flights."),
        ("JERUSALEM", "President taps ex-army chief Eisenkot to form "
         "a government."),
        ("ODISHA", "Cyclone Akvan makes landfall; Indonesia fire "
         "losses may hit $30B."),
    ]
    col_w = (CONTENT_W - 28) // 2
    f_br = font(SANS, 16)
    f_brb = font(SANS_B, 16)
    for i, (place, body) in enumerate(briefs):
        col, row = i % 2, i // 2
        x = MARGIN + 6 + col * (col_w + 16)
        y = by + row * 39
        num_s = f"{i + 1}."
        d.text((x, y), num_s, font=f_brb, fill=RED)
        off0 = max(30, int(text_w(d, num_s, f_brb)) + 8)
        tag_s = place + " — "
        d.text((x + off0, y), tag_s, font=f_brb, fill=INK)
        avail = col_w - off0 - text_w(d, tag_s, f_brb)
        words, line1 = body.split(), ""
        while words:
            trial = words[0] if not line1 else line1 + " " + words[0]
            if text_w(d, trial, f_br) <= avail:
                line1 = trial
                words.pop(0)
            else:
                break
        d.text((x + off0 + text_w(d, tag_s, f_brb), y), line1, font=f_br,
               fill=INK)
        if words:
            line2 = " ".join(words)
            while text_w(d, line2, f_br) > col_w - off0 and " " in line2:
                line2 = line2.rsplit(" ", 1)[0]
            d.text((x + off0, y + 20), line2, font=f_br, fill=INK)

    # ---- numbers strip
    ny = 912
    d.rectangle([MARGIN + 4, ny, RIGHT - 4, ny + 50], fill=DARK)
    stats = [("~100", "missiles fired at Ukraine"),
             ("-3.7%", "S&P 500, into correction"),
             ("$119.5B", "Anthropic's record IPO"),
             ("42", "injured in Kryvyi Rih"),
             ("3", "missiles stopped over Riyadh")]
    sw = (CONTENT_W - 8) // len(stats)
    for i, (num, lab) in enumerate(stats):
        x = MARGIN + 12 + i * sw
        d.text((x, ny + 5), num, font=font(SANS_B, 21),
               fill=(240, 200, 110))
        d.text((x, ny + 31), lab, font=font(SANS, 12),
               fill=(232, 228, 216))

    foot = "Compiled from the day's reporting · One image, one day"
    d.text(((W - text_w(d, foot, font(SANS, 13))) / 2, 972), foot,
           font=font(SANS, 13), fill=FAINT)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
