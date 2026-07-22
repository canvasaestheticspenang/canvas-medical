/* ============================================================
   CANVAS — interactions
   ============================================================ */
(function () {
  'use strict';

  /* mark document so CSS reveal animations activate */
  document.documentElement.classList.add('js-loaded');

  /* ---------- custom cursor (fine pointers only, hero section only) ---------- */
  var finePointer = window.matchMedia('(pointer:fine)').matches;
  if (finePointer) {
    var cur = document.getElementById('cur'),
        cr  = document.getElementById('cur-r'),
        hero = document.getElementById('hero');
    var mx = 0, my = 0, rx = 0, ry = 0, started = false, cursorActive = false;

    function enableCursor() {
      if (cursorActive) return;
      cursorActive = true;
      if (cur) cur.style.display = 'block';
      if (cr) cr.style.display = 'block';
    }
    function disableCursor() {
      cursorActive = false;
      if (cur) cur.style.display = 'none';
      if (cr) cr.style.display = 'none';
    }
    disableCursor();

    if (hero) {
      hero.addEventListener('mouseenter', enableCursor);
      hero.addEventListener('mouseleave', disableCursor);
    }

    document.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      if (cur) { cur.style.left = mx + 'px'; cur.style.top = my + 'px'; }
      if (!started && cursorActive) { started = true; loop(); }
    });
    function loop() {
      if (!cursorActive) { started = false; return; }
      rx += (mx - rx) * 0.12; ry += (my - ry) * 0.12;
      if (cr) { cr.style.left = rx + 'px'; cr.style.top = ry + 'px'; }
      requestAnimationFrame(loop);
    }
    document.addEventListener('mouseover', function (e) {
      if (!cursorActive) return;
      if (e.target.closest('a,button,.dot,.faq-q,input,select,image-slot')) {
        if (cr) { cr.style.width = '48px'; cr.style.height = '48px'; }
      }
    });
    document.addEventListener('mouseout', function (e) {
      if (!cursorActive) return;
      if (e.target.closest('a,button,.dot,.faq-q,input,select,image-slot')) {
        if (cr) { cr.style.width = '30px'; cr.style.height = '30px'; }
      }
    });
  }

  /* ---------- nav scroll state ---------- */
  var nav = document.getElementById('nav');
  function onScroll() {
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 50);
    var fab = document.getElementById('fab');
    if (fab) fab.classList.toggle('show', window.scrollY > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  var toggle = document.getElementById('navToggle');
  var menu = document.getElementById('mobileMenu');
  function setMenu(open) {
    if (!menu) return;
    menu.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  if (toggle) toggle.addEventListener('click', function () {
    setMenu(!menu.classList.contains('open'));
  });
  if (menu) menu.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () { setMenu(false); });
  });
  var navClose = document.getElementById('navClose');
  if (navClose) navClose.addEventListener('click', function () { setMenu(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu && menu.classList.contains('open')) setMenu(false);
  });

  /* ---------- reveal on scroll ---------- */
  /* each stagger child lags the previous by 70ms — CSS reads --si */
  document.querySelectorAll('.reveal-stagger').forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.style.setProperty('--si', i);
    });
  });
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('on'); obs.unobserve(e.target); }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal, .reveal-stagger').forEach(function (el) { obs.observe(el); });

  /* ---------- theme toggle ---------- */
  var root = document.documentElement;
  try {
    var savedTheme = localStorage.getItem('canvas-theme');
    if (savedTheme) root.setAttribute('data-theme', savedTheme);
  } catch (err) {}
  var themeBtn = document.getElementById('themeToggle');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('canvas-theme', next); } catch (err) {}
  });

  /* ---------- testimonials ---------- */
  var ct = 0;
  var ti = document.querySelectorAll('.testi-item');
  var td = document.querySelectorAll('.dot');
  var testiTimer;

  function setStageHeight() {
    var stage = document.querySelector('.testi-stage');
    if (!stage || !ti.length) return;
    var maxH = 0;
    ti.forEach(function(item) {
      item.style.position = 'relative';
      item.style.opacity = '1';
      item.style.visibility = 'visible';
      var h = item.offsetHeight;
      if (h > maxH) maxH = h;
      item.style.position = '';
      item.style.opacity = '';
      item.style.visibility = '';
    });
    stage.style.height = maxH + 'px';
  }

  function goT(i) {
    if (!ti.length) return;
    var prev = ct;
    ct = ((i % ti.length) + ti.length) % ti.length;
    if (prev === ct) return;
    ti[prev].classList.remove('active');
    ti[prev].classList.add('leaving');
    td[prev].classList.remove('active');
    setTimeout(function() { ti[prev].classList.remove('leaving'); }, 700);
    ti[ct].classList.add('active');
    td[ct].classList.add('active');
  }

  function nextT() { goT(ct + 1); }
  function prevT() { goT(ct - 1); }

  function resetTimer() {
    clearInterval(testiTimer);
    testiTimer = setInterval(nextT, 6000);
  }

  td.forEach(function(d, i) {
    d.addEventListener('click', function() { goT(i); resetTimer(); });
  });

  var btnNext = document.getElementById('testiNext');
  var btnPrev = document.getElementById('testiPrev');
  if (btnNext) btnNext.addEventListener('click', function() { nextT(); resetTimer(); });
  if (btnPrev) btnPrev.addEventListener('click', function() { prevT(); resetTimer(); });

  if (ti.length) {
    setStageHeight();
    window.addEventListener('resize', setStageHeight);
    resetTimer();
  }

  /* ---------- FAQ ---------- */
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = q.parentElement;
      var open = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(function (f) {
        f.classList.remove('open');
        var b = f.querySelector('.faq-q'); if (b) b.setAttribute('aria-expanded', 'false');
      });
      if (!open) { item.classList.add('open'); q.setAttribute('aria-expanded', 'true'); }
    });
  });

  /* ---------- treatment cards: click / tap opens the description ---------- */
  document.querySelectorAll('.svc-card').forEach(function (card) {
    var btn = card.querySelector('.svc-toggle');
    card.addEventListener('click', function (e) {
      if (e.target.closest('a')) return; /* Reserve & Details navigate as normal */
      var open = card.classList.toggle('open');
      if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* ---------- smooth anchor scroll ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id.length < 2) return;
      var t = document.querySelector(id);
      if (t) { e.preventDefault(); window.scrollTo({ top: t.getBoundingClientRect().top + window.scrollY - 70, behavior: 'smooth' }); }
    });
  });

  /* ---------- booking form → WhatsApp ---------- */
  // Two booking lines
  var LINES = {
    medical: '601128547882',   // medical aesthetics physician booking
    aesthetics: '60189815639'  // aesthetics booking
  };
  // treatments routed to the physician (medical) line
  var MEDICAL_TREATMENTS = ['Radiofrequency', 'Laser', 'Ultrasound (Ultherapy / Ultraformer)', 'Regenerative & Wellness', 'Stem Cell Therapy', 'Sexual Health & Enhancements', 'Body Aesthetics & Functional Medicine', 'Dermatology Consultation'];

  var form = document.getElementById('bookForm');
  function field(name) { return form ? form.querySelector('[name="' + name + '"]') : null; }
  function markInvalid(el, bad) {
    if (!el) return; var wrap = el.closest('.f-field');
    if (wrap) wrap.classList.toggle('invalid', bad);
  }
  function pad2(n) { return n < 10 ? '0' + n : '' + n; }
  function localISO(d) { return d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate()); }

  if (form) {
    // limit the date picker to today … +90 days
    var dateEl = field('prefDate');
    if (dateEl) {
      var now = new Date();
      dateEl.min = localISO(now);
      var horizon = new Date(now); horizon.setDate(horizon.getDate() + 90);
      dateEl.max = localISO(horizon);
    }
    form.querySelectorAll('input,select').forEach(function (el) {
      el.addEventListener('input', function () { markInvalid(el, false); });
      el.addEventListener('change', function () { markInvalid(el, false); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fn = field('firstName'), ln = field('lastName'),
          ph = field('phone'), em = field('email'),
          doc = field('physician'), tr = field('treatment'),
          dt = field('prefDate'), tm = field('prefTime');
      var firstBad = null;
      function bad(el) { markInvalid(el, true); if (!firstBad) firstBad = el; }
      if (!fn.value.trim()) bad(fn);
      if (!ph.value.trim() || ph.value.replace(/\D/g, '').length < 7) bad(ph);
      if (em.value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value.trim())) bad(em);
      if (!tr.value) bad(tr);
      if (!dt.value || dt.value < dt.min) bad(dt);
      if (firstBad) {
        firstBad.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstBad.focus({ preventScroll: true });
        return;
      }

      var treatment = tr.value;
      var line = MEDICAL_TREATMENTS.indexOf(treatment) !== -1 ? LINES.medical : LINES.aesthetics;

      var niceDate = new Date(dt.value + 'T00:00:00').toLocaleDateString('en-GB',
        { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });

      var msg = '';
      msg += 'Hello CANVAS, I’d like to book a consultation.\n\n';
      msg += '*Name:* ' + (fn.value.trim() + ' ' + ln.value.trim()).trim() + '\n';
      msg += '*Phone:* ' + ph.value.trim() + '\n';
      if (em.value.trim()) msg += '*Email:* ' + em.value.trim() + '\n';
      msg += '*Treatment:* ' + treatment + '\n';
      if (doc.value && doc.value.indexOf('No preference') === -1) msg += '*Preferred physician:* ' + doc.value + '\n';
      msg += '*Preferred date:* ' + niceDate + '\n';
      msg += '*Preferred time:* ' + (tm.value || 'Flexible (10am–10pm)') + '\n';
      msg += '\nSent from the CANVAS website.';

      var url = 'https://wa.me/' + line + '?text=' + encodeURIComponent(msg);

      // keep the retry link ready in case the popup is blocked
      var retry = document.getElementById('waRetry');
      if (retry) retry.href = url;

      // loading state on the submit button while the WhatsApp handoff opens
      var submitBtn = form.querySelector('.btn-submit');
      if (submitBtn) { submitBtn.classList.add('is-loading'); submitBtn.disabled = true; }

      // open within the click gesture so the popup is not blocked
      window.open(url, '_blank');

      var success = document.getElementById('formSuccess');
      var wrap = document.getElementById('formWrap');
      function reveal() {
        if (submitBtn) { submitBtn.classList.remove('is-loading'); submitBtn.disabled = false; }
        if (success && wrap) { wrap.style.display = 'none'; success.classList.add('show'); }
      }
      // brief, motivated feedback; skip the delay when motion is reduced
      if (window.matchMedia('(prefers-reduced-motion:reduce)').matches) reveal();
      else setTimeout(reveal, 650);
    });
  }

  /* ---------- decorative hero visual on treatment/article pages ---------- */
  /* fills the empty right side of the .tp-hero with a champagne "energy
     field". Skipped when a real product image (.tp-hero-media) is present,
     so per-page imagery can override the motif without markup churn. */
  (function () {
    var th = document.querySelector('.tp-hero');
    if (!th || th.querySelector('.tp-hero-media') || th.querySelector('.tp-hero-orb')) return;
    var orb = document.createElement('div');
    orb.className = 'tp-hero-orb';
    orb.setAttribute('aria-hidden', 'true');
    orb.innerHTML =
      '<span class="orb-halo"></span><span class="orb-ring r1"></span>' +
      '<span class="orb-ring r2"></span><span class="orb-ring r3"></span>' +
      '<span class="orb-core"></span>';
    th.appendChild(orb);
  })();

  /* ---------- hero visual drifts away and fades on scroll ---------- */
  /* the device image / orb eases down-right and fades as you scroll past the
     hero, then returns cleanly at the top. Skipped for reduced-motion. */
  (function () {
    var vis = document.querySelector('.tp-hero-media, .tp-hero-orb');
    var hero = document.querySelector('.tp-hero');
    if (!vis || !hero) return;
    if (window.matchMedia('(prefers-reduced-motion:reduce)').matches) return;
    var ticking = false;
    function apply() {
      ticking = false;
      var y = window.pageYOffset || 0;
      // at the top, hand control back to the CSS entrance animation
      if (y < 4) { vis.style.removeProperty('opacity'); vis.style.removeProperty('transform'); return; }
      var p = Math.min(y / (hero.offsetHeight * 0.85 || 500), 1);
      // !important so the scroll state beats the entrance animation's forwards fill
      vis.style.setProperty('opacity', String(1 - p), 'important');
      // the orb is vertically centred (keep -50%); the media is bottom-anchored
      var ty = vis.classList.contains('tp-hero-orb')
        ? 'calc(-50% + ' + (p * 40).toFixed(1) + 'px)'
        : (p * 60).toFixed(1) + 'px';
      vis.style.setProperty('transform',
        'translateY(' + ty + ') ' +
        'translateX(' + (p * 34).toFixed(1) + 'px) scale(' + (1 - p * 0.05).toFixed(3) + ')',
        'important');
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(apply); }
    }, { passive: true });
  })();
})();
