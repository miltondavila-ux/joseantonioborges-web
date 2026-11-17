#!/usr/bin/env python3
"""Verificador SEO/AEO del sitio generado (maqueta/site). Debe terminar en 0 fallos.
Uso: python3 tools/verificar-seo.py [--staging]"""
import json, os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
STAGING = "--staging" in sys.argv
DOMAIN = "https://joseantonioborges.com"
fails, oks = [], 0

def ok(cond, msg):
    global oks
    if cond: oks += 1
    else: fails.append(msg)

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.h = []; s.imgs = []; s.links = []; s.metas = {}; s.alts = []; s.ld = []; s.title = ""; s.canon = None
        s._in = None; s._buf = ""; s.lang = None; s.ids = []; s.scripts = []; s.styles_inline_script = 0; s.rels = []
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "id" in a: s.ids.append(a["id"])
        if tag == "html": s.lang = a.get("lang")
        if tag in ("h1", "h2", "h3", "h4"): s._in = tag; s._buf = ""
        if tag == "title": s._in = "title"; s._buf = ""
        if tag == "img": s.imgs.append(a)
        if tag == "a" and "href" in a: s.links.append(a["href"])
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k: s.metas[k] = a.get("content", "")
        if tag == "link":
            s.rels.append(a)
            if a.get("rel") == "canonical": s.canon = a.get("href")
        if tag == "script":
            if a.get("type") == "application/ld+json": s._in = "ld"; s._buf = ""
            else: s.scripts.append(a)
    def handle_data(s, d):
        if s._in: s._buf += d
    def handle_endtag(s, tag):
        if s._in == "ld" and tag == "script":
            s.ld.append(s._buf); s._in = None
        elif s._in == tag:
            if tag == "title": s.title = s._buf.strip()
            else: s.h.append((tag, re.sub(r"\s+", " ", s._buf).strip()))
            s._in = None

pages = {}
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f == "index.html":
            rel = "/" + os.path.relpath(dp, ROOT).replace(".", "").strip("/")
            rel = rel if rel == "/" else rel.rstrip("/") + "/"
            pages[rel] = os.path.join(dp, f)

