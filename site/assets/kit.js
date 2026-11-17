/* Kit de contacto (esquema de la Super Guía): QR en escritorio, botones en móvil.
   Sin formularios ni servidor. Canales: Llamar, SMS, WhatsApp, Email, Agendar.
   Los NÚMEROS NO SE MUESTRAN en pantalla: solo viajan dentro de los enlaces y los QR.
   Edita SOLO CONFIG (datos actuales = EJEMPLO). */
(function () {
  var CONFIG = {
    phone: '34000000000',                          /* EJEMPLO: número real pendiente (solo dígitos con país) */
    email: 'correo@joseantonioborges.com',         /* EJEMPLO */
    site: 'https://joseantonioborges.com'
  };
  var T = {
    es: { title: 'Conectemos', ready: 'Tu mensaje está preparado', intro: 'Escanea con la cámara de tu celular.', introReady: 'Elige cómo quieres enviarlo.', introM: 'Elige cómo quieres conectar.',
      names: { call: 'LLAMAR', sms: 'SMS', wa: 'WHATSAPP', mail: 'EMAIL', agenda: 'AGENDAR' },
      sub: { call: 'Llamada directa', sms: 'Mensaje de texto', wa: 'Chat de WhatsApp', mail: 'Correo electrónico', agenda: 'Reservar conversación' },
      msg: 'Hola José Antonio, me gustaría conectar contigo.', subject: 'Contacto desde joseantonioborges.com', close: 'Cerrar',
      qrTitle: '¡Pásalo a móvil!', qrP: 'Abre la cámara de tu celular y apunta al código. Se abre esta misma página.', qrBtn: 'Pásalo a móvil', menu: 'Menú',
      share: 'Compartir', shareP: 'Escanea para abrir esta página en otro dispositivo.', agendaPath: '/es/contacto/#agendar' },
    en: { title: "Let's connect", ready: 'Your message is ready', intro: "Scan with your phone's camera.", introReady: 'Choose how you want to send it.', introM: 'Choose how to get in touch.',
      names: { call: 'CALL', sms: 'SMS', wa: 'WHATSAPP', mail: 'EMAIL', agenda: 'SCHEDULE' },
      sub: { call: 'Direct call', sms: 'Text message', wa: 'WhatsApp chat', mail: 'Email', agenda: 'Book a conversation' },
      msg: "Hello José Antonio, I'd like to connect with you.", subject: 'Contact from joseantonioborges.com', close: 'Close',
      qrTitle: 'Open it on your phone!', qrP: "Open your phone's camera and point it at the code. This same page will open.", qrBtn: 'Open on your phone', menu: 'Menu',
      share: 'Share', shareP: 'Scan to open this page on another device.', agendaPath: '/en/contact/#agendar' }
  };
  var C = CONFIG;
  var t = function () { return T[document.documentElement.lang === 'en' ? 'en' : 'es']; };
  var icons = {
    call: '<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>',
    sms: '<svg viewBox="0 0 24 24"><path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-5 4v-4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/></svg>',
    wa: '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm5 14c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 .9-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .6l-.4.6-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l1.9.9c.3.1.5.2.5.3.1.2.1.8-.1 1.4z"/></svg>',
    mail: '<svg viewBox="0 0 24 24"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm9 7L4.5 7v1.6L12 13.6l7.5-5V7z"/></svg>',
    agenda: '<svg viewBox="0 0 24 24"><path d="M7 2h2v2h6V2h2v2h3a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h3V2zm-2 8v9h14v-9H5z"/></svg>'
  };
  var enc = encodeURIComponent;
  var links = function (m) { return {
    call: 'tel:+' + C.phone,
    sms: 'sms:+' + C.phone + '?&body=' + enc(m),
    wa: 'https://wa.me/' + C.phone + '?text=' + enc(m),
    mail: 'mailto:' + C.email + '?subject=' + enc(t().subject) + '&body=' + enc(m)
  }; };
  var agendaUrl = function () { return C.site + t().agendaPath; };
  var isMobile = function () { return innerWidth <= 600 || /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent); };
  var esc = function (s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\n/g, '<br>'); };
  function qr(text, cell) {
    if (!window.qrcode) return '';
    var q = qrcode(0, 'M'); q.addData(text); q.make();
    return q.createSvgTag({ cellSize: cell || 4, margin: 0, scalable: true });
  }
  function pageUrl() {
    var c = document.querySelector('link[rel="canonical"]');
    return (c && c.href) || (location.origin + location.pathname);
  }

  var box = document.createElement('div');
  box.className = 'cw'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true');
  document.body.appendChild(box);
  var last = null;

  function card(k, link) { return '<div class="cw-q"><div class="code">' + qr(link) + '</div><b>' + icons[k] + t().names[k] + '</b><small>' + t().sub[k] + '</small></div>'; }

  function render(msg) {
    var tx = t(), L = links(msg || tx.msg), keys = ['call', 'sms', 'wa', 'mail'], h;
    var head = msg ? '<h3>' + tx.ready + '</h3><div class="cw-msg">' + esc(msg) + '</div><p class="intro-t">' + tx.introReady + '</p>'
                   : '<h3>' + tx.title + '</h3><p class="intro-t">' + (isMobile() ? tx.introM : tx.intro) + '</p>';
    if (isMobile()) {
      h = head + '<div class="cw-list">' + keys.map(function (k) {
        return '<a class="cw-opt" href="' + L[k] + '"' + (k === 'wa' ? ' target="_blank" rel="noopener"' : '') + '>' + icons[k] + '<span>' + tx.names[k] + '<small>' + tx.sub[k] + '</small></span></a>';
      }).join('') + '<a class="cw-opt" href="' + agendaUrl() + '" data-agenda>' + icons.agenda + '<span>' + tx.names.agenda + '<small>' + tx.sub.agenda + '</small></span></a></div>';
    } else {
      h = head + '<div class="cw-qr">' + keys.map(function (k) { return card(k, L[k]); }).join('') + card('agenda', agendaUrl()) + '</div>';
    }
    var demo = document.documentElement.hasAttribute('data-demo') ? '<p class="cw-demo">' + (document.documentElement.lang === 'en' ? 'Sample data, pending confirmation.' : 'Datos de ejemplo, pendientes de confirmar.') + '</p>' : '';
    box.innerHTML = '<div class="cw-box"><button class="cw-x" aria-label="' + tx.close + '">&times;</button>' + h + demo + '</div>';
  }
  function show() { last = document.activeElement; box.classList.add('on'); document.documentElement.classList.add('cw-open'); var x = box.querySelector('.cw-x'); if (x) x.focus(); }
  function close() { if (!box.classList.contains('on')) return; box.classList.remove('on'); document.documentElement.classList.remove('cw-open'); if (last && last.focus) last.focus(); }
  function open(msg) { render(msg || null); show(); }

  function pass() {
    var tx = t();
    box.innerHTML = '<div class="cw-box sm"><button class="cw-x" aria-label="' + tx.close + '">&times;</button><h3>' + tx.qrTitle + '</h3><div style="width:236px;margin:22px auto;padding:12px;border:1px solid rgba(255,255,255,.4);line-height:0">' + qr(pageUrl(), 6) + '</div><p class="intro-t" style="margin:0">' + tx.qrP + '</p></div>';
    show();
  }

  box.addEventListener('click', function (e) {
    if (e.target === box || (e.target.closest && e.target.closest('.cw-x'))) return close();
    var g = e.target.closest && e.target.closest('[data-agenda]'), dest = document.getElementById('agendar');
    if (g && dest) { e.preventDefault(); close(); dest.scrollIntoView({ block: 'center' }); }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-contact]');
    if (!a) return;
    e.preventDefault(); open(a.getAttribute('data-message'));
  });
  addEventListener('resize', function () { if (box.classList.contains('on') && box.querySelector('.cw-qr,.cw-list')) render(null); });

  /* Encabezado: botón QR (escritorio) y menú hamburguesa con QR para compartir (móvil) */
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
  window.ContactKit = { open: open, close: close };
})();
