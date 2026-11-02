#!/usr/bin/env python3
"""
Convert a worksheet pack written in plain markdown to colorful .docx files.

Harness-agnostic export for the english-worksheet skill: any AI coding agent
that can run a shell command can call this.

Usage:
    python3 md_to_docx.py input.md output.docx          one file, worksheets on separate pages
    python3 md_to_docx.py input.md output_dir/ --split  one .docx per worksheet

Worksheets are separated by a line containing only `<!-- worksheet -->`.
Anything before the first marker is an overview/cover section (a plan table, how to
use the pack). In --split mode it is written as 00-overview.docx if it has content.
`<!-- pagebreak -->` forces a page break inside a worksheet.

Markdown supported:
    # Title               pack title (blue, with a rule underneath)
    ## Worksheet title    a full-width blue banner
    ### Part heading      accent-colored heading with a rule underneath
    **bold**, *italic*, bullets, numbered lists that restart at 1, markdown tables
    > text                a message or quote, with a tinted background and an accent bar
    ![alt](path){2.5}     an image from a local file, centered. The optional {2.5} is the
                          width in inches (default 2). Paths are relative to the markdown
                          file. A missing file prints a warning and is skipped.
    :::box ... :::        the focus box: tinted, with an accent border and an accent title
    :::box bank ... :::   a yellow word bank
    :::box watch ... :::  a soft red "watch out" box
    :::write N ... :::    a tinted answer box about N lines tall; the student clicks
                          inside and types, and the box grows as they type. Text between the
                          fences (a message to correct) is already inside the box.
    A table gets a blue header row. If its last column is headed "Your answer" (or "Your sentence", when the answer is typed into the sentence itself),
    the answer cells are tinted light blue with a minimum height, so the student types next to
    the item without touching the layout. A row numbered 0 is the worked example: its answer
    cell is light green and already filled in. Column widths are set automatically.

Requires: pip install python-docx
"""

