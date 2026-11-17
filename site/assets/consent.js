/* Aviso de cookies (LSSI-CE art. 22.2 + RGPD + guía AEPD):
   - Aparece abajo hasta que eliges. "Aceptar todas" y "Rechazar" tienen el mismo peso visual.
   - Las no necesarias (analítica) están DESACTIVADAS por defecto y solo se activan con consentimiento.
   - La elección se guarda 12 meses en localStorage ("jab-consent") y se puede cambiar cuando quieras.
   - Hoy el sitio no carga analítica ni cookies de terceros: cuando se añada, debe escucharse el evento
     "jab:consent" (detail.analytics === true) y NO cargar nada antes de que sea true. */
(function () {
  var KEY = 'jab-consent', MAXAGE = 365 * 24 * 3600 * 1000;
  var T = {
    es: { title: 'Cookies y privacidad', text: 'Usamos únicamente almacenamiento técnico necesario para que el sitio funcione y recordar tu elección. No activamos analítica ni cookies de terceros sin tu consentimiento.', more: 'Política de cookies', accept: 'Aceptar todas', reject: 'Rechazar', conf: 'Configurar',
      nec: 'Necesarias', necD: 'Permiten que el sitio funcione y recuerde tu elección. Siempre activas.', ana: 'Analíticas', anaD: 'Miden el uso del sitio para mejorarlo. Hoy no se usa ninguna herramienta.', save: 'Guardar preferencias', on: 'Siempre activas', path: '/es/cookies/', region: 'Aviso de cookies' },
    en: { title: 'Cookies and privacy', text: 'We only use technical storage necessary for the site to work and to remember your choice. We do not enable analytics or third-party cookies without your consent.', more: 'Cookie policy', accept: 'Accept all', reject: 'Reject', conf: 'Settings',
      nec: 'Necessary', necD: 'They let the site work and remember your choice. Always on.', ana: 'Analytics', anaD: 'They measure site usage to improve it. No tool is used today.', save: 'Save preferences', on: 'Always on', path: '/en/cookies/', region: 'Cookie notice' }
  };
  var lang = function () { return document.documentElement.lang === 'en' ? 'en' : 'es'; };
  var read = function () { try { var v = JSON.parse(localStorage.getItem(KEY)); if (v && v.v === 1 && Date.now() - v.ts < MAXAGE) return v; } catch (e) {} return null; };
  var write = function (a) {
    var v = { v: 1, analytics: !!a, ts: Date.now() };
    try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {}
    document.dispatchEvent(new CustomEvent('jab:consent', { detail: v }));
  };
  var box = null;
  function hide() { if (box) { box.remove(); box = null; } document.documentElement.classList.remove('consent-open'); document.documentElement.style.removeProperty('--cb-h'); }
  function show(openConf) {
    hide();
    var t = T[lang()], cur = read();
    box = document.createElement('div');
    box.className = 'cb'; box.setAttribute('role', 'region'); box.setAttribute('aria-label', t.region);
    box.innerHTML =
      '<div class="cb-in">' +
        '<div class="cb-t"><b>' + t.title + '</b><p>' + t.text + ' <a href="' + t.path + '">' + t.more + '</a>.</p></div>' +
        '<div class="cb-act"><button type="button" class="cb-b" data-a="accept">' + t.accept + '</button><button type="button" class="cb-b" data-a="reject">' + t.reject + '</button><button type="button" class="cb-l" data-a="conf" aria-expanded="false">' + t.conf + '</button></div>' +
      '</div>' +
      '<div class="cb-conf" hidden>' +
        '<div class="cb-row"><div><b>' + t.nec + '</b><p>' + t.necD + '</p></div><span class="cb-fix">' + t.on + '</span></div>' +
        '<div class="cb-row"><div><b>' + t.ana + '</b><p>' + t.anaD + '</p></div><label class="cb-sw"><input type="checkbox" id="cb-ana"' + (cur && cur.analytics ? ' checked' : '') + ' aria-label="' + t.ana + '"><i></i></label></div>' +
        '<button type="button" class="cb-b" data-a="save">' + t.save + '</button>' +
      '</div>';
    document.body.appendChild(box);
    var conf = box.querySelector('.cb-conf'), cbtn = box.querySelector('[data-a="conf"]');
    box.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('[data-a]'); if (!a) return;
      var k = a.getAttribute('data-a');
      if (k === 'accept') { write(true); hide(); }
      else if (k === 'reject') { write(false); hide(); }
      else if (k === 'save') { write(box.querySelector('#cb-ana').checked); hide(); }
      else if (k === 'conf') { var o = conf.hidden; conf.hidden = !o; cbtn.setAttribute('aria-expanded', o); size(); }
    });
    if (openConf) { conf.hidden = false; cbtn.setAttribute('aria-expanded', 'true'); }
    document.documentElement.classList.add('consent-open'); size();
  }
  function size() { if (box) document.documentElement.style.setProperty('--cb-h', box.offsetHeight + 'px'); }
  addEventListener('resize', size);
  document.addEventListener('click', function (e) { var o = e.target.closest && e.target.closest('[data-consent-open]'); if (o) { e.preventDefault(); show(true); } });
  window.JABConsent = { get: read, open: function () { show(true); } };
  function init() { var c = read(); if (c) document.dispatchEvent(new CustomEvent('jab:consent', { detail: c })); else show(false); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