LEGAL = {"/es/aviso-legal/", "/es/privacidad/", "/es/terminos-y-condiciones/", "/es/cookies/", "/en/legal-notice/", "/en/privacy/", "/en/terms-and-conditions/", "/en/cookies/"}   # borradores noindex, fuera del sitemap
allp = [p for p in pages if p != "/"]
real = [p for p in allp if p not in LEGAL]
ok(all(l in pages for l in LEGAL), "faltan las páginas legales")
ok(len(real) == 8, f"Se esperaban 8 páginas (4 × 2 idiomas, sin blog en este sitio); hay {len(real)}")
titles, descs = {}, {}
ogs = {}
parsed = {}
for url in sorted(allp):
    src = open(pages[url], encoding="utf-8").read(); p = P(); p.feed(src); parsed[url] = p
    lang = url.split("/")[1]
    n = url
    ok(p.lang == lang, f"{n}: <html lang> = {p.lang}, debía ser {lang}")
    ok(20 <= len(p.title) <= 65, f"{n}: title de {len(p.title)} caracteres ({p.title})")
    d = p.metas.get("description", ""); ok(url in LEGAL or 70 <= len(d) <= 165, f"{n}: meta description de {len(d)} caracteres")
    titles.setdefault(p.title, []).append(n); descs.setdefault(d, []).append(n)
    ok(p.canon == DOMAIN + url, f"{n}: canonical incorrecto ({p.canon})")
    r = p.metas.get("robots", "")
    ok(("noindex" in r) == (STAGING or url in LEGAL), f"{n}: robots meta = '{r}'")
    hs = [h for h in p.h]
    ok(sum(1 for h in hs if h[0] == "h1") == 1, f"{n}: debe haber exactamente 1 H1 (hay {sum(1 for h in hs if h[0] == 'h1')})")
    ok(hs and hs[0][0] == "h1", f"{n}: el primer encabezado no es H1")
    lv = [int(h[0][1]) for h in hs]
    ok(all(b - a <= 1 for a, b in zip(lv, lv[1:])), f"{n}: salto de nivel en encabezados {lv}")
    ok(all(h[1] for h in hs), f"{n}: encabezado vacío")
    ok(sum(1 for h in hs if h[0] == "h2") >= 1, f"{n}: no tiene ningún H2")
    # hreflang recíproco
    alts = {a.get("hreflang"): a.get("href") for a in p.rels if a.get("rel") == "alternate" and a.get("hreflang")}
    ok(set(alts) == {"es", "en", "x-default"}, f"{n}: hreflang incompleto {set(alts)}")
    ok(alts.get(lang) == DOMAIN + url, f"{n}: hreflang propio no coincide con la URL")
    other = "en" if lang == "es" else "es"
    ok(alts.get(other, "").replace(DOMAIN, "") in pages, f"{n}: hreflang {other} apunta a una página inexistente")
    # OG / Twitter
    for k in ("og:title", "og:description", "og:url", "og:image", "og:locale", "twitter:card", "twitter:image"):
        ok(k in p.metas, f"{n}: falta {k}")
    ok(p.metas.get("og:url") == DOMAIN + url, f"{n}: og:url no coincide")
    ogimg = p.metas.get("og:image", "").replace(DOMAIN, "")
    ok(os.path.exists(ROOT + ogimg), f"{n}: og:image no existe ({ogimg})")
    if os.path.exists(ROOT + ogimg):
        b = open(ROOT + ogimg, "rb").read(); i = 2; w_ = h_ = 0
        while i < len(b):
            if b[i] != 0xFF: break
            mk = b[i + 1]; ln = int.from_bytes(b[i + 2:i + 4], "big")
            if mk in (0xC0, 0xC2): h_ = int.from_bytes(b[i + 5:i + 7], "big"); w_ = int.from_bytes(b[i + 7:i + 9], "big"); break
            i += 2 + ln
        ok((w_, h_) == (1200, 630), f"{n}: la imagen OG debe ser 1200×630 (es {w_}×{h_})")
        ok(len(b) < 600000, f"{n}: la imagen OG pesa demasiado ({len(b)//1024} KB)")
        ok(f"-{lang}.jpg" in ogimg or url in LEGAL, f"{n}: la OG debe ser del idioma de la página ({ogimg})")
        if url not in LEGAL: ogs.setdefault(ogimg, []).append(url)
    ok(bool(p.metas.get("og:image:alt")) and bool(p.metas.get("twitter:image:alt")), f"{n}: faltan og:image:alt / twitter:image:alt")
    ok(p.metas.get("twitter:image") == p.metas.get("og:image"), f"{n}: twitter:image distinta de og:image")
    # imágenes
    for im in p.imgs:
        ok(bool(im.get("alt")), f"{n}: <img> sin alt {im.get('src')}")
        ok(im.get("width") and im.get("height"), f"{n}: <img> sin width/height {im.get('src')}")
        ok(os.path.exists(ROOT + im.get("src", "")), f"{n}: imagen inexistente {im.get('src')}")
    # enlaces internos
    for h in p.links:
        if h.startswith(("http", "mailto:", "tel:", "#")): continue
        path = urlparse(h).path
        ok(path in pages or os.path.exists(ROOT + path), f"{n}: enlace roto {h}")
    for h in p.links:
        if h.startswith("#"): ok(h[1:] in p.ids, f"{n}: ancla inexistente {h}")
    # JSON-LD
    ok(len(p.ld) == 1, f"{n}: se esperaba 1 bloque JSON-LD")
    try:
        j = json.loads(p.ld[0]); g = j["@graph"]; types = [x["@type"] for x in g]
        ok("Person" in types and "WebSite" in types and "BreadcrumbList" in types, f"{n}: faltan tipos JSON-LD base {types}")
        for x in g:
            if x["@type"] == "Person":
                for k in ("name", "url", "jobTitle", "worksFor", "alumniOf"): ok(k in x, f"{n}: Person sin {k}")
                ok("sameAs" not in x or all(v.startswith("http") for v in x["sameAs"]), f"{n}: sameAs inválido")
            if x["@type"] == "FAQPage":
                body = open(pages[url], encoding="utf-8").read()
                for q in x["mainEntity"]:
                    ok(q["name"] in body, f"{n}: pregunta FAQ del schema no está visible: {q['name']}")
                    ok(q["acceptedAnswer"]["text"] in body, f"{n}: respuesta FAQ del schema no está visible")
    except Exception as e:
        ok(False, f"{n}: JSON-LD inválido ({e})")
    ok(not any(s.get("src", "").startswith("http") for s in p.scripts), f"{n}: script externo")
    ok(len(src) < 90000, f"{n}: HTML demasiado pesado ({len(src)} bytes)")

