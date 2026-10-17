#!/usr/bin/env python3
"""Generates NOVIQ's original SVG artwork (hero, services, portfolio, blog, general). The logo files are the supplied NOVIQ logo.

These are illustrated placeholders in the NOVIQ palette. Replace any of them with real
photography or project screenshots by dropping a file in the same folder and updating the
<img src> (or keep the same filename).
Run:  python3 tools/svgart.py
"""
import os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'images')

GOLD = '#e9b54a'
PAL = {
    'dusk':    dict(sky=['#0b3a37', '#2c6a5c', '#e8a565', '#f9dba4'], sun='#fff1c9', b1='#06281f', b2='#0d4131', win='#ffd987', wat=['#f4c98b', '#0d4a3a']),
    'emerald': dict(sky=['#032a20', '#0a4a38', '#1c7a5c', '#7ccaa6'], sun='#d5f6e3', b1='#031f17', b2='#0a3a2b', win='#f6d98f', wat=['#5fb896', '#083a2c']),
    'sand':    dict(sky=['#dfeae4', '#efeee0', '#f7e3bd', '#f2c987'], sun='#fff6dc', b1='#0b3d2d', b2='#14604a', win='#ffe9b0', wat=['#f1d29a', '#8fc7ae']),
    'night':   dict(sky=['#02110c', '#06241b', '#0d4232', '#1a6a4f'], sun='#f6d98f', b1='#021610', b2='#07301f', win='#f6d98f', wat=['#1a6a4f', '#03170f']),
    'peach':   dict(sky=['#123d33', '#3d7a63', '#f0a86a', '#ffd7a0'], sun='#fff0cf', b1='#082e23', b2='#124c3a', win='#ffe2a0', wat=['#f6c48a', '#164f3d']),
}


def svg(w, h, body, p):
    s = p['sky']
    defs = f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{s[0]}"/><stop offset=".45" stop-color="{s[1]}"/><stop offset=".78" stop-color="{s[2]}"/><stop offset="1" stop-color="{s[3]}"/></linearGradient>
