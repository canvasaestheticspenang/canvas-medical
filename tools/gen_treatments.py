#!/usr/bin/env python3
"""Generate CANVAS Medical treatment landing pages from a shared template.
Run from repo root:  python3 tools/gen_treatments.py
Outputs <slug>.html for each treatment, reusing styles.css / app.js / nav / footer.
"""
import html, os, json

SITE = "https://canvas-medical.com"

# ---- shared chrome -----------------------------------------------------------
NAV = '''<nav id="nav">
  <a href="index.html" class="nav-logo" aria-label="CANVAS — home"><img src="assets/canvas-logo.png" alt="CANVAS Medical Clinic"></a>
  <ul class="nav-links">
    <li><a href="index.html#services">Treatments</a></li>
    <li><a href="index.html#philosophy">About</a></li>
    <li><a href="index.html#team">Physicians</a></li>
    <li><a href="index.html#location">Visit Us</a></li>
    <li><a href="index.html#faq">FAQ</a></li>
  </ul>
  <div class="nav-cta">
    <a href="index.html#book" class="nav-book">Book Now</a>
    <button id="navToggle" class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<div id="mobileMenu" class="mobile-menu" aria-hidden="true">
  <button id="navClose" class="mobile-menu-close" aria-label="Close menu">
    <span></span><span></span>
  </button>
  <a href="index.html#services">Treatments</a>
  <a href="index.html#philosophy">About</a>
  <a href="index.html#team">Physicians</a>
  <a href="index.html#location">Visit Us</a>
  <a href="index.html#faq">FAQ</a>
  <a href="index.html#book" class="mm-book">Book a Consultation</a>
  <div class="mm-meta">Gurney Walk, George Town · Penang<br>Daily 10am – 10pm</div>
</div>'''

FOOTER = '''<section id="contact">
  <div class="contact-block reveal">
    <div class="contact-logo"><img src="assets/canvas-logo.png" alt="CANVAS Medical Clinic"></div>
    <p class="contact-tag">Penang's premier medical aesthetic clinic. Where science meets artistry.</p>
  </div>
  <div class="c-col reveal d1">
    <h4>Visit Us</h4>
    <p>Gurney Walk, Lot G-6 (GF) &amp; Lot S-1 (2nd Floor)</p>
    <p>No. 18A, Persiaran Gurney</p>
    <p>10250 George Town, Penang</p>
    <div class="c-gap">
      <a href="tel:+601128547882">+60 11-2854 7882 · Medical Aesthetics</a>
      <a href="tel:+60189815639">+60 18-981 5639 · Aesthetics</a>
    </div>
  </div>
  <div class="c-col reveal d2">
    <h4>Hours</h4>
    <p>Open daily</p>
    <p>10:00am – 10:00pm</p>
    <div class="c-gap">
      <h4>Follow</h4>
      <a href="#">Instagram</a>
      <a href="https://wa.me/601128547882" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>

<footer>
  <p>© 2026 CANVAS Medical Clinic · George Town, Penang. All rights reserved.</p>
  <div class="foot-links">
    <a href="index.html">Home</a>
    <a href="index.html#services">Treatments</a>
  </div>
</footer>

<a id="fab" class="fab" href="https://wa.me/601128547882" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.945C.16 5.335 5.495 0 12.05 0a11.82 11.82 0 018.413 3.488 11.82 11.82 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884a9.86 9.86 0 001.516 5.26l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
</a>

<script src="app.js"></script>'''


def esc(s):
    return html.escape(s, quote=True)


