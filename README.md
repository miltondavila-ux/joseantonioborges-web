# joseantonioborges-web

Sitio web personal bilingüe (ES/EN) de José Antonio Borges. Sitio estático, sin servidor ni base de datos.

- `site/` — el sitio **ya generado**. Es lo que se publica (Cloudflare Workers sirve esta carpeta tal cual).
- `tools/build.py` — generador (Python 3). Crea `site/` a partir del contenido y de las fotos originales.
- `tools/verificar-seo.py` y `tools/verificar-decisiones.py` — verificadores. Deben terminar en **0 fallos**.
- `tools/og.py` — genera las 8 imágenes Open Graph (1200×630) con Google Chrome headless.
- `tools/dev-server.py` — servidor local con recarga automática (`http://localhost:8766/es/`).
- `docs/decisiones.md` — decisiones aprobadas del proyecto.
- `wrangler.jsonc` — configuración de Cloudflare Workers (carpeta `./site`).

## Regenerar y verificar

```bash
python3 tools/build.py --staging      # vista previa: noindex y robots.txt con Disallow
python3 tools/build.py                # producción: indexable
python3 tools/verificar-seo.py        # añade --staging si generaste en modo staging
python3 tools/verificar-decisiones.py
```

`build.py` usa `sips` y `cwebp` (macOS) y las fotos originales en `../fotos`, que **no** están en este repositorio. Por eso se sube `site/` ya generado.

## Publicación

Vista previa: https://joseantonioborges-web.magiapura.workers.dev/ (modo **staging**, `noindex`).

```bash
python3 tools/build.py --staging
npx wrangler@latest deploy      # con la sesión de wrangler de la cuenta correcta de Cloudflare
```

Antes de desplegar comprueba con `npx wrangler whoami` que la cuenta sea la del propietario del proyecto.

## Pendiente antes de publicar con dominio

Teléfono/WhatsApp y correo reales · URLs de LinkedIn e Instagram · dominio · datos del titular y revisión legal · fotos originales · artículos del blog (el blog vive en `blog.joseantonioborges.com`).
