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

## Rules of thumb

- Never hand-edit a generated region in a page; edit the source and rerun.
- Adding a physician: add to `data/physicians.json`, create their profile
  page under `doctors/<slug>/`, add it to `sitemap.xml`, run the tools
  (they warn if the profile page is missing).
- Page-specific content (treatment copy, FAQs, per-page schema) is
  authored in the page itself — only shared knowledge is generated.
