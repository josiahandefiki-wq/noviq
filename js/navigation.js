/* NOVIQ — navigation: accessible mobile menu + Services dropdown */
(function () {
  'use strict';
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (!toggle || !nav) return;
  var mq = window.matchMedia('(max-width: 1000px)');
  var service = nav.querySelector('.nav-dropdown');
  var serviceToggle = service && service.querySelector('.nav-dropdown-toggle');

  function setOpen(open) {
    document.body.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (!open && service) setServiceOpen(false);
  }
  function setServiceOpen(open) {
    if (!service || !serviceToggle) return;
    service.classList.toggle('is-open', open);
    serviceToggle.setAttribute('aria-expanded', String(open));
    serviceToggle.setAttribute('aria-label', open ? 'Close Services menu' : 'Open Services menu');
  }
  toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
  if (serviceToggle) {
    serviceToggle.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      setServiceOpen(serviceToggle.getAttribute('aria-expanded') !== 'true');
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (service && service.classList.contains('is-open')) setServiceOpen(false);
      else if (document.body.classList.contains('nav-open')) { setOpen(false); toggle.focus(); }
    }
  });
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) setOpen(false);
  });
  document.addEventListener('click', function (e) {
    if (service && service.classList.contains('is-open') && !e.target.closest('.nav-dropdown')) setServiceOpen(false);
    if (document.body.classList.contains('nav-open') && !e.target.closest('.site-header')) setOpen(false);
  });
  (mq.addEventListener ? mq.addEventListener.bind(mq, 'change') : mq.addListener.bind(mq))(function () {
    if (!mq.matches) setOpen(false);
  });
})();
