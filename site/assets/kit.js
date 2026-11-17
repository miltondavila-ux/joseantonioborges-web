/* Encabezado: botón QR «Pásalo a móvil» (escritorio), menú hamburguesa (móvil) con QR para compartir la página.
   Ya NO existe ninguna ventana de contacto por llamada, SMS o WhatsApp (decisión del propietario, v2): el contacto es el formulario. */
(function () {
  var T = {
    es: { close: 'Cerrar', qrTitle: '¡Pásalo a móvil!', qrP: 'Abre la cámara de tu celular y apunta al código. Se abre esta misma página.', qrBtn: 'Pásalo a móvil', menu: 'Menú', share: 'Compartir', shareP: 'Escanea para abrir esta página en otro dispositivo.' },
    en: { close: 'Close', qrTitle: 'Open it on your phone!', qrP: "Open your phone's camera and point it at the code. This same page will open.", qrBtn: 'Open on your phone', menu: 'Menu', share: 'Share', shareP: 'Scan to open this page on another device.' }
  };
  var t = function () { return T[document.documentElement.lang === 'en' ? 'en' : 'es']; };
  function qr(text, cell) {
    if (!window.qrcode) return '';
    var q = qrcode(0, 'M'); q.addData(text); q.make();
    return q.createSvgTag({ cellSize: cell || 4, margin: 0, scalable: true });
  }
  function pageUrl() { var c = document.querySelector('link[rel="canonical"]'); return (c && c.href) || (location.origin + location.pathname); }

  var box = document.createElement('div');
  box.className = 'cw'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true');
  document.body.appendChild(box);
  var last = null;
  function show() { last = document.activeElement; box.classList.add('on'); document.documentElement.classList.add('cw-open'); var x = box.querySelector('.cw-x'); if (x) x.focus(); }
  function close() { if (!box.classList.contains('on')) return; box.classList.remove('on'); document.documentElement.classList.remove('cw-open'); if (last && last.focus) last.focus(); }
  function pass() {
    var tx = t();
    box.innerHTML = '<div class="cw-box sm"><button class="cw-x" aria-label="' + tx.close + '">&times;</button><h3>' + tx.qrTitle + '</h3><div style="width:236px;margin:22px auto;padding:12px;border:1px solid rgba(255,255,255,.4);line-height:0">' + qr(pageUrl(), 6) + '</div><p class="intro-t" style="margin:0">' + tx.qrP + '</p></div>';
    show();
  }
  box.addEventListener('click', function (e) { if (e.target === box || (e.target.closest && e.target.closest('.cw-x'))) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  var hd = document.querySelector('header'), nav = hd && hd.querySelector('nav');
  if (nav) {
    var tx = t(), lang = document.getElementById('lang');
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'qr-btn'; b.title = tx.qrBtn; b.setAttribute('aria-label', tx.qrBtn); b.setAttribute('aria-haspopup', 'dialog');
    b.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="3.5" width="6.5" height="6.5" rx="1"/><rect x="14" y="3.5" width="6.5" height="6.5" rx="1"/><rect x="3.5" y="14" width="6.5" height="6.5" rx="1"/><path d="M14 14h2.5v2.5H14zM18 14h2.5M14 19v1.5M17.5 17.5h3v3"/></svg>';
    b.addEventListener('click', pass);
    nav.insertBefore(b, lang);

    var share = document.createElement('div');
    share.className = 'm-share';
    share.innerHTML = '<div class="code" role="img" aria-label="' + tx.share + '">' + qr(pageUrl(), 4) + '</div><p><b>' + tx.share + '</b>' + tx.shareP + '</p>';
    nav.appendChild(share);
    var soc = document.querySelector('footer .soc');
    if (soc) nav.appendChild(soc.cloneNode(true));

    var m = document.createElement('button');
    m.type = 'button'; m.className = 'burger'; m.setAttribute('aria-label', tx.menu); m.setAttribute('aria-expanded', 'false');
    m.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 8h16M4 16h16"/></svg>';
    m.addEventListener('click', function () { var o = hd.classList.toggle('menu'); m.setAttribute('aria-expanded', o); });
    nav.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('a')) { hd.classList.remove('menu'); m.setAttribute('aria-expanded', 'false'); } });
    hd.querySelector('.nav').appendChild(m);
  }
})();
