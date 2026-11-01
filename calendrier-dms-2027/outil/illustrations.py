# Illustrations de saison (SVG) : aides à domicile stylisées, aux couleurs du logo DMS
import math, random

VIOLET = "#6b2fa6"; VIOLET2 = "#7b3fbf"; JAUNE = "#f2d81c"; ORANGE = "#e89a1a"
SKINS = ["#f3c9a5", "#e8b48e", "#c98d63", "#8d5a3b", "#f0d0b5", "#a8704a"]

def defs(c1, c2, gid="g"):
    return f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'

def sun(x, y, r, col="#ffd84a"):
    rays = "".join(f'<line x1="{x+math.cos(a)*(r+8)}" y1="{y+math.sin(a)*(r+8)}" x2="{x+math.cos(a)*(r+30)}" y2="{y+math.sin(a)*(r+30)}" stroke="{col}" stroke-width="8" stroke-linecap="round"/>' for a in [i*math.pi/6 for i in range(12)])
    return f'<g>{rays}<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/></g>'

def snow(n=40, seed=1, w=720, h=300):
    random.seed(seed)
    return "".join(f'<circle cx="{random.randint(0,w)}" cy="{random.randint(0,h)}" r="{random.choice([3,4,5,6])}" fill="#fff" opacity=".9"/>' for _ in range(n))

def flower(x, y, r, petal, center=JAUNE, n=5):
    ps = "".join(f'<ellipse cx="{x+math.cos(a)*r}" cy="{y+math.sin(a)*r}" rx="{r*0.75}" ry="{r*0.55}" transform="rotate({math.degrees(a)} {x+math.cos(a)*r} {y+math.sin(a)*r})" fill="{petal}"/>' for a in [i*2*math.pi/n for i in range(n)])
    return f'<g>{ps}<circle cx="{x}" cy="{y}" r="{r*0.55}" fill="{center}"/></g>'

def leaf(x, y, s, col, rot=0):
    return f'<path transform="translate({x},{y}) rotate({rot}) scale({s})" d="M0,0 C20,-30 55,-30 70,0 C55,30 20,30 0,0 Z" fill="{col}"/>'

def hills(c1, c2):
    return f'<path d="M0,430 C150,370 300,420 450,385 C580,355 660,395 720,380 L720,520 L0,520 Z" fill="{c1}"/><path d="M0,470 C180,430 330,480 500,448 C610,428 680,460 720,450 L720,520 L0,520 Z" fill="{c2}"/>'

# --- personnage ---
def person(x, y, s=1.0, skin=SKINS[0], hair="#4a2c1a", bun=True, item="", accessory="", outfit=VIOLET):
    body = f'''
<g transform="translate({x},{y}) scale({s})">
  <path d="M-98,0 C-98,-82 -64,-134 0,-134 C64,-134 98,-82 98,0 Z" fill="{outfit}"/>
  <rect x="-15" y="-156" width="30" height="30" rx="10" fill="{skin}"/>
  <polygon points="-24,-132 0,-92 24,-132" fill="#fff"/>
  <circle cx="-52" cy="-92" r="10" fill="{JAUNE}"/><circle cx="-52" cy="-92" r="4" fill="{ORANGE}"/>
  {accessory if accessory.startswith('<!--back-->') else ''}
  <path d="M-84,-104 Q-102,-40 -46,-40" stroke="{outfit}" stroke-width="38" fill="none" stroke-linecap="round"/>
  <path d="M84,-104 Q102,-40 46,-40" stroke="{outfit}" stroke-width="38" fill="none" stroke-linecap="round"/>
  <circle cx="0" cy="-190" r="48" fill="{skin}"/>
  {'<circle cx="0" cy="-246" r="22" fill="'+hair+'"/>' if bun else ''}
  <path d="M-50,-192 C-52,-252 52,-252 50,-192 C38,-222 -38,-222 -50,-192 Z" fill="{hair}"/>
  <circle cx="-18" cy="-188" r="4" fill="#3b2a4a"/><circle cx="18" cy="-188" r="4" fill="#3b2a4a"/>
  <path d="M-17,-168 Q0,-152 17,-168" stroke="#b04a5a" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  <circle cx="-32" cy="-172" r="7" fill="#f4a6a6" opacity=".55"/><circle cx="32" cy="-172" r="7" fill="#f4a6a6" opacity=".55"/>
  {item}
  <circle cx="-44" cy="-38" r="17" fill="{skin}"/><circle cx="44" cy="-38" r="17" fill="{skin}"/>
  {accessory if not accessory.startswith('<!--back-->') else ''}
</g>'''
    return body

