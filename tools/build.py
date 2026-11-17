#!/usr/bin/env python3
"""Generador del sitio José Antonio Borges (ES/EN, estático).
Uso:  python3 tools/build.py            -> sitio de producción (indexable)
      python3 tools/build.py --staging  -> noindex + robots Disallow:/  (para pruebas)
Salida: maqueta/site/   (assets/site.css, kit.js, site.js, qrcode.min.js ya existen)."""
import json, os, re, shutil, subprocess, sys
from html import escape as esc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import legal_content

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
FOTOS = os.path.join(os.path.dirname(ROOT), "fotos")
STAGING = "--staging" in sys.argv
DOMAIN = "https://joseantonioborges.com"      # PENDIENTE: confirmar y registrar
LASTMOD = "2026-11-16"
UPDATED = {"es": "16 de noviembre de 2026", "en": "16 November 2026"}
DEMO = True      # True = muestra el aviso "datos de ejemplo". Poner False al publicar con datos reales
NAME = "José Antonio Borges"
BLOG_URL = "https://blog.joseantonioborges.com"   # el blog vive FUERA de este sitio
LINKEDIN = ""    # PENDIENTE: URL real. Si se rellena, se añade a sameAs y al pie
INSTAGRAM = ""   # PENDIENTE: URL real

OG_ALT = {
 "home": ("Construir. Escalar. Transformar. José Antonio Borges, ejecutivo y emprendedor del sector inmobiliario, en el escenario", "Build. Scale. Transform. José Antonio Borges, executive and real estate entrepreneur, on stage"),
 "about": ("Sobre mí: José Antonio Borges, ejecutivo y emprendedor del sector inmobiliario, en el escenario de eXpcon Barcelona", "About: José Antonio Borges, executive and real estate entrepreneur, on the eXpcon Barcelona stage"),
 "exp": ("Trayectoria: del desafío al resultado. eXp Realty España, Hauzz, Tiko y Private Equity", "Experience: from challenge to outcome. eXp Realty Spain, Hauzz, Tiko and Private Equity"),
 "contact": ("Contacto: conversemos. Entrevistas, alianzas, negocios e inversión con José Antonio Borges", "Contact: let’s talk. Interviews, partnerships, business and investment with José Antonio Borges"),
}
PAGES = {
    "home":    {"es": "/es/", "en": "/en/"},
    "about":   {"es": "/es/sobre-mi/", "en": "/en/about/"},
    "exp":     {"es": "/es/trayectoria/", "en": "/en/experience/"},
    "contact": {"es": "/es/contacto/", "en": "/en/contact/"},
    "legal":   {"es": "/es/aviso-legal/", "en": "/en/legal-notice/"},
    "privacy": {"es": "/es/privacidad/", "en": "/en/privacy/"},
    "terms":   {"es": "/es/terminos-y-condiciones/", "en": "/en/terms-and-conditions/"},
    "cookies": {"es": "/es/cookies/", "en": "/en/cookies/"},
}
NOINDEX = ("legal", "privacy", "terms", "cookies")            # borradores a la espera de datos del titular
INDEXABLE = [k for k in PAGES if k not in NOINDEX]
NAV = [("home", "Inicio", "Home"), ("about", "Sobre mí", "About"), ("exp", "Trayectoria", "Experience"), ("contact", "Contacto", "Contact")]
OTHER = {"es": "en", "en": "es"}
LOCALE = {"es": "es_ES", "en": "en_US"}

META = {
 "home": {"es": ("José Antonio Borges | Liderazgo empresarial y real estate", "José Antonio Borges, líder de eXp Realty España: cómo hacer crecer una agencia inmobiliaria con sistemas, datos y autonomía. Entrevistas y conversaciones."),
          "en": ("José Antonio Borges | Business Leadership & Real Estate", "José Antonio Borges, leader of eXp Realty Spain: how to grow a real estate business with systems, data and autonomy. Interviews and conversations.")},
 "about": {"es": ("Sobre mí | José Antonio Borges", "La historia de José Antonio Borges: de la inversión en Estados Unidos a fundar Hauzz y liderar compañías inmobiliarias en España."),
           "en": ("About | José Antonio Borges", "José Antonio Borges's journey from investment in the United States to founding Hauzz and leading real estate businesses in Spain.")},
 "exp": {"es": ("Trayectoria y resultados | José Antonio Borges", "Experiencia de José Antonio Borges en eXp Realty España, Hauzz, Rive, Tiko e inversiones en Estados Unidos."),
         "en": ("Experience & Results | José Antonio Borges", "José Antonio Borges's experience at eXp Realty Spain, Hauzz, Rive, Tiko and in US private equity.")},
 "legal": {"es": ("Aviso legal | José Antonio Borges", "Aviso legal del sitio web de José Antonio Borges."), "en": ("Legal notice | José Antonio Borges", "Legal notice for José Antonio Borges's website.")},
 "privacy": {"es": ("Política de privacidad | José Antonio Borges", "Política de privacidad del sitio web de José Antonio Borges."), "en": ("Privacy policy | José Antonio Borges", "Privacy policy for José Antonio Borges's website.")},
 "terms": {"es": ("Términos y condiciones | José Antonio Borges", "Términos y condiciones de uso del sitio web de José Antonio Borges."), "en": ("Terms and conditions | José Antonio Borges", "Terms and conditions of use for José Antonio Borges's website.")},
 "cookies": {"es": ("Política de cookies | José Antonio Borges", "Política de cookies del sitio web de José Antonio Borges."), "en": ("Cookie policy | José Antonio Borges", "Cookie policy for José Antonio Borges's website.")},
 "contact": {"es": ("Contacto | José Antonio Borges", "Contacta con José Antonio Borges para conexiones profesionales, alianzas estratégicas, proyectos empresariales y colaboraciones."),
             "en": ("Contact | José Antonio Borges", "Connect with José Antonio Borges about business opportunities, strategic partnerships, investment networks and professional collaboration.")},
}

# ---------------------------------------------------------------- imágenes
IMGS = {  # clave: (archivo original, alt es, alt en)
 "controlas": ("JA -00 (5).jpg", "José Antonio Borges en el escenario ante una pantalla que dice «No controlas el resultado. Sí controlas tu siguiente paso.»", "José Antonio Borges on stage in front of a screen reading “You don't control the outcome. You do control your next step.”"),
 "hero": ("exp-34.jpg", "José Antonio Borges hablando en un evento, con una presentación al fondo", "José Antonio Borges speaking at an event with a presentation behind him"),
 "cierre": ("JA-cierre (1).jpg", "José Antonio Borges con micrófono ante una pantalla con la audiencia de un congreso", "José Antonio Borges holding a microphone in front of a screen showing a conference audience"),
 "audiencia": ("exp-6.jpg", "José Antonio Borges hablando a una audiencia en una sala de formación", "José Antonio Borges speaking to an audience in a training room"),
 "lidera": ("JA-00 (8).jpg", "José Antonio Borges en el escenario ante una pantalla que dice «Lidérate a ti primero», junto al atril de eXp Realty", "José Antonio Borges on stage in front of a screen reading “Lead yourself first”, next to the eXp Realty lectern"),
 "cero": ("IMG_8511.jpeg", "José Antonio Borges en el escenario ante un marcador 0–0 en una sala de congresos", "José Antonio Borges on stage in front of a 0–0 scoreboard in a conference room"),
 "country": ("Copia de eXpcon-Barcelona2025-AJ--1068.jpg", "Pantalla de un congreso que presenta a José Antonio Borges como Country Leader, Spain, ante una gran audiencia", "Conference screen introducing José Antonio Borges as Country Leader, Spain, in front of a large audience"),
 "barcelona": ("eXpcon-Barcelona2025-AJ--940.jpg", "José Antonio Borges hablando en el escenario de un congreso inmobiliario en Barcelona", "José Antonio Borges speaking on the stage of a real estate conference in Barcelona"),
}
DIMS = {}
WIDTHS = [640, 1024, 1600]

def sh(*a):
    subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def exif_orientation(path):
    import struct
    d = open(path, "rb").read(262144); i = d.find(b"Exif\x00\x00")
    if i < 0: return 1
    t = d[i + 6:]; bo = "<" if t[:2] == b"II" else ">"
    off = struct.unpack(bo + "I", t[4:8])[0]; n = struct.unpack(bo + "H", t[off:off + 2])[0]
    for k in range(n):
        e = t[off + 2 + 12 * k: off + 14 + 12 * k]
        if struct.unpack(bo + "H", e[:2])[0] == 0x0112: return struct.unpack(bo + "H", e[8:10])[0]
    return 1

