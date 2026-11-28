#!/usr/bin/env python3
"""Rebuild the 1200 x 1200 square covers from the product JPGs, trimming empty
white margins so the product fills about 85% of the frame (Shopee asks for 70%+)."""
import io, json, pathlib
from PIL import Image, ImageChops
ROOT = pathlib.Path(__file__).resolve().parent.parent
for it in json.loads((ROOT / "shop-images/manifest.json").read_text()):
    if not it["square"]: continue
    im = Image.open(ROOT / it["path"]).convert("RGB")
    mask = ImageChops.difference(im, Image.new("RGB", im.size, "white")).convert("L").point(lambda v: 255 if v > 12 else 0)
    box = mask.getbbox() or (0, 0, im.width, im.height)
    im = im.crop(box)
    s = min(1020 / im.width, 1020 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c = Image.new("RGB", (1200, 1200), "white"); c.paste(im, ((1200 - im.width) // 2, (1200 - im.height) // 2))
    for q in (90, 85, 80):
        buf = io.BytesIO(); c.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= 2_000_000: break
    (ROOT / it["square"]).write_bytes(buf.getvalue())
print("squares rebuilt")
