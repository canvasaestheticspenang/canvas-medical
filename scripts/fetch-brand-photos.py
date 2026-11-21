#!/usr/bin/env python3
"""Download the partner-brand photos listed in assets/brands/manifest.json from
Google Drive and save web-sized WebP copies next to it:

  assets/brands/<id>-s.webp   560 px wide  (product grid, thumbnails)
  assets/brands/<id>-l.webp  1200 px wide  (lightbox)

Skips files that already exist, so it is safe to rerun. Needs Pillow.
The Drive files must be shared "anyone with the link" while this runs.
"""
import io, json, pathlib, sys, time, urllib.request
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "assets/brands"
SIZES = {"s": 560, "l": 1200}
URLS = ["https://lh3.googleusercontent.com/d/{id}=w1600",
        "https://drive.google.com/thumbnail?id={id}&sz=w1600"]

def fetch(fid):
    for u in URLS:
        for attempt in range(3):
            try:
                req = urllib.request.Request(u.format(id=fid), headers={"User-Agent": "Mozilla/5.0"})
                data = urllib.request.urlopen(req, timeout=60).read()
                im = Image.open(io.BytesIO(data)); im.load()
                return im
            except Exception as ex:
                err = ex; time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{fid}: {err}")

ids = json.loads((DIR / "manifest.json").read_text())
failed = []
for n, fid in enumerate(ids, 1):
    if all((DIR / f"{fid}-{k}.webp").exists() for k in SIZES):
        continue
    try:
        im = ImageOps.exif_transpose(fetch(fid))
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        for k, w in SIZES.items():
            out = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            out.save(DIR / f"{fid}-{k}.webp", "WEBP", quality=78, method=6)
        print(f"[{n}/{len(ids)}] {fid} ok {im.size}")
    except Exception as ex:
        failed.append(fid); print(f"[{n}/{len(ids)}] FAILED {ex}")
print(f"done, {len(failed)} failed")
sys.exit(1 if failed else 0)
