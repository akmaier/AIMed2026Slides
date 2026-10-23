#!/usr/bin/env python3
"""Convert the rendered PDF deck to a PowerPoint, embedding animated GIFs
on the three "What is agentic AI?" attempt slides.

For every PDF page we add a full-bleed picture of the rasterized page.
On pages 22/23/24 we additionally drop the source GIF on top of the
static PNG so PowerPoint shows the animation in slideshow mode.

The GIF placement matches the static image's bounding box on the
rasterized page exactly:

  1. Find the bbox of non-white content inside the source PNG file
     (the 1200x1200 image has whitespace around the matplotlib figure).
  2. Find the bbox of non-white content inside the rasterized page's
     body region (skipping header & footer).
  3. The ratio between the two gives the on-slide scale factor; from
     that we recover the full 1200x1200 placement rectangle and put the
     GIF there. Since GIF and PNG are the same size and layout, the
     GIF aligns pixel-for-pixel with the static image.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Emu

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "output_tex" / "main.pdf"
FIG_DIR = ROOT / "output_tex" / "figures"
PAGES_DIR = ROOT / "build_pptx" / "pages"
# Write the regenerated deck *inside* build_pptx/ so we never clobber
# the manually-edited committed copy at the repo root.
OUT = ROOT / "build_pptx" / "Gesundheitsdaten_Innovationsmotor_GDLH_2026.pptx"

# Slide-page -> (gif filename, source png filename).  The GDLH deck has
# no animated slides, so nothing is overlaid.
TARGETS: dict[int, tuple[str, str]] = {}

# Slide-page -> (mp4 filename, poster png, x-range of the page to search for
# the video still, as fractions of the page width).  The still is located as
# the dense dark rectangle in that range, so text elsewhere on the slide
# does not disturb the placement.  The video is embedded on top of it and
# set to start automatically and loop.  No video slides in the GDLH deck.
MOVIES: dict[int, tuple[str, str, tuple[float, float]]] = {}

# Body region of an FAU-themed slide (fractions of page height).
# Tightened to skip the title bar / logos (top) and footer (bottom);
# determined empirically from probe_layout.py on a target page.
BODY_TOP_FRAC = 0.22
BODY_BOT_FRAC = 0.95


def content_bbox(arr: np.ndarray, white_threshold: int = 240) -> tuple[int, int, int, int] | None:
    """(xmin, ymin, xmax, ymax) of pixels darker than `white_threshold`."""
    if arr.ndim == 3:
        # Handle RGBA: treat fully transparent as white
        if arr.shape[2] == 4:
            rgb = arr[..., :3].astype(np.float32)
            alpha = arr[..., 3:4].astype(np.float32) / 255.0
            arr = (rgb * alpha + 255 * (1 - alpha)).astype(np.uint8)
        gray = arr.mean(axis=2)
    else:
        gray = arr
    mask = gray < white_threshold
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if not rows.any() or not cols.any():
        return None
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return int(cmin), int(rmin), int(cmax) + 1, int(rmax) + 1


def gif_placement(page_png: Path, source_png: Path,
                  page_w: int, page_h: int) -> tuple[float, float, float, float]:
    """Return (x_frac, y_frac, w_frac, h_frac) for the GIF on the slide,
    in fractions of slide width/height."""
    # Source PNG content bbox (in PNG pixels)
    src = np.array(Image.open(source_png))
    src_h, src_w = src.shape[:2]
    sb = content_bbox(src)
    if sb is None:
        raise RuntimeError(f"No content found in {source_png}")
    sx0, sy0, sx1, sy1 = sb
    src_cw, src_ch = sx1 - sx0, sy1 - sy0

    # Rasterized page: content bbox restricted to the body region
    page = np.array(Image.open(page_png))
    pH, pW = page.shape[:2]
    body_top = int(pH * BODY_TOP_FRAC)
    body_bot = int(pH * BODY_BOT_FRAC)
    pb = content_bbox(page[body_top:body_bot, :])
    if pb is None:
        raise RuntimeError(f"No body content found in {page_png}")
    px0, py0_rel, px1, py1_rel = pb
    py0 = py0_rel + body_top
    py1 = py1_rel + body_top
    page_cw, page_ch = px1 - px0, py1 - py0

    # Scale: rasterized content size / source content size
    scale_w = page_cw / src_cw
    scale_h = page_ch / src_ch

    # Full PNG placement on the rasterized page (in page pixels)
    full_x = px0 - sx0 * scale_w
    full_y = py0 - sy0 * scale_h
    full_w = src_w * scale_w
    full_h = src_h * scale_h

    return full_x / pW, full_y / pH, full_w / pW, full_h / pH


def dark_bbox(page_png: Path, x_range: tuple[float, float],
              dark: int = 128, density: float = 0.3) -> tuple[float, float, float, float]:
    """(x_frac, y_frac, w_frac, h_frac) of the dense dark rectangle (a video
    still on a white slide) inside the body region and the given x-range.
    Rows/columns count as part of it when more than `density` of their
    pixels are darker than `dark`; sparse text never reaches that."""
    page = np.asarray(Image.open(page_png).convert("L"))
    H, W = page.shape
    top, bot = int(H * BODY_TOP_FRAC), int(H * BODY_BOT_FRAC)
    x0, x1 = int(W * x_range[0]), int(W * x_range[1])
    mask = page[top:bot, x0:x1] < dark

    def longest_run(flags: np.ndarray) -> tuple[int, int]:
        # largest contiguous run of True; thin stray bands (text strokes)
        # elsewhere on the slide are ignored
        best, start = (0, -1), None
        for k, f in enumerate(list(flags) + [False]):
            if f and start is None:
                start = k
            elif not f and start is not None:
                if k - start > best[1] - best[0]:
                    best = (start, k)
                start = None
        return best

    r0, r1 = longest_run(mask.mean(axis=1) > density)
    if r1 <= r0:
        raise RuntimeError(f"No video still found in {page_png}")
    c0, c1 = longest_run(mask[r0:r1].mean(axis=0) > density)
    px0, px1 = x0 + c0, x0 + c1
    py0, py1 = top + r0, top + r1
    return px0 / W, py0 / H, (px1 - px0) / W, (py1 - py0) / H


def media_duration_ms(path: Path) -> int:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True).stdout
    return int(round(float(out) * 1000))


def set_autoplay_loop(slide, shape_id: int, dur_ms: int) -> None:
    """Replace python-pptx's click-to-play timing with the structure
    PowerPoint writes for a video set to 'Start: Automatically' and
    'Loop until Stopped'."""
    from lxml import etree
    P = "http://schemas.openxmlformats.org/presentationml/2006/main"
    xml = f"""
