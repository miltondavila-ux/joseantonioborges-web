#!/usr/bin/env python3
"""Genera las imágenes Open Graph (1200x630) de cada página y idioma con Chrome headless.
Salida: site/assets/og/og-<pagina>-<idioma>.jpg   (home, about, exp, contact × es, en)
Uso: python3 tools/og.py        (requiere Google Chrome y las fotos ya generadas en site/img)"""
import os, subprocess, sys, tempfile
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "assets", "og")
IMG = os.path.join(ROOT, "site", "img")
FOTOS = os.path.join(os.path.dirname(ROOT), "fotos")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# pagina -> (foto, estilo, posición del objeto, textos por idioma)
PAGES = {
 "home": ("controlas-1600.jpg", "full", "62% 28%", {
    "es": ("LÍDER EMPRESARIAL · EMPRENDEDOR · REAL ESTATE", "Construir.", "Escalar. Transformar.", "Ejecutivo y emprendedor del sector inmobiliario. Actualmente al frente de eXp Realty España."),
    "en": ("BUSINESS LEADER · ENTREPRENEUR · REAL ESTATE EXECUTIVE", "Build.", "Scale. Transform.", "Executive and entrepreneur in real estate. Currently leading eXp Realty Spain.")}),
 "about": ("barcelona-1024.jpg", "panel", "43% 50%", {
    "es": ("SOBRE MÍ", "José Antonio", "Borges.", "Ejecutivo y emprendedor del sector inmobiliario."),
    "en": ("ABOUT", "José Antonio", "Borges.", "Executive and entrepreneur in real estate.")}),
 "exp": ("@Copia de eXpcon-Barcelona2025-AJ--1068.jpg", "panel", "50% 40%", {
    "es": ("TRAYECTORIA", "Del desafío", "al resultado.", "eXp Realty España · Hauzz · Tiko · Private Equity"),
    "en": ("EXPERIENCE", "From challenge", "to outcome.", "eXp Realty Spain · Hauzz · Tiko · Private Equity")}),
 "contact": ("hero-1600.jpg", "full", "50% 31%", {
    "es": ("CONTACTO", "Conectemos.", "", "Oportunidades · Alianzas · Proyectos · Inversión"),
    "en": ("CONTACT", "Let’s connect.", "", "Opportunities · Partnerships · Projects · Investment")}),
 "ideas": ("lidera-1600.jpg", "panel", "38% 45%", {
    "es": ("IDEAS", "Ideas y", "perspectivas.", "Reflexiones desde la experiencia sobre liderazgo, real estate y negocios."),
    "en": ("INSIGHTS", "Ideas &", "insights.", "Perspectives on leadership, real estate and business.")}),
}

