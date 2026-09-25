#!/usr/bin/env python3
"""NOVIQ static site builder.

Reads data/*.json and writes every HTML page, sitemap.xml and robots.txt.
Usage (from the NOVIQ folder):  python3 tools/build.py
The output is plain HTML/CSS/JS: hosting needs no build step.
"""
import json, os, sys, html, re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n): return json.load(open(os.path.join(ROOT, 'data', n + '.json'), encoding='utf-8'))
SITE, SERVICES, PROJECTS, TESTIS, ARTICLES = (load(x) for x in ('site', 'services', 'projects', 'testimonials', 'articles'))
TESTIS = TESTIS['testimonials'] if isinstance(TESTIS, dict) else TESTIS
E = html.escape
URL = SITE['url'].rstrip('/')
OG = 'assets/images/general/og-image.jpg'

# ---------------------------------------------------------------- icons
IC = {
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>', 'arrow-ur': '<path d="M7 17L17 7M8 7h9v9"/>',
 'chev-l': '<path d="M15 6l-6 6 6 6"/>', 'chev-r': '<path d="M9 6l6 6-6 6"/>', 'chev-d': '<path d="M6 9l6 6 6-6"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'shield': '<path d="M12 3l7.5 3v5.5c0 4.7-3.2 8-7.5 9.5-4.300-1.500-7.500-4.800-7.500-9.500V6z"/><path d="M8.5 12l2.5 2.500 4.500-5"/>',
 'users': '<circle cx="9" cy="8" r="3.200"/><path d="M3 20c0-3.300 2.700-6 6-6s6 2.700 6 6"/><circle cx="17" cy="9" r="2.500"/><path d="M17 14c2.400.2 4 2 4 4.500"/>',
 'lock': '<rect x="5" y="11" width="14" height="9" rx="2.500"/><path d="M8 11V8a4 4 0 018 0v3"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.500 2.600 3.800 5.600 3.800 9S14.500 18.400 12 21c-2.500-2.600-3.800-5.600-3.800-9S9.500 5.600 12 3z"/>',
 'code': '<path d="M8 8l-4.500 4L8 16M16 8l4.500 4L16 16M13.500 5l-3 14"/>',
 'trending': '<path d="M3 17l6-6 4 4 7-8M15 7h5v5"/>',
 'calendar': '<rect x="3.500" y="5" width="17" height="15.500" rx="3"/><path d="M3.500 10h17M8 3v4M16 3v4"/>',
 'megaphone': '<path d="M4 10v4a1 1 0 001 1h2l7 4V5L7 9H5a1 1 0 00-1 1z"/><path d="M18 9.500a4 4 0 010 5M7 15l1.500 5h2.500L10 16.500"/>',
 'camera': '<path d="M4 8h3l1.500-2.500h7L17 8h3a1 1 0 011 1v9a1 1 0 01-1 1H4a1 1 0 01-1-1V9a1 1 0 011-1z"/><circle cx="12" cy="13" r="3.500"/>',
 'layers': '<path d="M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5"/>',
 'star': '<path d="M12 3.500l2.600 5.300 5.800.8-4.200 4.100 1 5.800L12 16.800l-5.200 2.700 1-5.800-4.200-4.100 5.800-.8z" fill="currentColor" stroke="none"/>',
 'phone': '<path d="M5 4h4l2 5-2.500 1.500a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7l8 6 8-6"/>',
 'pin': '<path d="M12 21s7-6.200 7-11.500A7 7 0 005 9.500C5 14.800 12 21 12 21z"/><circle cx="12" cy="9.500" r="2.500"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
 'search': '<circle cx="11" cy="11" r="6.500"/><path d="M16 16l4.500 4.500"/>',
 'chat': '<path d="M4 20l1.300-4.200A8 8 0 1112 20a8 8 0 01-3.800-1z"/>',
 'spark': '<path d="M12 3c.6 4.500 2.500 6.400 7 7-4.500.6-6.400 2.500-7 7-.6-4.500-2.500-6.400-7-7 4.500-.6 6.400-2.500 7-7z"/>',
 'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.200"/>',
 'heart': '<path d="M12 20s-7.500-4.400-7.500-10A4.300 4.300 0 0112 7.500 4.300 4.300 0 0119.500 10c0 5.600-7.500 10-7.500 10z"/>',
 'play': '<path d="M8 5.500v13l11-6.500z"/>', 'layout': '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M9 9v11"/>',
 'pen': '<path d="M4 20l4-1 11-11-3-3L5 16l-1 4zM14 6l3 3"/>', 'send': '<path d="M21 3L10 14M21 3l-7 18-4-7-7-4z"/>',
 'palette': '<circle cx="12" cy="12" r="9"/><circle cx="8.500" cy="10" r="1"/><circle cx="12" cy="7.500" r="1"/><circle cx="15.500" cy="10" r="1"/><path d="M12 21c-2 0-2-2 0-3s1-3 3-3h3"/>',
 'zap': '<path d="M13 3L5 13.500h6L10 21l8-10.500h-6z"/>', 'briefcase': '<rect x="3" y="7" width="18" height="13" rx="3"/><path d="M9 7V5.500A1.500 1.500 0 0110.500 4h3A1.500 1.500 0 0115 5.500V7M3 13h18"/>',
 'instagram': '<rect x="3.500" y="3.500" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r=".8" fill="currentColor"/>',
 'facebook': '<path d="M14 8.500h2.500V4.500H14A3.500 3.500 0 0010.500 8v2.500H8V14h2.500v6.500H14V14h2.300l.5-3.500H14V8.500z"/>',
 'linkedin': '<rect x="4" y="9" width="3.500" height="11"/><circle cx="5.700" cy="5.500" r="1.800"/><path d="M11 9h3.300v1.600C15 9.500 16.300 8.800 18 8.800c3 0 3.500 2 3.500 4.600V20H18v-5.800c0-1.400-.2-2.400-1.700-2.400S14.500 13 14.500 14.400V20H11z"/>',
 'xsoc': '<path d="M4 4l16 16M20 4L4 20"/>', 'whatsapp': '<path d="M4 20l1.300-4.200A8 8 0 1112 20a8 8 0 01-3.800-1z"/><path d="M9 9.500c.3 2.500 2.500 4.700 5 5l1-1.200-1.800-1-.9.700c-.8-.4-1.500-1.100-1.900-1.900l.7-.9-1-1.800z"/>',
}
CLIPS = ('<clipPath id="clip-hero" clipPathUnits="objectBoundingBox"><path d="M0.30,0 L1,0 L1,1 L0.10,1 C0.26,0.72 0.02,0.36 0.30,0Z"/></clipPath>'
         '<clipPath id="clip-hero-m" clipPathUnits="objectBoundingBox"><path d="M0,0.10 C0.30,-0.02 0.66,0.20 1,0.04 L1,1 L0,1Z"/></clipPath>'
         '<clipPath id="clip-blob" clipPathUnits="objectBoundingBox"><path d="M0.26,0 H0.95 Q1,0 1,0.06 V0.94 Q1,1 0.95,1 H0.34 C0.12,1 0.02,0.78 0.03,0.52 C0.04,0.28 0,0.06 0.26,0Z"/></clipPath>')
