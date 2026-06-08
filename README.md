# BAIOSPHERE MEDICAL 2026 — Opening

Slides for the **Opening / Welcome** of [BAIOSPHERE MEDICAL
2026](https://baiomed.fau.de), held in Erlangen, Germany on
**8–9 June 2026**.  Presented by Andreas Maier (FAU
Erlangen-N&#252;rnberg) on behalf of the editors and the organising
committee.

This is the `baiosphere-medical-2026-opening` branch.

The deck walks the audience through the story of the meeting (an
idea at ECR Vienna in March 2026, three months to the event), the
programme statistics (106 submissions, 93 accepted, ~350 authors
across three continents), the four keynote lectures, the Best
Scientific Contribution Award candidates, the two venues, the
program at a glance, the conference dinner at *Entla’s Keller*, a
short note that the Book of Abstracts was itself assembled with
the help of agentic AI, and thanks to the sponsors **Siemens
Healthineers**, **Medical Valley EMN e.V.** and the **German
Society for AI in Medicine (KImed)**.

Other versions of the slide template:

* `main` — *“What next in medical AI?”* (AIMed 2026, Krak&#243;w).
* `de-msd-senso` — *„KI in der Onkologie“* (MSD Senso-Abend, Munich).
* `india-talk` — *“Towards Bringing Agentic AI to Healthcare”* (Bangalore).
* `wch-80-years-orthopedics` — bilingual EN/中文 deck for the West
  China Hospital orthopedics 80th anniversary.

The compiled deck is `output_tex/main.pdf` (14 slides). Source is
`output_tex/main.tex`, built against the FAU beamer template (the
`styles/`, `template-art/` and `conf-art/` directories are checked in
under `output_tex/`).

## Build

The deck is plain English, so a standard pdflatex build is enough:

```
cd output_tex
pdflatex main.tex
pdflatex main.tex
```

Two passes settle the page counter in the footer. The deck is
self-contained: no external CJK fonts, no `animate` package, no
extracted frame sequences.

## PowerPoint variant

`AIMed2026_What_next_in_medical_AI.pptx` at the repo root is a
14-slide PowerPoint conversion of the PDF (each PDF page is
rasterised at 200 DPI and dropped as a full-bleed picture onto a
16:9 slide). This deck has no animated panels, so no GIF overlays
are embedded — the script's overlay table (`TARGETS` in
`build_pptx/build_pptx.py`) is empty for this branch.

To regenerate from scratch:

```
# rebuild the PDF first if you edited main.tex
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r200 \
   -sOutputFile=build_pptx/pages/page-%02d.png output_tex/main.pdf
python3 build_pptx/build_pptx.py
cp build_pptx/AIMed2026_What_next_in_medical_AI.pptx \
   AIMed2026_What_next_in_medical_AI.pptx
```

## Contents

* `output_tex/main.tex` — LaTeX source
* `output_tex/main.pdf` — compiled deck (14 slides)
* `AIMed2026_What_next_in_medical_AI.pptx` — PowerPoint variant
* `output_tex/figures/baiomed_logo.jpg` — BAIOSPHERE MEDICAL logo
  (from baiomed.fau.de)
* `output_tex/figures/medical_valley_logo.png` — sponsor logo
  (Medical Valley EMN e.V.)
* `output_tex/styles/`, `output_tex/template-art/`,
  `output_tex/conf-art/` — FAU beamer template
* `build_pptx/build_pptx.py` — PDF-to-PowerPoint converter
* `build_pptx/probe_layout.py` — diagnostic for finding the FAU
  theme's body region on a rasterised page

## Theme tweak on this branch

The FAU outer theme's frametitle box width was widened from
`0.565` to `0.80` of the slide width
(`output_tex/styles/beamerouterthemefau.sty`, param #9 of
`frametitle default`). Since this deck uses no additional logos in
the title strip beyond the standard FAU wordmark, longer titles
now fit on a single line.

## Links

* BAIOSPHERE MEDICAL 2026: <https://baiomed.fau.de>
* Programme at a glance: <https://baiomed.fau.de/program-at-a-glance/>
* Medical Valley EMN e.V.: <https://www.medical-valley-emn.de>