def reset_orientation(path):
    """Pone la etiqueta EXIF de orientación en 1 (los píxeles ya están girados)."""
    import struct
    raw = bytearray(open(path, "rb").read()); i = bytes(raw[:262144]).find(b"Exif\x00\x00")
    if i < 0: return
    t0 = i + 6; bo = "<" if raw[t0:t0 + 2] == b"II" else ">"
    off = struct.unpack(bo + "I", bytes(raw[t0 + 4:t0 + 8]))[0]; n = struct.unpack(bo + "H", bytes(raw[t0 + off:t0 + off + 2]))[0]
    for k in range(n):
        e = t0 + off + 2 + 12 * k
        if struct.unpack(bo + "H", bytes(raw[e:e + 2]))[0] == 0x0112: raw[e + 8:e + 10] = struct.pack(bo + "H", 1)
    open(path, "wb").write(bytes(raw))

def prepared(src, key):
    """Devuelve una copia con la orientación EXIF aplicada a los píxeles (si hace falta)."""
    o = exif_orientation(src)
    if o not in (3, 6, 8): return src
    tmp = os.path.join(OUT, ".tmp"); os.makedirs(tmp, exist_ok=True)
    dst = os.path.join(tmp, key + ".jpg")
    sh("sips", "-r", {3: "180", 6: "90", 8: "270"}[o], src, "--out", dst)
    reset_orientation(dst)
    return dst

def build_images():
    d = os.path.join(OUT, "img"); os.makedirs(d, exist_ok=True)
    for k, (f, _, _) in IMGS.items():
        src = prepared(os.path.join(FOTOS, f), k)
        info = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", src], capture_output=True, text=True).stdout
        w = int(re.search(r"pixelWidth: (\d+)", info).group(1)); h = int(re.search(r"pixelHeight: (\d+)", info).group(1))
        DIMS[k] = (w, h)
        for tw in WIDTHS:
            if tw > w: continue
            jpg = os.path.join(d, f"{k}-{tw}.jpg"); webp = os.path.join(d, f"{k}-{tw}.webp")
            if not os.path.exists(webp):
                sh("sips", "--resampleWidth", str(tw), "-s", "format", "jpeg", "-s", "formatOptions", "76", src, "--out", jpg)
                sh("cwebp", "-q", "76", jpg, "-o", webp)
    shutil.rmtree(os.path.join(OUT, ".tmp"), ignore_errors=True)
    # imágenes OG 1200x630
    o = os.path.join(OUT, "assets", "og"); os.makedirs(o, exist_ok=True)
    for name, key in (("og-home", "controlas"), ("og-about", "hero")):
        p = os.path.join(o, name + ".jpg")
        if not os.path.exists(p):
            sh("sips", "--resampleWidth", "1200", "-s", "format", "jpeg", "-s", "formatOptions", "80", os.path.join(FOTOS, IMGS[key][0]), "--out", p)
            sh("sips", "-c", "630", "1200", p)

def widths_for(k):
    w = DIMS[k][0]
    return [x for x in WIDTHS if x <= w]

def picture(k, lang, sizes, cls="", eager=False, style=""):
    w, h = DIMS[k]; ws = widths_for(k)
    alt = IMGS[k][1 if lang == "es" else 2]
    big = ws[-1] if eager else ws[min(1, len(ws) - 1)]
    ss = lambda ext: ", ".join(f"/img/{k}-{x}.{ext} {x}w" for x in ws)
    attrs = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img{attrs}{st} src="/img/{k}-{big}.jpg" srcset="{ss("jpg")}" sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}" {load}></picture>')

# ---------------------------------------------------------------- contenido compartido
def t(lang, es, en): return es if lang == "es" else en

