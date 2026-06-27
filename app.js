/* ============================================================
   CANVAS — interactions
   ============================================================ */
(function () {
  'use strict';

  /* ---------- custom cursor (fine pointers only) ---------- */
  var finePointer = window.matchMedia('(pointer:fine)').matches;
  if (finePointer) {
    var cur = document.getElementById('cur'),
        cr  = document.getElementById('cur-r');
    var mx = 0, my = 0, rx = 0, ry = 0, started = false;
    document.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      if (cur) { cur.style.left = mx + 'px'; cur.style.top = my + 'px'; }
      if (!started) { started = true; loop(); }
    });
    function loop() {
      rx += (mx - rx) * 0.12; ry += (my - ry) * 0.12;
      if (cr) { cr.style.left = rx + 'px'; cr.style.top = ry + 'px'; }
      requestAnimationFrame(loop);
    }
    document.addEventListener('mouseover', function (e) {
      if (e.target.closest('a,button,.dot,.faq-q,input,select,image-slot')) {
        if (cr) { cr.style.width = '48px'; cr.style.height = '48px'; }
      }
    });
    document.addEventListener('mouseout', function (e) {
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
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('on'); obs.unobserve(e.target); }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { obs.observe(el); });

  /* ---------- RF model — scroll appear/disappear ---------- */
  var rfModelWrap = document.querySelector('.rf-model-wrap');
  if (rfModelWrap) {
    var rfBlock = document.querySelector('.has-model');
    var rfVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        rfModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    rfVisObs.observe(rfBlock);
  }

  /* ---------- Stem Cell model — scroll appear/disappear ---------- */
  var scModelWrap = document.querySelector('.sc-model-wrap');
  if (scModelWrap) {
    var scBlock = document.querySelector('.has-model-sc');
    var scVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        scModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    scVisObs.observe(scBlock);
  }

  /* ---------- Mental Wellness model — scroll appear/disappear ---------- */
  var mwModelWrap = document.querySelector('.mw-model-wrap');
  if (mwModelWrap) {
    var mwBlock = document.querySelector('.has-model-mw');
    var mwVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        mwModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    mwVisObs.observe(mwBlock);
  }

  /* ---------- Contrast Suites model — scroll appear/disappear ---------- */
  var csModelWrap = document.querySelector('.cs-model-wrap');
  if (csModelWrap) {
    var csBlock = document.querySelector('.has-model-cs');
    var csVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        csModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    csVisObs.observe(csBlock);
  }

  /* ---------- Body Aesthetics model — scroll appear/disappear ---------- */
  var baModelWrap = document.querySelector('.ba-model-wrap');
  if (baModelWrap) {
    var baBlock = document.querySelector('.has-model-ba');
    var baVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        baModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    baVisObs.observe(baBlock);
  }

  /* ---------- Sexual Health model — scroll appear/disappear ---------- */
  var shModelWrap = document.querySelector('.sh-model-wrap');
  if (shModelWrap) {
    var shBlock = document.querySelector('.has-model-sh');
    var shVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        shModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    shVisObs.observe(shBlock);
  }

  /* ---------- Regenerative & Wellness model — scroll appear/disappear ---------- */
  var rwModelWrap = document.querySelector('.rw-model-wrap');
  if (rwModelWrap) {
    var rwBlock = document.querySelector('.has-model-rw');
    var rwVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        rwModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    rwVisObs.observe(rwBlock);
  }

  /* ---------- Injectables model — scroll appear/disappear ---------- */
  var injModelWrap = document.querySelector('.inj-model-wrap');
  if (injModelWrap) {
    var injBlock = document.querySelector('.inj-block');
    var injVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        injModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    injVisObs.observe(injBlock);
  }

  /* ---------- Laser model — scroll appear/disappear ---------- */
  var laserModelWrap = document.querySelector('.laser-model-wrap');
  if (laserModelWrap) {
    var laserBlock = document.querySelector('.has-model-laser');
    var laserVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        laserModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    laserVisObs.observe(laserBlock);
  }

  /* ---------- Medical Facials model — scroll appear/disappear ---------- */
  var mfModelWrap = document.querySelector('.mf-model-wrap');
  if (mfModelWrap) {
    var mfBlock = document.querySelector('.has-model-mf');
    var mfVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        mfModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    mfVisObs.observe(mfBlock);
  }

  /* ---------- Ultrasound model — scroll appear/disappear ---------- */
  var usModelWrap = document.querySelector('.us-model-wrap');
  if (usModelWrap) {
    var usBlock = document.querySelector('.has-model-us');
    var usVisObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        usModelWrap.classList.toggle('visible', e.isIntersecting);
      });
    }, { threshold: 0.05 });
    usVisObs.observe(usBlock);
  }

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
  if (form) {
    form.querySelectorAll('input,select').forEach(function (el) {
      el.addEventListener('input', function () { markInvalid(el, false); });
      el.addEventListener('change', function () { markInvalid(el, false); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fn = field('firstName'), ln = field('lastName'),
          ph = field('phone'), em = field('email'),
          doc = field('physician'), tr = field('treatment');
      var ok = true;
      if (!fn.value.trim()) { markInvalid(fn, true); ok = false; }
      if (!ph.value.trim() || ph.value.replace(/\D/g, '').length < 7) { markInvalid(ph, true); ok = false; }
      if (em.value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value.trim())) { markInvalid(em, true); ok = false; }
      if (!tr.value) { markInvalid(tr, true); ok = false; }
      if (!ok) return;

      var treatment = tr.value;
      var line = MEDICAL_TREATMENTS.indexOf(treatment) !== -1 ? LINES.medical : LINES.aesthetics;

      var msg = '';
      msg += 'Hello CANVAS, I would like to request a consultation.\n\n';
      msg += 'Name: ' + fn.value.trim() + ' ' + ln.value.trim() + '\n';
      msg += 'Phone: ' + ph.value.trim() + '\n';
      if (em.value.trim()) msg += 'Email: ' + em.value.trim() + '\n';
      msg += 'Treatment: ' + treatment + '\n';
      if (doc.value && doc.value.indexOf('No preference') === -1) msg += 'Preferred physician: ' + doc.value + '\n';
      msg += '\nSent from canvasmedical website.';

      var url = 'https://wa.me/' + line + '?text=' + encodeURIComponent(msg);
      window.open(url, '_blank');

      // success state
      var success = document.getElementById('formSuccess');
      var wrap = document.getElementById('formWrap');
      if (success && wrap) { wrap.style.display = 'none'; success.classList.add('show'); }
    });
  }
})();
