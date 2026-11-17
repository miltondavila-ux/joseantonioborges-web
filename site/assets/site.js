/* Efectos discretos: el contenido es visible sin JavaScript (la clase .js la añade este archivo). */
(function () {
  var d = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) d.classList.add('js');
  function init() {
  /* filtro simple por categoría en Ideas */
  var chips = document.querySelectorAll('.chip[data-cat]');
  if (chips.length) chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var k = c.getAttribute('data-cat');
      chips.forEach(function (x) { x.classList.toggle('on', x === c); });
      document.querySelectorAll('.artlist li').forEach(function (li) { li.hidden = !(k === 'all' || li.getAttribute('data-cat') === k); });
    });
  });

    var hd = document.getElementById('hd');
    function sc() { if (hd) hd.classList.toggle('solid', scrollY > 80); }
    addEventListener('scroll', sc, { passive: true }); sc();
    var els = document.querySelectorAll('.rv');
    if ('IntersectionObserver' in window && !reduce) {
      var io = new IntersectionObserver(function (a) { a.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('on'); io.unobserve(x.target); } }); }, { threshold: .1 });
      els.forEach(function (e) { io.observe(e); });
    } else { els.forEach(function (e) { e.classList.add('on'); }); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
