import base64, calendar, datetime as dt, io, sys
from dateutil.easter import easter
from PIL import Image

SRC = sys.argv[1]; OUT = sys.argv[2]
import os
ILLUS_DIR = sys.argv[4] if len(sys.argv) > 4 else None
SAP_LOGO = sys.argv[5] if len(sys.argv) > 5 else None   # logotype officiel « Services à la personne » (NOVA)
PHOTO_DIR = sys.argv[3] if len(sys.argv) > 3 else None   # dossier contenant 01.jpg ... 12.jpg et credits.txt
PHOTOS = {}; CREDITS = {}
if PHOTO_DIR and os.path.isdir(PHOTO_DIR):
    for m in range(1, 13):
        for ext in ("jpg", "jpeg", "png", "webp"):
            p = os.path.join(PHOTO_DIR, f"{m:02d}.{ext}")
            if os.path.exists(p):
                ph = Image.open(p).convert("RGB")
                ph.thumbnail((1500, 1500))
                b = io.BytesIO(); ph.save(b, "JPEG", quality=84, optimize=True)
                PHOTOS[m] = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
                break
    cp = os.path.join(PHOTO_DIR, "credits.txt")
    if os.path.exists(cp):
        for line in open(cp, encoding="utf-8"):
            parts = [x.strip() for x in line.strip().split("|")]
            if len(parts) >= 3 and parts[0].isdigit():
                CREDITS[int(parts[0])] = " – ".join(x for x in parts[1:] if x)
YEAR = 2027

if ILLUS_DIR and os.path.isdir(ILLUS_DIR):
    for m in range(1, 13):
        p = os.path.join(ILLUS_DIR, f"{m:02d}.svg")
        if m not in PHOTOS and os.path.exists(p):
            PHOTOS[m] = "data:image/svg+xml;base64," + base64.b64encode(open(p, "rb").read()).decode()

