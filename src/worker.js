// Cloudflare Worker: sirve el sitio estático (carpeta ./site) y recibe el formulario de contacto en /api/contact.
// - No guarda mensajes ni datos personales; los entrega por correo y los descarta.
// - Antispam: campo trampa (honeypot), tiempo mínimo de relleno, comprobación de origen, validación estricta y límite por IP
//   (opcional: Turnstile si se define TURNSTILE_SECRET, y un binding RATE_LIMITER).
// - El correo de destino es PRIVADO: vive solo en variables/secretos de Cloudflare (CONTACT_TO), nunca en el código ni en la web.
//
// Configuración necesaria para que el envío funcione (una sola vez):
//   npx wrangler secret put RESEND_API_KEY     # clave de la API de Resend (u otro proveedor; ver sendMail)
//   npx wrangler secret put CONTACT_TO         # correo privado que recibirá los mensajes
//   npx wrangler secret put CONTACT_FROM       # remitente verificado, p. ej. "Web José Antonio Borges <web@joseantonioborges.com>"
// Mientras falte algo de lo anterior, /api/contact responde 503 {code:"not_configured"} y la web lo explica.

const REASONS = { negocio: "Oportunidad empresarial", alianza: "Alianza", inversion: "Inversión", medios: "Medios o eventos", otro: "Otro" };
const RETURN_PATH = { es: "/es/contacto/", en: "/en/contact/" };
const hits = new Map(); // límite simple por IP (por instancia; refuerza al binding RATE_LIMITER si existe)

const json = (obj, status = 200) => new Response(JSON.stringify(obj), {
  status,
  headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "x-content-type-options": "nosniff" },
});
const clean = (v, max) => String(v ?? "").replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "").trim().slice(0, max);
const oneLine = (v, max) => clean(v, max).replace(/[\r\n]+/g, " ");

async function handleContact(request, env, url) {
  const wantsJson = (request.headers.get("accept") || "").includes("application/json");
  const lang = ((await peekLang(request)) === "en") ? "en" : "es";
  const back = (q) => new Response(null, { status: 303, headers: { location: RETURN_PATH[lang] + q, "cache-control": "no-store" } });
  const fail = (status, code, q) => (wantsJson ? json({ ok: false, code }, status) : back(q || "?error=err"));

  if (request.method !== "POST") return json({ ok: false, code: "method" }, 405);
  const origin = request.headers.get("origin");
  if (origin && new URL(origin).host !== url.host) return fail(403, "origin");

  const ip = request.headers.get("cf-connecting-ip") || "x";
  if (env.RATE_LIMITER) {
    const { success } = await env.RATE_LIMITER.limit({ key: ip });
    if (!success) return fail(429, "rate", "?error=err");
  } else {
    const now = Date.now(), arr = (hits.get(ip) || []).filter((t) => now - t < 10 * 60 * 1000);
    if (arr.length >= 5) return fail(429, "rate", "?error=err");
    arr.push(now); hits.set(ip, arr);
  }

  let fd;
  try { fd = await request.formData(); } catch { return fail(400, "invalid", "?error=req"); }

  if (clean(fd.get("website"), 200)) return wantsJson ? json({ ok: true }) : back("?enviado=1"); // trampa: se simula éxito
  const age = Date.now() - Number(fd.get("t"));
  if (!(age > 3000 && age < 2 * 24 * 3600 * 1000)) return fail(400, "invalid", "?error=req");

  const name = oneLine(fd.get("name"), 120), email = oneLine(fd.get("email"), 160), company = oneLine(fd.get("company"), 160);
  const reason = clean(fd.get("reason"), 20), message = clean(fd.get("message"), 4000), consent = clean(fd.get("consent"), 3);
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !REASONS[reason] || message.length < 10 || consent !== "1") return fail(400, "invalid", "?error=req");

  if (env.TURNSTILE_SECRET) {
    const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: clean(fd.get("cf-turnstile-response"), 2048), remoteip: ip }) });
    if (!(await r.json()).success) return fail(400, "captcha", "?error=req");
  }

  if (env.DELIVERY_MODE === "test") return wantsJson ? json({ ok: true, test: true }) : back("?enviado=1"); // solo para pruebas locales
  if (!(env.RESEND_API_KEY && env.CONTACT_TO && env.CONTACT_FROM)) return fail(503, "not_configured", "?error=nc");

  const text = `Nuevo mensaje desde la web\n\nNombre: ${name}\nCorreo: ${email}\nEmpresa / organización: ${company || "—"}\nMotivo: ${REASONS[reason]}\nIdioma: ${lang}\n\n${message}\n`;
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, "content-type": "application/json" },
    body: JSON.stringify({ from: env.CONTACT_FROM, to: [env.CONTACT_TO], reply_to: email, subject: `[Web] ${REASONS[reason]} — ${name}`, text }),
  });
  if (!res.ok) return fail(502, "delivery_failed", "?error=err");
  return wantsJson ? json({ ok: true }) : back("?enviado=1");
}

async function peekLang(request) {
  try { const fd = await request.clone().formData(); return clean(fd.get("lang"), 2); } catch { return "es"; }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/contact") return handleContact(request, env, url);
    if (url.pathname.startsWith("/api/")) return json({ ok: false, code: "not_found" }, 404);
    return env.ASSETS.fetch(request);
  },
};