BIO = [  # (es, en)
 ("Soy José Antonio Borges, ejecutivo y emprendedor con trayectoria internacional en inversión, creación de empresas y liderazgo, especializado en el sector inmobiliario.",
  "I'm José Antonio Borges, an executive and entrepreneur with an international background in investment, company building and business leadership, with a particular focus on real estate."),
 ("Actualmente lidero eXp Realty España. Junto con mi equipo hemos impulsado un crecimiento del 120 % de la facturación en 22 meses y una transformación de la operación basada en rentabilidad, procesos, sistemas y decisiones informadas por datos.",
  "I currently lead eXp Realty Spain. Together with my team, we have driven 120% revenue growth over 22 months and transformed the operation through a stronger focus on profitability, processes, systems and data-informed decision-making."),
 ("Comencé mi trayectoria profesional en Estados Unidos, dentro del mundo de la inversión y el private equity. Participé en el análisis y desarrollo de operaciones de adquisición y financiación, una experiencia que me enseñó a evaluar negocios desde sus fundamentos económicos.",
  "My professional journey began in the United States, working in private equity and investment. I was involved in evaluating acquisitions and financing opportunities, an experience that taught me to look at businesses through the lens of their underlying economics."),
 ("En 2019 me trasladé con mi familia a España con el propósito de emprender. Exploré distintas oportunidades antes de fundar Hauzz, un negocio inmobiliario que llegó a reunir a cientos de agentes y que posteriormente fue adquirido por Rive.",
  "In 2019, I moved to Spain with my family, determined to pursue entrepreneurship. After exploring different business opportunities, I founded Hauzz, a real estate business that grew to include hundreds of agents and was subsequently acquired by Rive."),
 ("Después continué desarrollando operaciones y equipos en Rive, Tiko y eXp Realty. He trabajado tanto creando negocios desde cero como transformando organizaciones existentes, siempre con interés por la combinación de estrategia, ejecución y personas.",
  "I went on to develop operations and teams at Rive, Tiko and eXp Realty. I've had the opportunity to build businesses from the ground up as well as transform established organizations, always drawn to the intersection of strategy, execution and people."),
 ("Mi manera de trabajar también está influida por años dedicados al tenis de alto rendimiento y por mi formación en Matemáticas y Economía. Ambas experiencias me enseñaron que el progreso requiere preparación, disciplina, capacidad para aprender y voluntad de revisar las propias decisiones.",
  "My approach to leadership was also shaped outside the business world. Years of high-performance tennis and a background in Mathematics and Economics taught me the importance of preparation, discipline, learning and the ability to question my own assumptions."),
 ("Creo en organizaciones que miden lo importante, anticipan los problemas y permiten que las personas tengan autonomía para hacer bien su trabajo. Para mí, liderar es crear las condiciones en las que otros pueden crecer.",
  "I believe strong organizations measure what matters, identify problems early and give people the autonomy to do their best work. To me, leadership is about creating the conditions in which others can grow."),
]
EXP = [  # id, empresa, cargo(es,en), titular(es,en), párrafos [(es,en)], destacados(es,en)|None
 ("exp", "eXp Realty España", ("Country Leader / Managing Director", "Country Leader / Managing Director"),
  ("Crecimiento sostenible apoyado en sistemas, datos y talento.", "Sustainable growth powered by systems, data and people."),
  [("Al frente de eXp Realty España, y trabajando junto a un equipo comprometido, he impulsado una transformación enfocada en crecimiento, rentabilidad y disciplina operativa. En 22 meses el negocio incrementó su facturación un 120 % y alcanzó la rentabilidad durante 2026.",
    "Leading eXp Realty Spain alongside a committed team, I've helped drive a transformation focused on growth, profitability and operational discipline. In 22 months, the business grew revenue by 120% and achieved profitability in 2026."),
   ("Más allá de los resultados, uno de los cambios fundamentales ha sido crear una estructura operativa más sólida: procesos claros, herramientas de gestión, medición constante de indicadores y capacidad para anticipar dificultades. El objetivo es escalar sin limitar innecesariamente la autonomía de los agentes.",
    "Beyond the results, one of the most meaningful changes has been building stronger operating foundations: clear processes, management tools, regular performance measurement and the ability to anticipate issues. The goal is to scale without unnecessarily restricting agents' independence."),
   ("También hemos avanzado en la incorporación de equipos y agencias de mayor tamaño, ampliando las formas en que los profesionales inmobiliarios pueden desarrollar su negocio dentro de eXp.",
    "We have also expanded the business by attracting and integrating larger real estate teams and agencies.")],
  ("+120 % de facturación en 22 meses · rentabilidad en 2026 · sistemas y métricas · integración de equipos y agencias", "+120% revenue growth in 22 months · profitability in 2026 · operational systems and KPIs · team and agency integration")),
 ("hauzz", "Hauzz", ("Fundador y CEO", "Founder & CEO"),
  ("De una oportunidad de mercado a una compañía adquirida.", "From an opportunity to an acquired business."),
  [("Fundé Hauzz después de trasladarme a España en 2019 y explorar diversas oportunidades empresariales. Desarrollé una compañía inmobiliaria que llegó a contar con cientos de agentes y que posteriormente fue adquirida por Rive.",
    "I founded Hauzz after moving to Spain in 2019 and exploring several business opportunities. I built a real estate company that grew to hundreds of agents and was later acquired by Rive."),
   ("Esta etapa marcó mi experiencia como fundador: formar equipos, construir una propuesta de valor, tomar decisiones bajo incertidumbre y desarrollar una operación capaz de crecer.",
    "It was a defining entrepreneurial experience: forming teams, developing a value proposition, making decisions under uncertainty and building an operation designed to grow.")], None),
 ("rive", "Rive / Kodit", ("Dirección del negocio de intermediación inmobiliaria", "Real Estate Brokerage Leadership"),
  ("Integración y crecimiento después de una adquisición.", "Integration and growth following an acquisition."),
  [("Tras la adquisición de Hauzz, me incorporé a Rive / Kodit para contribuir al desarrollo del negocio de intermediación inmobiliaria. Durante un período aproximado de 18 meses, el negocio prácticamente duplicó su facturación.",
    "After Rive acquired Hauzz, I joined the business to help develop its real estate brokerage operations. Over approximately 18 months, the business nearly doubled its revenue."),
   ("La experiencia combinó integración, crecimiento comercial, desarrollo de equipos y ejecución de una estrategia en una organización de mayor escala.",
    "The experience brought together integration, commercial growth, team development and execution within a larger organization.")], None),
 ("tiko", "Tiko · España y Portugal", ("Head of Brokerage", "Head of Brokerage"),
  ("Construir una operación comercial desde cero.", "Building a commercial operation from the ground up."),
  [("Lideré la creación y expansión de la división de brokerage en España y Portugal. La operación pasó de una infraestructura inicial limitada a una estructura con CRM, herramientas, contratos, procesos y un equipo interno de gestión, desarrollando una red de aproximadamente 250 agentes.",
    "I led the creation and expansion of the brokerage division across Spain and Portugal. Starting with limited operating infrastructure, we implemented a CRM, systems, contracts, tools and processes, established an internal management team and developed a network of approximately 250 agents."),
   ("Fue una experiencia exigente de construcción operativa, escalabilidad comercial y coordinación de equipos en dos mercados.",
    "This was a demanding experience in operational design, commercial scaling and cross-market team leadership.")], None),
 ("pe", "Private Equity · Estados Unidos", ("Senior Acquisitions Associate", "Senior Acquisitions Associate"),
  ("Una base financiera para tomar decisiones empresariales.", "A financial foundation for business decisions."),
  [("Trabajé directamente con la dirección de una firma de private equity, participando en el análisis y los procesos de adquisición relacionados con un volumen agregado aproximado de US$250 millones en un año. Posteriormente profundicé en el análisis de financiación y deuda en Pensam.",
    "Working directly with the managing director of a private equity firm, I participated in the analysis and acquisition processes relating to approximately US$250 million in aggregate transaction volume over one year. I later expanded my experience in lending and structured debt analysis at Pensam."),
   ("Estas experiencias fortalecieron una forma de pensar centrada en la calidad de los activos, el riesgo, la economía de un negocio y la disciplina en la toma de decisiones.",
    "These roles helped develop a way of thinking grounded in asset quality, risk, business economics and disciplined decision-making.")], None),
]
AREAS = [
 ("Liderazgo inmobiliario", "Real Estate Leadership", "Modelos de negocio, expansión e innovación en el real estate.", "Business models, expansion and innovation in real estate."),
 ("Emprendimiento y escalabilidad", "Entrepreneurship &amp; Scaling", "De una oportunidad a una operación que crece.", "Turning opportunities into growing organizations."),
 ("Estrategia y excelencia operativa", "Strategy &amp; Operational Excellence", "Procesos, rentabilidad, métricas y ejecución.", "Processes, profitability, metrics and execution."),
 ("Tecnología e inteligencia artificial", "Technology &amp; AI", "Aplicaciones prácticas para mejorar la operación y la experiencia del cliente.", "Practical ways technology can improve operations and customer experiences."),
 ("Equipos y liderazgo comercial", "Commercial Teams &amp; Leadership", "Cultura, talento, productividad y autonomía.", "Culture, talent, performance and autonomy."),
]
FAQ = [
 ("¿Quién es José Antonio Borges?", "Who is José Antonio Borges?",
  "José Antonio Borges es un ejecutivo y emprendedor con trayectoria internacional en inversión, creación de empresas y liderazgo, especializado en el sector inmobiliario. Actualmente lidera eXp Realty España.",
  "José Antonio Borges is an executive and entrepreneur with an international background in investment, company building and business leadership, focused on real estate. He currently leads eXp Realty Spain."),
 ("¿Qué empresa fundó José Antonio Borges?", "Which company did José Antonio Borges found?",
  "Fundó Hauzz, un negocio inmobiliario que llegó a reunir a cientos de agentes y que posteriormente fue adquirido por Rive.",
  "He founded Hauzz, a real estate business that grew to include hundreds of agents and was subsequently acquired by Rive."),
 ("¿Qué resultados ha logrado al frente de eXp Realty España?", "What results has he achieved at eXp Realty Spain?",
  "Junto con su equipo, la facturación creció un 120 % en 22 meses, con una operación basada en rentabilidad, procesos, sistemas y decisiones informadas por datos.",
  "Together with his team, revenue grew 120% over 22 months, with an operation built on profitability, processes, systems and data-informed decisions."),
 ("¿Dónde estudió José Antonio Borges?", "Where did José Antonio Borges study?",
  "Estudió Matemáticas y Economía y realizó estudios de posgrado en Matemáticas en la Universidad de Miami, donde también tuvo experiencia en docencia universitaria.",
  "He studied Mathematics and Economics and did postgraduate study in Mathematics at the University of Miami, where he also taught at university level."),
]
ARTICLES = [  # categoría(es,en), título(es,en)
 (("Estrategia y operaciones", "Strategy &amp; Operations"), ("Crecer sin perder el control: por qué los sistemas importan más que las reglas", "Scaling Without Losing Control: Why Systems Matter More Than Rules")),
 (("Emprendimiento", "Entrepreneurship"), ("Qué aprendí construyendo una empresa inmobiliaria desde cero", "What Building a Real Estate Business from Scratch Taught Me")),
 (("Estrategia y operaciones", "Strategy &amp; Operations"), ("Los indicadores que ayudan a anticipar problemas en una organización comercial", "The Metrics That Help Commercial Organizations Spot Problems Early")),
 (("Real Estate", "Real Estate"), ("El futuro del agente inmobiliario: tecnología, especialización y relaciones humanas", "The Future of Real Estate Agents: Technology, Specialization and Human Relationships")),
 (("Liderazgo y equipos", "Leadership &amp; Teams"), ("Cada día empieza 0–0: liderar el proceso cuando no controlas el resultado", "Every Day Starts at 0–0: Leading the Process When You Can't Control the Outcome")),
]
CATS = [("Real Estate", "Real Estate"), ("Emprendimiento", "Entrepreneurship"), ("Estrategia y operaciones", "Strategy &amp; Operations"), ("Tecnología e IA", "Technology &amp; AI"), ("Liderazgo y equipos", "Leadership &amp; Teams")]
TOPICS = [  # problemas que resuelve (cada uno sale de hechos del brief) -> es / en
 ("Mi agencia factura, pero no crece ni gana dinero como debería.", "My agency brings in revenue, but doesn't grow or earn the way it should."),
 ("Quiero crecer sin perder el control ni asfixiar a mi equipo con reglas.", "I want to grow without losing control or smothering my team with rules."),
 ("Necesito construir una red de agentes desde cero.", "I need to build an agent network from scratch."),
 ("Estoy pensando en vender mi negocio o integrarlo en otro.", "I'm thinking of selling my business or merging it into another."),
 ("Quiero mirar mi negocio con ojos de inversor.", "I want to look at my business through an investor's eyes."),
 ("Quiero usar IA en mi operación, pero no sé por dónde empezar.", "I want to use AI in my operation, but I don't know where to start."),
]
USEFUL = {  # "Útil si…" por etapa de la trayectoria
 "exp": ("necesitas crecer y ser rentable con una operación ordenada, basada en sistemas, datos y talento.", "you need to grow and be profitable with an orderly operation built on systems, data and talent."),
 "hauzz": ("estás construyendo una empresa inmobiliaria, o pensando en venderla.", "you are building a real estate company, or thinking about selling it."),
 "rive": ("vas a integrar un negocio tras una adquisición, o crecer dentro de una organización mayor.", "you are about to integrate a business after an acquisition, or grow inside a larger organization."),
 "tiko": ("tienes que montar desde cero una operación comercial y una red de agentes.", "you have to set up a commercial operation and an agent network from scratch."),
 "pe": ("evalúas una inversión, una adquisición o la economía de un negocio.", "you are evaluating an investment, an acquisition or the economics of a business."),
}
AUDIENCES = [  # quién se beneficia de conversar -> (público es, en, qué resuelve es, en, mensaje es, en)
 ("Agentes y propietarios de agencias", "Agents and agency owners", "Crecer con credibilidad, un modelo de gestión claro y autonomía para tu equipo.", "Growing with credibility, a clear management model and autonomy for your team.", "Hola José Antonio, dirijo una agencia o equipo inmobiliario y me gustaría conversar contigo.", "Hello José Antonio, I run a real estate agency or team and I'd like to talk with you."),
 ("Empresarios y posibles socios", "Entrepreneurs and potential partners", "Construir y escalar un negocio con criterio y ejecución.", "Building and scaling a business with judgement and execution.", "Hola José Antonio, soy empresario y me gustaría explorar una colaboración contigo.", "Hello José Antonio, I'm an entrepreneur and I'd like to explore working together."),
 ("Inversores, fondos y directivos", "Investors, funds and executives", "Mirar un negocio por sus fundamentos: métricas, mejora operativa y rentabilidad.", "Looking at a business through its fundamentals: metrics, operational improvement and profitability.", "Hola José Antonio, te escribo desde el mundo de la inversión o la dirección y me gustaría conversar.", "Hello José Antonio, I'm writing from the investment or executive world and I'd like to talk."),
 ("Medios y organizadores", "Media and organizers", "Una conversación con experiencia directa sobre real estate, liderazgo y escalabilidad.", "A conversation grounded in firsthand experience of real estate, leadership and scaling.", "Hola José Antonio, me gustaría invitarte a una entrevista, podcast o evento.", "Hello José Antonio, I'd like to invite you to an interview, podcast or event."),
]

