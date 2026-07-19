#!/usr/bin/env python3
"""
Optimize item photos for a sale-catalog site. Run it from a sale repo's root.

Reads every image in assets/images/ (top level) and writes two resized,
EXIF-rotation-corrected copies:

    assets/images/web/<name>    ~1600px long edge  (fullscreen gallery)
    assets/images/thumb/<name>  ~800px  long edge  (card thumbnails)

Re-run it whenever you add new photos. Requires Pillow:  pip install pillow
"""
import glob
import os
from PIL import Image, ImageOps

SRC = "assets/images"
WEB_EDGE, WEB_Q = 1600, 82
THUMB_EDGE, THUMB_Q = 800, 78
EXTS = ("*.jpg", "*.jpeg", "*.png", "*.webp")


def save(im, path, long_edge, quality):
    w, h = im.size
    scale = min(1.0, long_edge / max(w, h))
    if scale < 1.0:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    im.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def main():
    os.makedirs(os.path.join(SRC, "web"), exist_ok=True)
    os.makedirs(os.path.join(SRC, "thumb"), exist_ok=True)

    files = []
    for pat in EXTS:
        files += glob.glob(os.path.join(SRC, pat))
    files = sorted(set(files))

    if not files:
        print("No source images found in", SRC)
        return

    for f in files:
        name = os.path.basename(f)
        im = ImageOps.exif_transpose(Image.open(f))  # honor iPhone rotation
        save(im.copy(), os.path.join(SRC, "web", name), WEB_EDGE, WEB_Q)
        save(im.copy(), os.path.join(SRC, "thumb", name), THUMB_EDGE, THUMB_Q)
        print("optimized", name)

    print(f"\nDone — {len(files)} image(s) -> {SRC}/web and {SRC}/thumb")


if __name__ == "__main__":
    main()
