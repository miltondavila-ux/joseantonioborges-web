# Decisiones aprobadas — sitio José Antonio Borges

Verificadores (deben terminar en 0 fallos antes de entregar cualquier cambio):
`python3 tools/build.py && python3 tools/verificar-seo.py && python3 tools/verificar-decisiones.py`

Referencia de método: el repo https://github.com/miltondavila-ux/milton-davila-web (docs de decisiones, verificadores, respaldos con checksums). Se toma siempre como buen ejemplo.


# ⭐ INDICACIONES DEL PROPIETARIO (2026-11-17) — PREVALECEN sobre todo lo anterior

Fuente: documento «José Antonio Borges — Cambios para la versión 2 de la web». Alcance de esta iteración: contenidos y enfoque (SEO técnico y diseño visual quedan para una fase posterior, sin eliminarse del proyecto).

1. **Posicionamiento:** Líder empresarial · Emprendedor · Real Estate (Business Leader · Entrepreneur · Real Estate Executive). Capacidad de construir, escalar y transformar empresas; real estate como principal fuente de autoridad hoy. **Sin enfoque de consultoría/servicios** en títulos, intros, tarjetas ni llamadas a la acción.
2. **Inicio — hero:** se mantiene el titular «Construir. Escalar. Transformar.». Subtítulo = texto del propietario («Ejecutivo y emprendedor con trayectoria internacional… Actualmente al frente de eXp Realty España.»). Botones: **Conoce mi trayectoria** (principal) y **Sobre mí** (secundario). «Conversemos» NO es la llamada principal.
3. **Inicio — resultados:** +120 % eXp (~22 meses), Hauzz (fundada y vendida a Rive), Tiko (~250 agentes ES/PT) + explicación visible de la transformación operativa de eXp (texto del propietario) + private equity (~US$250 M agregados en un año) fácil de encontrar.
4. **Inicio — «¿Qué estás intentando resolver?» ELIMINADO.** Sustituido por **«Áreas de experiencia»** (5 áreas, como experiencia e intereses, **no servicios**: sin enlaces ni botones).
5. **Sobre mí:** se conserva la base (80 % profesional / 20 % personal). Añadido el párrafo personal (tenis de alto rendimiento, lesión, Matemáticas y Economía), Pensam, y la precisión de que llegó a España en 2019 para emprender y estar cerca de la familia **sin tesis inmobiliaria previa**. FAQ breve (3) y discreta al final.
6. **Trayectoria:** 5 etapas (eXp, Hauzz, Rive/Kodit, Tiko, Private Equity/Pensam) con hechos clave; **eliminados los cierres «Útil si…»**; cada etapa termina con un dato/responsabilidad. Sin explicaciones sobre problemas financieros de Tiko.
7. **Ideas / Insights:** integrado en el sitio (`/es/ideas/`, `/en/insights/`, artículos en `/es/ideas/<slug>/`); **el menú ya no tiene «Blog» externo**. Los artículos los redacta/aprueba José Antonio con su asistente de IA; el desarrollador implementa páginas, plantilla y carga. Contenido en `content/ideas/*.md` (ver su README). **Pendiente:** CMS editable para publicar sin desarrollador (ver «Pendientes»).
8. **Contacto:** **formulario real** (Nombre, Correo, Empresa/organización opcional, Motivo [oportunidad empresarial, alianza, inversión, medios/eventos, otro], Mensaje, «Enviar mensaje»). Entrega a un **correo privado** (variable `CONTACT_TO`, nunca en el código ni visible), confirmación de envío, antispam (trampa, tiempo mínimo, origen, límite por IP, Turnstile opcional) y casilla de privacidad. **Eliminados** llamada, SMS, WhatsApp y teléfono personal; también «Una conversación, sin compromiso». Título «Conectemos.» + texto del propietario.
9. **Conferencias/podcasts/speaking:** sin sección principal ni botones prominentes; solo como prueba secundaria (fotos) y como motivo «Medios o eventos» del formulario. «Cada día empieza 0–0» fuera del Home.
10. **Se conserva:** 5 páginas (Inicio, Sobre mí, Trayectoria, Ideas, Contacto), ES+EN, nombre, dominio previsto, «Construir. Escalar. Transformar.», independencia de eXp, trayectoria y logros, fotos originales del Drive (fase visual).

