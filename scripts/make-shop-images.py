#!/usr/bin/env python3
"""Make Shopee-ready JPGs for the partner-brand products.

Reads shop-images/manifest.json and, for each photo, downloads a large copy
from Google Drive and saves:
  shop-images/<brand>/<product>-<n>.jpg       long side up to 1600 px
  shop-images/<brand>/<product>-detail-<n>.jpg tall detail panels, 1000 px wide
  shop-images/<brand>/<product>-square.jpg     1200 x 1200 cover, white background
Every file is kept under 2 MB (Shopee's limit). Existing files are skipped.
The Drive files must be shared "anyone with the link" while this runs.
"""
import io, json, pathlib, sys, time, urllib.request
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIMIT = 2_000_000
URLS = ["https://lh3.googleusercontent.com/d/{id}=w2400",
        "https://drive.google.com/thumbnail?id={id}&sz=w2400"]

def fetch(fid):
    err = None
    for u in URLS:
        for attempt in range(3):
            try:
                req = urllib.request.Request(u.format(id=fid), headers={"User-Agent": "Mozilla/5.0"})
                im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=90).read())); im.load()
                return im
            except Exception as ex:
                err = ex; time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{fid}: {err}")

def flatten(im):
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[-1]); return bg
    return im.convert("RGB")

def save_jpg(im, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    for q in (90, 85, 80, 75, 70, 65):
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= LIMIT: break
    path.write_bytes(buf.getvalue())

def fit(im, box_w, box_h):
    s = min(box_w / im.width, box_h / im.height, 1)
    return im if s == 1 else im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)

items = json.loads((ROOT / "shop-images/manifest.json").read_text())
failed = []
for n, it in enumerate(items, 1):
    out = ROOT / it["path"]; sq = ROOT / it["square"] if it["square"] else None
    if out.exists() and (sq is None or sq.exists()): continue
    try:
        im = flatten(fetch(it["id"]))
        big = fit(im, 1000, 20000) if "-detail-" in it["path"] else fit(im, 1600, 1600)
        save_jpg(big, out)
        if sq:
            c = Image.new("RGB", (1200, 1200), "white"); p = fit(im, 1080, 1080)
            c.paste(p, ((1200 - p.width) // 2, (1200 - p.height) // 2)); save_jpg(c, sq)
        print(f"[{n}/{len(items)}] {it['path']} {big.size}")
    except Exception as ex:
        failed.append(it["path"]); print(f"[{n}/{len(items)}] FAILED {it['path']} {ex}")
print(f"done, {len(failed)} failed")
sys.exit(1 if failed else 0)
