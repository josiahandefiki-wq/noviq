/* NOVIQ — forms.js: validation + delivery for the contact and newsletter forms.
   Delivery order: 1) data-endpoint (e.g. Formspree) via fetch, 2) mailto: fallback if an email is set,
   3) friendly "not connected yet" message. No data is sent anywhere until you configure data/site.json. */
(function () {
  'use strict';
  var forms = document.querySelectorAll('form[data-form]');

  function setStatus(form, msg, kind) {
    var s = form.parentNode.querySelector('.form-status') || form.querySelector('.form-status');
    if (!s) return;
    s.textContent = msg; s.className = 'form-status' + (kind ? ' is-' + kind : '');
  }
  function fieldError(input, msg) {
    var wrap = input.closest('.field'); if (!wrap) return;
    var err = wrap.querySelector('.field-error');
    if (msg) {
      input.setAttribute('aria-invalid', 'true');
      if (!err) { err = document.createElement('p'); err.className = 'field-error'; err.id = input.id + '-err'; wrap.appendChild(err); }
      err.textContent = msg; input.setAttribute('aria-describedby', err.id);
    } else {
      input.removeAttribute('aria-invalid'); input.removeAttribute('aria-describedby'); if (err) err.remove();
    }
  }
  function validate(form) {
    var first = null;
    form.querySelectorAll('[required]').forEach(function (el) {
      var v = el.value.trim(), msg = '';
      if (!v) msg = 'This field is required.';
      else if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) msg = 'Enter a valid email address, like name@example.com.';
      if (el.closest('.field')) fieldError(el, msg);
      else el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      if (msg && !first) first = el;
    });
    if (first) first.focus();
    return !first;
  }

  forms.forEach(function (form) {
    form.addEventListener('input', function (e) { if (e.target.getAttribute('aria-invalid') === 'true' && e.target.value.trim()) fieldError(e.target, ''); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var type = form.getAttribute('data-form');
      if (!validate(form)) { setStatus(form, 'Please check the highlighted fields.', 'error'); return; }
      var data = {}; new FormData(form).forEach(function (v, k) { data[k] = v; });
      var endpoint = form.getAttribute('data-endpoint'), mail = form.getAttribute('data-email');
      var okMsg = type === 'contact' ? 'Thanks. Your message has been sent and we will reply soon.' : 'Thanks for subscribing.';
      if (endpoint) {
        setStatus(form, 'Sending…', '');
        fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
          .then(function (r) { if (!r.ok) throw new Error(); form.reset(); setStatus(form, okMsg, 'ok'); })
          .catch(function () { setStatus(form, 'Something went wrong sending your message. Please try again or contact us directly.', 'error'); });
      } else if (type === 'contact' && mail) {
        var body = Object.keys(data).filter(function (k) { return data[k]; }).map(function (k) { return k + ': ' + data[k]; }).join('\n');
        window.location.href = 'mailto:' + mail + '?subject=' + encodeURIComponent('New project enquiry from ' + (data.name || 'website')) + '&body=' + encodeURIComponent(body);
        setStatus(form, 'Opening your email app with your message ready to send.', 'ok');
      } else {
        setStatus(form, type === 'contact'
          ? 'Thanks. This form is not connected to an inbox yet, so your message has not been sent. Please use WhatsApp, phone or email instead.'
          : 'Newsletter sign-up will be available soon.', type === 'contact' ? 'error' : '');
      }
    });
  });
})();
