# Version "manga" des illustrations : mêmes scènes, personnages et cadre façon planche de manga
import illus, illus2
from illus import VIOLET, VIOLET2, JAUNE, ORANGE, SKINS, svg

INK = "#2b1d3d"
IRIS = ["#5b3aa8", "#3a6fb5", "#6b3a1e", "#2f7d5a", "#7a3b8f"]

def _hair_hi(col):
    return {"#4a2c1a": "#7a4a2a", "#2a1b12": "#5a3a2a", "#b0652a": "#e0924a", "#7a7a7a": "#c7c7c7", "#1f1f2e": "#4a4a6a", "#7a3b1a": "#b0652a"}.get(col, "#ffffff")

def person_manga(x, y, s=1.0, skin=SKINS[0], hair="#4a2c1a", bun=True, item="", accessory="", outfit=VIOLET, chibi=False, iris=None):
    iris = iris or IRIS[(int(x) // 7) % len(IRIS)]
    hi = _hair_hi(hair)
    back = accessory if accessory.startswith("<!--back-->") else ""
    front = "" if accessory.startswith("<!--back-->") else accessory
    hs = 1.22 if chibi else 1.0
    eyes = ""
    for sx in (-1, 1):
        cx = 21 * sx
        eyes += f'''<ellipse cx="{cx}" cy="-186" rx="13.5" ry="17" fill="#fff" stroke="none"/>
<ellipse cx="{cx}" cy="-184" rx="10" ry="14.5" fill="{iris}" stroke="none"/><ellipse cx="{cx}" cy="-183" rx="5" ry="8.5" fill="#1b1030" stroke="none"/>
<circle cx="{cx-4*sx}" cy="-190" r="4.6" fill="#fff" stroke="none"/><circle cx="{cx+4*sx}" cy="-177" r="2.3" fill="#fff" stroke="none"/>
<path d="M{cx-17},-189 Q{cx},-206 {cx+17},-189" stroke="{INK}" stroke-width="4.5" fill="none" stroke-linecap="round"/>
<path d="M{cx+15*sx},-191 l{7*sx},-5" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
<path d="M{cx-14},-216 Q{cx},-224 {cx+14},-214" stroke="{hair}" stroke-width="4" fill="none" stroke-linecap="round"/>
<ellipse cx="{cx*1.42}" cy="-166" rx="9" ry="5" fill="#f08c9a" opacity=".55" stroke="none"/>
<path d="M{cx*1.42-6},-162 l4,-7 M{cx*1.42},-161 l4,-7 M{cx*1.42+6},-162 l4,-7" stroke="#e0687a" stroke-width="1.6" stroke-linecap="round" opacity=".7"/>'''
    bunsvg = f'<circle cx="0" cy="-252" r="23" fill="{hair}"/><path d="M-12,-262 q12,-8 24,0" stroke="{hi}" stroke-width="4" fill="none" opacity=".8"/><rect x="-24" y="-232" width="48" height="8" rx="4" fill="{JAUNE}"/>' if bun else ''
    return f'''
<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round">
  {back}
  <path d="M-98,0 C-98,-82 -64,-134 0,-134 C64,-134 98,-82 98,0 Z" fill="{outfit}"/>
  <path d="M-60,0 C-62,-40 -52,-84 -40,-112 M60,0 C62,-40 52,-84 40,-112" stroke="#4a1f78" stroke-width="2.5" fill="none" opacity=".55"/>
  <rect x="-15" y="-160" width="30" height="34" rx="10" fill="{skin}"/>
  <polygon points="-24,-132 0,-92 24,-132" fill="#fff"/>
  <circle cx="-52" cy="-92" r="10" fill="{JAUNE}"/><circle cx="-52" cy="-92" r="4" fill="{ORANGE}" stroke="none"/>
  <path d="M-84,-104 Q-102,-40 -46,-40" stroke="{INK}" stroke-width="43" fill="none"/>
  <path d="M-84,-104 Q-102,-40 -46,-40" stroke="{outfit}" stroke-width="36" fill="none"/>
  <path d="M84,-104 Q102,-40 46,-40" stroke="{INK}" stroke-width="43" fill="none"/>
  <path d="M84,-104 Q102,-40 46,-40" stroke="{outfit}" stroke-width="36" fill="none"/>
  <g transform="translate(0,-190) scale({hs}) translate(0,190)">
  {bunsvg}
  <path d="M-52,-196 C-58,-258 58,-258 52,-196 C50,-168 30,-146 0,-142 C-30,-146 -50,-168 -52,-196 Z" fill="{hair}" stroke="none"/>
  <path d="M-46,-198 C-46,-168 -26,-146 0,-142 C26,-146 46,-168 46,-198 C46,-236 -46,-236 -46,-198 Z" fill="{skin}"/>
  {eyes}
  <path d="M-3,-172 q3,4 6,0" stroke="#b07a5a" stroke-width="2" fill="none"/>
  <path d="M-10,-158 Q0,-148 10,-158" stroke="#b04a5a" stroke-width="3.6" fill="none"/>
  <path d="M-50,-198 C-54,-250 54,-250 50,-198 L43,-208 L34,-197 L24,-216 L11,-198 L-1,-221 L-13,-198 L-25,-216 L-35,-197 L-43,-208 Z" fill="{hair}"/>
  <path d="M-24,-228 q10,-8 22,-8 M18,-230 q8,-3 16,2" stroke="{hi}" stroke-width="5" fill="none" opacity=".75" stroke-linecap="round"/>
  </g>
  {item}
  <circle cx="-44" cy="-38" r="17" fill="{skin}"/><circle cx="44" cy="-38" r="17" fill="{skin}"/>
  {front}
</g>'''

def child_manga(x, y, s, skin, hair, shirt, bag=False):
    b = f'<rect x="{x-62*s}" y="{y-170*s}" width="{44*s}" height="{78*s}" rx="{12*s}" fill="#e8446a" stroke="{INK}" stroke-width="3"/>' if bag else ''
    return b + person_manga(x, y, s * 0.78, skin, hair, False, "", "", shirt, chibi=True)

def label_manga(txt):
    w = len(txt) * 18.5 + 56
    return f'<g transform="translate(18,18) skewX(-8)"><rect x="4" y="5" width="{w}" height="56" fill="{INK}"/><rect width="{w}" height="56" fill="#fff" stroke="{INK}" stroke-width="4"/><text x="22" y="40" font-family="Inter,Liberation Sans,sans-serif" font-size="30" font-weight="800" fill="{INK}">{txt}</text></g>'

def star(x, y, r, col="#fff"):
    return f'<path d="M{x},{y-r} Q{x+r*0.18},{y-r*0.18} {x+r},{y} Q{x+r*0.18},{y+r*0.18} {x},{y+r} Q{x-r*0.18},{y+r*0.18} {x-r},{y} Q{x-r*0.18},{y-r*0.18} {x},{y-r} Z" fill="{col}" stroke="{INK}" stroke-width="2"/>'

def decorate(svg_text):
    dots = '<pattern id="ht" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="2.6" fill="#2b1d3d"/></pattern><linearGradient id="fade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient><mask id="mk"><rect width="720" height="520" fill="url(#fade)"/></mask>'
    over = (f'<rect x="0" y="260" width="720" height="260" fill="url(#ht)" opacity=".13" mask="url(#mk)"/>'
            + star(655, 150, 22, "#fff7b0") + star(60, 260, 15, "#fff") + star(690, 300, 12, "#fff7b0")
            + f'<rect x="5" y="5" width="710" height="510" fill="none" stroke="{INK}" stroke-width="10"/>')
    return svg_text.replace("</svg>", dots + over + "</svg>")

def scene3(m):
    illus2.person = person_manga
    illus2.child = child_manga
    illus2.label = label_manga
    return decorate(illus2.scene2(m))

if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for m in range(1, 13):
        open(f"{out}/{m:02d}.svg", "w", encoding="utf-8").write(scene3(m))
    print("12 planches manga")
