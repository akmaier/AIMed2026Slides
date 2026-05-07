# AIMed 2026 Slides

Slides for the talk **"What next in medical AI?"** by Andreas Maier
(FAU Erlangen-N&#252;rnberg) at the
[AIMed 2026](https://my.ebm.one/aimed) conference,
Krak&#243;w, 7-9 May 2026.

The compiled deck is `output_tex/main.pdf` (46 frames). Source is
`output_tex/main.tex`, built against the FAU beamer template (the
`styles/` and `template-art/` directories are vendored under
`output_tex/`).

## Build

```
cd output_tex
pdflatex main.tex
pdflatex main.tex     # second pass for the QR-code aux file
```

Two passes are needed because the QR code on the closing slide is
rendered by the `qrcode` LaTeX package, which writes its bitmap to
`main.aux` on the first pass and reads it back on the second.

For the animations on slides 24-26 (Spin-echo EPI screencasts) the
deck uses `\animategraphics` from the `animate` package; play them in
Adobe Reader/Acrobat, Okular or pdf-presenter-console. Other viewers
fall back to the first frame.

## Contents

* `output_tex/main.tex` -- LaTeX source
* `output_tex/main.pdf` -- compiled deck (also the QR-code target)
* `output_tex/figures/` -- images and per-frame animation sequences
* `output_tex/styles/`, `output_tex/template-art/` -- FAU beamer template
* `slide_check.md` -- typesetting / translation report

The original PowerPoint, the rasterised slide previews and the
`extracted_pptx/` JSON dump are kept locally for traceability but are
excluded from this repository via `.gitignore`.
