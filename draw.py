#!/usr/bin/env python3
"""news-23 b139 heroes-scene: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024 front page, 31 stories. PIL only. Run: python3 draw.py -> entry.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/truetype/dejavu"

CREAM = (247, 243, 232)
INK = (26, 26, 26)
RED = (163, 22, 33)
DARKRED = (139, 26, 26)
GOLD = (166, 124, 0)
GOLD_L = (184, 134, 11)
NAVY = (31, 56, 100)
GREEN = (46, 125, 50)
PURPLE = (106, 27, 154)
TEAL = (0, 105, 92)
ORANGE = (230, 81, 0)
GREY = (90, 85, 75)
LIGHT = (232, 226, 210)
MAPGREEN = (196, 214, 178)
MAPEDGE = (150, 175, 130)


def f_serif(size):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSerif-Bold.ttf"), size)


def f_bold(size):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSans-Bold.ttf"), size)


def f_reg(size):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSans.ttf"), size)


def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def wrap(draw, s, font, max_w):
    """Greedy wrap into lines <= max_w."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_size(draw, s, path, max_size, min_size, max_w):
    """Largest font size (<=max_size, >=min_size) making s fit on one line."""
    for sz in range(max_size, min_size - 1, -1):
        f = ImageFont.truetype(path, sz)
        if text_w(draw, s, f) <= max_w:
            return f
    return ImageFont.truetype(path, min_size)


def chip(draw, x, y, label, fill):
    """Pill chip, right edge anchored at x. Returns left edge."""
    f = f_bold(8)
    tw = text_w(draw, label, f)
    w = int(tw) + 10
    h = 12
    draw.rounded_rectangle([x - w, y, x, y + h], radius=6, fill=fill)
    draw.text((x - w + 5, y + 1), label, font=f, fill=(255, 255, 255))
    return x - w


