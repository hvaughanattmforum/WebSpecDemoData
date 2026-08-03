"""
Render a component-specification-documentation .md file to a .pdf with all diagrams visible,
a cover + notice page generated fresh from the component YAML, a freshly rebuilt table of
contents, and every table's columns sized to its actual content.

Why this exists: xhtml2pdf (pure-Python, no pandoc/wkhtmltopdf needed) can't rasterize inline
.svg <img> references, so this rewrites any .svg reference to its sibling .png (rendering it
first via svglib -> reportlab -> pymupdf if missing) before conversion. Three more fixes on top
of that:

1. xhtml2pdf's automatic table-column-width algorithm ignores `table-layout` and `<colgroup>`
   entirely and can allocate a column so little width that its text overlaps the neighboring
   column or runs off the page edge -- confirmed on both the 2-column SID ABE table and the
   4-column Version History table. The only thing that actually works is an explicit `width:%`
   inline style on every <th>/<td> in a column, so this computes a content-based width per
   column and injects it.
2. The cover + notice pages are generated from the component's own YAML (`componentMetadata`),
   not copied from the old official PDF -- this is what lets the skill run for a component that
   never had a PDF at all. See `_maturity_level`/`_approval_status` for the exact status ->
   display-field mapping (user-specified, not guessed) and `NOTICE_TEXT` for the fixed legal
   boilerplate (identical across every TM Forum component document, so it's a constant here, not
   read from anywhere).
3. Chapters 5.2/5.3 (Jira References, Further resources) and 6 (Administrative Appendix) have no
   YAML source -- they're curated content maintained by hand in a sibling `..._Supplement.md`
   file (see SKILL.md, "Supplement file"). This script concatenates that file's content onto the
   main .md's body (right after 5.1) before rendering, so the final PDF reads as one continuous
   document even though it's assembled from two source files.

The .md file itself is never modified -- all of this only affects the in-memory HTML/PDF
produced for this rendering pass; Markdown viewers still get native SVG and no front matter.

Usage:
    python build_pdf.py path/to/TMFCxxx_Name.md [output.pdf]
"""
import glob
import html as html_lib
import os
import re
import sys

import fitz
import markdown
import yaml
from xhtml2pdf import pisa

_IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+\.svg)\)')
_HEADING_RE = re.compile(r'^(#{2,4})\s+(.+?)\s*$', re.MULTILINE)
_TABLE_RE = re.compile(r'<table[^>]*>.*?</table>', re.DOTALL)
_ROW_RE = re.compile(r'<tr>(.*?)</tr>', re.DOTALL)
_CELL_RE = re.compile(r'<(th|td)([^>]*)>(.*?)</\1>', re.DOTALL)
_TAG_RE = re.compile(r'<[^>]+>')

# TM Forum brand palette, sampled directly from a real published component PDF (TMFC001 v2.2.2) --
# see references/pdf_visual_template.md for how these were extracted and what they're used for.
TMF_RED = "#C00000"       # chapter headings (##), subsection headings (####), "Notice"/"Table of
                          # Contents" -- every heading one level "odd" out from a plain black one
TMF_DARK_GRAY = "#404040"  # cover page title/labels
TABLE_HEADER_BG = "#EFEFEF"

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "tmforum_logo.png")

# Heading color/weight follows the original PDF's own convention exactly (sampled per-span color,
# see references/pdf_visual_template.md): the "depth" of a heading's number alternates red/black --
# unnumbered chapter-level headings (Notice, Table of Contents) and numbered chapters ("2. eTOM...")
# are both red; a numbered section one level down ("2.1 eTOM business activities") is plain black;
# a numbered sub-section two levels down ("5.2.1 Functional Framework") is red again.
BASE_CSS = f"""
@page {{ size: A4; margin-top: 100pt; margin-bottom: 60pt; margin-left: 60pt; margin-right: 60pt; }}
body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: black; }}
h1 {{ font-size: 22pt; font-weight: bold; color: {TMF_RED}; margin-top: 4pt; margin-bottom: 14pt; }}
h2 {{ font-size: 20pt; font-weight: bold; color: {TMF_RED}; margin-top: 20pt; margin-bottom: 10pt; }}
h3 {{ font-size: 13pt; font-weight: bold; color: black; margin-top: 14pt; }}
h4 {{ font-size: 12pt; font-weight: bold; color: {TMF_RED}; margin-top: 10pt; }}
code {{ font-family: Courier, monospace; }}
table {{ border-collapse: collapse; width: 100%; margin: 6pt 0; }}
th, td {{ border: 1px solid #999999; padding: 4pt; font-size: 9pt; vertical-align: top;
          word-wrap: break-word; }}
th {{ background-color: {TABLE_HEADER_BG}; font-weight: bold; text-align: left; }}
img {{ max-width: 100%; display: block; margin: 8pt auto; }}
"""