import os
import re
import sys

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
except ImportError:
    print(
        "python-docx is required. Install it with: pip install python-docx",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------- colors ----------
# Blue is the main color (banners, headers, titles); other colors mark other elements.
# Fills are light so typed black text stays easy to read. Dark blue keeps white text at 4.5:1 or better.
THEME = {"dark": "1F4E9A", "tint": "F3F7FD", "answer": "E6EFFB"}
EXAMPLE = {"fill": "E3F3E6"}
BANK = {"fill": "FFF6D6", "border": "E0B83C", "title": "7A5B00"}
WATCH = {"fill": "FDECEA", "border": "D9534F", "title": "B71C1C"}
WHITE = RGBColor(255, 255, 255)

WORKSHEET_MARKER = "<!-- worksheet -->"
PAGEBREAK_MARKER = "<!-- pagebreak -->"
ANSWER_HEADERS = {"your answer", "answer", "your sentence"}
INLINE_PATTERN = re.compile(r"(\*\*\*.+?\*\*\*|\*\*.+?\*\*|\*.+?\*)")
LINK_PATTERN = re.compile(r"(?<!!)\[([^\]]+)\]\([^)]+\)")  # image syntax is left alone
IMAGE_PATTERN = re.compile(r"^!\[(.*?)\]\((.+?)\)(?:\{([\d.]+)\})?$")
TABLE_SEPARATOR_PATTERN = re.compile(r"^\|?[\s:|-]+\|?$")


def rgb(hex_string):
    return RGBColor.from_string(hex_string)


def strip_links(text):
    """Turn [label](url) into plain label text so nothing renders as a link."""
    return LINK_PATTERN.sub(r"\1", text)


# ---------- inline text ----------
def add_inline_runs(paragraph, text, italic_default=False):
    """Split text on **bold**/*italic*/***bold italic*** markers and add runs."""
    pos = 0
    for match in INLINE_PATTERN.finditer(text):
        if match.start() > pos:
            run = paragraph.add_run(text[pos : match.start()])
            run.italic = italic_default
        token = match.group(0)
        if token.startswith("***") and token.endswith("***"):
            run = paragraph.add_run(token[3:-3])
            run.bold = True
            run.italic = True
        elif token.startswith("**") and token.endswith("**"):
            run = paragraph.add_run(token[2:-2])
            run.bold = True
            run.italic = italic_default
        else:
            run = paragraph.add_run(token[1:-1])
            run.italic = True
        pos = match.end()
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        run.italic = italic_default


def style_runs(paragraph, color=None, bold=None, size=None):
    for run in paragraph.runs:
        if color is not None:
            run.font.color.rgb = color
        if bold is not None:
            run.bold = bold
        if size is not None:
            run.font.size = Pt(size)


# ---------- numbered lists ----------
def _numbering_element(doc):
    return doc.part.numbering_part.numbering_definitions._numbering


def _get_or_create_decimal_abstract_num(doc):
    numbering = _numbering_element(doc)
    cached_id = getattr(doc, "_lesson_abstract_num_id", None)
    if cached_id is not None:
        return cached_id
    existing_ids = [int(el.get(qn("w:abstractNumId"))) for el in numbering.findall(qn("w:abstractNum"))]
    abstract_id = max(existing_ids, default=-1) + 1
    abstract_num = OxmlElement("w:abstractNum")
    abstract_num.set(qn("w:abstractNumId"), str(abstract_id))
    lvl = OxmlElement("w:lvl")
    lvl.set(qn("w:ilvl"), "0")
    for tag, val in (("w:start", "1"), ("w:numFmt", "decimal"), ("w:lvlText", "%1."), ("w:lvlJc", "left")):
        el = OxmlElement(tag)
        el.set(qn("w:val"), val)
        lvl.append(el)
    p_pr = OxmlElement("w:pPr")
    ind = OxmlElement("w:ind")
    ind.set(qn("w:left"), "720")
    ind.set(qn("w:hanging"), "360")
    p_pr.append(ind)
    lvl.append(p_pr)
    abstract_num.append(lvl)
    numbering.insert(0, abstract_num)
    doc._lesson_abstract_num_id = abstract_id
    return abstract_id


def start_new_numbered_list(doc):
    """Create a fresh numbering definition (restarting at 1) and return its numId."""
    numbering = _numbering_element(doc)
    abstract_id = _get_or_create_decimal_abstract_num(doc)
    existing = [int(el.get(qn("w:numId"))) for el in numbering.findall(qn("w:num"))]
    num_id = max(existing, default=0) + 1
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(num_id))
    abstract = OxmlElement("w:abstractNumId")
    abstract.set(qn("w:val"), str(abstract_id))
    num.append(abstract)
    numbering.append(num)
    return num_id


def apply_numbering(paragraph, num_id):
    p_pr = paragraph._p.get_or_add_pPr()
    num_pr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num_id_el = OxmlElement("w:numId")
    num_id_el.set(qn("w:val"), str(num_id))
    num_pr.append(ilvl)
    num_pr.append(num_id_el)
    p_pr.append(num_pr)
    order_ppr(p_pr)


# ---------- XML ordering helpers ----------
# Strict viewers ignore or reject properties that appear out of schema order.
TBLPR_ORDER = [
    "tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize", "tblStyleColBandSize",
    "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar",
    "tblLook", "tblCaption", "tblDescription",
]
PPR_ORDER = [
    "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl", "numPr",
    "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
    "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi", "adjustRightInd",
    "snapToGrid", "spacing", "ind", "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc",
    "textDirection", "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr",
    "sectPr", "pPrChange",
]


def _reorder(parent, order):
    def key(el):
        name = el.tag.split("}")[1]
        return order.index(name) if name in order else len(order)

    children = sorted(list(parent), key=key)
    for el in list(parent):
        parent.remove(el)
    for el in children:
        parent.append(el)


def order_tbl_pr(tbl_pr):
    _reorder(tbl_pr, TBLPR_ORDER)


def order_ppr(p_pr):
    _reorder(p_pr, PPR_ORDER)


# ---------- paragraph styling ----------
def shade_paragraph(paragraph, fill):
    p_pr = paragraph._p.get_or_add_pPr()
    for old in p_pr.findall(qn("w:shd")):
        p_pr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    p_pr.append(shd)
    order_ppr(p_pr)


