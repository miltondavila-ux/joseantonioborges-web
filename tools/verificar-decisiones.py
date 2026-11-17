#!/usr/bin/env python3
"""Comprueba que el sitio generado respeta TODAS las decisiones de docs/decisiones.md.
Uso: python3 tools/verificar-decisiones.py   (debe terminar en 0 fallos)"""
import os, re, sys

R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
fails, oks = [], 0
def ok(c, m):
    global oks
    if c: oks += 1
    else: fails.append(m)
rd = lambda p: open(os.path.join(R, p.lstrip("/")), encoding="utf-8").read()

css, kit = rd("assets/site.css"), rd("assets/kit.js")
PAGES = {"es": ["/es/", "/es/sobre-mi/", "/es/trayectoria/", "/es/contacto/"],
         "en": ["/en/", "/en/about/", "/en/experience/", "/en/contact/"]}

def sections(h):
    m = re.search(r"<main.*?</main>", h, re.S).group(0)
    return re.findall(r'<section([^>]*)>', m)

for lang, pages in PAGES.items():
    home = rd(pages[0] + "index.html")
    n = pages[0]
    # --- Home = v2 (+ agenda v3), en orden
    classes = [re.search(r'class="([^"]*)"', a).group(1) if 'class="' in a else "(sin clase)" for a in sections(home)]
    ok(classes == ["hero", "intro", "(sin clase)", "topics", "dark", "split", "contact"], f"{n}: orden de secciones del Home distinto del aprobado (v2 + «Temas»): {classes}")
    ok(home.count("data-contact") >= 14, f"{n}: el Home debe invitar a entrevistar/contactar a lo largo de la página ({home.count('data-contact')} invitaciones)")
    ok(len(re.findall(r'class="row topic"', home)) == 6, f"{n}: la sección «¿Qué estás intentando resolver?» debe tener 6 problemas")
    ok(("¿Qué estás intentando" in home) if lang == "es" else ("What are you trying" in home), f"{n}: falta el bloque de problemas que resuelve")
    ok(("Del desafío" in home) if lang == "es" else ("From challenge" in home), f"{n}: los resultados deben tener el título ejecutivo «Del desafío al resultado»")
    ok(not re.search(r"he resuelto|ya resolví|I have (already )?solved|I've solved", re.sub(r"<[^>]+>", " ", home)), f"{n}: tono defensivo: no usar «he resuelto» en títulos")
    ok(not re.search(r"<p class=\"sub\">(Lidero|I lead)", home), f"{n}: el hero no debe empezar hablando de lo que él hace")
    ok(not re.search(r"Lo aprendí|I learned it|Es la base con la que", re.sub(r"<[^>]+>", " ", home)), f"{n}: tono anecdótico en el bloque de disciplina; debe ser ejecutivo")
    lead = re.search(r'<p class="lead">(.*?)</p>', home, re.S).group(1)
    ok(not re.search(r"Hauzz|Rive|eXp|120|fundé|founded", lead), f"{n}: el texto de entrada del Home no debe listar credenciales para justificarse")
    ok('class="avail"' not in home and not re.search(r"disponible para|available for|busco|looking for", re.sub(r"<[^>]+>", " ", home), re.I), f"{n}: el sitio no debe sonar a búsqueda de trabajo («disponible para…»)")
    ok(("Entrevista, podcast o evento" in home) if lang == "es" else ("Interview, podcast or event" in home), f"{n}: falta la vía «Entrevista, podcast o evento»")
    ok('class="now"' in home and 'class="eyebrow"' in home and "display" in home, f"{n}: hero sin eyebrow/«Actualmente»/titular")
    ok(("Construir." in home) if lang == "es" else ("Build." in home), f"{n}: falta el titular Construir/Build")
    ok('id="sobre"' in home, f"{n}: falta #sobre (Enfoque)")
    ok(len(re.findall(r'<a class="row" href="[^"]*#(exp|hauzz|rive|tiko|pe)"', home)) == 5, f"{n}: la trayectoria del Home debe tener 5 filas enlazadas")
    for lab in ("Country Leader / MD", "Founder &amp; CEO", "Brokerage", "Head of Brokerage", "Senior Acquisitions Associate"):
        ok(f'<span class="role">{lab}</span>' in home, f"{n}: falta etiqueta v2 «{lab}»")
    ok(("Tiko · ES + PT" in home) and ("Private Equity · " in home), f"{n}: etiquetas Tiko/Private Equity de la v2")
    ok("Every Day Starts" not in home and "Cada día empieza" not in home, f"{n}: no debe haber enlaces a un blog que no existe en este sitio")
    ok(len(re.findall(r'class="intent"', home)) == 4, f"{n}: contacto del Home debe tener 4 vías")
    ok('class="agenda"' not in home and "Calendario pendiente" not in home and "Calendar pending" not in home, f"{n}: el bloque «Agenda una conversación» fue eliminado por pedido de Milton")
    ok("filter:grayscale" in css and ".intro figure img" in css, "CSS: fotos en blanco y negro")
    # --- Menú, pie
    for pg in pages:
        h = rd(pg + "index.html")
        navl = re.findall(r'<nav class="links".*?</nav>', h, re.S)[0]
        ok(len(re.findall(r"<a ", navl)) == 6, f"{pg}: el menú debe tener Inicio, Sobre mí, Trayectoria, Blog, Contacto + idioma")
        ok('href="https://blog.joseantonioborges.com" target="_blank" rel="noopener"' in navl and re.findall(r"<a [^>]*>(.*?)</a>", navl, re.S)[3].startswith("Blog"), f"{pg}: el menú debe tener BLOG en 4.ª posición, apuntando a https://blog.joseantonioborges.com (pestaña nueva)")
        ok(re.findall(r'<a href="([^"]*)"', navl)[0] == pages[0], f"{pg}: el primer enlace del menú debe ser Inicio/Home ({pages[0]})")
        ok(f'href="{pages[1]}"' in navl, f"{pg}: el menú no enlaza a Sobre mí/About")
        foot = re.search(r"<footer>.*?</footer>", h, re.S).group(0)
        ok(not re.search(r'<a [^>]*(linkedin|instagram)', foot, re.I), f"{pg}: los logos de redes NO deben ser enlaces")
        ok(foot.count('role="img"') == 2, f"{pg}: el pie debe tener los 2 logos de redes (sin enlace)")
        ok(len(re.findall(r"<(span|div)[ >]", foot)) <= 6 and "<ul" not in foot, f"{pg}: el pie debe ser minimalista")
        vis = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", h, flags=re.S)
        ok(not re.search(r"\+?\d[\d ()-]{8,}\d", vis.replace("2026", "")), f"{pg}: hay un número de teléfono visible")
        ok('<script src="/assets/kit.js' in h and '<script src="/assets/qrcode.min.js' in h, f"{pg}: faltan los scripts del kit")
    # About
    ab = rd(pages[1] + "index.html")
    ok(ab.count('class="row aud-r"') == 4 and 'id="para-quien"' in ab, f"{pages[1]}: About debe decir para quién es útil conversar (4 públicos)")
    ex = rd(pages[2] + "index.html")
    ok(ex.count('class="useful"') == 5, f"{pages[2]}: cada etapa debe decir en qué situación es útil ('Útil si…')")
    ok(ab.count("<h1") == 1 and 'class="faq"' in ab and 'class="areas"' in ab and "glance" in ab, f"{pages[1]}: About incompleta")
    ok('id="biografia"' in ab and 'id="filosofia"' in ab and 'id="formacion"' in ab and 'id="preguntas"' in ab, f"{pages[1]}: faltan secciones de About")