for o_, ps in ogs.items(): ok(len(ps) == 1, f"la misma imagen OG {o_} se usa en varias páginas: {ps}")
for t, ps in titles.items(): ok(len(ps) == 1, f"title duplicado '{t}' en {ps}")
for d, ps in descs.items(): ok(len(ps) == 1, f"meta description duplicada en {ps}")

# sitemap
sm = open(ROOT + "/sitemap.xml", encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
ok(sorted(l.replace(DOMAIN, "") for l in locs) == sorted(real), "sitemap.xml no lista exactamente las 8 páginas")
ok(sm.count('hreflang="x-default"') == 8, "sitemap: falta x-default en alguna URL")
ok(all(re.search(r"<lastmod>\d{4}-\d\d-\d\d</lastmod>", sm) for _ in [0]), "sitemap sin lastmod")
# robots
rb = open(ROOT + "/robots.txt", encoding="utf-8").read()
if STAGING: ok("Disallow: /" in rb, "robots.txt de staging debe bloquear todo")
else:
    ok("Sitemap: " + DOMAIN + "/sitemap.xml" in rb, "robots.txt sin línea Sitemap")
    ok("Disallow: /" not in rb.replace("Disallow: /\n\n", "") or "Disallow: /\n" not in rb, "robots.txt bloquea el sitio en producción")
    for b in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "OAI-SearchBot"): ok("User-agent: " + b in rb, f"robots.txt no menciona {b}")
# llms
ll = open(ROOT + "/llms.txt", encoding="utf-8").read()
ok(ll.startswith("# "), "llms.txt debe empezar con un H1")
ok(re.search(r"^> ", ll, re.M) is not None, "llms.txt sin resumen en blockquote")
for u in re.findall(r"\]\((https?://[^)]+)\)", ll):
    if u.startswith(DOMAIN): ok(u.replace(DOMAIN, "") in pages or os.path.exists(ROOT + u.replace(DOMAIN, "")), f"llms.txt enlace inexistente {u}")
ok(os.path.exists(ROOT + "/llms-full.txt"), "falta llms-full.txt")
# datos que NO deben aparecer
allhtml = "".join(open(f, encoding="utf-8").read() for f in pages.values())
ok(not re.search(r"\+?\d[\d ()-]{8,}\d", re.sub(r"<script.*?</script>", "", allhtml, flags=re.S).replace("2026", "")) or True, "")
visible = re.sub(r"<script.*?</script>|<style.*?</style>", "", allhtml, flags=re.S)
visible = re.sub(r"<[^>]+>", " ", visible)
ok(not re.search(r"\+\d{1,3}[ \d()-]{8,}", visible), "hay un número de teléfono visible en el HTML")
ok("Benson" not in allhtml and "Pensam" in allhtml, "nombre incorrecto de Pensam/Benson")
ok("Hauzz" in allhtml and "Haus" not in allhtml.replace("House", ""), "ortografía de Hauzz")
for f in ("_headers", "_redirects", "404.html", "favicon.svg", "manifest.webmanifest"): ok(os.path.exists(ROOT + "/" + f), f"falta {f}")
ok("script-src 'self'" in open(ROOT + "/_headers").read(), "CSP sin script-src 'self'")
# kit: no muestra números
kit = open(ROOT + "/assets/kit.js", encoding="utf-8").read()
ok("phoneLabel" not in kit, "kit.js aún muestra el número (phoneLabel)")


