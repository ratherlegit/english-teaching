#!/usr/bin/env python3
"""Build a compact, black-text, one-page .docx from a one-pager markdown file.

Usage: one_pager_docx.py <one_pager.md> <out.docx>
Supports: '# ' title, '## ' section headings, '- ' bullets, markdown tables,
**bold** / *italic*, plain paragraphs. Exits with an error if the page is over
the length budget (450 words or about 55 lines), because the point is one page.
Requires: pip install python-docx. Run with plain `python3` (the -I flag hides user-installed packages such as python-docx).
"""
import math, re, sys
from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

MAX_WORDS, MAX_LINES, CHARS_PER_LINE = 450, 55, 95
BLACK = RGBColor(0, 0, 0)

def plain(t):
    return re.sub(r"\*{1,3}", "", t)

def add_runs(par, text, size=10, bold=False):
    for tok in re.split(r"(\*\*\*.+?\*\*\*|\*\*.+?\*\*|\*.+?\*)", text):
        if not tok:
            continue
        b, i = bold, False
        if tok.startswith("***") and tok.endswith("***"): tok, b, i = tok[3:-3], True, True
        elif tok.startswith("**") and tok.endswith("**"): tok, b = tok[2:-2], True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2: tok, i = tok[1:-1], True
        r = par.add_run(tok); r.bold, r.italic = b, i
        r.font.size, r.font.color.rgb = Pt(size), BLACK

def tight(par, before=0, after=2):
    f = par.paragraph_format
    f.space_before, f.space_after = Pt(before), Pt(after)
    f.line_spacing_rule = WD_LINE_SPACING.SINGLE

def underline(par):
    pPr = par._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "1"), ("w:color", "000000")):
        b.set(qn(k), v)
    bdr.append(b); pPr.append(bdr)

def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
    words = sum(len(re.findall(r"\S+", plain(l))) for l in lines if not re.match(r"^\|[-| :]+\|$", l))
    est = 0.0
    for l in lines:
        s = l.strip()
        if not s or re.match(r"^\|[-| :]+\|$", s): continue
        est += 1.6 if s.startswith("#") else (1 if s.startswith("|") else math.ceil(len(plain(s)) / CHARS_PER_LINE))
    if words > MAX_WORDS or est > MAX_LINES:
        sys.exit(f"Too long for one page: {words} words (max {MAX_WORDS}), about {est:.0f} lines (max {MAX_LINES}). Cut the least useful bullets.")

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(0.7)
    sec.top_margin = sec.bottom_margin = Inches(0.6)
    st = doc.styles["Normal"]; st.font.name = "Arial"; st.font.size = Pt(10)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")

    rows = []
    def flush():
        if not rows: return
        t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
        for ri, row in enumerate(rows):
            for ci, cell in enumerate(row):
                c = t.cell(ri, ci); c.text = ""
                p = c.paragraphs[0]; tight(p, 1, 1)
                add_runs(p, cell.strip(), 10, bold=(ri == 0))
        doc.add_paragraph().paragraph_format.space_after = Pt(0)
        rows.clear()

    for l in lines:
        s = l.strip()
        if s.startswith("|"):
            if not re.match(r"^\|[-| :]+\|$", s):
                rows.append([c for c in s.strip("|").split("|")])
            continue
        flush()
        if not s: continue
        if s.startswith("## "):
            p = doc.add_paragraph(); tight(p, 6, 2); add_runs(p, s[3:], 11, bold=True); underline(p)
        elif s.startswith("# "):
            p = doc.add_paragraph(); tight(p, 0, 2); add_runs(p, s[2:], 16, bold=True)
        elif s.startswith("- "):
            p = doc.add_paragraph(style="List Bullet"); tight(p, 0, 1); add_runs(p, s[2:])
        else:
            p = doc.add_paragraph(); tight(p, 0, 2); add_runs(p, s)
    flush()
    doc.save(sys.argv[2])
    print(f"wrote {sys.argv[2]} ({words} words, about {est:.0f} lines)")

if __name__ == "__main__":
    main()
