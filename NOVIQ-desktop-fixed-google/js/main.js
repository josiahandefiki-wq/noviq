/* NOVIQ — main.js: small shared helpers */
(function () {
  'use strict';
  // Smooth-scroll to in-page anchors and move focus for keyboard users
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a || a.getAttribute('href') === '#') return;
    var t = document.getElementById(a.getAttribute('href').slice(1));
    if (t) { t.setAttribute('tabindex', '-1'); t.focus({ preventScroll: true }); }
  });
})();