def it_cup():  # tasse de thé
    return '<path d="M-26,-72 L-26,-40 Q-26,-20 0,-20 Q26,-20 26,-40 L26,-72 Z" fill="#fff" stroke="#d9c9ec" stroke-width="3"/><path d="M26,-62 q18,2 0,24" stroke="#fff" stroke-width="6" fill="none"/><path d="M-10,-86 q-8,-12 0,-22 M6,-88 q-8,-12 0,-22" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/>'

def it_bouquet(cols):
    stems = "".join(f'<line x1="0" y1="-18" x2="{dx}" y2="{-82-dy}" stroke="#3f8f3f" stroke-width="5"/>' for dx, dy in [(-34, 0), (-12, 16), (12, 10), (34, 0)])
    fl = "".join(flower(dx, -88-dy, 14, c, JAUNE if c != "#fff" else ORANGE) for (dx, dy), c in zip([(-34, 0), (-12, 16), (12, 10), (34, 0)], cols))
    return f'{stems}{fl}'

def it_galette():
    return f'<circle cx="0" cy="-52" r="40" fill="#e4a64a"/><circle cx="0" cy="-52" r="30" fill="#f0c273"/><path d="M-20,-52 L-14,-72 L-4,-60 L0,-76 L4,-60 L14,-72 L20,-52 Z" fill="{JAUNE}" stroke="#c99a00" stroke-width="2"/>'

def it_basket_grapes():
    g = "".join(f'<circle cx="{dx}" cy="{dy}" r="9" fill="#5a2a82"/>' for dx, dy in [(-14,-82),(0,-86),(14,-82),(-7,-72),(7,-72),(0,-62)])
    return f'{g}<path d="M-34,-60 L34,-60 L26,-22 L-26,-22 Z" fill="#a86f3a"/><path d="M-30,-48 L30,-48 M-28,-36 L28,-36" stroke="#8a5628" stroke-width="3"/>'

def it_gift():
    return f'<rect x="-34" y="-74" width="68" height="48" rx="6" fill="{JAUNE}"/><rect x="-6" y="-74" width="12" height="48" fill="{VIOLET2}"/><rect x="-34" y="-54" width="68" height="10" fill="{VIOLET2}"/><path d="M0,-74 q-20,-22 -26,-4 M0,-74 q20,-22 26,-4" stroke="{VIOLET2}" stroke-width="6" fill="none"/>'

def it_bottle():
    return '<rect x="-14" y="-92" width="28" height="64" rx="10" fill="#a8d8f0" stroke="#fff" stroke-width="3"/><rect x="-8" y="-102" width="16" height="12" rx="3" fill="#7b3fbf"/>'

def acc_sunhat():
    return '<ellipse cx="0" cy="-222" rx="86" ry="16" fill="#e9c46a"/><path d="M-48,-224 C-48,-268 48,-268 48,-224 Z" fill="#f4d98c"/><rect x="-48" y="-232" width="96" height="8" fill="#7b3fbf"/>'

def acc_scarf(col):
    return f'<path d="M-44,-136 Q0,-112 44,-136 L40,-118 Q0,-96 -40,-118 Z" fill="{col}"/><rect x="18" y="-122" width="22" height="48" rx="8" fill="{col}"/>'

def acc_beanie(col):
    return f'<path d="M-52,-224 C-52,-282 52,-282 52,-224 Z" fill="{col}"/><rect x="-54" y="-232" width="108" height="16" rx="8" fill="#fff" opacity=".9"/><circle cx="0" cy="-282" r="10" fill="#fff"/>'

def umbrella():
    return f'<!--back--><path d="M-130,-215 C-130,-300 130,-300 130,-215 Z" fill="{VIOLET2}"/><path d="M-130,-215 q22,18 43,0 q22,18 43,0 q22,18 44,0 q21,18 43,0 q22,18 43,0" fill="{VIOLET2}"/><line x1="0" y1="-215" x2="0" y2="-40" stroke="#4a2c1a" stroke-width="6"/>'

