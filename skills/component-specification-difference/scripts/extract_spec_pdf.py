"""
Extract the structured content of a TM Forum ODA component specification PDF.

Returns a dict per document (cover metadata, overview, eTOM activities, SID ABEs, Functional Framework
functions, exposed/dependent APIs, events, standards versions), which build_difference.py then compares
across two versions.

Two design decisions carry most of the weight here:

1. **Sections are located by heading TEXT, never by section number.** Successive generations of these
   documents number things differently -- one places the API context diagram in its own 3.1 subsection
   and numbers Exposed APIs 3.2, another has no such subsection and numbers Exposed APIs 3.1. Matching
   "Exposed APIs" survives that; matching "3.1" silently compares the wrong sections.

2. **A section that isn't found is recorded as absent, not as empty.** This matters more than it looks:
   if extraction quietly returns [] for a section the old document tabulates differently (its Events
   section is a diagram with no table at all), a naive diff reports every event as newly added. Callers
   must distinguish "this document has no such table" from "this table has no rows", so `sections_found`
   tracks which sections were actually located.

Column handling is deliberately mixed, because these PDFs are not uniform -- see
references/pdf_extraction.md for the full account. In short: ID-anchored tables (eTOM, Functional
Framework) are read positionally from each row's non-empty cells, because in real documents the header
labels sit in *different columns than their own data*. Tables whose column set varies between versions
(SID, APIs, events) are read by mapping header text to column index, with a positional fallback.

Usage:
    python extract_spec_pdf.py <spec.pdf> [--json out.json]
"""
import argparse
import html
import json
import os
import re

import fitz

# --- section identification: matched against heading text, case-insensitively ---
SECTION_PATTERNS = [
    ("overview", r"^\d*\.?\s*Overview$"),
    ("etoms", r"eTOM business activities"),
    ("sids", r"SID ABEs$"),
    ("etom_sid_links", r"eTOM L2\s*[-–]\s*SID ABEs links"),
    ("ffs", r"Functional Framework Functions"),
    ("apis_and_events", r"TM Forum Open APIs\s*&\s*Events"),
    ("exposed_apis", r"Exposed APIs$"),
    ("dependent_apis", r"Dependent APIs$"),
    ("events", r"^\d*\.?\d*\.?\s*Events$"),
    ("published_events", r"Published Events"),
    ("subscribed_events", r"Subscribed Events"),
    ("machine_readable", r"Machine Readable Component Specification"),
    ("standards", r"TMF Standards related versions"),
    ("jira", r"Jira References"),
    ("further_resources", r"Further resources"),
    ("version_history", r"Version History"),
    ("release_history", r"Release History"),
    ("acknowledgements", r"Acknowledge?ments"),
]
_COMPILED = [(key, re.compile(pat, re.IGNORECASE)) for key, pat in SECTION_PATTERNS]

ETOM_ID = re.compile(r"^\d+(\.\d+)+$")
FF_ID = re.compile(r"^\d{1,4}$")

HEADER_WORDS = ("identifier", "activity name", "function id", "function name", "function description",
                "aggregate function", "sid abe", "api id", "api name", "mandatory", "resource",
                "operations", "rationale", "standard", "version", "events", "component name",
                "description", "oda function block", "level")


def clean(text):
    """Collapse a PDF cell's hard line wraps into flowing prose.

    De-hyphenation runs before the newline collapse: a word broken across lines ("pre-\\norder") must
    rejoin without a space, otherwise every such word reads as "pre- order" and then shows up as a
    spurious difference between two documents that wrapped it in different places.

    Framework descriptions sometimes carry raw HTML (`&amp;`, a `<ul><li>` list) rather than plain
    prose, which would otherwise be compared -- and later rendered -- as literal markup."""
    if text is None:
        return ""
    text = str(text)
    text = re.sub(r"(?i)</\s*li\s*>", " ", text)
    text = re.sub(r"(?i)<\s*li\s*>", " - ", text)
    text = re.sub(r"<[^>]{1,80}>", " ", text)
    text = html.unescape(text)
    for bad, good in (("•", "- "), ("“", '"'), ("”", '"'),
                      ("‘", "'"), ("’", "'"), ("–", "-"), (" ", " ")):
        text = text.replace(bad, good)
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1-\2", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def _norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().rstrip("'").lower()


