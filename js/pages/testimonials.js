/* NOVIQ — testimonial slider (progressive enhancement: all slides show without JS) */
(function () {
  'use strict';
  var root = document.querySelector('[data-slider]'); if (!root) return;
  var slides = root.querySelectorAll('[data-slide]'), dotsWrap = root.querySelector('.dots'), i = 0;
  if (slides.length < 2) { root.querySelector('.t-controls').hidden = true; return; }
  var dots = [];
  slides.forEach(function (_, n) {
    var d = document.createElement('button'); d.type = 'button'; d.className = 'dot'; d.setAttribute('aria-label', 'Show testimonial ' + (n + 1));
    d.addEventListener('click', function () { show(n); }); dotsWrap.appendChild(d); dots.push(d);
  });
  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach(function (s, k) { s.hidden = k !== i; });
    dots.forEach(function (d, k) { d.classList.toggle('is-active', k === i); if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
  }
  root.querySelector('[data-prev]').addEventListener('click', function () { show(i - 1); });
  root.querySelector('[data-next]').addEventListener('click', function () { show(i + 1); });
  show(0);
})();
