#!/usr/bin/env python3
"""Remplace le bandeau « Mois – Activité » des illustrations par un bandeau « Activité » seule.
usage: retirer_mois.py dossier_planche dossier_sortie"""
import sys, os, math
import numpy as np
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
LAB = {'01':'Aide à domicile','02':'Entretien de la maison','03':'Préparation de repas à domicile','04':'Repassage',
       '05':'Courses','06':'Jardinage','10':'Garde d’enfants','11':'Mobilité accompagnée YouGoo'}
LINES = {'01':['Aide à domicile'],'02':['Entretien','de la maison'],'03':['Préparation de','repas à domicile'],'04':['Repassage'],
         '05':['Courses'],'06':['Jardinage'],'10':['Garde','d’enfants'],'11':['Mobilité accompagnée','YouGoo']}
FONT = '/usr/share/fonts/opentype/inter/Inter-BoldItalic.otf'
def comps(m):
    H, W = m.shape; lab = np.zeros((H, W), int); k = 0; res = []
    for y in range(H):
        for x in range(W):
            if m[y, x] and not lab[y, x]:
                k += 1; q = deque([(y, x)]); lab[y, x] = k; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = k; q.append((ny, nx))
                res.append(pts)
    return res
for n, label in LAB.items():
    im = Image.open(f'{src}/{n}.png').convert('RGB'); W, H = im.size; a = np.array(im).astype(int)
    r, g, b = a[...,0], a[...,1], a[...,2]
    m = (b > r+15) & (r > 45) & (r < 135) & (g < 85) & (b > 85) & (b < 190)
    m[int(H*0.40):, :] = False; m[:, int(W*0.66):] = False
    mi = Image.fromarray((m*255).astype('uint8')).filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(7))
    m = np.array(mi) > 0
    cs = [c for c in comps(m) if len(c) > 400]
    cs = [c for c in cs if min(p[0] for p in c) < H*0.2 and np.mean([p[1] for p in c]) < W*0.5]
    c = max(cs, key=len); ys = np.array([p[0] for p in c]); xs = np.array([p[1] for p in c])
    cols = {}
    for y, x in zip(ys, xs): lo, hi = cols.get(x, (y, y)); cols[x] = (min(lo, y), max(hi, y))
    hull = Image.new('L', (W, H), 0); dh = ImageDraw.Draw(hull)
    X = sorted(cols); top = np.array([cols[x][0] for x in X]); bot = np.array([cols[x][1] for x in X])
    for x in X: dh.line([(x, cols[x][0]), (x, cols[x][1])], fill=255)
    if n == '01':  # « Janvier » est au-dessus du bandeau : on l'inclut
        x0, x1 = min(X), max(X); dh.polygon([(x0, 15), (x1, 15), (x1, max(bot)), (x0, max(bot))], fill=255)
        top = np.minimum(top, 15)
    hull = hull.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(1.2))
    col = tuple(int(v) for v in np.median(a[ys, xs], axis=0))
    base = im.copy(); base.paste(Image.new('RGB', (W, H), col), mask=hull.point(lambda v: 255 if v > 90 else 0))
    # texte
    bbox = hull.point(lambda v: 255 if v > 90 else 0).getbbox(); bw, bh = bbox[2]-bbox[0], bbox[3]-bbox[1]
    slope = np.polyfit(X, (top+bot)/2, 1)[0]; ang = -math.degrees(math.atan(slope))
    lay = Image.new('RGBA', (bw*2, bh*2), (0,0,0,0)); d = ImageDraw.Draw(lay)
    lines = LINES[n]; fs = int(bh*0.6/len(lines))
    while fs > 10:
        f = ImageFont.truetype(FONT, fs)
        if max(d.textlength(l, font=f) for l in lines) <= bw*0.68: break
        fs -= 2
    f = ImageFont.truetype(FONT, fs); lh = int(fs*1.15); y0 = bh - lh*len(lines)//2
    for i, l in enumerate(lines): d.text((bw - d.textlength(l, font=f)/2, y0 + i*lh), l, font=f, fill=(255,255,255,255))
    lay = lay.rotate(ang, resample=Image.BICUBIC, center=(bw, bh))
    cx, cy = (bbox[0]+bbox[2])//2, (bbox[1]+bbox[3])//2
    base = base.convert('RGBA'); base.alpha_composite(lay, (cx-bw, cy-bh)); base.convert('RGB').save(f'{out}/{n}.png')
    print(n, 'ok', bbox, round(ang,1), fs, lines)
