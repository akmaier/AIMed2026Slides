#!/usr/bin/env python3
"""Render strict black-and-white QR codes for the slide deck.

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

FIG = Path(__file__).parent / "output_tex" / "figures" / "talk"
QR_CODES = [
    # closing slide: this branch on GitHub
    ("https://github.com/akmaier/AIMed2026Slides/tree/bvb-verbundkonferenz-2026",
     FIG / "qr_github.png"),
    # nursing-interviews slide: the live demonstrator
    ("https://akmaier.github.io/German-nursing-interviews/",
     FIG / "qr_nursing_demo.png"),
]


def render(url: str, output: Path) -> None:
    qr = qrcode.QRCode(
        version=None,             # auto-pick smallest version that fits
        error_correction=ERROR_CORRECT_M,
        box_size=20,              # px per module -> ~stable when scaled in beamer
        border=2,                 # quiet zone (modules)
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("1")
    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output, format="PNG", optimize=True)

    print(f"Wrote {output} ({output.stat().st_size} bytes, "
          f"{img.size[0]}x{img.size[1]} px, mode={img.mode}) -> {url}")


def main() -> None:
    for url, output in QR_CODES:
        render(url, output)


if __name__ == "__main__":
    main()
