# Zukunft von KI in Big Data — Mamma-Symposium Ostsachsen 2026

Folien zum Closing-Talk **„Zukunft von KI in Big Data — Einfluss auf
Arbeitsabläufe"** von Andreas Maier (FAU Erlangen-Nürnberg) auf dem
**Mamma-Symposium des Brustzentrums Ostsachsen** (Klinikum Oberlausitzer
Bergland) — **Freitag, 27. November 2026, 16:20–17:00, online**
(Vor-Ort-Veranstaltung Taubenheim/Spree, Haus Oberlausitz, 13:45–18:00).
Eingeladen von Christin Keßner, organisatorische Leitung Brustzentrum
Zittau. Publikum: Klinikerinnen und Kliniker verschiedener Fachrichtungen.

Branch `mamma-ostsachsen-2026`, geforkt von `bvb-verbundkonferenz-2026`.
Gegenüber der BVB-Keynote:

* **Entfernt** (für klinisches Publikum nicht relevant): Herz-CT-Bewegungs-
  kompensation, VesselROVER (Koronar-Angiographie), die vier
  „Fast alles ist jetzt einfach…"-Folien (ConferenceStats), die
  Publikationswesen-/Agent4CT-/Living-PRISMA-Folien, zwei Vibe-Coding-
  Unterfolien.
* **Konsolidiert**: die beiden Pflegeinterview-Folien sind zu einer
  zusammengezogen (Workflow + Kernzahlen auf einer Folie).
* **Neu ergänzt**: zwei PRAEGNANT-Folien aus `de-msd-senso` (multimodale
  Datenintegration in der Onkologie + Generieren → Verifizieren →
  Falsifizieren-Loop am Beispiel [PRAEGNANT](https://praegnant.org)).
  Eine neue Abschluss-Folie *„Einfluss auf Arbeitsabläufe"* mit
  konkreten Effekten im Brustzentrum (Tumorboard-Vorbereitung,
  Studien-Matching, Dokumentation & Arztbrief, Zweitmeinung).
* **Angepasst an klinisches Publikum**: *„Medizin im Agententempo –
  Chancen und Risiken"* (zuvor „Wissenschaft im Agententempo") und
  *„Was das für die klinische Arbeit bedeutet – fünf Regeln"*.

Die drei Spin-Echo-EPI-Demovideos (Mensch / GPT-4o / GROK-3-think) bleiben
als animierte GIFs in der PowerPoint erhalten; in der PDF werden sie als
Standbilder gezeigt.

Andere Varianten dieses Foliensatzes: `main` (AIMed 2026, Kraków),
`india-talk` (Bangalore), `de-msd-senso` (MSD Senso-Abend, München),
`dldxhealth-2026` (DLDxHealth, München),
`bvb-verbundkonferenz-2026` (BVB-Keynote, München), `bacai-vibe-coding`
(Bamberg), `gdlh-gesundheitsdaten-2026`, `puls-retreat-2026`,
`visual-heritage-2026`, `shenkang-prl-visit-2026`,
`shanghai-sino-euro-2026`, `wch-radiology-summit-2026`,
`wch-80-years-orthopedics`, `west-china-collaboration-2026`,
`baiosphere-medical-2026-opening` / `…-closing`,
`robotics-ai-hackathon-2026`.

## Build

Der Foliensatz wird in LaTeX gesetzt; die PowerPoint ist nur der Container
fürs Präsentieren und für die animierten GIFs. pdflatex mit ngerman-babel.

```
cd output_tex
pdflatex main.tex && pdflatex main.tex    # zweimal: remember-picture-Overlays
cd ..
python3 build_pptx/build_pptx.py          # PDF-Seiten @200 dpi + GIF-Overlays
cp build_pptx/KI_in_Big_Data_Mamma_Ostsachsen_2026.pptx .
```

`build_pptx.py` erkennt die GIF-Folien an ihrem (deutschen) Untertitel,
Folien können also ohne Nacharbeit umsortiert werden. Die beiden QR-Codes
werden von `generate_qr.py` erzeugt (`output_tex/figures/talk/qr_github.png`
für den Slides-Branch, `output_tex/figures/talk/qr_nursing_demo.png` für
den Live-Demonstrator der Pflegeinterviews).

## Inhalt

* `output_tex/main.tex` — LaTeX-Quelle (ngerman)
* `output_tex/main.pdf` — fertiges Deck (51 Folien)
* `KI_in_Big_Data_Mamma_Ostsachsen_2026.pptx` — PowerPoint mit eingebetteten
  Spin-Echo-EPI-GIFs auf den Folien *„Mensch als Referenz"*,
  *„Versuch von GPT-4o"* und *„Versuch von GROK-3-think"*
* `output_tex/figures/` + `output_tex/figures/talk/` — Grafiken, QR-Codes,
  GIFs und Fotos
* `output_tex/styles/`, `output_tex/template-art/`, `output_tex/conf-art/`
  — vendorte FAU-Beamer-Vorlage
* `generate_qr.py` — QR-Erzeugung (beide QRs)
* `build_pptx/build_pptx.py` — PDF → PowerPoint + GIF-Overlays