HTML = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300;1,6..72,400&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden;background:#0E1626}
.c{position:relative;width:1200px;height:630px;overflow:hidden;font-family:Newsreader,Georgia,serif;color:#fff;background:#0E1626}
.ph{position:absolute;background-size:cover;background-repeat:no-repeat;filter:grayscale(1) contrast(1.08) brightness(.95)}
.full .ph{inset:0;background-position:%POS%}
.panel .ph{top:0;right:0;width:610px;height:630px;background-position:%POS%;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 34%);mask-image:linear-gradient(90deg,transparent 0,#000 34%)}
.tint{position:absolute;inset:0;background:linear-gradient(100deg,#0E1626 0%,rgba(14,22,38,.94) 30%,rgba(14,22,38,.55) 62%,rgba(14,22,38,.18) 100%)}
.panel .tint{background:linear-gradient(100deg,#0E1626 0%,rgba(14,22,38,.97) 38%,rgba(14,22,38,.2) 100%)}
.glow{position:absolute;left:-180px;bottom:-260px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(61,104,180,.55),rgba(61,104,180,0) 68%)}
.vig{position:absolute;inset:0;box-shadow:inset 0 0 160px rgba(0,0,0,.55)}
.grain{position:absolute;inset:0;opacity:.09;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='200' height='200' filter='url(%23n)'/></svg>")}
.mono{position:absolute;left:72px;top:60px;display:flex;align-items:center;gap:16px;font-family:Inter,sans-serif;font-weight:600;font-size:15px;letter-spacing:.22em;text-transform:uppercase;color:#dfe5f1}
.mono i{display:inline-grid;place-items:center;width:46px;height:46px;border:1.5px solid rgba(255,255,255,.7);border-radius:50%;font:400 19px Newsreader,Georgia,serif;letter-spacing:0;font-style:normal;color:#fff}
.t{position:absolute;left:72px;top:150px;width:940px}
.eb{font-family:Inter,sans-serif;font-weight:600;font-size:17px;letter-spacing:.24em;color:#9db9ea;margin-bottom:26px;display:flex;align-items:center;gap:16px}
.eb::before{content:"";width:46px;height:2px;background:#3D68B4}
h1{font-weight:300;font-size:%FS%px;line-height:.95;letter-spacing:-.035em}
h1 em{display:block;font-style:italic;font-weight:300;color:#bcd0f2}
.sub{margin-top:30px;font-size:27px;line-height:1.35;font-weight:300;color:#dfe5f1;max-width:640px}
.ft{position:absolute;left:72px;right:72px;bottom:50px;display:flex;justify-content:space-between;align-items:flex-end;font-family:Inter,sans-serif;font-size:19px;letter-spacing:.06em;color:#c9d3e6}
.ft b{font-family:Newsreader,Georgia,serif;font-weight:400;font-size:30px;letter-spacing:-.01em;color:#fff}
.bar{position:absolute;left:0;right:0;bottom:0;height:6px;background:linear-gradient(90deg,#3D68B4,#bcd0f2)}
</style></head><body>
<div class="c %STYLE%">
 <div class="ph" style="background-image:url('file://%PHOTO%')"></div>
 <div class="tint"></div><div class="glow"></div><div class="vig"></div><div class="grain"></div>
 <div class="mono"><i>JB</i></div>
 <div class="t"><div class="eb">%EB%</div><h1>%H1%<em>%H2%</em></h1><p class="sub">%SUB%</p></div>
 <div class="ft"><b>José Antonio Borges</b><span>joseantonioborges.com</span></div>
 <div class="bar"></div>
</div></body></html>"""

def render(key, lang, tmp):
    photo, style, pos, tx = PAGES[key][0], PAGES[key][1], PAGES[key][2], PAGES[key][3][lang]
    fs = {"home": 98, "about": 112, "exp": 112, "contact": 150, "ideas": 118}[key]
    h = (HTML.replace("%POS%", pos).replace("%STYLE%", style).replace("%PHOTO%", quote(os.path.join(FOTOS, photo[1:]) if photo.startswith("@") else os.path.join(IMG, photo))).replace("%FS%", str(fs))
         .replace("%EB%", tx[0]).replace("%H1%", tx[1]).replace("%H2%", tx[2]).replace("%SUB%", tx[3]))
    html = os.path.join(tmp, f"og-{key}-{lang}.html"); png = os.path.join(tmp, f"og-{key}-{lang}.png")
    open(html, "w", encoding="utf-8").write(h)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=1200,630", "--virtual-time-budget=9000", "--allow-file-access-from-files",
                    f"--screenshot={png}", "file://" + html], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    out = os.path.join(OUT, f"og-{key}-{lang}.jpg")
    subprocess.run(["sips", "-c", "630", "1200", png, "--out", png], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", png, "--out", out], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out

if __name__ == "__main__":
    if not os.path.exists(CHROME): sys.exit("No encuentro Google Chrome")
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for key in PAGES:
            for lang in ("es", "en"):
                o = render(key, lang, tmp)
                print("OK", os.path.relpath(o, ROOT), round(os.path.getsize(o) / 1024), "KB")