SPRITE = ('<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
          + ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in IC.items())
          + CLIPS + '</defs></svg>')

def icon(n, cls=''): return f'<svg class="ic {cls}" aria-hidden="true" focusable="false"><use href="#i-{n}"/></svg>'

# ---------------------------------------------------------------- helpers
class Ctx:
    def __init__(s, path):
        s.path = path; s.depth = path.count('/'); s.p = '../' * s.depth
    def u(s, target): return s.p + target
    def canon(s): return URL + '/' + ('' if s.path == 'index.html' else s.path)

def fmt_date(d): return datetime.strptime(d, '%Y-%m-%d').strftime('%b %d, %Y').replace(' 0', ' ')
def sp(slug): return f'pages/{slug}.html'
def img(c, src, alt, w, h, lazy=True, cls='', extra=''):
    return f'<img class="{cls}" src="{c.u(src)}" alt="{E(alt)}" width="{w}" height="{h}" {"loading=\"lazy\" decoding=\"async\"" if lazy else "fetchpriority=\"high\" decoding=\"async\""} {extra}>'
def rv(i=0): return f'reveal" style="--d:{i*0.07:.2f}s'   # use inside class="..."

def btn(c, target, label, cls='btn-gold', ic=None):
    return f'<a class="btn {cls}" href="{c.u(target)}">{E(label)}{icon(ic) if ic else ""}</a>'

def contact_bits():
    ph, em, wa, loc = SITE['phone'].strip(), SITE['email'].strip(), re.sub(r'\D', '', SITE['whatsapp']), SITE['location'].strip()
    return dict(
        phone=(f'<a href="tel:{E(re.sub(r"[^+0-9]", "", ph))}">{E(ph)}</a>' if ph else '<span class="ph">Phone number to be added</span>'),
        email=(f'<a href="mailto:{E(em)}">{E(em)}</a>' if em else '<span class="ph">Email address to be added</span>'),
        wa=(f'<a href="https://wa.me/{wa}" rel="noopener">Chat on WhatsApp</a>' if wa else '<span class="ph">WhatsApp number to be added</span>'),
        loc=(E(loc) if loc else '<span class="ph">Location to be added</span>'))

def socials(c, cls='socials'):
    out = []
    for key, ic, label in [('instagram', 'instagram', 'Instagram'), ('facebook', 'facebook', 'Facebook'), ('linkedin', 'linkedin', 'LinkedIn'), ('x', 'xsoc', 'X')]:
        v = SITE['social'].get(key, '').strip()
        if v: out.append(f'<li><a class="soc" href="{E(v)}" rel="noopener" aria-label="NOVIQ on {label}">{icon(ic)}</a></li>')
        else: out.append(f'<li><a class="soc is-placeholder" href="{c.u("pages/contact.html")}#social" aria-label="{label} link coming soon">{icon(ic)}</a></li>')
    return f'<ul class="{cls}">{"".join(out)}</ul>'

NAV = [('Home', 'index.html', 'home'), ('Services', 'pages/services.html', 'services'), ('Our Work', 'pages/work.html', 'work'),
       ('About', 'pages/about.html', 'about'), ('Insights', 'pages/insights.html', 'insights'), ('Contact', 'pages/contact.html', 'contact')]

def header(c, active):
    links = ''.join(f'<li><a class="nav-link" href="{c.u(t)}"{" aria-current=\"page\"" if k == active else ""}>{n}</a></li>' for n, t, k in NAV)
    wa = re.sub(r'\D', '', SITE['whatsapp'])
    wa_href = f'https://wa.me/{wa}' if wa else c.u('pages/contact.html') + '#whatsapp'
    em = SITE['email'].strip()
    mail_href = f'mailto:{em}' if em else c.u('pages/contact.html') + '#email'
    return f'''<header class="site-header">
  <a class="brand" href="{c.u('index.html')}"><img class="brand-logo" src="{c.u('assets/images/logo/logo-light.png')}" alt="NOVIQ, Ideas to Impact: home" width="476" height="258" fetchpriority="high" decoding="async"></a>
  <nav class="nav" id="primary-nav" aria-label="Primary"><ul>{links}</ul><a class="btn btn-gold nav-cta" href="{c.u('pages/contact.html')}#project-form">Start a Project</a></nav>
  <div class="header-actions"><a class="icon-btn" href="{wa_href}" aria-label="Message NOVIQ on WhatsApp">{icon('whatsapp')}</a><a class="icon-btn" href="{mail_href}" aria-label="Email NOVIQ">{icon('mail')}</a><a class="btn btn-gold btn-sm header-cta" href="{c.u('pages/contact.html')}#project-form">Start a Project</a></div>
  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu">{icon('menu', 'i-open')}{icon('x', 'i-close')}</button>
</header>'''

SWOOSH = ('<svg class="hero-swoosh" viewBox="0 0 1 1" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="swg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fe8bd"/><stop offset="1" stop-color="#1d8a63"/></linearGradient></defs>'
          '<path class="sw-d" d="M0.10,1 C0.26,0.72 0.02,0.36 0.30,0" fill="none" stroke="url(#swg)" stroke-width="14" vector-effect="non-scaling-stroke" stroke-linecap="round" opacity=".9"/>'
          '<path class="sw-m" d="M0,0.10 C0.30,-0.02 0.66,0.20 1,0.04" fill="none" stroke="url(#swg)" stroke-width="12" vector-effect="non-scaling-stroke" stroke-linecap="round" opacity=".9"/></svg>')

def hero_home(c):
    svc_opts = ''.join(f'<option>{E(s["title"])}</option>' for s in SERVICES)
    return f'''<div class="shell hero-shell hero-home">{header(c, 'home')}
<section class="hero" id="main-content" tabindex="-1" aria-labelledby="hero-title">
  <div class="hero-copy">
    <p class="hero-kicker">Ideas to Impact.</p>
    <h1 id="hero-title"><span>We Turn</span> <span class="gold">Ideas Into</span> <span>Impact.</span></h1>
    <p class="hero-lead">NOVIQ helps small businesses grow through powerful websites, social media, advertising and creative content.</p>
    <form class="quick-brief" action="{c.u('pages/contact.html')}" method="get" aria-label="Start a project">
      <div class="qb-field">{icon('briefcase')}<div><label for="qb-service">Service</label><select id="qb-service" name="service"><option value="">Any service</option>{svc_opts}</select></div></div>
      <div class="qb-field">{icon('target')}<div><label for="qb-goal">Main goal</label><select id="qb-goal" name="goal"><option value="">Any goal</option><option>Get more customers</option><option>Look professional online</option><option>Grow my following</option><option>Run ads</option></select></div></div>
      <div class="qb-field">{icon('zap')}<div><label for="qb-budget">Budget range</label><select id="qb-budget" name="budget"><option value="">Not sure yet</option><option>Starter</option><option>Growth</option><option>Scale</option></select></div></div>
      <button class="qb-submit" type="submit" aria-label="Start a Project"><span class="qb-label">Start a Project</span>{icon('arrow')}</button>
    </form>
  </div>
  <div class="hero-visual">{img(c, 'assets/images/hero/hero-main.svg', 'Illustration of a website, a social media post and a growth chart above a city skyline at sunset', 1200, 900, lazy=False)}{SWOOSH}</div>
  <a class="hero-badge" href="{c.u('pages/about.html')}"><span class="ring">{icon('spark')}</span><span>We grow<br>small businesses</span></a>
</section>
<ul class="trust">
  <li><span class="t-ic">{icon('shield')}</span><div><strong>Strategy-Led</strong><span>Goals before tactics</span></div></li>
  <li><span class="t-ic">{icon('users')}</span><div><strong>Small-Business Focus</strong><span>Sized to your budget</span></div></li>
  <li><span class="t-ic">{icon('layers')}</span><div><strong>Clear Process</strong><span>Simple, open steps</span></div></li>
  <li><span class="t-ic">{icon('globe')}</span><div><strong>Full-Service</strong><span>Web, social, ads, content</span></div></li>
</ul></div>'''