def _compact(row):
    return [clean(c) for c in row if clean(c)]


def _looks_like_header(row):
    joined = _norm(" ".join(str(c or "") for c in row))
    return any(re.search(rf"\b{re.escape(w)}\b", joined) for w in HEADER_WORDS)


def _walk(pdf_path):
    """Yield (section_key, table_rows) in reading order.

    Headings and tables on a page are interleaved by vertical position so that a page carrying the end
    of one section and the start of the next assigns its tables correctly. A table continuing onto later
    pages keeps the current section, since no heading intervenes."""
    doc = fitz.open(pdf_path)
    current = None
    for page in doc:
        items = []
        for block in page.get_text("blocks"):
            y0, text = block[1], clean(block[4])
            if not text or len(text) > 120:
                continue
            for key, rx in _COMPILED:
                if rx.search(text):
                    items.append((y0, "heading", key))
                    break
        for tab in page.find_tables().tables:
            items.append((tab.bbox[1], "table", (tab.extract(), page, tab.bbox)))
        for _y, kind, payload in sorted(items, key=lambda it: it[0]):
            if kind == "heading":
                current = payload
            else:
                yield (current,) + payload


def _section_api_ids(pdf_path):
    """Every TMFnnn id appearing in the text of each API section.

    A safety net for presence, independent of table parsing. Cell-level parsing can lose a row outright
    -- the older layout packs a bullet list into the operations cell and one row's id went with it --
    and a lost row would otherwise be reported as an API newly added in the other version. Comparing
    against the ids actually printed on the page stops that class of false claim, at the cost of
    occasionally including an id merely mentioned in prose."""
    doc = fitz.open(pdf_path)
    seen = {"exposed_apis": set(), "dependent_apis": set()}
    current = None
    for page in doc:
        # blocks come back in creation order, not reading order, so a table's text can arrive before the
        # heading above it and get attributed to the previous section
        for block in sorted(page.get_text("blocks"), key=lambda b: (round(b[1], 1), b[0])):
            text = clean(block[4])
            if not text:
                continue
            if len(text) <= 120:
                for key, rx in _COMPILED:
                    if rx.search(text):
                        current = key
                        break
            if current in seen:
                seen[current].update(re.findall(r"\bTMF(\d{3})\b", text))
    return {k: {f"TMF{v}" for v in vs} for k, vs in seen.items()}


def _id_anchored(rows, id_pattern, field_names):
    """Parse an ID-led table positionally from each row's non-empty cells.

    Used for the eTOM and Functional Framework tables because in real published documents
    find_tables() reports them with spurious empty columns AND with the header labels offset from
    their own data -- the FF table's "Function" header sits in column 1 while every function ID sits
    in column 0. Mapping header text to a column index therefore reads the wrong cells entirely.

    A row that doesn't lead with an ID is either a header or a continuation of the row above (a
    description that spilled across a page break)."""
    out = []
    desc_field = "description"
    for row in rows:
        cells = _compact(row)
        if not cells:
            continue
        if not id_pattern.match(cells[0]):
            if _looks_like_header(row) or all(len(c) < 24 for c in cells):
                continue
            if out:
                out[-1][desc_field] = (out[-1].get(desc_field, "") + " " + max(cells, key=len)).strip()
            continue
        rec = {"id": cells[0]}
        for name, value in zip(field_names, cells[1:]):
            rec[name] = value
        for name in field_names:
            rec.setdefault(name, "")
        out.append(rec)
    return out


def _data_rows(rows):
    return [r for r in rows if not _looks_like_header(r) and _compact(r)]


