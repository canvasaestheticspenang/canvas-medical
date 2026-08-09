# Site maintenance tools

This is a static site kept DRY by generation: shared knowledge lives in
exactly one place, and these tools propagate it everywhere it appears.

## Sources of truth

| File | Owns |
|---|---|
| `data/site.json` | Clinic constants — phones, WhatsApp, address, geo, hours, GA id, socials, tagline, copyright year |
| `data/physicians.json` | Physician roster and display order |
| `templates/chrome.html` | Shared page chrome — nav, mobile menu, contact section, footer, WhatsApp button, analytics snippet |

## Workflow

Edit the source file, then run:

```
python3 scripts/update-all.py
```

and commit. `update-all.py` runs the three tools in order:

1. **update-site.py** — stamps clinic constants into every page's visible
   copy and every JSON-LD block; validates that no page carries a rogue
   phone number, analytics tag or hour format. Exits non-zero on drift.
2. **update-physicians.py** — regenerates the homepage team grid,
   physician-count stat, Physician schema graph, booking-form dropdown,
   doctors hub cards/ItemList, and the physician row on every page.
   Generated regions sit between `<!-- physicians:*:start/end -->` markers.
3. **update-chrome.py** — renders the shared chrome blocks onto all pages
   with depth-aware paths (the homepage keeps same-page anchors; 404.html
   keeps absolute paths).

All tools are idempotent — a second run changes nothing — and safe to run
any time as a consistency check.

## Gallery photos

`watermark-gallery.py` prepares a shoot photo for the homepage carousel:
crops it to the card's 4:3, resizes, and stamps the CANVAS V-mark.

```
python3 scripts/watermark-gallery.py gallery-16 ~/shoot/DSC_1234.jpg
python3 scripts/watermark-gallery.py gallery-16 ~/shoot/DSC_1234.jpg 0.14
```

The optional third argument shifts the crop vertically as a fraction of
the source height (negative up, positive down). Shoot files are usually
2:3 portrait against a 4:3 card, so a centred crop keeps only the middle
band — check the framing, and pass an offset when it cuts a face.

The watermark is baked into the pixels, not applied in CSS, so always
pass the original photo; the script refuses a file already in
`assets/gallery/` rather than stamping a second mark over the first.
Settings live at the top of the script and match the existing photos:
V-mark at 40% of image width, 2.5% margin, 55% opacity, bottom-right.

Writing the file is only step one — the photo also needs a `.g-item`
card in the gallery track in `index.html` and an entry in `slots.js`,
both keyed by the same slot id, or it will not appear on the page.

Unlike the generators above, this one needs Pillow (`pip install
pillow`).

## Rules of thumb

- Never hand-edit a generated region in a page; edit the source and rerun.
- Adding a physician: add to `data/physicians.json`, create their profile
  page under `doctors/<slug>/`, add it to `sitemap.xml`, run the tools
  (they warn if the profile page is missing).
- Page-specific content (treatment copy, FAQs, per-page schema) is
  authored in the page itself — only shared knowledge is generated.
