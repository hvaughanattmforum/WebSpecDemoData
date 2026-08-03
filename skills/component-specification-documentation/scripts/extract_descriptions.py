"""One-off/reusable extractor: pulls eTOM business-activity descriptions and Functional
Framework function descriptions (+ aggregate function levels) out of a versioned component
docx (the officially-published TMFCxxx <Name> vX.Y.Z.docx files), by header-matching the
'2.1 eTOM business activities' and '2.4 Functional Framework Functions' tables.

Usage:
    python extract_descriptions.py <path-to-docx>
Prints a JSON blob: {"etom": {id: description}, "ff": {id: {"description":, "agg1":, "agg2":}}}
"""
import sys
import json
import docx
from docx.oxml.ns import qn
from docx.table import Table


def _walk_tables(body):
    P = qn("w:p")
    TBL = qn("w:tbl")

    def walk(elm):
        for child in elm:
            tag = child.tag
            if tag == TBL:
                yield child
            elif tag.endswith("}sdt"):
                content = child.find(qn("w:sdtContent"))
                if content is not None:
                    yield from walk(content)
            elif tag.endswith("}sdtContent"):
                yield from walk(child)
            elif tag == P:
                continue

    yield from walk(body)


def _cell_text(cell):
    # join multi-paragraph cell content with " / ", matching the dump convention used
    # elsewhere in this skill so descriptions read the same as other transcribed tables
    return " / ".join(p.strip() for p in cell.text.split("\n") if p.strip()).strip()


def extract(docx_path):
    d = docx.Document(docx_path)
    etom = {}
    ff = {}
    for tbl_el in _walk_tables(d.element.body):
        tbl = Table(tbl_el, d)
        if not tbl.rows:
            continue
        header = [c.text.strip() for c in tbl.rows[0].cells]
        header_norm = [h.lower() for h in header]

        if header_norm[:4] == ["identifier", "level", "business activity name", "description"]:
            for row in tbl.rows[1:]:
                cells = row.cells
                ident = cells[0].text.strip()
                desc = _cell_text(cells[3])
                if ident and desc:
                    etom[ident] = desc

        elif header_norm and header_norm[0] == "function id" and any("function description" in h for h in header_norm):
            desc_idx = next(i for i, h in enumerate(header_norm) if "function description" in h)
            # tolerate real-world header variance across the 13 versioned docs: "Aggregate"
            # vs typo "Aggegate", "Function" vs "Functions", extra "Sub-Domain Functions
            # Level N" line prepended, "AF L1/L2 Id" sibling columns interleaved — match on
            # "aggregat|aggegat" + "level 1"/"level 2" appearing together in one cell
            agg1_idx = next(
                (i for i, h in enumerate(header_norm)
                 if ("aggregat" in h or "aggegat" in h) and "level 1" in h), None)
            agg2_idx = next(
                (i for i, h in enumerate(header_norm)
                 if ("aggregat" in h or "aggegat" in h) and "level 2" in h), None)
            for row in tbl.rows[1:]:
                cells = row.cells
                fid = cells[0].text.strip()
                if not fid:
                    continue
                desc = _cell_text(cells[desc_idx]) if desc_idx < len(cells) else ""
                # agg1/agg2 cells are sometimes multi-paragraph too (e.g. TMFC040's "Product Usage
                # Management\nRating and Follow up") — must go through _cell_text the same as desc,
                # or a raw embedded "\n" breaks the one-row-per-line markdown table on write-out
                agg1 = _cell_text(cells[agg1_idx]) if agg1_idx is not None and agg1_idx < len(cells) else ""
                agg2 = _cell_text(cells[agg2_idx]) if agg2_idx is not None and agg2_idx < len(cells) else ""
                ff[fid] = {"description": desc, "agg1": agg1, "agg2": agg2}

    return {"etom": etom, "ff": ff}


if __name__ == "__main__":
    result = extract(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
