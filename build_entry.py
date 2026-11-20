#!/usr/bin/env python3
"""news-image-20261120 candidate C — "THE WORLD BY REGION".

Broadsheet front page summing up Friday 20 November 2026 in 40 stories.
All headlines/numbers are exact programmatic text; illustrations are flat
vector-style drawings made with PIL. No photos, no copied art.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 3300
CREAM = (247, 241, 227)
PAPER = (252, 248, 238)
INK = (17, 17, 17)
RED = (176, 30, 30)
NAVY = (18, 38, 66)
TEAL = (14, 94, 94)
PURPLE = (74, 42, 110)
GREY = (90, 86, 76)
LIGHT = (233, 226, 208)
GOLD = (198, 142, 32)

FD = "/usr/share/fonts/truetype/dejavu/"

def F(name, size):
    return ImageFont.truetype(FD + name, size)

NOTO = "/usr/share/fonts/truetype/noto/"
def FI(name, size):
    return ImageFont.truetype(NOTO + name, size)

SERIF = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF_R = lambda s: F("DejaVuSerif.ttf", s)
SERIF_I = lambda s: FI("NotoSerif-Italic.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
M = 64  # margin
CW = W - 2 * M  # content width 1472

def wrap(text, font, width):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) <= width:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def para(text, font, x, y, width, fill=INK, leading=None):
    if leading is None:
        leading = int(font.size * 1.32)
    for ln in wrap(text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def rule(y, fill=INK, wdt=3):
    d.line([(M, y), (W - M, y)], fill=fill, width=wdt)
    return y + wdt

def centre(text, font, y, fill=INK, x0=M, x1=W - M):
    tw = d.textlength(text, font=font)
    d.text(((x0 + x1 - tw) / 2, y), text, font=font, fill=fill)
    return y + int(font.size * 1.25)

# ---------------------------------------------------------------- masthead
y = 26
centre("T H E   W O R L D   I N   O N E   P A G E", SANS_B(24), y)
y = 62
centre("Friday 20 November 2026", SERIF(86), y)
y = 168
centre("Akvan comes ashore  ·  Trump puts Iran off to 2027  ·  A missile over Riyadh",
       SERIF_I(30), y, fill=RED)
y = 214
rule(y, wdt=4)
y = 226

# ---------------------------------------------------------------- region bar
regions = [("ASIA-PACIFIC", 18), ("EUROPE", 7), ("AMERICAS", 9),
           ("MIDEAST", 2), ("AFRICA", 2), ("OCEANIA", 2)]
d.rectangle([M, y, W - M, y + 46], fill=NAVY)
rx = M + 18
for name, n in regions:
    t = f"{name} {n}"
    d.text((rx, y + 9), t, font=SANS_B(24), fill=(255, 255, 255))
    rx += d.textlength(t, font=SANS_B(24)) + 46
    if name != "OCEANIA":
        d.text((rx - 30, y + 9), "·", font=SANS_B(24), fill=(150, 170, 200))
y += 46
y = rule(y + 10, wdt=2)

# ---------------------------------------------------------------- stats strip
y += 14
stats = [("300,000", "EVACUATED AS AKVAN LANDFALLS"),
         ("$1.8bn", "GTA VI DAY-ONE SALES"),
         ("−1,100", "DOW POINTS LOST"),
         ("16bn miles", "VOYAGER 1 FROM EARTH"),
         ("9–6", "ICJ VOTE: MYANMAR GUILTY")]
colw = CW / 5
for i, (num, lab) in enumerate(stats):
    x = M + i * colw
    d.text((x + 8, y), num, font=SERIF(38), fill=RED)
    para(lab, SANS_B(16), x + 8, y + 54, colw - 16, fill=GREY)
    if i:
        d.line([(x, y + 4), (x, y + 96)], fill=(200, 190, 165), width=2)
y += 112
y = rule(y, wdt=2)

# ---------------------------------------------------------------- lead illustrations
def ill_akvan(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 58, 86))
    # rain bands
    for i in range(9):
        d.line([(x + 30 + i * 60, y + 18), (x + 10 + i * 60, y + 70)],
               fill=(120, 170, 205), width=5)
    # cyclone spiral
    cx, cy = x + w // 2, y + h // 2 + 8
    for r in (95, 72, 50, 30):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=(255, 255, 255), width=10)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=GOLD)
    # coastline + houses
    d.polygon([(x, y + h), (x, y + h - 46), (x + w, y + h - 46), (x + w, y + h)],
              fill=(214, 196, 150))
    for hx in (x + 40, x + 130, x + 430):
        d.polygon([(hx, y + h - 46), (hx + 26, y + h - 72), (hx + 52, y + h - 46)],
                  fill=RED)
        d.rectangle([hx + 4, y + h - 46, hx + 48, y + h - 20], fill=(255, 255, 255))
    d.text((x + 210, y + h - 26), "GOPALPUR · ODISHA", font=SANS_B(18), fill=INK)

def ill_summit(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 198))
    # three flags
    fx, fy, fw, fh = x + 30, y + 22, 130, 84
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(178, 34, 52))
    for s in range(9):
        d.rectangle([fx, fy + s * 10, fx + fw, fy + s * 10 + 5], fill=(255, 255, 255))
    d.rectangle([fx, fy, fx + 52, fy + 42], fill=NAVY)
    d.rectangle([fx + 180, fy, fx + 180 + fw, fy + fh], fill=(222, 41, 16))
    for sx, sy in ((fx + 245, fy + 42), (fx + 205, fy + 28), (fx + 285, fy + 28)):
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 222, 0))
    d.rectangle([fx + 360, fy, fx + 360 + fw, fy + fh], fill=(255, 255, 255))
    d.rectangle([fx + 360, fy, fx + 360 + fw, fy + 28], fill=(255, 255, 255))
    d.rectangle([fx + 360, fy + 28, fx + 360 + fw, fy + 56], fill=(0, 57, 166))
    d.rectangle([fx + 360, fy + 56, fx + 360 + fw, fy + 84], fill=(213, 0, 50))
    # table + big 2027
    d.rectangle([x + 30, y + 128, x + w - 30, y + 150], fill=(120, 82, 40))
    d.text((x + 30, y + 166), "IRAN DECISION →", font=SERIF(28), fill=INK)
    d.text((x + 350, y + 158), "2027", font=SERIF(58), fill=RED)

def ill_riyadh(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 40))
    # stars
    for sx, sy in ((40, 30), (140, 60), (300, 24), (430, 55)):
        d.ellipse([x + sx - 3, y + sy - 3, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # skyline
    base = y + h
    for bx, bw, bh, col in ((0, 70, 120, (40, 60, 90)), (80, 60, 170, (55, 80, 115)),
                            (150, 80, 100, (40, 60, 90)), (430, 70, 150, (55, 80, 115)),
                            (510, 60, 110, (40, 60, 90))):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=col)
    # KAFD twisted tower (centre)
    d.polygon([(x + 250, base - 210), (x + 300, base - 210), (x + 330, base),
               (x + 220, base)], fill=(120, 150, 190))
    d.polygon([(x + 250, base - 210), (x + 300, base - 210), (x + 288, base - 150),
               (x + 262, base - 150)], fill=(200, 215, 235))
    for wy in range(base - 200, base - 20, 22):
        d.line([(x + 252, wy), (x + 298, wy)], fill=(60, 90, 130), width=3)
    # missile streak + burst
    d.line([(x + 90, y + 20), (x + 275, y + 120)], fill=(255, 200, 60), width=8)
    d.line([(x + 60, y + 14), (x + 275, y + 120)], fill=(255, 120, 40), width=4)
    for ang in range(0, 360, 45):
        import math
        ex = x + 275 + int(26 * math.cos(math.radians(ang)))
        ey = y + 120 + int(26 * math.sin(math.radians(ang)))
        d.line([(x + 275, y + 120), (ex, ey)], fill=(255, 170, 40), width=6)
    d.ellipse([x + 258, y + 103, x + 292, y + 137], fill=(255, 220, 90))
    d.text((x + 330, y + 16), "KAFD · RIYADH", font=SANS_B(20), fill=(255, 255, 255))

# ---------------------------------------------------------------- leads
leads = [
    ("1", NAVY, "ODISHA · CYCLONE", "Akvan comes ashore",
     "Cyclone Akvan made landfall near Gopalpur around noon, with winds of "
     "90–100 km/h gusting to 110. Some 300,000 people were evacuated and "
     "423 rescue teams deployed across Odisha.", ill_akvan),
    ("2", TEAL, "SHENZHEN · SUMMIT", "Trump puts the Iran decision off to 2027",
     "Trump, Xi and Putin held a historic three-way summit in Shenzhen and "
     "signed a joint peace declaration. Trump said he would \u201csee what "
     "happens\u201d on Iran after 1 January — the war decision waits until 2027.", ill_summit),
    ("3", PURPLE, "RIYADH · MISSILE", "A missile over Riyadh",
     "A Houthi missile struck the KAFD financial district in Riyadh, "
     "damaging a Saudi sovereign-wealth-fund tower. No casualties were "
     "reported.", ill_riyadh),
]

y += 18
centre("T H E   T H R E E   B I G   S T O R I E S", SANS_B(24), y)
y += 44
for num, band, kicker, head, body, ill in leads:
    d.rectangle([M, y, W - M, y + 44], fill=band)
    d.text((M + 16, y + 7), num, font=SERIF(30), fill=(255, 255, 255))
    d.text((M + 62, y + 9), kicker, font=SANS_B(24), fill=(255, 255, 255))
    y += 44
    ill(M, y, 580, 230)
    d.text((M + 612, y + 6), head, font=SERIF(38), fill=INK)
    para(body, SERIF_R(24), M + 612, y + 62, CW - 612, leading=33)
    y += 230
    y = rule(y + 12, fill=(200, 190, 165), wdt=2)
    y += 10

# ---------------------------------------------------------------- secondary grid
centre("T E N   M O R E   S T O R I E S", SANS_B(24), y)
y += 42
secondaries = [
    ("4", "THE HAGUE · JUSTICE", "Myanmar guilty of genocide",
     "The ICJ rules 9–6: Myanmar committed genocide against the Rohingya in 2017 — the first state ever convicted of genocide.", (30, 60, 110)),
    ("5", "GAMING · RECORD", "GTA VI banks $1.8bn on day one",
     "Day-one sales pass The Odyssey's $1.80bn global run. Peak viewers: 7.91 million.", (20, 110, 60)),
    ("6", "SPACE · NASA", "Voyager 1 crosses one light-day",
     "The 1977 probe is now 25.9bn km — 16bn miles — from Earth, NASA confirms.", (90, 50, 90)),
    ("7", "EUROPE · UKRAINE", "Europe ready for talks with Russia",
     "European leaders signal readiness to negotiate an end to the war in Ukraine.", (40, 90, 130)),
    ("8", "SEOUL · COURT", "Ex-PM Han Duck-soo cleared",
     "South Korea's top court clears the former PM in the 2024 martial-law case.", (150, 110, 30)),
    ("9", "YONGBYON · NUCLEAR", "North Korea expands enrichment",
     "The UN watchdog reports uranium enrichment is expanding at Yongbyon.", (120, 40, 40)),
    ("10", "CARACAS · DIPLOMACY", "US and Venezuela restore military ties",
     "Washington and Caracas agree to restore military cooperation.", (30, 100, 100)),
    ("11", "CRIMEA · ATTACK", "Bridge attack halts rail traffic",
     "A Ukrainian attack on the Crimean Bridge stops railway traffic across it.", (100, 80, 40)),
    ("12", "FIJI · CLIMATE", "Fiji declares national disaster",
     "Severe drought and El Niño water shortages push Fiji to declare a national disaster.", (200, 140, 30)),
    ("13", "DELHI · ROYALS", "Modi meets the Prince and Princess",
     "The Prince and Princess of Wales meet Prime Minister Modi in Delhi.", (140, 40, 110)),
]
cell_w = (CW - 24) // 2
cell_h = 150
gx, gy = M, y
for i, (num, kicker, head, body, col) in enumerate(secondaries):
    cx = M + (i % 2) * (cell_w + 24)
    cy = gy + (i // 2) * (cell_h + 14)
    d.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=PAPER, outline=(205, 195, 170), width=2)
    d.rectangle([cx, cy, cx + 92, cy + cell_h], fill=col)
    nf = SERIF(52) if len(num) == 1 else SERIF(40)
    nw = d.textlength(num, font=nf)
    d.text((cx + (92 - nw) / 2, cy + (cell_h - nf.size) / 2 - 6), num, font=nf, fill=(255, 255, 255))
    d.text((cx + 110, cy + 12), kicker, font=SANS_B(17), fill=RED)
    d.text((cx + 110, cy + 36), head, font=SERIF(25), fill=INK)
    para(body, SANS(19), cx + 110, cy + 72, cell_w - 130, leading=25)
y = gy + 5 * (cell_h + 14) - 14
y = rule(y + 14, wdt=2)

# ---------------------------------------------------------------- world map
y += 16
centre("W H E R E   I T   H A P P E N E D", SANS_B(24), y)
y += 40
map_x, map_y, map_w, map_h = M, y, CW, 270
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(214, 228, 238),
            outline=(180, 195, 210), width=2)
# rough continents (equirectangular lon/lat -> map px)
def px(lon, lat):
    return (map_x + (lon + 180) / 360 * map_w,
            map_y + (90 - lat) / 180 * map_h)
continents = [
    # North America (ordered clockwise)
    [(-168, 66), (-150, 70), (-130, 71), (-110, 68), (-90, 70), (-80, 73), (-65, 62),
     (-55, 50), (-60, 45), (-70, 42), (-75, 35), (-80, 26), (-90, 20), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-168, 66)],
    # South America
    [(-80, 10), (-70, 11), (-60, 8), (-50, 0), (-40, -5), (-35, -10), (-38, -20),
     (-48, -28), (-55, -35), (-65, -40), (-68, -50), (-72, -45), (-73, -30),
     (-75, -18), (-80, -5), (-80, 10)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 11), (48, 2),
     (40, -10), (35, -18), (32, -28), (20, -35), (15, -27), (12, -18), (9, -1),
     (9, 4), (-8, 5), (-15, 11), (-17, 15), (-17, 20), (-10, 28), (-6, 35)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 58), (28, 60), (30, 62), (30, 70), (35, 68), (40, 65), (35, 60),
     (30, 55), (25, 55), (20, 50), (15, 45), (12, 44), (8, 44), (3, 42), (0, 39),
     (-2, 37), (-9, 37), (-10, 36)],
    # Asia (stylised blob)
    [(30, 36), (40, 38), (50, 40), (60, 45), (70, 50), (80, 55), (90, 60), (100, 65),
     (110, 70), (120, 72), (140, 72), (160, 70), (170, 66), (165, 60), (160, 55),
     (150, 50), (140, 45), (135, 40), (130, 35), (127, 38), (122, 30), (115, 22),
     (108, 15), (105, 8), (100, 8), (98, 15), (92, 20), (88, 22), (80, 15),
     (77, 8), (72, 20), (66, 25), (60, 25), (55, 26), (50, 29), (44, 29), (40, 32),
     (35, 36), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -11), (137, -12), (132, -12), (126, -14),
     (122, -17), (118, -20), (113, -22)],
]
for poly in continents:
    d.polygon([px(lon, lat) for lon, lat in poly], fill=(196, 178, 140),
              outline=(150, 132, 95))
pins = [(1, 85, 20), (2, 114, 22), (3, 47, 25), (4, 97, 21), (5, -95, 38),
        (7, 4, 51), (8, 127, 37), (9, 118, 45), (10, -67, 7), (11, 34, 45),
        (12, 170, -18), (13, 77, 29)]
for num, lon, lat in pins:
    x, yy = px(lon, lat)
    x = min(max(x, map_x + 16), map_x + map_w - 16)
    d.ellipse([x - 13, yy - 13, x + 13, yy + 13], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x - 5, yy - 11), str(num), font=SANS_B(15), fill=(255, 255, 255))
# Voyager 6: off the map, in deep space
d.ellipse([map_x + map_w - 52, map_y + 18, map_x + map_w - 26, map_y + 44],
          fill=(255, 220, 90), outline=(255, 255, 255), width=2)
vlab = "6 · VOYAGER 1 — 16bn miles out, off the map"
vw = d.textlength(vlab, font=SANS_B(19))
d.text((map_x + map_w - 60 - vw, map_y + 16), vlab, font=SANS_B(19), fill=NAVY)
d.text((map_x + 12, map_y + map_h - 34),
       "Pins 1–13 mark the lead and secondary stories above. 14–40 are listed below.",
       font=SANS(19), fill=GREY)
y = map_y + map_h + 16
y = rule(y, wdt=2)

# ---------------------------------------------------------------- ALSO list
y += 16
centre("A L S O   O N   F R I D A Y   2 0   N O V E M B E R", SANS_B(24), y)
y += 40
also = [
    (14, "Markets slide: Dow −1,100, S&P −2.02%"),
    (15, "Hayabusa2 engine trouble — landing scrapped"),
    (16, "Migrant boat capsizes off Senegal"),
    (17, "COP31 final day in Antalya — $120bn goal"),
    (18, "NZ 243/5, Nicholls 113* at Basin Reserve"),
    (19, "APEC leaders meet in Shenzhen"),
    (20, "Fire at Muhammad Yunus's ancestral home"),
    (21, "Sensex +1.21% on Thursday"),
    (22, "Nifty past 25,400"),
    (23, "Trump invites Putin to the G20 in Miami"),
    (24, "US jobless claims 203,000"),
    (25, "EU–UK summit opens in Brussels"),
    (26, "India beat Malaysia in Hong Kong Open"),
    (27, "Women's Asian Hockey Trophy begins"),
    (28, "Amur falcons cross the Arabian Sea"),
    (29, "NATO assembly opens its 72nd session"),
    (30, "Argentina 0–2 Australia in the U17 Cup"),
    (31, "EU gas storage rules agreed"),
    (32, "EU methane rules — 24 months"),
    (33, "Modi pitches India at FICCI centenary"),
    (34, "COP31: India pushes climate resilience"),
    (35, "Google's Gemini 4 enters the AI race"),
    (36, "India launches its own H5N1 vaccine"),
    (37, "Pakistan PM to lead the SCO delegation"),
    (38, "Kenya's IEBC visits Nigeria"),
    (39, "Anthropic valued at a reported $1.5T"),
    (40, "Xi urges open trade, AI cooperation"),
]
col_w = (CW - 48) // 3
for i, (num, text) in enumerate(also):
    cx = M + (i % 3) * (col_w + 24)
    cy = y + (i // 3) * 31
    d.text((cx, cy), f"{num}.", font=SANS_B(19), fill=RED)
    # shrink font until the one-liner fits its column
    fs = 19
    while fs > 14 and d.textlength(text, font=SANS(fs)) > col_w - 42:
        fs -= 1
    d.text((cx + 40, cy), text, font=SANS(fs), fill=INK)
y += 9 * 31 + 10
y = rule(y, wdt=2)

# ---------------------------------------------------------------- date check + footer
y += 16
d.rectangle([M, y, W - M, y + 118], fill=(238, 230, 212), outline=RED, width=3)
d.text((M + 18, y + 10), "DATE CHECK — deliberately left out", font=SANS_B(23), fill=RED)
para("These happened on 19 November or earlier, so they are NOT in today's 40: "
     "the Van Gogh painting's record $190.4m sale (19 Nov) · Anthropic's first "
     "trades (19 Nov) · the Crimean Bridge span falling (17–18 Nov — today's "
     "rail halt is new).", SANS(20), M + 18, y + 44, CW - 36, leading=27)
y += 118
y += 16
centre("Every story here happened or was first reported on Friday 20 November 2026.",
       SERIF_I(22), y)
y += 30
centre("Sources: Reuters · AP · AFP · BBC · NASA · ICJ · BSE · NSE · APEC · COP31",
       SANS(19), y, fill=GREY)
y += 26
centre("40 stories · 6 regions · one day", SANS_B(19), y, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, "final y:", y, "canvas H:", H)