def border_paragraph(paragraph, color, sides=("bottom",), size=8, space=1):
    p_pr = paragraph._p.get_or_add_pPr()
    for old in p_pr.findall(qn("w:pBdr")):
        p_pr.remove(old)
    pbdr = OxmlElement("w:pBdr")
    for side in ("top", "left", "bottom", "right"):
        if side in sides:
            el = OxmlElement(f"w:{side}")
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(size))
            el.set(qn("w:space"), str(space))
            el.set(qn("w:color"), color)
            pbdr.append(el)
    p_pr.append(pbdr)
    order_ppr(p_pr)


# ---------- tables ----------
def set_table_borders(table, color="A6A6A6", size=4):
    """Write explicit borders so every viewer (Word, Google Docs, previewers) draws them."""
    tbl_pr = table._tbl.tblPr
    for old in tbl_pr.findall(qn("w:tblBorders")):
        tbl_pr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(size))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tbl_pr.append(borders)
    order_tbl_pr(tbl_pr)


def style_table(table, border_color="A6A6A6", size=4):
    table.style = "Table Grid"
    set_table_borders(table, border_color, size)


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    for old in tc_pr.findall(qn("w:shd")):
        tc_pr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_row_min_height(row, inches):
    """Make a table row at least `inches` tall (it still grows when text is typed)."""
    tr_pr = row._tr.get_or_add_trPr()
    tr_pr.append(OxmlElement("w:cantSplit"))  # a single row never breaks across pages; the table itself flows
    height = OxmlElement("w:trHeight")
    height.set(qn("w:val"), str(int(inches * 1440)))
    height.set(qn("w:hRule"), "atLeast")
    tr_pr.append(height)


def set_column_widths(table, widths_in_inches):
    """Fix the table width and column widths in the XML so Word, Google Docs and
    previewers all draw the same layout."""
    table.autofit = False
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    for tag in ("w:tblW", "w:tblLayout"):
        for old in tbl_pr.findall(qn(tag)):
            tbl_pr.remove(old)
    tbl_w = OxmlElement("w:tblW")
    tbl_w.set(qn("w:w"), str(int(sum(widths_in_inches) * 1440)))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_pr.append(tbl_w)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    order_tbl_pr(tbl_pr)
    for col, width in zip(tbl.tblGrid.findall(qn("w:gridCol")), widths_in_inches):
        col.set(qn("w:w"), str(int(width * 1440)))
    for row in table.rows:
        for cell, width in zip(row.cells, widths_in_inches):
            cell.width = Inches(width)


def proportional_widths(rows, total_inches):
    """Column widths in proportion to the longest text in each column. A column is never
    narrower than its longest single word, so no word is ever broken across lines."""
    cols = len(rows[0])
    cells = [[re.sub(r"[*_]", "", r[c]) if c < len(r) else "" for r in rows] for c in range(cols)]
    weights = [min(max(max(len(t) for t in col), 6), 40) for col in cells]
    floors = [max(len(w) for t in col for w in (t.split() or [""])) * 0.105 + 0.25 for col in cells]
    widths = [total_inches * w / sum(weights) for w in weights]
    for _ in range(cols):  # raise narrow columns to their floor, taking the space from the roomiest
        short = [i for i in range(cols) if widths[i] < floors[i]]
        if not short:
            break
        for i in short:
            take = floors[i] - widths[i]
            donor = max((j for j in range(cols) if j not in short), key=lambda j: widths[j] - floors[j], default=None)
            if donor is None:
                break
            widths[donor] -= take
            widths[i] = floors[i]
    scale = total_inches / sum(widths)
    return [w * scale for w in widths]


def parse_table_row(line):
    """Split a `| a | b |` row into cell strings, dropping the outer empty cells."""
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_answer_header(text):
    return re.sub(r"[*_]", "", text).strip().lower() in ANSWER_HEADERS


def style_header_row(table, theme):
    for cell in table.rows[0].cells:
        shade_cell(cell, theme["dark"])
        for paragraph in cell.paragraphs:
            style_runs(paragraph, color=WHITE, bold=True)


