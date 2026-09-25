#!/usr/bin/env python3
"""Renders assets/images/general/og-image.jpg (1200x630) for social sharing. Needs: pip install playwright && playwright install chromium"""
import os
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = f'''<body style="margin:0;width:1200px;height:630px;background:linear-gradient(120deg,#031f17,#0a4232);font-family:Poppins,Arial,sans-serif;color:#fff;overflow:hidden;position:relative">
<img src="file://{ROOT}/assets/images/hero/hero-main.svg" style="position:absolute;right:0;top:0;width:760px;height:630px;object-fit:cover;-webkit-mask-image:linear-gradient(90deg,transparent,#000 35%)">
<img src="file://{ROOT}/assets/images/logo/logo-light.png" style="position:absolute;left:62px;top:56px;height:120px">
<div style="position:absolute;left:70px;top:230px;font-size:66px;font-weight:700;line-height:1.1;width:560px">We Turn <span style="color:#e9b54a">Ideas Into</span> Impact.</div>
<div style="position:absolute;left:70px;top:480px;font-size:22px;color:#cfe3d8;width:520px">Websites, social media, advertising and content for small businesses.</div></body>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1200,'height':630}); pg.set_content(html); pg.wait_for_timeout(400)
    pg.screenshot(path=os.path.join(ROOT, 'assets/images/general/og-image.jpg'), type='jpeg', quality=84); b.close()
print('og-image.jpg written')