MIN_COL_PCT = 8
MAX_CELL_SAMPLE = 40


def _svg_to_png(svg_path):
    png_path = os.path.splitext(svg_path)[0] + ".png"
    if os.path.exists(png_path):
        return png_path
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF

    drawing = svg2rlg(svg_path)
    tmp_pdf = svg_path + ".tmp.pdf"
    renderPDF.drawToFile(drawing, tmp_pdf)
    doc = fitz.open(tmp_pdf)
    doc[0].get_pixmap(dpi=150).save(png_path)
    doc.close()
    os.remove(tmp_pdf)
    return png_path


_SOURCE_CAPTION_LINE = re.compile(
    r"(?m)^[ \t]*\*\(\s*(?:PlantUML|SVG|Mermaid)\s+source\s*:.*?\)\*[ \t]*\r?\n?")


def _strip_source_captions(text):
    """Drop the italic "*(PlantUML source: <file>)*" line that follows each diagram.

    These captions carry provenance back to the diagram source file, which is useful in the `.md` where
    the link is clickable -- but the published document doesn't show them, so they're removed for the
    PDF the same way build_docx_scroll.py removes them for Word. The `.md` itself keeps them: this
    filter runs on the in-memory copy only, never on the file."""
    return _SOURCE_CAPTION_LINE.sub("", text)


def _strip_front_matter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:]
    return text


def _cell_text_len(cell_html):
    text = html_lib.unescape(_TAG_RE.sub("", cell_html)).strip()
    return min(len(text), MAX_CELL_SAMPLE)


def _optimize_table_widths(html_doc):
    """Inject a content-proportional width:% onto every <th>/<td>.

    xhtml2pdf's own column-width algorithm can size a column to almost nothing (confirmed:
    a short header next to a long-content neighbor collapses to near-zero width, and that
    column's text then overlaps the next column or runs off the page). Explicit per-cell
    width is the only thing that reliably works -- <colgroup>/table-layout:fixed are both
    silently ignored by xhtml2pdf.
    """
    def _fix_table(match):
        table_html = match.group(0)
        rows = [_CELL_RE.findall(r) for r in _ROW_RE.findall(table_html)]
        n_cols = max((len(r) for r in rows), default=0)
        if n_cols <= 1:
            return table_html

        weight = [1] * n_cols
        for row in rows:
            for j, (_tag, _attrs, content) in enumerate(row):
                weight[j] = max(weight[j], _cell_text_len(content))

        budget = 100 - MIN_COL_PCT * n_cols
        total = sum(weight)
        pct = [MIN_COL_PCT + budget * (w / total) for w in weight]
        pct_int = [int(round(p)) for p in pct]
        pct_int[-1] += 100 - sum(pct_int)  # absorb rounding error in the last column

        def _fix_row(row_match):
            col = [0]

            def _fix_cell(cell_match):
                tag, attrs, content = cell_match.groups()
                j = min(col[0], n_cols - 1)
                col[0] += 1
                style = f"width:{pct_int[j]}%"
                if "style=" in attrs:
                    new_attrs = re.sub(r'style="', f'style="{style};', attrs, count=1)
                else:
                    new_attrs = f'{attrs} style="{style}"'
                return f"<{tag}{new_attrs}>{content}</{tag}>"

            return f"<tr>{_CELL_RE.sub(_fix_cell, row_match.group(1))}</tr>"

        return _ROW_RE.sub(_fix_row, table_html)

    return _TABLE_RE.sub(_fix_table, html_doc)


