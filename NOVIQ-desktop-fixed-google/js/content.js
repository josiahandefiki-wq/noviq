/* NOVIQ content bridge.
   Admin edits JSON in /data and this script applies those edits to the live pages.
   Static HTML remains as a safe fallback if JSON is unavailable. */
(function () {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }
  function getJSON(path) {
    return fetch(path, {cache:'no-store'}).then(function (r) {
      if (!r.ok) throw new Error('fetch failed: ' + path);
      return r.json();
    });
  }
  function currentServiceSlug() {
    var m = location.pathname.match(/\/pages\/(service-[^/]+)\.html$/);
    return m ? m[1] : null;
  }

  /* Images */
  getJSON('/data/images.json').then(function (map) {
    document.querySelectorAll('[data-img]').forEach(function (el) {
      var v = map[el.getAttribute('data-img')];
      if (!v || !v.src) return;
      el.setAttribute('src', v.src);
      if (v.alt) el.setAttribute('alt', v.alt);
    });
  }).catch(function () {});

  /* Contact/social settings */
  getJSON('/data/site.json').then(function (site) {
    function telHref(v) { return 'tel:' + v.replace(/[^+0-9]/g, ''); }
    function mailHref(v) { return 'mailto:' + v; }
    function waHref(v) { return 'https://wa.me/' + v.replace(/\D/g, ''); }
    function apply(key, builder) {
      var val = (site[key] || '').trim();
      if (!val) return;
      document.querySelectorAll('[data-site="' + key + '"]').forEach(function (wrap) {
        var text = esc(val);
        wrap.innerHTML = builder ? '<a href="' + builder(val) + '"' + (builder === waHref ? ' target="_blank" rel="noopener"' : '') + '>' + text + '</a>' : text;
      });
    }
    apply('whatsapp', waHref); apply('phone', telHref); apply('email', mailHref); apply('location', null);
    if (site.social) Object.keys(site.social).forEach(function (key) {
      var url = (site.social[key] || '').trim(); if (!url) return;
      document.querySelectorAll('[data-social="' + key + '"]').forEach(function (a) {
        a.href=url; a.target='_blank'; a.rel='noopener'; a.classList.remove('is-placeholder');
        a.setAttribute('aria-label', key === 'x' ? 'X (Twitter)' : key.charAt(0).toUpperCase()+key.slice(1));
      });
    });
  }).catch(function () {});

  /* Services: the Admin service editor is the source of truth for service cards and detail pages. */
  getJSON('/data/services.json').then(function (raw) {
    var services = Array.isArray(raw) ? raw : (raw && Array.isArray(raw.services) ? raw.services : []);
    if (!services.length) return;

    var serviceSlug = currentServiceSlug();
    if (!serviceSlug) {
      var grid = document.querySelector('.svc-grid');
      if (grid) {
        var cta = grid.querySelector('.svc-cta');
        grid.innerHTML = services.map(function (s, i) {
          var href = '/pages/' + esc(s.slug) + '.html';
          var image = esc(s.image || '');
          var alt = esc(s.title || 'NOVIQ service');
          var feats = Array.isArray(s.features) ? s.features.slice(0,4) : [];
          return '<article class="svc-card reveal" style="--d:' + (Math.min(i,8)*0.05).toFixed(2) + 's">' +
            '<a class="svc-card-photo" href="' + href + '"><div class="svc-media"><img src="' + image + '" alt="' + alt + '" loading="lazy" decoding="async"></div></a>' +
            '<h3>' + esc(s.title) + '</h3><p>' + esc(s.short) + '</p>' +
            (feats.length ? '<ul class="check-list">' + feats.map(function(f){return '<li><svg aria-hidden="true" class="ic"><use href="#i-check"></use></svg>' + esc(f) + '</li>';}).join('') + '</ul>' : '') +
            '<a class="link-arrow" href="' + href + '">Learn more<svg aria-hidden="true" class="ic"><use href="#i-arrow"></use></svg></a></article>';
        }).join('');
        if (cta) grid.appendChild(cta);
      }
      return;
    }

    var s = services.find(function (item) { return item.slug === serviceSlug; });
    if (!s) return;
    var title = document.getElementById('hero-title');
    var kicker = document.querySelector('.hero-kicker');
    var lead = document.querySelector('.hero-lead');
    if (kicker) kicker.textContent = s.title || kicker.textContent;
    if (title) title.textContent = s.hero_title || s.title || title.textContent;
    if (lead) lead.textContent = s.lead || lead.textContent;
    if (s.meta) document.querySelector('meta[name="description"]')?.setAttribute('content', s.meta);
    document.title = (s.title || document.title) + ' | NOVIQ';

    var img = document.querySelector('.hero-visual img[data-img]');
    if (img && s.image) { img.src=s.image; img.alt=s.title || img.alt; }
    document.querySelectorAll('main img[data-img]').forEach(function (el) { if (s.image) {el.src=s.image; el.alt=s.title || el.alt;} });

    var incList = document.querySelector('.why-list-1');
    if (incList && Array.isArray(s.includes)) {
      incList.innerHTML = s.includes.map(function (x, i) {
        var icon = x[0] || x.icon || 'check', h = x[1] || x.title || '', p = x[2] || x.description || '';
        return '<li class="reveal" style="--d:' + (i*0.07).toFixed(2) + 's"><span class="f-ic"><svg class="ic" aria-hidden="true"><use href="#i-' + esc(icon) + '"></use></svg></span><div><h3>' + esc(h) + '</h3><p>' + esc(p) + '</p></div></li>';
      }).join('');
    }
    var forLead = document.querySelector('.lead-sm');
    if (forLead && s.for) forLead.textContent = s.for;
    var forList = forLead && forLead.parentElement ? forLead.parentElement.querySelector('.check-list') : null;
    if (forList && Array.isArray(s.features)) forList.innerHTML = s.features.map(function(f){return '<li><svg class="ic" aria-hidden="true"><use href="#i-check"></use></svg>'+esc(f)+'</li>';}).join('');
    var steps = document.querySelector('.mini-grid-2');
    if (steps && Array.isArray(s.steps)) steps.innerHTML = s.steps.map(function(x,i){return '<li class="mini-card reveal" style="--d:'+(i*0.07).toFixed(2)+'s"><span class="step-no step-no-light">'+String(i+1).padStart(2,'0')+'</span><h3>'+esc(x[0]||x.title||'')+'</h3><p>'+esc(x[1]||x.description||'')+'</p></li>';}).join('');
  }).catch(function () {});

  /* Testimonials */
  function initTestiSlider(root) {
    if (!root) return;
    var slides=root.querySelectorAll('[data-slide]'), dotsWrap=root.querySelector('.dots'), controls=root.querySelector('.t-controls');
    if (!dotsWrap) return; dotsWrap.innerHTML=''; var i=0;
    if (slides.length<2){slides.forEach(function(s){s.hidden=false;}); if(controls)controls.hidden=true; return;}
    if(controls)controls.hidden=false; var dots=[];
    function show(n){i=(n+slides.length)%slides.length;slides.forEach(function(s,k){s.hidden=k!==i;});dots.forEach(function(d,k){d.classList.toggle('is-active',k===i);if(k===i)d.setAttribute('aria-current','true');else d.removeAttribute('aria-current');});}
    slides.forEach(function(_,n){var d=document.createElement('button');d.type='button';d.className='dot';d.setAttribute('aria-label','Show testimonial '+(n+1));d.onclick=function(){show(n);};dotsWrap.appendChild(d);dots.push(d);});
    var p=root.querySelector('[data-prev]'), q=root.querySelector('[data-next]'); if(p)p.onclick=function(){show(i-1)}; if(q)q.onclick=function(){show(i+1)}; show(0);
  }
  var sliderRoot=document.querySelector('[data-slider]');
  if(sliderRoot) getJSON('/data/testimonials.json').then(function(data){
    var list=data&&data.testimonials;if(!Array.isArray(list)||!list.length)return;var track=sliderRoot.querySelector('.t-slides');if(!track)return;
    var stars=new Array(5).fill('<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-star"></use></svg>').join('');
    track.innerHTML=list.map(function(t){return '<figure class="t-slide" data-slide><div class="t-head"><span class="avatar" aria-hidden="true">'+esc(t.initials||'')+'</span><div><strong>'+esc(t.name||'')+'</strong><span>'+esc(t.role||'')+'</span></div></div><div class="stars" role="img" aria-label="5 out of 5 stars">'+stars+'</div><blockquote>“'+esc(t.quote||'')+'”</blockquote></figure>';}).join('');
    initTestiSlider(sliderRoot);
  }).catch(function(){});
})();
