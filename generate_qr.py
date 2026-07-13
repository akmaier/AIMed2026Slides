#!/usr/bin/env python3
"""Render a strict black-and-white QR code for the slide deck.

Replaces the inline LaTeX `qrcode` package call on the Thank-you slide so
the QR is a pre-rendered raster image rather than something the LaTeX
engine has to lay out.  Pure black modules on a pure white background, no
anti-aliasing, error-correction level M (matches the previous LaTeX
parameters).
"""

from __future__ import annotations

from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M

# (url, output filename in output_tex/figures/)
TARGETS = [
    ("https://github.com/akmaier/AIMed2026Slides/tree/bacai-vibe-coding",
     "qr_github.png"),
    ("https://faubox.rrze.uni-erlangen.de/getlink/fi23C1i8prL7K57xaTsZGS/book_build.pdf",
     "qr_book.png"),
]

FIG_DIR = Path(__file__).parent / "output_tex" / "figures"


def render_qr(url: str, out_path: Path) -> None:
    qr = qrcode.QRCode(
        version=None,             # auto-pick smallest version that fits
        error_correction=ERROR_CORRECT_M,
        box_size=20,              # px per module -> ~stable when scaled in beamer
        border=2,                 # quiet zone (modules)
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("1")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)

    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes, "
          f"{img.size[0]}x{img.size[1]} px, mode={img.mode})")


def main() -> None:
    for url, name in TARGETS:
        render_qr(url, FIG_DIR / name)


if __name__ == "__main__":
    main()