def _wrap_html(body_html, extra_css=""):
    return (f'<html><head><meta charset="utf-8"><style>{BASE_CSS}{extra_css}'
            f'</style></head><body>{body_html}</body></html>')


def _render_pdf(html_doc, out_path, base_dir):
    with open(out_path, "wb") as f:
        result = pisa.CreatePDF(html_doc, dest=f, link_callback=lambda uri, rel: (
            os.path.join(base_dir, uri) if not os.path.isabs(uri) else uri
        ))
    assert result.err == 0, f"PDF conversion failed for {out_path}"


def _extract_headings(text):
    """Returns [(depth, text)], depth 0 for ##, 1 for ###, 2 for ####. Skips the H1 title."""
    return [(len(hashes) - 2, heading) for hashes, heading in _HEADING_RE.findall(text)]


def _locate_headings(body_pdf_path, headings):
    """Page index (0-based, within the body PDF) of each heading, via text search."""
    doc = fitz.open(body_pdf_path)
    pages = []
    search_from = 0
    for _depth, heading in headings:
        found = search_from
        for i in range(search_from, len(doc)):
            if doc[i].search_for(heading):
                found = i
                break
        pages.append(found)
        search_from = found
    doc.close()
    return pages


TOC_CSS = """
table.toc, table.toc td { border: none; }
table.toc td { padding: 3pt 4pt; font-size: 11pt; border-bottom: 1px dotted #999; }
table.toc td.pg { text-align: right; width: 30pt; white-space: nowrap; }
"""


def _build_toc_html(entries):
    """entries: [(indent_pt, text, page_number)]. Rendered as a borderless 2-column table
    with a shared dotted bottom border, approximating a classic dotted-leader ToC line --
    a plain float-right span didn't work, xhtml2pdf's float support isn't reliable enough
    for this (the "page number" ended up glued to the left, right next to the heading text,
    not pushed to the margin)."""
    rows = ['<h1 style="margin-bottom:14pt;">Table of Contents</h1>', '<table class="toc">']
    for indent, text, page in entries:
        rows.append(
            f'<tr><td style="padding-left:{indent + 4}pt;">{html_lib.escape(text)}</td>'
            f'<td class="pg">{html_lib.escape(str(page))}</td></tr>'
        )
    rows.append("</table>")
    return "\n".join(rows)


_MINOR_WORDS = {"and", "or", "of", "the", "for", "to", "in", "on"}


def _spaced_name(concatenated):
    """ProductInventory -> Product Inventory -- same rule the main .md's H1 title uses."""
    # a connector left lowercase in the source ("OrchestrationandManagement") needs a split on both
    # sides of it, since the generic rule below only splits at a lower->upper boundary
    with_connectors = re.sub(r'([a-z])(and|or|of|the)([A-Z])', r'\1 \2 \3', concatenated)
    spaced = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', with_connectors)
    # a connector that was already capitalized ("OrchestrationAndManagement", as in TMFC003) splits
    # correctly but keeps its capital, giving "Orchestration And Management" where the published
    # document titles it "Orchestration and Management". Only interior words are lowered, so a name
    # that legitimately begins with one keeps its capital.
    words = spaced.split()
    return " ".join(w if i == 0 or w.lower() not in _MINOR_WORDS else w.lower()
                    for i, w in enumerate(words))


def _maturity_level(status):
    s = status.lower()
    if s in ("preview", "production"):
        return "General Availability (GA)"
    if s == "roadmap":
        return "Beta"
    if s == "backlog":
        return "Alpha"
    raise ValueError(f"Unrecognized componentMetadata.status {status!r} -- can't derive Maturity Level")


def _approval_status(status):
    s = status.lower()
    if s == "production":
        return "TM Forum Approved"
    if s == "preview":
        return "Team Approved"
    if s in ("roadmap", "backlog"):
        return "Not yet approved"
    raise ValueError(f"Unrecognized componentMetadata.status {status!r} -- can't derive Approval Status")


