#!/usr/bin/env python3
"""Servidor de prueba con recarga automática (solo desarrollo; NO forma parte del sitio publicado).
Uso: python3 tools/dev-server.py   ->  http://localhost:8766/es/
Sin caché, e inyecta un pequeño script que recarga la pestaña cuando cambia cualquier archivo de site/."""
import http.server, os, socketserver, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
PORT = 8766
SNIPPET = b"""<script>(function(){var last=null;function t(){fetch('/__mtime',{cache:'no-store'}).then(function(r){return r.text()}).then(function(v){if(last!==null&&v!==last){location.reload()}last=v}).catch(function(){})}setInterval(t,800);t()})()</script>"""

def newest():
    m = 0
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            try: m = max(m, os.stat(os.path.join(d, f)).st_mtime_ns)
            except OSError: pass
    return str(m)

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0"); super().end_headers()
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path.split("?")[0] == "/__mtime":
            b = newest().encode(); self.send_response(200); self.send_header("Content-Type", "text/plain"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
        path = self.translate_path(self.path.split("?")[0])
        if os.path.isdir(path): path = os.path.join(path, "index.html")
        if path.endswith(".html") and os.path.exists(path):
            data = open(path, "rb").read()
            data = data.replace(b"</body>", SNIPPET + b"</body>", 1) if b"</body>" in data else data + SNIPPET
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        super().do_GET()

socketserver.ThreadingTCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("", PORT), H) as s:
    s.serve_forever()