def hero_inner(c, active, kicker, h1, lead, crumbs, image, alt, ctas=''):
    cr = ''.join((f'<li><a href="{c.u(t)}">{E(n)}</a></li>' if t else f'<li aria-current="page">{E(n)}</li>') for n, t in crumbs)
    return f'''<div class="shell hero-shell hero-inner">{header(c, active)}
<section class="hero" id="main-content" tabindex="-1" aria-labelledby="hero-title">
  <div class="hero-copy">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>{cr}</ol></nav>
    <p class="hero-kicker">{E(kicker)}</p>
    <h1 id="hero-title">{h1}</h1>
    <p class="hero-lead">{E(lead)}</p>
    {f'<div class="hero-ctas">{ctas}</div>' if ctas else ''}
  </div>
  <div class="hero-visual">{img(c, image, alt, 1200, 900, lazy=False)}{SWOOSH}</div>
</section></div>'''

def eyebrow(t, ic='spark'): return f'<span class="eyebrow">{icon(ic)}{E(t)}</span>'

def section_head(eb, title, link=None, ic='spark', dark=False):
    l = f'<a class="link-arrow" href="{link[0]}">{E(link[1])}{icon("arrow")}</a>' if link else ''
    return f'<div class="section-head {rv()}"><div>{eyebrow(eb, ic)}<h2 class="section-title">{title}</h2></div>{l}</div>'

# ---------------------------------------------------------------- sections
def work_card(c, p, i=0):
    meta = ''.join(f'<li>{icon(ic)}{E(t)}</li>' for ic, t in zip(['layout', 'code', 'search'] if p['filter'] == 'web' else ['spark', 'layers', 'target'], p['tags']))
    href = c.u(f'projects/{p["slug"]}.html')
    return f'''<article class="work-card {rv(i)}" data-cat="{p['filter']}">
  <a class="work-media" href="{href}" tabindex="-1" aria-hidden="true">{img(c, p['image'], f'Sample illustration for {p["title"]}', 800, 600)}<span class="pill pill-light">{E(p['category'])}</span><span class="pill pill-sample">Sample</span></a>
  <div class="work-body"><h3><a href="{href}">{E(p['title'])}</a></h3><p class="work-loc">{icon('pin')}Sample concept · fictional brand</p>
  <ul class="work-meta">{meta}</ul><p class="work-sum">{E(p['summary'])}</p>
  <div class="work-foot"><span class="work-label">View Project</span><a class="round-btn" href="{href}" aria-label="View project: {E(p['title'])}">{icon('arrow')}</a></div></div></article>'''

def filters(items, target, label):
    b = '<button type="button" class="chip is-active" data-filter="all" aria-pressed="true">All</button>' + ''.join(f'<button type="button" class="chip" data-filter="{k}" aria-pressed="false">{E(n)}</button>' for k, n in items)
    return f'<div class="filters {rv()}" role="group" aria-label="{label}" data-filter-target="{target}">{b}</div>'

def sec_work(c, page=False):
    fl = [('web', 'Websites'), ('social', 'Social Media'), ('ads', 'Advertising')]
    cards = ''.join(work_card(c, p, i) for i, p in enumerate(PROJECTS))
    head = '' if page else section_head('Featured Work', 'Handpicked Work Made<br>to Grow Small Brands', (c.u('pages/work.html'), 'View All Work'), 'layers')
    return f'''<section class="section {'section-work' if not page else 'section-tight'}" aria-labelledby="{'work-h' if page else 'x'}"><div class="container">{head}{filters(fl, '#work-grid', 'Filter projects by category')}
<div class="work-grid" id="work-grid">{cards}</div><p class="empty-state" hidden>No projects in this category yet.</p>
<p class="sample-note {rv()}">All projects shown are clearly labelled sample concepts for fictional brands. Real client work will be added when it is ready to share.</p></div></section>'''

