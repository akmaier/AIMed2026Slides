#!/usr/bin/env python3
"""Build West_China_Collaboration_2026.pptx (branch west-china-collaboration-2026).

Sources (not in the repository; BrainLab_maier.pptx is 172 MB):
  ~/Downloads/PRL_7min_landtag.pptx  -- the Landtag deck (14/15 October 2026), 21 slides
  ~/Downloads/BrainLab_maier.pptx    -- slides 3 (Strategic Goals) and 5 (SFB/CRC) are taken over

What the script does:
  1. Opens the Landtag deck and inserts BrainLab slides 3 and 5 around Landtag slide 4
     (Collaboration Building), in the BrainLab order: Strategic Goals, Collaboration
     Building, SFB/CRC.  All three are a full-slide picture on the "Textfolie" layout,
     so a BrainLab slide is a copy of Landtag slide 4 with its picture swapped.
  2. Replaces the full-slide pictures that were rendered from beamer (Landtag slides 2,
     13-17, 19, 21) with the pages of output_tex/main.pdf, rasterised to
     build_pptx/wch_collab_pages/page-NN.png.  Those pages carry the Chinese subheading
     and the West China footer.  Screenshot overlays on slides 14 and 17 are kept.
  3. Adds the Chinese translation of each native slide's title as its subheading.
  4. Turns the German footer and date fields into English.

Run from the repository root:
  gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r200 \
     -sOutputFile=build_pptx/wch_collab_pages/page-%02d.png output_tex/main.pdf
  python3 build_pptx/build_wch_collab.py
"""
import copy
import io
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.oxml.ns import qn
from pptx.util import Pt

HOME = Path.home()
LANDTAG = HOME / "Downloads" / "PRL_7min_landtag.pptx"
BRAINLAB = HOME / "Downloads" / "BrainLab_maier.pptx"
ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "build_pptx" / "wch_collab_pages"
OUT = ROOT / "build_pptx" / "West_China_Collaboration_2026.pptx"

CJK_FONT = "Microsoft YaHei"   # bundled with PowerPoint; standard on Chinese Windows
SUB_TOP, SUB_LEFT = Pt(54), Pt(41)  # the template's subtitle line (placeholder idx 37)

# BrainLab picture parts of slides 3 and 5 (read from the slide relationships)
BRAINLAB_MEDIA = {"strategic_goals": "ppt/media/image14.png",
                  "sfb_crc": "ppt/media/image16.png"}

# Landtag slide number -> beamer page that replaces its full-slide picture
RASTER = {2: 1, 13: 2, 14: 3, 15: 4, 16: 5, 17: 6, 19: 7, 21: 8}


def picture_blob(slide, name="Picture 1"):
    return next(s for s in slide.shapes if s.name == name)


def swap_picture(slide, pic, blob):
    """Point an existing picture shape at a new image."""
    image_part, rid = slide.part.get_or_add_image_part(io.BytesIO(blob))
    pic._element.blipFill.find(qn("a:blip")).set(qn("r:embed"), rid)


def duplicate_slide(prs, slide):
    """Append a copy of `slide` (same layout, same shapes, images re-linked)."""
    new = prs.slides.add_slide(slide.slide_layout)
    for ph in list(new.placeholders):
        ph._element.getparent().remove(ph._element)
    for shp in slide.shapes:
        el = copy.deepcopy(shp._element)
        new.shapes._spTree.append(el)
        for blip in el.iter(qn("a:blip")):
            rid = blip.get(qn("r:embed"))
            blob = slide.part.related_part(rid).blob
            _, new_rid = new.part.get_or_add_image_part(io.BytesIO(blob))
            blip.set(qn("r:embed"), new_rid)
    return new


def style_run(run, size, color=None, theme=MSO_THEME_COLOR.ACCENT_3, bold=False):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    if color is not None:
        f.color.rgb = color
    else:
        f.color.theme_color = theme
    rpr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea"):
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {})
            rpr.append(el)
        el.set("typeface", CJK_FONT)
    rpr.set("lang", "zh-CN")


def add_box(slide, text, left, top, width, height, size=16, color=None):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tb.name = "Chinese subheading"
    tf = tb.text_frame
    tf.word_wrap = False
    for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, side, 0)
    run = tf.paragraphs[0].add_run()
    run.text = text
    style_run(run, size, color)
    return tb


def subheading(slide, text):
    """Chinese title translation on the template's subtitle line (idx 37 at 54 pt)."""
    sub = next((s for s in slide.placeholders if s.placeholder_format.idx == 37), None)
    if sub is None:
        sub = next((s for s in slide.shapes if s.has_text_frame and not s.is_placeholder
                    and abs(s.top - Pt(48)) < Pt(4) and s.text_frame.text.strip() == "."), None)
    if sub is not None and sub.text_frame.text.strip() not in ("", "."):
        # an English subtitle already exists: the Chinese follows it on the same line
        p = sub.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = " " + text
        style_run(run, 16)
        return
    if sub is not None:
        tf = sub.text_frame
        for p in tf.paragraphs[1:]:
            p._p.getparent().remove(p._p)
        p = tf.paragraphs[0]
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        run = p.add_run()
        run.text = text
        style_run(run, 16)
        return
    add_box(slide, text, SUB_LEFT, SUB_TOP, Pt(539), Pt(20))