**Menú vigente:** Inicio · Sobre mí · Trayectoria · Ideas · Contacto · ES/EN (todo interno).
**Se conserva de Milton (no contradicho):** diseño v2, fotos sin repetir, logos de redes sin enlace hasta nuevo aviso, pie minimalista, QR para compartir en el menú móvil, aviso de cookies, textos legales, números de teléfono nunca visibles, cuentas (solo miltondavila-ux / Cloudflare de Milton).

## Pendientes tras esta iteración
- **CMS editable de Ideas** (Decap CMS u otro): requiere un OAuth de GitHub y un flujo de publicación automático (CI) con un token de Cloudflare; hoy los artículos se añaden como archivos Markdown y se despliegan con `build.py` + `wrangler deploy`.
- **Formulario:** definir el correo privado de destino y el proveedor de envío (`RESEND_API_KEY`, `CONTACT_TO`, `CONTACT_FROM` como secretos de Cloudflare). Hasta entonces responde «aún no está activo».
- LinkedIn/Instagram (URLs), dominio, datos legales + revisión, fotos originales del Drive, artículos de lanzamiento (4–6), fuentes alojadas en el propio sitio.

## Reglas de trabajo (de Milton)
1. **Sin regresiones.** Hacer solo lo que se pide. Si se ve otra cosa por arreglar, avisar y esperar el OK. Nunca quitar algo que no se pidió quitar.
2. Antes de tocar una sección, confirmar que es la que se nombró.
3. No inventar datos (cifras, citas, URLs, fechas, números de teléfono). Lo pendiente va marcado como ejemplo/pendiente.
4. Cada cambio de texto se refleja también en SEO/AEO (title, meta, OG, JSON-LD, FAQ, llms.txt, sitemap).

## Dirección de diseño
- **Aprobada: la versión 2** (editorial: papel hueso `#F4F0E8`, azul noche `#0E1626`, serif Newsreader + Inter, hero con la foto del escenario).
- **También gustó la versión 3** = v2 + el kit de contacto, menú y bloque «Agenda una conversación».
- **NO mezclar con la versión 1** (azul/blanco, tarjetas, botones redondos, estilo miltondavila.com).
- Referencias estudiadas: miltondavila.com (parte técnica/SEO/AEO, verificadores), leopareja.com (prueba social, media kit), sitios de Reid Hoffman, Collison, Serhant, Corcoran (ideas de contenido).

## ⚠ REEMPLAZADO (ver «Indicaciones del propietario») — Estructura del Home (= v2 + agenda de la v3 + «Temas»)
1. Hero (foto del escenario, «Construir. Escalar. Transformar.», bloque «Actualmente»).
2. Enfoque (`#sobre`): foto en blanco y negro + titular + «Mi historia».
3. Resultados: filas +120 % · Hauzz · ~250, con invitación «Pregúntamelo en una conversación».
3b. **Temas (nuevo):** 6 temas de entrevista que enlazan al kit de contacto con un mensaje de entrevista ya escrito.
4. Trayectoria (azul noche): 5 filas enlazadas (Country Leader / MD · Founder & CEO · Brokerage · Head of Brokerage · Senior Acquisitions Associate).
5. Disciplina: foto con micrófono, cita 0–0, enlace «Leer: Cada día empieza 0–0».
6. Ideas: 4 filas (Estrategia y operaciones, Emprendimiento, Liderazgo y equipos, Real Estate) + tira de 3 fotos.
7. Contacto: 4 vías (Entrevistas, Alianzas, Negocio, Capital) + bloque «Agenda una conversación».
- Menú: Sobre mí · Trayectoria · Ideas · Contacto · ES/EN. Pie minimalista.

