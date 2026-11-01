# Illustrations "dessin animé" des activités de services à la personne de DMS
import math, random
from illus import *

def label(txt):
    w = len(txt) * 18.5 + 84
    return f'<g><rect x="16" y="16" width="{w}" height="56" rx="28" fill="{VIOLET}" opacity=".96"/><circle cx="44" cy="44" r="10" fill="{JAUNE}"/><text x="64" y="55" font-family="Inter,Liberation Sans,sans-serif" font-size="30" font-weight="700" fill="#fff">{txt}</text></g>'

def room(wall="#fde8d2", floor="#d9a86c", window=True):
    s = f'<rect width="720" height="520" fill="{wall}"/><rect y="400" width="720" height="120" fill="{floor}"/><rect y="394" width="720" height="10" fill="#b98a4e" opacity=".5"/>'
    if window:
        s += '<rect x="560" y="90" width="120" height="150" rx="6" fill="#bfe3f7" stroke="#fff" stroke-width="10"/><line x1="620" y1="90" x2="620" y2="240" stroke="#fff" stroke-width="6"/><line x1="560" y1="165" x2="680" y2="165" stroke="#fff" stroke-width="6"/>'
    return s

def child(x, y, s, skin, hair, shirt, bag=False):
    b = f'<rect x="-52" y="-150" width="40" height="70" rx="12" fill="#e8446a"/>' if bag else ''
    return f'''<g transform="translate({x},{y}) scale({s})">{b}
  <path d="M-70,0 C-70,-66 -46,-104 0,-104 C46,-104 70,-66 70,0 Z" fill="{shirt}"/>
  <circle cx="0" cy="-150" r="52" fill="{skin}"/>
  <path d="M-54,-156 C-56,-214 56,-214 54,-156 C40,-186 -40,-186 -54,-156 Z" fill="{hair}"/>
  <circle cx="-18" cy="-150" r="5" fill="#3b2a4a"/><circle cx="18" cy="-150" r="5" fill="#3b2a4a"/>
  <path d="M-18,-128 Q0,-110 18,-128" stroke="#b04a5a" stroke-width="5" fill="none" stroke-linecap="round"/>
  <circle cx="-34" cy="-134" r="8" fill="#f4a6a6" opacity=".55"/><circle cx="34" cy="-134" r="8" fill="#f4a6a6" opacity=".55"/></g>'''

# --- accessoires (coordonnées locales de la personne) ---
def it_book():
    return '<path d="M-52,-76 L0,-64 L52,-76 L52,-30 L0,-18 L-52,-30 Z" fill="#fff" stroke="#d9c9ec" stroke-width="3"/><line x1="0" y1="-64" x2="0" y2="-18" stroke="#d9c9ec" stroke-width="3"/><circle cx="-26" cy="-50" r="10" fill="#f2d81c"/><path d="M14,-56 h28 M14,-46 h28 M14,-36 h20" stroke="#b9a3d6" stroke-width="4" stroke-linecap="round"/>'

def it_clean():
    foam = "".join(f'<circle cx="{dx}" cy="{dy}" r="{r}" fill="#fff" stroke="#cfe6f5" stroke-width="2"/>' for dx, dy, r in [(-16,-96,13),(8,-104,16),(28,-92,12),(-2,-88,10)])
    return f'{foam}<path d="M-38,-82 L38,-82 L30,-26 L-30,-26 Z" fill="#4aa3d9"/><ellipse cx="0" cy="-82" rx="38" ry="8" fill="#7cc1ea"/><path d="M-38,-82 Q0,-150 38,-82" stroke="#6b6b6b" stroke-width="4" fill="none"/>'

