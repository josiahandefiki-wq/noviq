/* NOVIQ — contact page: prefill the form from the homepage quick-brief bar (?service=&goal=&budget=) */
(function () {
  'use strict';
  var q = new URLSearchParams(window.location.search);
  function fill(id, val) {
    var el = document.getElementById(id); if (!el || !val) return;
    if (el.tagName === 'SELECT') { Array.prototype.forEach.call(el.options, function (o) { if (o.text === val || o.value === val) el.value = o.value || o.text; }); }
    else el.value = val;
  }
  fill('f-service', q.get('service')); fill('f-budget', q.get('budget'));
  var goal = q.get('goal'), msg = document.getElementById('f-msg');
  if (goal) { document.getElementById('f-goal').value = goal; if (msg && !msg.value) msg.value = 'My main goal: ' + goal + '.\n'; }
})();