def _header_mapped(rows, wanted):
    """Map normalized header labels to column indices, then read data rows at those same indices.

    Suits tables whose column *set* legitimately differs between versions (the API tables gained a
    Version and a Rationales column; the SID table gained a definition column) -- positional reading
    can't tell which columns are present, but the header can.

    Returns (col_index_by_key, data_rows, header_seen). `header_seen` matters because a long table is
    reported by find_tables() as a separate fragment *per page*, and only the first fragment carries the
    header row -- callers reuse the mapping from that first fragment for the continuation fragments,
    which is the difference between reading 8 of 55 API rows and reading all of them."""
    if not rows:
        return {}, [], False
    header_idx = None
    for i, row in enumerate(rows[:3]):
        if _looks_like_header(row):
            header_idx = i
            break
    if header_idx is None:
        return {}, _data_rows(rows), False

    # merge only genuine header rows: a two-line header ("Function" / "ID") spans two rows, but pulling
    # in a data row would let its content decide the column mapping
    merged = {}
    for row in rows[header_idx:header_idx + 2]:
        if row is not rows[header_idx] and not _looks_like_header(row):
            break
        for j, cell in enumerate(row):
            t = clean(cell)
            if t:
                merged[j] = (merged.get(j, "") + " " + t).strip()

    cols = {}
    for key, labels in wanted.items():
        for j, text in sorted(merged.items()):
            if any(_norm(text).startswith(_norm(lbl)) for lbl in labels):
                cols[key] = j
                break
    return cols, _data_rows(rows[header_idx + 1:]), True


VERB = r"(?:GET /id|GET /\s?id|GET|POST|PATCH /id|PATCH|DELETE /id|DELETE|PUT)"
_OPS_ONLY = re.compile(rf"^{VERB}(?:\s*,\s*{VERB})*$")
_GLUED_OPS = re.compile(rf"^([A-Za-z][A-Za-z0-9]*?)((?:{VERB})(?:\s*,\s*{VERB})*)$")
_API_HEADER_CELLS = {"api id", "api name", "mandatory / optional", "mandatory/optional", "version",
                     "version(s)", "resource", "resources", "operations", "rationale", "rationales",
                     "id", "name", "events"}


def _repair_glued(cells):
    """Rejoin a resource name that a mis-detected column boundary split mid-word.

    Long tables spanning pages are reported as one fragment per page, and the column grid is detected
    independently per fragment -- one real fragment yields 'cancelServiceOr' followed by
    'derGET, GET /id, POST', i.e. the resource was cut in half and its tail glued onto the operations.
    Detect a cell that starts with a lowercase run and continues straight into HTTP verbs, split it, and
    give the head back to the preceding partial-resource cell."""
    out = []
    for c in cells:
        # resource and operations sharing one column (a column rule the renderer didn't draw on that
        # page) reads as "productSpecification GET, GET /id" -- split cleanly on the whitespace before
        # the first verb, which is unambiguous since resource names never contain spaces
        m2 = re.match(rf"^([a-z][A-Za-z0-9]*)\s+({VERB}(?:\s*,\s*{VERB})*)$", c)
        if m2:
            out.append(m2.group(1))
            out.append(m2.group(2))
            continue
        m = _GLUED_OPS.match(c)
        if m and not _OPS_ONLY.match(c):
            head, ops = m.group(1), m.group(2)
            if out and re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", out[-1]) and not re.search(VERB, out[-1]):
                out[-1] += head
            elif head:
                out.append(head)
            out.append(ops)
        else:
            out.append(c)
    return out


def _is_api_header_row(cells):
    return any(_norm(c) in _API_HEADER_CELLS for c in cells)