# --- scènes ---
W, H = 720, 520
def svg(inner): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{inner}</svg>'

def scene(m):
    if m == 1:
        i = defs("#cfe3f7", "#eaf3fc") + '<rect width="720" height="520" fill="url(#g)"/>' + snow(46, 1) + hills("#fff", "#eef4fb")
        i += person(360, 520, 1.5, SKINS[0], "#4a2c1a", True, it_galette(), acc_scarf(JAUNE))
    elif m == 2:
        i = defs("#d9e8f6", "#f2f7fb") + '<rect width="720" height="520" fill="url(#g)"/>' + hills("#f4f9fc", "#e6eff7")
        for x in [90, 150, 560, 630]:
            i += f'<path d="M{x},500 q-4,-70 8,-110" stroke="#3f8f3f" stroke-width="6" fill="none"/><ellipse cx="{x+8}" cy="{385}" rx="14" ry="22" fill="#fff" stroke="#dfeaf3" stroke-width="3"/>'
        i += snow(24, 2, 720, 200)
        i += person(360, 520, 1.5, SKINS[2], "#2a1b12", False, it_cup(), acc_beanie(VIOLET2))
    elif m == 3:
        i = defs("#e9f6d6", "#fbfde9") + '<rect width="720" height="520" fill="url(#g)"/>' + hills("#bfe29a", "#9fd176")
        random.seed(3)
        for k in range(26):
            x = random.randint(40, 680); y = random.randint(40, 330)
            i += f'<circle cx="{x}" cy="{y}" r="{random.randint(9,15)}" fill="#f6dc2b"/>'
        i += person(360, 520, 1.5, SKINS[1], "#b0652a", True, it_bouquet(["#f6dc2b", "#f6dc2b", "#fff", "#f6dc2b"]), "")
    elif m == 4:
        i = defs("#d8ecfb", "#f6fbff") + '<rect width="720" height="520" fill="url(#g)"/>' + hills("#bfe29a", "#9fd176")
        random.seed(4)
        i += '<path d="M-20,120 C140,100 220,60 420,40 C560,30 640,50 740,30" stroke="#6a4a3a" stroke-width="10" fill="none"/>'
        for k in range(40):
            x = random.randint(20, 700); y = random.randint(20, 190)
            i += flower(x, y, 11, random.choice(["#f9c6d8", "#fbd9e6", "#f4a9c4"]), "#fff3a3")
        i += person(360, 520, 1.5, SKINS[4], "#7a7a7a", True, it_cup(), "")
    elif m == 5:
        i = defs("#e6f5e0", "#f7fcf4") + '<rect width="720" height="520" fill="url(#g)"/>' + hills("#a5d68b", "#86c46b")
        for x in [60, 120, 610, 665]:
            for k, dy in enumerate([0, 30, 60]):
                i += f'<circle cx="{x+k*4}" cy="{300+dy}" r="9" fill="#fff" stroke="#e5efe0" stroke-width="2"/>'
            i += f'<path d="M{x},500 q-6,-110 4,-210" stroke="#3f8f3f" stroke-width="5" fill="none"/>' + leaf(x, 470, 0.8, "#3f8f3f", -60) + leaf(x, 480, 0.7, "#58a64c", -120)
        i += person(360, 520, 1.5, SKINS[0], "#2a1b12", False, it_bouquet(["#fff", "#fff", "#fff", "#fff"]), "")
    elif m == 6:
        i = defs("#cfe9fb", "#f4fbff") + '<rect width="720" height="520" fill="url(#g)"/>' + sun(110, 100, 46) + hills("#b8e08f", "#96cf6e")
        for x, y, c in [(90, 430, "#e8446a"), (150, 455, "#f27a97"), (590, 440, "#e8446a"), (640, 462, "#f27a97"), (545, 470, "#c7284f")]:
            i += flower(x, y, 17, c, "#ffd0a0", 6)
        i += person(360, 520, 1.5, SKINS[3], "#1f1f2e", False, it_bouquet(["#e8446a", "#f27a97", "#e8446a", "#f4a9c4"]), acc_sunhat())
    elif m == 7:
        i = defs("#9fd4f5", "#e6f6ff") + '<rect width="720" height="520" fill="url(#g)"/>' + sun(620, 90, 52) + hills("#e6c84a", "#d6b230")
        for x in [70, 150, 240, 520, 600, 660]:
            y = 400 + (x % 7) * 6
            i += f'<line x1="{x}" y1="{y}" x2="{x}" y2="520" stroke="#3f8f3f" stroke-width="7"/>' + flower(x, y - 10, 24, "#f7c500", "#5a3a1a", 12)
        i += person(360, 520, 1.5, SKINS[2], "#4a2c1a", True, it_bottle(), acc_sunhat())
    elif m == 8:
        i = defs("#ffe9b8", "#fff8e4") + '<rect width="720" height="520" fill="url(#g)"/>' + sun(110, 100, 50, "#ffcf3d") + hills("#e8c25c", "#d4a93a")
        for x in range(30, 700, 38):
            i += f'<path d="M{x},520 q-6,-90 4,-170" stroke="#c99a2a" stroke-width="5" fill="none"/><ellipse cx="{x+4}" cy="345" rx="7" ry="22" fill="#e0b545" transform="rotate(8 {x+4} 345)"/>'
        i += person(360, 520, 1.5, SKINS[1], "#7a3b1a", True, it_bottle(), acc_sunhat())
    elif m == 9:
        i = defs("#fbe9c8", "#fff6e6") + '<rect width="720" height="520" fill="url(#g)"/>' + hills("#c9d77a", "#a9bf5a")
        for x, y in [(70, 150), (170, 90), (560, 120), (650, 190), (120, 260), (600, 280)]:
            i += leaf(x, y, 1.0, "#6aa84f", random.choice([-30, 20, 60]))
        for x, y in [(110, 200), (610, 230)]:
            i += "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="11" fill="#5a2a82"/>' for dx, dy in [(0,0),(14,-6),(-14,-6),(7,12),(-7,12),(0,26)])
        i += person(360, 520, 1.5, SKINS[4], "#2a1b12", False, it_basket_grapes(), "")
    elif m == 10:
        i = defs("#f7d6a8", "#fdeed5") + '<rect width="720" height="520" fill="url(#g)"/>' + hills("#d9a24a", "#b97e2c")
        random.seed(10)
        for k in range(22):
            i += leaf(random.randint(10, 680), random.randint(10, 360), random.choice([0.5, 0.7, 0.9]), random.choice(["#d9531e", "#e8a317", "#b23a1a", "#c97b1a"]), random.randint(0, 360))
        i += person(360, 520, 1.5, SKINS[0], "#b0652a", True, it_cup(), acc_scarf("#d9531e"))
    elif m == 11:
        i = defs("#cfd6e2", "#eceff5") + '<rect width="720" height="520" fill="url(#g)"/>' + hills("#b7c0cf", "#a2adbf")
        for x in [70, 170, 560, 650]:
            i += f'<rect x="{x-6}" y="300" width="12" height="160" fill="#7a6a62"/><ellipse cx="{x}" cy="280" rx="44" ry="74" fill="#9aa8b8" opacity=".8"/>'
        i += person(360, 520, 1.45, SKINS[3], "#1f1f2e", False, "", umbrella())
    else:
        i = defs("#1f2a5a", "#3b4a8a") + '<rect width="720" height="520" fill="url(#g)"/>' + snow(46, 12, 720, 420) + hills("#f4f8fd", "#e2ebf6")
        for x in [90, 630]:
            i += f'<polygon points="{x},210 {x-60},400 {x+60},400" fill="#2f7d3a"/><polygon points="{x},290 {x-80},450 {x+80},450" fill="#3a9548"/><rect x="{x-9}" y="450" width="18" height="30" fill="#6a4a3a"/>'
            i += f'<circle cx="{x-20}" cy="340" r="7" fill="{JAUNE}"/><circle cx="{x+24}" cy="390" r="7" fill="#e8446a"/><circle cx="{x}" cy="270" r="7" fill="{JAUNE}"/><polygon points="{x},190 {x-9},210 {x+9},210" fill="{JAUNE}"/>'
        i += person(360, 520, 1.5, SKINS[4], "#4a2c1a", True, it_gift(), acc_beanie("#d9323f"))
    return svg(i)

if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for m in range(1, 13):
        open(f"{out}/{m:02d}.svg", "w", encoding="utf-8").write(scene(m))
    print("12 scènes")
