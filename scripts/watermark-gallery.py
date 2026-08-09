#!/usr/bin/env python3
"""Prepare a photo for the homepage gallery carousel.

Usage:  python3 scripts/watermark-gallery.py <slot> <source-photo> [offset]
        python3 scripts/watermark-gallery.py gallery-16 ~/shoot/DSC_1234.jpg
        python3 scripts/watermark-gallery.py gallery-16 ~/shoot/DSC_1234.jpg 0.14

Takes an original photo and writes assets/gallery/<slot>.webp: cropped to
the card's 4:3, resized, and stamped with the CANVAS V-mark.

`offset` shifts the crop window vertically, as a fraction of the source
height (negative up, positive down, default centred). Gallery cards are
4:3 but shoot files are usually 2:3 portrait, so a centred crop keeps
only the middle band — enough to cut the eyes off a face that sits low
or clip the top of a head that sits high. Preview the framing before
committing and pass an offset when the default misses.

The watermark settings match the photos already in the gallery: V-mark
at 40% of image width, 2.5% margin, 55% opacity, bottom-right. They were
recovered by fitting the overlay back onto a pre-watermark revision, and
40% agrees with the note in 97e4c3c.

Always run this against the ORIGINAL photo. The watermark is baked into
the pixels, so re-running it on a file already in assets/gallery/ would
stamp a second mark on top of the first; the script refuses to do that.

Requires Pillow (pip install pillow) — unlike the generators in this
directory, which are stdlib-only.

After writing the file, add the card to the gallery track in index.html
and a slot entry to slots.js, both keyed by the same <slot> id.
"""
import pathlib
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: pip install pillow")

ROOT = pathlib.Path(__file__).resolve().parent.parent
GALLERY = ROOT / "assets" / "gallery"
MARK = ROOT / "assets" / "canvas-v-mark.png"

CARD_ASPECT = 4 / 3          # .g-item is aspect-ratio:4/3 in styles.css
OUT_WIDTH = 1600             # long edge used by the rest of the gallery
WM_WIDTH_FRAC = 0.40         # V-mark width, as a fraction of image width
WM_MARGIN_FRAC = 0.025       # gap from the right and bottom edges
WM_OPACITY = 0.55
WEBP_QUALITY = 82            # lands near the ~80 KB of the existing set


def build(slot, source, offset=0.0):
    source = pathlib.Path(source).expanduser().resolve()
    if GALLERY.resolve() in source.parents:
        sys.exit(
            f"{source.name} is already in assets/gallery/. The watermark is "
            "baked in, so re-stamping would double it — pass the original photo."
        )
    if not source.is_file():
        sys.exit(f"no such file: {source}")

    im = Image.open(source).convert("RGB")
    width, height = im.size

    # crop a full-width 4:3 window, shifted by `offset` and clamped in frame
    window = int(width / CARD_ASPECT)
    if window > height:
        sys.exit(
            f"{source.name} is {width}x{height} — too wide to crop to 4:3 "
            "without letterboxing. Crop it by hand first."
        )
    top = int((height - window) / 2 + offset * height)
    top = max(0, min(height - window, top))
    im = im.crop((0, top, width, top + window))
    im = im.resize((OUT_WIDTH, int(OUT_WIDTH / CARD_ASPECT)), Image.LANCZOS)

    im = stamp(im)
    GALLERY.mkdir(parents=True, exist_ok=True)
    out = GALLERY / f"{slot}.webp"
    im.save(out, "WEBP", quality=WEBP_QUALITY, method=6)

    kb = out.stat().st_size // 1024
    print(f"{out.relative_to(ROOT)}  {im.width}x{im.height}  {kb} KB")
    print(f"  crop top {top}/{height - window} px ({offset:+.0%})")
    print(f"  add a .g-item card for data-slot=\"{slot}\" to index.html,")
    print(f"  and a matching entry to slots.js")
    return out


def stamp(im):
    """Composite the V-mark into the bottom-right corner."""
    mark = Image.open(MARK).convert("RGBA")
    mark_w = round(im.width * WM_WIDTH_FRAC)
    mark = mark.resize(
        (mark_w, round(mark_w * mark.height / mark.width)), Image.LANCZOS
    )
    faded = mark.copy()
    faded.putalpha(mark.getchannel("A").point(lambda a: round(a * WM_OPACITY)))

    margin = round(im.width * WM_MARGIN_FRAC)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    layer.paste(faded, (im.width - mark_w - margin, im.height - faded.height - margin))
    return Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")


if __name__ == "__main__":
    if not 3 <= len(sys.argv) <= 4:
        sys.exit(__doc__)
    slot_arg, source_arg = sys.argv[1], sys.argv[2]
    offset_arg = float(sys.argv[3]) if len(sys.argv) == 4 else 0.0
    build(slot_arg, source_arg, offset_arg)
