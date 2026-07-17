#!/usr/bin/env python3
"""Propagate clinic-wide constants from data/site.json into every page.

Usage:  python3 scripts/update-site.py

Keeps the site DRY: phones, address, hours, geo, socials and the footer
tagline are defined once in data/site.json. This script:

  1. Rewrites every JSON-LD block on every page, replacing telephone,
     PostalAddress, openingHoursSpecification, geo and sameAs values
     with the canonical ones (idempotent round-trip via json).
  2. Canonicalises known text variants (e.g. hour formats) in visible
     copy, and sets the footer tagline everywhere.
  3. Validates: flags any phone-like string or GA tag that does not
     match the canonical values, and any page missing analytics.

Physician-derived surfaces are handled by scripts/update-physicians.py.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = json.loads((ROOT / "data/site.json").read_text())

ADDRESS_LD = {
    "@type": "PostalAddress",
    "streetAddress": SITE["address"]["street"],
    "addressLocality": SITE["address"]["locality"],
    "addressRegion": SITE["address"]["region"],
    "postalCode": SITE["address"]["postcode"],
    "addressCountry": SITE["address"]["country"],
}
HOURS_LD = [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": SITE["hours"]["days"],
    "opens": SITE["hours"]["opens"],
    "closes": SITE["hours"]["closes"],
}]
GEO_LD = {"@type": "GeoCoordinates", "latitude": SITE["geo"]["lat"], "longitude": SITE["geo"]["lng"]}
SOCIALS = [SITE["socials"]["instagram"], SITE["socials"]["facebook"]]
PHONE = SITE["phones"]["medical"]["display"]

def normalise(node):
    """Recursively stamp canonical values into a JSON-LD structure."""
    if isinstance(node, dict):
        if "telephone" in node:
            node["telephone"] = PHONE
        if isinstance(node.get("address"), dict) and node["address"].get("@type") == "PostalAddress":
            node["address"] = dict(ADDRESS_LD)
        if "openingHoursSpecification" in node:
            node["openingHoursSpecification"] = [dict(h) for h in HOURS_LD]
        if isinstance(node.get("geo"), dict):
            node["geo"] = dict(GEO_LD)
        if node.get("@type") == "MedicalClinic" and "sameAs" in node:
            node["sameAs"] = list(SOCIALS)
        for v in node.values():
            normalise(v)
    elif isinstance(node, list):
        for v in node:
            normalise(v)

# visible-copy variants -> canonical
TEXT_FIXES = [
    ("10:00am – 10:00pm", SITE["hours"]["text"]),
    ("10:00am – 10:00pm".replace(" – ", " - "), SITE["hours"]["text"]),
]
TAG_RE = re.compile(r'(<p class="contact-tag">).*?(</p>)')
LD_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

pages = [f for f in sorted(ROOT.rglob("*.html"))
         if f.name != "admin.html" and "templates" not in f.relative_to(ROOT).parts]
warnings, changed = [], 0
for f in pages:
    s = orig = f.read_text()

    def fix_ld(m):
        try:
            data = json.loads(m.group(2))
        except Exception:
            warnings.append(f"{f}: unparseable JSON-LD left untouched")
            return m.group(0)
        normalise(data)
        return m.group(1) + "\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n" + m.group(3)
    s = LD_RE.sub(fix_ld, s)

    for old, new in TEXT_FIXES:
        s = s.replace(old, new)
    s = TAG_RE.sub(r"\g<1>" + SITE["tagline"] + r"\g<2>", s)

    # validation
    valid_phones = {SITE["phones"]["medical"]["display"], SITE["phones"]["aesthetics"]["display"],
                    SITE["phones"]["medical"]["tel"], SITE["phones"]["aesthetics"]["tel"]}
    for ph in set(re.findall(r"\+60[\d\s-]{9,14}", s)):
        if ph.strip() not in valid_phones:
            warnings.append(f"{f}: unexpected phone {ph!r}")
    for tel in set(re.findall(r'(?:tel:|wa\.me/)(\+?\d+)', s)):
        if tel not in (SITE["phones"]["medical"]["tel"], SITE["phones"]["aesthetics"]["tel"],
                       SITE["whatsapp"].rsplit("/", 1)[1]):
            warnings.append(f"{f}: unexpected tel/wa target {tel!r}")
    if "googletagmanager" in s and SITE["ga_id"] not in s:
        warnings.append(f"{f}: GA id differs from canonical")
    if f.name != "404.html" and "googletagmanager" not in s:
        warnings.append(f"{f}: missing analytics tag")

    if s != orig:
        f.write_text(s)
        changed += 1

print(f"{len(pages)} pages scanned, {changed} updated")
for w in warnings:
    print("WARN:", w)
if warnings:
    sys.exit(1)
print("all constants consistent with data/site.json")