def _classify_api_row(cells):
    """Identify each field by what it looks like rather than by which column it landed in.

    Column positions are unreliable across page fragments (see _repair_glued), but the vocabulary here
    is tightly constrained -- TMF ids, Mandatory/Optional, short numeric versions, HTTP verbs, camelCase
    resource names -- so classifying by content is far more robust than trusting the grid."""
    rest = list(cells)

    def take(pred):
        for i, c in enumerate(rest):
            if pred(c):
                return rest.pop(i)
        return ""

    api_id = take(lambda c: re.fullmatch(r"TMF\d{3}", c))
    flag = take(lambda c: _norm(c) in ("mandatory", "optional"))
    version = take(lambda c: re.fullmatch(r"\d+(?:\.\d+){0,2}", c) and len(c) <= 6)
    operations = take(lambda c: bool(_OPS_ONLY.match(c)))
    if not operations:
        operations = take(lambda c: bool(re.search(VERB, c)) and len(c) < 120)
    name = take(lambda c: " " in c and ("api" in _norm(c) or _norm(c).endswith("management")))
    resource = take(lambda c: bool(re.fullmatch(r"[a-z][A-Za-z0-9]*", c)))
    rationale = max(rest, key=len) if rest else ""
    return {"id": api_id, "name": name, "flag": flag, "version": version,
            "resource": resource, "operations": operations, "rationale": rationale}


def _parse_api_section(rows, carry):
    """Rows for one fragment of an exposed/dependent API table.

    `carry` holds the last seen id/name/flag/version so continuation rows -- which blank those cells
    when they repeat -- attribute to the right API."""
    out = []
    for row in rows:
        cells = _repair_glued(_compact(row))
        if not cells or _is_api_header_row(cells):
            continue
        rec = _classify_api_row(cells)
        # `name` is deliberately NOT carried. A continuation row blanks the id and the name together,
        # so carrying the name means that if a row is ever attributed to the wrong API the name follows
        # it -- which is how TMF701 came to be labelled "Resource Ordering Management API". Names are
        # instead resolved per API id from the rows that actually state one.
        for k in ("id", "flag", "version"):
            if rec[k]:
                carry[k] = rec[k]
            else:
                rec[k] = carry.get(k, "")
        # Keep a row that names an API even when its resource and operations couldn't be parsed. The
        # older layout packs a whole bullet list into one cell, which no amount of classification will
        # split reliably -- but the API is unambiguously present in the document, and dropping the row
        # would report it as newly added in the comparison, which is worse than having no detail for it.
        if not (rec["id"] or rec["resource"] or rec["operations"]):
            continue
        # Flag rows whose resource/operations text can't be trusted. When find_tables() mis-places a
        # column boundary, pymupdf interleaves the two neighbouring cells' characters by x position
        # ('productOfferingPrice' + 'GET' -> 'productOfferingP' + 'ricGeET'), which is not recoverable
        # afterwards. Marking the row lets the comparison stay silent about resource-level detail
        # instead of reporting a truncated name as a change.
        rec["resource_confident"] = bool(
            rec["resource"] and (not rec["operations"] or _OPS_ONLY.match(rec["operations"])))
        out.append(rec)
    return out


def _parse_event_section(rows):
    """Event rows: an API id/name plus a comma-separated event list. Event names are recognisable in
    their own right (they end in Event, or are the odd StateChange), so the list is recovered by token
    rather than by relying on the cell boundaries surviving pagination."""
    out = []
    for row in rows:
        cells = _compact(row)
        if not cells or _is_api_header_row(cells):
            continue
        api_id = next((c for c in cells if re.fullmatch(r"TMF\d{3}", c)), "")
        name = next((c for c in cells if " " in c and "api" in _norm(c)), "")
        version = next((c for c in cells if re.fullmatch(r"[\d.,\s]+", c) and any(ch.isdigit() for ch in c)), "")
        events = []
        for c in cells:
            for tok in re.split(r"[,\s]+", c):
                tok = tok.strip()
                if tok.endswith("Event") or tok.endswith("StateChange") or tok.endswith("Change"):
                    if tok not in events:
                        events.append(tok)
        if events:
            out.append({"id": api_id, "name": name, "version": version, "events": events})
    return out


def _cell(row, cols, key):
    j = cols.get(key)
    if j is None or j >= len(row):
        return ""
    return clean(row[j])


