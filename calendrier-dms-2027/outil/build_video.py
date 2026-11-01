#!/usr/bin/env python3
"""Video DMS 1080x1920 (~50 s). usage: build_video.py logo.png out_dir"""
import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFont
logo_p, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__)); PL = os.path.join(HERE, '..', 'planche')
W, H = 1080, 1920
BG, V, V2, Y = (247,242,251), (91,42,145), (123,63,191), (242,216,28)
F = lambda n, s: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{n}.otf', s)
logo = Image.open(logo_p).convert('RGBA'); logo = logo.crop(logo.getbbox())

def wrap(d, t, f, w):
    out, cur = [], ''
    for wd in t.split():
        if d.textlength((cur+' '+wd).strip(), font=f) <= w: cur = (cur+' '+wd).strip()
        else: out.append(cur); cur = wd
    return out + [cur]

def center(d, lines, f, y, fill, gap=1.25):
    for l in lines:
        d.text((W/2 - d.textlength(l, font=f)/2, y), l, font=f, fill=fill); y += int(f.size*gap)
    return y

def base():
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 16], fill=V); d.rectangle([0, H-16, W, H], fill=Y)
    return im, d

def put_logo(im, h, cx, y):
    l = logo.resize((int(logo.width*h/logo.height), h), Image.LANCZOS)
    im.paste(l, (int(cx-l.width/2), y), l)

scenes = []  # (png, seconds, voice text)
# intro
im, d = base(); put_logo(im, 900, W/2, 150)
center(d, ['Services à la personne'], F('Bold', 60), 1160, V)
center(d, ['à Sézanne et alentours'], F('Medium', 48), 1240, V2)
im.save(f'{out}/s00.png'); scenes.append(('s00', 5.5, "DMS, De la Mémoire aux Soins : des services à la personne à Sézanne et alentours."))

items = [('01','Aide à domicile',"Un soutien au quotidien, pour bien vivre chez soi."),
 ('02','Entretien de la maison',"Une maison nette, un quotidien plus léger."),
 ('03','Préparation de repas',"Des repas faits maison, partagés avec plaisir."),
 ('04','Repassage',"Du linge impeccable, du temps retrouvé."),
 ('05','Courses',"Vos courses faites, le frigo bien rempli."),
 ('06','Jardinage',"Un jardin soigné, le plaisir de profiter dehors."),
 ('10','Garde d’enfants',"Un moment de confiance pour vos enfants de plus de 3 ans."),
 ('11','Mobilité accompagnée YouGoo',"Vous conduire plus loin, en toute confiance.")]
for i, (n, title, voice) in enumerate(items, 1):
    im, d = base(); put_logo(im, 170, 150, 60)
    d.rounded_rectangle([60, 270, W-60, 410], 40, fill=V)
    f = F('ExtraBold', 62)
    if d.textlength(title, font=f) > W-200: f = F('ExtraBold', 50)
    d.text((W/2 - d.textlength(title, font=f)/2, 340 - f.size/2), title, font=f, fill='white')
    p = Image.open(f'{PL}/{n}.png').convert('RGB')
    bw, bh = 960, 1260; sc = min(bw/p.width, bh/p.height); p = p.resize((int(p.width*sc), int(p.height*sc)), Image.LANCZOS)
    x, y = (W-p.width)//2, 470 + (bh-p.height)//2
    d.rounded_rectangle([x-14, y-14, x+p.width+14, y+p.height+14], 30, fill='white', outline=V2, width=6)
    im.paste(p, (x, y))
    d.rounded_rectangle([W/2-140, 1800, W/2+140, 1812], 6, fill=V2)
    im.save(f'{out}/s{i:02d}.png'); scenes.append((f's{i:02d}', 4.6, voice))

