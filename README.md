# CANVAS Medical Clinic — Website

Static marketing site for **CANVAS Medical Clinic**, Gurney Walk, Georgetown, Penang.
Served via GitHub Pages at **https://canvas-medical.com**.

## Structure
- `index.html` — the full single-page site
- `styles.css` — styling (dark/light theming via `[data-theme]`)
- `app.js` — interactions (nav, FAQ, testimonials, WhatsApp booking)
- `assets/` — logo, mark, and treatment images (optimized)
- `CNAME` — custom domain for GitHub Pages
- `robots.txt`, `sitemap.xml`, `.nojekyll`

## Notes
- The booking form has no backend — it opens a pre-filled WhatsApp chat (`wa.me`).
- Photo areas for the hero, the 4 physician portraits, the location, and the gallery
  currently show branded placeholders. Replace each `<div class="ph">…</div>` with an
  `<img src="assets/your-photo.jpg" alt="…">` to add real photos.

## Deploy
Pushing to `main` auto-publishes via GitHub Pages (source: `main` / root).