<p:timing xmlns:p="{P}">
  <p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>
    <p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>
      <p:par><p:cTn id="3" fill="hold">
        <p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst>
        <p:childTnLst><p:par><p:cTn id="4" fill="hold">
          <p:stCondLst><p:cond delay="0"/></p:stCondLst>
          <p:childTnLst><p:par>
            <p:cTn id="5" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="afterEffect">
              <p:stCondLst><p:cond delay="0"/></p:stCondLst>
              <p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr>
                <p:cTn id="6" dur="{dur_ms}" fill="hold"/>
                <p:tgtEl><p:spTgt spid="{shape_id}"/></p:tgtEl>
              </p:cBhvr></p:cmd></p:childTnLst>
            </p:cTn>
          </p:par></p:childTnLst>
        </p:cTn></p:par></p:childTnLst>
      </p:cTn></p:par>
    </p:childTnLst></p:cTn>
    <p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
    <p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
    </p:seq>
    <p:video><p:cMediaNode vol="80000">
      <p:cTn id="7" repeatCount="indefinite" fill="hold" display="0">
        <p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>
      </p:cTn>
      <p:tgtEl><p:spTgt spid="{shape_id}"/></p:tgtEl>
    </p:cMediaNode></p:video>
  </p:childTnLst></p:cTn></p:par></p:tnLst>
</p:timing>"""
    sld = slide._element
    old = sld.find(f"{{{P}}}timing")
    new = etree.fromstring(xml.strip())
    if old is not None:
        old.addprevious(new)
        sld.remove(old)
    else:
        sld.append(new)


def main() -> None:
    page_files = sorted(PAGES_DIR.glob("page-*.png"))
    if not page_files:
        raise SystemExit(f"No rasterized pages in {PAGES_DIR}; "
                         "run pdftoppm first.")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for i, page_png in enumerate(page_files, start=1):
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(
            str(page_png), 0, 0,
            width=prs.slide_width, height=prs.slide_height,
        )

        if i in TARGETS:
            gif_name, png_name = TARGETS[i]
            with Image.open(page_png) as im:
                pw, ph = im.size
            xf, yf, wf, hf = gif_placement(
                page_png, FIG_DIR / png_name, pw, ph,
            )
            x = int(prs.slide_width * xf)
            y = int(prs.slide_height * yf)
            w = int(prs.slide_width * wf)
            h = int(prs.slide_height * hf)
            slide.shapes.add_picture(
                str(FIG_DIR / gif_name), x, y, width=w, height=h,
            )
            print(f"  page {i}: overlaid {gif_name} "
                  f"x={xf:.4f} y={yf:.4f} w={wf:.4f} h={hf:.4f}")

        if i in MOVIES:
            mp4_name, poster_name, x_range = MOVIES[i]
            xf, yf, wf, hf = dark_bbox(page_png, x_range)
            movie = slide.shapes.add_movie(
                str(FIG_DIR / mp4_name),
                int(prs.slide_width * xf), int(prs.slide_height * yf),
                int(prs.slide_width * wf), int(prs.slide_height * hf),
                poster_frame_image=str(FIG_DIR / poster_name),
                mime_type="video/mp4",
            )
            set_autoplay_loop(slide, movie.shape_id,
                              media_duration_ms(FIG_DIR / mp4_name))
            print(f"  page {i}: embedded {mp4_name} (autoplay, loop) "
                  f"x={xf:.4f} y={yf:.4f} w={wf:.4f} h={hf:.4f}")

    prs.save(str(OUT))
    print(f"\nWrote {OUT} ({OUT.stat().st_size:,} bytes, "
          f"{len(page_files)} slides)")


if __name__ == "__main__":
    main()
