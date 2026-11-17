#!/usr/bin/env python3
"""Comprueba que el sitio generado respeta TODAS las decisiones de docs/decisiones.md
(incluidas las indicaciones del PROPIETARIO del 2026-11-17, que prevalecen sobre las anteriores).
Uso: python3 tools/verificar-decisiones.py   (debe terminar en 0 fallos)"""
import collections, glob, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(BASE, "site")
fails, oks = [], 0
def ok(c, m):
    global oks
    if c: oks += 1
    else: fails.append(m)
rd = lambda p: open(os.path.join(R, p.lstrip("/")), encoding="utf-8").read()
vis = lambda h: re.sub(r"\s+", " ", re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", h, flags=re.S))

css, kit = rd("assets/site.css"), rd("assets/kit.js")
PAGES = {"es": ["/es/", "/es/sobre-mi/", "/es/trayectoria/", "/es/ideas/", "/es/contacto/"],
         "en": ["/en/", "/en/about/", "/en/experience/", "/en/insights/", "/en/contact/"]}
LEGAL = ["/es/aviso-legal/", "/es/privacidad/", "/es/terminos-y-condiciones/", "/es/cookies/", "/en/legal-notice/", "/en/privacy/", "/en/terms-and-conditions/", "/en/cookies/"]

def sections(h):
    m = re.search(r"<main.*?</main>", h, re.S).group(0)
    return re.findall(r'<section([^>]*)>', m)

# Lenguaje comercial o de «servicios» y canales de mensajería que el propietario pidió eliminar
FORBIDDEN = ["Conversemos", "Let's talk", "Let’s talk", "Útil si", "Useful if", "resolver", "trying to solve", "Invítame", "Invite me", "Pregúntamelo", "Ask me in a conversation",
             "sin compromiso", "no strings", "consultor", "asesoría", "Para quién", "Who is it for", "problemas que", "Problems I", "Entrevista, podcast", "Interview, podcast",
             "wa.me", "sms:", "href=\"tel:", "data-contact", "ContactKit", "Agenda una conversación", "Book a conversation", "Disponible para", "Available for"]

for lang, pages in PAGES.items():
    home = rd(pages[0] + "index.html"); n = pages[0]; hv = vis(home)
    # ---------- 1·2 Inicio: hero
    classes = [re.search(r'class="([^"]*)"', a).group(1) if 'class="' in a else "(sin clase)" for a in sections(home)]
    base = ["hero", "intro", "(sin clase)", "expertise", "dark", "split"]
    ok(classes in (base + ["contact"], base + ["ideas-home", "contact"]), f"{n}: orden de secciones del Home incorrecto: {classes}")
    hero = re.search(r'<section class="hero">.*?</section>', home, re.S).group(0); hh = vis(hero)
    ok(("Líder empresarial · Emprendedor · Real Estate" if lang == "es" else "Business Leader · Entrepreneur · Real Estate Executive") in hh, f"{n}: el hero debe llevar la identificación profesional del propietario")
    ok(re.search(r'class="display"', hero) and (("Construir." in hh and "Escalar. Transformar." in hh) if lang == "es" else ("Build." in hh and "Scale. Transform." in hh)), f"{n}: el hero debe conservar «Construir. Escalar. Transformar.»")
    sub = ("Ejecutivo y emprendedor con trayectoria internacional en inversión, creación de empresas y liderazgo empresarial. Especializado en el crecimiento y la transformación de compañías inmobiliarias. Actualmente al frente de eXp Realty España." if lang == "es"
           else "Executive and entrepreneur with an international background in investment, company building and business leadership. Focused on the growth and transformation of real estate companies. Currently leading eXp Realty Spain.")
    ok(sub in hh, f"{n}: el subtítulo del hero debe ser el texto del propietario")
    ok(f'<a class="btn" href="{pages[2]}">' in hero and f'<a class="ulink" href="{pages[1]}">' in hero, f"{n}: botón principal → Trayectoria y secundario → Sobre mí")
    ok(hero.index(pages[2]) < hero.index(pages[1]), f"{n}: «Conoce mi trayectoria» debe ser el botón principal (va primero)")
    ok("contacto" not in hero.lower().replace("contacto/", "") and "contact" not in re.sub(r'href="[^"]*"', "", hero).lower(), f"{n}: el contacto no debe ser la llamada principal de la portada")
    # ---------- 3 resultados + transformación eXp
    ok("+120 %" in home and ">Hauzz<" in home and "~250" in home, f"{n}: faltan los resultados +120 % · Hauzz · ~250")
    tr = ("En eXp Realty España, junto con mi equipo, hemos combinado crecimiento y rentabilidad con una transformación operativa basada en procesos, sistemas de gestión y decisiones apoyadas en datos." if lang == "es"
          else "At eXp Realty Spain, together with my team, we have combined growth and profitability with an operational transformation built on processes, management systems and data-driven decisions.")
    ok(tr in hv, f"{n}: falta la explicación visible de la transformación de eXp")
    ok(("US$250 M" if lang == "es" else "US$250M") in hv, f"{n}: la experiencia de ~US$250 M en private equity debe ser fácil de encontrar desde Inicio")
    ok(('<span class="role">Country Leader / MD</span>' in home) and ("Private Equity" in home), f"{n}: trayectoria del Home (eXp y Private Equity)")
    ok(len(re.findall(r'<a class="row" href="[^"]*#(exp|hauzz|rive|tiko|pe)"', home)) == 5, f"{n}: la trayectoria del Home debe tener 5 filas enlazadas")
    # ---------- 4 áreas de experiencia (sin servicios ni contacto por área)
    ex = re.search(r'<section class="expertise".*?</section>', home, re.S).group(0)
    ok(len(re.findall(r'class="row area-r"', ex)) == 5, f"{n}: «Áreas de experiencia» debe tener 5 áreas")
    ok("<a " not in ex and "<button" not in ex, f"{n}: las áreas son experiencia, no servicios: sin enlaces ni botones de contacto")
    for kw in (("Real estate y liderazgo inmobiliario", "Emprendimiento y escalabilidad", "Estrategia y excelencia operativa", "Tecnología, IA y transformación empresarial", "Liderazgo comercial y desarrollo de talento") if lang == "es"
               else ("Real estate and real estate leadership", "Entrepreneurship and scaling", "Strategy and operational excellence", "Technology, AI and business transformation", "Commercial leadership and talent development")):
        ok(kw in ex, f"{n}: falta el área «{kw}»")
    ok(("Áreas de experiencia" if lang == "es" else "Areas of expertise") in ex, f"{n}: título «Áreas de experiencia»")
    # ---------- 9 el 0–0, conferencias y podcasts no compiten con el posicionamiento ejecutivo
    sp = re.search(r'<section class="split">.*?</section>', home, re.S).group(0)
    ok("0–0" not in vis(sp) and "0-0" not in vis(sp), f"{n}: la filosofía «Cada día empieza 0–0» no debe estar en el Home")
    # ---------- contacto del Home: breve, después de la credibilidad
    ct = re.search(r'<section class="contact".*?</section>', home, re.S).group(0)
    ok(("Conectemos." if lang == "es" else "Let's connect.") in vis(ct) and f'href="{pages[4]}"' in ct, f"{n}: el contacto del Home es «Conectemos.» con botón a Contacto")
    ok('class="intent"' not in home, f"{n}: el Home no debe tener vías de contacto por tema")
    ok('class="contact"' in sections(home)[-1], f"{n}: el contacto va al final, después de la credibilidad")
    ok("filter:grayscale" in css and ".intro figure img" in css, "CSS: fotos en blanco y negro")
    # ---------- menú y pie en las 5 páginas
    for pg in pages:
        h = rd(pg + "index.html")
        navl = re.findall(r'<nav class="links".*?</nav>', h, re.S)[0]
        labels = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<a [^>]*>(.*?)</a>", navl, re.S)]
        exp_labels = ["Inicio", "Sobre mí", "Trayectoria", "Ideas", "Contacto"] if lang == "es" else ["Home", "About", "Experience", "Insights", "Contact"]
        ok(labels[:5] == exp_labels and len(labels) == 6, f"{pg}: el menú debe ser {exp_labels} + idioma (es {labels})")
        hrefs = re.findall(r'<a href="([^"]*)"', navl)[:5]
        ok(hrefs == pages, f"{pg}: los enlaces del menú deben ser internos y las 5 páginas ({hrefs})")
        ok("target=" not in navl.split('id="lang"')[0], f"{pg}: «Ideas» está integrado en el sitio: ningún enlace del menú abre otra pestaña")
        foot = re.search(r"<footer>.*?</footer>", h, re.S).group(0)
        ok(not re.search(r'<a [^>]*(linkedin|instagram)', foot, re.I), f"{pg}: los logos de redes NO son enlaces hasta nuevo aviso")
        ok(foot.count('role="img"') == 2, f"{pg}: el pie debe tener los 2 logos de redes (sin enlace)")
        ok(len(re.findall(r"<(span|div)[ >]", foot)) <= 6 and "<ul" not in foot, f"{pg}: el pie debe ser minimalista")
        v = vis(h)
        ok(not re.search(r"\+?\d[\d ()-]{8,}\d", v.replace("2026", "")), f"{pg}: hay un número de teléfono visible")
        ok(not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", v), f"{pg}: hay una dirección de correo visible (el correo de destino es privado)")
        ok('<script src="/assets/kit.js' in h and '<script src="/assets/qrcode.min.js' in h, f"{pg}: faltan los scripts del encabezado")
        for bad in FORBIDDEN: ok(bad not in h, f"{pg}: contiene «{bad}» (lenguaje comercial o canal eliminado por el propietario)")
    # ---------- 5 Sobre mí
    ab = rd(pages[1] + "index.html"); av = vis(ab)
    ok(ab.count("<h1") == 1 and "glance" in ab, f"{pages[1]}: About incompleta")
    ok(all(f'id="{x}"' in ab for x in ("biografia", "filosofia", "formacion", "preguntas")), f"{pages[1]}: faltan secciones de About")
    ok(("tenis de alto rendimiento" in av and "lesión" in av and "Matemáticas y Economía" in av) if lang == "es" else ("high-performance tennis" in av and "injury" in av and "Mathematics and Economics" in av), f"{pages[1]}: falta el párrafo personal (tenis, lesión, estudios)")
    ok("Pensam" in av, f"{pages[1]}: debe mencionar Pensam")
    ok(("sin una tesis inmobiliaria definida de antemano" if lang == "es" else "without a real estate thesis defined in advance") in av, f"{pages[1]}: precisión biográfica: llegó a España sin tesis inmobiliaria definida")
    ok(ab.count("<details>") <= 3 and ab.index('id="preguntas"') > ab.index('id="formacion"'), f"{pages[1]}: la FAQ debe ser breve (≤3) y estar al final")
    ok('class="areas"' not in ab and 'aud-r' not in ab, f"{pages[1]}: sin bloques de áreas/públicos tipo catálogo")
    # ---------- 6 Trayectoria
    xp = rd(pages[2] + "index.html")
    ok(xp.count('class="xp"') == 5 and xp.count('class="hl"') == 5, f"{pages[2]}: 5 etapas, cada una con su dato/conclusión profesional")
    ok(("US$250" in vis(xp)) and ("Pensam" in vis(xp)), f"{pages[2]}: private equity ~US$250 M y Pensam")
    ok(all(x in xp for x in ('id="exp"', 'id="hauzz"', 'id="rive"', 'id="tiko"', 'id="pe"')), f"{pages[2]}: etapas eXp, Hauzz, Rive/Kodit, Tiko, Private Equity")
    ok(not re.search(r"dificultades financieras|financial difficulties|deuda de la compañía", vis(xp)), f"{pages[2]}: sin explicaciones sobre problemas financieros de Tiko")
    # ---------- 7 Ideas integrado
    idx = rd(pages[3] + "index.html")
    ok(idx.count("<h1") == 1 and ("Ideas y perspectivas" if lang == "es" else "Ideas &amp; insights") in idx, f"{pages[3]}: página Ideas/Insights integrada")
    # ---------- 8 Contacto: formulario real
    co = rd(pages[4] + "index.html")
    ok('id="cform"' in co and 'action="/api/contact"' in co and 'method="post"' in co, f"{pages[4]}: debe tener un formulario real hacia /api/contact")
    for fld in ('name="name"', 'name="email"', 'name="company"', 'name="reason"', 'name="message"', 'name="consent"', 'name="website"', 'name="t"'):
        ok(fld in co, f"{pages[4]}: falta el campo {fld}")
    ok(len(re.findall(r'<option value="(negocio|alianza|inversion|medios|otro)"', co)) == 5, f"{pages[4]}: 5 motivos (oportunidad empresarial, alianza, inversión, medios/eventos, otro)")
    ok(("Enviar mensaje" if lang == "es" else "Send message") in co and "data-ok=" in co and "data-err=" in co, f"{pages[4]}: botón de envío y confirmación")
    ok(("Para oportunidades empresariales, alianzas estratégicas, nuevos proyectos, inversiones y colaboraciones profesionales." if lang == "es" else "For business opportunities, strategic partnerships, new projects, investments and professional collaborations.") in vis(co), f"{pages[4]}: texto sugerido del propietario")
    ok('/assets/form.js' in co and 'href="' + ("/es/privacidad/" if lang == "es" else "/en/privacy/") in co, f"{pages[4]}: form.js y enlace a privacidad")

# ---------- textos de llms sin lenguaje comercial
for f in ("llms.txt", "llms-full.txt"):
    tx = rd(f)
    for bad in ("Conversemos", "Útil si", "Useful if", "resolver", "trying to solve", "Problemas en los que", "wa.me"): ok(bad not in tx, f"{f}: contiene «{bad}»")
    ok("blog.joseantonioborges.com" not in tx, f"{f}: «Ideas» está integrado; no debe enlazar a un blog externo")

# ---------- Kit/encabezado: sin canales de mensajería
for bad in ("wa.me", "sms:", "tel:", "call:", "CONFIG", "agenda"): ok(bad not in kit, f"kit.js: no debe contener «{bad}» (eliminado por el propietario)")
ok("m-share" in kit and "burger" in kit and "qr-btn" in kit, "kit.js: QR de compartir / hamburguesa / botón QR")
ok("<form" not in kit, "kit.js: sin formularios")
ok(re.search(r"\.cw-box\{[^}]*background:#16264a", css) is not None and ".cw .code svg path{fill:#fff" in css and ".m-share .code svg path{fill:#fff" in css, "CSS: ventana del QR azul con QR blanco")
ok("max-width:700px" in css and "header.menu" in css, "CSS: menú móvil")

# ---------- Worker del formulario
wk = open(os.path.join(BASE, "src", "worker.js"), encoding="utf-8").read()
ok("/api/contact" in wk and "not_configured" in wk and "RESEND_API_KEY" in wk and "CONTACT_TO" in wk and "website" in wk, "src/worker.js: endpoint del formulario, antispam y correo privado por variables")
ok(not re.search(r"@gmail\.|@hotmail\.|@outlook\.", wk), "src/worker.js: el correo de destino no puede estar en el código")
wr = open(os.path.join(BASE, "wrangler.jsonc"), encoding="utf-8").read()
ok('"main": "src/worker.js"' in wr and "run_worker_first" in wr and '"directory": "./site"' in wr, "wrangler.jsonc: Worker + carpeta ./site")

# ---------- SIN IMÁGENES REPETIDAS (por idioma)
for lg in ("es", "en"):
    use = collections.defaultdict(list)
    for f in sorted(glob.glob(R + "/" + lg + "/**/index.html", recursive=True)):
        h = open(f, encoding="utf-8").read(); ks = re.findall(r'<img[^>]*src="/img/([a-z]+)-\d+\.jpg"', h)
        for k in set(ks): use[k].append(f.replace(R, ""))
        ok(len(ks) == len(set(ks)), f"{f.replace(R, '')}: foto repetida dentro de la misma página")
    for k, pgs in use.items(): ok(len(pgs) == 1, f"/{lg}/: la foto «{k}» se repite en {pgs}")

# ---------- no mezclar con la v1; diseño v2; aviso; legales; cookies
for bad in (".portrait{", ".facts{", ".fact b", ".tag{", ".cards{", ".b1{", ".cta-s"): ok(bad not in css, f"CSS: aparece un resto de la v1 ({bad})")
ok("Newsreader" in rd("/es/index.html") and "#F4F0E8" in css, "Diseño v2: serif Newsreader y papel hueso")
ok('class="note"' in rd("/es/index.html"), "Falta el aviso de maqueta")
for p in LEGAL: ok(os.path.exists(R + p + "index.html"), f"falta {p}")
for p in ("/es/privacidad/", "/en/privacy/"):
    tx = vis(rd(p + "index.html")).lower()
    ok("formulario" in tx or "form" in tx, f"{p}: la política de privacidad debe describir el formulario de contacto")
    ok("sms" not in tx and "whatsapp" not in tx, f"{p}: la política de privacidad no debe hablar de SMS ni WhatsApp")
ok(os.path.exists(R + "/assets/consent.js") and ".cb{position:fixed" in css and "bottom:0" in css.split(".cb{position:fixed")[1][:80], "Falta el aviso de cookies inferior")

print(f"{oks} comprobaciones correctas · {len(fails)} fallos")
for f in fails: print(" ✗", f)
sys.exit(1 if fails else 0)
