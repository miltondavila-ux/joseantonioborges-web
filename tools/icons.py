#!/usr/bin/env python3
"""Genera el favicon y los íconos de app (monograma «JB») a partir de SVG, con las herramientas de macOS.
Salida (en site/):
  favicon.svg · favicon.ico (16/32/48) · apple-touch-icon.png (180)
  assets/icons/icon-32.png · icon-180.png · icon-192.png · icon-512.png · icon-maskable-512.png
Uso: python3 tools/icons.py"""
import os, shutil, struct, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
ICONS = os.path.join(SITE, "assets", "icons")
NAVY, PAPER = "#0E1626", "#F4F0E8"
FONT = "Georgia,'Times New Roman',serif"

FAVICON = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="{NAVY}"/><text x="32" y="44.5" text-anchor="middle" font-family="{FONT}" font-size="35" fill="{PAPER}">JB</text></svg>\n'

def app_svg(ring_r, font):
    # monograma dentro de un anillo, igual que en las imágenes OG
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" fill="{NAVY}"/>'
            f'<circle cx="256" cy="256" r="{ring_r}" fill="none" stroke="{PAPER}" stroke-width="7" opacity=".85"/>'
            f'<text x="256" y="{256 + font * 0.33:.0f}" text-anchor="middle" font-family="{FONT}" font-size="{font}" fill="{PAPER}">JB</text></svg>\n')

def sh(*a): subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render(svg_text, name, tmp, px=512):
    p = os.path.join(tmp, name + ".svg"); open(p, "w", encoding="utf-8").write(svg_text)
    sh("qlmanage", "-t", "-s", str(px), "-o", tmp, p)
    return os.path.join(tmp, name + ".svg.png")

def resized(src, px, dst):
    sh("sips", "-z", str(px), str(px), src, "--out", dst)

def make_ico(pngs, dst):
    """ICO con imágenes PNG incrustadas (válido en todos los navegadores modernos)."""
    imgs = [(s, open(p, "rb").read()) for s, p in pngs]
    head = struct.pack("<HHH", 0, 1, len(imgs)); off = 6 + 16 * len(imgs); ent = b""; data = b""
    for s, b in imgs:
        ent += struct.pack("<BBBBHHII", s % 256, s % 256, 0, 0, 1, 32, len(b), off + len(data)); data += b
    open(dst, "wb").write(head + ent + data)

if __name__ == "__main__":
    os.makedirs(ICONS, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(SITE, "favicon.svg"), "w", encoding="utf-8").write(FAVICON)
        fav = render(FAVICON, "fav", tmp)
        any512 = render(app_svg(205, 176), "any", tmp)
        mask512 = render(app_svg(150, 128), "mask", tmp)       # contenido dentro de la zona segura (80 %)
        for px in (512, 192, 180, 32):
            dst = os.path.join(ICONS, f"icon-{px}.png")
            shutil.copy(any512, dst) if px == 512 else resized(any512, px, dst)
        shutil.copy(mask512, os.path.join(ICONS, "icon-maskable-512.png"))
        shutil.copy(os.path.join(ICONS, "icon-180.png"), os.path.join(SITE, "apple-touch-icon.png"))
        pngs = []
        for px in (16, 32, 48):
            d = os.path.join(tmp, f"f{px}.png"); resized(fav, px, d); pngs.append((px, d))
        make_ico(pngs, os.path.join(SITE, "favicon.ico"))
    for f in ("favicon.svg", "favicon.ico", "apple-touch-icon.png"): print("OK", f, os.path.getsize(os.path.join(SITE, f)), "bytes")
    for f in sorted(os.listdir(ICONS)): print("OK assets/icons/" + f, os.path.getsize(os.path.join(ICONS, f)), "bytes")
