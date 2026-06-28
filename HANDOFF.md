# CANVAS Medical Clinic — Project Handoff

Everything needed to continue working on **canvas-medical.com** from any computer.

## What this is
A static website (plain HTML/CSS/JS — no build step, no server needed) for CANVAS
Medical Clinic, Penang. The booking form opens WhatsApp; photos are managed through a
self-serve admin page.

## Where it's hosted
- **Code:** GitHub repo `canvasaestheticspenang/canvas-medical` (branch `main`, public).
- **Hosting:** GitHub Pages — **pushing to `main` auto-publishes** in ~1 minute.
- **Domain/DNS:** `canvas-medical.com` is registered/managed on **Cloudflare**.
  Apex A-records → GitHub IPs (185.199.108–111.153), `www` → `canvasaestheticspenang.github.io`,
  all **DNS-only (grey cloud)**. HTTPS cert is issued by Let's Encrypt and enforced.

---

## Continue on a NEW computer

### Option A — clone from GitHub (recommended)
1. Install **Git** (https://git-scm.com) and **GitHub CLI** (https://cli.github.com).
2. Sign in:  `gh auth login`  (choose GitHub.com → HTTPS → login via browser).
3. Clone:   `git clone https://github.com/canvasaestheticspenang/canvas-medical.git`
4. Edit files, then publish:
   `git add -A && git commit -m "your change" && git push`
   → the live site updates automatically.

### Option B — use this ZIP package
This folder is already a full git repo (history + GitHub remote included). On the new PC:
1. Unzip it.
2. Install Git + GitHub CLI, run `gh auth login`.
3. From inside the folder: `git pull` (get latest), edit, then `git add -A && git commit -m "..." && git push`.

---

## Preview locally (optional)
```
node tools/serve.js      →  open http://localhost:8731
```
(Plain `index.html` double-click also mostly works, but the local server is needed for
the photos.json fetch to behave exactly like production.)

## Key files
| File | Purpose |
|------|---------|
| `index.html` | The whole single-page site |
| `styles.css` | All styling (dark/light theme via `data-theme`) |
| `app.js` | Interactions (nav, FAQ, testimonials, WhatsApp booking) |
| `slots.js` | Map of photo slots (id + label + page location) |
| `photos.js` | Fills photo slots on the live site from `photos.json` |
| `photos.json` | Which uploaded image goes in which slot (managed by admin) |
| `admin.html` | **Photo uploader** — see below |
| `assets/` | Logo, mark, treatment images (already optimized) |
| `CNAME` | Custom domain for GitHub Pages — do not delete |
| `tools/serve.js` | Local preview server |
| `tools/optimize.js` | Re-compress images: `npm i sharp && node tools/optimize.js` |

## Managing photos (no coding)
Open **https://canvas-medical.com/admin.html** (unlisted). Paste a GitHub **fine-grained
token** once (Settings → Developer settings → Fine-grained tokens; Repository access =
canvas-medical; Permissions → Contents = **Read and write**). Then drag a photo onto any
tile and click **Publish** — it auto-resizes and goes live in ~1 minute.

## If HTTPS ever breaks
Re-queue the certificate by toggling the custom domain:
```
gh api -X PUT repos/canvasaestheticspenang/canvas-medical/pages -f cname=
gh api -X PUT repos/canvasaestheticspenang/canvas-medical/pages -f cname=canvas-medical.com -f "source[branch]=main" -f "source[path]=/"
```
Wait for the cert (`gh api repos/canvasaestheticspenang/canvas-medical/pages --jq .https_certificate.state`
→ `approved`), then: `gh api -X PUT .../pages -F https_enforced=true -f "source[branch]=main" -f "source[path]=/"`.
The API toggle commits to the remote CNAME file — run `git pull` afterward to resync.