# outro
im, d = base(); put_logo(im, 520, W/2, 120)
y = center(d, ['Parlons de vos besoins'], F('ExtraBold', 72), 700, V)
y = center(d, ['Un devis, une question ?'], F('Medium', 52), y+10, V2)
d.rounded_rectangle([90, y+50, W-90, y+330], 40, fill='white', outline=V, width=5)
center(d, ['09 54 94 21 31', '07 49 55 14 85'], F('Bold', 64), y+80, V, 1.3)
center(d, ['contact@dms-aideadomicile.com'], F('Medium', 40), y+245, V2)
center(d, ['www.dms-aideadomicile.com'], F('Medium', 40), y+300-0, V2) if False else None
legal = ("SASU De la Mémoire aux Soins (DMS) – 232 rue Sternberg, 51120 Sézanne – SIRET 981 382 948 00017. "
         "Organisme de services à la personne déclaré sous le n° SAP981382948. "
         "Crédit d’impôt de 50 % sur les services éligibles, selon la réglementation en vigueur.")
fl = F('Regular', 28); lines = wrap(d, legal, fl, W-180)
center(d, lines, fl, 1560, (74,53,102), 1.35)
# emplacement logotype SAP (fichier officiel NOVA à fournir)
d.rounded_rectangle([W/2-230, 1740, W/2+230, 1860], 14, outline=(154,127,192), width=3)
center(d, ['Logotype « Services à la personne »', '(à insérer – fichier NOVA)'], F('Medium', 26), 1762, V, 1.3)
im.save(f'{out}/s99.png'); scenes.append(('s99', 9.0, "Contactez-nous pour parler de vos besoins."))

# render
FPS, XF = 30, 0.6
clips = []
for name, dur, _ in scenes:
    o = f'{out}/{name}.mp4'
    zf = f"zoompan=z='1+0.04*on/({int(dur*FPS)})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(dur*FPS)}:s={W}x{H}:fps={FPS}"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',f'{out}/{name}.png','-vf',zf,'-t',str(dur),'-pix_fmt','yuv420p','-c:v','libx264','-crf','18',o],check=True)
    clips.append((o, dur))
inp = sum([['-i', c] for c, _ in clips], [])
fc, last, off = '', '[0:v]', 0
for i in range(1, len(clips)):
    off += clips[i-1][1] - XF
    fc += f'{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.2f}[v{i}];'; last = f'[v{i}]'
total = off + clips[-1][1]
fc = fc.rstrip(';')
# musique douce synthétisée (accords la mineur / do majeur, libre de droits car générée ici)
mus = f"{out}/musique.wav"
chords = [(220,261.63,329.63),(174.61,220,261.63),(261.63,329.63,392),(196,246.94,293.66)]
parts = []
for k, (a, b, c) in enumerate(chords):
    parts.append(f"sin(2*PI*{a}*t)+sin(2*PI*{b}*t)+sin(2*PI*{c}*t)")
seg = 12.5
expr = '+'.join(f"between(t,{k*seg},{(k+1)*seg})*({p})" for k, p in enumerate(parts))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i',f"aevalsrc='0.07*({expr})*(0.75+0.25*sin(2*PI*0.15*t)):s=44100:d={total:.1f}'",
  '-af',f'lowpass=f=1200,afade=t=in:d=2,afade=t=out:st={total-3:.1f}:d=3,aecho=0.8:0.7:500:0.3',mus],check=True)
final = f'{out}/DMS_presentation_familles.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error',*inp,'-i',mus,'-filter_complex',fc,'-map',last,'-map',f'{len(clips)}:a',
  '-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',final],check=True)
# script voix off + sous-titres SRT
t, srt = 0, []
def ts(s): return f"{int(s//3600):02}:{int(s%3600//60):02}:{int(s%60):02},{int(s%1*1000):03}"
for i, (n, dur, v) in enumerate(scenes, 1):
    srt.append(f"{i}\n{ts(t+0.3)} --> {ts(t+dur-0.4)}\n{v}\n"); t += dur - XF
open(f'{out}/DMS_presentation_familles.srt','w').write('\n'.join(srt))
open(f'{out}/script_voix_off.txt','w').write('\n'.join(v for _,_,v in scenes))
print('OK', final, round(total,1), 's')