def sec_why(c):
    items = [('users', 'Clear Guidance', 'Plain-language advice, no jargon.'), ('layers', 'One Team, Five Services', 'Web, social, ads and content together.'),
             ('shield', 'Transparent Process', 'You know what happens and when.'), ('target', 'Made for Small Business', 'Plans sized to your budget and goals.')]
    f = ''.join(f'<li class="{rv(i)}"><span class="f-ic">{icon(ic)}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (ic, t, d) in enumerate(items))
    return f'''<section class="section section-panel" aria-labelledby="why-h"><div class="container"><div class="panel-dark why-panel">
  <div class="why-copy {rv()}">{eyebrow('Why Choose NOVIQ', 'spark').replace('eyebrow', 'eyebrow eyebrow-gold')}<h2 id="why-h" class="panel-title">Your Growth Partner for Everything Digital</h2>
  <p>From your first website to your next campaign, we make marketing simple, practical and built around what your business actually needs.</p><ul class="why-list">{f}</ul>{btn(c, 'pages/about.html', 'Learn More')}</div>
  <div class="why-visual">{img(c, 'assets/images/general/why.svg', 'Illustration of a website and social media post beside a rising growth chart', 1000, 800)}<svg class="hero-swoosh" viewBox="0 0 1 1" preserveAspectRatio="none" aria-hidden="true"><path class="sw-d" d="M0.10,1 C0.26,0.72 0.02,0.36 0.30,0" fill="none" stroke="url(#swg)" stroke-width="12" vector-effect="non-scaling-stroke" stroke-linecap="round" opacity=".9"/></svg></div></div></div></section>'''

def sec_services(c):
    cards = ''.join(f'<a class="mini-card {rv(i)}" href="{c.u("pages/" + s["slug"] + ".html")}"><span class="mini-ic">{icon(s["icon"])}</span><h3>{E(s["title"])}</h3><p>{E(s["short"])}</p></a>' for i, s in enumerate(SERVICES))
    return f'''<section class="section section-tight" aria-labelledby="svc-h"><div class="container">
  <div class="section-head {rv()}"><div>{eyebrow('Our Services', 'briefcase')}<h2 id="svc-h" class="section-title">More Than Just Websites.<br>Complete Digital Solutions.</h2></div><a class="link-arrow" href="{c.u('pages/services.html')}">Explore All Services{icon('arrow')}</a></div>
  <div class="mini-grid">{cards}</div></div></section>'''

STEPS = [('search', 'Discover', 'We learn your business, customers and goals.'), ('target', 'Strategy', 'We agree a clear plan and priorities.'),
         ('pen', 'Create', 'We design, build and produce the work.'), ('zap', 'Launch', 'We go live with everything checked.'), ('trending', 'Grow', 'We track results and keep improving.')]

def sec_process(c, sid='process'):
    rows = ''.join(f'<li class="{rv(i)}"><span class="step-no">0{i+1}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (ic, t, d) in enumerate(STEPS))
    return f'''<section class="section section-panel" id="{sid}" aria-labelledby="{sid}-h"><div class="container"><div class="panel-dark process-panel">
  <div class="process-copy {rv()}">{eyebrow('How We Work', 'layers').replace('eyebrow', 'eyebrow eyebrow-gold')}<h2 id="{sid}-h" class="panel-title">From First Idea<br>to Visible Impact</h2><p>A simple five-step process keeps every project clear, on track and easy to follow.</p><ol class="step-list">{rows}</ol>{btn(c, 'pages/contact.html#project-form', 'Start a Project')}</div>
  <div class="collage {rv(2)}"><figure class="c-main">{img(c, 'assets/images/services/web-development.svg', 'Illustration of a website design on a laptop-style browser window', 800, 600)}</figure><figure>{img(c, 'assets/images/services/social-media.svg', 'Illustration of a social media post on a phone', 800, 600)}</figure><figure>{img(c, 'assets/images/services/advertising.svg', 'Illustration of an advertising target and performance chart', 800, 600)}</figure>
  <span class="badge-circle">{icon('spark')}<span>Ideas to Impact</span></span></div></div></div></section>'''

def sec_testimonials(c):
    slides = ''.join(f'''<figure class="t-slide" data-slide><div class="t-head"><span class="avatar" aria-hidden="true">{E(t['initials'])}</span><div><strong>{E(t['name'])}</strong><span>{E(t['role'])}</span></div></div>
<div class="stars" role="img" aria-label="5 out of 5 stars">{icon('star') * 5}</div><blockquote>“{E(t['quote'])}”</blockquote><figcaption class="ph-tag">Placeholder testimonial: replace with real client feedback.</figcaption></figure>''' for t in TESTIS)
    return f'''<section class="section section-tight" aria-labelledby="testi-h"><div class="container testi-wrap">
  <div class="testi-copy">{f'<div class="{rv()}">' }{eyebrow('What Clients Say', 'heart')}<h2 id="testi-h" class="section-title">Real Stories.<br>Real Growth.</h2><p class="lead-sm">Feedback from the small businesses we work with will appear here.</p></div>
  <div class="t-card {rv(1)}" data-slider aria-roledescription="carousel" aria-label="Client testimonials"><div class="t-slides" aria-live="polite">{slides}</div>
  <div class="t-controls"><button type="button" class="ctl" data-prev aria-label="Previous testimonial">{icon('chev-l')}</button><div class="dots" role="presentation"></div><button type="button" class="ctl" data-next aria-label="Next testimonial">{icon('chev-r')}</button></div></div></div>
  <div class="testi-visual {rv(2)}">{img(c, 'assets/images/testimonials/testimonial.svg', 'Illustration of a website and growth chart above a skyline at sunset', 800, 900)}<span class="badge-circle badge-circle-dark">{icon('users')}<span>Built for Small Business</span></span></div></div></section>'''.replace('<div class="reveal', '<div class="reveal', 1)

def sec_specialists(c):
    sp_ = [('code', 'Web Development', 'Websites and landing pages', 'service-web-development'), ('trending', 'Social Media', 'Strategy, campaigns and management', 'service-social-media'),
           ('megaphone', 'Advertising', 'Campaigns and performance tracking', 'service-advertising'), ('camera', 'Content Creation', 'Graphics and short-form video', 'service-content')]
    cards = ''.join(f'<article class="spec-card {rv(i)}"><span class="spec-av">{icon(ic)}</span><h3>{t}</h3><p>{d}</p><a class="spec-foot" href="{c.u("pages/" + s + ".html")}"><span>View service</span><span class="round-btn round-sm">{icon("arrow")}</span></a></article>' for i, (ic, t, d, s) in enumerate(sp_))
    return f'''<section class="section section-tight" aria-labelledby="spec-h"><div class="container">
  <div class="section-head {rv()}"><div>{eyebrow('Meet the Specialists', 'users')}<h2 id="spec-h" class="section-title">Focused Teams.<br>Real Support.</h2></div><a class="link-arrow" href="{c.u('pages/services.html')}">View All Services{icon('arrow')}</a></div>
  <div class="spec-grid">{cards}</div><p class="sample-note {rv()}">Team profiles will be added here once they are ready to share.</p></div></section>'''

def art_card(c, a, i=0):
    href = c.u(f'blog/{a["slug"]}.html')
    return f'''<article class="art-card {rv(i)}" data-cat="{a['category'].lower().replace(' ', '-')}"><a class="art-media" href="{href}" tabindex="-1" aria-hidden="true">{img(c, a['image'], f'Illustration for the article: {a["title"]}', 800, 520)}<span class="pill pill-light">{E(a['category'])}</span></a>
  <div class="art-body"><p class="art-date">{fmt_date(a['date'])} · {a['read']}</p><h3><a href="{href}">{E(a['title'])}</a></h3><p class="art-ex">{E(a['excerpt'])}</p><a class="link-arrow" href="{href}">Read More{icon('arrow')}<span class="sr-only"> about {E(a['title'])}</span></a></div></article>'''

def sec_insights(c, page=False):
    cats = ['Marketing', 'Social Media', 'Websites', 'Advertising', 'Small Business', 'Content']
    fl = filters([(x.lower().replace(' ', '-'), x) for x in cats], '#art-grid', 'Filter articles by category') if page else ''
    head = '' if page else f'<div class="section-head {rv()}"><div>{eyebrow("Latest News", "pen")}<h2 class="section-title">Marketing Insights<br>&amp; Practical Tips</h2><p class="lead-sm">Simple advice for small businesses. Sample articles, ready to be replaced.</p></div><a class="link-arrow" href="{c.u("pages/insights.html")}">View All Articles{icon("arrow")}</a></div>'
    return f'''<section class="section section-tight" aria-label="Articles"><div class="container">{head}{fl}<div class="art-grid" id="art-grid">{''.join(art_card(c, a, i) for i, a in enumerate(ARTICLES))}</div><p class="empty-state" hidden>No articles in this category yet. Check back soon.</p></div></section>'''

def sec_cta(c, title='Your Next Idea Is<br>Just a Message Away', text='Tell us about your business and what you want to achieve. We will reply with clear next steps, no jargon and no pressure.'):
    b = contact_bits()
    return f'''<section class="section section-panel" aria-labelledby="cta-h"><div class="container"><div class="cta-panel">
  {img(c, 'assets/images/general/cta.svg', '', 1400, 700, cls='cta-bg', extra='aria-hidden="true"')}<div class="cta-copy"><h2 id="cta-h" class="panel-title">{title}</h2><p>{text}</p>{btn(c, 'pages/contact.html#project-form', "Let's Talk")}</div>
  <div class="cta-card"><ul><li>{icon('whatsapp')}<span>{b['wa']}</span></li><li>{icon('mail')}<span>{b['email']}</span></li><li>{icon('pin')}<span>{b['loc']}</span></li></ul>{socials(c)}</div></div></div></section>'''

def footer(c):
    svc = ''.join(f'<li><a href="{c.u("pages/" + s["slug"] + ".html")}">{E(s["title"])}</a></li>' for s in SERVICES)
    q = ''.join(f'<li><a href="{c.u(t)}">{n}</a></li>' for n, t, k in NAV)
    return f'''<footer class="site-footer"><div class="foot-panel"><div class="foot-grid">
  <div class="foot-brand"><a class="brand" href="{c.u('index.html')}"><img class="brand-logo" src="{c.u('assets/images/logo/logo-light.png')}" alt="NOVIQ, Ideas to Impact: home" width="476" height="258" loading="lazy" decoding="async"></a><p>We grow small businesses through websites, social media, advertising and creative content.</p></div>
  <nav aria-label="Quick links"><h2>Quick Links</h2><ul>{q}</ul></nav>
  <nav aria-label="Services"><h2>Services</h2><ul>{svc}</ul></nav>
  <nav aria-label="Support"><h2>Support</h2><ul><li><a href="{c.u('pages/contact.html')}">Contact Us</a></li><li><a href="{c.u('pages/contact.html')}#project-form">Start a Project</a></li><li><a href="{c.u('pages/contact.html')}#faq">FAQs</a></li><li><a href="{c.u('index.html')}#process">Our Process</a></li></ul></nav>
  <div class="foot-news"><h2>Newsletter</h2><p>Get marketing tips for small businesses.</p><form class="newsletter" data-form="newsletter" data-endpoint="{E(SITE['newsletter_endpoint'])}" novalidate><label class="sr-only" for="nl-email-{c.depth}">Email address</label><input id="nl-email-{c.depth}" name="email" type="email" placeholder="Your email address" autocomplete="email" required><button class="btn btn-gold" type="submit" aria-label="Subscribe">{icon('arrow')}</button></form><p class="form-status" role="status" aria-live="polite"></p></div>
</div>
<div class="foot-bottom"><p class="script">Ideas to Impact.</p><p>© 2026 NOVIQ. All rights reserved.</p></div></div></footer>'''

# ---------------------------------------------------------------- page shell
def breadcrumb_ld(c, crumbs):
    items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": URL + '/' + t} for i, (n, t) in enumerate(crumbs)]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def org_ld():
    o = {"@context": "https://schema.org", "@type": "ProfessionalService", "@id": URL + "/#organization", "name": "NOVIQ", "slogan": "Ideas to Impact",
         "description": "NOVIQ is a digital marketing and creative agency that helps small businesses grow through web development, social media, advertising and content creation.",
         "url": URL + "/", "logo": URL + "/assets/images/logo/logo.png", "image": URL + "/" + OG,
         "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s['title']}} for s in SERVICES]}
    if SITE['email'].strip(): o['email'] = SITE['email'].strip()
    if SITE['phone'].strip(): o['telephone'] = SITE['phone'].strip()
    same = [v for v in SITE['social'].values() if v.strip()]
    if same: o['sameAs'] = same
    return o

def page(path, title, desc, hero, body, active, css=None, js=None, ld=None, og_type='website', body_class=''):
    c = Ctx(path)
    css_files = ['style', 'components'] + ([f'pages/{css}'] if css else []) + ['responsive']
    css_html = ''.join(f'<link rel="stylesheet" href="{c.u("css/" + f + ".css")}">' for f in css_files)
    js_files = ['main', 'navigation', 'animations', 'forms'] and ['main', 'navigation', 'animations', 'forms'] + [f'pages/{j}' for j in (js or [])]
    js_html = ''.join(f'<script src="{c.u("js/" + f + ".js")}" defer></script>' for f in js_files)
    lds = [org_ld()] + (ld or [])
    ld_html = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    og = f'{URL}/{OG}'
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{c.canon()}">
<meta name="theme-color" content="#072f23">
<link rel="icon" type="image/png" sizes="64x64" href="{c.u('assets/icons/favicon.png')}">
<link rel="apple-touch-icon" href="{c.u('assets/icons/apple-touch-icon.png')}">
<meta property="og:site_name" content="NOVIQ"><meta property="og:type" content="{og_type}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{c.canon()}"><meta property="og:image" content="{og}"><meta property="og:image:alt" content="NOVIQ: Ideas to Impact"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{og}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&amp;family=Poppins:wght@400;500;600;700&amp;display=swap">
<script>document.documentElement.classList.add('js')</script>
{css_html}
{ld_html}
</head>
<body class="{body_class}">
{SPRITE}
<a class="skip-link" href="#main-content">Skip to content</a>
<div class="page-wrap">{hero(c)}</div>
<main>{body(c)}</main>
<div class="page-wrap">{footer(c)}</div>
{js_html}
</body>
</html>'''
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(out)
    return path

# ---------------------------------------------------------------- pages
PAGES = []
def crumbs_for(*items): return [('Home', 'index.html')] + list(items)

def build_home():
    PAGES.append(page('index.html', 'NOVIQ | Ideas to Impact: Digital Marketing & Creative Agency',
        'NOVIQ is a digital marketing and creative agency that helps small businesses grow with websites, social media, advertising and content creation.',
        hero_home, lambda c: sec_work(c) + sec_why(c) + sec_services(c) + sec_process(c) + sec_testimonials(c) + sec_specialists(c) + sec_insights(c) + sec_cta(c),
        'home', 'home', ['filters', 'testimonials'],
        [{"@context": "https://schema.org", "@type": "WebSite", "name": "NOVIQ", "url": URL + "/", "publisher": {"@id": URL + "/#organization"}}], body_class='page-home'))

def service_cards_lg(c):
    cards = ''
    for i, s in enumerate(SERVICES):
        feats = ''.join(f'<li>{icon("check")}{E(f)}</li>' for f in s['features'])
        cards += f'''<article class="svc-card {rv(i)}"><span class="mini-ic">{icon(s['icon'])}</span><h3>{E(s['title'])}</h3><p>{E(s['short'])}</p><ul class="check-list">{feats}</ul><a class="link-arrow" href="{c.u('pages/' + s['slug'] + '.html')}">Learn more<span class="sr-only"> about {E(s['title'])}</span>{icon('arrow')}</a></article>'''
    cards += f'''<article class="svc-card svc-cta {rv(5)}"><h3>Not sure what you need?</h3><p>Tell us about your business and we will suggest a sensible starting point.</p>{btn(c, 'pages/contact.html#project-form', "Let's Talk")}</article>'''
    return f'<section class="section section-tight" aria-labelledby="svc-lg-h"><div class="container">{section_head("What We Do", "Five Services.<br>One Goal: Your Growth.", None, "briefcase").replace("<h2 ", "<h2 id=\"svc-lg-h\" ")}<div class="svc-grid">{cards}</div></div></section>'

def build_services():
    PAGES.append(page('pages/services.html', 'Services | NOVIQ Digital Marketing & Creative Agency',
        'Web development, social media marketing, social media management, advertising and content creation for small businesses.',
        lambda c: hero_inner(c, 'services', 'Our Services', 'Services Built to <span class="gold">Grow</span> Small Businesses', 'Everything a small business needs to be seen, trusted and chosen online, from one team.', crumbs_for(('Services', None)), 'assets/images/hero/hero-alt.svg', 'Illustration of a phone, website and growth chart at sunset', btn(c, 'pages/contact.html#project-form', 'Start a Project') + btn(c, 'pages/work.html', 'Explore Our Work', 'btn-ghost')),
        lambda c: service_cards_lg(c) + sec_why(c) + sec_process(c) + sec_cta(c), 'services', 'services',
        ld=[breadcrumb_ld(Ctx('pages/services.html'), [('Home', 'index.html'), ('Services', 'pages/services.html')]),
            {"@context": "https://schema.org", "@type": "ItemList", "name": "NOVIQ services", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{URL}/pages/{s['slug']}.html", "name": s['title']} for i, s in enumerate(SERVICES)]}]))

def build_service_pages():
    for s in SERVICES:
        path = f'pages/{s["slug"]}.html'
        def body(c, s=s):
            inc = ''.join(f'<li class="{rv(i)}"><span class="f-ic">{icon(ic)}</span><div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for i, (ic, t, d) in enumerate(s['includes']))
            steps = ''.join(f'<li class="mini-card {rv(i)}"><span class="step-no step-no-light">0{i+1}</span><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(s['steps']))
            others = ''.join(f'<a class="mini-card {rv(i)}" href="{c.u("pages/" + o["slug"] + ".html")}"><span class="mini-ic">{icon(o["icon"])}</span><h3>{E(o["title"])}</h3><p>{E(o["short"])}</p></a>' for i, o in enumerate([x for x in SERVICES if x is not s]))
            return f'''<section class="section section-panel" aria-labelledby="inc-h"><div class="container"><div class="panel-dark process-panel">
  <div class="process-copy">{eyebrow("What's Included", "check").replace("eyebrow", "eyebrow eyebrow-gold")}<h2 id="inc-h" class="panel-title">What You Get With {E(s['title'])}</h2><ul class="why-list why-list-1">{inc}</ul></div>
  <div class="collage collage-single"><figure class="c-main">{img(c, s['image'], f'Illustration representing {s["title"]}', 800, 600)}</figure><span class="badge-circle">{icon(s['icon'])}<span>{E(s['title'])}</span></span></div></div></div></section>
<section class="section section-tight" aria-labelledby="for-h"><div class="container split"><div class="{rv()}">{eyebrow('Who It Is For', 'users')}<h2 id="for-h" class="section-title">Made for Small Businesses</h2><p class="lead-sm">{E(s['for'])}</p><ul class="check-list check-list-lg">{''.join(f'<li>{icon("check")}{E(f)}</li>' for f in s['features'])}</ul></div>
<div class="{rv(1)}">{eyebrow('How It Works', 'layers')}<h2 class="section-title">Four Simple Steps</h2><ol class="mini-grid mini-grid-2">{steps}</ol></div></div></section>
<section class="section section-tight" aria-labelledby="oth-h"><div class="container"><div class="section-head {rv()}"><div>{eyebrow('More From NOVIQ', 'briefcase')}<h2 id="oth-h" class="section-title">Explore Our Other Services</h2></div><a class="link-arrow" href="{c.u('pages/services.html')}">All Services{icon('arrow')}</a></div><div class="mini-grid mini-grid-4">{others}</div></div></section>''' + sec_cta(c)
        PAGES.append(page(path, f'{s["title"]} | NOVIQ', s['meta'],
            lambda c, s=s: hero_inner(c, 'services', s['title'], s['hero_title'], s['lead'], crumbs_for(('Services', 'pages/services.html'), (s['title'], None)), s['image'], f'Illustration representing {s["title"]}', btn(c, 'pages/contact.html#project-form', 'Start a Project') + btn(c, 'pages/work.html', 'Explore Our Work', 'btn-ghost')),
            body, 'services', 'services',
            ld=[breadcrumb_ld(None, [('Home', 'index.html'), ('Services', 'pages/services.html'), (s['title'], path)]),
                {"@context": "https://schema.org", "@type": "Service", "name": s['title'], "description": s['meta'], "provider": {"@id": URL + "/#organization"}, "url": f"{URL}/{path}", "serviceType": s['title']}]))

def build_work():
    PAGES.append(page('pages/work.html', 'Our Work | NOVIQ Sample Projects',
        'Explore sample website, social media and advertising projects from NOVIQ, a digital marketing and creative agency for small businesses.',
        lambda c: hero_inner(c, 'work', 'Our Work', 'Work Made to <span class="gold">Grow</span> Small Brands', 'A look at how we approach websites, social media and advertising, shown through sample concept projects.', crumbs_for(('Our Work', None)), 'assets/images/hero/hero-main.svg', 'Illustration of a website, phone and growth chart above a skyline', btn(c, 'pages/contact.html#project-form', 'Start a Project')),
        lambda c: sec_work(c, True) + sec_cta(c, 'Want Your Project<br>on This Page?'), 'work', 'work', ['filters'],
        ld=[breadcrumb_ld(None, [('Home', 'index.html'), ('Our Work', 'pages/work.html')]), {"@context": "https://schema.org", "@type": "CollectionPage", "name": "NOVIQ sample projects", "url": URL + "/pages/work.html"}]))

def build_projects():
    for i, p in enumerate(PROJECTS):
        path = f'projects/{p["slug"]}.html'
        nxt = PROJECTS[(i + 1) % len(PROJECTS)]
        def body(c, p=p, nxt=nxt):
            ap = ''.join(f'<li>{icon("check")}{E(x)}</li>' for x in p['approach'])
            dl = ''.join(f'<li>{icon("check")}{E(x)}</li>' for x in p['deliverables'])
            return f'''<section class="section section-tight"><div class="container">
<div class="notice {rv()}">{icon('spark')}<p><strong>Sample project.</strong> This concept was created to show how NOVIQ approaches this kind of work. It is not a real client engagement.</p></div>
<div class="proj-media {rv()}">{img(c, p['image'], f'Sample illustration for {p["title"]}', 800, 600, lazy=False)}</div>
<dl class="proj-facts {rv()}"><div><dt>Category</dt><dd>{E(p['category'])}</dd></div><div><dt>Client</dt><dd>Fictional brand</dd></div><div><dt>Status</dt><dd>Sample concept</dd></div><div><dt>Focus</dt><dd>{E(', '.join(p['tags']))}</dd></div></dl>
<div class="proj-cols"><article class="{rv()}"><h2 class="section-title sm">The brief</h2><p class="lead-sm">{E(p['brief'])}</p></article>
<article class="{rv(1)}"><h2 class="section-title sm">Our approach</h2><ul class="check-list check-list-lg">{ap}</ul></article>
<article class="{rv(2)}"><h2 class="section-title sm">Deliverables</h2><ul class="check-list check-list-lg">{dl}</ul></article></div>
<div class="proj-next {rv()}"><a class="link-arrow" href="{c.u('pages/work.html')}">{icon('chev-l')}All projects</a><a class="link-arrow" href="{c.u('projects/' + nxt['slug'] + '.html')}">Next: {E(nxt['title'])}{icon('arrow')}</a></div></div></section>''' + sec_cta(c)
        PAGES.append(page(path, f'{p["title"]} | Sample Project | NOVIQ', p['summary'],
            lambda c, p=p: hero_inner(c, 'work', p['category'], E(p['title']), p['summary'], crumbs_for(('Our Work', 'pages/work.html'), (p['title'], None)), p['image'], f'Sample illustration for {p["title"]}', btn(c, 'pages/' + p['service_slug'] + '.html', 'About This Service') + btn(c, 'pages/contact.html#project-form', 'Start a Project', 'btn-ghost')),
            body, 'work', 'work',
            ld=[breadcrumb_ld(None, [('Home', 'index.html'), ('Our Work', 'pages/work.html'), (p['title'], path)]), {"@context": "https://schema.org", "@type": "CreativeWork", "name": p['title'], "description": p['summary'] + " (Sample concept for a fictional brand.)", "creator": {"@id": URL + "/#organization"}}]))

def build_about():
    def body(c):
        cards = [('users', 'Who we serve', 'Independent shops, cafés, local service providers, studios and other small businesses that want to be seen and chosen online.'),
                 ('briefcase', 'What we do', 'Web development, social media marketing and management, advertising and content creation, all under one roof.'),
                 ('heart', 'Why we exist', 'Many small businesses have good ideas but limited time, budget and marketing know-how. NOVIQ closes that gap with clear plans and creative work sized to fit.')]
        cc = ''.join(f'<article class="mini-card mini-card-lg {rv(i)}"><span class="mini-ic">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate(cards))
        vals = [('eye' if False else 'search', 'Clarity', 'Plain language, clear plans and no hidden steps.'), ('pen', 'Craft', 'Careful design and build, whatever the size of the project.'), ('heart', 'Care', 'We treat your business as if it were our own.'), ('target', 'Accountability', 'We set goals and measure progress against them.')]
        vv = ''.join(f'<li class="mini-card {rv(i)}"><span class="mini-ic">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></li>' for i, (ic, t, d) in enumerate(vals))
        return f'''<section class="section section-tight" aria-labelledby="who-h"><div class="container about-split"><div class="about-copy {rv()}">{eyebrow('Who We Are', 'spark')}<h2 id="who-h" class="section-title">A Marketing and Creative Agency for Small Businesses</h2>
<p class="lead-sm">NOVIQ helps small businesses turn ideas into visible, practical and measurable digital impact.</p><p>We combine strategy and creative work so that your website, social media, advertising and content all pull in the same direction. We keep things simple, explain what we are doing and size every plan to your goals.</p>{btn(c, 'pages/contact.html#project-form', "Let's Talk")}</div>
<div class="about-visual {rv(1)}">{img(c, 'assets/images/general/about.svg', 'Illustration of a website and social media post above a skyline at sunset', 800, 900)}</div></div></section>
<section class="section section-tight"><div class="container"><div class="mini-grid mini-grid-3">{cc}</div></div></section>
<section class="section section-panel" aria-labelledby="meaning-h"><div class="container"><div class="panel-dark meaning-panel"><div class="meaning-head {rv()}">{eyebrow('Our Name and Tagline', 'spark').replace('eyebrow', 'eyebrow eyebrow-gold')}<h2 id="meaning-h" class="panel-title">The Meaning Behind “Ideas to Impact”</h2></div>
<div class="meaning-cols"><div class="{rv(1)}"><h3>Ideas</h3><p>Every business starts with an idea: a product, a service or a better way of doing something. Ideas are where we begin.</p></div><span class="meaning-arrow" aria-hidden="true">{icon('arrow')}</span><div class="{rv(2)}"><h3>Impact</h3><p>Impact is when that idea is seen, understood and chosen, through a website that converts, content that connects and advertising that reaches the right people.</p></div></div></div></div></section>
<section class="section section-tight" aria-labelledby="val-h"><div class="container">{section_head('What We Value', 'How We Work With You', None, 'heart').replace('<h2 ', '<h2 id="val-h" ')}<ul class="mini-grid mini-grid-4">{vv}</ul></div></section>''' + sec_process(c, 'process') + sec_cta(c)
    PAGES.append(page('pages/about.html', 'About NOVIQ | Ideas to Impact for Small Businesses',
        'Learn who NOVIQ is, who we serve and why we exist: helping small businesses turn ideas into visible, practical and measurable digital impact.',
        lambda c: hero_inner(c, 'about', 'About NOVIQ', 'Ideas Into <span class="gold">Impact</span>, for Small Businesses', 'We help small businesses turn ideas into visible, practical and measurable digital impact.', crumbs_for(('About', None)), 'assets/images/hero/hero-alt.svg', 'Illustration of a phone, website and growth chart at sunset', btn(c, 'pages/services.html', 'Our Services') + btn(c, 'pages/contact.html#project-form', 'Start a Project', 'btn-ghost')),
        body, 'about', 'about',
        ld=[breadcrumb_ld(None, [('Home', 'index.html'), ('About', 'pages/about.html')]), {"@context": "https://schema.org", "@type": "AboutPage", "name": "About NOVIQ", "url": URL + "/pages/about.html"}]))

def build_insights():
    PAGES.append(page('pages/insights.html', 'Insights | Marketing Tips for Small Businesses | NOVIQ',
        'Practical marketing, social media, website and advertising advice for small businesses from NOVIQ.',
        lambda c: hero_inner(c, 'insights', 'Insights', 'Marketing Insights &amp; <span class="gold">Practical</span> Tips', 'Simple, honest advice on websites, social media, advertising and content for small businesses.', crumbs_for(('Insights', None)), 'assets/images/hero/hero-alt.svg', 'Illustration of a phone, website and growth chart at sunset'),
        lambda c: sec_insights(c, True) + f'<section class="section section-tight"><div class="container"><p class="sample-note">These are sample articles that can be replaced with your own. See data/articles.json.</p></div></section>' + sec_cta(c), 'insights', 'insights', ['filters'],
        ld=[breadcrumb_ld(None, [('Home', 'index.html'), ('Insights', 'pages/insights.html')]), {"@context": "https://schema.org", "@type": "Blog", "name": "NOVIQ Insights", "url": URL + "/pages/insights.html"}]))

def build_articles():
    for i, a in enumerate(ARTICLES):
        path = f'blog/{a["slug"]}.html'
        def body(c, a=a):
            parts = ''
            for b in a['body']:
                if b['t'] == 'p': parts += f'<p>{E(b["x"])}</p>'
                elif b['t'] == 'h2': parts += f'<h2>{E(b["x"])}</h2>'
                else: parts += '<ul>' + ''.join(f'<li>{E(x)}</li>' for x in b['x']) + '</ul>'
            rel = ''.join(art_card(c, x, j) for j, x in enumerate([y for y in ARTICLES if y is not a]))
            return f'''<section class="section section-tight"><div class="container"><article class="article"><figure class="art-hero">{img(c, a['image'], f'Illustration for the article: {a["title"]}', 800, 520, lazy=False)}</figure>
<p class="art-meta">By the NOVIQ team · {fmt_date(a['date'])} · {a['read']}</p><div class="prose">{parts}</div><p class="sample-note">Sample article: replace with your own content.</p></article></div></section>
<section class="section section-tight"><div class="container"><div class="section-head"><div>{eyebrow('Keep Reading', 'pen')}<h2 class="section-title">More Insights</h2></div><a class="link-arrow" href="{c.u('pages/insights.html')}">All Articles{icon('arrow')}</a></div><div class="art-grid art-grid-2">{rel}</div></div></section>''' + sec_cta(c)
        PAGES.append(page(path, f'{a["title"]} | NOVIQ Insights', a['excerpt'],
            lambda c, a=a: hero_inner(c, 'insights', a['category'], E(a['title']), a['excerpt'], crumbs_for(('Insights', 'pages/insights.html'), (a['category'], None)), a['image'], f'Illustration for the article: {a["title"]}'),
            body, 'insights', 'insights', og_type='article',
            ld=[breadcrumb_ld(None, [('Home', 'index.html'), ('Insights', 'pages/insights.html'), (a['title'], path)]),
                {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a['title'], "description": a['excerpt'], "datePublished": a['date'], "dateModified": a['date'], "image": f"{URL}/{a['image']}", "author": {"@id": URL + "/#organization"}, "publisher": {"@id": URL + "/#organization"}, "mainEntityOfPage": f"{URL}/{path}"}]))

def build_contact():
    b = contact_bits()
    def body(c):
        svc_opts = ''.join(f'<option>{E(s["title"])}</option>' for s in SERVICES) + '<option>Not sure yet</option>'
        methods = f'''<ul class="contact-methods">
<li id="whatsapp" class="{rv()}"><span class="f-ic">{icon('whatsapp')}</span><div><h3>WhatsApp</h3><p>{b['wa']}</p></div></li>
<li class="{rv(1)}"><span class="f-ic">{icon('phone')}</span><div><h3>Phone</h3><p>{b['phone']}</p></div></li>
<li id="email" class="{rv(2)}"><span class="f-ic">{icon('mail')}</span><div><h3>Email</h3><p>{b['email']}</p></div></li>
<li class="{rv(3)}"><span class="f-ic">{icon('pin')}</span><div><h3>Location</h3><p>{b['loc']}</p></div></li></ul>
<div id="social" class="social-block {rv(4)}"><h3>Follow NOVIQ</h3>{socials(c)}<p class="ph-note">Social links will appear here once accounts are added.</p></div>'''
        form = f'''<form class="contact-form {rv(1)}" id="project-form" data-form="contact" data-endpoint="{E(SITE['form_endpoint'])}" data-email="{E(SITE['email'])}" novalidate>
<h2 class="form-title">Tell us about your project</h2>
<div class="field-row"><div class="field"><label for="f-name">Name <span class="req">*</span></label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="f-biz">Business name</label><input id="f-biz" name="business" type="text" autocomplete="organization"></div></div>
<div class="field-row"><div class="field"><label for="f-email">Email <span class="req">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div></div>
<div class="field-row"><div class="field"><label for="f-service">Service needed</label><select id="f-service" name="service"><option value="">Select a service</option>{svc_opts}</select></div>
<div class="field"><label for="f-budget">Budget range <span class="opt">(optional)</span></label><select id="f-budget" name="budget"><option value="">Prefer to discuss</option><option>Starter</option><option>Growth</option><option>Scale</option></select></div></div>
<div class="field"><label for="f-msg">Project description <span class="req">*</span></label><textarea id="f-msg" name="message" rows="5" required></textarea></div>
<input type="hidden" name="goal" id="f-goal">
<button class="btn btn-gold btn-lg" type="submit">Let's Talk{icon('arrow')}</button><p class="form-status" role="status" aria-live="polite"></p></form>'''
        faqs = [('How do I start a project?', 'Send us the form above with a few details about your business and what you would like to achieve. We will reply with clear next steps.'),
                ('How long does a project take?', 'It depends on the size and type of work. We agree a realistic schedule with you after our first conversation.'),
                ('Can you work with a small budget?', 'Yes. We focus on small businesses and will recommend a sensible starting point that fits your budget and goals.'),
                ('What should I prepare?', 'It helps to know your main goal, who your customers are and any examples of brands or websites you like. If you do not have these yet, we can help you work them out.')]
        fq = ''.join(f'<details class="faq-item {rv(i)}"><summary>{E(q)}{icon("chev-d")}</summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(faqs))
        return f'''<section class="section section-tight"><div class="container contact-grid"><div class="contact-side"><div class="{rv()}">{eyebrow('Get in Touch', 'chat')}<h2 class="section-title">We would love to hear about your business</h2><p class="lead-sm">Choose whichever way is easiest for you. Details marked as pending will be added before launch.</p></div>{methods}</div>{form}</div></section>
<section class="section section-tight" id="faq" aria-labelledby="faq-h"><div class="container faq-wrap"><div class="{rv()}">{eyebrow('FAQs', 'spark')}<h2 id="faq-h" class="section-title">Common Questions</h2></div><div class="faq-list">{fq}</div></div></section>'''
    PAGES.append(page('pages/contact.html', 'Contact NOVIQ | Start a Project',
        'Contact NOVIQ by WhatsApp, phone, email or the project form to talk about websites, social media, advertising or content for your small business.',
        lambda c: hero_inner(c, 'contact', 'Contact', 'Let’s Grow Your <span class="gold">Business</span> Together', 'Tell us where you are and where you want to go. We will help you plan the next step.', crumbs_for(('Contact', None)), 'assets/images/hero/hero-main.svg', 'Illustration of a website, phone and growth chart above a skyline at sunset'),
        body, 'contact', 'contact', ['contact'],
        ld=[breadcrumb_ld(None, [('Home', 'index.html'), ('Contact', 'pages/contact.html')]), {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact NOVIQ", "url": URL + "/pages/contact.html"}]))

def build_meta():
    urls = ''.join(f'<url><loc>{URL}/{"" if p == "index.html" else p}</loc><lastmod>{SITE["lastmod"]}</lastmod><priority>{"1.0" if p == "index.html" else "0.7"}</priority></url>\n' for p in PAGES)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n')

if __name__ == '__main__':
    build_home(); build_services(); build_service_pages(); build_work(); build_projects(); build_about(); build_insights(); build_articles(); build_contact(); build_meta()
    print(f'built {len(PAGES)} pages')