# --- logo: crop transparent margins, resize ---
im = Image.open(SRC).convert("RGBA")
bbox = im.getbbox(); im = im.crop(bbox)
h = 1500; w = round(im.width * h / im.height)
im = im.resize((w, h), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
LOGO = base64.b64encode(buf.getvalue()).decode()
LOGO_RATIO = im.width / im.height

def sap_zone():
    if SAP_LOGO and os.path.exists(SAP_LOGO):
        im = Image.open(SAP_LOGO).convert("RGBA"); im.thumbnail((900, 500))
        bf = io.BytesIO(); im.save(bf, "PNG", optimize=True)
        return '<div class="sap"><img src="data:image/png;base64,' + base64.b64encode(bf.getvalue()).decode() + '"></div>'
    return '<div class="sap empty">Emplacement du logotype officiel<br>« Services à la personne »<br><small>à télécharger sur NOVA</small></div>'

MONTHS = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
DAYS = ["Lun","Mar","Mer","Jeu","Ven","Sam","Dim"]

pq = easter(YEAR)
holidays = {
    dt.date(YEAR,1,1): "Jour de l'an",
    pq + dt.timedelta(days=1): "Lundi de Pâques",
    dt.date(YEAR,5,1): "Fête du travail",
    dt.date(YEAR,5,8): "Victoire 1945",
    pq + dt.timedelta(days=39): "Ascension",
    pq + dt.timedelta(days=50): "Lundi de Pentecôte",
    dt.date(YEAR,7,14): "Fête nationale",
    dt.date(YEAR,8,15): "Assomption",
    dt.date(YEAR,11,1): "Toussaint",
    dt.date(YEAR,11,11): "Armistice 1918",
    dt.date(YEAR,12,25): "Noël",
}
# fête des mères: dernier dimanche de mai (sauf Pentecôte), fête des pères: 3e dimanche de juin
d = dt.date(YEAR,5,31)
while d.weekday()!=6: d -= dt.timedelta(days=1)
if d == pq + dt.timedelta(days=49): d = dt.date(YEAR,6,6)
specials = {d: "Fête des mères"}
d = dt.date(YEAR,6,1)
while d.weekday()!=6: d += dt.timedelta(days=1)
specials[d + dt.timedelta(days=14)] = "Fête des pères"
specials[dt.date(YEAR,10,6)] = "Journée nationale des aidants"

PHRASES = [
 "Vous faites grandir la confiance, un jeu après l'autre.",
 "Une maison bien tenue, c'est du bien-être que vous offrez.",
 "Chaque pli soigneusement repassé redonne du temps à ceux que vous aidez.",
 "Vous prenez soin du jardin, et de la joie de ceux qui le regardent.",
 "Un repas partagé, c'est du lien avant d'être une assiette.",
 "Vos courses du jour préservent l'autonomie de chacun.",
 "Chaque trajet accompagné, c'est un peu de liberté en plus.",
 "Un enfant accompagné, des parents rassurés : merci.",
 "Veiller sur une maison, c'est veiller sur la sérénité de ceux qui l'habitent.",
 "Une présence rassurante la nuit, c'est un sommeil plus serein.",
 "Marcher ensemble, c'est retrouver le plaisir du dehors.",
 "Merci à toute l'équipe : ensemble, on prend soin.",
]

def month_page(m):
    cal = calendar.Calendar(firstweekday=0).monthdatescalendar(YEAR, m)
    cells = []
    for dd in DAYS:
        cells.append(f'<div class="dh">{dd}</div>')
    for week in cal:
        for day in week:
            if day.month != m:
                cells.append('<div class="c empty"></div>'); continue
            cls = "c"
            if day.weekday() >= 5: cls += " we"
            lab = ""
            if day in holidays: cls += " fer"; lab = holidays[day]
            elif day in specials: cls += " spe"; lab = specials[day]
            cells.append(f'<div class="{cls}"><span class="n">{day.day}</span><span class="l">{lab}</span></div>')
    rows = len(cal)
    return f'''<section class="page month">
  <aside class="side{" has-photo" if m in PHOTOS else ""}">
    <div class="logo-card"><div class="logo"></div></div>
    <div class="mname">{MONTHS[m-1]}</div>
    <div class="year">{YEAR}</div>
    <p class="phrase">« {PHRASES[m-1]} »</p>
    {('<div class="photo" style="background-image:url(' + PHOTOS[m] + ')"></div>') if m in PHOTOS else ''}
    <div class="brand">DMS – De la Mémoire aux Soins</div>
  </aside>
  <main class="grid rows{rows}">{''.join(cells)}</main>
</section>'''

cover = f'''<section class="page cover">
  <div class="cover-left"><div class="logo big"></div></div>
  <div class="cover-right">
    <div class="kicker">Calendrier</div>
    <div class="bigyear">{YEAR}</div>
    <p class="dedic">À toutes les aides à domicile de DMS</p>
    <p class="cphrase">« Merci d'être là, chaque jour. »</p>
    {sap_zone()}
    <div class="brand light">DMS – De la Mémoire aux Soins · Sézanne</div>
  </div>
</section>'''

back = f'''<section class="page back">
  <div class="back-inner">
    <div class="logo small"></div>
    <h2>Les numéros à garder sous la main</h2>
    <div class="nums">
      <div><b>15</b><span>SAMU – urgence médicale</span></div>
      <div><b>112</b><span>Numéro d'urgence européen</span></div>
      <div><b>17</b><span>Police secours</span></div>
      <div><b>18</b><span>Pompiers</span></div>
      <div><b>3977</b><span>Signalement des maltraitances envers les personnes âgées ou handicapées</span></div>
    </div>
    <p class="note">En cas de danger, on appelle d'abord les secours, puis la responsable DMS.</p>
    {('<p class="credits">Photos : ' + ' · '.join(f"{MONTHS[k-1]} : {v}" for k, v in sorted(CREDITS.items())) + '</p>') if CREDITS else ''}
    <div class="contact">
      <b>DMS – De la Mémoire aux Soins</b><br>
      232 rue Sternberg – 51120 Sézanne<br>
      09 54 94 21 31 · 07 49 55 14 85<br>
      contact@dms-aideadomicile.com · www.dms-aideadomicile.com
    </div>
    {sap_zone()}
    <p class="legal">SASU DE LA MÉMOIRE AUX SOINS (DMS), au capital de 100 € – 232 rue Sternberg, 51120 Sézanne – SIRET 981 382 948 00017 – RCS Reims. Organisme de services à la personne déclaré sous le n° SAP981382948 (récépissé de déclaration du préfet de la Marne du 16/06/2025). Les activités illustrées sont réalisées dans le cadre de la déclaration de l'organisme, selon les modalités et les publics prévus par la loi.</p>
  </div>
</section>'''

CSS = '''
@page { size: 297mm 210mm; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
html, body { background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact }
body { font-family: "Inter", "Liberation Sans", sans-serif; color: #2b1d3d }
:root { --v: #5b2a91; --v2: #7b3fbf; --l: #efe6f8; --l2: #f7f2fb; --y: #f2d81c; --yl: #fdf4b8 }
.page { width: 297mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; break-after: page }
.logo { background-image: url(data:image/png;base64,__LOGO__); background-repeat: no-repeat; background-position: center; background-size: contain; aspect-ratio: __RATIO__ }
/* mois */
.month { display: flex }
.side { width: 92mm; height: 210mm; background: linear-gradient(170deg, var(--v) 0%, var(--v2) 100%); color: #fff; padding: 14mm 7mm 12mm; display: flex; flex-direction: column; align-items: center; text-align: center }
.logo-card { background: #fff; border-radius: 6mm; width: 46mm; height: 56mm; padding: 4mm; display: flex; align-items: center; justify-content: center; box-shadow: 0 1mm 3mm rgba(0,0,0,.25) }
.logo-card .logo { height: 100%; width: auto }
.mname { font-family: "Caladea", "Liberation Serif", serif; font-weight: 700; font-size: 34pt; line-height: 1; margin-top: 10mm }
.year { font-size: 13pt; letter-spacing: 6px; margin-top: 2mm; color: var(--y); font-weight: 600 }
.phrase { font-family: "Caladea", "Liberation Serif", serif; font-style: italic; font-size: 17pt; line-height: 1.35; margin-top: 11mm; padding: 0 2mm }
.side.has-photo .logo-card { width: 34mm; height: 42mm; padding: 3mm }
.side.has-photo .mname { font-size: 28pt; margin-top: 6mm }
.side.has-photo .phrase { font-size: 13.5pt; margin-top: 6mm }
.photo { width: 78mm; height: 56mm; border-radius: 4mm; background-size: cover; background-position: center; margin-top: 7mm; box-shadow: 0 1mm 3mm rgba(0,0,0,.3) }
.credits { font-size: 6.5pt; line-height: 1.4; color: #4a3566; margin: 0 0 6mm }
.brand { margin-top: auto; font-size: 8.5pt; letter-spacing: .5px; opacity: .85 }
.brand.light { color: #fff }
.grid { flex: 1; padding: 12mm 12mm 10mm 10mm; display: grid; grid-template-columns: repeat(7, 1fr); grid-auto-rows: 1fr; grid-template-rows: 9mm; gap: 1.2mm }
.grid.rows5 { grid-template-rows: 9mm repeat(5, 1fr) }
.grid.rows6 { grid-template-rows: 9mm repeat(6, 1fr) }
.grid.rows4 { grid-template-rows: 9mm repeat(4, 1fr) }
.dh { background: var(--v); color: #fff; font-size: 9.5pt; font-weight: 600; display: flex; align-items: center; justify-content: center; border-radius: 1.5mm; text-transform: uppercase; letter-spacing: 1px }
.c { background: var(--l2); border: .3mm solid var(--l); border-radius: 1.5mm; padding: 1.4mm 1.8mm; display: flex; flex-direction: column; min-height: 0 }
.c.empty { background: transparent; border-color: transparent }
.c.we { background: var(--l) }
.c .n { font-size: 14pt; font-weight: 700; color: var(--v); line-height: 1 }
.c .l { font-size: 7pt; line-height: 1.15; margin-top: 1mm; color: #4a3566; font-weight: 500 }
.c.fer { background: var(--yl); border-color: var(--y) }
.c.fer .n { color: #7a5a00 }
.c.spe { border-color: var(--v2); border-style: dashed }
/* couverture */
.cover { background: linear-gradient(160deg, var(--v) 0%, var(--v2) 100%); display: flex; color: #fff }
.cover-left { width: 120mm; display: flex; align-items: center; justify-content: center; padding: 14mm }
.cover-left .logo.big { background-color: #fff; border-radius: 10mm; height: 170mm; width: 100mm; background-size: 85%; box-shadow: 0 2mm 6mm rgba(0,0,0,.3); aspect-ratio: auto }
.cover-right { flex: 1; padding: 30mm 20mm 18mm 8mm; display: flex; flex-direction: column }
.kicker { font-size: 18pt; letter-spacing: 10px; text-transform: uppercase; color: var(--y); font-weight: 600 }
.bigyear { font-family: "Caladea", serif; font-weight: 700; font-size: 120pt; line-height: 1; margin-top: 4mm }
.dedic { font-size: 20pt; margin-top: 12mm; font-weight: 500 }
.cphrase { font-family: "Caladea", serif; font-style: italic; font-size: 30pt; margin-top: 16mm; line-height: 1.25; color: var(--yl) }
.cover-right .side.has-photo .logo-card { width: 34mm; height: 42mm; padding: 3mm }
.side.has-photo .mname { font-size: 28pt; margin-top: 6mm }
.side.has-photo .phrase { font-size: 13.5pt; margin-top: 6mm }
.photo { width: 78mm; height: 56mm; border-radius: 4mm; background-size: cover; background-position: center; margin-top: 7mm; box-shadow: 0 1mm 3mm rgba(0,0,0,.3) }
.credits { font-size: 6.5pt; line-height: 1.4; color: #4a3566; margin: 0 0 6mm }
.brand { margin-top: auto; font-size: 11pt }
/* dos */
.back { background: var(--l2); display: flex; align-items: center; justify-content: center }
.back-inner { width: 210mm; text-align: center }
.back .logo.small { height: 46mm; margin: 0 auto 6mm; aspect-ratio: __RATIO__ }
.back h2 { font-family: "Caladea", serif; font-size: 26pt; color: var(--v); margin-bottom: 8mm }
.nums { display: grid; grid-template-columns: repeat(5, 1fr); gap: 4mm }
.nums div { background: #fff; border: .4mm solid var(--v2); border-radius: 3mm; padding: 5mm 3mm; display: flex; flex-direction: column; gap: 2mm }
.nums b { font-size: 26pt; color: var(--v); line-height: 1 }
.nums span { font-size: 8.5pt; line-height: 1.25 }
.note { margin: 8mm 0; font-size: 11pt; font-style: italic }
.sap { width: 52mm; height: 24mm; background: #fff; border-radius: 3mm; display: flex; align-items: center; justify-content: center; margin: 5mm auto 0; padding: 2mm; overflow: hidden }
.sap img { max-width: 100%; max-height: 100% }
.sap.empty { border: .5mm dashed #9a7fc0; color: #5b2a91; font-size: 7.5pt; line-height: 1.3; text-align: center; background: transparent }
.sap.empty small { font-size: 6.5pt; opacity: .8 }
.cover-right .sap { margin: 14mm 0 0; width: 56mm; align-self: flex-start }
.cover-right .sap.empty { color: #fff; border-color: #cbb6e8 }
.legal { font-size: 7pt; line-height: 1.4; color: #4a3566; margin: 5mm auto 0; max-width: 200mm }
.contact { font-size: 10pt; line-height: 1.6; color: var(--v) }
'''
CSS = CSS.replace("__LOGO__", LOGO).replace("__RATIO__", f"{LOGO_RATIO:.4f}")
html = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Calendrier DMS {YEAR}</title><style>{CSS}</style></head><body>{cover}{"".join(month_page(m) for m in range(1,13))}{back}</body></html>'
open(OUT, "w", encoding="utf-8").write(html)
print("ok", len(html)//1024, "KB", "holidays:", sorted(holidays.items()))