def it_iron():
    board = '<path d="M-130,-58 L130,-58 L110,-40 L-110,-40 Z" fill="#9fb4d6"/><line x1="-70" y1="-40" x2="-92" y2="40" stroke="#6b6b6b" stroke-width="6"/><line x1="70" y1="-40" x2="92" y2="40" stroke="#6b6b6b" stroke-width="6"/>'
    shirt = '<path d="M-90,-60 L-50,-68 L-30,-60 L-30,-44 L-90,-44 Z" fill="#fff" stroke="#d9c9ec" stroke-width="2"/>'
    iron = '<path d="M30,-56 L88,-56 Q104,-56 100,-70 L84,-82 L40,-82 Z" fill="#c9cdd6"/><rect x="48" y="-96" width="30" height="14" rx="7" fill="#e8446a"/>'
    steam = '<path d="M40,-96 q-8,-14 0,-26 M62,-102 q-8,-14 0,-26" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".85"/>'
    return board + shirt + iron + steam

def it_wcan():
    drops = "".join(f'<circle cx="{-26+dx}" cy="{-46+dy}" r="4" fill="#4aa3d9"/>' for dx, dy in [(0,0),(8,16),(-8,30),(10,44),(0,60)])
    return f'<line x1="40" y1="-60" x2="-18" y2="-102" stroke="#2f7ab3" stroke-width="9" stroke-linecap="round"/><circle cx="-22" cy="-105" r="10" fill="#2f7ab3"/><rect x="34" y="-92" width="66" height="54" rx="12" fill="#4aa3d9"/><path d="M100,-84 q26,4 0,38" stroke="#2f7ab3" stroke-width="8" fill="none"/>{drops}'

def it_pot():
    steam = '<path d="M-22,-102 q-9,-14 0,-28 M0,-108 q-9,-14 0,-28 M22,-102 q-9,-14 0,-28" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".9"/>'
    return f'{steam}<path d="M-52,-84 L52,-84 L46,-26 L-46,-26 Z" fill="#6b6f7c"/><rect x="-58" y="-90" width="116" height="10" rx="5" fill="#8b90a0"/><line x1="40" y1="-100" x2="76" y2="-30" stroke="#a86f3a" stroke-width="8" stroke-linecap="round"/><ellipse cx="38" cy="-104" rx="12" ry="8" fill="#a86f3a"/>'

def it_bags():
    l = '<path d="M-100,-96 L-40,-96 L-34,-26 L-96,-26 Z" fill="#c8924f"/><rect x="-88" y="-132" width="10" height="44" rx="5" fill="#e6c58a" transform="rotate(-12 -83 -110)"/><rect x="-70" y="-136" width="10" height="44" rx="5" fill="#e6c58a" transform="rotate(10 -65 -114)"/>'
    r = '<path d="M40,-96 L100,-96 L94,-26 L34,-26 Z" fill="#e0b070"/><path d="M52,-96 q-6,-34 2,-42 M72,-96 q0,-40 10,-46 M88,-96 q8,-30 18,-34" stroke="#3f9a3f" stroke-width="9" fill="none" stroke-linecap="round"/><circle cx="64" cy="-62" r="12" fill="#e8446a"/>'
    return l + r

def acc_crutch():
    return '<line x1="-62" y1="-104" x2="-122" y2="40" stroke="#8a8f9a" stroke-width="9" stroke-linecap="round"/><line x1="-86" y1="-58" x2="-60" y2="-48" stroke="#8a8f9a" stroke-width="8" stroke-linecap="round"/>'

def acc_blanket():
    return f'<path d="M-98,-30 Q0,-70 98,-30 L98,0 L-98,0 Z" fill="#f2d81c" opacity=".95"/><path d="M-98,-30 Q0,-70 98,-30" stroke="#d9b800" stroke-width="5" fill="none"/>'