# ---------- blocks ----------
def add_box(doc, box_lines, theme, kind="focus"):
    """Render the lines of a :::box block as a tinted one-cell table.
    Markdown tables inside the block become real nested tables."""
    if kind == "bank":
        fill, border, title = BANK["fill"], BANK["border"], BANK["title"]
    elif kind == "watch":
        fill, border, title = WATCH["fill"], WATCH["border"], WATCH["title"]
    else:
        fill, border, title = theme["tint"], theme["dark"], theme["dark"]
    table = doc.add_table(rows=1, cols=1)
    style_table(table, border, 8)
    cell = table.rows[0].cells[0]
    shade_cell(cell, fill)
    set_column_widths(table, [6.5])
    first = True
    first_text = True
    k = 0
    while k < len(box_lines):
        text = box_lines[k].strip()
        if not text:
            k += 1
            continue
        if text.startswith("|"):
            rows = []
            while k < len(box_lines) and box_lines[k].strip().startswith("|"):
                row_text = box_lines[k].strip()
                if not TABLE_SEPARATOR_PATTERN.match(row_text):
                    rows.append(parse_table_row(row_text))
                k += 1
            nested = cell.add_table(rows=len(rows), cols=len(rows[0]))
            style_table(nested, "BFBFBF")
            set_column_widths(nested, proportional_widths(rows, 6.1))
            for r_idx, row_cells in enumerate(rows):
                for c_idx, cell_text in enumerate(row_cells):
                    add_inline_runs(nested.rows[r_idx].cells[c_idx].paragraphs[0], cell_text)
            style_header_row(nested, theme)
            for r_idx in range(1, len(rows)):
                for c_idx in range(len(rows[0])):
                    shade_cell(nested.rows[r_idx].cells[c_idx], "FFFFFF")
            first = False
            continue
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        if text.startswith("- ") or text.startswith("* "):
            text = text[2:].strip()  # no bullet dots inside boxes: each item is its own line
        add_inline_runs(p, text)
        is_label = text.startswith("**") and text.endswith("**") and text.count("**") == 2
        if first_text and is_label:
            style_runs(p, color=rgb(title), size=12)
        elif is_label:
            p.paragraph_format.space_before = Pt(12)  # a section label ("Examples", "How to do it") needs room above
            p.paragraph_format.space_after = Pt(4)
        first_text = False
        k += 1
    if cell._tc[-1].tag == qn("w:tbl"):
        cell.add_paragraph()  # a cell cannot end with a table
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_banner(doc, text, theme):
    """The worksheet title: white text in a full-width dark cell. A table cell is shaded by every
    viewer, unlike paragraph shading, so the white text is never left on a white page."""
    table = doc.add_table(rows=1, cols=1)
    style_table(table, theme["dark"], 4)
    cell = table.rows[0].cells[0]
    shade_cell(cell, theme["dark"])
    set_column_widths(table, [6.5])
    p = cell.paragraphs[0]
    p.style = doc.styles["Heading 1"]
    add_inline_runs(p, text)
    style_runs(p, color=WHITE, bold=True, size=20)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_write_box(doc, lines_tall, theme, body=None):
    """A tinted one-cell table the student types into. Text inside the fence
    (for example a message to correct) is placed in the box already."""
    table = doc.add_table(rows=1, cols=1)
    style_table(table, theme["dark"], 6)
    cell = table.rows[0].cells[0]
    shade_cell(cell, theme["answer"])
    filled = [line.strip() for line in (body or [])]
    while filled and not filled[0]:
        filled.pop(0)
    while filled and not filled[-1]:
        filled.pop()
    for k, text in enumerate(filled):  # blank lines stay as empty paragraphs (letter layout)
        p = cell.paragraphs[0] if k == 0 else cell.add_paragraph()
        add_inline_runs(p, text)
    set_column_widths(table, [6.5])
    set_row_min_height(table.rows[0], max(0.5, lines_tall * 0.27))
    doc.add_paragraph()


def is_example_row(row_cells):
    return row_cells[0].strip() == "0"