FOOTER = {"Technische Fakultät": "Faculty of Engineering"}
DATES = ("14. Oktober 2026", "15. Oktober 2026", "6. Februar 2026",
         "October 14, 2026", "October 28, 2026")


def english_footers(slide):
    for shp in slide.placeholders:
        t = shp.placeholder_format.type
        if t is None or not shp.has_text_frame:
            continue
        txt = shp.text_frame.text.strip()
        if txt in FOOTER:
            new = FOOTER[txt]
        elif txt in DATES or shp.name.startswith(("Datumsplatzhalter", "Date Placeholder")):
            new = "October 2026"
        else:
            continue
        p = shp.text_frame.paragraphs[0]
        rpr = None
        first = p._p.find(qn("a:r")) if p._p.find(qn("a:r")) is not None else p._p.find(qn("a:fld"))
        if first is not None and first.find(qn("a:rPr")) is not None:
            rpr = copy.deepcopy(first.find(qn("a:rPr")))
        for child in list(p._p):
            if child.tag in (qn("a:r"), qn("a:fld"), qn("a:br")):
                p._p.remove(child)
        run = p.add_run()
        run.text = new
        if rpr is not None:
            run._r.remove(run._r.find(qn("a:rPr"))) if run._r.find(qn("a:rPr")) is not None else None
            run._r.insert(0, rpr)


def main():
    prs = Presentation(str(LANDTAG))
    slides = list(prs.slides)
    assert len(slides) == 21, len(slides)
    S = {i + 1: s for i, s in enumerate(slides)}

    # 1. BrainLab slides 3 and 5, as copies of Landtag slide 4 with their pictures
    with zipfile.ZipFile(BRAINLAB) as z:
        media = {k: z.read(v) for k, v in BRAINLAB_MEDIA.items()}
    goals = duplicate_slide(prs, S[4])
    swap_picture(goals, picture_blob(goals, "Grafik 4"), media["strategic_goals"])
    sfb = duplicate_slide(prs, S[4])
    swap_picture(sfb, picture_blob(sfb, "Grafik 4"), media["sfb_crc"])

    # 2. beamer-rendered pages
    for n, page in RASTER.items():
        pic = picture_blob(S[n])
        assert pic.left <= 0 and pic.top <= 0 and pic.width >= prs.slide_width * 0.99, n
        swap_picture(S[n], pic, (PAGES / f"page-{page:02d}.png").read_bytes())

    # 3. Chinese subheadings on the native slides
    white = RGBColor(0xFF, 0xFF, 0xFF)
    add_box(S[1], "模式识别实验室简介", Pt(46), Pt(230), Pt(600), Pt(28), size=20, color=white)
    add_box(S[3], "FAU医学工程重点研究中心", Pt(41), Pt(302), Pt(700), Pt(34), size=26, color=white)
    add_box(goals, "战略目标", Pt(41), Pt(54), Pt(400), Pt(20))
    add_box(S[4], "合作网络建设：我们的策略", Pt(200), Pt(52), Pt(420), Pt(20))
    add_box(sfb, "合作研究中心：以多模态人工智能变革医疗", Pt(190), Pt(64), Pt(440), Pt(20), size=14)
    add_box(S[5], "模式识别实验室", Pt(598), Pt(450), Pt(170), Pt(30), size=22, color=white)
    for n, text in {6: "温故而知新", 7: "我们的团队", 8: "研究方向", 9: "实验室的工作",
                    10: "运动补偿", 11: "多器官分割", 12: "五十年历程概览",
                    18: "NHR@FAU高性能计算中心：设备概览", 20: "合作伙伴"}.items():
        subheading(S[n], text)

    # source typo on the Cooperations slide
    for shp in S[20].shapes:
        if shp.has_text_frame:
            for p in shp.text_frame.paragraphs:
                for r in p.runs:
                    if "collarboration" in r.text:
                        r.text = r.text.replace("collarboration", "collaboration")

    # 4. English footer and date
    for s in prs.slides:
        english_footers(s)

    # order: Landtag 1-3, Strategic Goals, Landtag 4, SFB/CRC, Landtag 5-21
    lst = prs.slides._sldIdLst
    ids = list(lst)
    order = ids[:3] + [ids[21], ids[3], ids[22]] + ids[4:21]
    for el in ids:
        lst.remove(el)
    for el in order:
        lst.append(el)

    prs.save(str(OUT))
    print(f"wrote {OUT} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