## ⚠ REEMPLAZADO — Comunicación (Super Guía de QR): ya no hay llamada/SMS/WhatsApp; el contacto es un formulario
- Escritorio: ventana con **QR**; móvil: **botones**. Sin formularios.
- Canales: **Llamar, SMS, WhatsApp, Email, Agendar**.
- **El número de teléfono NUNCA se escribe en pantalla** (solo viaja dentro de los enlaces y los QR). El número actual es de ejemplo (`kit.js` → `CONFIG.phone`).
- Ventana de conexión: **fondo azul, QR y letras en blanco**.
- Botón QR en el encabezado (escritorio, «Pásalo a móvil»).
- Menú hamburguesa (móvil): enlaces + **QR para compartir** + selector de idioma + logos de redes.
- **Logos de LinkedIn e Instagram: visibles pero NO clicables hasta nuevo aviso** (en pie y menú). Se activan rellenando `LINKEDIN` / `INSTAGRAM` en `tools/build.py`.
- Footer **minimalista**: © + avisos legales + logos.

## SEO / AEO (al 100 %)
- URLs separadas `/es/…` y `/en/…`, canonical, hreflang es/en/x-default, un solo H1 por página, H2/H3 sin saltos.
- JSON-LD: WebSite, Person, AboutPage/ContactPage/CollectionPage/WebPage, BreadcrumbList, FAQPage (visible), ItemList.
- `robots.txt` (bots de IA permitidos), `sitemap.xml` con alternates, `llms.txt`, `llms-full.txt`, `_headers` (CSP), `_redirects`, `404.html`, manifest e iconos.
- Páginas legales: borradores `noindex`, fuera del sitemap hasta tener datos del titular.

## Página About
Importante para el posicionamiento: resumen de datos clave, biografía, filosofía, formación, áreas de conocimiento, 4 FAQ, lectura relacionada, contacto.

## Pendiente (no inventar)
Teléfono/WhatsApp reales · correo · URLs de LinkedIn e Instagram · dominio · titular legal · masters de fotos y retrato hero limpio · artículos (los redactan José Antonio + ChatGPT) · IDs de Search Console/Bing/analítica · alojar las fuentes en el propio sitio.

## ⚠ REEMPLAZADO — Enfoque «entrevistas / Conversemos» (ahora son secundarios)
- El sitio **no debe leerse como un CV ni como una oda**: debe hablarle a quien quiere conocerlo y **provocar que quieran entrevistarlo o contactarlo**, a lo largo de TODA la página (hero, enfoque, resultados, temas, trayectoria, disciplina, ideas, contacto, About, Trayectoria, Ideas, Contacto).
- Posicionamiento: **exponente de referencia en real estate y en dirección de empresas inmobiliarias**, que invita a **entrevistas, podcasts, eventos y colaboraciones** sin decir «disponible» (suena a búsqueda de empleo; el brief lo prohíbe).
- CTA principal del hero: **«Conversemos»** (abre el kit con mensaje preparado). La vía de contacto n.º 1 es **«Entrevista, podcast o evento»**.
- **No inventar credenciales ni pruebas** (no «coach certificado», no testimonios, no cifras nuevas). Los temas de entrevista salen solo de hechos del brief.
- Cambios quirúrgicos: no se tocó el diseño v2, solo textos, enlaces de invitación y una sección.

## Legal (UE/España)
- Aviso legal (LSSI-CE), Términos y condiciones, Política de privacidad (RGPD/LOPDGDD) y Política de cookies, ES/EN, **borradores** con datos del titular `[PENDIENTE]` y `noindex` hasta completarlos y revisarlos con un profesional.
- Aviso de cookies inferior: Aceptar todas / Rechazar / Configurar (mismo peso), analítica desactivada por defecto, elección 12 meses en `localStorage` (`jab-consent`), evento `jab:consent` para activar analítica futura solo con consentimiento.
- Los archivos de `/assets` llevan `?v=<hash>` (caché larga sin servir versiones viejas).

- **Prohibido en el sitio:** frases tipo «Disponible para…», «Busco…», «Open to work». Se invita con «Conversemos», no con disponibilidad.

