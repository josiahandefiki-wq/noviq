# NOVIQ: Ideas to Impact

A multi-page marketing-agency website built with **HTML5, CSS3 and vanilla JavaScript** (no frameworks).
The UI/UX follows the supplied reference: dark forest-green rounded hero panel with an S-curve image edge,
gold accent, pill navigation and buttons, white rounded cards, dark feature panels, circular badges and a dark footer.

## Open it
Open `index.html` in a browser, or upload the folder to any static host (Netlify, Cloudflare Pages, GitHub Pages, cPanel).
No build step is needed for hosting.

## Pages (17)
Home · Services · Our Work · About · Insights · Contact · 5 service pages · 3 project pages · 3 article pages.
Plus `sitemap.xml` and `robots.txt`.

## Before you launch: replace placeholders
1. **Contact details and domain**: edit `data/site.json` (`url`, `email`, `phone`, `whatsapp`, `location`, `social`).
   Empty values show clearly labelled "to be added" placeholders. `url` is currently `https://www.noviq.example`, so change it to your real domain.
2. **Form delivery**: the contact and newsletter forms validate in the browser but send nothing until connected.
   Set `form_endpoint` / `newsletter_endpoint` (for example a Formspree URL) in `data/site.json`. If only `email` is set, the contact form opens the visitor's email app.
3. **Rebuild** after editing data: `python3 tools/build.py` (regenerates every HTML page, sitemap and robots).
   Or edit the HTML files directly.
4. **Imagery**: all pictures are original illustrated SVG placeholders in `assets/images/`. Replace them with real photography or project
   screenshots (keep filenames or update the `<img src>`). Regenerate the social preview image with `python3 tools/render_og.py`.
5. **Testimonials, team and projects** are clearly marked sample or placeholder content. Replace them via `data/*.json` when real material exists.
6. **Fonts**: Poppins and Dancing Script load from Google Fonts with system fallbacks. To self-host, place font files in `assets/fonts/` and add `@font-face` rules.

## Structure
```
index.html   pages/   projects/   blog/
css/  style.css · components.css · responsive.css · pages/*.css
js/   main.js · navigation.js · animations.js · forms.js · pages/{filters,testimonials,contact}.js
data/ site.json · services.json · projects.json · testimonials.json · articles.json
tools/ build.py · svgart.py · render_og.py   (optional build helpers)
```

## Notes
- Accessibility: skip link, semantic landmarks, visible focus, labelled forms, `aria-current`, `prefers-reduced-motion` respected.
- SEO: unique title/description, canonical, Open Graph, Twitter cards, JSON-LD (organisation, breadcrumbs, service, blog post, contact) on every page.
- No fake clients, statistics, awards, addresses, phone numbers or social accounts are used anywhere.
