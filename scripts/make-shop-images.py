#!/usr/bin/env python3
"""Shopee-ready product photos for the partner-brand pages.

shop-images/manifest.json lists every photo with its Drive id and target path:
  shop-images/<brand>/<brand>-<product>-NN.jpg  1200 x 1200 square, white
      background, under 2 MB. 01 is the cover. Use 01-09 for Shopee.
  shop-images/<brand>/extra/...                 long detail panels and logos
      (shown on the site, not for Shopee item images)
  .../small/<same name>                         600 px copies for page grids

Run with --from-drive to rebuild from the Drive originals (they must be shared
"anyone with the link"); without it, the listed files are re-made in place.
"""
import io, json, pathlib, sys, time, urllib.request
from PIL import Image, ImageChops, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIMIT = 2_000_000

def fetch(fid):
    err = None
    for u in ("https://lh3.googleusercontent.com/d/{id}=w2400", "https://drive.google.com/thumbnail?id={id}&sz=w2400"):
        for attempt in range(3):
            try:
                req = urllib.request.Request(u.format(id=fid), headers={"User-Agent": "Mozilla/5.0"})
                im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=90).read())); im.load(); return im
            except Exception as ex:
                err = ex; time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{fid}: {err}")

def flatten(im):
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[-1]); return bg
    return im.convert("RGB")

def is_cutout(im):
    w, h = im.size
    return all(sum(im.getpixel(c)) >= 735 for c in [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)])

def square(im, size=1200):
    if is_cutout(im):
        mask = ImageChops.difference(im, Image.new("RGB", im.size, "white")).convert("L").point(lambda v: 255 if v > 12 else 0)
        im = im.crop(mask.getbbox() or (0, 0, im.width, im.height)); inner = round(size * 0.85)
        bg = (255, 255, 255)
    else:
        inner = size
        w, h = im.size  # pad with the photo's own edge colour so the bars blend in
        px = [im.getpixel((x, y)) for x in range(0, w, max(1, w // 40)) for y in (0, h - 1)] + \
             [im.getpixel((x, y)) for y in range(0, h, max(1, h // 40)) for x in (0, w - 1)]
        bg = tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))
    s = min(inner / im.width, inner / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    c = Image.new("RGB", (size, size), bg); c.paste(im, ((size - im.width) // 2, (size - im.height) // 2)); return c

def save(im, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    for q in (90, 86, 82, 78, 74, 70):
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= LIMIT: break
    path.write_bytes(buf.getvalue())

def small_path(p):
    p = pathlib.Path(p); return p.parent / "small" / p.name

def make(it, src):
    out = ROOT / it["path"]
    if it["kind"] == "shopee":
        big = square(src); save(big, out); save(big.resize((600, 600), Image.LANCZOS), ROOT / small_path(it["path"]))
    else:
        big = src if src.width <= 1000 else src.resize((1000, round(src.height * 1000 / src.width)), Image.LANCZOS)
        save(big, out)
        sm = big if big.width <= 560 else big.resize((560, round(big.height * 560 / big.width)), Image.LANCZOS)
        save(sm, ROOT / small_path(it["path"]))

if __name__ == "__main__":
    items = json.loads((ROOT / "shop-images/manifest.json").read_text())
    failed = []
    for n, it in enumerate(items, 1):
        try:
            src = flatten(fetch(it["id"])) if "--from-drive" in sys.argv else flatten(Image.open(ROOT / it["path"]))
            make(it, src); print(f"[{n}/{len(items)}] {it['path']}")
        except Exception as ex:
            failed.append(it["path"]); print(f"[{n}/{len(items)}] FAILED {it['path']} {ex}")
    print(f"done, {len(failed)} failed"); sys.exit(1 if failed else 0)