def add_table(doc, header_cells, rows, theme):
    table = doc.add_table(rows=1, cols=len(header_cells))
    style_table(table, "BFBFBF")
    for cell, text in zip(table.rows[0].cells, header_cells):
        add_inline_runs(cell.paragraphs[0], text)
    for row_cells in rows:
        row = table.add_row()
        for cell, text in zip(row.cells, row_cells):
            add_inline_runs(cell.paragraphs[0], text)
    style_header_row(table, theme)
    if is_answer_header(header_cells[-1]):
        for row, row_cells in zip(table.rows[1:], rows):
            if is_example_row(row_cells):
                shade_cell(row.cells[-1], EXAMPLE["fill"])
            else:
                shade_cell(row.cells[-1], theme["answer"])
            set_row_min_height(row, 0.4)
        cols = len(header_cells)
        if cols == 3 and re.sub(r"[*_]", "", header_cells[-1]).strip().lower() == "your sentence":
            widths = [0.5, 2.2, 3.8]  # the sentence with the gap is the tinted, typed-in cell
        elif cols == 2 and header_cells[0].strip() == "#":
            widths = [0.6, 3.0]
        else:
            widths = {2: [3.6, 2.9], 3: [0.5, 3.3, 2.7], 4: [0.5, 1.9, 2.6, 1.5]}.get(cols, [6.5 / cols] * cols)
        set_column_widths(table, widths)
    else:
        set_column_widths(table, proportional_widths([header_cells] + rows, 6.5))
    doc.add_paragraph()


def add_image(doc, alt, path, width, base_dir):
    full = path if os.path.isabs(path) else os.path.join(base_dir, path)
    if not os.path.isfile(full):
        print(f"Warning: image not found, skipped: {path}", file=sys.stderr)
        return None
    doc.add_picture(full, width=Inches(float(width) if width else 2.0))
    paragraph = doc.paragraphs[-1]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return paragraph


def add_break_anchor(doc):
    """A 1-point empty paragraph with page-break-before, so a table or box can start a new
    page without a visible gap or stray character."""
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)
    run = paragraph.add_run("")
    run.font.size = Pt(1)
    mark_page_break_before(paragraph)


