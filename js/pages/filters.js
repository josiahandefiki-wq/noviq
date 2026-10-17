/* NOVIQ — filter chips for work and article grids */
(function () {
  'use strict';
  document.querySelectorAll('.filters[data-filter-target]').forEach(function (group) {
    var grid = document.querySelector(group.getAttribute('data-filter-target'));
    if (!grid) return;
    var empty = grid.parentNode.querySelector('.empty-state');
    group.addEventListener('click', function (e) {
      var b = e.target.closest('.chip'); if (!b) return;
      var f = b.getAttribute('data-filter'), shown = 0;
      group.querySelectorAll('.chip').forEach(function (c) { var on = c === b; c.classList.toggle('is-active', on); c.setAttribute('aria-pressed', String(on)); });
      grid.querySelectorAll('[data-cat]').forEach(function (card) {
        var show = f === 'all' || card.getAttribute('data-cat') === f;
        card.hidden = !show; if (show) { shown++; card.classList.add('is-visible'); }
      });
      if (empty) empty.hidden = shown > 0;
    });
  });
})();
