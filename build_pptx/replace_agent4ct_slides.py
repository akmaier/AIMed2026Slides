#!/usr/bin/env python3
"""Replace the three English Agent4CT slides in the committed PowerPoint
deck with the German renders produced by the updated `main.tex`.

The presentation has been hand-edited (videos, animated GIFs, high-quality
overlays), so we do NOT regenerate the whole file via `build_pptx.py`.
Instead we surgically swap out the three rasterised page images that
back the Agent4CT slides:

  pptx slide 46  ->  ppt/media/image51.png   (Agent4CT, page 1)
  pptx slide 47  ->  ppt/media/image52.png   (Agent4CT, page 2)
  pptx slide 48  ->  ppt/media/image53.png   (Agent4CT, page 3)

The German versions live on the corresponding PDF pages of the freshly
compiled `output_tex/main.pdf` (frames 41, 42, 43 in the de-msd-senso
deck, which expand to pages 44, 45, 46 of the PDF when the five overlay
sub-pages from earlier frames are counted).

Workflow:
  1. Compile output_tex/main.tex (separately, with pdflatex).
  2. Run this script:  python3 build_pptx/replace_agent4ct_slides.py
  3. The script writes a new pptx next to the original with the
     `.de-agent4ct.pptx` suffix. Inspect it, then mv it over the
     committed copy when you are happy.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "output_tex" / "main.pdf"
PPTX_IN = ROOT / "AIMed2026_What_next_in_medical_AI.pptx"
PPTX_OUT = ROOT / "AIMed2026_What_next_in_medical_AI.de-agent4ct.pptx"

# Which PDF pages back the German Agent4CT slides, and which file inside
# the pptx they should overwrite.  Page numbers below are 1-based and
# reflect the layout of the updated main.tex (4 \pause frames + 1
# \only-overlay frame before Agent4CT  =>  Agent4CT starts at page 46).
PAGE_TO_IMAGE = {
    46: "image51.png",   # Agent4CT: Alle Deep-Learning-CT-Methoden ...
    47: "image52.png",   # Agent4CT: Vom Paper zum Benchmark
    48: "image53.png",   # Agent4CT: Das Pentathlon
    52: "image57.png",   # Referenzen (re-rendered: +Agent4CT entry, smaller font)
}

# Rasterisation DPI -- matches build_pptx.py / the existing rendered pages
# (200 DPI -> 2667x1500 px on a 13.333x7.5in slide, per README.md).
DPI = 200


def render_page(pdf: Path, page: int, out_png: Path) -> None:
    """Render a single PDF page to PNG.  Tries pdftoppm first, falls back
    to Ghostscript (shipped with MacTeX)."""
    out_png.parent.mkdir(parents=True, exist_ok=True)
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm:
        prefix = out_png.with_suffix("")
        subprocess.run(
            [pdftoppm, "-r", str(DPI), "-f", str(page), "-l", str(page),
             "-png", "-singlefile", str(pdf), str(prefix)],
            check=True,
        )
        return
    gs = shutil.which("gs") or shutil.which("/Library/TeX/texbin/gs")
    if not gs:
        raise SystemExit(
            "Neither `pdftoppm` (from poppler) nor `gs` (Ghostscript) is "
            "on PATH.  Install poppler (`brew install poppler`) or ensure "
            "MacTeX's bin directory is on PATH."
        )
    subprocess.run(
        [gs, "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m",
         f"-r{DPI}", f"-dFirstPage={page}", f"-dLastPage={page}",
         f"-sOutputFile={out_png}", str(pdf)],
        check=True,
    )


def main() -> None:
    if not PDF.exists():
        raise SystemExit(
            f"Missing {PDF}.  Compile output_tex/main.tex with pdflatex "
            "first (run twice for the page-counter footer).")
    if not PPTX_IN.exists():
        raise SystemExit(f"Missing {PPTX_IN}.")

    work = ROOT / "build_pptx" / "_agent4ct_renders"
    work.mkdir(parents=True, exist_ok=True)

    renders: dict[str, Path] = {}
    for page, target_name in PAGE_TO_IMAGE.items():
        png = work / f"page_{page:02d}_{target_name}"
        print(f"Rendering PDF page {page} -> {png.name}")
        render_page(PDF, page, png)
        renders[target_name] = png

    print(f"\nWriting {PPTX_OUT.name}")
    with zipfile.ZipFile(PPTX_IN, "r") as zin, \
         zipfile.ZipFile(PPTX_OUT, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            base = item.filename.rsplit("/", 1)[-1]
            if item.filename.startswith("ppt/media/") and base in renders:
                data = renders[base].read_bytes()
                print(f"  replaced {item.filename}  "
                      f"({len(data):,} bytes)")
            zout.writestr(item, data)

    print(f"\nDone.  Review {PPTX_OUT}, then:")
    print(f"  mv '{PPTX_OUT}' '{PPTX_IN}'")


if __name__ == "__main__":
    main()
