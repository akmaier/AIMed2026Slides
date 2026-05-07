# Slide Check Report

LaTeX conversion of `Besonderer Vortrag Maier.pptx` into the FAU beamer template.
Output: `output_tex/main.tex` -> `output_tex/main.pdf` (46 pages).

The original PPT used a non-standard 25.98 in x 5.51 in canvas with
2-4 animation panels per slide laid out side-by-side. Each panel was
extracted into a separate beamer frame (16:9), so 16 PPT slides became
**46 LaTeX frames**.

The deck has been **fully translated to English**, retitled
"What next in medical AI?", and reauthored under Andreas Maier alone for
the AIMed 2026 conference (Krak&#243;w, 7-9 May 2026).

## Frame map (PPT -> LaTeX, with English titles)

| PPT # | English title                       | LaTeX frames | Notes |
|------:|-------------------------------------|:-----------:|-------|
| 1     | What next in medical AI?            | 1 (title)   | AIMed logo + conference info, plain `[t]` layout |
| 2     | Outline                             | 3           | Plain TOC + 2 highlighted-bullet variants with companion image |
| 3     | Section: What is deep learning?     | 1 (title)   | Section divider |
| 4     | Deep learning                       | 4           | WER chart, Top-5 chart, Atari games, AlphaGo |
| 5     | Generative AI                       | 4           | Source photo, prompt-description, generation, style variants |
| 6     | Deep learning in medicine           | 4           | Segmentation, reconstruction, MRI variational network, Nobel laureates |
| 7     | Section: What is agentic AI?        | 1 (title)   | Section divider |
| 8     | What is agentic AI?                 | 3           | Question, long answer, LLM-with-tools (was 4 panels in PPT, two merged) |
| 9     | Spin-echo EPI code                  | 4           | Task definition + **3 animated frames** (Human, GPT-4o, GROK-3-think) |
| 10    | LLM vs. Agent4MR                    | 4           | Pipeline, interactions, costs, iterative results |
| 11    | Adaptive use cases                  | 3           | Adaptive system, sketch->diagram, patient information |
| 12    | Vibe coding / advanced techniques   | 4           | Vibe coding, AI techniques, quality gates, textbook |
| 13    | Section: What is coming next?       | 1 (title)   | Section divider |
| 14    | Almost everything is easy now...    | 4           | China, conferences, workflow, country share |
| 15    | Foundation models                   | 4           | Bavarian foundation, multimodal, voice/emotion, knowledge |
| 16    | Thank you!                          | 1           | Centered QR code linking to https://github.com/akmaier/AIMed2026Slides |

## Title and thank-you slides

- **Title slide** (frame 1) is a custom plain `[t]` frame -- it embeds the
  official AIMed 2026 banner logo (`figures/aimed_logo.pdf`, fetched from
  the conference website), the talk title, subtitle "From code to clinic",
  the speaker, the affiliation, and the conference dates/venue. It avoids
  the FAU `titleimage` wave artwork, which had previously collided with
  the logo.

- **Thank-you slide** (frame 46) renders a vector QR code via the
  `qrcode` LaTeX package pointing to
  `https://github.com/akmaier/AIMed2026Slides`. The QR code is sharp at
  any zoom level (no rasterisation), centered at 5 cm height, with the
  URL printed below in monospaced text.

## GIFs are real animations now

The three Spin-echo EPI screencasts (`img_08_02.gif`, `img_08_03.gif`,
`img_08_04.gif`, ~145 frames each) were previously rasterised to a
single PNG, losing the animation. They are now embedded as proper
beamer animations:

  1. Each GIF is decomposed with `magick foo.gif -coalesce -resize 600x600
     foo/all-%03d.png`.
  2. Every 4th frame is kept (37 frames per animation) and renumbered as
     `frame-0.png ... frame-36.png` under `figures/anim_08_02/`,
     `figures/anim_08_03/`, `figures/anim_08_04/`.
  3. `\animategraphics[autoplay,loop,height=.78\textheight]{12}{anim_08_02/frame-}{0}{36}`
     drives them at 12 fps with autoplay and loop.

This requires a PDF viewer that supports embedded JavaScript animations
(Adobe Reader/Acrobat, pdf-presenter-console, Okular). In other viewers
the first frame is shown statically. The original `.gif` files are kept
on disk under `figures/` for traceability but are no longer referenced
from `main.tex`.

Animation footprint: ~6.4 MB across all three sequences (so the deck
grew from ~22 MB to ~25.7 MB).

## Translation pass (German -> English)

All visible text was translated. Notable choices:

| Section title (DE)               | English                                   |
|----------------------------------|-------------------------------------------|
| Inhaltsverzeichnis               | Outline                                   |
| Was ist Deep Learning?           | What is deep learning?                    |
| Was ist Agentische KI?           | What is agentic AI?                       |
| Was kommt da noch auf uns zu?    | What is coming next?                      |
| Generative KI                    | Generative AI                             |
| Deep Learning in der Medizin     | Deep learning in medicine                 |
| Fast alles ist jetzt einfach...  | Almost everything is easy now...          |
| Basis Modelle                    | Foundation models                         |
| Vielen Dank                      | Thank you!                                |

Sub-titles ("Sprache" -> "Speech", "Bildklassifikation" -> "Image
classification", "Eingangsbild" -> "Source image", etc.) were translated
in line; the math/code line on slide 9 ("Code a spin echo EPI ...") was
already English in the source. Babel's `english` option is now loaded so
hyphenation and punctuation default to British/American conventions.

## Typo / spelling fixes carried over from the German pass

| Where (PPT)        | Original         | Corrected to     | Reason |
|--------------------|------------------|------------------|--------|
| Slide 1 title      | "Zukunft von Kl" | "Zukunft von KI" | "Kl" was OCR-style mis-capitalisation of "KI" (Kuenstliche Intelligenz) |
| Slides 8/10/11/12  | "agentitsche"    | "agentische"     | German typo; correct form is "agentische" |
| Throughout         | smart quotes     | `\textquotedblleft ... \textquotedblright` | Avoids babel-quote / fontenc rendering glitches |
| Slide 5 description| curly apostrophes| straight ASCII   | UTF-8 curly quotes were not in the T1 font |

## Empty / sparse slides addressed

The PPT had three slides whose individual panels were almost empty
(title-only or image-with-mostly-whitespace). These were reworked:

- **PPT 8 panels 1+2** ("Wie faehrt man ein Auto?" + cue text) merged
  into one frame "A simple question" with the question, the cue text
  ("Thought for a few seconds..."), and a short bullet list explaining
  the setup.

- **PPT 9 panel 1** (single italicised prompt line) was expanded to
  "Task for the models": prompt, plus three bullets explaining the task
  and the three contestants.

- **PPT 6 panel 4** (originally just a Nobel-Prize image overlay with no
  text) is now a centered text frame "Hopfield and Hinton -- Nobel Prize
  in Physics 2024" since no usable image survived the panel split.

- The original PowerPoint screenshot `img_07_04.png` was dropped from
  the deck because it was 80% whitespace; its information is inlined as
  text instead.

## Compile status

- Engine: `pdflatex` (TeX Live 2025).
- Result: `main.pdf`, 46 pages, ~25.7 MB, no fatal errors.
- Two passes are needed because the `qrcode` package writes its bitmap
  to `main.aux` on the first pass and reads it back on the second.
- Bibliography is wired up (biber/biblatex) but no citations in deck;
  no biber run required.

## Overfull \\hbox warnings

After build the log contains 229 overfull-hbox messages. They fall in
**two groups**:

### Group A: template-internal, cosmetic (do not appear in any visual frame area)

These come from the FAU beamer outer theme rendering the headline and
the title-slide art. They fire once per frame at the `\begin{frame}`
line and are identical from frame to frame:

| Width    | Count | Source                                  |
|----------|------:|-----------------------------------------|
| 21.69 pt | ~82   | Headline -- "FAU FAU FAU" 3-logo wordmark stacked into the header band. `WordMarkBoxWidth=90mm` is too narrow when 3 logos are placed; padding overflows by ~0.76 cm. Cosmetic only - the band is white over black bar, so the overflow is invisible. |
| 14.05 pt | ~46   | Same mechanism, shorter pass. |
| 2.85 pt  | ~92   | Footline footer line - the institute/title strip is 2.85 pt wider than the page text width at the chosen `scale=1.` setting. Visually unnoticeable. |
| 50.95 pt | 1     | Title-art metrics fired once at the title slide while the wave image is queried (we no longer render it, but the template still measures it). |

These are template-level. To silence them globally one could:

  1. Use `\hfuzz=60pt \vfuzz=60pt` after `\begin{document}` (suppresses
     the warning, output unchanged), **or**
  2. Reduce `WordMarkBoxWidth` to e.g. `82mm` in
     `styles/beamerthemefau.sty` and re-tune the headline metrics. Not
     recommended for a one-off conversion.

### Group B: from converted content

After group A is excluded, **zero** entries are from user content.
All bullet text, math fragments, English captions and quoted strings
fit within their column widths.

## Underfull boxes

`grep "Underfull" main.log` returns 0 -- no underfull warnings.

## Image issues

- Three GIFs (`img_08_02.gif`, `img_08_03.gif`, `img_08_04.gif`) used to
  be flattened to a static PNG; they are now real animations (see "GIFs
  are real animations now" above). The original `.gif` files remain in
  `figures/` for traceability.

- `img_07_04.png` (the chat-screenshot with mostly whitespace) is
  unused in `main.tex` - kept on disk for traceability.

- Several photographs used by the PPT carry a wide aspect ratio and
  are scaled by `height=.78\textheight`. Visual inspection of each
  rendered frame confirms no clipping, no whitespace banner, no
  pixelation at presentation size.

## Per-frame visual check

PDFs were rasterised at 80-200 DPI and inspected. All 46 frames render
with:

  * a populated title bar (frame title or slide-title pair),
  * non-empty content area,
  * no image clipping,
  * no overlapping placeholders.

Section dividers (frames 5, 18, 37) intentionally use the
`[t,title]` colour-bar layout from the template and contain only the
section heading, which is the template-defined behaviour.

## Things that may need a human pass before presenting

1. **Speaker label under photo.** Frame 21 ("From language model to
   agent") labels the head-shot as "Andreas Maier"; the PPT did not
   label it, so confirm.

2. **Sub-titles.** Each content frame carries an English sub-title
   ("Speech", "Image classification", ...). These are inferences from
   the panel content, not present in the PPT - feel free to adjust.

3. **Bibliography.** The template loads `biblatex` and references
   `bibliography.bib` (template's default file). The PPT contained
   inline citations like "[Mnih 2013]", "[Toshev, Szegedy 2014]" as
   image overlays; I kept those as plain caption text inside the
   image. If you'd like real `\cite{...}` entries, populate
   `bibliography.bib` and replace the captions.

4. **Headline visual quirk.** The "FAU FAU FAU" stacked wordmark in
   the top-right is the `Tech` institute headline rendered with the
   default `SecondLogo`/`ThirdLogo` settings inherited from the
   template demo. Adjust `institute=` and the logo options accordingly
   in `main.tex` lines 8-16 if a different faculty.

5. **Animation playback.** `animategraphics` requires a PDF viewer with
   JavaScript support (Adobe Reader/Acrobat, Okular,
   pdf-presenter-console). Built-in viewers in macOS Preview, browsers,
   and many tablets show only the first frame. Mention this when
   sharing the deck or screen-record the animations as MP4 fallback.

## Reproducibility

```
cd output_tex
pdflatex main.tex   # twice for the QR code aux pass
pdflatex main.tex
```

Source artefacts kept under repo root (gitignored, regeneratable from
the `.pptx`):

  * `extract_pptx.py`          -- PPTX -> JSON / images / summary
  * `analyze_layout.py`        -- shape position dump
  * `inspect_clicks.py`        -- animation click-effect listing
  * `check_timing.py`          -- click count per slide
  * `extracted_pptx/`          -- structural extraction
  * `slide_images/slide-NN.png` -- raster of original PPT for reference
  * `Besonderer Vortrag Maier.pptx` -- the source PowerPoint

These are excluded by `.gitignore` so they are never pushed to the
public slides repo.
