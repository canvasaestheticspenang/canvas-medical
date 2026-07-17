#!/usr/bin/env python3
"""Render the shared page chrome from templates/chrome.html onto every page.

Usage:  python3 scripts/update-chrome.py

The nav, mobile menu, contact section, footer, WhatsApp button and the
analytics snippet exist once, in templates/chrome.html, parameterised
with constants from data/site.json. This script rewrites those blocks
on every page (path prefixes adjusted per page depth; index and 404
get their special link forms). Edit the template, not the pages.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = json.loads((ROOT / "data/site.json").read_text())
TPL = (ROOT / "templates/chrome.html").read_text()

BLOCKS = dict(re.findall(r"<!-- block:(\w+) -->\n(.*?)\n<!-- endblock -->", TPL, re.S))
assert set(BLOCKS) == {"nav", "menu", "contact", "footer", "fab", "gtag"}, sorted(BLOCKS)

PAGE_RES = {
    "nav": re.compile(r'<nav id="nav">.*?</nav>', re.S),
    "menu": re.compile(r'<div id="mobileMenu".*?mm-meta.*?</div>\s*\n</div>', re.S),
    "contact": re.compile(r'<section id="contact">.*?</section>', re.S),
    "footer": re.compile(r'<footer>.*?</footer>', re.S),
    "fab": re.compile(r'<a id="fab".*?</a>', re.S),
    "gtag": re.compile(r"<!-- Google tag \(gtag\.js\) -->.*?gtag\('config'[^<]*</script>", re.S),
}

CONST = {
    "tagline": SITE["tagline"],
    "hours_text": SITE["hours"]["text"],
    "phone_med_tel": SITE["phones"]["medical"]["tel"],
    "phone_med_display": SITE["phones"]["medical"]["display"],
    "phone_med_label": SITE["phones"]["medical"]["label"],
    "phone_aes_tel": SITE["phones"]["aesthetics"]["tel"],
    "phone_aes_display": SITE["phones"]["aesthetics"]["display"],
    "phone_aes_label": SITE["phones"]["aesthetics"]["label"],
    "whatsapp": SITE["whatsapp"],
    "instagram": SITE["socials"]["instagram"],
    "ga_id": SITE["ga_id"],
    "year": SITE["copyright_year"],
}

changed = 0
for f in sorted(ROOT.rglob("*.html")):
    rel = f.relative_to(ROOT)
    if f.name == "admin.html" or "templates" in rel.parts:
        continue
    if f.name == "404.html":
        home, assets, logo = "/", "/", "/"
    elif str(rel) == "index.html":
        home, assets, logo = "", "", "#hero"
    else:
        assets = "../" * (len(rel.parts) - 1)
        home = assets + "index.html"
        logo = home
    ctx = {"home": home, "assets": assets, "logo_href": logo, **CONST}

    s = orig = f.read_text()
    for name, pat in PAGE_RES.items():
        block = BLOCKS[name].format(**ctx)
        s, n = pat.subn(lambda _m: block, s)
        if n != 1:
            sys.exit(f"ERROR: {rel}: block {name!r} matched {n} times")
    if s != orig:
        f.write_text(s)
        changed += 1
print(f"chrome rendered on {changed} page(s); all pages consistent with templates/chrome.html")