def mark_page_break_before(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    p_pr.append(OxmlElement("w:pageBreakBefore"))
    order_ppr(p_pr)


def prepare_styles(doc):
    """Arial throughout, and no default blue rule under the Title style."""
    styles_el = doc.styles.element
    for border in list(styles_el.iter(qn("w:pBdr"))):
        border.getparent().remove(border)
    for name in ("Normal", "Title", "Heading 1", "Heading 2", "Heading 3", "List Bullet", "List Number"):
        try:
            doc.styles[name].font.name = "Arial"
        except KeyError:
            pass
    doc.styles["Normal"].font.size = Pt(11)
    doc.styles["Normal"].paragraph_format.space_after = Pt(6)


def convert_lines(lines, output_path, base_dir="."):
    """Render markdown lines to a .docx."""
    doc = Document()
    for section in doc.sections:
        section.left_margin = section.right_margin = Inches(1)
    zoom = doc.settings.element.find(qn("w:zoom"))
    if zoom is not None and zoom.get(qn("w:percent")) is None:
        zoom.set(qn("w:percent"), "100")  # the python-docx template omits this required attribute
    prepare_styles(doc)

    theme = THEME
    current_list_num_id = None
    wrote_content = False
    pending_break = False

    i = 0
    n = len(lines)
    while i < n:
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue

        if stripped in (WORKSHEET_MARKER, PAGEBREAK_MARKER):
            if wrote_content or stripped == PAGEBREAK_MARKER:
                pending_break = True
            current_list_num_id = None
            i += 1
            continue

        fence = re.match(r":::(box|write)\b\s*(\w+)?", stripped)
        if fence:
            kind_word, arg = fence.group(1), fence.group(2)
            i += 1
            body = []
            while i < n and lines[i].strip() != ":::":
                body.append(lines[i])
                i += 1
            i += 1
            if pending_break:
                add_break_anchor(doc)
                pending_break = False
            if kind_word == "box":
                add_box(doc, body, theme, arg if arg in ("bank", "watch") else "focus")
            else:
                add_write_box(doc, int(arg) if arg and arg.isdigit() else 4, theme, body)
            wrote_content = True
            current_list_num_id = None
            continue

        wrote_content = True
        is_numbered_item = bool(re.match(r"^\d+\.\s", stripped))
        if not is_numbered_item:
            current_list_num_id = None

        if stripped.startswith("|") and i + 1 < n and TABLE_SEPARATOR_PATTERN.match(lines[i + 1].strip()):
            header_cells = parse_table_row(stripped)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(parse_table_row(lines[i].strip()))
                i += 1
            if pending_break:
                add_break_anchor(doc)
                pending_break = False
            add_table(doc, header_cells, rows, theme)
            continue

        image = IMAGE_PATTERN.match(stripped)
        p = None
        if image:
            p = add_image(doc, image.group(1), image.group(2), image.group(3), base_dir)
        elif stripped.startswith("### "):
            p = doc.add_heading(level=2)
            add_inline_runs(p, stripped[4:].strip())
            style_runs(p, color=rgb(theme["dark"]), bold=True, size=14)
            border_paragraph(p, theme["dark"], ("bottom",), size=8, space=2)
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
        elif stripped.startswith("## "):
            if pending_break:
                add_break_anchor(doc)
                pending_break = False
            add_banner(doc, stripped[3:].strip(), theme)
        elif stripped.startswith("# "):
            p = doc.add_heading(level=0)
            add_inline_runs(p, stripped[2:].strip())
            style_runs(p, color=rgb(THEME["dark"]), bold=True, size=26)
            border_paragraph(p, THEME["dark"], ("bottom",), size=12, space=4)
        elif stripped.startswith("> "):
            p = doc.add_paragraph()
            p.paragraph_format.keep_with_next = True
            add_inline_runs(p, stripped[2:].strip(), italic_default=True)
            shade_paragraph(p, theme["tint"])
            border_paragraph(p, theme["dark"], ("left",), size=24, space=8)
            p.paragraph_format.left_indent = Inches(0.25)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            add_inline_runs(p, stripped[2:].strip())
        elif is_numbered_item:
            if current_list_num_id is None:
                current_list_num_id = start_new_numbered_list(doc)
            p = doc.add_paragraph(style="List Number")
            add_inline_runs(p, re.sub(r"^\d+\.\s", "", stripped))
            apply_numbering(p, current_list_num_id)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.keep_with_next = True  # an instruction stays with the table or box under it
            add_inline_runs(p, stripped)

        if pending_break and p is not None:
            mark_page_break_before(p)
            pending_break = False
        i += 1

    doc.save(output_path)


# ---------- entry points ----------
def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "worksheet"


def split_sections(lines):
    """Return (preamble_lines, [worksheet_lines, ...]) split on the worksheet marker."""
    sections = [[]]
    for line in lines:
        if line.strip() == WORKSHEET_MARKER:
            sections.append([])
        else:
            sections[-1].append(line)
    return sections[0], sections[1:]


def first_heading(section):
    for line in section:
        m = re.match(r"^#{1,3}\s+(.*)", line.strip())
        if m:
            return m.group(1)
    return "worksheet"


def read_lines(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        return strip_links(f.read()).splitlines()


def convert(input_path, output_path):
    convert_lines(read_lines(input_path), output_path, base_dir=os.path.dirname(os.path.abspath(input_path)))


def convert_split(input_path, output_dir):
    base_dir = os.path.dirname(os.path.abspath(input_path))
    preamble, sheets = split_sections(read_lines(input_path))
    os.makedirs(output_dir, exist_ok=True)
    written = []
    if any(line.strip() for line in preamble):
        path = os.path.join(output_dir, "00-overview.docx")
        convert_lines(preamble, path, base_dir=base_dir)
        written.append(path)
    for number, section in enumerate(sheets, start=1):
        path = os.path.join(output_dir, f"{number:02d}-{slugify(first_heading(section))}.docx")
        convert_lines(section, path, base_dir=base_dir)
        written.append(path)
    return written


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--split"]
    split = "--split" in sys.argv[1:]
    if len(args) != 2:
        print(
            "Usage: python3 md_to_docx.py input.md output.docx\n"
            "       python3 md_to_docx.py input.md output_dir/ --split",
            file=sys.stderr,
        )
        sys.exit(1)
    if split:
        for path in convert_split(args[0], args[1]):
            print(f"Wrote {path}")
    else:
        convert(args[0], args[1])
        print(f"Wrote {args[1]}")