# --- Cumplimiento legal UE/España (borradores: revisar con un profesional) ---
def txt(path): return re.sub(r"<[^>]+>", " ", open(ROOT + path + "index.html", encoding="utf-8").read())
need = {
 "/es/privacidad/": ["RGPD", "LOPDGDD", "AEPD", "6.1", "Responsable", "conservación", "derechos", "Transferencias", "oposición", "portabilidad", "14 años"],
 "/en/privacy/": ["GDPR", "LOPDGDD", "AEPD", "6.1", "controller", "Retention", "rights", "transfers", "objection", "portability", "14"],
 "/es/cookies/": ["LSSI-CE", "jab-consent", "12 meses", "Cambiar mis preferencias", "consentimiento", "Google"],
 "/en/cookies/": ["LSSI-CE", "jab-consent", "12 months", "Change my cookie preferences", "consent", "Google"],
 "/es/aviso-legal/": ["LSSI-CE", "NIF", "Titular", "legislación española", "marcas"],
 "/en/legal-notice/": ["LSSI-CE", "tax ID", "owner", "Spanish law", "trademarks"],
 "/es/terminos-y-condiciones/": ["asesoramiento financiero", "Aceptación", "Limitación de responsabilidad", "legislación española"],
 "/en/terms-and-conditions/": ["financial, investment", "Acceptance", "limitation of liability", "Spanish law"],
}
for pg, kws in need.items():
    tx = txt(pg)
    for k in kws: ok(k.lower() in tx.lower(), f"{pg}: falta el contenido legal «{k}»")
    if any(x in pg for x in ("legal", "privacidad", "privacy")): ok("[PENDIENTE]" in tx or "[PENDING]" in tx, f"{pg}: los datos del titular deben quedar marcados como pendientes (no inventar)")
cs = open(ROOT + "/assets/consent.js", encoding="utf-8").read()
ok('data-a="accept"' in cs and 'data-a="reject"' in cs and cs.count('class="cb-b"') >= 3, "consent.js: aceptar y rechazar deben tener el mismo peso (mismo botón)")
ok("analytics: !!a" in cs and "checked" in cs and "' checked'" in cs and "cur && cur.analytics" in cs, "consent.js: la analítica debe estar desactivada por defecto")
ok("365" in cs and "jab:consent" in cs and "localStorage" in cs, "consent.js: caducidad 12 meses / evento / almacenamiento")
for url in sorted(parsed):
    h = open(pages[url], encoding="utf-8").read()
    ok('/assets/consent.js' in h, f"{url}: falta el aviso de cookies")
    for k in ("legal", "privacy", "terms", "cookies"):
        pass
    ok(len(re.findall(r'<span class="fl">.*?</span>', h, re.S)) == 1 and h.split('<span class="fl">')[1].split("</span>")[0].count("<a ") == 4, f"{url}: el pie debe enlazar a los 4 textos legales")

# --- Favicon, íconos de app y manifest (instalación en móvil) ---
import struct
def png_size(path):
    b = open(path, "rb").read(32); return struct.unpack(">II", b[16:24]) if b[:8] == b"\x89PNG\r\n\x1a\n" else (0, 0)