# --- scènes ---
def scene2(m):
    if m == 1:  # garde d'enfants
        i = room() + "".join(f'<rect x="{x}" y="{y}" width="44" height="44" rx="6" fill="{c}" stroke="#fff" stroke-width="3"/>' for x, y, c in [(330,452,"#e8446a"),(376,452,"#f2d81c"),(353,408,"#4aa3d9")])
        i += person(190, 520, 1.45, SKINS[0], "#4a2c1a", True, it_book(), "")
        i += child(500, 520, 1.1, SKINS[4], "#b0652a", "#f2d81c") + child(630, 520, 0.8, SKINS[2], "#2a1b12", "#4aa3d9")
        t = "Garde d'enfants"
    elif m == 2:  # ménage
        i = room("#e3f1fb", "#cfd8e3") + "".join(f'<path d="M{x},{y} l6,-14 l6,14 l-6,14 Z" fill="{JAUNE}"/>' for x, y in [(90,310),(140,370),(600,330),(640,390),(520,300)])
        i += person(360, 520, 1.5, SKINS[1], "#2a1b12", False, it_clean(), "")
        t = "Entretien de la maison"
    elif m == 3:  # repassage
        i = room("#f4e6f8", "#d9c4e6", False) + '<line x1="40" y1="130" x2="300" y2="130" stroke="#8a8f9a" stroke-width="8"/>' + "".join(f'<path d="M{x},134 l40,0 l8,50 l-14,6 l-4,-20 l0,60 l-30,0 l0,-60 l-4,20 l-14,-6 Z" fill="{c}"/>' for x, c in [(70,"#f2d81c"),(150,"#4aa3d9"),(230,"#e8446a")])
        i += person(360, 520, 1.35, SKINS[3], "#1f1f2e", False, it_iron(), "")
        t = "Repassage"
    elif m == 4:  # jardinage
        i = f'<rect width="720" height="520" fill="#cfe9fb"/>' + sun(620, 90, 44) + '<rect y="380" width="720" height="140" fill="#8fcf6a"/><rect y="340" width="720" height="60" fill="#b8e08f"/>' + "".join(f'<rect x="{x}" y="300" width="20" height="100" fill="#fff" stroke="#e5e5e5"/>' for x in range(0, 720, 60))
        for x in [80, 150, 560, 640]:
            i += f'<line x1="{x}" y1="470" x2="{x}" y2="410" stroke="#3f8f3f" stroke-width="6"/>' + flower(x, 400, 16, random.choice(["#e8446a", "#f27a97", "#f2d81c", "#ffffff"]), "#ffcf3d", 6)
        i += person(360, 520, 1.45, SKINS[4], "#7a7a7a", True, it_wcan(), acc_sunhat())
        t = "Jardinage"
    elif m == 5:  # repas
        i = room("#fdeed5", "#e3b98a") + '<rect x="0" y="330" width="720" height="70" fill="#a88b6b"/><rect x="0" y="322" width="720" height="14" fill="#c4a584"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in [(90,300,22,"#e8446a"),(140,306,18,"#e8446a"),(560,298,14,"#f08a1a"),(600,302,14,"#f08a1a"),(640,298,14,"#f08a1a")])
        i += person(360, 520, 1.45, SKINS[0], "#b0652a", True, it_pot(), "")
        t = "Préparation de repas"
    elif m == 6:  # courses
        i = '<rect width="720" height="520" fill="#d6ecfb"/><rect y="400" width="720" height="120" fill="#cdd2dc"/>' + "".join(f'<rect x="{x}" y="{y}" width="140" height="{400-y}" fill="{c}"/><polygon points="{x-8},{y} {x+70},{y-50} {x+148},{y}" fill="#b24a3a"/><rect x="{x+20}" y="{y+30}" width="34" height="46" fill="#fff"/><rect x="{x+86}" y="{y+30}" width="34" height="46" fill="#fff"/>' for x, y, c in [(20,200,"#fbe3b0"),(560,170,"#f5c9d3")])
        i += '<rect x="200" y="250" width="320" height="150" fill="#e6f3e0"/><rect x="190" y="230" width="340" height="30" fill="#2f7d3a"/><text x="360" y="254" font-family="Inter,sans-serif" font-size="22" font-weight="700" fill="#fff" text-anchor="middle">MARCHÉ</text>'
        i += person(360, 520, 1.45, SKINS[2], "#2a1b12", False, it_bags(), "")
        t = "Courses"
    elif m == 7:  # mobilité
        i = '<rect width="720" height="520" fill="#cfe9fb"/>' + sun(110, 100, 40) + '<path d="M0,360 C160,300 320,350 480,320 C600,300 680,340 720,330 L720,520 L0,520 Z" fill="#a6d98a"/><rect y="400" width="720" height="120" fill="#5a5f6e"/><line x1="0" y1="462" x2="720" y2="462" stroke="#fff" stroke-width="8" stroke-dasharray="40 30"/>'
        i += f'<path d="M110,400 L130,340 Q140,310 190,306 L320,300 Q372,260 440,260 L520,262 Q574,264 588,320 L620,330 Q650,336 650,372 L650,400 Z" fill="{VIOLET2}"/><path d="M300,300 Q354,266 430,268 L510,270 Q550,274 560,316 L300,316 Z" fill="#bfe3f7"/><line x1="426" y1="268" x2="426" y2="316" stroke="{VIOLET2}" stroke-width="8"/>'
        i += f'<circle cx="440" cy="296" r="18" fill="{SKINS[0]}"/><path d="M422,290 C424,266 458,266 458,290 C450,278 430,278 422,290 Z" fill="#4a2c1a"/><circle cx="494" cy="298" r="16" fill="{SKINS[4]}"/><path d="M478,292 C480,272 508,272 510,292 C502,282 486,282 478,292 Z" fill="#7a7a7a"/>'
        i += flower(240, 360, 20, "#f2d81c", "#e89a1a", 6) + '<circle cx="190" cy="408" r="40" fill="#2b2b36"/><circle cx="190" cy="408" r="18" fill="#c9cdd6"/><circle cx="540" cy="408" r="40" fill="#2b2b36"/><circle cx="540" cy="408" r="18" fill="#c9cdd6"/>'
        t = "Accompagnement en voiture"
    elif m == 8:  # accompagnement des enfants
        i = '<rect width="720" height="520" fill="#d6ecfb"/>' + sun(640, 90, 40) + '<rect y="410" width="720" height="110" fill="#b9bfcb"/>' + f'<rect x="60" y="200" width="260" height="210" fill="#f5c9a0"/><polygon points="40,200 190,120 340,200" fill="#b24a3a"/><rect x="160" y="320" width="60" height="90" fill="#7b3fbf"/><rect x="90" y="240" width="44" height="50" fill="#fff"/><rect x="246" y="240" width="44" height="50" fill="#fff"/><line x1="190" y1="120" x2="190" y2="70" stroke="#6b6b6b" stroke-width="5"/><rect x="190" y="70" width="46" height="28" fill="#4aa3d9"/>'
        i += person(330, 520, 1.4, SKINS[1], "#2a1b12", False, "", "") + child(540, 520, 1.15, SKINS[4], "#b0652a", "#f2d81c", True)
        t = "Trajets des enfants"
    elif m == 9:  # vigilance maison
        i = '<rect width="720" height="520" fill="#d6ecfb"/><rect y="420" width="720" height="100" fill="#9fd176"/>' + f'<rect x="170" y="90" width="380" height="330" fill="#f5e1c0"/><polygon points="140,90 360,10 580,90" fill="#b24a3a"/><rect x="310" y="280" width="100" height="140" fill="#7b3fbf"/><circle cx="396" cy="352" r="6" fill="{JAUNE}"/>'
        for x in [200, 440]:
            i += f'<rect x="{x}" y="150" width="90" height="100" fill="#bfe3f7" stroke="#fff" stroke-width="6"/><rect x="{x-34}" y="150" width="34" height="100" fill="#3f8f3f"/><rect x="{x+90}" y="150" width="34" height="100" fill="#3f8f3f"/>'
        i += "".join(flower(x, 404, 14, c, JAUNE, 6) for x, c in [(130, "#e8446a"), (600, "#f27a97"), (650, "#ffffff")])
        i += person(150, 520, 1.3, SKINS[3], "#1f1f2e", False, it_wcan(), "")
        t = "Veille sur la maison"
    elif m == 10:  # présence de nuit
        i = '<rect width="720" height="520" fill="#1f2a5a"/><rect y="410" width="720" height="110" fill="#2f3a74"/>' + '<rect x="530" y="70" width="150" height="190" rx="8" fill="#2a3a7a" stroke="#c9d3f2" stroke-width="8"/><circle cx="620" cy="130" r="34" fill="#fff6c0"/><circle cx="634" cy="122" r="28" fill="#2a3a7a"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#fff"/>' for x, y in [(560,110),(580,210),(650,200),(550,160),(660,95)])
        i +=  '<circle cx="150" cy="230" r="90" fill="#ffd84a" opacity=".25"/><circle cx="150" cy="230" r="46" fill="#ffd84a" opacity=".35"/><rect x="144" y="236" width="12" height="150" fill="#8a8f9a"/><path d="M110,236 L190,236 L170,190 L130,190 Z" fill="#ffd84a"/>'
        i += '<path d="M240,300 Q240,250 300,250 L420,250 Q480,250 480,300 L480,420 L240,420 Z" fill="#7b3fbf"/>'
        i += person(360, 520, 1.45, SKINS[0], "#4a2c1a", True, it_cup(), "")
        t = "Présence de nuit"
    elif m == 11:  # sortie accompagnée
        i = '<rect width="720" height="520" fill="#d6ecfb"/>' + sun(110, 90, 40) + '<path d="M0,380 C200,340 380,380 720,350 L720,520 L0,520 Z" fill="#a6d98a"/><path d="M-20,520 C200,430 420,470 740,400 L740,520 Z" fill="#e8d6a8"/>'
        for x in [560, 640, 90]:
            i += f'<rect x="{x-9}" y="250" width="18" height="140" fill="#7a5a3a"/><circle cx="{x}" cy="220" r="62" fill="#4a9a4a"/><circle cx="{x-30}" cy="250" r="40" fill="#5db25d"/>'
        i += person(220, 520, 1.45, SKINS[1], "#2a1b12", True, "", "") + person(500, 520, 1.45, SKINS[5], "#2a1b12", False, "", acc_crutch(), outfit="#2f7ab3")
        t = "Sorties accompagnées"
    else:  # équipe
        i = defs("#f7f2fb", "#e1d2f3") + '<rect width="720" height="520" fill="url(#g)"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".9"/>' for x, y, r, c in [(60,120,9,JAUNE),(120,200,7,"#e8446a"),(660,140,9,JAUNE),(600,220,7,"#4aa3d9"),(300,90,8,"#e8446a"),(430,80,9,JAUNE),(40,300,7,"#4aa3d9"),(690,320,8,"#e8446a")])
        i += '<path d="M360,170 C330,110 250,130 270,190 C285,230 340,250 360,280 C380,250 435,230 450,190 C470,130 390,110 360,170 Z" fill="#e8446a" transform="translate(0,-10)"/>'
        i += person(120, 520, 1.1, SKINS[3], "#1f1f2e", False, "", "") + person(600, 520, 1.1, SKINS[4], "#7a7a7a", True, "", "") + person(360, 520, 1.35, SKINS[0], "#4a2c1a", True, "", "")
        t = "Merci à l'équipe"
    return svg(f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7f2fb"/><stop offset="1" stop-color="#e1d2f3"/></linearGradient></defs>' + i.replace(defs("#f7f2fb", "#e1d2f3"), "") + label(t))

if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for m in range(1, 13):
        open(f"{out}/{m:02d}.svg", "w", encoding="utf-8").write(scene2(m))
    print("12 activités")
