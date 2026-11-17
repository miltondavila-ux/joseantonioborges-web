# Auditoría SEO READY — 2026-11-16 (vista previa en línea)

Sitio auditado: https://joseantonioborges-web.magiapura.workers.dev/ (staging, `noindex`) y el mismo código en modo producción.

## Resultado

| Área | Estado | Detalle |
|---|---|---|
| **H1** | ✅ | 16 páginas, 1 H1 cada una, primer encabezado, coherente con la página. Corregido el espacio en el H1 del Home («Build. Scale.»). |
| **Jerarquía H2/H3** | ✅ | Sin saltos de nivel (verificador). |
| **llms.txt / llms-full.txt** | ✅ | H1 + resumen + secciones ES/EN + datos clave + problemas en los que aporta + enlace al blog. `llms-full.txt` ahora incluye «Útil si…», públicos y fecha. Sin teléfonos. |
| **Imágenes OG** | ✅ | 8 imágenes 1200×630 (Home, Sobre mí, Trayectoria, Contacto × ES/EN), con `og:image:alt`/`twitter:image:alt`. |
| **Favicon** | ✅ | `favicon.ico` (16/32/48) en la raíz — antes devolvía 404 —, `favicon.svg`, PNG 32. |
| **Íconos de app** | ✅ | `apple-touch-icon.png` 180 en la raíz, 192/512 `any` y 512 `maskable` (con margen de seguridad); manifest con `id`, `scope`, `short_name` «JA Borges» y accesos directos. |
| **Rastreo en vivo** | ✅ | 16 páginas, 69 recursos/enlaces internos únicos, 0 rotos. |
| **Cabeceras** | ✅ | HSTS, CSP, X-Frame-Options, nosniff, Referrer-Policy; Brotli; caché inmutable en imágenes. |
| **Rendimiento (medido, sin Lighthouse)** | ✅ | Carga inicial ≈ 64 KB (HTML+CSS+JS+hero). LCP precargado, imágenes con width/height y lazy. |
| **Producción vs staging** | ✅ | Ambos modos pasan los verificadores (producción 1294, staging 1288 comprobaciones). |

## Pendiente (no se puede cerrar sin datos o permisos)

1. **Dominio `joseantonioborges.com`**: no está en Cloudflare. Las URLs canónicas, `hreflang`, sitemap y OG ya lo usan; hasta que exista, las vistas previas al compartir no cargan la imagen.
2. **Fuentes de Google** (`fonts.googleapis.com`): único recurso externo; envía la IP del visitante a Google y retrasa la pintura. Solución: alojarlas en el propio sitio (requiere descargar Newsreader e Inter, licencia OFL).
3. **Lighthouse** no se ejecutó (la herramienta requiere descargar un paquete de terceros). Alternativa: correrlo el propietario en Chrome DevTools → Lighthouse sobre la URL de producción.
4. **Search Console / Bing Webmaster / analítica**: faltan los códigos de verificación y el ID de analítica (el aviso de cookies ya espera el evento `jab:consent`).
5. **Datos reales**: teléfono/WhatsApp, correo, LinkedIn/Instagram (activan `sameAs` en el JSON-LD), datos legales y revisión por un abogado.
6. **Publicar en producción**: `python3 tools/build.py` (sin `--staging`), quitar `DEMO=True` en `tools/build.py`, redirigir `www`, registrar el dominio y enviar el sitemap.
