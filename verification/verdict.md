# CANVAS Medical — SEO / Technical Verification

**Verdict: PASS** (no P0/P1 blockers; P1 content gap + P2 polish noted)
**Scope:** live site `https://canvas-medical.com` + local repo `/opt/data/canvas-medical/`
**Date:** 2026-07-05 · **Mode:** read-only, no files modified
**Method:** live `curl` fetch of all 13 pages + `grep`/`perl` extraction; local repo grep for NAP/stale content. Live page bytes == local file bytes (deployed == repo, e.g. hifu 22842 both).

Pages fetched (all HTTP 200): home, botox, dermal-fillers, hifu, laser, medical-facials, rf-skin-tightening, prp, profhilo, microneedling, stem-cell, doctors/, blog/. `/about` & `/contact` = 404 (content lives as home sections — see notes).

---

## Per-item checklist

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | **Title** unique & <60 chars | ✅ | 13/13 unique; longest 56 (blog), home 53, botox 39 |
| 2 | **Meta description** unique & <160 | ✅ | 13/13 unique; longest 157 (doctors), rest 142–155 |
| 3 | **H1** exactly one, includes "Penang" | ✅ | 1 `<h1>` per page; every H1 contains Penang (home: "…Aesthetic Clinic in Penang…"; service pages "X in <em>Penang</em>…"; doctors "Our Physicians in Penang") |
| 4 | **Open Graph** og:title/description/image | ✅ (⚠️img) | All three present on all pages. ⚠️ `og:image` = same generic `assets/hero-model.png` on every page (resolves 200) |
| 5 | **JSON-LD** MedicalClinic + NAP match | ✅ | `MedicalClinic` on all 13 pages; also FAQPage, MedicalProcedure, BreadcrumbList, Physician (×4), Blog/BlogPosting. Schema NAP byte-matches canonical (see NAP block) |
| 6 | **Canonical URL** | ✅ | All 13 self-referential, absolute https, unique, trailing-slash correct on dir pages |
| 7 | **Image alt text** | ✅ | 0 images missing `alt`. Only empty `alt=""` is the decorative `canvas-mark.png` watermark, correctly paired with `aria-hidden="true"` |
| 8 | **Responsive** | ✅* | `<meta name=viewport width=device-width,initial-scale=1.0>` present; 16 `@media` queries in styles.css; mobile-UA fetch returns identical 60684 bytes (static, no cloaking). *Not pixel-rendered — no browser driven |
| 9 | **NAP consistency** | ⚠️ | Phone/email/address/postcode match canonical everywhere EXCEPT 2 deviations (see P2-a, P2-b) |
| 10 | **Stale content** | ✅ | No "Sungai Dua"/Bayan/Gelugor/Jelutong/old postcodes. Only 2 phone numbers in use, both canonical |
| 11 | **Content gaps** | ❌/⚠️ | No pricing anywhere (P1). FAQ ✅. Map/testimonials/gallery present on home only |

---

## NAP verification (vs owner-confirmed canonical)

| Field | Canonical | Live site | Match |
|-------|-----------|-----------|-------|
| Street | Gurney Walk, Lot G-6 (GF) & Lot S-1 (2nd Floor), No. 18A, Persiaran Gurney | 36× exact | ✅ (2 exceptions below) |
| Locality/Region/Postcode | George Town / Pulau Pinang / 10250 | matches | ✅ |
| Phone (Medical) | +60 11-2854 7882 | 52× display + `tel:+601128547882` | ✅ |
| Phone (Aesthetics) | +60 18-981 5639 | 28× display + `tel:+60189815639` | ✅ |
| Email | hello@canvas-medical.com | 7× (plus benign `your@email.com` form placeholder) | ✅ |
| Hours | Open daily · 10:00am – 10:00pm | present but formatting varies (P2-b) | ⚠️ |

---

## Issues (ordered)

### P0 — none

### P1
- **P1-a — No pricing on any page.** `RM` + digits = 0 matches site-wide (home & all service pages). No price ranges, no "from RM…", no fee guidance. Explicit gap for the task's pricing check. (Common/deliberate for aesthetic clinics, but flagged as requested.)

### P2 (polish / consistency)
- **P2-a — NAP address deviation.** 2× "Lot G-6 **(Ground Floor)**" instead of canonical "Lot G-6 **(GF)**" — both in home FAQ: `index.html:175` (JSON-LD FAQ answer) and `index.html:750` (visible FAQ). Every other rendering (36×) uses "(GF)".
- **P2-b — Hours formatting inconsistent.** Mixed renderings: `10:00am – 10:00pm` (canonical, 23×) vs `10am – 10pm` (32×) vs `10am–10pm` (21×); label casing `Open daily`/`Open Daily`/`open daily`. Hurts strict citation/NAP byte-consistency.
- **P2-c — Generic OG image.** Every page (including 11 service pages) shares `hero-model.png` as `og:image`. Per-service social images would improve share CTR / differentiation.
- **P2-d — Social proof weak / thin location on service pages.** Home has 3 testimonials + Google Maps link + gallery section; service pages carry only footer NAP + FAQ (no map embed, no gallery/before-after, no testimonials). Note: no `Review`/`AggregateRating` schema anywhere — this appears **intentional** (git `a43e329` stripped Review microdata from unverified testimonials — correct, avoids Google penalty).

---

## Positive notes
- Technical SEO foundation is strong: unique titles/descriptions/canonicals across all 13 pages, single keyworded H1 each, complete OG set, rich valid JSON-LD (MedicalClinic + Physician + FAQPage + Breadcrumb + Blog).
- FAQ coverage: 14 Q on home, 5 Q per service page — good long-tail + FAQ-rich-result surface.
- `robots.txt` correct (`Allow: /`, `Disallow: /admin.html`), sitemap.xml live (200) with 20 URLs, lastmod 2026-07-03.
- Alt text and decorative-image accessibility handled correctly.
- Zero stale legacy content; NAP phones/email fully consistent.

**Bottom line:** ship-ready. Fix the two home-FAQ "(Ground Floor)"→"(GF)" strings and normalise hours formatting (P2, ~10 min), then decide on pricing (P1) as a content/business call.
