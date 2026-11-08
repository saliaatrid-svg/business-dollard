#!/usr/bin/env python3
"""Visuels pub Facebook 1080x1080. usage: build_pub.py logo.png out_dir [logo_sap.png]"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
logo_p, out = sys.argv[1], sys.argv[2]; sap_p = sys.argv[3] if len(sys.argv) > 3 else None
os.makedirs(out, exist_ok=True)
PL = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'calendrier-dms-2027', 'planche')
V, V2, BG = (91,42,145), (123,63,191), (247,242,251)
F = lambda n, s: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{n}.otf', s)
logo = Image.open(logo_p).convert('RGBA'); logo = logo.crop(logo.getbbox())
ads = [('annonce1_seniors', '02', 'Votre quotidien allégé', 'Entretien, repas, courses à Sézanne et alentours'),
       ('annonce2_enfants', '10', 'Un relais pour vos enfants', 'Garde à domicile dès 3 ans, trajets d’école'),
       ('annonce3_jardin', '06', 'Jardin soigné, linge repassé', 'On s’en occupe, à Sézanne et alentours')]
LEG = "DMS – organisme de services à la personne déclaré sous le n° SAP981382948"
def wrap(d, t, f, w):
    o, c = [], ''
    for x in t.split():
        if d.textlength((c+' '+x).strip(), font=f) <= w: c = (c+' '+x).strip()
        else: o.append(c); c = x
    return o + [c]
for name, n, head, sub in ads:
    im = Image.new('RGB', (1080, 1080), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1080, 14], fill=V)
    l = logo.resize((int(logo.width*150/logo.height), 150), Image.LANCZOS); im.paste(l, (40, 35), l)
    f = F('ExtraBold', 54); d.text((220, 50), head, font=f, fill=V)
    for i, t in enumerate(wrap(d, sub, F('Medium', 34), 800)): d.text((220, 125+i*42), t, font=F('Medium', 34), fill=V2)
    p = Image.open(f'{PL}/{n}.png').convert('RGB'); bw, bh = 700, 700
    s = min(bw/p.width, bh/p.height); p = p.resize((int(p.width*s), int(p.height*s)), Image.LANCZOS)
    x, y = 40, 215; d.rounded_rectangle([x-8, y-8, x+p.width+8, y+p.height+8], 24, fill='white', outline=V2, width=4); im.paste(p, (x, y))
    # colonne droite : logotype SAP
    zx, zy, zw, zh = 40+p.width+30, 215, 1080-(40+p.width+30)-40, 260
    if sap_p and os.path.exists(sap_p):
        s2 = Image.open(sap_p).convert('RGBA'); s2.thumbnail((zw, zh)); im.paste(s2, (zx, zy), s2)
    else:
        d.rounded_rectangle([zx, zy, zx+zw, zy+zh], 14, outline=(154,127,192), width=3)
        for i, t in enumerate(wrap(d, 'Logotype « Services à la personne » à insérer (fichier NOVA)', F('Medium', 24), zw-30)):
            d.text((zx+15, zy+20+i*32), t, font=F('Medium', 24), fill=V)
    for i, t in enumerate(wrap(d, 'Devis gratuit : écrivez-nous en message', F('Bold', 36), zw)): d.text((zx, 520+i*46), t, font=F('Bold', 36), fill=V)
    d.text((40, 1030), LEG, font=F('Regular', 22), fill=(74,53,102))
    im.save(f'{out}/{name}.png')
print('ok')