def _find_component_yaml(base_dir):
    """The main .md lives in the component's Diagrams/ folder (see SKILL.md "Where the data lives"),
    so the one component-root *.yaml sits one directory up from base_dir, not inside it -- base_dir
    itself is full of unrelated *.yaml diagram sources (Exposed_API.yaml, Events.yaml, etc.)."""
    component_dir = os.path.dirname(base_dir)
    matches = glob.glob(os.path.join(component_dir, "*.yaml"))
    if len(matches) != 1:
        raise FileNotFoundError(
            f"Expected exactly one top-level *.yaml in the component folder (to read componentMetadata "
            f"from) in {component_dir}, found {len(matches)}: {matches}. Pass yaml_path explicitly."
        )
    return matches[0]


def _load_component_metadata(yaml_path):
    with open(yaml_path, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    meta = doc["spec"]["componentMetadata"] if "spec" in doc else doc["componentMetadata"]
    return meta


NOTICE_TEXT = """
<p>Copyright &copy; TM Forum {year}. All Rights Reserved.</p>
<p>This document and translations of it may be copied and furnished to others, and derivative
works that comment on or otherwise explain it or assist in its implementation may be prepared,
copied, published, and distributed, in whole or in part, without restriction of any kind,
provided that the above copyright notice and this section are included on all such copies and
derivative works. However, this document itself may not be modified in any way, including by
removing the copyright notice or references to TM FORUM, except as needed for the purpose of
developing any document or deliverable produced by a TM FORUM Collaboration Project Team (in
which case the rules applicable to copyrights, as set forth in the
<a href="http://www.tmforum.org/IPRPolicy/11525/home.html">TM FORUM IPR Policy</a>, must be
followed) or as required to translate it into languages other than English.</p>
<p>The limited permissions granted above are perpetual and will not be revoked by TM FORUM or its
successors or assigns.</p>
<p>This document and the information contained herein is provided on an &ldquo;AS IS&rdquo; basis
and TM FORUM DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY
WARRANTY THAT THE USE OF THE INFORMATION HEREIN WILL NOT INFRINGE ANY OWNERSHIP RIGHTS OR ANY
IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.</p>
<p>Direct inquiries to the TM Forum office:</p>
<p>100 Enterprise Drive<br/>Suite 301 #1649<br/>Rockaway, NJ 070866, USA<br/>
Tel No. +1 862 227 1648<br/>TM Forum Web Page: <a href="http://www.tmforum.org/">www.tmforum.org</a></p>
"""


def _build_cover_notice_html(meta):
    """meta: the raw componentMetadata dict (id, name, version, status, publicationDate, ...)."""
    status = meta["status"]
    year = meta["publicationDate"].year if hasattr(meta["publicationDate"], "year") else int(str(meta["publicationDate"])[:4])
    display_name = _spaced_name(meta["name"])
    team_approved_date = (
        meta["publicationDate"].strftime("%d-%b-%Y")
        if hasattr(meta["publicationDate"], "strftime")
        else str(meta["publicationDate"])
    )

    # Layout, colors, and field order match the original published PDF's cover exactly (see
    # references/pdf_visual_template.md) -- red "TM Forum Component" kicker, dark-gray bold title,
    # a large gap, then the bold dark-gray id + a bordered 3-row/2-column field table. The TM Forum
    # logo itself is NOT embedded here -- it's stamped on every page (including this one) by
    # _apply_page_chrome() after the whole PDF is assembled, so there's a single source of truth
    # for its position instead of one HTML copy per render pass.
    cover = f"""
    <div style="page-break-after: always;">
      <div style="margin-top:90pt;">
        <p style="font-size:20pt; font-weight:bold; color:{TMF_RED}; margin:0;">TM Forum Component</p>
        <h1 style="font-size:24pt; color:{TMF_DARK_GRAY}; margin-top:24pt; margin-bottom:0;">{html_lib.escape(display_name)}</h1>
      </div>
      <div style="margin-top:180pt;">
        <p style="font-size:13pt; font-weight:bold; color:{TMF_DARK_GRAY}; margin-bottom:10pt;">{html_lib.escape(meta['id'])}</p>
        <table style="width:100%; border-collapse:collapse;">
          <tr>
            <td style="width:50%; border:1px solid #999999; padding:5pt 8pt; font-size:10.5pt; font-weight:bold; color:{TMF_DARK_GRAY};">Maturity Level: {_maturity_level(status)}</td>
            <td style="width:50%; border:1px solid #999999; padding:5pt 8pt; font-size:10.5pt; font-weight:bold; color:{TMF_DARK_GRAY};">Team Approved Date: {team_approved_date}</td>
          </tr>
          <tr>
            <td style="border:1px solid #999999; padding:5pt 8pt; font-size:10.5pt; font-weight:bold; color:{TMF_DARK_GRAY};">Release Status: {html_lib.escape(str(status).capitalize())}</td>
            <td style="border:1px solid #999999; padding:5pt 8pt; font-size:10.5pt; font-weight:bold; color:{TMF_DARK_GRAY};">Approval Status: {_approval_status(status)}</td>
          </tr>
          <tr>
            <td style="border:1px solid #999999; padding:5pt 8pt; font-size:10.5pt; font-weight:bold; color:{TMF_DARK_GRAY};">Version {html_lib.escape(str(meta['version']))}</td>
            <td style="border:1px solid #999999; padding:5pt 8pt; font-size:10.5pt; font-weight:bold; color:{TMF_DARK_GRAY};">IPR Mode: RAND</td>
          </tr>
        </table>
      </div>
    </div>
    <div>
      <h1>Notice</h1>
      {NOTICE_TEXT.format(year=year)}
    </div>
    """
    return cover


# Logo size/position and the running-title/footer positions are all sampled directly from the
# real PDF's embedded image + text spans (see references/pdf_visual_template.md) -- not eyeballed.
LOGO_W, LOGO_H = 70, 58.5   # ~1.196:1, the logo's real aspect ratio
LOGO_MARGIN_RIGHT, LOGO_MARGIN_TOP = 60, 15
MARGIN_LEFT = 60
FOOTER_Y_FROM_BOTTOM = 40
HEADER_Y_FROM_TOP = 40


def _apply_page_chrome(doc, meta):
    """Stamp the TM Forum logo, per-page running title, and footer (copyright + page N of M)
    onto every page of the fully-assembled PDF, in a single pass over the final page count.

    Done here (via direct PyMuPDF drawing on the merged document) rather than inside each of the
    three xhtml2pdf render passes (cover+notice, ToC, body) because those are rendered as three
    separate, independently-paginated documents and only merged into one afterward -- xhtml2pdf's
    own `<pdf:pagenumber/>`/`<pdf:pagecount/>` tags would each restart at 1 per pass and have no
    way to know the true final page count, which is exactly the "Page N of M" this needs to get
    right. Operating on the merged `doc` after the fact sidesteps that entirely.
    """
    display_name = _spaced_name(meta["name"])
    year = meta["publicationDate"].year if hasattr(meta["publicationDate"], "year") else int(str(meta["publicationDate"])[:4])
    running_title = f"{meta['id']} {display_name} v{meta['version']}"
    total = len(doc)

    for i, page in enumerate(doc):
        pr = page.rect
        logo_rect = fitz.Rect(
            pr.width - LOGO_MARGIN_RIGHT - LOGO_W, LOGO_MARGIN_TOP,
            pr.width - LOGO_MARGIN_RIGHT, LOGO_MARGIN_TOP + LOGO_H,
        )
        page.insert_image(logo_rect, filename=LOGO_PATH, keep_proportion=True)

        if i > 0:  # the cover page itself carries the title as its own big heading, not this line
            page.insert_text(
                (MARGIN_LEFT, HEADER_Y_FROM_TOP), running_title,
                fontsize=9, fontname="Helvetica-Oblique", color=(0, 0, 0),
            )

        footer_y = pr.height - FOOTER_Y_FROM_BOTTOM
        copyright_text = f"© TM Forum {year}. All Rights Reserved."
        page.insert_text((MARGIN_LEFT, footer_y), copyright_text, fontsize=9, fontname="Helvetica", color=(0, 0, 0))
        page_num_text = f"Page {i + 1} of {total}"
        text_w = fitz.get_text_length(page_num_text, fontname="Helvetica", fontsize=9)
        page.insert_text(
            (pr.width - MARGIN_LEFT - text_w, footer_y), page_num_text,
            fontsize=9, fontname="Helvetica", color=(0, 0, 0),
        )


def build_pdf(md_path, out_path=None, yaml_path=None, supplement_path=None):
    md_path = os.path.abspath(md_path)
    base_dir = os.path.dirname(md_path)
    out_path = out_path or os.path.splitext(md_path)[0] + ".pdf"
    yaml_path = yaml_path or _find_component_yaml(base_dir)
    supplement_path = supplement_path or (os.path.splitext(md_path)[0] + "_Supplement.md")
    if not os.path.exists(supplement_path):
        raise FileNotFoundError(
            f"No supplement file at {supplement_path} -- chapters 5.2/5.3/6 live there, hand-"
            f"maintained (see SKILL.md, 'Supplement file'). Create one from "
            f"templates/Supplement_Template.md before building the PDF."
        )

    meta = _load_component_metadata(yaml_path)

    with open(md_path, encoding="utf-8") as f:
        main_text = _strip_front_matter(f.read())
    with open(supplement_path, encoding="utf-8") as f:
        # The Component Specification Studio app writes its own `---`-delimited
        # front matter (componentMetadata name/version) at the top of the
        # Supplement file, display-only in that app -- strip it here the same
        # way the main .md's front matter is stripped, so it never leaks into
        # the assembled PDF between chapter 5.1 and 5.2.
        supplement_text = _strip_front_matter(f.read())
    text = main_text.rstrip("\n") + "\n\n" + supplement_text.lstrip("\n")
    text = _strip_source_captions(text)

    def _replace_svg(match):
        alt, rel_path = match.group(1), match.group(2)
        abs_svg = os.path.join(base_dir, rel_path)
        abs_png = _svg_to_png(abs_svg)
        rel_png = os.path.relpath(abs_png, base_dir).replace("\\", "/")
        return f"![{alt}]({rel_png})"

    text = _IMG_RE.sub(_replace_svg, text)
    headings = _extract_headings(text)

    body_html = markdown.markdown(text, extensions=["tables", "fenced_code"])
    body_html = _optimize_table_widths(body_html)

    tmp_dir = base_dir
    body_pdf_path = os.path.join(tmp_dir, "_body_tmp.pdf")
    front_pdf_path = os.path.join(tmp_dir, "_front_tmp.pdf")
    toc_pdf_path = os.path.join(tmp_dir, "_toc_tmp.pdf")
    try:
        _render_pdf(_wrap_html(body_html), body_pdf_path, base_dir)
        body_page_of = _locate_headings(body_pdf_path, headings)

        _render_pdf(_wrap_html(_build_cover_notice_html(meta)), front_pdf_path, base_dir)
        front_pages = len(fitz.open(front_pdf_path))

        toc_pages_guess = 1
        for _attempt in range(4):
            offset = front_pages + toc_pages_guess
            entries = [(0, "Notice", front_pages), (0, "Table of Contents", front_pages + 1)]
            for (depth, heading), page_idx in zip(headings, body_page_of):
                entries.append((depth * 14, heading, offset + page_idx + 1))

            toc_html = _wrap_html(_build_toc_html(entries), extra_css=f"h1{{font-size:16pt;}}{TOC_CSS}")
            _render_pdf(toc_html, toc_pdf_path, base_dir)
            actual_toc_pages = len(fitz.open(toc_pdf_path))
            if actual_toc_pages == toc_pages_guess:
                break
            toc_pages_guess = actual_toc_pages

        final = fitz.open()
        final.insert_pdf(fitz.open(front_pdf_path))
        final.insert_pdf(fitz.open(toc_pdf_path))
        final.insert_pdf(fitz.open(body_pdf_path))
        _apply_page_chrome(final, meta)
        final.save(out_path)
        final.close()
    finally:
        for p in (body_pdf_path, front_pdf_path, toc_pdf_path):
            if os.path.exists(p):
                os.remove(p)

    return out_path


if __name__ == "__main__":
    src = sys.argv[1]
    dest = sys.argv[2] if len(sys.argv) > 2 else None
    out = build_pdf(src, dest)
    print("wrote", out)
