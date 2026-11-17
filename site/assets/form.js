/* Formulario de contacto: envío por fetch a /api/contact (Cloudflare Worker). Sin cookies ni analítica.
   Sin JavaScript el formulario también funciona: el Worker responde con una redirección (?enviado=1 / ?error=...). */
(function () {
  var f = document.getElementById('cform'); if (!f) return;
  var msg = document.getElementById('fmsg'), ts = document.getElementById('cf-ts'), btn = f.querySelector('button[type=submit]');
  ts.value = String(Date.now());
  function say(k, cls) { msg.className = 'fmsg ' + (cls || ''); msg.textContent = f.getAttribute('data-' + k) || ''; }
  var q = new URLSearchParams(location.search);
  if (q.get('enviado') === '1') say('ok', 'ok');
  else if (q.get('error')) say(q.get('error') === 'nc' ? 'nc' : q.get('error') === 'req' ? 'req' : 'err', 'bad');
  var pre = q.get('motivo'); if (pre && f.elements.reason) f.elements.reason.value = pre;

  function invalid() {
    var bad = false;
    f.querySelectorAll('[required]').forEach(function (el) {
      var inv = el.type === 'checkbox' ? !el.checked : !String(el.value).trim();
      if (el.type === 'email' && !inv) inv = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value);
      el.setAttribute('aria-invalid', inv ? 'true' : 'false'); if (inv) bad = true;
    });
    return bad;
  }
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    if (invalid()) { say('req', 'bad'); return; }
    btn.disabled = true; say('sending', '');
    fetch(f.action, { method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(f) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { r: r, j: j }; }); })
      .then(function (x) {
        btn.disabled = false;
        if (x.r.ok && x.j.ok) { f.reset(); ts.value = String(Date.now()); say('ok', 'ok'); }
        else if (x.j && x.j.code === 'not_configured') say('nc', 'bad');
        else if (x.r.status === 400) say('req', 'bad');
        else say('err', 'bad');
      })
      .catch(function () { btn.disabled = false; say('err', 'bad'); });
  });
})();
