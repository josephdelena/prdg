from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1000, 1000
img = Image.new("RGBA", (W, H), "#0d0d0d")
draw = ImageDraw.Draw(img)

fd = "/System/Library/Fonts/Supplemental/"
f_hero  = ImageFont.truetype(fd + "Arial Bold.ttf", 108)
f_sub   = ImageFont.truetype(fd + "Arial Bold.ttf", 36)
f_label = ImageFont.truetype(fd + "Arial.ttf", 22)
f_hl    = ImageFont.truetype(fd + "Arial Bold.ttf", 21)
f_badge = ImageFont.truetype(fd + "Arial Bold.ttf", 20)
f_eye   = ImageFont.truetype(fd + "Arial Bold.ttf", 18)

def alpha_circle(base, cx, cy, r, color):
    for i in range(r, 0, -4):
        a = int(color[3] * (1 - i/r))
        ov = Image.new("RGBA", (W, H), (0,0,0,0))
        d = ImageDraw.Draw(ov)
        d.ellipse([cx-i, cy-i, cx+i, cy+i], fill=(*color[:3], a))
        base = Image.alpha_composite(base, ov)
    return base

# Glows
img = alpha_circle(img, 160, 200, 380, (124, 58, 237, 90))
img = alpha_circle(img, 840, 800, 340, (232, 97, 26, 80))
img = alpha_circle(img, 500, 500, 200, (100, 40, 200, 30))

draw = ImageDraw.Draw(img)

# Grid
for x in range(0, W, 80):
    draw.line([(x,0),(x,H)], fill=(255,255,255,6), width=1)
for y in range(0, H, 80):
    draw.line([(0,y),(W,y)], fill=(255,255,255,6), width=1)

# Hexagon top-right
def hexagon(d, cx, cy, size, color, width=2):
    pts = []
    for i in range(6):
        a = math.radians(60*i - 30)
        pts.append((cx + size*math.cos(a), cy + size*math.sin(a)))
    d.polygon(pts, outline=color, width=width)

hexagon(draw, 860, 140, 110, (124,58,237,150), 2)
hexagon(draw, 860, 140, 65,  (232,97,26,100),  1)
hexagon(draw, 860, 140, 25,  (124,58,237,180), 1)

# Diamond bottom-left
draw.polygon([(70,860),(120,800),(170,860),(120,920)], outline=(124,58,237,160), width=2)
draw.polygon([(85,860),(120,815),(155,860),(120,905)], outline=(232,97,26,80), width=1)

# Circle accent bottom-right area
draw.ellipse([780,700,880,800], outline=(232,97,26,80), width=1)
draw.ellipse([800,720,860,780], outline=(124,58,237,60), width=1)

# Top bar
for i,alpha in enumerate([220,160,80,30]):
    draw.rectangle([60, 60+i*2, 940, 62+i*2], fill=(124,58,237,alpha))

# Eyebrow
draw.text((62, 90), "DIGITAL PRODUCT  ·  2026 EDITION", font=f_eye, fill=(124,58,237,220))

# Hero text
draw.text((60, 180), "Konten", font=f_hero, fill=(255,255,255,255))
# "Kilat" with orange
draw.text((60, 295), "Kilat", font=f_hero, fill=(232,97,26,255))

# Accent line under hero
draw.rectangle([60, 420, 460, 424], fill=(124,58,237,255))
draw.rectangle([464, 420, 620, 424], fill=(232,97,26,255))

# Sub-headline
draw.text((60, 440), "Sistem Konten AI untuk UMKM Indonesia", font=f_sub, fill=(200,200,200,230))

# Divider
draw.rectangle([60, 510, 940, 511], fill=(50,50,50,255))

# 3 Highlight components
components = [
    ("1.000+ Prompt AI", "10 Kategori Konten"),
    ("105 Template Canva", "11 Platform Digital"),
    ("E-Book Panduan", "9 Bab Lengkap"),
]
col_w = (880) // 3
for i, (title, detail) in enumerate(components):
    x = 60 + i * col_w
    # card bg
    draw.rounded_rectangle([x, 528, x+col_w-16, 650], radius=12,
        fill=(20,12,35,255), outline=(124,58,237,120), width=1)
    # number accent
    num = title.split()[0]
    rest = title[len(num)+1:]
    tw_num = draw.textlength(num, font=f_hl)
    draw.text((x+20, 548), num, font=f_hl, fill=(232,97,26,255))
    draw.text((x+20+tw_num+6, 548), rest, font=f_hl, fill=(255,255,255,230))
    draw.text((x+20, 580), detail, font=f_label, fill=(150,130,200,200))
    # small dot
    draw.ellipse([x+20, 612, x+28, 620], fill=(124,58,237,180))
    draw.text((x+34, 608), "Termasuk dalam paket", font=ImageFont.truetype(fd+"Arial.ttf",16), fill=(100,100,100,200))

# Bottom section
draw.rectangle([60, 900, 940, 902], fill=(40,40,40,255))
draw.rectangle([60, 900, 320, 902], fill=(124,58,237,255))
draw.rectangle([320, 900, 480, 902], fill=(232,97,26,255))

# Edition left
draw.text((62, 912), "Vol. 1  ·  2026 Edition", font=f_badge, fill=(80,80,80,255))

# Badge right
badge = "🇮🇩 Bahasa Indonesia"
bw = int(draw.textlength(badge, font=f_badge))
bx = W - bw - 80
draw.rounded_rectangle([bx-14, 908, bx+bw+14, 944], radius=8,
    fill=(30,15,50,255), outline=(232,97,26,200), width=1)
draw.text((bx, 916), badge, font=f_badge, fill=(255,200,100,255))

out = "/Users/menhefari/Documents/workspace/toko/brandingkit/konten_kilat_cover.png"
img.convert("RGB").save(out, "PNG")
print("Saved:", out)
