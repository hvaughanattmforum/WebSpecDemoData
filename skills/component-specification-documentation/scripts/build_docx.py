"""
Render a component-specification-documentation .md file (+ its sibling _Supplement.md) to a
.docx, mirroring build_pdf.py's cover/notice/table-of-contents assembly but targeting Word
instead of PDF.

Why two languages: docx-js (npm `docx`) is the recommended way to *create* a .docx from
scratch (see the `docx` skill) -- python-docx would work too, but docx-js's native
`TableOfContents` field means Word computes and updates page numbers itself on open, instead
of needing the fixed-point page-location dance build_pdf.py has to do for xhtml2pdf. So this
script does the YAML/Markdown/image work in Python (reusing build_pdf.py's helpers directly
rather than re-implementing them), serializes the result to JSON, and hands that to
build_docx.js to actually assemble the .docx.

The .md files themselves are never modified -- same as build_pdf.py.

Usage:
    python build_docx.py path/to/TMFCxxx_Name.md [output.docx]
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pdf import (
    LOGO_PATH,
    NOTICE_TEXT,
    TMF_RED,
    _approval_status,
    _find_component_yaml,
    _load_component_metadata,
    _maturity_level,
    _spaced_name,
    _strip_front_matter,
    _svg_to_png,
)

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

_HEADING_RE = re.compile(r'^(#{1,4})\s+(.+?)\s*$')
_IMAGE_RE = re.compile(r'^!\[([^\]]*)\]\(([^)\s]+)\)\s*$')
_TABLE_ROW_RE = re.compile(r'^\|(.+)\|\s*$')
_TABLE_SEP_RE = re.compile(r'^\|[\s:|-]+\|\s*$')
_BULLET_RE = re.compile(r'^(\s*)-\s+(.+)$')
_INLINE_RE = re.compile(r'(\*\*.+?\*\*|`[^`]+`)')
_ESCAPED_STAR = ""

MIN_COL_PCT = 8
MAX_CELL_SAMPLE = 40


def _unescape_placeholder(text):
    return text.replace(_ESCAPED_STAR, "*")


def _parse_inline(text):
    """Bold (**) and inline code (`) only -- the only inline markup this document's prose
    actually uses. Links are flattened to their display text: relative paths (diagram
    source files) aren't meaningful as Word hyperlinks, so there's nothing worth preserving
    by keeping them clickable."""
    text = text.replace("\\*", _ESCAPED_STAR)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    runs = []
    pos = 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > pos:
            runs.append({"text": _unescape_placeholder(text[pos:m.start()])})
        token = m.group(0)
        if token.startswith("**"):
            runs.append({"text": _unescape_placeholder(token[2:-2]), "bold": True})
        else:
            runs.append({"text": _unescape_placeholder(token[1:-1]), "code": True})
        pos = m.end()
    if pos < len(text):
        runs.append({"text": _unescape_placeholder(text[pos:])})
    return runs or [{"text": ""}]


def _cell_weight(cell_text):
    return min(len(cell_text), MAX_CELL_SAMPLE)


def _col_widths_pct(header, rows):
    n_cols = len(header)
    weight = [max(1, _cell_weight(header[j])) for j in range(n_cols)]
    for row in rows:
        for j in range(min(n_cols, len(row))):
            weight[j] = max(weight[j], _cell_weight(row[j]))
    budget = 100 - MIN_COL_PCT * n_cols
    total = sum(weight)
    pct = [MIN_COL_PCT + budget * (w / total) for w in weight]
    pct_int = [int(round(p)) for p in pct]
    pct_int[-1] += 100 - sum(pct_int)
    return pct_int


def _parse_blocks(text, base_dir):
    """Parses the specific Markdown subset this skill's own generator emits: headings
    (#-####), pipe tables, image lines (optionally followed by an italic caption
    paragraph), bullet lists (with a "  - " nested level and plain continuation lines),
    and plain paragraphs. Not a general CommonMark parser -- it doesn't need to be one."""
    lines = text.split("\n")
    n = len(lines)
    blocks = []
    i = 0
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        m = _HEADING_RE.match(line)
        if m:
            hashes, htext = m.groups()
            blocks.append({"type": "heading", "level": len(hashes), "runs": _parse_inline(htext)})
            i += 1
            continue

        m = _IMAGE_RE.match(line)
        if m:
            alt, rel_path = m.groups()
            abs_path = os.path.join(base_dir, rel_path)
            if abs_path.lower().endswith(".svg"):
                abs_path = _svg_to_png(abs_path)
            blocks.append({"type": "image", "alt": alt, "path": abs_path})
            i += 1
            continue

        if _TABLE_ROW_RE.match(line) and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and _TABLE_ROW_RE.match(lines[i]):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            blocks.append({
                "type": "table",
                "header": [_parse_inline(c) for c in header],
                "rows": [[_parse_inline(c) for c in row] for row in rows],
                "colWidthsPct": _col_widths_pct(header, rows),
            })
            continue

        if _BULLET_RE.match(line):
            items = []
            while i < n and lines[i].strip():
                bm = _BULLET_RE.match(lines[i])
                if bm:
                    indent, itext = bm.groups()
                    items.append({"level": len(indent) // 2, "text": itext})
                    i += 1
                elif lines[i].startswith((" ", "\t")) and items:
                    items[-1]["text"] += " " + lines[i].strip()
                    i += 1
                else:
                    break
            blocks.append({"type": "list", "items": [
                {"level": it["level"], "runs": _parse_inline(it["text"])} for it in items
            ]})
            continue

        para_lines = [line.strip()]
        i += 1
        while (i < n and lines[i].strip() and not _HEADING_RE.match(lines[i])
               and not _IMAGE_RE.match(lines[i]) and not _TABLE_ROW_RE.match(lines[i])
               and not _BULLET_RE.match(lines[i])):
            para_lines.append(lines[i].strip())
            i += 1
        para_text = " ".join(para_lines)
        italic = para_text.startswith("*(") and para_text.endswith(")*")
        if italic:
            para_text = para_text[2:-2]
        blocks.append({"type": "para", "runs": _parse_inline(para_text), "italic": italic})

    return blocks


# Same alternating red/black convention as build_pdf.py's BASE_CSS (h1/h2 red, h3 black,
# h4 red) -- see build_pdf.py's comment above BASE_CSS for why it alternates by depth.
def _heading_color(level):
    return {1: TMF_RED, 2: TMF_RED, 3: "000000", 4: TMF_RED}[level].lstrip("#")


def build_docx(md_path, out_path=None, yaml_path=None, supplement_path=None):
    md_path = os.path.abspath(md_path)
    base_dir = os.path.dirname(md_path)
    out_path = out_path or os.path.splitext(md_path)[0] + ".docx"
    yaml_path = yaml_path or _find_component_yaml(base_dir)
    supplement_path = supplement_path or (os.path.splitext(md_path)[0] + "_Supplement.md")
    if not os.path.exists(supplement_path):
        raise FileNotFoundError(
            f"No supplement file at {supplement_path} -- chapters 5.2/5.3/6 live there, hand-"
            f"maintained (see SKILL.md, 'Supplement file'). Create one from "
            f"templates/Supplement_Template.md before building the Word doc."
        )

    meta = _load_component_metadata(yaml_path)

    with open(md_path, encoding="utf-8") as f:
        main_text = _strip_front_matter(f.read())
    with open(supplement_path, encoding="utf-8") as f:
        supplement_text = _strip_front_matter(f.read())

    title_match = re.search(r'^#\s+(.+?)\s*$', main_text, re.MULTILINE)
    body_text = main_text[title_match.end():] if title_match else main_text
    text = body_text.rstrip("\n") + "\n\n" + supplement_text.lstrip("\n")

    blocks = _parse_blocks(text, base_dir)
    for b in blocks:
        if b["type"] == "heading":
            b["color"] = _heading_color(b["level"])

    status = meta["status"]
    pub_date = meta["publicationDate"]
    year = pub_date.year if hasattr(pub_date, "year") else int(str(pub_date)[:4])
    team_approved_date = (
        pub_date.strftime("%d-%b-%Y") if hasattr(pub_date, "strftime") else str(pub_date)
    )
    display_name = _spaced_name(meta["name"])

    payload = {
        "outPath": out_path,
        "logoPath": LOGO_PATH,
        "docTitle": f"{meta['id']} – {display_name}",
        "runningTitle": f"{meta['id']} {display_name} v{meta['version']}",
        "cover": {
            "displayName": display_name,
            "id": meta["id"],
            "maturityLevel": _maturity_level(status),
            "teamApprovedDate": team_approved_date,
            "releaseStatus": str(status).capitalize(),
            "approvalStatus": _approval_status(status),
            "version": str(meta["version"]),
        },
        "notice": {
            "year": year,
            "paragraphs": [
                html.unescape(re.sub(r'<[^>]+>', '', p)).strip()
                for p in NOTICE_TEXT.format(year=year).replace("<br/>", "\n").split("</p>")
                if re.sub(r'<[^>]+>', '', p).strip()
            ],
        },
        "blocks": blocks,
    }

    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8", dir=base_dir
    ) as f:
        json.dump(payload, f)
        payload_path = f.name

    try:
        subprocess.run(
            ["node", os.path.join(SCRIPTS_DIR, "build_docx.js"), payload_path],
            check=True,
        )
    finally:
        os.remove(payload_path)

    return out_path


if __name__ == "__main__":
    src = sys.argv[1]
    dest = sys.argv[2] if len(sys.argv) > 2 else None
    out = build_docx(src, dest)
    print("wrote", out)
