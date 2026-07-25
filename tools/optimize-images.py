#!/usr/bin/env python3
"""
Optimize item photos for a sale-catalog site. Run it from a sale repo's root.

Reads every image in assets/images/ (top level, any-case extension) and writes
two resized, EXIF-rotation-corrected JPEG copies:

    assets/images/web/<name>.jpeg    ~1600px long edge  (fullscreen gallery)
    assets/images/thumb/<name>.jpeg  ~800px  long edge  (card thumbnails)

Output is always JPEG with a lowercase .jpeg extension regardless of the source
extension or its case, so IMG_0001.JPG and IMG_0002.png both become <name>.jpeg.

Re-run it whenever you add new photos. Requires Pillow:  pip install pillow
"""
import os
from PIL import Image, ImageOps

SRC = "assets/images"
WEB_EDGE, WEB_Q = 1600, 82
THUMB_EDGE, THUMB_Q = 800, 78
EXTS = {".jpg", ".jpeg", ".png", ".webp"}  # matched case-insensitively


def save(im, path, long_edge, quality):
    w, h = im.size
    scale = min(1.0, long_edge / max(w, h))
    if scale < 1.0:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    im.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def main():
    os.makedirs(os.path.join(SRC, "web"), exist_ok=True)
    os.makedirs(os.path.join(SRC, "thumb"), exist_ok=True)

    files = sorted(
        os.path.join(SRC, n) for n in os.listdir(SRC)
        if os.path.isfile(os.path.join(SRC, n))
        and os.path.splitext(n)[1].lower() in EXTS
    )

    if not files:
        print("No source images found in", SRC)
        return

    for f in files:
        name = os.path.splitext(os.path.basename(f))[0] + ".jpeg"  # always JPEG output
        im = ImageOps.exif_transpose(Image.open(f))  # honor iPhone rotation
        save(im.copy(), os.path.join(SRC, "web", name), WEB_EDGE, WEB_Q)
        save(im.copy(), os.path.join(SRC, "thumb", name), THUMB_EDGE, THUMB_Q)
        print("optimized", os.path.basename(f), "->", name)

    print(f"\nDone — {len(files)} image(s) -> {SRC}/web and {SRC}/thumb")


if __name__ == "__main__":
    main()
