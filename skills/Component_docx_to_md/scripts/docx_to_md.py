"""Minimal, dependency-free DOCX -> Markdown converter.

Parses word/document.xml directly (a .docx is just a zip of XML) using only
the standard library - no pandoc, no python-docx. Handles headings
(Heading1/2/3), bold/italic runs (merged before wrapping so a phrase split
across many runs doesn't render as "**foo****bar**"), tables, hyperlinks
(resolved to real URLs via the relationships file), and inline images
(copied to a sibling "<name>_media/" folder, referenced at their original
position in the text flow).

Content wrapped in <w:sdt> (content controls - Word wraps cover pages and
auto-generated TOCs in these) and <w:hyperlink>/<w:ins>/<w:del>/<w:smartTag>
(wrapping runs - TOC entries, @mentions, pasted links) is walked into
explicitly; see SKILL.md in this skill's directory for why that matters.

Usage: python docx_to_md.py <input.docx> <output.md>
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def load_rels(zf, part_name):
    rels_path = f"{Path(part_name).parent}/_rels/{Path(part_name).name}.rels"
    try:
        data = zf.read(rels_path)
    except KeyError:
        return {}
    root = ET.fromstring(data)
    ns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    return {
        rel.get("Id"): rel.get("Target")
        for rel in root.findall(f"{ns}Relationship")
    }


def run_segments(run, rels, media_dir, media_used, link_url):
    """Yields ('text', text, bold, italic, link_url) or ('image', markdown)
    tuples, in document order, for one w:r - kept separate from markdown-
    wrapping so adjacent same-formatted runs can be merged before wrapping
    (Word splits a single visual bold phrase across many runs for
    spell-check/rsid reasons, which would otherwise produce
    "**foo****bar**" instead of "**foobar**")."""
    bold = run.find(f"{W}rPr/{W}b") is not None
    italic = run.find(f"{W}rPr/{W}i") is not None
    buf = []
    for child in run:
        tag = child.tag
        if tag == f"{W}t":
            buf.append(child.text or "")
        elif tag == f"{W}tab":
            buf.append("\t")
        elif tag == f"{W}br":
            buf.append("\n")
        elif tag == f"{W}drawing":
            if buf:
                yield ("text", "".join(buf), bold, italic, link_url)
                buf = []
            for blip in child.iter(f"{A}blip"):
                rid = blip.get(f"{R}embed")
                target = rels.get(rid)
                if target:
                    src_name = Path(target).name
                    media_used.add(src_name)
                    yield ("image", f"![]({media_dir.name}/{src_name})")
    if buf:
        yield ("text", "".join(buf), bold, italic, link_url)


def iter_runs_with_links(node, rels, link_url=None):
    """Recursively walks direct children of a paragraph (or a wrapper inside
    one), yielding (w:r element, link_url) pairs in document order.
    <w:hyperlink r:id="..."> resolves to an external URL via the
    relationships file; internal bookmark links (w:anchor, no r:id) yield
    link_url=None since there's no external target to point at."""
    for child in node:
        tag = child.tag
        if tag == f"{W}r":
            yield (child, link_url)
        elif tag == f"{W}hyperlink":
            rid = child.get(f"{R}id")
            url = rels.get(rid) if rid else None
            yield from iter_runs_with_links(child, rels, url or link_url)
        elif tag in (f"{W}ins", f"{W}del", f"{W}smartTag"):
            yield from iter_runs_with_links(child, rels, link_url)


def render_segments(segments):
    merged = []
    for seg in segments:
        if seg[0] == "text" and merged and merged[-1][0] == "text" and merged[-1][2:] == seg[2:]:
            merged[-1] = ("text", merged[-1][1] + seg[1], *seg[2:])
        else:
            merged.append(seg)
    pieces = []
    for seg in merged:
        if seg[0] == "image":
            pieces.append(seg[1])
            continue
        _, text, bold, italic, link_url = seg
        if not text:
            continue
        if bold and italic:
            text = f"***{text}***"
        elif bold:
            text = f"**{text}**"
        elif italic:
            text = f"*{text}*"
        if link_url:
            text = f"[{text}]({link_url})"
        pieces.append(text)
    return "".join(pieces)


