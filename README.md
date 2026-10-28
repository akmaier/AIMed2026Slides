# Pattern Recognition Lab – A short introduction — West China Hospital, International Office (October 2026)

Slides (English, with the **Chinese translation of every slide title as its
subheading**) for Andreas Maier's introduction of the Pattern Recognition Lab
and the FAU Profile Center Medical Engineering to the **International Office of
West China Hospital** (华西医院), Chengdu, October 2026.

This is the `west-china-collaboration-2026` branch ("West China Collaboration
2026"; git branch names cannot contain spaces). It is the deck shown at the
Bavarian State Parliament (`PRL_7min_landtag.pptx`, 14/15 October 2026) with
two more Profile Center slides from `BrainLab_maier.pptx`, recreated in TeX:

| # | Slide | Chinese subheading | Source |
|---|---|---|---|
| 1 | Pattern Recognition Lab – A short introduction | 模式识别实验室简介 | Landtag 1 |
| 2 | About the Speaker | 主讲人简介 | Landtag 2 |
| 3 | Profile Center FAU MT | FAU医学工程重点研究中心 | Landtag 3 |
| 4 | Strategic Goals | 战略目标 | **BrainLab 3** |
| 5 | Collaboration Building – Our strategy | 合作网络建设：我们的策略 | Landtag 4 |
| 6 | Transforming Healthcare with Multimodal AI (SFB/CRC) | 合作研究中心：以多模态人工智能变革医疗 | **BrainLab 5** |
| 7 | Pattern Recognition Lab (team photo) | 模式识别实验室 | Landtag 5 |
| 8 | Know the Past to Understand the Future | 温故而知新 | Landtag 6 |
| 9 | Our Team Today | 我们的团队 | Landtag 7 |
| 10 | Research Areas | 研究方向 | Landtag 8 |
| 11 | Work at the Lab | 实验室的工作 | Landtag 9 |
| 12 | Motion Compensation | 运动补偿 | Landtag 10 |
| 13 | Multi-Organ Segmentation | 多器官分割 | Landtag 11 |
| 14 | 50 Years in a Nutshell | 五十年历程概览 | Landtag 12 |
| 15–16 | What is agentic AI? (Textbook) | 什么是智能体AI？ | Landtag 13–14 |
| 17 | Publishing, Disrupted | 出版业的变革 | Landtag 15 |
| 18–19 | Speed of Agentic AI | 智能体AI的速度 | Landtag 16–17 |
| 20 | NHR @ FAU – Equipment Snapshot | NHR@FAU高性能计算中心：设备概览 | Landtag 18 |
| 21 | Foundation models | 基础模型 | Landtag 19 |
| 22 | Cooperations | 合作伙伴 | Landtag 20 |
| 23 | References | 参考文献 | Landtag 21 |
| 24 | Thank you! (QR code to this branch) | 谢谢！ | closing slide of the LaTeX decks |

The BrainLab deck's other opening slides (title, Profile Center divider,
Collaboration Building, team photo, history, team, research areas, work at the
lab) were already in the Landtag deck. The Landtag deck's text was already
English; what was German were the footer ("Technische Fakultät" → "Faculty of
Engineering") and the dates ("14. Oktober 2026" → "October 2026").

## The deck

The deck is **typeset in LaTeX** on the FAU beamer template: `output_tex/main.tex`
→ `output_tex/main.pdf` (24 pages). Every slide is a beamer frame, including the
ones that were native PowerPoint in the sources. Those are recreated in TeX:

* **Recreated as TikZ layouts**, with only photos, portraits and logos as image
  files (`output_tex/figures/wchc/`): Strategic Goals (cards), Collaboration
  Building (the project bubbles), SFB/CRC (boxes, spokespersons, partners), Our
  Team Today, Research Areas, Multi-Organ Segmentation (legend), Cooperations
  (the 29 sites as TikZ stars at the Landtag slide's positions). The Strategic
  Goals and SFB/CRC slides were screenshots of a different template in
  `BrainLab_maier.pptx`; their photos and logos were cropped out of those
  screenshots, everything else is set in TeX.
* **Text slides** (Know the Past, NHR@FAU, the title and section slides) are plain
  beamer.
* The **header** shows the PRL logo on the title and section frames only;
  content frames carry the FAU wordmark alone, so the bilingual titles keep the
  full width (a small change in `styles/beamerouterthemefau.sty`, commented).

`West_China_Collaboration_2026.pptx` is only the container for presenting: each
PDF page as a full-bleed picture, plus the two **animated GIFs** of the Motion
Compensation slide placed exactly on their first-frame stills
(`build_pptx/build_wch_collab.py`, `MOTION_GIFS`; the positions are fixed in
`main.tex`).

## Build

```
cd output_tex && xelatex main.tex && xelatex main.tex && cd ..
python3 build_pptx/build_wch_collab.py
cp build_pptx/West_China_Collaboration_2026.pptx .
```

`main.tex` needs **XeLaTeX** (xeCJK; Songti SC / Heiti SC from macOS) and two runs
(remember-picture overlays). Chinese text is set by xeCJK in Heiti SC.

Other versions of the deck: `wch-80-years-orthopedics` (bilingual EN/中文,
West China Hospital orthopedics, May 2026), `main` (AIMed 2026, Kraków),
`dldxhealth-2026`, `india-talk`, `de-msd-senso`, `gdlh-gesundheitsdaten-2026`,
`robotics-ai-hackathon-2026`, `puls-retreat-2026`, `visual-heritage-2026`,
`baiosphere-medical-2026-opening` / `-closing`.