<radialGradient id="sun"><stop offset="0" stop-color="{p['sun']}" stop-opacity="1"/><stop offset=".3" stop-color="{p['sun']}" stop-opacity=".5"/><stop offset="1" stop-color="{p['sun']}" stop-opacity="0"/></radialGradient>
<linearGradient id="wat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p['wat'][0]}"/><stop offset="1" stop-color="{p['wat'][1]}"/></linearGradient>
<linearGradient id="hg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b3d2d"/><stop offset="1" stop-color="#1c7a5c"/></linearGradient>
<linearGradient id="warm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7d08a"/><stop offset="1" stop-color="#e58f57"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="sh" x="-25%" y="-25%" width="150%" height="160%"><feDropShadow dx="0" dy="16" stdDeviation="16" flood-color="#021a12" flood-opacity=".38"/></filter>'''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>{body}</svg>')


def sky(w, h, p, horizon=.74, sun_x=.68, sun_r=.4):
    hy = h * horizon
    return (f'<rect width="{w}" height="{h}" fill="url(#sky)"/>'
            f'<circle cx="{w*sun_x:.0f}" cy="{hy-h*.05:.0f}" r="{h*sun_r:.0f}" fill="url(#sun)"/>'
            f'<circle cx="{w*sun_x:.0f}" cy="{hy-h*.04:.0f}" r="{h*.065:.0f}" fill="{p["sun"]}"/>')


def water(w, h, p, horizon=.74, refl=''):
    hy = h * horizon
    lines = ''.join(f'<rect x="{(i*97)%int(w*.8):.0f}" y="{hy+14+i*((h-hy)/9):.0f}" width="{60+(i*41)%180}" height="3" rx="1.5" fill="#fff" opacity=".18"/>' for i in range(9))
    return f'<rect y="{hy:.0f}" width="{w}" height="{h-hy:.0f}" fill="url(#wat)"/>{refl}{lines}'


def skyline(x0, x1, base, maxh, p, n=10, seed=1, wins=True, flip=False):
    r = random.Random(seed)
    bw = (x1 - x0) / n
    out = []
    for i in range(n):
        hh = maxh * (0.28 + 0.72 * (i + 1) / n) * (0.86 + 0.28 * r.random())
        x = x0 + i * bw
        col = p['b1'] if i % 2 else p['b2']
        y = base - hh if not flip else base
        out.append(f'<rect x="{x+3:.1f}" y="{y:.1f}" width="{bw-6:.1f}" height="{hh:.1f}" rx="5" fill="{col}"/>')
        if wins:
            rows, cols = int(hh // 36), max(1, int((bw - 6) // 24))
            for a in range(rows):
                for b in range(cols):
                    if r.random() < .34:
                        wy = (base - hh + 16 + a * 36) if not flip else (base + 16 + a * 36)
                        out.append(f'<rect x="{x+13+b*24:.1f}" y="{wy:.1f}" width="10" height="14" rx="2" fill="{p["win"]}" opacity="{.45+.55*r.random():.2f}"/>')
    return ''.join(out)


def sparkle(x, y, s, c=GOLD, o=1):
    return (f'<path transform="translate({x} {y}) scale({s})" opacity="{o}" fill="{c}" '
            f'd="M0-1C.1-.2.2-.1 1 0 .2.1.1.2 0 1-.1.2-.2.1-1 0-.2-.1-.1-.2 0-1Z"/>')


def heart(x, y, s, c=GOLD):
    return f'<path transform="translate({x} {y}) scale({s})" fill="{c}" d="M0 .9C-1.2-.1-.6-.9 0-.35.6-.9 1.2-.1 0 .9Z"/>'


def trend(pts, w=8, c=GOLD):
    d = 'M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in pts)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    L = 34
    ax = [(x2 - L * math.cos(a - .5), y2 - L * math.sin(a - .5)), (x2 - L * math.cos(a + .5), y2 - L * math.sin(a + .5))]
    dots = ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{w*.9:.0f}" fill="{c}"/>' for x, y in pts[:-1])
    return (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>{dots}'
            f'<path d="M{ax[0][0]:.0f},{ax[0][1]:.0f} L{x2:.0f},{y2:.0f} L{ax[1][0]:.0f},{ax[1][1]:.0f}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def browser(x, y, w, h, tilt=0, accent=GOLD, layout=0):
    bar = h * .09
    o = f'<g transform="translate({x} {y}) rotate({tilt} {w/2:.0f} {h/2:.0f})" filter="url(#sh)">'
    o += f'<rect width="{w}" height="{h}" rx="18" fill="#fff"/><path d="M0 {bar:.0f}V18a18 18 0 0 1 18-18h{w-36}a18 18 0 0 1 18 18v{bar-18:.0f}Z" fill="#e9f0ec"/>'
    for i, c in enumerate(['#f28b82', '#f6c65b', '#7ed39a']):
        o += f'<circle cx="{22+i*17}" cy="{bar/2:.0f}" r="5" fill="{c}"/>'
    o += f'<rect x="{w*.22:.0f}" y="{bar*.28:.0f}" width="{w*.5:.0f}" height="{bar*.44:.0f}" rx="{bar*.22:.0f}" fill="#fff"/>'
    hy = bar + h * .05
    if layout == 0:
        o += f'<rect x="{w*.05:.0f}" y="{hy:.0f}" width="{w*.9:.0f}" height="{h*.4:.0f}" rx="12" fill="url(#hg)"/>'
        o += f'<rect x="{w*.1:.0f}" y="{hy+h*.08:.0f}" width="{w*.38:.0f}" height="{h*.05:.0f}" rx="{h*.025:.0f}" fill="#fff"/>'
        o += f'<rect x="{w*.1:.0f}" y="{hy+h*.15:.0f}" width="{w*.3:.0f}" height="{h*.05:.0f}" rx="{h*.025:.0f}" fill="{accent}"/>'
        o += f'<rect x="{w*.1:.0f}" y="{hy+h*.24:.0f}" width="{w*.26:.0f}" height="{h*.06:.0f}" rx="{h*.03:.0f}" fill="{accent}"/>'
        o += f'<circle cx="{w*.72:.0f}" cy="{hy+h*.2:.0f}" r="{h*.13:.0f}" fill="url(#warm)"/>'
        cy = hy + h * .46
        for i in range(3):
            cx = w * .05 + i * w * .31
            o += f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{w*.28:.0f}" height="{h*.26:.0f}" rx="10" fill="#f1f6f3"/><rect x="{cx+12:.0f}" y="{cy+12:.0f}" width="{w*.09:.0f}" height="{w*.09:.0f}" rx="8" fill="{accent if i==1 else "#17654c"}"/><rect x="{cx+12:.0f}" y="{cy+h*.14:.0f}" width="{w*.2:.0f}" height="7" rx="3.5" fill="#c9d8d0"/><rect x="{cx+12:.0f}" y="{cy+h*.18:.0f}" width="{w*.14:.0f}" height="7" rx="3.5" fill="#dce7e1"/>'
    else:
        o += f'<rect x="{w*.05:.0f}" y="{hy:.0f}" width="{w*.42:.0f}" height="{h*.5:.0f}" rx="12" fill="url(#warm)"/>'
        for i, wd in enumerate([.4, .32, .36, .24]):
            o += f'<rect x="{w*.53:.0f}" y="{hy+i*h*.09:.0f}" width="{w*wd:.0f}" height="{h*.045:.0f}" rx="{h*.022:.0f}" fill="{"#0b3d2d" if i==0 else "#c9d8d0"}"/>'
        o += f'<rect x="{w*.53:.0f}" y="{hy+h*.4:.0f}" width="{w*.24:.0f}" height="{h*.08:.0f}" rx="{h*.04:.0f}" fill="{accent}"/>'
        for i in range(4):
            o += f'<rect x="{w*.05+i*w*.235:.0f}" y="{hy+h*.56:.0f}" width="{w*.21:.0f}" height="{h*.22:.0f}" rx="10" fill="{["#dfeae4","#f1e3c4","#cfe3d8","#e9dcc0"][i]}"/>'
    return o + '</g>'


def phone(x, y, w, h, tilt=0, warm=True):
    o = f'<g transform="translate({x} {y}) rotate({tilt} {w/2:.0f} {h/2:.0f})" filter="url(#sh)">'
    o += f'<rect width="{w}" height="{h}" rx="{w*.15:.0f}" fill="#0a1f18"/><rect x="{w*.04:.0f}" y="{w*.04:.0f}" width="{w*.92:.0f}" height="{h-w*.08:.0f}" rx="{w*.12:.0f}" fill="#fff"/>'
    o += f'<rect x="{w*.36:.0f}" y="{w*.07:.0f}" width="{w*.28:.0f}" height="{w*.05:.0f}" rx="{w*.025:.0f}" fill="#0a1f18"/>'
    o += f'<circle cx="{w*.2:.0f}" cy="{w*.26:.0f}" r="{w*.07:.0f}" fill="url(#hg)"/><rect x="{w*.32:.0f}" y="{w*.22:.0f}" width="{w*.36:.0f}" height="{w*.03:.0f}" rx="{w*.015:.0f}" fill="#c9d8d0"/><rect x="{w*.32:.0f}" y="{w*.28:.0f}" width="{w*.24:.0f}" height="{w*.025:.0f}" rx="{w*.012:.0f}" fill="#dce7e1"/>'
    o += f'<rect x="{w*.08:.0f}" y="{w*.4:.0f}" width="{w*.84:.0f}" height="{h*.42:.0f}" rx="{w*.06:.0f}" fill="url(#{"warm" if warm else "hg"})"/>'
    o += f'<circle cx="{w*.5:.0f}" cy="{w*.4+h*.2:.0f}" r="{w*.16:.0f}" fill="#fff" opacity=".35"/>'
    o += heart(w * .16, w * .4 + h * .42 + w * .1, w * .045) + f'<circle cx="{w*.3:.0f}" cy="{w*.4+h*.42+w*.1:.0f}" r="{w*.04:.0f}" fill="none" stroke="#0b3d2d" stroke-width="3"/>'
    o += f'<rect x="{w*.1:.0f}" y="{w*.4+h*.42+w*.2:.0f}" width="{w*.6:.0f}" height="{w*.03:.0f}" rx="{w*.015:.0f}" fill="#c9d8d0"/><rect x="{w*.1:.0f}" y="{w*.4+h*.42+w*.27:.0f}" width="{w*.4:.0f}" height="{w*.03:.0f}" rx="{w*.015:.0f}" fill="#dce7e1"/>'
    return o + '</g>'


def bubble(x, y, w, h, c='#fff', tail='l', dots=True):
    o = f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.0f}" fill="{c}"/>'
    tx = x + 22 if tail == 'l' else x + w - 22
    o += f'<path d="M{tx} {y+h-2} l{-8 if tail=="l" else 8} 16 l{22 if tail=="l" else -22} -14Z" fill="{c}"/></g>'
    if dots:
        for i in range(3):
            o += f'<circle cx="{x+w/2-16+i*16:.0f}" cy="{y+h/2:.0f}" r="4.5" fill="#0b3d2d" opacity="{.35+.3*i:.2f}"/>'
    return o


def calendar(x, y, w, h, filled=(2, 5, 9, 11, 16, 19, 23)):
    o = f'<g filter="url(#sh)" transform="translate({x} {y})"><rect width="{w}" height="{h}" rx="20" fill="#fff"/><path d="M0 {h*.16:.0f}V20a20 20 0 0 1 20-20h{w-40}a20 20 0 0 1 20 20v{h*.16-20:.0f}Z" fill="#0b3d2d"/>'
    o += f'<rect x="{w*.06:.0f}" y="{h*.055:.0f}" width="{w*.3:.0f}" height="{h*.04:.0f}" rx="{h*.02:.0f}" fill="#fff" opacity=".9"/>'
    cw, ch = w * .84 / 7, h * .74 / 4
    for r_ in range(4):
        for c_ in range(7):
            i = r_ * 7 + c_
            cx, cy = w * .08 + c_ * cw, h * .21 + r_ * ch
            col = ['#e9b54a', '#17654c', '#f0a86a'][i % 3] if i in filled else '#eef3f0'
            o += f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{cw-8:.0f}" height="{ch-8:.0f}" rx="9" fill="{col}"/>'
    return o + '</g>'


def target(cx, cy, r):
    o = '<g filter="url(#sh)">'
    for i, c in enumerate(['#0b3d2d', '#ffffff', '#e9b54a', '#ffffff', '#0b3d2d']):
        o += f'<circle cx="{cx}" cy="{cy}" r="{r*(1-i*.19):.0f}" fill="{c}"/>'
    o += (f'<path d="M{cx} {cy} L{cx+r*.9:.0f} {cy-r*.9:.0f}" stroke="#0a1f18" stroke-width="9" stroke-linecap="round"/>'
          f'<path d="M{cx+r*.9:.0f} {cy-r*.9:.0f} l-38 4 M{cx+r*.9:.0f} {cy-r*.9:.0f} l-4 38" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/></g>')
    return o


def chartcard(x, y, w, h):
    o = f'<g filter="url(#sh)" transform="translate({x} {y})"><rect width="{w}" height="{h}" rx="18" fill="#fff"/>'
    n = 7
    bw = w * .72 / n
    pts = []
    for i in range(n):
        bh = h * (.18 + .5 * (i + 1) / n * (.85 + .3 * ((i * 37) % 10) / 10))
        bx = w * .1 + i * (w * .8 / n)
        o += f'<rect x="{bx:.0f}" y="{h*.88-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="7" fill="{"#17654c" if i%2 else "#0b3d2d"}"/>'
        pts.append((bx + bw / 2, h * .88 - bh - 14))
    o += '<path d="M' + ' L'.join(f'{a:.0f},{b:.0f}' for a, b in pts) + f'" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    o += ''.join(f'<circle cx="{a:.0f}" cy="{b:.0f}" r="6" fill="{GOLD}"/>' for a, b in pts)
    return o + '</g>'


def play(cx, cy, r):
    return (f'<g filter="url(#sh)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD}"/>'
            f'<path d="M{cx-r*.28:.0f} {cy-r*.4:.0f} L{cx+r*.46:.0f} {cy} L{cx-r*.28:.0f} {cy+r*.4:.0f}Z" fill="#0b3d2d"/></g>')


def swatches(x, y, s):
    cols = ['#0b3d2d', '#17654c', '#e9b54a', '#f0a86a', '#f6ead0']
    return '<g filter="url(#sh)">' + ''.join(f'<rect x="{x+i*(s+10)}" y="{y-(i%2)*14}" width="{s}" height="{s*1.5:.0f}" rx="14" fill="{c}"/>' for i, c in enumerate(cols)) + '</g>'


def write(path, content):
    full = os.path.join(IMG, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)


# ---------- scenes ----------
def scene_hero(pal='dusk', variant=0, w=1200, h=900):
    p = PAL[pal]
    hy = h * .74
    b = sky(w, h, p, .74, .66 if variant == 0 else .5)
    b += skyline(w * .34, w * 1.0, hy, h * .56, p, 10, 3 + variant)
    b += water(w, h, p, .74, f'<g opacity=".28">{skyline(w*.34, w*1.0, hy, h*.34, p, 10, 3+variant, wins=False, flip=True)}</g><rect y="{hy:.0f}" width="{w}" height="{h*.26:.0f}" fill="url(#wat)" opacity=".55"/>')
    b += trend([(w * .36, h * .58), (w * .5, h * .5), (w * .62, h * .53), (w * .76, h * .34), (w * .92, h * .16)], 9)
    if variant == 0:
        b += browser(w * .09, h * .3, w * .5, h * .42, -3)
        b += phone(w * .66, h * .34, w * .19, h * .44, 4)
        b += chartcard(w * .5, h * .66, w * .25, h * .2)
    else:
        b += phone(w * .16, h * .28, w * .2, h * .46, -4)
        b += browser(w * .42, h * .38, w * .46, h * .38, 2, layout=1)
        b += bubble(w * .1, h * .2, 150, 66, tail='r')
    b += sparkle(w * .56, h * .22, 26) + sparkle(w * .9, h * .42, 16, '#fff', .8) + sparkle(w * .3, h * .16, 12, '#fff', .7)
    return svg(w, h, b, p)


def scene_service(kind, pal, w=800, h=600):
    p = PAL[pal]
    b = sky(w, h, p, .78, .7, .45) + skyline(w * .5, w, h * .78, h * .42, p, 7, 7, False) + water(w, h, p, .78)
    if kind == 'web':
        b += browser(w * .1, h * .16, w * .62, h * .56, -3)
        b += phone(w * .68, h * .34, w * .16, h * .42, 5)
        b += sparkle(w * .8, h * .18, 20)
    elif kind == 'social':
        b += phone(w * .3, h * .1, w * .26, h * .72, -3)
        b += bubble(w * .08, h * .22, 130, 56, tail='l') + bubble(w * .6, h * .5, 150, 60, '#e9b54a', 'r', False)
        b += heart(w * .68, h * .26, 34) + heart(w * .2, h * .58, 22, '#fff') + sparkle(w * .78, h * .12, 18)
    elif kind == 'management':
        b += calendar(w * .12, h * .12, w * .56, h * .62)
        b += bubble(w * .62, h * .5, 170, 64, tail='r') + phone(w * .72, h * .14, w * .15, h * .38, 4)
        b += sparkle(w * .1, h * .1, 16, '#fff', .8)
    elif kind == 'advertising':
        b += target(w * .34, h * .47, h * .3) + chartcard(w * .54, h * .3, w * .34, h * .4)
        b += sparkle(w * .5, h * .14, 20) + sparkle(w * .9, h * .22, 13, '#fff', .8)
    elif kind == 'content':
        b += phone(w * .1, h * .14, w * .2, h * .58, -5) + phone(w * .33, h * .1, w * .2, h * .58, 0, False)
        b += play(w * .68, h * .36, h * .12) + swatches(w * .58, h * .56, 52)
        b += sparkle(w * .86, h * .16, 22)
    return svg(w, h, b, p)


def scene_project(kind, pal, w=800, h=600):
    p = PAL[pal]
    b = sky(w, h, p, .8, .3 if kind == 'social' else .75, .5) + water(w, h, p, .8)
    if kind == 'web':
        b += browser(w * .12, h * .14, w * .58, h * .56, -2, layout=1) + phone(w * .66, h * .3, w * .17, h * .44, 5) + sparkle(w * .86, h * .16, 18)
    elif kind == 'social':
        b += phone(w * .08, h * .18, w * .2, h * .56, -5) + phone(w * .3, h * .1, w * .22, h * .62, 0, False) + phone(w * .54, h * .18, w * .2, h * .56, 5)
        b += heart(w * .84, h * .3, 30) + bubble(w * .74, h * .5, 130, 56, tail='r') + sparkle(w * .2, h * .1, 14, '#fff')
    else:
        b += target(w * .3, h * .5, h * .28) + chartcard(w * .5, h * .22, w * .38, h * .46) + trend([(w * .52, h * .78), (w * .66, h * .7), (w * .8, h * .56)], 7) + sparkle(w * .9, h * .12, 18)
    return svg(w, h, b, p)


def scene_wide(w=1400, h=700, pal='dusk'):
    p = PAL[pal]
    hy = h * .7
    b = sky(w, h, p, .7, .72, .6) + skyline(w * .45, w, hy, h * .58, p, 12, 11)
    b += water(w, h, p, .7, f'<g opacity=".25">{skyline(w*.45, w, hy, h*.3, p, 12, 11, False, True)}</g>')
    b += trend([(w * .5, h * .56), (w * .66, h * .44), (w * .8, h * .48), (w * .93, h * .16)], 9) + sparkle(w * .58, h * .16, 24) + sparkle(w * .86, h * .5, 14, '#fff', .8)
    return svg(w, h, b, p)


def scene_portrait(w=800, h=900, pal='peach'):
    p = PAL[pal]
    hy = h * .76
    b = sky(w, h, p, .76, .55, .4) + skyline(w * .05, w * .95, hy, h * .56, p, 8, 21) + water(w, h, p, .76)
    b += browser(w * .1, h * .3, w * .56, h * .3, -3) + phone(w * .62, h * .4, w * .2, h * .32, 4) + trend([(w * .12, h * .24), (w * .4, h * .18), (w * .7, h * .1)], 8) + sparkle(w * .8, h * .16, 20)
    return svg(w, h, b, p)


def scene_blog(kind, pal, w=800, h=520):
    p = PAL[pal]
    b = sky(w, h, p, .8, .75, .5) + water(w, h, p, .8)
    if kind == 'checklist':
        b += browser(w * .18, h * .14, w * .56, h * .58, -2) + sparkle(w * .82, h * .2, 22)
        for i in range(3):
            b += f'<g filter="url(#sh)"><circle cx="{w*.82:.0f}" cy="{h*(.36+i*.14):.0f}" r="20" fill="{GOLD}"/><path d="M{w*.82-8:.0f} {h*(.36+i*.14):.0f} l6 7 l11 -13" fill="none" stroke="#0b3d2d" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>'
    elif kind == 'calendar':
        b += calendar(w * .1, h * .14, w * .5, h * .62) + phone(w * .64, h * .12, w * .17, h * .6, 4) + heart(w * .58, h * .18, 24) + sparkle(w * .9, h * .2, 16, '#fff', .8)
    else:
        b += target(w * .3, h * .5, h * .26) + chartcard(w * .52, h * .2, w * .36, h * .5) + sparkle(w * .5, h * .12, 18)
    return svg(w, h, b, p)


def logo_mark(size=48):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="{size}" height="{size}" role="img" aria-label="NOVIQ">'
            f'<path d="M11 38V11l26 27V11" fill="none" stroke="{GOLD}" stroke-width="5.2" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="37" cy="7" r="3.2" fill="{GOLD}"/></svg>')


def main():
    write('hero/hero-main.svg', scene_hero('dusk', 0))
    write('hero/hero-alt.svg', scene_hero('peach', 1))
    for kind, slug, pal in [('web', 'web-development', 'emerald'), ('social', 'social-media', 'dusk'), ('management', 'management', 'sand'),
                            ('advertising', 'advertising', 'night'), ('content', 'content', 'peach')]:
        write(f'services/{slug}.svg', scene_service(kind, pal))
    for i, (kind, pal) in enumerate([('web', 'sand'), ('social', 'dusk'), ('ads', 'emerald')], 1):
        write(f'portfolio/project-0{i}.svg', scene_project(kind, pal))
    for i, (kind, pal) in enumerate([('checklist', 'emerald'), ('calendar', 'dusk'), ('ads', 'night')], 1):
        write(f'blog/article-0{i}.svg', scene_blog(kind, pal))
    write('general/why.svg', scene_hero('emerald', 1, 1000, 800))
    write('general/cta.svg', scene_wide(1400, 700, 'dusk'))
    write('general/about.svg', scene_portrait(800, 900, 'peach'))
    write('testimonials/testimonial.svg', scene_portrait(800, 900, 'dusk'))
    print('artwork written')


if __name__ == '__main__':
    main()
