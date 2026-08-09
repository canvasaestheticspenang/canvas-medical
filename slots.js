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
  /* gallery uses data-slot attributes, not position — the carousel
     shuffles card order on every load, so nth-child isn't stable */
  { id: 'gallery-1',     label: 'Gallery — photo 1',             selector: '.g-item[data-slot="gallery-1"] .ph' },
  { id: 'gallery-2',     label: 'Gallery — photo 2',             selector: '.g-item[data-slot="gallery-2"] .ph' },
  { id: 'gallery-3',     label: 'Gallery — photo 3',             selector: '.g-item[data-slot="gallery-3"] .ph' },
  { id: 'gallery-4',     label: 'Gallery — photo 4',             selector: '.g-item[data-slot="gallery-4"] .ph' },
  { id: 'gallery-5',     label: 'Gallery — photo 5',             selector: '.g-item[data-slot="gallery-5"] .ph' },
  { id: 'gallery-6',     label: 'Gallery — photo 6',             selector: '.g-item[data-slot="gallery-6"] .ph' },
  { id: 'gallery-7',     label: 'Gallery — photo 7',             selector: '.g-item[data-slot="gallery-7"] .ph' },
  { id: 'gallery-8',     label: 'Gallery — photo 8',             selector: '.g-item[data-slot="gallery-8"] .ph' },
  { id: 'gallery-9',     label: 'Gallery — photo 9',             selector: '.g-item[data-slot="gallery-9"] .ph' },
  { id: 'gallery-10',    label: 'Gallery — photo 10',            selector: '.g-item[data-slot="gallery-10"] .ph' },
  { id: 'gallery-11',    label: 'Gallery — photo 11',            selector: '.g-item[data-slot="gallery-11"] .ph' },
  { id: 'gallery-12',    label: 'Gallery — photo 12',            selector: '.g-item[data-slot="gallery-12"] .ph' },
  { id: 'gallery-13',    label: 'Gallery — photo 13',            selector: '.g-item[data-slot="gallery-13"] .ph' },
  { id: 'gallery-14',    label: 'Gallery — photo 14',            selector: '.g-item[data-slot="gallery-14"] .ph' },
  { id: 'gallery-15',    label: 'Gallery — photo 15',            selector: '.g-item[data-slot="gallery-15"] .ph' }
];