## ⚠ REEMPLAZADO — Principio de mensaje «qué resuelve» (el propietario pidió quitar el enfoque de consultoría)
- El sitio **no comunica lo que él hace ni lo presume**: habla de **lo que resuelve y de cómo conecta con la gente que lo necesita**.
- Se aplica así: hero («Para quienes dirigen agencias y equipos inmobiliarios…»), Enfoque (empieza por el lector), Resultados = **«Del desafío al resultado»** (tono ejecutivo, nunca «problemas que ya he resuelto»: suena a defensa), sección **«¿Qué estás intentando resolver?»** (6 problemas), Trayectoria con **«Útil si…»** por etapa, About con **«¿Para quién?»** (4 públicos), cierre «Cuéntame qué estás intentando resolver».
- Todo problema o «útil si» sale de un hecho del brief (eXp +120 %/rentabilidad, Hauzz→Rive, Tiko ~250 agentes, private equity, IA como operador). **No inventar servicios, tarifas ni resultados.**
- La descripción SEO del Home se escribió desde el lector («cómo hacer crecer una agencia inmobiliaria…»).
- **Sin justificarse:** los textos de entrada (hero, Enfoque) no listan credenciales para convencer («fundé…, vendí…, lidero…»). Los hechos viven en Resultados y Trayectoria; el lead habla del lector. (Pedido de Milton: «si lo dices es porque lo necesitas».)
- **Voz ejecutiva y elevada:** evitar fórmulas defensivas o de justificación («ya he resuelto», «lo vendí…»). Títulos vigentes: «Del desafío al resultado» (Resultados) y «El recorrido detrás de cada resultado» (Trayectoria del Home).
- **Sin tono anecdótico ni «pueblerino»:** nada de «Lo aprendí en…», «Es la base con la que…». El bloque de disciplina dice: «El marcador no se controla; el proceso, sí…».
- **Imágenes del Home:** Resultados (franja «Lidérate a ti primero»), ¿Qué estás intentando resolver? (foto del 0–0), Trayectoria (pantalla «Country Leader, Spain») y Contacto (la foto del hero, oscurecida, como cierre).

## ⚠ REEMPLAZADO — Blog externo (ahora «Ideas / Insights» va integrado en el sitio)
- **El blog NO se hace en este sitio**: existirá en otro lugar. La página «Ideas» no existe aquí (ni en sitemap, Home ni About).
- Las 3 fotos que estaban en esa sección del Home se conservan como franja visual («En escena», sin título).
- Cuando exista el blog: enlazarlo desde el menú (nueva pestaña) con su URL real y volver a añadirlo a `llms.txt`.
- **Menú vigente: Inicio · Sobre mí · Trayectoria · BLOG · Contacto · ES/EN.** «BLOG» abre `https://blog.joseantonioborges.com` en pestaña nueva (sitio aparte, ocupa el lugar de «Ideas»).
- **Eliminado a pedido de Milton:** el bloque «Agenda una conversación / Calendario pendiente de configurar» del Home. (El canal AGENDAR del kit de contacto se mantiene.)
- **Foto del 0–0:** la cámara la guarda con orientación EXIF 6; el generador de imágenes la aplica a los píxeles (`prepared()` en `build.py`).

## Imágenes (pedido de Milton, 2026-11-16): NO repetir fotos en todo el sitio
- Cada escena aparece **una sola vez** (ojo: varias fotos son la misma escena con otro ángulo: «No controlas el resultado» ×2, marcador 0–0 ×2; solo se usa una de cada).
- Reparto actual — Home: hero `controlas` · Enfoque `hero` (exp-34) · Resultados `lidera` («Lidérate a ti primero») · ¿Qué estás intentando resolver? `cero` (0–0, IMG_8511) · Trayectoria `country` («Country Leader, Spain») · Disciplina `cierre` · Contacto `audiencia` (fondo). About: `barcelona` (eXpcon Barcelona).
- No usadas a propósito: `JA-00 (6)` y `JA-00 (2)` (misma escena que otras), `portada1…940` (duplicado exacto) y la foto de grupo `ig_…` (terceros, diluye la marca individual).
- Si se añade una foto nueva, debe ser de otra escena. El verificador lo comprueba.

