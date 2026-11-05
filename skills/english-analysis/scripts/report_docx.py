#!/usr/bin/env python3
"""Build a black-text, multi-page .docx from a lesson report or student profile markdown file.

Usage: report_docx.py <report.md> <out.docx>
Supports: '# ' title, '## ' and '### ' headings, '- ' bullets, '1. ' numbered items,
'> ' quotes, markdown tables, **bold** / *italic*, plain paragraphs, and a page number
in the footer. Unlike one_pager_docx.py there is no length limit.
Requires: pip install python-docx. Run with plain `python3` (the -I flag hides
user-installed packages such as python-docx).
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from one_pager_docx import add_runs, tight, underline

TABLE_ROW = re.compile(r"^\|[-| :]+\|$")


def page_number(par):
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        run = par.add_run()
        if kind:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = text
        run._r.append(el)


def build(lines, out):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(0.8)
    sec.top_margin = sec.bottom_margin = Inches(0.7)
    st = doc.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    foot = sec.footer.paragraphs[0]
    foot.alignment = 1
    page_number(foot)

    rows = []

    def flush():
        if not rows:
            return
        t = doc.add_table(rows=len(rows), cols=max(len(r) for r in rows)); t.style = "Table Grid"
        for ri, row in enumerate(rows):
            for ci, cell in enumerate(row):
                c = t.cell(ri, ci); c.text = ""
                p = c.paragraphs[0]; tight(p, 1, 1)
                add_runs(p, cell.strip(), 9.5, bold=(ri == 0))
        doc.add_paragraph().paragraph_format.space_after = Pt(0)
        rows.clear()

    for raw in lines:
        s = raw.strip()
        if s.startswith("|"):
            if not TABLE_ROW.match(s):
                rows.append(s.strip("|").split("|"))
            continue
        flush()
        if not s:
            continue
        if s.startswith("### "):
            p = doc.add_paragraph(); tight(p, 6, 2); add_runs(p, s[4:], 10.5, bold=True)
        elif s.startswith("## "):
            p = doc.add_paragraph(); tight(p, 10, 3); add_runs(p, s[3:], 12.5, bold=True); underline(p)
        elif s.startswith("# "):
            p = doc.add_paragraph(); tight(p, 0, 3); add_runs(p, s[2:], 18, bold=True)
        elif s.startswith("- "):
            p = doc.add_paragraph(style="List Bullet"); tight(p, 0, 2); add_runs(p, s[2:])
        elif re.match(r"^\d+\.\s", s):
            p = doc.add_paragraph(style="List Number"); tight(p, 0, 2); add_runs(p, re.sub(r"^\d+\.\s", "", s))
        elif s.startswith("> "):
            p = doc.add_paragraph(); tight(p, 0, 3); p.paragraph_format.left_indent = Inches(0.3)
            add_runs(p, s[2:])
            for r in p.runs:
                r.italic = True
        else:
            p = doc.add_paragraph(); tight(p, 0, 4); add_runs(p, s)
    flush()
    doc.save(out)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
    build(lines, sys.argv[2])
    words = sum(len(re.findall(r"\S+", re.sub(r"\*{1,3}", "", l))) for l in lines if not TABLE_ROW.match(l.strip()))
    print(f"wrote {sys.argv[2]} ({words} words)")


if __name__ == "__main__":
    main()
