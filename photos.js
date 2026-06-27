/* ============================================================
   CANVAS — fill photo slots from photos.json
   For every slot that has an uploaded image, replace its
   placeholder (.ph) with a real <img>. Slots with no entry
   keep their branded placeholder.
   ============================================================ */
(function () {
  'use strict';
  function fill(map) {
    var slots = window.CANVAS_SLOTS || [];
    slots.forEach(function (slot) {
      var src = map[slot.id];
      if (!src) return;
      var ph = document.querySelector(slot.selector);
      if (!ph) return;
      var img = document.createElement('img');
      img.className = 'slot-img';
      img.src = src;
      img.alt = slot.label;
      img.loading = 'lazy';
      img.decoding = 'async';
      ph.replaceWith(img);
    });
  }
  // cache-bust so a freshly published photo shows up promptly
  fetch('photos.json?t=' + Date.now(), { cache: 'no-store' })
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (map) { if (map && typeof map === 'object') fill(map); })
    .catch(function () { /* no photos.json yet — placeholders stay */ });
})();
