# CANVAS Medical — Design System

## Brand Register
- **Kind:** Luxury medical-aesthetic clinic landing page
- **Register:** Brand (design IS the product)
- **Audience:** Design-conscious Penang consumers choosing a premium clinic
- **Vibe:** Quiet luxury, bronze warmth, dark editorial
- **Physical scene:** Warm bronze accents, dark wood, soft lighting — Gurney Walk clinic

## Colour Palette

### Accent (locked page-wide)
| Token | Value | Usage |
|-------|-------|-------|
| `--accent` | `oklch(0.55 0.0396 70)` | Borders, hover states, tinted surfaces |
| `--accent-strong` | `oklch(0.46 0.0432 70)` | CTAs, focus rings, interactive highlights |

The accent is a low-chroma champagne/bronze (`70°` hue, chroma ~4%). **Never change the hue.** Chroma is dialled up on light theme to preserve legibility.

### Dark theme (default)
| Token | Value | Notes |
|-------|-------|-------|
| `--bg` | `#070707` | Near-black, not pure #000 |
| `--surface` | `oklch(0.12 0.003 70)` | Card/panel surfaces |
| `--text` | `oklch(0.88 0.01 70)` | Body ink, tinted warm |
| `--text-dim` | `oklch(0.62 0.012 70)` | Secondary text |

### Light theme
| Token | Value | Notes |
|-------|-------|-------|
| `--bg` | `oklch(0.97 0 0)` | Neutral gallery white — chroma 0 |
| `--surface` | `oklch(0.99 0 0)` | Card/panel surfaces |
| `--text` | `oklch(0.22 0 0)` | Body ink, neutral |
| `--text-dim` | `oklch(0.44 0 0)` | Secondary text |

Warmth is carried by the accent + serif typography + imagery, **never** by the body background.

### Banned palettes
- Cream/beige/warm-paper backgrounds (`#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`)
- Espresso warm-text on warm-paper (`#1a1714`, `#1a1814`)
- Brass/clay/oxblood accents (`#b08947`, `#9a2436`, `#b6553a`)
- AI-purple/blue gradient glow

## Typography

| Role | Font | Weight | Notes |
|------|------|--------|-------|
| Display serif | Cormorant Garamond | 300, 400 | Hero headings, section titles |
| Display serif (alt) | EB Garamond | 400 | Section titles |
| Display serif (alt) | Playfair Display | 400 | Emphasis words, pull quotes |
| Body sans | Jost | 200, 300, 400 | Body text, labels, nav |
| Monospace | (system) | — | Decorative monogram placeholder |

- **Body:** tinted (`var(--text)` not pure white/black), max-width 65–75ch
- **Serif is defensible** because the brand is luxury/heritage medical. All three serifs are on the acceptable list.
- **No Inter** (overused). Jost is the body sans.
- **No italic serif as default.** Italic serif emphasis is a *signature device*, used on ≤2 section headers per page.

## Spacing & Layout
- Max-width container: `1160px`
- Section vertical spacing: `120px` (`--space-section`)
- Grid gutters: `24px`
- Content columns are airy (VISUAL_DENSITY: 3/10)

## z-Index Scale (semantic)
| Token | Value | Element |
|-------|-------|---------|
| `--z-fab` | 40 | Floating WhatsApp button |
| `--z-nav` | 50 | Sticky header |
| `--z-overlay` | 60 | Mobile menu overlay |
| `--z-nav-open` | 65 | Header above open overlay |
| `--z-toggle` | 70 | Hamburger toggle |
| `--z-skip` | 80 | Skip-to-content link |
| `--z-modal` | 90 | Dialogs (reserved) |
| `--z-cursor` | 100 | Custom cursor (hero only) |

**No raw z-index values in CSS** — always use these tokens.

## Motion
- **Dials:** VARIANCE=7, MOTION_INTENSITY=6, VISUAL_DENSITY=3
- Scroll reveals use `IntersectionObserver` (not raw scroll handlers)
- Ease-out curves only — no bounce, no elastic; signature ease is `cubic-bezier(.22,1,.36,1)`
- `prefers-reduced-motion` respected on all animations
- Motion is motivated: hierarchy, storytelling, state feedback — never decoration
- Reveal staggering: `.reveal-stagger` for list children (70ms steps via `--si`
  index set by app.js), `.reveal` for standalone
- Page load: body fade-in (`pageIn`), hero lines rise sequentially, treatment-page
  hero (`.tp-crumb → h1 → .tp-lead → .tp-hero-btns`) staggers on load
- Ambient: `heroDrift` champagne aura on `#hero` and `.tp-hero` (transform-only, GPU)
- Hover: card lifts (`.t-card`, `.tp-card` — transform + shadow), CTA sheen sweep
  (`.btn-fill`, `.nav-book`, `.btn-submit`), footer link underlines, gallery zoom

## Interaction States
Every interactive element must define:
- **Hover** — colour shift, underline, or scale
- **Active** (`:active`) — pressed feedback (darker, smaller)
- **Focus** — `:focus-visible` ring (2px solid `--accent-strong`, 3px offset)
- **Loading** — `.is-loading` class with spinner (buttons, forms)
- **Error** — `.invalid` class on `.f-field` (forms)
- **Success** — `.show` on `.form-success` block

## Component Kit

### `.t-card`
Treatment/service card. Variants:
- **Default:** single column, icon + name + description + link
- **`.feature`:** Larger tile (2×2 on 4-col grid), tinted background, prominent icon + tag
- **`.wide`:** Spans 2 columns, wider description
- **`.cta`:** Call-to-action card at grid end, accent-tinted background

### Buttons
- **`.btn-fill`:** Solid accent CTA
- **`.btn-line`:** Outlined secondary CTA
- **`.btn-submit`:** Form submit button with `.is-loading` state

### Forms
- `.f-field.invalid` triggers `.f-err` error text visibility
- Spinner via `.spinner` inside `.btn-submit.is-loading`
- Success: #formWrap hidden, #formSuccess.show displayed

## Image Strategy
- **Real imagery is non-negotiable** — the biggest quality lever
- Crosshair placeholders replaced with `ph-mono` monogram (`C`)
- Images served as WebP when possible
- `image-slot` custom element for admin-managed photos

## Accessibility
- Skip link (`.skip-link`)
- `:focus-visible` on all interactive elements
- `sr-only` class for screen-reader-only content
- ARIA attributes on nav toggle, FAQ items
- Semantic HTML: `<nav>`, `<main>`, `<section>`, `<footer>`
- Contrast: body ≥4.5:1, large text ≥3:1
- Custom cursor scoped to hero section only (trust concern for medical brand)

## Preflight Checklist (before shipping any change)
- [ ] No em-dashes in visible copy
- [ ] Not the beige+brass+espresso palette
- [ ] All interactive elements have hover/active/focus states
- [ ] Not 3+ identical feature cards
- [ ] No full uppercase eyebrows above every section
- [ ] prefers-reduced-motion respected
- [ ] Body text contrast ≥4.5:1 (WCAG AA)
- [ ] Hero fits viewport without scroll
- [ ] No numbered section markers
- [ ] At least 1 real image on the page
- [ ] No raw scroll listeners (use IntersectionObserver)
- [ ] All z-index values use `--z-*` tokens
- [ ] No dead `#` links, no lorem ipsum