REASONS = [
 ("Entrevista, podcast o evento", "Interview, podcast or event", "Hola José Antonio, me gustaría invitarte a una entrevista, podcast o evento.", "Hello José Antonio, I'd like to invite you to an interview, podcast or event."),
 ("Alianza empresarial", "Strategic partnership", "Hola José Antonio, me gustaría explorar una alianza empresarial.", "Hello José Antonio, I'd like to explore a strategic partnership."),
 ("Negocio o proyecto", "Business or project", "Hola José Antonio, quiero comentarte un negocio o proyecto.", "Hello José Antonio, I'd like to share a business opportunity or project."),
 ("Inversión o dirección", "Investment or leadership", "Hola José Antonio, quiero hablar contigo sobre una inversión o un puesto de dirección.", "Hello José Antonio, I'd like to talk about an investment or a leadership role."),
 ("Otro motivo", "Something else", "Hola José Antonio, me gustaría ponerme en contacto contigo.", "Hello José Antonio, I'd like to get in touch."),
]

# ---------------------------------------------------------------- piezas HTML
IC_LI = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.06c.53-1 1.83-2 3.77-2 4.03 0 4.77 2.65 4.77 6.1V21h-4v-4.8c0-1.15-.02-2.62-1.6-2.62-1.6 0-1.85 1.25-1.85 2.54V21h-4z"/></svg>'
IC_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H7zm5 3.5A4.5 4.5 0 1 1 7.5 12 4.5 4.5 0 0 1 12 7.5zm0 2A2.5 2.5 0 1 0 14.5 12 2.5 2.5 0 0 0 12 9.5zm5.3-3.8a1 1 0 1 1-1 1 1 1 0 0 1 1-1z"/></svg>'

def u(key, lang): return PAGES[key][lang]
def abs_u(key, lang): return DOMAIN + PAGES[key][lang]

def header(lang, key):
    items = [f'<a href="{u(k, lang)}"{" aria-current=\"page\"" if k == key else ""}>{t(lang, a, b)}</a>' for k, a, b in NAV]
    items.insert(3, f'<a href="{BLOG_URL}" target="_blank" rel="noopener" class="blog-l">Blog<span class="sr"> ({t(lang, "se abre en una pestaña nueva", "opens in a new tab")})</span></a>')
    links = "".join(items)
    o = OTHER[lang]
    return (f'<header id="hd"><div class="wrap nav"><a class="logo" href="{u("home", lang)}" aria-label="{NAME}, {t(lang, "inicio", "home")}">{NAME}</a>'
            f'<nav class="links" aria-label="{t(lang, "Principal", "Main")}">{links}'
            f'<a id="lang" class="lang" href="{u(key, o)}" hreflang="{o}" lang="{o}" aria-label="{t(lang, "Read this page in English", "Leer esta página en español")}">{o.upper()}</a></nav></div></header>')

def footer(lang):
    soc = ""
    for ic, nm, url in ((IC_LI, "LinkedIn", LINKEDIN), (IC_IG, "Instagram", INSTAGRAM)):
        if url: soc += f'<a href="{url}" rel="me noopener" target="_blank" aria-label="{nm}" style="display:inline-flex;width:34px;height:34px;border:1px solid #3a3730;border-radius:50%;align-items:center;justify-content:center;color:#8e897d">{ic}</a>'
        else:   soc += f'<span role="img" aria-label="{nm} ({t(lang, "próximamente", "coming soon")})" title="{t(lang, "Próximamente", "Coming soon")}">{ic}</span>'
    legal = '<span class="fl">' + "".join(f'<a href="{u(k, lang)}">{t(lang, a_, b_)}</a>' for k, a_, b_ in (("legal", "Aviso legal", "Legal notice"), ("privacy", "Privacidad", "Privacy"), ("terms", "Términos", "Terms"), ("cookies", "Cookies", "Cookies"))) + '</span>'
    return f'<footer><div class="wrap"><span>© 2026 {NAME}</span>{legal}<div class="soc">{soc}</div></div></footer>'

def person(lang):
    p = {"@type": "Person", "@id": DOMAIN + "/#persona", "name": NAME, "url": abs_u("home", lang),
         "jobTitle": "Country Leader / Managing Director, eXp Realty España" if lang == "es" else "Country Leader / Managing Director, eXp Realty Spain",
         "description": t(lang, "Ejecutivo y emprendedor con trayectoria internacional en inversión, creación de empresas y liderazgo, especializado en el sector inmobiliario.",
                         "Executive and entrepreneur with an international background in investment, company building and business leadership, focused on real estate."),
         "image": DOMAIN + f"/assets/og/og-about-{lang}.jpg",
         "worksFor": {"@type": "Organization", "name": t(lang, "eXp Realty España", "eXp Realty Spain")},
         "alumniOf": {"@type": "CollegeOrUniversity", "name": "University of Miami"},
         "knowsAbout": [t(lang, a, b).replace("&amp;", "&") for a, b, _, _ in AREAS] if False else [re.sub("&amp;", "&", t(lang, a, b)) for a, b, _, _ in AREAS],
         "knowsLanguage": ["es", "en"]}
    sa = [x for x in (LINKEDIN, INSTAGRAM) if x]
    if sa: p["sameAs"] = sa
    return p

def crumbs(lang, key):
    items = [{"@type": "ListItem", "position": 1, "name": t(lang, "Inicio", "Home"), "item": abs_u("home", lang)}]
    if key != "home":
        nm = {"about": ("Sobre mí", "About"), "exp": ("Trayectoria", "Experience"), "contact": ("Contacto", "Contact"), "legal": ("Aviso legal", "Legal notice"), "privacy": ("Privacidad", "Privacy"), "terms": ("Términos y condiciones", "Terms and conditions"), "cookies": ("Cookies", "Cookies")}[key]
        items.append({"@type": "ListItem", "position": 2, "name": t(lang, *nm), "item": abs_u(key, lang)})
    return {"@type": "BreadcrumbList", "itemListElement": items}

def website(lang):
    return {"@type": "WebSite", "@id": DOMAIN + "/#web", "url": DOMAIN + "/", "name": NAME, "inLanguage": ["es", "en"], "publisher": {"@id": DOMAIN + "/#persona"}}

def page(key, lang, body, extra_ld, lcp=None, og="og/og-home-es"):
    title, desc = META[key][lang]; o = OTHER[lang]
    url = abs_u(key, lang)
    ld = {"@context": "https://schema.org", "@graph": [website(lang), person(lang)] + extra_ld}
    robots = "noindex, nofollow" if (STAGING or key in NOINDEX) else "index, follow, max-image-preview:large, max-snippet:-1"
    pre = ""
    if lcp:
        k, sizes = lcp; ws = widths_for(k)
        pre = f'<link rel="preload" as="image" type="image/webp" imagesrcset="{", ".join(f"/img/{k}-{x}.webp {x}w" for x in ws)}" imagesizes="{sizes}" fetchpriority="high">'
    ot = {"home": "website", "about": "profile"}.get(key, "website")
    return f'''<!doctype html>
<html lang="{lang}"{" data-demo" if DEMO else ""}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#0E1626">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="{lang}" href="{url}">
<link rel="alternate" hreflang="{o}" href="{abs_u(key, o)}">
<link rel="alternate" hreflang="x-default" href="{abs_u(key, "es")}">
<link rel="alternate" type="text/plain" href="{DOMAIN}/llms.txt" title="LLMs.txt">
<meta property="og:type" content="{ot}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{LOCALE[lang]}">
<meta property="og:locale:alternate" content="{LOCALE[o]}">
<meta property="og:image" content="{DOMAIN}/assets/{og}.jpg">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(OG_ALT.get(key, OG_ALT["home"])[0 if lang == "es" else 1])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/{og}.jpg">
<meta name="twitter:image:alt" content="{esc(OG_ALT.get(key, OG_ALT["home"])[0 if lang == "es" else 1])}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/icons/icon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="application-name" content="{NAME}">
<meta name="apple-mobile-web-app-title" content="JA Borges">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="format-detection" content="telephone=no">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{pre}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300;1,6..72,400&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js"></script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
<a class="skip" href="#main">{t(lang, "Saltar al contenido", "Skip to content")}</a>
{header(lang, key)}
<main id="main">
{body}
</main>
{footer(lang)}
{f'<div class="note">{t(lang, "Maqueta · datos de ejemplo (teléfono, correo y redes pendientes)", "Mockup · sample data (phone, email and social pending)")}</div>' if DEMO else ""}
<script src="/assets/qrcode.min.js"></script>
<script src="/assets/kit.js"></script>
<script src="/assets/consent.js"></script>
</body>
</html>
'''

