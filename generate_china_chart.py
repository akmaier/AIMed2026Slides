#!/usr/bin/env python3
"""Render the China-share chart for the GDLH deck in the FAU template colours.

Data: github.com/akmaier/ConferenceStats, output/country_overview_all_papers.md
(share of accepted papers with at least one author from China; denominator =
all accepted papers, i.e. the conservative lower bound).  AAAI is highlighted
in FAUBlue, the other conferences are drawn in TechMetallic and identified by
direct labels at the end of each line.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUTPUT = Path(__file__).parent / "output_tex" / "figures" / "china_share_de.png"

# FAU template colours (output_tex/styles/fau-colors.sty)
FAU_BLUE = "#002F6C"          # FAUBlue        RGB(0, 47, 108)
TECH_METALLIC = "#779FB5"     # TechMetallic   RGB(119, 159, 181)
TECH_DARK = "#41748D"         # TechDarkMetallic RGB(65, 116, 141)
INK = "#1A1A1A"
INK_MUTED = "#4D4D4D"
GRID = "#DDE7ED"              # TechMetallic at ~12.5 % on white

YEARS = list(range(2015, 2026))
SHARE = {  # percent, None = conference not held that year
    "AAAI":    [20.86, 25.30, 30.07, 34.57, 39.09, 43.24, 40.10, 41.77, 52.79, 59.78, 64.83],
    "CVPR":    [19.93, 21.15, 24.39, 30.64, 38.72, 41.20, 41.75, 44.94, 47.26, 47.79, 52.84],
    "ECCV":    [None, 3.86, None, 2.70, None, 17.85, None, 23.85, None, 23.66, None],
    "ICCV":    [21.86, None, 30.27, None, 35.72, None, 39.58, None, 48.24, None, 54.46],
    "ICML":    [7.78, 6.52, 7.37, 9.18, 8.28, 10.15, 13.44, 18.65, 18.87, 27.74, 34.56],
    "NeurIPS": [3.97, 6.51, 8.55, 13.19, 12.19, 13.33, 18.25, 23.82, 25.73, 33.63, 38.98],
}
HIGHLIGHT = "AAAI"
# vertical nudges (percentage points) so end labels do not collide
LABEL_NUDGE = {"ICCV": 2.2, "CVPR": -2.2, "NeurIPS": 1.4, "ICML": -1.4}


def pick_font() -> str:
    for name in ("Helvetica", "Arial", "Liberation Sans", "DejaVu Sans"):
        try:
            font_manager.findfont(name, fallback_to_default=False)
            return name
        except ValueError:
            continue
    return "sans-serif"


def main() -> None:
    plt.rcParams.update({
        "font.family": pick_font(),
        "font.size": 21,
        "axes.edgecolor": TECH_METALLIC,
        "axes.labelcolor": INK_MUTED,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
    })
    fig, ax = plt.subplots(figsize=(10.5, 5.6), dpi=200)

    order = [k for k in SHARE if k != HIGHLIGHT] + [HIGHLIGHT]   # highlight on top
    for conf in order:
        pts = [(y, v) for y, v in zip(YEARS, SHARE[conf]) if v is not None]
        xs, ys = zip(*pts)
        hi = conf == HIGHLIGHT
        ax.plot(xs, ys, color=FAU_BLUE if hi else TECH_METALLIC,
                linewidth=3.5 if hi else 2.0, marker="o",
                markersize=8 if hi else 6, markeredgecolor="white",
                markeredgewidth=1.5, zorder=3 if hi else 2,
                solid_capstyle="round")
        x_end, y_end = xs[-1], ys[-1]
        ax.annotate(f"{conf}  {y_end:.0f} %",
                    xy=(x_end, y_end),
                    xytext=(10, LABEL_NUDGE.get(conf, 0.0) * 6.5),
                    textcoords="offset points", va="center", ha="left",
                    fontsize=22, color=INK if hi else INK_MUTED,
                    fontweight="bold" if hi else "normal")

    ax.set_xlim(2014.6, 2025.4)
    ax.set_ylim(0, 70)
    ax.set_xticks(YEARS)
    ax.set_xticklabels([str(y) if y % 2 == 1 else "" for y in YEARS])
    ax.set_yticks(range(0, 71, 10))
    ax.set_yticklabels([f"{v} %" for v in range(0, 71, 10)])
    ax.set_ylabel("Paper mit Beteiligung aus China")
    ax.grid(axis="y", color=GRID, linewidth=1.0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", length=4, color=TECH_METALLIC)

    fig.tight_layout()
    fig.subplots_adjust(right=0.80)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, facecolor="white")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
