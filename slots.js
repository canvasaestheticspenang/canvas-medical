/* ============================================================
   CANVAS — shared photo-slot map
   Used by photos.js (live site fill) AND admin.html (uploader).
   Each slot: id (key in photos.json), label (shown in uploader),
   selector (the .ph placeholder element on the live page).
   ============================================================ */
window.CANVAS_SLOTS = [
  { id: 'hero-bg',       label: 'Hero background (clinic photo)', selector: '.hero-photo .ph' },
  { id: 'hero-portrait', label: 'Hero side portrait',            selector: '.hero-split-img .ph' },
  { id: 'team-1',        label: 'Dr. Samuel Tong',               selector: '.team-grid > div:nth-child(1) .ph' },
  { id: 'team-2',        label: 'Dr. Tan Chin Loon',             selector: '.team-grid > div:nth-child(2) .ph' },
  { id: 'team-3',        label: 'Dr. Chong Jee Can',             selector: '.team-grid > div:nth-child(3) .ph' },
  { id: 'team-4',        label: 'Dr. Kang Eik Hong',             selector: '.team-grid > div:nth-child(4) .ph' },
  { id: 'gallery-1',     label: 'Gallery — The Clinic',          selector: '.gallery-grid .g-item:nth-child(1) .ph' },
  { id: 'gallery-2',     label: 'Gallery — Injectables',         selector: '.gallery-grid .g-item:nth-child(2) .ph' },
  { id: 'gallery-3',     label: 'Gallery — Radiofrequency',      selector: '.gallery-grid .g-item:nth-child(3) .ph' },
  { id: 'gallery-4',     label: 'Gallery — Laser',               selector: '.gallery-grid .g-item:nth-child(4) .ph' },
  { id: 'gallery-5',     label: 'Gallery — Ultrasound',          selector: '.gallery-grid .g-item:nth-child(5) .ph' }
];