# --- SIN IMÁGENES REPETIDAS: cada foto una sola vez en todo el sitio (por idioma)
import collections, glob
for lg in ("es", "en"):
    use = collections.defaultdict(list)
    for f in sorted(glob.glob(R + "/" + lg + "/**/index.html", recursive=True)):
        h = open(f, encoding="utf-8").read()
        for k in set(re.findall(r'<img[^>]*src="/img/([a-z]+)-\d+\.jpg"', h)):
            use[k].append(f.replace(R, ""))
        for k in re.findall(r'<img[^>]*src="/img/([a-z]+)-\d+\.jpg"', h):
            pass
    # una foto no puede aparecer en dos páginas, ni dos veces en una misma página
    for k, pgs in use.items(): ok(len(pgs) == 1, f"/{lg}/: la foto «{k}» se repite en {pgs}")
    for f in sorted(glob.glob(R + "/" + lg + "/**/index.html", recursive=True)):
        h = open(f, encoding="utf-8").read(); ks = re.findall(r'<img[^>]*src="/img/([a-z]+)-\d+\.jpg"', h)
        ok(len(ks) == len(set(ks)), f"{f.replace(R, '')}: foto repetida dentro de la misma página {sorted(k for k in ks if ks.count(k) > 1)}")
# --- Kit: canales y reglas de contacto
for k in ("call:", "sms:", "wa:", "mail:", "agenda:"): ok(k in kit, f"kit.js: falta el canal {k}")
ok("phoneLabel" not in kit, "kit.js: no debe existir etiqueta con el número")
ok("m-share" in kit and "burger" in kit and "qr-btn" in kit, "kit.js: faltan QR de compartir / hamburguesa / botón QR")
ok("data-demo" in kit, "kit.js: falta la línea de datos de ejemplo")
ok("<form" not in kit, "kit.js: sin formularios")
# --- Ventana azul con QR y letras blancos
ok(re.search(r"\.cw-box\{[^}]*background:#16264a", css) is not None, "CSS: la ventana de conexión debe ser azul")
ok(".cw .code svg path{fill:#fff" in css, "CSS: los QR deben ser blancos")
ok(re.search(r"\.cw-q b\{color:#fff", css) and re.search(r"\.cw-q small\{color:#fff", css) and re.search(r"\.cw-opt\{[^}]*color:#fff", css), "CSS: las letras de la ventana deben ser blancas")
ok(".m-share .code svg path{fill:#fff" in css, "CSS: el QR del menú debe ser blanco")
# --- Móvil: el menú aparece solo bajo 700 px
ok("max-width:700px" in css and "header.menu" in css, "CSS: menú móvil")
# --- No mezclar con la v1
for bad in (".portrait{", ".facts{", ".fact b", ".tag{", ".cards{", ".b1{", ".cta-s"): ok(bad not in css, f"CSS: aparece un resto de la v1 ({bad})")
ok("Newsreader" in rd("/es/index.html") and "#F4F0E8" in css, "Diseño v2: serif Newsreader y papel hueso")
# --- Aviso de datos de ejemplo
ok('class="note"' in rd("/es/index.html"), "Falta el aviso de maqueta (restaurado de la v2)")
# --- Legales
for p in ("/es/aviso-legal/", "/es/privacidad/", "/es/terminos-y-condiciones/", "/es/cookies/", "/en/legal-notice/", "/en/privacy/", "/en/terms-and-conditions/", "/en/cookies/"): ok(os.path.exists(R + p + "index.html"), f"falta {p}")
ok(os.path.exists(R + "/assets/consent.js") and ".cb{position:fixed" in css and "bottom:0" in css.split(".cb{position:fixed")[1][:80], "Falta el aviso de cookies inferior")

print(f"{oks} comprobaciones correctas · {len(fails)} fallos")
for f in fails: print(" ✗", f)
sys.exit(1 if fails else 0)