def paragraph_text(p, rels, media_dir, media_used):
    # A <w:p> can't contain a nested <w:p>, so recursing through wrapper tags
    # (hyperlink/ins/del/smartTag) can't cross into another paragraph.
    segments = []
    for run, link_url in iter_runs_with_links(p, rels):
        segments.extend(run_segments(run, rels, media_dir, media_used, link_url))
    return render_segments(segments)


def iter_block_items(container):
    """Yields <w:p>/<w:tbl> elements in document order, descending through
    wrapper elements (<w:sdt> content controls - used for cover pages/TOC,
    <w:ins>/<w:del> - tracked-change-wrapped blocks) that aren't themselves
    paragraphs or tables but contain them."""
    for child in container:
        tag = child.tag
        if tag in (f"{W}p", f"{W}tbl"):
            yield child
        elif tag == f"{W}sdt":
            sdt_content = child.find(f"{W}sdtContent")
            if sdt_content is not None:
                yield from iter_block_items(sdt_content)
        elif tag in (f"{W}ins", f"{W}del"):
            yield from iter_block_items(child)


def paragraph_style(p):
    pStyle = p.find(f"{W}pPr/{W}pStyle")
    return pStyle.get(f"{W}val") if pStyle is not None else None


def cell_text(tc, rels, media_dir, media_used):
    parts = []
    for p in tc.findall(f"{W}p"):
        t = paragraph_text(p, rels, media_dir, media_used).strip()
        if t:
            parts.append(t)
    return "<br>".join(parts)


def table_to_md(tbl, rels, media_dir, media_used):
    rows = []
    for tr in tbl.findall(f"{W}tr"):
        cells = [cell_text(tc, rels, media_dir, media_used) for tc in tr.findall(f"{W}tc")]
        rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    lines = []
    header = rows[0]
    lines.append("| " + " | ".join(c.replace("|", "\\|") for c in header) + " |")
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for r in rows[1:]:
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in r) + " |")
    return "\n".join(lines)


HEADING_MAP = {"Heading1": "#", "Heading2": "##", "Heading3": "###", "Heading4": "####"}


def convert(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)
    media_dir = output_path.with_suffix("").parent / f"{output_path.stem}_media"

    with zipfile.ZipFile(input_path) as zf:
        rels = load_rels(zf, "word/document.xml")
        doc_xml = zf.read("word/document.xml")
        root = ET.fromstring(doc_xml)
        body = root.find(f"{W}body")

        media_dir.mkdir(parents=True, exist_ok=True)
        media_used = set()

        out_lines = []
        for el in iter_block_items(body):
            tag = el.tag
            if tag == f"{W}p":
                style = paragraph_style(el)
                text = paragraph_text(el, rels, media_dir, media_used)
                if not text.strip():
                    out_lines.append("")
                    continue
                prefix = HEADING_MAP.get(style)
                if prefix:
                    out_lines.append(f"{prefix} {text.strip()}")
                elif style == "Titlesubtitle":
                    out_lines.append(f"*{text.strip()}*")
                else:
                    out_lines.append(text)
                out_lines.append("")
            elif tag == f"{W}tbl":
                out_lines.append(table_to_md(el, rels, media_dir, media_used))
                out_lines.append("")
            elif tag == f"{W}sectPr":
                continue

        # copy only the images actually referenced, into media_dir
        for name in sorted(media_used):
            src = f"word/media/{name}"
            with zf.open(src) as f_in, open(media_dir / name, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

    md = "\n".join(out_lines)
    md = re.sub(r"\n{3,}", "\n\n", md)
    output_path.write_text(md, encoding="utf-8")
    print(f"Wrote {output_path} ({len(md)} chars), {len(media_used)} image(s) -> {media_dir}")


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