def render(p):
    url = f"{SITE}/{p['slug']}"
    paras = lambda lst: "\n        ".join(f"<p>{x}</p>" for x in lst)
    steps = "\n        ".join(f"<li>{x}</li>" for x in p["how"])
    cards = "\n        ".join(
        f'<div class="tp-card"><h3>{h}</h3><p>{b}</p></div>' for h, b in p["benefits"]
    )
    who = "\n        ".join(p["who"])  # data entries already include <li> tags
    why = "\n          ".join(f"<li>{x}</li>" for x in p["why"])
    focus = "\n        ".join(f"<span>{x}</span>" for x in p["focus"])
    faq_items = []
    faq_schema = []
    for i, (q, a) in enumerate(p["faqs"]):
        d = " d1" if i % 3 == 1 else (" d2" if i % 3 == 2 else "")
        faq_items.append(
            f'<div class="faq-item reveal{d}">\n'
            f'          <button class="faq-q" aria-expanded="false"><span>{q}</span><span class="faq-plus" aria-hidden="true">+</span></button>\n'
            f'          <div class="faq-a">{a}</div>\n'
            f'        </div>'
        )
        faq_schema.append({
            "@type": "Question",
            "name": html.unescape(q),
            "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)},
        })
    faq_html = "\n        ".join(faq_items)

    proc_schema = {
        "@context": "https://schema.org",
        "@type": "MedicalProcedure",
        "@id": f"{url}#procedure",
        "name": p["procName"],
        "alternateName": p["alt"],
        "procedureType": "https://schema.org/NoninvasiveProcedure" if p.get("noninvasive", True) else "https://schema.org/PercutaneousProcedure",
        "bodyLocation": p.get("body", "Face"),
        "description": p["procDesc"],
        "url": url,
        "howPerformed": p["howPerformed"],
        "preparation": p["prep"],
        "followup": p["followup"],
        "provider": {
            "@type": "MedicalClinic",
            "@id": f"{SITE}/#clinic",
            "name": "CANVAS Medical Clinic",
            "telephone": "+60 11-2854 7882",
            "url": f"{SITE}/",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Gurney Walk, Lot G-6 (GF) & Lot S-1 (2nd Floor), No. 18A, Persiaran Gurney",
                "addressLocality": "George Town",
                "addressRegion": "Pulau Pinang",
                "postalCode": "10250",
                "addressCountry": "MY",
            },
            "geo": {"@type": "GeoCoordinates", "latitude": 5.4382, "longitude": 100.3095},
        },
    }
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Treatments", "item": f"{SITE}/#services"},
            {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url},
        ],
    }
    faqpage_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}

    j = lambda o: json.dumps(o, indent=2, ensure_ascii=False)
    what_verb = "are" if p["short"].rstrip().endswith(("fillers", "facials")) else "is"

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light" data-cursor="on">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["meta"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=EB+Garamond:ital,wght@0,400;1,400&family=Jost:wght@200;300;400&family=Playfair+Display:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#070707">
<meta name="robots" content="index,follow">
<link rel="icon" type="image/png" href="assets/canvas-mark.png">
<link rel="apple-touch-icon" href="assets/canvas-mark.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="CANVAS Medical Clinic">
<meta property="og:title" content="{esc(p["title"])}">
<meta property="og:description" content="{esc(p["meta"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/hero-model.png">
<meta property="og:locale" content="en_MY">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p["title"])}">
<meta name="twitter:description" content="{esc(p["meta"])}">
<meta name="twitter:image" content="{SITE}/assets/hero-model.png">
<meta name="geo.region" content="MY-07">
<meta name="geo.placename" content="George Town, Penang">
<meta name="geo.position" content="5.4382;100.3095">
<meta name="ICBM" content="5.4382, 100.3095">
<script type="application/ld+json">
{j(proc_schema)}
</script>
<script type="application/ld+json">
{j(breadcrumb_schema)}
</script>
<script type="application/ld+json">
{j(faqpage_schema)}
</script>
</head>
<body>
<a href="#main" class="skip-link">Skip to content</a>
<div id="cur" aria-hidden="true"></div>
<div id="cur-r" aria-hidden="true"></div>

{NAV}

<main id="main">

<header class="tp-hero">
  <div class="tp-hero-inner">
    <nav class="tp-crumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a><span class="sep">/</span>
      <a href="index.html#services">Treatments</a><span class="sep">/</span>
      <span class="here">{p["crumb"]}</span>
    </nav>
    <h1>{p["h1"]}</h1>
    <p class="tp-lead">{p["lead"]}</p>
    <div class="tp-hero-btns">
      <a href="index.html#book" class="btn-fill">Book a Consultation</a>
      <a href="index.html#services" class="btn-line"><span class="bar"></span>All Treatments</a>
    </div>
  </div>
  <img class="tp-hero-watermark" src="assets/canvas-mark.png" alt="" aria-hidden="true">
</header>

<section class="tp-body">
  <div class="tp-wrap">

    <div class="tp-block reveal">
      <h2>What {what_verb} {p["short"]}?</h2>
      {paras(p["what"])}
      <div class="tp-focus">
        {focus}
      </div>
    </div>

    <div class="tp-block reveal">
      <h2>How it <em>works</em></h2>
      <ol class="tp-steps">
        {steps}
      </ol>
    </div>

    <div class="tp-block reveal">
      <h2>Benefits</h2>
      <div class="tp-cards">
        {cards}
      </div>
    </div>

    <div class="tp-block reveal">
      <h2>Who it's <em>for</em></h2>
      <div class="tp-why">
        <p>{p["whoIntro"]}</p>
        <ul>
        {who}
        </ul>
      </div>
    </div>

    <div class="tp-block reveal">
      <h2>Why CANVAS</h2>
      {paras(p["whyIntro"])}
      <div class="tp-why">
        <ul>
          {why}
        </ul>
      </div>
    </div>

  </div>
</section>

<section class="section dark">
  <div class="section-inner">
    <div class="tp-faq">
      <div class="sec-label reveal">FAQ</div>
      <h2 class="sec-title reveal" style="margin-bottom:38px;">{p["short"]}, <em>answered.</em></h2>
      <div class="faq-list">
        {faq_html}
      </div>
    </div>
  </div>
</section>

<section class="tp-body" style="padding-top:0;">
  <div class="tp-wrap">
    <div class="tp-cta-band reveal">
      <h2>Considering {p["short"]} in <em>Penang?</em></h2>
      <p>{p["ctaText"]}</p>
      <a href="index.html#book" class="btn-fill">Reserve a Consultation</a>
      <div class="tp-cta-meta">
        CANVAS Medical Clinic · Gurney Walk, No. 18A Persiaran Gurney, George Town, Penang<br>
        Medical aesthetics <a href="tel:+601128547882">+60 11-2854 7882</a> · Aesthetics <a href="tel:+60189815639">+60 18-981 5639</a> · Open daily 10am–10pm
      </div>
    </div>
  </div>
</section>

</main>

{FOOTER}
</body>
</html>'''


PAGES = json.load(open(os.path.join(os.path.dirname(__file__), "treatments_data.json"), encoding="utf-8"))

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for p in PAGES:
        out = os.path.join(root, p["slug"] + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(render(p))
        print("wrote", out)
    print(f"done: {len(PAGES)} pages")