def _cover(doc):
    """Cover-page metadata. Present in the officially published PDFs; a Confluence-style export has a
    plain title page instead, so every field is optional."""
    text = clean(doc[0].get_text()) if doc.page_count else ""
    def grab(label):
        m = re.search(rf"{label}\s*:?\s*([^:]*?)(?=\s+(?:Maturity Level|Team Approved Date|Release "
                      rf"Status|Approval Status|Version|IPR Mode)\b|$)", text, re.IGNORECASE)
        return clean(m.group(1)) if m else ""
    return {k: v for k, v in {
        "maturity_level": grab("Maturity Level"),
        "team_approved_date": grab("Team Approved Date"),
        "release_status": grab("Release Status"),
        "approval_status": grab("Approval Status"),
        "ipr_mode": grab("IPR Mode"),
    }.items() if v}


def _version(doc, pdf_path):
    """Version from the running header/cover ("TMFC003 ... v2.0.0" / "Version 2.0.0"), falling back to
    the filename. The header is preferred because a file can be renamed."""
    probe = " ".join(clean(doc[p].get_text()) for p in range(min(3, doc.page_count)))
    for rx in (r"\bv(\d+\.\d+\.\d+)\b", r"\bVersion\s+(\d+\.\d+\.\d+)\b"):
        m = re.search(rx, probe)
        if m:
            return m.group(1)
    m = re.search(r"v(\d+\.\d+\.\d+)", os.path.basename(pdf_path))
    return m.group(1) if m else ""


