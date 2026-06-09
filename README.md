# BAIOSPHERE MEDICAL 2026 — Closing Remarks

Short closing deck for [BAIOSPHERE MEDICAL
2026](https://baiomed.fau.de), Erlangen, **9 June 2026** (end of
Day 2). Presented by Siming Bayer and Andreas Maier
(FAU Erlangen-N&#252;rnberg).

This is the `baiosphere-medical-2026-closing` branch.

Four slides:

1. **Title** — BAIOMED banner, presenters, date.
2. **Thank you to our keynote speakers** — Alejandro F. Frangi,
   Mengyun Qiao, Nils D. Forkert, Lyu Su.
3. **Thank you to our team** — organising team, editors and
   co-chairs, program committee and reviewers, award committee,
   student helpers.
4. **Thank you to all of you** — speakers, authors, participants
   — plus the practical reminder: conference dinner, bus transfer
   at **18:15**.

PDF only on this branch — the opening deck's tracked PPTX file
has been dropped (it would have been stale here).

Other versions of the slide template:

* `main` — *“What next in medical AI?”* (AIMed 2026, Krak&#243;w).
* `de-msd-senso` — *„KI in der Onkologie“* (MSD Senso-Abend, Munich).
* `india-talk` — *“Towards Bringing Agentic AI to Healthcare”* (Bangalore).
* `wch-80-years-orthopedics` — bilingual EN/中文 deck for the West
  China Hospital orthopedics 80th anniversary.
* `baiosphere-medical-2026-opening` — the opening companion to this
  closing deck.

The compiled deck is `output_tex/main.pdf` (4 slides). Source is
`output_tex/main.tex`, built against the FAU beamer template.

## Build

Plain English deck, standard pdflatex:

```
cd output_tex
pdflatex main.tex
pdflatex main.tex
```

Two passes settle the page counter in the footer.

## Contents

* `output_tex/main.tex` — LaTeX source
* `output_tex/main.pdf` — compiled deck (4 slides)
* `output_tex/figures/baiomed_logo.jpg` — BAIOSPHERE MEDICAL logo
  (from baiomed.fau.de)
* `output_tex/styles/`, `output_tex/template-art/`,
  `output_tex/conf-art/` — FAU beamer template

## Links

* BAIOSPHERE MEDICAL 2026: <https://baiomed.fau.de>
* Programme at a glance: <https://baiomed.fau.de/program-at-a-glance/>