def draw_pin(draw, x, y, n):
    r = 9
    draw.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=2)
    f = f_bold(9)
    t = str(n)
    draw.text((x - text_w(draw, t, f) / 2, y - 6), t, font=f, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.text((8, 6), "THE WORLD TODAY", font=f_serif(44), fill=INK)
    d.text((1016, 26), "MONDAY 23 NOVEMBER 2026", font=f_bold(15),
           fill=GOLD, anchor="ra")
    d.rectangle([8, 60, 1016, 63], fill=GOLD)

    # ---------- kicker ----------
    d.rectangle([8, 66, 1016, 86], fill=RED)
    kick = ("AI rout hits Asia   \u00b7   UN chief urges AI rules   \u00b7   "
            "US lead over China at record low   \u00b7   Anthropic IPO $107.3B")
    d.text((512, 71), kick, font=f_bold(12), fill=(255, 255, 255), anchor="ma")

    # ---------- number strip (2 rows x 5) ----------
    strip = [
        [("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"),
         ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
         ("2%", "BILLIONAIRE TAX IN PARIS")],
        [("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
         ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
         ("$107.3B", "ANTHROPIC IPO")],
    ]
    col_w = 1008 / 5
    for r, row in enumerate(strip):
        y0 = 88 + r * 31
        for i, (val, lab) in enumerate(row):
            cx = 8 + i * col_w
            d.text((cx, y0), val, font=f_bold(20), fill=INK)
            d.text((cx, y0 + 21), lab, font=f_bold(8), fill=GREY)
            if i:
                d.line([cx - 6, y0 + 2, cx - 6, y0 + 26], fill=(200, 192, 172), width=1)

    # ---------- region bar ----------
    segs = [("ASIA-PACIFIC 7", 7, NAVY), ("AMERICAS 8", 8, RED),
            ("MIDDLE EAST 6", 6, PURPLE), ("EUROPE 5", 5, TEAL),
            ("AFRICA 3", 3, GREEN), ("WORLD 2", 2, GOLD_L)]
    x = 8
    for label, n, col in segs:
        w = 1008 * n / 31
        d.rectangle([x, 152, x + w - 1, 172], fill=col)
        f = f_bold(11)
        d.text((x + w / 2, 158), label, font=f, fill=(255, 255, 255), anchor="ma")
        x += w

    # ---------- UTC strip ----------
    d.text((8, 176), "THE DAY IN UTC", font=f_bold(10), fill=INK)
    utc = ("~00:00 Kospi dives    ~05:30 Guterres opens    ~09:00 Power Index    "
           "~12:00 Paris 2% tax    ~15:00 Kyiv missiles")
    d.text((150, 176), utc, font=f_reg(10), fill=INK)
    d.text((1016, 176), "~ APPROX", font=f_reg(10), fill=GREY, anchor="ra")

    # ---------- hero scenes (3 big panels) ----------
    hx = [8, 348, 688]
    hw = 328
    hy, hh = 192, 130

    # --- scene 1: Kospi skyline + chart ---
    x0 = hx[0]
    d.rectangle([x0, hy, x0 + hw, hy + hh], fill=(16, 32, 64))
    # buildings with lit windows
    import random
    rnd = random.Random(23)
    bx = x0 + 8
    while bx < x0 + hw - 30:
        bw = rnd.randint(26, 44)
        bh = rnd.randint(46, 96)
        by = hy + hh - 22 - bh
        d.rectangle([bx, by, bx + bw, hy + hh - 22], fill=(38, 62, 110))
        for wy in range(by + 6, hy + hh - 28, 12):
            for wx in range(bx + 5, bx + bw - 5, 10):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
        bx += bw + 4
    # descending orange chart line
    pts = [(x0 + 150, hy + 62), (x0 + 185, hy + 70), (x0 + 220, hy + 66),
           (x0 + 255, hy + 78), (x0 + 290, hy + 74), (x0 + 318, hy + 88)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for p in pts:
        d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=(255, 255, 255))
    d.text((x0 + 10, hy + 6), "-3.3%", font=f_bold(34), fill=(255, 255, 255))
    d.rectangle([x0, hy + hh - 22, x0 + hw, hy + hh], fill=(10, 20, 44))
    d.text((x0 + hw / 2, hy + hh - 18),
           "KOSPI 4,708.54  \u00b7  -161 PTS  \u00b7  SAMSUNG -3.1%  \u00b7  HYNIX -2.5%",
           font=f_bold(9), fill=(255, 255, 255), anchor="ma")

    # --- scene 2: Guterres green + globe ---
    x0 = hx[1]
    d.rectangle([x0, hy, x0 + hw, hy + hh], fill=(27, 94, 32))
    d.text((x0 + 12, hy + 2), "150", font=f_bold(44), fill=(255, 214, 90))
    gold_lines = ["DELEGATES", "BACK A RISK", "FRAMEWORK"]
    gy = hy + 52
    for ln in gold_lines:
        d.text((x0 + 12, gy), ln, font=f_bold(17), fill=(255, 214, 90))
        gy += 21
    # globe, arcs masked inside its own circle
    cx, cy, r = x0 + hw - 62, hy + 58, 46
    globe = Image.new("RGB", (2 * r, 2 * r), (210, 235, 200))
    gd = ImageDraw.Draw(globe)
    gd.ellipse([4, 4, 2 * r - 4, 2 * r - 4], outline=(120, 170, 120), width=2)
    for k in range(-2, 3):
        gd.arc([4 + k * 18, 4, 2 * r - 4 - k * 18, 2 * r - 4],
               0, 360, fill=(120, 170, 120), width=2)
    gd.line([4, r, 2 * r - 4, r], fill=(120, 170, 120), width=2)
    mask = Image.new("L", (2 * r, 2 * r), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, 2 * r, 2 * r], fill=255)
    img.paste(globe, (cx - r, cy - r), mask)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.rectangle([x0, hy + hh - 22, x0 + hw, hy + hh], fill=(18, 66, 22))
    d.text((x0 + hw / 2, hy + hh - 18), "BRIDGETOWN SUMMIT, BARBADOS",
           font=f_bold(9), fill=(255, 255, 255), anchor="ma")

    # --- scene 3: Power Index bars ---
    x0 = hx[2]
    d.rectangle([x0, hy, x0 + hw, hy + hh], fill=(250, 246, 236))
    d.text((x0 + 10, hy + 6), "NARROWEST SINCE 2018", font=f_bold(12), fill=INK)
    d.text((x0 + hw - 10, hy + 6), "GAP 5.3", font=f_bold(12), fill=RED, anchor="ra")
    bars = [("78.9", "US", NAVY, 0.90), ("73.6", "CHINA", RED, 0.84),
            ("40.5", "INDIA", GOLD_L, 0.46)]
    by = hy + 34
    for val, name, col, frac in bars:
        d.text((x0 + 10, by), val, font=f_bold(13), fill=INK)
        bw = int(200 * frac)
        d.rectangle([x0 + 62, by + 2, x0 + 62 + bw, by + 16], fill=col)
        f = f_bold(10)
        d.text((x0 + 62 + bw - 5, by + 3), name, font=f, fill=(255, 255, 255),
               anchor="ra")
        by += 26
    d.text((x0 + 10, hy + hh - 20), "ASIA POWER INDEX 2026  \u00b7  LOWY INSTITUTE",
           font=f_bold(9), fill=GREY)

    # ---------- hero headlines + bodies ----------
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. "
         "Samsung -3.1%, SK Hynix -2.5%.",
         "KOREA EXCHANGE"),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; "
         "150 back a risk framework.",
         "UNITED NATIONS"),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, "
         "narrowest since 2018. India third at 40.5.",
         "LOWY INSTITUTE"),
    ]
    for i, (head, body, src) in enumerate(heroes):
        x0 = hx[i]
        lines = wrap(d, head, f_bold(18), hw)
        y = 322 if len(lines) > 1 else 330
        for ln in lines[:2]:
            d.text((x0, y), ln, font=f_bold(18), fill=INK)
            y += 21
        blines = wrap(d, body, f_reg(10), hw)
        y = 364
        for ln in blines[:2]:
            d.text((x0, y), ln, font=f_reg(10), fill=INK)
            y += 12
        d.text((x0, 388), src, font=f_bold(8), fill=GREY)
        chip(d, x0 + hw, 386, "REPORTED", NAVY)

    # ---------- MORE OF THE DAY bar ----------
    d.rectangle([8, 400, 1016, 420], fill=INK)
    d.text((8, 405), "MORE OF THE DAY  \u2014  10 STORIES", font=f_bold(12),
           fill=(255, 255, 255))

    # ---------- 10 cards ----------
    cards = [
        ("1", "AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.",
         "WSJ", "REPORTED", NAVY),
        ("2", "AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.",
         "AP", "REPORTED", NAVY),
        ("3", "WHITE HOUSE", "IRAN STRIKES MAY RESUME", "May resume in New Year.",
         "Reuters", "REPORTED", NAVY),
        ("4", "MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.",
         "Bloomberg", "REPORTED", NAVY),
        ("5", "SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.",
         "AP", "REPORTED", NAVY),
        ("6", "SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.",
         "ESPN", "REPORTED", NAVY),
        ("7", "LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.",
         "AP", "REPORTED", NAVY),
        ("8", "TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.",
         "WSJ", "REPORTED", NAVY),
        ("9", "EUROPE", "POLAND: 3 MISSILES CROSSED", "Kyiv: 3 Kh-101s crossed.",
         "AP", "CLAIM", RED),
        ("10", "SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.",
         "Reuters", "CLAIM", RED),
    ]
    cat_col = {"AMERICAS": RED, "WHITE HOUSE": PURPLE, "MARKETS": TEAL,
               "SPORT": NAVY, "LEGAL": GREEN, "TECH": PURPLE, "EUROPE": TEAL,
               "SPACE": RED}
    cw = 201.6
    for idx, (num, cat, head, body, src, chip_lab, chip_col) in enumerate(cards):
        row, col = divmod(idx, 5)
        x0 = 8 + col * cw
        y0 = 422 + row * 67
        d.text((x0, y0 + 4), num, font=f_bold(12), fill=RED)
        d.text((x0 + 22, y0 + 5), cat, font=f_bold(10), fill=cat_col[cat])
        hf = fit_size(d, head, os.path.join(FD, "DejaVuSans-Bold.ttf"), 12, 10,
                      cw - 4)
        d.text((x0, y0 + 22), head, font=hf, fill=INK)
        d.text((x0, y0 + 40), body, font=f_reg(9), fill=INK)
        d.text((x0, y0 + 55), src, font=f_bold(8), fill=GREY)
        chip(d, x0 + cw - 6, y0 + 53, chip_lab, chip_col)

    # ---------- WHERE IT HAPPENED bar ----------
    d.rectangle([8, 558, 1016, 578], fill=INK)
    d.text((8, 563), "WHERE IT HAPPENED", font=f_bold(12), fill=(255, 255, 255))

    # ---------- map blobs ----------
    americas = [(20, 620), (60, 595), (110, 600), (140, 630), (150, 680),
                (135, 730), (110, 758), (70, 760), (35, 740), (15, 700)]
    eurasia = [(170, 620), (220, 595), (300, 600), (345, 630), (350, 680),
               (330, 730), (290, 758), (220, 755), (175, 715), (160, 670)]
    africa = [(365, 660), (400, 650), (425, 680), (420, 720), (400, 755),
              (375, 752), (360, 710)]
    for poly in (americas, eurasia, africa):
        d.polygon(poly, fill=MAPGREEN, outline=MAPEDGE)
    pins = [(1, 325, 640), (2, 80, 745), (3, 305, 668), (4, 85, 650),
            (5, 110, 680), (6, 270, 645), (7, 220, 668), (8, 195, 640),
            (9, 258, 618), (10, 215, 618), (11, 300, 705), (12, 290, 732),
            (13, 392, 720)]
    for n, px, py in pins:
        draw_pin(d, px, py, n)
    legend = ["Pins 1\u201313: 1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing  \u00b7  4 Washington",
              "5 New York  \u00b7  6 Kyiv  \u00b7  7 Paris  \u00b7  8 London  \u00b7  9 Warsaw  \u00b7  10 Manchester",
              "11 Beirut  \u00b7  12 Gaza  \u00b7  13 Khartoum"]
    ly = 800 - 30
    for ln in legend:
        d.text((8, ly), ln, font=f_reg(9), fill=INK)
        ly += 12

    # ---------- ALSO ----------
    d.text((440, 584), "ALSO ON MONDAY", font=f_bold(13), fill=INK)
    also_l = [
        "14. Paris: 100+ back 2% billionaire tax",
        "15. Manchester: 12,000 cleared",
        "16. Zelenskyy: 165 missiles in a week",
        "17. COP31: day after Antalya pact rejected",
        "18. Israel unity talks resume",
        "19. Gaza: two killed in Israeli strike",
        "20. West Bank settler attacks",
        "21. Iran war: no deal in sight",
        "22. Lebanon seizes 264 kg explosives",
    ]
    also_r = [
        "23. Bahrain: strike hits plant, 2 hurt",
        "24. Benghazi: UN demands probe [CLAIM]",
        "25. Sudan: defences down drones [CLAIM]",
        "26. DRC: fighting traps Ebola teams",
        "27. Bangladesh: Hasina jailed if she returns",
        "28. Seoul minister quits over AI exam row",
        "29. SK Telecom -7.3% as hype cools",
        "30. China eases margin rules",
        "31. Seoul readies 10T-won fund",
    ]
    for j, ln in enumerate(also_l):
        d.text((440, 606 + j * 21), ln, font=f_reg(10), fill=INK)
    for j, ln in enumerate(also_r):
        d.text((735, 606 + j * 21), ln, font=f_reg(10), fill=INK)

    # ---------- DATE CHECK ----------
    d.rectangle([8, 802, 1016, 880], outline=RED, width=2)
    d.text((16, 810),
           "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  "
           "STORIES DATED 23 NOV ONLY",
           font=f_bold(11), fill=RED)
    d.text((16, 832),
           "LEFT OUT \u2014 NOT 23 NOV: Dems reach 258 (22 Nov)  \u00b7  "
           "Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)",
           font=f_reg(10), fill=INK)
    d.text((16, 850),
           "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  "
           "ICJ Myanmar ruling (19 Nov)",
           font=f_reg(10), fill=INK)
    d.text((16, 868),
           "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  "
           "4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  "
           "WHO evacuating trapped Ebola staff",
           font=f_reg(10), fill=INK)

    # ---------- footer ----------
    d.text((8, 888),
           "Sources: Reuters  \u00b7  AP  \u00b7  Bloomberg  \u00b7  AFP  \u00b7  Yonhap  "
           "\u00b7  BBC  \u00b7  WSJ  \u00b7  ESPN  \u00b7  Lowy Institute "
           "(Asia Power Index 2026).",
           font=f_reg(9), fill=GREY)
    d.text((8, 902),
           "CHIPS: REPORTED = confirmed by wires  \u00b7  CLAIM = one side's claim, "
           "independently unconfirmed  \u00b7  ONGOING = still developing.",
           font=f_reg(9), fill=GREY)
    d.text((8, 916),
           "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn "
           "illustrations, not photographs.",
           font=f_reg(9), fill=GREY)
    d.line([8, 930, 1016, 930], fill=GOLD, width=2)
    d.text((512, 940),
           "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  "
           "\u00b7  6 regions",
           font=f_bold(11), fill=GOLD, anchor="ma")

    img.save(os.path.join(BASE, "entry.png"))
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
