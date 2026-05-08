#!/usr/bin/env python3
"""Diagnostic: figure out which y-bands on the rasterized page contain
the static image vs. the surrounding theme chrome (logos, footer)."""
from PIL import Image
import numpy as np
import sys

PAGE = sys.argv[1] if len(sys.argv) > 1 else (
    "/Users/maier/Documents/code/AIMedMaier/build_pptx/pages/page-25.png"
)
im = np.array(Image.open(PAGE))
H, W = im.shape[:2]
print(f"Page size: {W}x{H}")
gray = im[..., :3].mean(axis=2)
mask = gray < 240

bands = [(0, 0.18), (0.18, 0.22), (0.22, 0.25), (0.25, 0.30),
         (0.30, 0.92), (0.92, 0.95), (0.95, 1.00)]
for top, bot in bands:
    r0, r1 = int(H * top), int(H * bot)
    band = mask[r0:r1, :]
    cols = np.any(band, axis=0)
    if cols.any():
        c0, c1 = np.where(cols)[0][[0, -1]]
        rows_with_content = int(np.any(band, axis=1).sum())
        print(f"y {top:.2f}-{bot:.2f}: cols {c0/W:.3f}..{c1/W:.3f}  "
              f"({rows_with_content} non-empty rows)")
    else:
        print(f"y {top:.2f}-{bot:.2f}: empty")
