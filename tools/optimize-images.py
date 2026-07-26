#!/usr/bin/env python3
"""
Optimize item photos for a sale-catalog site. Run it from a sale repo's root.

Reads every image in assets/images/ (top level, any-case extension) and writes
resized, EXIF-rotation-corrected WebP copies:

    assets/images/web/<name>.webp       ~1600px long edge, full aspect (fullscreen gallery)
    assets/images/thumb/<name>.webp     ~800px  wide, 4:3 centre-crop  (card thumbnail, 2x)
    assets/images/thumb-sm/<name>.webp  ~400px  wide, 4:3 centre-crop  (card thumbnail, 1x)

The card grid displays a 4:3 box (object-fit: cover), so the thumbnails are
centre-cropped to 4:3 — they show the exact same area the grid already displays,
without carrying the pixels that would be cropped off. The grid serves
thumb-sm/thumb via srcset (1x/2x); the lightbox uses the full-aspect web copy.

Output is always WebP with a lowercase .webp extension regardless of the source
extension or its case, so IMG_0001.JPG and IMG_0002.png both become <name>.webp.

Re-run it whenever you add new photos. Requires Pillow:  pip install pillow
"""
import os
from PIL import Image, ImageOps

SRC = "assets/images"
GRID_RATIO = 4 / 3  # card-media aspect (width / height)
# dir, long edge, quality, crop-to-4:3
TIERS = [("web", 1600, 78, False), ("thumb", 800, 72, True), ("thumb-sm", 400, 75, True)]
EXTS = {".jpg", ".jpeg", ".png", ".webp"}  # matched case-insensitively


def crop_4_3(im):
    w, h = im.size
    if w / h > GRID_RATIO:            # too wide -> trim the sides
        nw = round(h * GRID_RATIO)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = round(w / GRID_RATIO)        # too tall -> trim top/bottom
    y = (h - nh) // 2
    return im.crop((0, y, w, y + nh))


def save(im, path, long_edge, quality, crop):
    if crop:
        im = crop_4_3(im)
    w, h = im.size
    scale = min(1.0, long_edge / max(w, h))
    if scale < 1.0:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    im.convert("RGB").save(path, "WEBP", quality=quality, method=6)


def main():
    for d, _, _, _ in TIERS:
        os.makedirs(os.path.join(SRC, d), exist_ok=True)

    files = sorted(
        os.path.join(SRC, n) for n in os.listdir(SRC)
        if os.path.isfile(os.path.join(SRC, n))
        and os.path.splitext(n)[1].lower() in EXTS
    )

    if not files:
        print("No source images found in", SRC)
        return

    for f in files:
        name = os.path.splitext(os.path.basename(f))[0] + ".webp"  # always WebP output
        im = ImageOps.exif_transpose(Image.open(f))  # honor iPhone rotation
        for d, edge, q, crop in TIERS:
            save(im.copy(), os.path.join(SRC, d, name), edge, q, crop)
        print("optimized", os.path.basename(f), "->", name)

    print(f"\nDone — {len(files)} image(s) -> " + ", ".join(SRC + "/" + d for d, _, _, _ in TIERS))


if __name__ == "__main__":
    main()
