# Artículos de «Ideas / Insights»

Cada artículo son **dos archivos** (uno por idioma) con el mismo nombre base:

```
content/ideas/<slug>.es.md      ->  /es/ideas/<slug>/
content/ideas/<slug>.en.md      ->  /en/insights/<slug>/
```

Los archivos que empiezan por `_` o con `draft: true` **no se publican**.

## Encabezado (obligatorio)

```
---
title: Título del artículo
date: 2026-12-15            # AAAA-MM-DD
category: estrategia        # real-estate | emprendimiento | estrategia | tecnologia | liderazgo
excerpt: Resumen de una o dos frases (mínimo 70 caracteres; es la descripción para buscadores).
translation: clave-comun    # misma clave en las versiones ES y EN para enlazarlas (hreflang)
---
```

## Texto (Markdown sencillo)

`## Subtítulo`, `### Subtítulo menor`, párrafos, `**negrita**`, `*cursiva*`, listas con `- `, citas con `> ` y enlaces `[texto](https://…)`.

## Quién hace qué

- **José Antonio Borges (con su asistente de IA):** decide temas, investiga, redacta, revisa y aprueba los artículos en español e inglés.
- **Desarrollo:** mantiene las plantillas, el listado y la publicación de los artículos ya aprobados.

Tras añadir o editar archivos: `python3 tools/build.py` + `python3 tools/verificar-seo.py` y desplegar.
