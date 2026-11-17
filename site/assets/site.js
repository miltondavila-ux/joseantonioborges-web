/* Efectos discretos: el contenido es visible sin JavaScript (la clase .js la añade este archivo). */
(function () {
  var d = document.documentElement;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) d.classList.add('js');
  function init() {
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