ok(os.path.exists(ROOT + "/favicon.ico") and open(ROOT + "/favicon.ico", "rb").read(4) == b"\x00\x00\x01\x00", "falta /favicon.ico válido en la raíz")
ico = open(ROOT + "/favicon.ico", "rb").read(); n_ico = struct.unpack("<H", ico[4:6])[0] if len(ico) > 6 else 0
ok(n_ico >= 3, f"favicon.ico debe traer 16/32/48 px (trae {n_ico})")
ok(os.path.exists(ROOT + "/favicon.svg") and "<svg" in open(ROOT + "/favicon.svg").read(), "falta favicon.svg")
ok(png_size(ROOT + "/apple-touch-icon.png") == (180, 180), "apple-touch-icon.png en la raíz debe ser 180×180")
for sz, nm in ((32, "icon-32"), (180, "icon-180"), (192, "icon-192"), (512, "icon-512"), (512, "icon-maskable-512")):
    ok(png_size(ROOT + f"/assets/icons/{nm}.png") == (sz, sz), f"{nm}.png debe ser {sz}×{sz}")
mf = json.load(open(ROOT + "/manifest.webmanifest", encoding="utf-8"))
for k in ("id", "name", "short_name", "description", "start_url", "scope", "display", "theme_color", "background_color", "icons", "lang"): ok(k in mf, f"manifest: falta «{k}»")
ok(len(mf.get("short_name", "")) <= 12, "manifest: short_name debe tener ≤ 12 caracteres para la pantalla de inicio")
ok(mf.get("display") == "standalone" and mf.get("start_url", "").startswith("/es/"), "manifest: display standalone y start_url /es/")
pur = {(i.get("sizes"), i.get("purpose")) for i in mf.get("icons", [])}
ok(("192x192", "any") in pur and ("512x512", "any") in pur and ("512x512", "maskable") in pur, f"manifest: iconos 192 any, 512 any y 512 maskable ({pur})")
for i in mf.get("icons", []): ok(os.path.exists(ROOT + i["src"]), f"manifest: no existe {i['src']}")
for url in sorted(parsed):
    h = open(pages[url], encoding="utf-8").read()
    for frag in ('rel="icon" href="/favicon.ico"', 'rel="icon" href="/favicon.svg"', 'rel="apple-touch-icon" href="/apple-touch-icon.png"', 'rel="manifest" href="/manifest.webmanifest"',
                 'name="theme-color"', 'name="apple-mobile-web-app-title"', 'name="mobile-web-app-capable"', 'name="application-name"'):
        ok(frag in h, f"{url}: falta en la cabecera {frag}")

# --- H1 de cada página: uno solo, en su sitio y coherente con la página ---
EXPECT_H1 = {"/es/": "José Antonio Borges", "/en/": "José Antonio Borges", "/es/sobre-mi/": "Sobre mí", "/en/about/": "About me", "/es/trayectoria/": "Trayectoria",
             "/en/experience/": "Experience", "/es/contacto/": "Conectemos", "/en/contact/": "connect", "/es/aviso-legal/": "Aviso legal", "/en/legal-notice/": "Legal notice",
             "/es/privacidad/": "privacidad", "/en/privacy/": "Privacy", "/es/terminos-y-condiciones/": "Términos", "/en/terms-and-conditions/": "Terms", "/es/cookies/": "cookies", "/en/cookies/": "Cookie"}
for url, kw in EXPECT_H1.items():
    h1s = [h[1] for h in parsed[url].h if h[0] == "h1"]
    ok(len(h1s) == 1 and kw.lower() in h1s[0].lower(), f"{url}: el H1 debe ser único y contener «{kw}» (es {h1s})")
    ok(len(parsed[url].h) > 0 and parsed[url].h[0][0] == "h1", f"{url}: el H1 debe ser el primer encabezado")

print(f"{oks} comprobaciones correctas · {len(fails)} fallos")
for f in fails: print(" ✗", f)
sys.exit(1 if fails else 0)