## SIGUIENTE TAREA PEDIDA (anotada 2026-11-16, ejecutar después del despliegue)
**Triple auditoría de «SEO READY»** del sitio (en vivo y en el código):
1. **H1:** uno solo por página, en su sitio, en las 8 páginas indexables (ES y EN) y coherente con el título.
2. **Archivo LLM:** `llms.txt` y `llms-full.txt` completos, con enlaces válidos y datos exactos.
3. **Imágenes OG:** 1200×630 por página (hoy solo hay `og-home` y `og-about`; revisar que cada página tenga la suya, con `og:image:alt`, y que Contacto/Trayectoria no compartan una imagen que no les corresponde).
4. **Íconos para instalar como app en el móvil:** manifest, `apple-touch-icon` (iPhone), íconos 192/512 y *maskable* (Android), `theme-color`, nombre de la app. Probar «Añadir a pantalla de inicio».
5. **Favicon:** SVG + PNG 32 + `.ico` en la raíz; que se vea bien en pestañas claras y oscuras.
Entregable: informe con lo encontrado, lo corregido y lo que queda pendiente, y los verificadores actualizados.

## Cuentas (regla de Milton, 2026-11-16)
- **Todo se sube a la cuenta de GitHub `miltondavila-ux`** y al Cloudflare de «correo privado de la cuenta». No tiene nada que ver con `10minuteswebsite` ni con otras cuentas.
- Al usar `gh`: `GH_TOKEN="$(gh auth token --user miltondavila-ux)"` y comprobar que `gh api user --jq .login` sea `miltondavila-ux`; no cambiar la cuenta activa global.
- En Cloudflare, al conectar GitHub, enlazar `miltondavila-ux`; **nunca** elegir `10minuteswebsite` en el selector.

## Imágenes Open Graph (2026-11-16)
- 8 imágenes de 1200×630 (Home, Sobre mí, Trayectoria, Contacto × ES/EN) en `site/assets/og/og-<página>-<idioma>.jpg`, generadas con `python3 tools/og.py` (Chrome headless). Cada página usa la suya; las legales usan la del Home.
- Diseño: azul noche, serif Newsreader, foto en blanco y negro de la propia página, titular de la página, nombre y dominio. El verificador exige 1200×630, < 600 KB, idioma correcto, `og:image:alt` y `twitter:image:alt`.

## Despliegue (hecho 2026-11-16)
- **Vista previa en línea (staging, noindex):** https://joseantonioborges-web.magiapura.workers.dev/ — Worker `joseantonioborges-web` en el Cloudflare de «correo privado de la cuenta» (cuenta `c94a480fa2021e0aa93ca267d04bd8f1`).
- **Cómo se publica:** `python3 tools/build.py --staging && npx wrangler@latest deploy`, con las credenciales **aisladas** de Milton: `XDG_CONFIG_HOME="/Users/miltondavila/Jose Antonio Borges/.cf-milton" CLOUDFLARE_ACCOUNT_ID=c94a480fa2021e0aa93ca267d04bd8f1`.
- **⚠ El login por defecto de `wrangler` en esta Mac es de OTRA cuenta («correo privado de la cuenta»).** Nunca desplegar sin las variables de arriba. Antes de publicar, comprobar con `wrangler whoami` que el correo sea «correo privado de la cuenta».
- La carpeta `.cf-milton` está fuera del repositorio (no se sube nunca).
- Pendiente para producción: dominio `joseantonioborges.com` en esa cuenta de Cloudflare, `python3 tools/build.py` (sin `--staging`), datos reales y revisión legal.

## ⚠ REEMPLAZADO — Menú con BLOG externo
- **«Inicio / Home» es el primer enlace del menú** (además del logo). Orden final: Inicio · Sobre mí · Trayectoria · BLOG ↗ · Contacto · ES/EN.

## Favicon e íconos de app (auditoría SEO READY)
- Generados con `python3 tools/icons.py`: `favicon.svg`, `favicon.ico` (16/32/48) y `apple-touch-icon.png` (180) en la raíz; `icon-32/180/192/512` y `icon-maskable-512` (con margen de seguridad) en `assets/icons/`. Monograma «JB» con anillo, azul noche y papel hueso.
- Manifest con `id`, `scope`, `short_name` «JA Borges», iconos `any` y `maskable` separados y accesos directos a Contacto y Trayectoria.
