/* NOVIQ — animations.js: subtle scroll reveal (respects prefers-reduced-motion)
   Handles two cases:
   1. Elements with class "reveal" present when the page first loads.
   2. Elements with class "reveal" added later (e.g. content.js rebuilding a
      section from /data JSON) — these are picked up via MutationObserver
      instead of being missed, which previously left them stuck invisible. */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var supported = 'IntersectionObserver' in window;

  var io = null;
  if (!reduce && supported) {
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-visible');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -4% 0px' });
  }

  function reveal(el) {
    if (el.classList.contains('is-visible')) return;
    if (reduce || !supported) { el.classList.add('is-visible'); return; }
    io.observe(el);
    // Safety net: if this element is somehow never flagged as intersecting
    // (e.g. a fast scroll moves it out of view before the browser gets a
    // chance to check), make sure it still shows up rather than staying
    // invisible forever.
    setTimeout(function () { el.classList.add('is-visible'); }, 2500);
  }

  function scan(root) {
    var nodes = (root || document).querySelectorAll('.reveal');
    for (var i = 0; i < nodes.length; i++) reveal(nodes[i]);
  }

  scan();

  if ('MutationObserver' in window) {
    var mo = new MutationObserver(function (mutations) {
      for (var i = 0; i < mutations.length; i++) {
        var added = mutations[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var node = added[j];
          if (node.nodeType !== 1) continue;
          if (node.classList && node.classList.contains('reveal')) reveal(node);
          if (node.querySelectorAll) scan(node);
        }
      }
    });
    mo.observe(document.documentElement, { childList: true, subtree: true });
  }
})();