def extract(pdf_path):
    doc = fitz.open(pdf_path)
    probe = " ".join(clean(doc[p].get_text()) for p in range(min(3, doc.page_count)))
    cid = (re.search(r"\b(TMFC\d{3})\b", probe) or [None, ""])[1] if re.search(r"\b(TMFC\d{3})\b", probe) else ""

    result = {
        "source_file": os.path.basename(pdf_path),
        "component_id": cid,
        "version": _version(doc, pdf_path),
        "pages": doc.page_count,
        "cover": _cover(doc),
        "overview": {},
        "etoms": [], "sids": [], "ffs": [],
        "exposed_apis": [], "dependent_apis": [],
        "published_events": [], "subscribed_events": [],
        "standards": {},
        "sections_found": [],
        "notes": [],
    }

    # a long table arrives as one fragment per page and only the first carries a header, so the column
    # mapping learned from that first fragment is reused by its continuation fragments
    cols_cache = {}
    # last seen id/name/flag/version per API section, so continuation rows across page fragments still
    # attribute to the right API
    api_carry = {}

    def mapped(section, rows, wanted):
        cols, data, header_seen = _header_mapped(rows, wanted)
        if header_seen and cols:
            cols_cache[section] = cols
        elif not cols and section in cols_cache:
            cols = cols_cache[section]
        return cols, data

    for section, rows, page, bbox in _walk(pdf_path):
        if section and section not in result["sections_found"]:
            result["sections_found"].append(section)

        if section == "overview":
            cols, data = mapped(section, rows, {
                "name": ["Component Name"], "id": ["ID"],
                "description": ["Description"], "block": ["ODA Function Block", "ODA Function"]})
            for row in data:
                desc = _cell(row, cols, "description")
                name = _cell(row, cols, "name")
                block = _cell(row, cols, "block")
                if not desc:
                    # header labels offset from their own data, as elsewhere in the older documents:
                    # fall back to the row's non-empty cells, where the description is by far the
                    # longest and the component id is recognisable on sight
                    compact = [c for c in _compact(row) if not re.fullmatch(r"TMFC\d{3}", c)]
                    if len(compact) >= 2:
                        desc = max(compact, key=len)
                        rest = [c for c in compact if c is not desc]
                        name = name or (rest[0] if rest else "")
                        block = block or (rest[-1] if len(rest) > 1 else "")
                if desc:
                    result["overview"] = {"component_name": name, "description": desc,
                                          "function_block": block}
                    break

        elif section == "etoms":
            result["etoms"] += _id_anchored(rows, ETOM_ID, ["level", "name", "description"])

        elif section == "sids":
            cols, data = mapped(section, rows, {
                "l1": ["SID ABE Level 1"], "definition": ["SID ABE L1 Definition", "Definition"],
                "l2": ["SID ABE Level 2"]})
            last_l1 = last_def = ""
            for row in data:
                compact = _compact(row)
                # An explicit "none" row is the old documents' way of saying this component owns no SID
                # ABEs. Recording it as a note rather than as zero rows keeps the diff honest: "the old
                # document said none" is a different statement from "the old document wasn't parsed".
                if len(compact) == 1 and _norm(compact[0]) == "none":
                    result["notes"].append('2.2 SID ABEs table states "none"')
                    continue
                l1 = _cell(row, cols, "l1")
                definition = _cell(row, cols, "definition")
                l2 = _cell(row, cols, "l2")
                if not (l1 or l2):
                    # header labels offset from their own data (seen in the older documents) -- fall back
                    # to reading the row's non-empty cells positionally
                    if len(compact) >= 3:
                        l1, definition, l2 = compact[0], compact[1], compact[2]
                    elif len(compact) == 2:
                        l1, l2 = compact[0], compact[1]
                    elif len(compact) == 1:
                        l1 = compact[0]
                l1 = l1 or last_l1
                definition = definition or (last_def if l1 == last_l1 else "")
                if not (l1 or l2):
                    continue
                result["sids"].append({"l1": l1, "l2": l2, "definition": definition})
                last_l1, last_def = l1, definition

        elif section == "ffs":
            result["ffs"] += _id_anchored(rows, FF_ID, ["name", "description", "af1", "af2"])

        elif section in ("exposed_apis", "dependent_apis"):
            result[section] += _parse_api_section(rows, api_carry.setdefault(section, {}))

        elif section in ("published_events", "subscribed_events"):
            result[section] += _parse_event_section(rows)

        elif section == "standards":
            cols, data = mapped(section, rows, {"standard": ["Standard"], "version": ["Version"]})
            for row in data:
                std, ver = _cell(row, cols, "standard"), _cell(row, cols, "version")
                if not (std and ver):
                    # same header-offset fallback as the SID table
                    compact = _compact(row)
                    if len(compact) >= 2:
                        std, ver = compact[0], compact[1]
                if std and ver and _norm(std) != "standard":
                    result["standards"][std] = ver

    if "events" in result["sections_found"] and not (result["published_events"]
                                                     or result["subscribed_events"]):
        result["notes"].append("Events section present but contains no table (diagram only)")
    result["api_ids_seen"] = {k: sorted(v) for k, v in _section_api_ids(pdf_path).items()}
    for key in ("exposed_apis", "dependent_apis"):
        parsed = {r["id"] for r in result[key] if r.get("id")}
        unparsed = sorted(set(result["api_ids_seen"].get(key, [])) - parsed)
        if unparsed:
            result["notes"].append(
                f"{key}: {', '.join(unparsed)} appear in the section text but no table row could be "
                f"parsed for them")
        shaky = sum(1 for r in result[key] if not r.get("resource_confident"))
        if shaky:
            result["notes"].append(
                f"{key}: {shaky} of {len(result[key])} rows had unreliable resource/operation text "
                f"(mis-detected table column boundary)")
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf")
    ap.add_argument("--json", help="write the extraction to this path")
    args = ap.parse_args()
    data = extract(args.pdf)
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"{data['source_file']}  {data['component_id']} v{data['version']} ({data['pages']}pp)")
    for key in ("etoms", "sids", "ffs", "exposed_apis", "dependent_apis",
                "published_events", "subscribed_events"):
        print(f"  {key:<18} {len(data[key])}")
    print(f"  standards          {data['standards']}")
    print(f"  sections found     {', '.join(data['sections_found'])}")
    for n in data["notes"]:
        print(f"  note: {n}")


if __name__ == "__main__":
    main()