def contact_btn(lang, label_es, label_en, cls="btn", msg=None):
    m = f' data-message="{esc(msg)}"' if msg else ""
    return f'<a class="{cls}" href="{u("contact", lang)}" data-contact{m}>{t(lang, label_es, label_en)}</a>'

# ---------------------------------------------------------------- páginas
def home(lang):
    L = lambda es, en: t(lang, es, en)
    hero = f'''<section class="hero">
  {picture("controlas", lang, "100vw", eager=True)}
  <div class="wrap">
    <p class="eyebrow">{L("Ejecutivo · Emprendedor · Real Estate", "Business Leader · Entrepreneur · Real Estate Executive")}</p>
    <h1 class="display"><span class="sr">{NAME}. </span>{L("Construir. <em>Escalar. Transformar.</em>", "Build. <em>Scale. Transform.</em>")}</h1>
    <p class="sub">{L("Para quienes dirigen agencias y equipos inmobiliarios: cómo crecer con orden, sin perder el control ni la autonomía de las personas.", "For those who run real estate agencies and teams: how to grow in an orderly way, without losing control or people’s autonomy.")}</p>
    <div class="cta">{contact_btn(lang, "Conversemos", "Let's talk", "btn", L("Hola José Antonio, me gustaría conversar contigo.", "Hello José Antonio, I'd like to have a conversation with you."))}<a class="ulink" href="{u("exp", lang)}">{L("Conoce mi trayectoria", "Explore my experience")}</a></div>
  </div>
  <div class="now"><span>{L("Actualmente", "Currently")}</span><b>{L("Country Leader, eXp Realty España", "Country Leader, eXp Realty Spain")}</b></div>
</section>'''
    intro = f'''<section class="intro" id="sobre"><div class="wrap">
  <figure class="rv">{picture("hero", lang, "(max-width: 860px) 90vw, 420px")}<figcaption>{NAME} · {L("eXp Realty España", "eXp Realty Spain")}</figcaption></figure>
  <div class="rv">
    <p class="kick">{L("Enfoque", "Approach")}</p>
    <h2>{L("El crecimiento es el resultado. <em>Los sistemas hacen que pueda repetirse.</em>", "Growth is the outcome. <em>Systems make it repeatable.</em>")}</h2>
    <p class="lead">{L("Crecer es la parte fácil de contar. Lo difícil es hacerlo sin perder el control ni a tu gente.", "Growing is the easy part to talk about. The hard part is doing it without losing control or your people.")}</p>
    <p class="txt">{L("Medir lo importante, anticipar los problemas y darle autonomía a las personas. Cuéntame qué estás intentando resolver y vemos si puedo aportarte algo.", "Measure what matters, spot problems early and give people autonomy. Tell me what you are trying to solve and we'll see if I can add something.")}</p>
    <div class="cta-row"><a class="ulink" href="{u("about", lang)}" style="color:var(--ink)">{L("Mi historia", "My story")}</a>{contact_btn(lang, "Conversemos", "Let's talk", "ulink", L("Hola José Antonio, me gustaría conversar contigo.", "Hello José Antonio, I'd like to have a conversation with you."))}</div>
  </div>
</div></section>'''
    res = f'''<section style="padding-top:0"><div class="wrap rv">
  <p class="kick">{L("Resultados", "Track record")}</p>
  <h2>{L("Del desafío <em>al resultado.</em>", "From challenge <em>to outcome.</em>")}</h2>
  <div class="rows">
    <div class="row"><span class="n">+120 %</span><h3>{L("Crecimiento con rentabilidad", "Growth with profitability")}</h3><p>{L("eXp Realty España: +120 % de facturación en 22 meses y rentabilidad en 2026.", "eXp Realty Spain: +120% revenue in 22 months and profitability in 2026.")}</p></div>
    <div class="row"><span class="n">Hauzz</span><h3>{L("De la idea a la adquisición", "From idea to acquisition")}</h3><p>{L("Hauzz: fundado, desarrollado y vendido a Rive.", "Hauzz: founded, scaled and sold to Rive.")}</p></div>
    <div class="row"><span class="n">~250</span><h3>{L("Una red construida desde cero", "A network built from scratch")}</h3><p>{L("Unos 250 agentes en España y Portugal, construidos desde cero en Tiko.", "About 250 agents across Spain and Portugal, built from scratch at Tiko.")}</p></div>
  </div>
  <figure class="band">{picture("lidera", lang, "(max-width: 1180px) 100vw, 1180px")}</figure>
  <p class="cta-line">{L("¿Quieres saber cómo se logró?", "Want to know how it was done?")} {contact_btn(lang, "Pregúntamelo en una conversación", "Ask me in a conversation", "ulink", L("Hola José Antonio, me gustaría que me cuentes cómo lograste estos resultados.", "Hello José Antonio, I'd like you to tell me how you achieved these results."))}</p>
</div></section>'''
    topic_rows = "".join(f'<a class="row topic" href="{u("contact", lang)}" data-contact data-message="{esc(L("Hola José Antonio, me identifico con esto: «", "Hello José Antonio, this sounds like me: “") + L(a, b) + L("». Me gustaría conversar contigo.", "”. I'd like to talk with you."))}"><span class="n2">0{i+1}</span><h3>{L(a, b)}</h3><span class="go">{L("Conversemos →", "Let's talk →")}</span></a>' for i, (a, b) in enumerate(TOPICS))
    topics = f'''<section class="topics" id="temas"><div class="wrap rv">
  <p class="kick">{L("¿Te suena?", "Sound familiar?")}</p>
  <h2>{L("¿Qué estás intentando <em>resolver?</em>", "What are you trying <em>to solve?</em>")}</h2>
  <p class="topics-p">{L("Elige lo que más se parezca a tu situación y lo conversamos.", "Pick what looks most like your situation and let's talk it through.")}</p>
  <div class="topics-grid"><figure class="tph">{picture("cero", lang, "(max-width: 900px) 90vw, 360px")}</figure><div class="rows">{topic_rows}</div></div>
</div></section>'''
    V2ROWS = {"exp": ("Country Leader / MD", "eXp Realty España", "eXp Realty Spain"), "hauzz": ("Founder &amp; CEO", "Hauzz", "Hauzz"), "rive": ("Brokerage", "Rive / Kodit", "Rive / Kodit"), "tiko": ("Head of Brokerage", "Tiko · ES + PT", "Tiko · ES + PT"), "pe": ("Senior Acquisitions Associate", "Private Equity · EE. UU.", "Private Equity · US")}
    tray_rows = "".join(f'<a class="row" href="{u("exp", lang)}#{i}"><span class="role">{V2ROWS[i][0]}</span><h3>{L(V2ROWS[i][1], V2ROWS[i][2])}</h3><p>{L(*hd)}</p></a>' for i, comp, role, hd, pp, hl in EXP)
    tray = f'''<section class="dark" id="trayectoria"><div class="wrap rv">
  <div class="tray-h"><div><p class="kick">{L("Trayectoria", "Experience")}</p>
  <h2>{L("El recorrido detrás <em>de cada resultado.</em>", "The path behind <em>every result.</em>")}</h2></div>
  <figure class="tph2">{picture("country", lang, "(max-width: 900px) 90vw, 440px")}</figure></div>
  <div class="rows">{tray_rows}</div>
  <p class="cta-line" style="color:#c5cde0">{L("¿Te interesa alguna de estas etapas?", "Interested in any of these stages?")} {contact_btn(lang, "Cuéntame y lo conversamos", "Tell me and let's talk it through", "ulink", L("Hola José Antonio, me gustaría conversar sobre tu trayectoria.", "Hello José Antonio, I'd like to talk about your career."))}</p>
</div></section>'''
    split = f'''<section class="split">
  {picture("cierre", lang, "(max-width: 860px) 100vw, 50vw")}
  <div>
    <p class="kick" style="color:#9db9ea">{L("La disciplina", "Discipline")}</p>
    <h2 class="q">{L("“No controlas el resultado. Sí controlas tu siguiente paso.”", "“You don't control the outcome. You do control your next step.”")}</h2>
    <p>{L("El marcador no se controla; el proceso, sí. Preparación, análisis riguroso y constancia: la disciplina del deporte de alto rendimiento llevada a la dirección de equipos y empresas.", "You don’t control the scoreboard; you do control the process. Preparation, rigorous analysis and consistency: the discipline of high-performance sport, applied to leading teams and companies.")}</p>
    {contact_btn(lang, "Invítame a tu evento o podcast", "Invite me to your event or podcast", "ulink", L("Hola José Antonio, me gustaría invitarte a nuestro evento o podcast.", "Hello José Antonio, I'd like to invite you to our event or podcast."))}
  </div>
</section>'''
    ints = "".join(f'<a class="intent" href="{u("contact", lang)}" data-contact data-message="{esc(L(c, d))}"><small>{L(sa, sb)}</small><b>{L(a, b)} →</b></a>' for (sa, sb), (a, b, c, d) in zip((("Entrevistas", "Interviews"), ("Alianzas", "Partnerships"), ("Negocio", "Business"), ("Capital", "Capital")), REASONS[:4]))
    cont = f'''<section class="contact" id="contacto">{picture("audiencia", lang, "100vw", cls="cbg")}<div class="wrap rv">
  <p class="kick" style="color:#9db9ea">{L("Contacto", "Contact")}</p>
  <h2>{L("Las buenas oportunidades <em>empiezan con una conversación.</em>", "Great opportunities <em>often begin with a conversation.</em>")}</h2>
  <p style="color:#b6c1d6;max-width:56ch;margin:-24px 0 40px;font-size:1.1rem">{L("Cuéntame qué estás intentando resolver. Si puedo aportar algo, lo conversamos. También para entrevistas, podcasts y eventos.", "Tell me what you are trying to solve. If I can add something, let’s talk. Also for interviews, podcasts and events.")}</p>
  <div class="intents">{ints}</div>
</div></section>'''
    wp = {"@type": "WebPage", "@id": abs_u("home", lang) + "#page", "url": abs_u("home", lang), "name": META["home"][lang][0], "description": META["home"][lang][1],
          "inLanguage": lang, "isPartOf": {"@id": DOMAIN + "/#web"}, "about": {"@id": DOMAIN + "/#persona"}, "primaryImageOfPage": {"@type": "ImageObject", "url": DOMAIN + "/img/controlas-1600.jpg"}}
    return hero + intro + res + topics + tray + split + cont, [wp, crumbs(lang, "home")]

def about(lang):
    L = lambda es, en: t(lang, es, en)
    hero = f'''<section class="ahero"><div class="wrap">
  <div>
    <p class="crumb"><a href="{u("home", lang)}">{L("Inicio", "Home")}</a> / {L("Sobre mí", "About")}</p>
    <h1>{L("Sobre mí", "About me")}</h1>
    <p class="ent">{L("Mi carrera se ha desarrollado alrededor de una misma idea: entender qué hace funcionar a un negocio y construir las condiciones para que crezca.", "My career has revolved around a simple question: what makes a business work, and what does it take to build the conditions for it to grow?")}</p>
  </div>
  <figure>{picture("barcelona", lang, "(max-width: 860px) 90vw, 420px", eager=True, style="object-position:43% 50%")}</figure>
</div></section>'''
    glance = f'''<section class="glance" style="padding:0"><div class="wrap"><dl>
  <div><dt>{L("Actualmente", "Currently")}</dt><dd>{L("Country Leader, eXp Realty España", "Country Leader, eXp Realty Spain")}</dd></div>
  <div><dt>{L("Fundó", "Founded")}</dt><dd>Hauzz</dd></div>
  <div><dt>{L("Formación", "Education")}</dt><dd>{L("Matemáticas y Economía · Universidad de Miami", "Mathematics &amp; Economics · University of Miami")}</dd></div>
  <div><dt>{L("Especialidad", "Focus")}</dt><dd>{L("Real estate, liderazgo y escalabilidad", "Real estate, leadership and scaling")}</dd></div>
</dl></div></section>'''
    paras = "".join(f'<p>{L(a, b)}</p>' for a, b in BIO)
    bio = f'''<section><div class="wrap bio">
  <aside aria-label="{L("En esta página", "On this page")}"><a href="#biografia">{L("Biografía", "Biography")}</a><a href="#filosofia">{L("Filosofía", "Philosophy")}</a><a href="#formacion">{L("Formación", "Education")}</a><a href="#preguntas">{L("Preguntas frecuentes", "FAQ")}</a></aside>
  <div class="prose" id="biografia"><h2>{L("Biografía", "Biography")}</h2>{paras}
  <p><a href="{u("exp", lang)}">{L("Más detalle de cada etapa en Trayectoria", "More detail on each stage in Experience")}</a>.</p>
  <p>{L("¿Quieres conversar sobre alguna de estas etapas o entrevistarme?", "Want to talk about any of these stages, or interview me?")} {contact_btn(lang, "Escríbeme", "Write to me", "ulink", L("Hola José Antonio, me gustaría entrevistarte.", "Hello José Antonio, I'd like to interview you."))}</p></div>
</div></section>'''
    aud_rows = "".join(f'<a class="row aud-r" href="{u("contact", lang)}" data-contact data-message="{esc(L(e, f))}"><span class="role">{L(a, b)}</span><h3>{L(c, d)}</h3><span class="go">{L("Conversemos →", "Let's talk →")}</span></a>' for a, b, c, d, e, f in AUDIENCES)
    aud = f'''<section class="aud" id="para-quien" style="padding-top:0"><div class="wrap">
  <p class="kick">{L("¿Para quién?", "Who is it for?")}</p>
  <h2>{L("Si te identificas, <em>conversemos.</em>", "If this is you, <em>let's talk.</em>")}</h2>
  <div class="rows">{aud_rows}</div>
</div></section>'''
    phil = f'''<section class="phil" id="filosofia"><div class="wrap">
  <p class="kick" style="color:#9db9ea">{L("Filosofía de liderazgo", "Leadership philosophy")}</p>
  <h2>{L("Autonomía con responsabilidad. <em>Crecimiento con método.</em>", "Autonomy with accountability. <em>Growth with discipline.</em>")}</h2>
  <p>{L("Una organización sólida no necesita multiplicar reglas para tener control. Necesita claridad, procesos, indicadores útiles y equipos capaces de actuar a tiempo. La disciplina operativa debe liberar capacidad, no convertirse en burocracia.", "Strong organizations don't need more rules for the sake of control. They need clarity, effective processes, meaningful metrics and teams empowered to act early. Operational discipline should enable people, not create bureaucracy.")}</p>
</div></section>'''
    edu = f'''<section id="formacion"><div class="wrap edu">
  <div><p class="kick">{L("Formación", "Education")}</p><h2>{L("Matemáticas <em>y Economía.</em>", "Mathematics <em>&amp; Economics.</em>")}</h2></div>
  <div><p>{L("Estudios de posgrado en Matemáticas en la Universidad de Miami, con experiencia en docencia universitaria.", "Postgraduate study in Mathematics at the University of Miami, with university teaching experience.")}</p>
  <p style="margin-top:18px">{L("El deporte, la familia y el aprendizaje continuo siguen siendo partes importantes de mi vida. Mi traslado a España fue también una elección personal: quería emprender y construir una vida más cerca de mi familia.", "Sport, family and continuous learning remain important parts of my life. Moving to Spain was both a professional and personal decision: I wanted to build something of my own and live closer to family.")}</p></div>
</div></section>'''
    areas = f'''<section class="dark"><div class="wrap">
  <p class="kick">{L("Áreas de conocimiento", "Expertise")}</p>
  <h2>{L("Las ideas que impulsan <em>mi trabajo.</em>", "The ideas behind <em>my work.</em>")}</h2>
  <div class="areas">{"".join(f'<div class="area"><span>0{i+1}</span><h3>{L(a, b)}</h3><p>{L(c, d)}</p></div>' for i, (a, b, c, d) in enumerate(AREAS))}</div>
</div></section>'''
    faq = f'''<section style="padding-top:0;margin-top:96px" id="preguntas"><div class="wrap">
  <p class="kick">{L("Preguntas frecuentes", "FAQ")}</p>
  <h2 style="margin-bottom:32px">{L("Lo esencial, <em>en breve.</em>", "The essentials, <em>in brief.</em>")}</h2>
  <div class="faq">{"".join(f"<details><summary>{L(a, b)}</summary><p>{L(c, d)}</p></details>" for a, b, c, d in FAQ)}</div>
</div></section>'''
    cont = f'''<section class="contact" style="background:var(--ink);color:#fff"><div class="wrap">
  <p class="kick" style="color:#9db9ea">{L("Contacto", "Contact")}</p>
  <h2 style="max-width:16ch;margin-bottom:34px">{L("Las buenas oportunidades <em>empiezan con una conversación.</em>", "Great opportunities <em>often begin with a conversation.</em>")}</h2>
  {contact_btn(lang, "Entrevístame", "Interview me", "btn", L("Hola José Antonio, me gustaría entrevistarte.", "Hello José Antonio, I'd like to interview you."))}
</div></section>'''
    ld = [{"@type": "AboutPage", "@id": abs_u("about", lang) + "#page", "url": abs_u("about", lang), "name": META["about"][lang][0], "description": META["about"][lang][1], "inLanguage": lang,
           "isPartOf": {"@id": DOMAIN + "/#web"}, "about": {"@id": DOMAIN + "/#persona"}, "mainEntity": {"@id": DOMAIN + "/#persona"}},
          crumbs(lang, "about"),
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": L(a, b), "acceptedAnswer": {"@type": "Answer", "text": L(c, d)}} for a, b, c, d in FAQ]}]
    return hero + glance + bio + aud + phil + edu + areas + faq + cont, ld

def exp(lang):
    L = lambda es, en: t(lang, es, en)
    head = f'''<section class="pgh"><div class="wrap">
  <p class="crumb"><a href="{u("home", lang)}">{L("Inicio", "Home")}</a> / {L("Trayectoria", "Experience")}</p>
  <h1>{L("Trayectoria y resultados", "Experience &amp; results")}</h1>
  <p class="ent">{L("He trabajado en distintas etapas del ciclo empresarial: analizar inversiones, crear negocios, ampliar operaciones, construir equipos y transformar modelos de gestión.", "I've worked across different stages of the business lifecycle: evaluating investments, founding companies, scaling operations, developing teams and transforming management systems.")}</p>
</div></section>'''
    items = ""
    for i, comp, role, hd, paras, hl in EXP:
        ps = "".join(f"<p>{L(a, b)}</p>" for a, b in paras)
        hls = (f'<p class="hl">{L(*hl)}</p>' if hl else "") + f'<p class="useful"><b>{L("Útil si", "Useful if")}</b> {L(*USEFUL[i])}</p>'
        items += f'<article class="xp" id="{i}"><div><p class="role" style="font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600">{L(*role)}</p></div><div><h2>{comp}</h2><p class="hd">{L(*hd)}</p>{ps}{hls}</div></article>'
    body = f'''<section style="padding:72px 0 0"><div class="wrap">{items}</div></section>
<section class="dark" style="margin-top:96px"><div class="wrap">
  <h2 style="max-width:20ch;margin-bottom:28px">{L("Mi trayectoria tiene un hilo conductor.", "A consistent thread runs through my career.")}</h2>
  <p style="color:#c5cde0;max-width:58ch;margin-bottom:34px;font-size:1.15rem">{L("Construir organizaciones con una dirección clara, los equipos adecuados y los sistemas necesarios para ejecutar.", "Building organizations with strategic direction, capable teams and the systems required to execute.")}</p>
  {contact_btn(lang, "Conversemos sobre esta trayectoria", "Let's talk about this journey", "btn", L("Hola José Antonio, me gustaría conversar sobre tu trayectoria.", "Hello José Antonio, I'd like to talk about your career."))}
</div></section>'''
    ld = [{"@type": "WebPage", "@id": abs_u("exp", lang) + "#page", "url": abs_u("exp", lang), "name": META["exp"][lang][0], "description": META["exp"][lang][1], "inLanguage": lang, "isPartOf": {"@id": DOMAIN + "/#web"}, "about": {"@id": DOMAIN + "/#persona"}},
          crumbs(lang, "exp"),
          {"@type": "ItemList", "name": L("Trayectoria profesional", "Professional experience"), "itemListElement": [{"@type": "ListItem", "position": n + 1, "name": f"{L(*role)} · {comp}".replace("&amp;", "&"), "url": abs_u("exp", lang) + "#" + i} for n, (i, comp, role, hd, p, hl) in enumerate(EXP)]}]
    return head + body, ld

def contact(lang):
    L = lambda es, en: t(lang, es, en)
    head = f'''<section class="pgh"><div class="wrap">
  <p class="crumb"><a href="{u("home", lang)}">{L("Inicio", "Home")}</a> / {L("Contacto", "Contact")}</p>
  <h1>{L("Conectemos.", "Let's connect.")}</h1>
  <p class="ent">{L("Entrevistas, podcasts, eventos, alianzas o una primera conversación. Me interesa conocer a personas y organizaciones que estén creando empresas, desarrollando ideas y construyendo proyectos con ambición a largo plazo. Si crees que podemos intercambiar perspectivas o explorar una colaboración, estaré encantado de conocerte.", "Interviews, podcasts, events, partnerships or a first conversation. I enjoy meeting people and organizations building businesses, developing ideas and pursuing ambitious long-term projects. If you think there is room to exchange perspectives or explore a collaboration, I'd be glad to hear from you.")}</p>
</div></section>'''
    reasons = "".join(f'<a class="reason" href="{u("contact", lang)}" data-contact data-message="{esc(L(c, d))}"><span>{L(a, b)}</span><span aria-hidden="true">→</span></a>' for a, b, c, d in REASONS)
    body = f'''<section><div class="wrap">
  <h2>{L("¿Sobre qué quieres <em>hablar?</em>", "What would you like <em>to discuss?</em>")}</h2>
  <div class="reasons">{reasons}</div>
  <p style="margin-top:28px;color:var(--mute);max-width:60ch;font-size:.92rem">{L("Al elegir un motivo se prepara un mensaje en tu dispositivo y eliges cómo enviarlo: llamada, SMS, WhatsApp o email. Esta web no guarda tus datos.", "Choosing a reason prepares a message on your device, and you pick how to send it: call, SMS, WhatsApp or email. This website does not store your data.")}</p>
</div></section>
<section class="dark" id="agendar"><div class="wrap">
  <p class="kick">{L("Agenda", "Schedule")}</p>
  <h2 style="margin-bottom:22px">{L("Una conversación, <em>sin compromiso.</em>", "A conversation, <em>no strings attached.</em>")}</h2>
  <p style="color:#c5cde0;max-width:54ch;margin-bottom:30px;font-size:1.1rem">{L("Escríbeme y coordinamos un momento para hablar.", "Write to me and we'll find a time to talk.")}</p>
  {contact_btn(lang, "Escribirme", "Write to me")}
</div></section>'''
    ld = [{"@type": "ContactPage", "@id": abs_u("contact", lang) + "#page", "url": abs_u("contact", lang), "name": META["contact"][lang][0], "description": META["contact"][lang][1], "inLanguage": lang, "isPartOf": {"@id": DOMAIN + "/#web"}, "about": {"@id": DOMAIN + "/#persona"}},
          crumbs(lang, "contact")]
    return head + body, ld

def legal(lang, kind):
    L = lambda es, en: t(lang, es, en)
    ctx = {"NAME": NAME, "DOMAIN": DOMAIN, "UPDATED": UPDATED, "u": u}
    h1, intro, body_html, _ = legal_content.doc(kind, lang, ctx)
    body = (f'<section class="pgh"><div class="wrap"><p class="crumb"><a href="{u("home", lang)}">{L("Inicio", "Home")}</a> / {h1}</p><h1>{h1}</h1><p class="ent">{intro}</p></div></section>'
            f'<section><div class="wrap"><div class="prose">{body_html}</div></div></section>')
    return body, [crumbs(lang, kind)]

BUILDERS = {"home": home, "about": about, "exp": exp, "contact": contact, "legal": lambda l: legal(l, "legal"), "privacy": lambda l: legal(l, "privacy"), "terms": lambda l: legal(l, "terms"), "cookies": lambda l: legal(l, "cookies")}

# ---------------------------------------------------------------- archivos de sitio
def write(path, txt):
    p = os.path.join(OUT, path.lstrip("/")); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(txt)

def sitemap():
    xs = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key in INDEXABLE:
        for lang in ("es", "en"):
            o = OTHER[lang]
            xs += ["  <url>", f"    <loc>{abs_u(key, lang)}</loc>", f"    <lastmod>{LASTMOD}</lastmod>",
                   f'    <xhtml:link rel="alternate" hreflang="es" href="{abs_u(key, "es")}"/>',
                   f'    <xhtml:link rel="alternate" hreflang="en" href="{abs_u(key, "en")}"/>',
                   f'    <xhtml:link rel="alternate" hreflang="x-default" href="{abs_u(key, "es")}"/>',
                   f"    <priority>{'1.0' if key == 'home' else '0.8'}</priority>", "  </url>"]
    xs.append("</urlset>")
    return "\n".join(xs) + "\n"

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot"]

def robots():
    if STAGING: return "User-agent: *\nDisallow: /\n"
    r = "# robots.txt de joseantonioborges.com\nUser-agent: *\nAllow: /\n\n# Buscadores y asistentes de IA: bienvenidos\n"
    for b in AI_BOTS: r += f"User-agent: {b}\nAllow: /\n\n"
    return r + f"Sitemap: {DOMAIN}/sitemap.xml\n"

def clean(s): return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&")

def llms():
    s = f"""# {NAME}

> {NAME} es ejecutivo y emprendedor con trayectoria internacional en inversión, creación de empresas y liderazgo, especializado en el sector inmobiliario en España. Actualmente lidera eXp Realty España. / {NAME} is an executive and entrepreneur with an international background in investment, company building and leadership, focused on real estate in Spain. He currently leads eXp Realty Spain.

Sitio oficial bilingüe (español e inglés). Cada página tiene su equivalente en el otro idioma. Los hechos de esta lista proceden de la propia web y de {NAME}.

## Español
"""
    for key in INDEXABLE: s += f"- [{META[key]['es'][0]}]({abs_u(key, 'es')}): {META[key]['es'][1]}\n"
    s += "\n## English\n"
    for key in INDEXABLE: s += f"- [{META[key]['en'][0]}]({abs_u(key, 'en')}): {META[key]['en'][1]}\n"
    s += f"""
## Datos clave / Key facts
- Cargo actual / Current role: Country Leader / Managing Director, eXp Realty España (Spain).
- eXp Realty España: facturación +120 % en 22 meses; rentabilidad alcanzada en 2026 / revenue +120% in 22 months; profitability reached in 2026.
- Hauzz: fundador y CEO; red de cientos de agentes; adquirida por Rive / founder & CEO; network of hundreds of agents; acquired by Rive.
- Rive / Kodit: unos 18 meses en los que el negocio de intermediación casi duplicó su facturación / about 18 months in which the brokerage business nearly doubled revenue.
- Tiko: Head of Brokerage, España y Portugal; red de unos 250 agentes / Spain & Portugal; network of about 250 agents.
- Private equity (EE. UU. / US): Senior Acquisitions Associate; participó en procesos de adquisición con un volumen agregado aproximado de US$250 M en un año (no es inversión personal) / participated in acquisition processes totalling about US$250M in one year (not personal investment).
- Formación / Education: Matemáticas y Economía; posgrado en Matemáticas, University of Miami / Mathematics & Economics; postgraduate Mathematics, University of Miami.

## Problemas en los que puede aportar / Problems he can help with
""" + "\n".join(f"- {a} / {b}" for a, b in TOPICS) + f"""

Contacto para entrevistas, podcasts, eventos y colaboraciones: {abs_u('contact', 'es')} / Contact for interviews, podcasts, events and collaborations: {abs_u('contact', 'en')}.

## Blog
- [Blog]({BLOG_URL}): artículos y perspectivas / articles and perspectives (sitio aparte / separate site)

## Optional
- [llms-full.txt]({DOMAIN}/llms-full.txt): contenido completo del sitio en texto / full site content in plain text.
"""
    return s

def llms_full():
    s = f"# {NAME} — contenido completo / full content\n\nFuente / Source: {DOMAIN} · Actualizado / Updated: {LASTMOD}\n"
    for lang in ("es", "en"):
        L = lambda es, en: t(lang, es, en)
        s += f"\n\n# {'ESPAÑOL' if lang == 'es' else 'ENGLISH'}\n\n## {L('Sobre mí', 'About')} ({abs_u('about', lang)})\n\n"
        s += "\n\n".join(clean(L(a, b)) for a, b in BIO)
        s += f"\n\n## {L('Trayectoria', 'Experience')} ({abs_u('exp', lang)})\n"
        for i, comp, role, hd, paras, hl in EXP:
            s += f"\n### {clean(comp)} — {clean(L(*role))}\n{clean(L(*hd))}\n\n" + "\n\n".join(clean(L(a, b)) for a, b in paras) + f"\n\n{L('Útil si', 'Useful if')} {clean(L(*USEFUL[i]))}\n"
        s += f"\n## {L('Áreas de conocimiento', 'Expertise')}\n" + "\n".join(f"- {clean(L(a, b))}: {clean(L(c, d))}" for a, b, c, d in AREAS)
        s += f"\n\n## {L('¿Para quién es útil conversar?', 'Who is it useful to talk with?')}\n" + "\n".join(f"- {clean(L(a, b))}: {clean(L(c, d))}" for a, b, c, d, e, f in AUDIENCES)
        s += f"\n\n## {L('Problemas en los que puede aportar', 'Problems he can help with')}\n" + "\n".join(f"- {L(a, b)}" for a, b in TOPICS)
        s += f"\n\n## {L('Preguntas frecuentes', 'FAQ')}\n" + "\n\n".join(f"**{clean(L(a, b))}**\n{clean(L(c, d))}" for a, b, c, d in FAQ)
        s += f"\n\n## {L('Contacto', 'Contact')} ({abs_u('contact', lang)})\n" + L("Contacto mediante la página de contacto: llamada, SMS, WhatsApp o email.", "Contact via the contact page: call, SMS, WhatsApp or email.") + "\n"
    return s

HEADERS = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), interest-cohort=()
  Cross-Origin-Opener-Policy: same-origin
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests

/es/*
  Cache-Control: public, max-age=0, must-revalidate
/en/*
  Cache-Control: public, max-age=0, must-revalidate
/assets/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400
/img/*
  Cache-Control: public, max-age=31536000, immutable
/robots.txt
  Cache-Control: public, max-age=3600
/sitemap.xml
  Cache-Control: public, max-age=3600
/llms.txt
  Cache-Control: public, max-age=3600
/llms-full.txt
  Cache-Control: public, max-age=3600
"""

def icons():
    d = os.path.join(OUT, "assets", "icons"); os.makedirs(d, exist_ok=True)
    if all(os.path.exists(os.path.join(d, f"icon-{n}.png")) for n in (32, 180, 192, 512)): return True
    try:
        from PIL import Image, ImageDraw, ImageFont
        for size in (32, 180, 192, 512):
            im = Image.new("RGB", (size, size), "#0E1626"); dr = ImageDraw.Draw(im)
            f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", int(size * .5))
            tx = "JB"; bb = dr.textbbox((0, 0), tx, font=f)
            dr.text(((size - (bb[2] - bb[0])) / 2 - bb[0], (size - (bb[3] - bb[1])) / 2 - bb[1]), tx, font=f, fill="#F4F0E8")
            im.save(os.path.join(d, f"icon-{size}.png"))
        return True
    except Exception as e:
        print("Iconos PNG omitidos:", e); return False

import hashlib
def ver(path):
    return hashlib.sha1(open(os.path.join(OUT, path.lstrip("/")), "rb").read()).hexdigest()[:8]

def bust(html):
    """Añade ?v=<hash> a los archivos de /assets para que la caché larga nunca sirva versiones viejas."""
    return re.sub(r'(/assets/(?:site\.css|site\.js|kit\.js|consent\.js|qrcode\.min\.js))(?=")', lambda m: m.group(1) + "?v=" + ver(m.group(1)), html)

def main():
    os.makedirs(OUT, exist_ok=True)
    build_images()
    icons_ok = icons()
    for key in PAGES:
        for lang in ("es", "en"):
            body, ld = BUILDERS[key](lang)
            lcp = ("controlas", "100vw") if key == "home" else (("barcelona", "(max-width: 860px) 90vw, 420px") if key == "about" else None)
            og = f"og/og-{key}-{lang}" if key in OG_ALT else f"og/og-home-{lang}"
            write(PAGES[key][lang] + "index.html", bust(page(key, lang, body, ld, lcp, og)))
    write("/index.html", f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{NAME}</title>
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="{'noindex' if STAGING else 'noindex, follow'}">
<link rel="canonical" href="{DOMAIN}/es/"><meta http-equiv="refresh" content="0; url=/es/">
<link rel="alternate" hreflang="es" href="{DOMAIN}/es/"><link rel="alternate" hreflang="en" href="{DOMAIN}/en/"><link rel="alternate" hreflang="x-default" href="{DOMAIN}/es/"></head>
<body><p><a href="/es/">Español</a> · <a href="/en/">English</a></p></body></html>
''')
    write("/404.html", bust(f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>404 | {NAME}</title><meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="/assets/site.css"></head>
<body style="background:var(--night);color:#fff;min-height:100vh;display:grid;place-items:center;text-align:center;padding:24px">
<main><h1 style="font-family:var(--serif);font-weight:300;font-size:3rem;margin-bottom:18px">404</h1>
<p style="margin-bottom:24px">Esta página no existe. / This page doesn't exist.</p>
<p><a class="btn" href="/es/">Inicio</a> <a class="btn" href="/en/">Home</a></p></main></body></html>
'''))
    write("/robots.txt", robots()); write("/sitemap.xml", sitemap()); write("/llms.txt", llms()); write("/llms-full.txt", llms_full())
    write("/_headers", HEADERS); write("/_redirects", "/  /es/  302\n")
    # favicon.svg, favicon.ico y los íconos de app los genera tools/icons.py
    man = {"id": "/es/", "name": NAME, "short_name": "JA Borges",
           "description": "José Antonio Borges: ejecutivo y emprendedor del sector inmobiliario. Entrevistas, alianzas y conversaciones.",
           "start_url": "/es/", "scope": "/", "display": "standalone", "orientation": "any", "lang": "es", "dir": "ltr",
           "background_color": "#0E1626", "theme_color": "#0E1626", "categories": ["business", "news"],
           "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                     {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                     {"src": "/assets/icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
           "shortcuts": [{"name": "Contacto", "short_name": "Contacto", "url": "/es/contacto/", "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192"}]},
                         {"name": "Trayectoria", "short_name": "Trayectoria", "url": "/es/trayectoria/", "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192"}]}]}
    write("/manifest.webmanifest", json.dumps(man, ensure_ascii=False, indent=1))
    print("OK", "(STAGING)" if STAGING else "(producción)")

if __name__ == "__main__":
    main()
