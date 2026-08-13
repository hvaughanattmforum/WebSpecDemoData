"""
Builds a TMFCxxx component's main .md (sections 1 through 5.1) plus every diagram source/image it
references, entirely from the component's current YAML plus its hand-maintained lookup files
(eTOM/SID/FF Descriptions, eTOM-SID Links). Everything this module writes lands in Diagrams/temp/ (see
SKILL.md, "Diagrams/temp/") -- disposable, regenerated fresh every run, never itself a source of truth.
The Supplement file (5.2/5.3/6) is never touched here.

Usage:
    from build_main_md import generate
    report = generate(component_dir, component_id)
    # writes Diagrams/temp/<stem>.md and every diagram source/image; returns a report dict
"""
import glob
import json
import os
import re
import sys
import time

import httplib2
import plantuml
import yaml

sys.path.insert(0, os.path.dirname(__file__))
from build_pdf import _spaced_name, reset_temp_dir
import render_api_context_svg
import render_etom_sid_svg
import sync_diagram_yaml

# Repo-root apiIndex.json ({"TMF679_v4.0.0": {"name": "...", ...}, ...}) is the authoritative id+version
# -> display-name source for a component whose own YAML entries carry no `name` field at all (unlike the
# tmforum-rand repo's, where the main YAML's own `name` was the documented fallback). Without this, a
# first-ever sync (no prior Diagrams/temp/ file to carry a resolved name forward) would mint a
# `UNRESOLVED-<id>` placeholder for every single API.
_API_INDEX_PATH = None


def _find_api_index(component_dir):
    global _API_INDEX_PATH
    if _API_INDEX_PATH is None:
        d = component_dir
        for _ in range(4):
            candidate = os.path.join(d, "apiIndex.json")
            if os.path.exists(candidate):
                _API_INDEX_PATH = candidate
                break
            d = os.path.dirname(d)
        else:
            _API_INDEX_PATH = ""
    return _API_INDEX_PATH


def _load_api_index(component_dir):
    path = _find_api_index(component_dir)
    if not path:
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _resolve_api_name(entry, api_index):
    """Best-effort id+version -> name lookup against apiIndex.json's `TMFxxx_v<semver>` keys, tried for
    every version this entry's `specification` list carries (an integer YAML version like `5` only gives
    the major component of the index's full semver key, so match by prefix)."""
    api_id = entry["id"]
    for version_block in entry.get("specification", []) or []:
        prefix = f"{api_id}_v{version_block.get('version')}."
        for key, info in api_index.items():
            if key.startswith(prefix) and info.get("name"):
                return info["name"]
    return None


def _git_show_head(repo_root, rel_path):
    import subprocess
    try:
        result = subprocess.run(["git", "show", f"HEAD:{rel_path}"], cwd=repo_root,
                                 capture_output=True, text=True, encoding="utf-8", errors="replace")
        return result.stdout if result.returncode == 0 else None
    except Exception:
        return None


def _find_repo_root(start_dir):
    d = start_dir
    for _ in range(6):
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        d = os.path.dirname(d)
    return None


def _names_from_existing_md(existing_md_path):
    """Second-tier fallback: apiIndex.json only covers 90 of the whole TMF catalog, so scrape any
    (id, name) pair still missing after that lookup straight from the 3.2/3.3 API tables of the
    about-to-be-superseded main .md that pre-dates the Diagrams/temp/ convention -- it already resolved
    these names correctly once, from whatever process (the Component Specification Studio app)
    originally produced it. A first successful run of this skill deletes that file from the working
    tree (it's superseded, and per the current convention doesn't belong directly under Diagrams/ any
    more) -- so on any run after the first, fall back to `git show HEAD:<path>` for its pre-deletion
    content, as long as nothing's been committed since (safe within one working session on an
    uncommitted branch; stops working, silently and harmlessly, once this branch's changes are committed
    -- by then every component will already have a name-seeded Exposed/Dependant_API.yaml of its own
    from a prior run, so the gap this fallback closes won't reopen)."""
    text = None
    if os.path.exists(existing_md_path):
        text = open(existing_md_path, encoding="utf-8").read()
    else:
        repo_root = _find_repo_root(os.path.dirname(existing_md_path))
        if repo_root:
            rel_path = os.path.relpath(existing_md_path, repo_root).replace("\\", "/")
            text = _git_show_head(repo_root, rel_path)
    if not text:
        return {}
    names = {}
    for line in text.splitlines():
        m = re.match(r"\|\s*(TMF\d+)\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            names.setdefault(m.group(1), m.group(2).strip())
    return names


def _seed_api_names(component_dir, component_id, core, temp_dir, existing_md_path):
    """Write a minimal id->name seed into Diagrams/temp/ before sync_diagram_yaml.sync_all() runs, so its
    old-file name resolution has something to carry forward on a component's very first sync (or any time
    apiIndex.json/the existing .md resolves a name the main YAML itself doesn't carry)."""
    api_index = _load_api_index(component_dir)
    fallback_names = _names_from_existing_md(existing_md_path)
    for base_name, key in (("Exposed_API", "exposedAPIs"), ("Dependant_API", "dependentAPIs")):
        seed_entries = []
        for entry in core.get(key, []):
            name = _resolve_api_name(entry, api_index) or fallback_names.get(entry["id"])
            if name:
                seed_entries.append({"id": entry["id"], "name": name})
        if seed_entries:
            path = os.path.join(temp_dir, f"{component_id}_{base_name}.yaml")
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write("@startyaml\n" + yaml.dump({key: seed_entries}, sort_keys=False) + "\n@endyaml\n")

NO_DESC = "*(no description available)*"
_SUFFIX_RE = re.compile(r"[ _](ABE|BE)$")
_L2_PREFIX_RE = re.compile(r"^(?:L\d+\s*-\s*)?(\d[\d.]*\s+)?")


def esc(text):
    return (text or "").strip().replace("|", "\\|")


# ---------------------------------------------------------------------------
# YAML loading + componentMetadata list parsing (see references/diagrams.md,
# "Parsing componentMetadata lists")
# ---------------------------------------------------------------------------

def find_main_yaml(component_dir):
    matches = [f for f in glob.glob(os.path.join(component_dir, "*.yaml"))]
    if len(matches) != 1:
        raise FileNotFoundError(f"expected exactly one main YAML in {component_dir}, found {matches}")
    return matches[0]


def load_component(component_dir):
    with open(find_main_yaml(component_dir), encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    spec = doc["spec"] if "spec" in doc else doc
    return spec["componentMetadata"], spec["coreFunction"]


def parse_etom_entries(etoms):
    rows = []
    for entry in etoms or []:
        parts = entry.split("|")
        ident, name, version = parts[0], parts[1], parts[-1]
        level = "L" + str(len(ident.split(".")) - 1)
        rows.append({"id": ident, "level": level, "name": name.replace("_", " "), "version": version,
                     "raw": entry})
    return rows


def _clean_sid_token(token):
    return _SUFFIX_RE.sub("", token).replace("_", " ")


def _sid_token_suffix(token):
    """The ABE/BE suffix a raw SID token itself carries (e.g. 'Loyalty_Program_ABE' -> 'ABE'), or ''
    if it has none. Kept separate from the cleaned display name (_clean_sid_token) because the
    SID_Descriptions.md lookup files are keyed by the bare, suffix-stripped name -- only the table's
    *displayed* L1/L2 columns should show the suffix back."""
    m = _SUFFIX_RE.search(token)
    return m.group(1) if m else ""


def parse_sid_entries(sids):
    rows = []
    for entry in sids or []:
        parts = entry.split("|")
        domain, version = parts[0], parts[-1]
        abe_tokens = parts[1:-1]
        if len(abe_tokens) <= 1:
            l1_tok, l2_tok = (abe_tokens[0] if abe_tokens else ""), ""
        elif len(abe_tokens) == 2:
            l1_tok, l2_tok = abe_tokens[0], abe_tokens[1]
        else:
            # more than two ABE tokens (e.g. TMFC037/038's Patterns_Domain entries): first token is
            # Level 1, last (leaf) token is Level 2, dropping the intermediate classification tokens
            l1_tok, l2_tok = abe_tokens[0], abe_tokens[-1]
        l1, l2 = _clean_sid_token(l1_tok), _clean_sid_token(l2_tok) if l2_tok else ""
        rows.append({"domain": domain, "l1": l1, "l2": l2, "version": version, "raw": entry,
                     "l1_suffix": _sid_token_suffix(l1_tok) if l1_tok else "",
                     "l2_suffix": _sid_token_suffix(l2_tok) if l2_tok else ""})
    return rows


def parse_ff_entries(ffs):
    rows = []
    for entry in ffs or []:
        parts = entry.split("|")
        fid, name, version = parts[0], parts[1], parts[-1]
        rows.append({"id": fid, "name": name.replace("_", " "), "version": version, "raw": entry})
    return rows


def collapse_etom_l2(etom_rows):
    """One box per top-level (L2) entry for the 2.3/3.1 diagrams -- fold an L3/L4 descendant into its
    L2 ancestor's box rather than drawing it separately. An entry with no L2 ancestor in the list (should
    be rare) gets boxed on its own rather than silently dropped."""
    boxes = [r for r in etom_rows if r["level"] == "L2"]
    l2_ids = {r["id"] for r in boxes}
    for r in etom_rows:
        if r["level"] != "L2" and not any(r["id"].startswith(l2id + ".") for l2id in l2_ids):
            boxes.append(r)
    return boxes


# ---------------------------------------------------------------------------
# Hand-maintained lookup files (read-only inputs -- never written here)
# ---------------------------------------------------------------------------

_UNESCAPED_PIPE_RE = re.compile(r"(?<!\\)\|")


def _split_row_cells(line):
    """Split one Markdown table row into its cells, honoring `\\|` as a literal pipe *inside* a cell
    (used throughout these Links/Descriptions files for a raw YAML `id|name|version` citation) rather
    than a column delimiter. A naive `line.split('|')` shreds any cell containing one of those escaped
    pipes into extra fragments, silently misaligning every column after it -- this bit a first version
    of the Links-file refresh logic, which read a mangled fragment instead of the real existing value
    and concluded it wasn't a real citation."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in _UNESCAPED_PIPE_RE.split(line)]


def _load_pipe_table(path):
    """Returns (rows, confirmed_empty). rows is a list of {header: value} dicts."""
    if not os.path.exists(path):
        return [], False
    text = open(path, encoding="utf-8").read()
    lines = [l for l in text.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], "confirmed empty" in text.lower()
    header = _split_row_cells(lines[0])
    rows = []
    for line in lines[2:]:
        cells = [c.replace("\\|", "|") for c in _split_row_cells(line)]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows, False


def load_etom_desc(diagrams_dir, cid):
    rows, _ = _load_pipe_table(os.path.join(diagrams_dir, f"{cid}_eTOM_Descriptions.md"))
    return {r["Identifier"]: r for r in rows if r.get("Identifier")}


def load_ff_desc(diagrams_dir, cid):
    rows, _ = _load_pipe_table(os.path.join(diagrams_dir, f"{cid}_FF_Descriptions.md"))
    return {r["Function ID"]: r for r in rows if r.get("Function ID")}


def load_sid_desc(diagrams_dir, cid):
    """Keyed by the *stripped* (ABE/BE-suffix-free) (L1, L2) pair so a lookup by the YAML-derived
    r['l1']/r['l2'] still hits, even though the file's own 'SID ABE Level 1'/'SID ABE Level 2' column
    text now carries the suffix back on (per explicit user instruction) -- that literal column text is
    what the 2.2/2.3 table displays, this dict's key is only for matching."""
    rows, _ = _load_pipe_table(os.path.join(diagrams_dir, f"{cid}_SID_Descriptions.md"))
    out = {}
    for r in rows:
        l1 = _SUFFIX_RE.sub("", r.get("SID ABE Level 1", "")).strip()
        l2 = _SUFFIX_RE.sub("", r.get("SID ABE Level 2", "")).strip()
        out[(l1, l2)] = r
    return out


# ---------------------------------------------------------------------------
# Section 1 / 2.1 / 2.2 / 2.4 tables
# ---------------------------------------------------------------------------

def build_section1(meta):
    name = _spaced_name(meta["name"])
    # functionalBlock is concatenated the same way `name` is (e.g. "CoreCommerce") -- same spacing rule
    block = _spaced_name(meta["functionalBlock"]) if meta.get("functionalBlock") else ""
    return ("| Component Name | ID | Description | ODA Function Block |\n"
            "|---|---|---|---|\n"
            f"| {name} | {meta['id']} | {esc(meta.get('description', ''))} | {block} |")


def build_etom_table(rows, desc_lookup):
    if not rows:
        return "*(none listed in the component YAML)*"
    lines = ["| Identifier | Level | Business Activity Name | Description |", "|---|---|---|---|"]
    for r in rows:
        desc = esc(desc_lookup.get(r["id"], {}).get("Description")) or NO_DESC
        lines.append(f"| {r['id']} | {r['level']} | {r['name']} | {desc} |")
    return "\n".join(lines)


def build_sid_table(rows, desc_lookup):
    if not rows:
        return "*(none listed in the component YAML)*"
    lines = ["| SID ABE L1 | SID ABE L1 Definition | SID ABE L2 (or set of BEs) | "
              "SID ABE L2 Definition |", "|---|---|---|---|"]
    for r in rows:
        # lookup is keyed on the bare name (see load_sid_desc) -- the ABE/BE-suffixed display text
        # comes from the Descriptions file's own "SID ABE Level 1"/"SID ABE Level 2" column text
        # (per explicit user instruction), falling back to reconstructing the suffix from the YAML's
        # own raw SID token only for a row that file doesn't cover yet.
        d = desc_lookup.get((r["l1"], r["l2"]), {})
        d1 = esc(d.get("SID ABE L1 Definition")) or NO_DESC
        d2 = esc(d.get("SID ABE L2 Definition")) or NO_DESC
        l1_display = d.get("SID ABE Level 1") or (f"{r['l1']} {r['l1_suffix']}".strip() if r["l1"] else r["l1"])
        l2_display = d.get("SID ABE Level 2") or (f"{r['l2']} {r['l2_suffix']}".strip() if r["l2"] else r["l2"])
        lines.append(f"| {l1_display} | {d1} | {l2_display} | {d2} |")
    return "\n".join(lines)


def build_ff_table(rows, desc_lookup):
    if not rows:
        return "*(none listed in the component YAML)*"
    lines = ["| Function ID | Function Name | Aggregate Function L1 | Aggregate Function L2 | "
              "Function Description |", "|---|---|---|---|---|"]
    for r in rows:
        d = desc_lookup.get(r["id"], {})
        desc = esc(d.get("Function Description")) or NO_DESC
        a1 = esc(d.get("Aggregate Function Level 1")) or NO_DESC
        a2 = esc(d.get("Aggregate Function Level 2")) or NO_DESC
        lines.append(f"| {r['id']} | {r['name']} | {a1} | {a2} | {desc} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section 3.2/3.3 (API tables, <br>-joined multi-value cells) and 3.4 (Events)
# ---------------------------------------------------------------------------

def build_api_table(entries, name_map, mandatory_first):
    """One row per resource (not per API+version) -- a resource with several operations lists them
    all, comma-joined, in that one row's Operations cell."""
    header = ("| API ID | API Name | Mandatory / Optional | API Version | Resource | Operations |"
               if mandatory_first else
               "| API ID | API Name | API Version | Mandatory / Optional | Resource | Operations |")
    lines = [header, "|---|---|---|---|---|---|"]
    for e in entries:
        name = name_map.get(e["id"], e.get("name", e["id"]))
        mo = "Mandatory" if e.get("required") else "Optional"
        for version_block in e.get("specification", []) or []:
            version = version_block.get("version")
            for resource in version_block.get("resources", []) or []:
                for rname, ops in resource.items():
                    ops_cell = ", ".join(ops or [])
                    row = ([e["id"], name, mo, version, rname, ops_cell] if mandatory_first else
                           [e["id"], name, version, mo, rname, ops_cell])
                    lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def build_events_table(entries, name_map):
    if not entries:
        return "*(none listed in the component YAML)*"
    lines = ["| API ID | API Name | Event Resources |", "|---|---|---|"]
    for e in entries:
        name = name_map.get(e.get("id"), e.get("name", e.get("id", "")))
        events_cell = "<br>".join(e.get("resources", []) or [])
        lines.append(f"| {e.get('id', '')} | {name} | {events_cell} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# PlantUML rendering (public plantuml.com server -- see SKILL.md)
# ---------------------------------------------------------------------------

def _diagram_page_paths(temp_dir, component_id, base_name):
    """A paginated diagram (sync_diagram_yaml.py, past the 60-operation/event threshold) writes
    `<ID>_<base>_1.yaml`, `_2.yaml`, ... instead of the plain unnumbered file -- check for the unnumbered
    form first (the common case) before falling back to the numbered pages."""
    unnumbered = os.path.join(temp_dir, f"{component_id}_{base_name}.yaml")
    if os.path.exists(unnumbered):
        return [unnumbered]
    return sorted(glob.glob(os.path.join(temp_dir, f"{component_id}_{base_name}_*.yaml")))


def render_and_embed_diagram(temp_dir, component_id, base_name, caption_label):
    """Renders every page of a diagram source and returns the Markdown image+caption block(s) to embed
    -- one block per page, numbered "(i of N)" in both the alt text and caption once N > 1, per
    references/diagrams.md's pagination convention."""
    paths = _diagram_page_paths(temp_dir, component_id, base_name)
    if not paths:
        return ""
    n = len(paths)
    blocks = []
    for i, yaml_path in enumerate(paths, start=1):
        png_path = os.path.splitext(yaml_path)[0] + ".png"
        render_plantuml_png(open(yaml_path, encoding="utf-8").read(), png_path)
        suffix = f" ({i} of {n})" if n > 1 else ""
        blocks.append(f"![{caption_label} diagram{suffix}]({os.path.basename(png_path)})\n\n"
                      f"*(PlantUML source: [{os.path.basename(yaml_path)}]({os.path.basename(yaml_path)}))*")
    return "\n\n".join(blocks)


def render_plantuml_png(source_text, out_png_path):
    h = httplib2.Http()
    url = "http://www.plantuml.com/plantuml/img/" + plantuml.deflate_and_encode(source_text)
    last_exc = None
    for _attempt in range(3):
        try:
            resp, content = h.request(url, "GET")
            if resp.status == 200 and content[:4] == b"\x89PNG":
                with open(out_png_path, "wb") as f:
                    f.write(content)
                return
        except Exception as exc:  # pragma: no cover -- network hiccup retry
            last_exc = exc
        time.sleep(1)
    raise RuntimeError(f"PlantUML render failed for {out_png_path}: {last_exc}")


# ---------------------------------------------------------------------------
# Section 2.3 (eTOM-SID links diagram) -- refresh the YAML cross-reference
# columns of an existing Links file, then render PlantUML (<=6 elements) or
# hand-drawn SVG (>6). Never touches the hand-maintained first three columns.
# ---------------------------------------------------------------------------

_COMBO_SPLIT_RE = re.compile(r"\s+/\s+")
_EXTERNAL_RE = re.compile(r"\(([^)]*TMFC\d+[^)]*)\)\s*$")


def _strip_etom_label(piece):
    piece = piece.strip()
    piece = re.sub(r"^L\d+\s*-\s*", "", piece)
    piece = re.sub(r"^\d[\d.]*\s+", "", piece)
    return piece.strip()


def _match_etom_piece(piece, etom_rows):
    name = _strip_etom_label(piece)
    for r in etom_rows:
        if r["name"].lower() == name.lower():
            return r
    # some Links files transcribe the eTOM name in its raw YAML underscored form (e.g.
    # "Develop_Sales_Proposal") rather than the spaced display form -- compare with underscores/spaces
    # both stripped before giving up.
    despaced = _despace(name)
    for r in etom_rows:
        if _despace(r["name"]) == despaced:
            return r
    return None


def _despace(text):
    return re.sub(r"[\s_]+", "", text).lower()


def _match_sid_cell(cell, sid_rows):
    m = _EXTERNAL_RE.search(cell)
    if m:
        return "external", None
    name = cell.strip()
    # strip a trailing "ABE"/"BE" word the Links file's own label sometimes carries (e.g. "Performance
    # Threshold ABE") that the cleaned YAML SID name already dropped -- try both forms.
    name_no_suffix = re.sub(r"\s+(ABE|BE)$", "", name)
    for r in sid_rows:
        combined = (r["l1"] + " " + r["l2"]).strip()
        candidates = {name.lower(), name_no_suffix.lower()}
        targets = {r["l2"].lower(), r["l1"].lower(), combined.lower()} - {""}
        if candidates & targets:
            return "matched", r
        # labeling-convention fallback: the diagram's cylinder label is sometimes concatenated
        # camelCase (e.g. "ResourcePerformance") while the current YAML's cleaned name is space-
        # separated ("Resource Performance") or vice versa -- compare with whitespace/underscores
        # stripped from both sides before giving up.
        despaced_targets = {_despace(t) for t in targets}
        if _despace(name) in despaced_targets or _despace(name_no_suffix) in despaced_targets:
            return "matched", r
    # the cell may name only the Level-1 ABE with no Level-2 (e.g. "Customer_Product_Order_ABE"), while
    # every YAML entry for that domain happens to carry a Level-2 sub-entity -- rather than a single
    # ambiguous match, cite every YAML row sharing that Level-1, joined, instead of a false NO MATCH.
    l1_matches = [r for r in sid_rows
                  if _despace(name_no_suffix) == _despace(r["l1"]) or _despace(name) == _despace(r["l1"])]
    if l1_matches:
        return "matched_multi", l1_matches
    return "no_match", None


def _existing_cell_still_valid(cell, valid_raws):
    """A previously-resolved `YAML eTOM`/`YAML SID` cell is trusted as-is (sticky) rather than
    recomputed, as long as every raw entry it cites is still verbatim present in the component's
    current YAML list. This is what lets a manual resolution of a label the automated matcher can't
    derive on its own (an intentionally-shortened diagram-box label, see references/diagrams.md)
    survive a future re-run -- the matcher only ever downgrades a cell to `**NO MATCH**` when the
    entry it used to cite has genuinely disappeared from the YAML (real drift worth re-flagging), never
    just because it can't re-derive a match it already has by itself. `external (cross-component)`
    cells are always trusted, since they're not a claim about *this* component's YAML at all."""
    if not cell or cell == "**NO MATCH**":
        return False
    if cell == "external (cross-component)":
        return True
    pieces = [p.strip().replace("\\|", "|") for p in cell.split("; ")]
    return all(p in valid_raws for p in pieces)


def refresh_links_file(links_path, etom_rows, sid_rows):
    """Returns (rows, mismatches) where rows is a list of {etom, sid, direction, yaml_etom, yaml_sid},
    and mismatches is a list of human-readable strings for anything that didn't match -- surfaced in
    the run report, never silently dropped. The last two columns are only recomputed when the existing
    value isn't still valid (see `_existing_cell_still_valid`) -- an already-resolved cell survives
    unchanged across runs even where the automated matcher alone couldn't have derived it."""
    text = open(links_path, encoding="utf-8").read()
    all_lines = text.splitlines()
    # Only the FIRST contiguous "|"-prefixed block is the standard 5-column table -- a file may also
    # carry a second, differently-shaped table below it (e.g. a SID-to-SID or eTOM-to-eTOM schema
    # deviation, see references/diagrams.md) that must never be parsed as more rows of this one.
    lines = []
    in_table = False
    for l in all_lines:
        is_pipe = l.strip().startswith("|")
        if is_pipe:
            in_table = True
            lines.append(l)
        elif in_table:
            break

    valid_etom_raws = {r["raw"] for r in etom_rows}
    valid_sid_raws = {r["raw"] for r in sid_rows}

    rows, mismatches = [], []
    for line in lines[2:]:
        cells = _split_row_cells(line)
        if len(cells) < 3:
            continue
        etom_cell, sid_cell, direction = cells[0], cells[1], cells[2]
        existing_yaml_etom = cells[3] if len(cells) > 3 else ""
        existing_yaml_sid = cells[4] if len(cells) > 4 else ""

        if _existing_cell_still_valid(existing_yaml_etom, valid_etom_raws):
            yaml_etom = existing_yaml_etom
        else:
            etom_matches = []
            for piece in _COMBO_SPLIT_RE.split(etom_cell):
                m = _match_etom_piece(piece, etom_rows)
                if m:
                    etom_matches.append(esc(m["raw"]))
                else:
                    mismatches.append(f"eTOM piece '{piece}' in row ({etom_cell} / {sid_cell}) -- NO MATCH")
            yaml_etom = "; ".join(etom_matches) if etom_matches else "**NO MATCH**"

        if _existing_cell_still_valid(existing_yaml_sid, valid_sid_raws):
            yaml_sid = existing_yaml_sid
        else:
            kind, sid_row = _match_sid_cell(sid_cell, sid_rows)
            if kind == "external":
                yaml_sid = "external (cross-component)"
            elif kind == "matched":
                yaml_sid = esc(sid_row["raw"])
            elif kind == "matched_multi":
                yaml_sid = "; ".join(esc(r["raw"]) for r in sid_row)
            else:
                yaml_sid = "**NO MATCH**"
                mismatches.append(f"SID ABE '{sid_cell}' in row ({etom_cell} / {sid_cell}) -- NO MATCH")

        rows.append({"etom": etom_cell, "sid": sid_cell, "direction": direction,
                     "yaml_etom": yaml_etom, "yaml_sid": yaml_sid})
    return rows, mismatches


def render_etom_sid_diagram(component_id, rows, temp_dir):
    """rows: refreshed Links-file rows (etom/sid/direction). Builds node lists from the distinct
    eTOM/SID labels actually used, in first-seen order, and renders @startuml (<=6 elements) or the
    hand-drawn SVG script (>6). Returns (kind, filename) -- kind is 'puml' or 'svg'."""
    etom_keys, sid_keys = {}, {}
    for r in rows:
        etom_keys.setdefault(r["etom"], f"ETOM_{len(etom_keys)}")
        sid_keys.setdefault(r["sid"], f"SID_{len(sid_keys)}")

    total = len(etom_keys) + len(sid_keys)
    if total <= 6:
        lines = ["@startuml", "skinparam rectangle {", "  BorderStyle dashed", "}", ""]
        for label, key in etom_keys.items():
            lines.append(f'rectangle "{label}" as {key}')
        lines.append("")
        for label, key in sid_keys.items():
            lines.append(f'database "{label}" as {key}')
        lines.append("")
        for r in rows:
            ek, sk = etom_keys[r["etom"]], sid_keys[r["sid"]]
            if r["direction"] == "bidirectional":
                lines.append(f"{ek} <--> {sk}")
            elif r["direction"] == "activity produces":
                lines.append(f"{ek} --> {sk}")
            else:  # "activity consumes"
                lines.append(f"{sk} --> {ek}")
        lines += ["", "legend right", "  |= |= |",
                  "  |<#FFFFFF,dashed>| eTOM Business Activity |", "  | <database> | SID Data Entity |",
                  "  |--->| produced by the activity |", "  |<---| consumed by the activity |",
                  "endlegend", "@enduml"]
        src = "\n".join(lines)
        puml_path = os.path.join(temp_dir, f"{component_id}_eTOM_SID.puml")
        png_path = os.path.join(temp_dir, f"{component_id}_eTOM_SID.png")
        with open(puml_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(src)
        render_plantuml_png(src, png_path)
        return "puml", f"{component_id}_eTOM_SID"
    else:
        etom_entries = [{"key": k, "label": label} for label, k in etom_keys.items()]
        sid_entries = [{"key": k, "label": label} for label, k in sid_keys.items()]
        dir_map = {"bidirectional": "bidirectional", "activity produces": "produced",
                   "activity consumes": "consumed"}
        links = [{"etom": etom_keys[r["etom"]], "sid": sid_keys[r["sid"]],
                  "direction": dir_map[r["direction"]]} for r in rows]
        svg = render_etom_sid_svg.build_svg(component_id, etom_entries, sid_entries, links)
        svg_path = os.path.join(temp_dir, f"{component_id}_eTOM_SID.svg")
        with open(svg_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
        return "svg", f"{component_id}_eTOM_SID"


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def generate(component_dir, component_id, existing_pdf_stem):
    """existing_pdf_stem: the base filename (no extension) the root PDF / main .md should use, e.g.
    'TMFC005_Product_Inventory' -- reused from the existing root PDF's own filename."""
    diagrams_dir = os.path.join(component_dir, "Diagrams")
    temp_dir = reset_temp_dir(diagrams_dir)
    meta, core = load_component(component_dir)
    report = {"mismatches": [], "unresolved_apis": [], "links_status": None, "sync": None}

    existing_md_path = os.path.join(diagrams_dir, f"{existing_pdf_stem}.md")
    _seed_api_names(component_dir, component_id, core, temp_dir, existing_md_path)
    sync_report = sync_diagram_yaml.sync_all(component_dir, component_id)
    report["sync"] = sync_report["changes"]
    report["unresolved_apis"] = sync_report["unresolved"]

    def _load_diagram_yaml(base_name):
        path = os.path.join(temp_dir, f"{component_id}_{base_name}.yaml")
        if not os.path.exists(path):
            return {}
        text = open(path, encoding="utf-8").read().replace("@startyaml", "").replace("@endyaml", "")
        return yaml.safe_load(text) or {}

    exposed_diagram = _load_diagram_yaml("Exposed_API").get("exposedAPIs", [])
    dependant_diagram = _load_diagram_yaml("Dependant_API").get("dependentAPIs", [])
    name_map = {e["id"]: e["name"] for e in exposed_diagram + dependant_diagram if e.get("id")}

    # 3.4's publishedEvents/subscribedEvents can reference an API id that never appears in
    # exposedAPIs/dependentAPIs at all (e.g. TMF672 in TMFC005, consumed but not otherwise depended
    # on) -- fall back to apiIndex.json for those before falling back to the event entry's own `name`.
    api_index = _load_api_index(component_dir)
    for event_entry in (core.get("publishedEvents", []) or []) + (core.get("subscribedEvents", []) or []):
        eid = event_entry.get("id")
        if eid and eid not in name_map:
            for key, info in api_index.items():
                if key.startswith(eid + "_") and info.get("name"):
                    name_map[eid] = info["name"]
                    break

    exposed_api_block = render_and_embed_diagram(temp_dir, component_id, "Exposed_API", "Exposed API")
    dependent_api_block = render_and_embed_diagram(temp_dir, component_id, "Dependant_API", "Dependent API")
    published_events_block = render_and_embed_diagram(temp_dir, component_id, "Published_Events",
                                                        "Published Events")
    subscribed_events_block = render_and_embed_diagram(temp_dir, component_id, "Subscribed_Events",
                                                         "Subscribed Events")

    etom_rows = parse_etom_entries(meta.get("eTOMs"))
    sid_rows = parse_sid_entries(meta.get("SIDs"))
    ff_rows = parse_ff_entries(meta.get("functionalFrameworkFunctions"))
    etom_desc = load_etom_desc(diagrams_dir, component_id)
    sid_desc = load_sid_desc(diagrams_dir, component_id)
    ff_desc = load_ff_desc(diagrams_dir, component_id)

    section21 = build_etom_table(etom_rows, etom_desc)
    section22 = build_sid_table(sid_rows, sid_desc)
    section24 = build_ff_table(ff_rows, ff_desc)

    links_path = os.path.join(diagrams_dir, f"{component_id}_eTOM_SID_Links.md")
    section23_block = None
    if os.path.exists(links_path):
        text = open(links_path, encoding="utf-8").read()
        if "confirmed empty" in text.lower() and "|---|" not in text:
            report["links_status"] = "confirmed_empty"
            section23_block = ("*(no eTOM–SID diagram for this component — confirmed empty, see "
                                f"[{component_id}_eTOM_SID_Links.md]({component_id}_eTOM_SID_Links.md))*")
        else:
            rows, mismatches = refresh_links_file(links_path, etom_rows, sid_rows)
            report["mismatches"] += mismatches
            kind, stem = render_etom_sid_diagram(component_id, rows, temp_dir)
            ext = "puml" if kind == "puml" else "svg"
            section23_block = (f"![eTOM L2 - SID ABEs links diagram]({stem}.png)\n\n"
                                f"*({'PlantUML' if kind == 'puml' else 'SVG'} source: "
                                f"[{stem}.{ext}]({stem}.{ext}))*" if kind == "puml" else
                                f"![eTOM L2 - SID ABEs links diagram]({stem}.svg)\n\n"
                                f"*(SVG source: [{stem}.svg]({stem}.svg))*")
            # write the refreshed links back (only the derived columns change) -- replace just the
            # first table's line range, leaving any second table (SID-to-SID/eTOM-to-eTOM schema
            # deviation) and any surrounding prose completely untouched.
            new_table_lines = ["| eTOM activity | SID ABE | Direction | YAML eTOM | YAML SID |",
                                "|---|---|---|---|---|"]
            for r in rows:
                new_table_lines.append(f"| {r['etom']} | {r['sid']} | {r['direction']} | "
                                        f"{r['yaml_etom']} | {r['yaml_sid']} |")
            all_lines = text.splitlines()
            start = next(i for i, l in enumerate(all_lines) if l.strip().startswith("| eTOM activity"))
            end = start
            while end < len(all_lines) and all_lines[end].strip().startswith("|"):
                end += 1
            new_lines_out = all_lines[:start] + new_table_lines + all_lines[end:]
            with open(links_path, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(new_lines_out) + "\n")
            report["links_status"] = f"refreshed ({len(rows)} links, {len(mismatches)} mismatches)"
    else:
        report["links_status"] = "missing"
        if not etom_rows:
            section23_block = "*(no eTOM business activities are listed for this component in the YAML — see 2.2)*"
        else:
            section23_block = ("*(eTOM–SID Links file not yet created for this component — see "
                                "references/diagrams.md, \"If the Links file doesn't exist yet\")*")

    etom_boxes = collapse_etom_l2(etom_rows)
    etom_ctx_entries = [f"{r['id']}\n{r['name']}" for r in etom_boxes]
    sid_ctx_entries = [f"{r['l1']}\n{r['l2']}" if r["l2"] else r["l1"] for r in sid_rows]
    dependent_ctx = [{"id": e["id"], "name": name_map.get(e["id"], e.get("name", e["id"]))}
                      for e in core.get("dependentAPIs", [])]
    exposed_ctx = [{"id": e["id"], "name": name_map.get(e["id"], e.get("name", e["id"]))}
                   for e in core.get("exposedAPIs", [])]
    svg = render_api_context_svg.build_svg(
        component_id=component_id, component_name=_spaced_name(meta["name"]),
        dependent_apis=dependent_ctx, exposed_apis=exposed_ctx,
        etom_entries=etom_ctx_entries, sid_entries=sid_ctx_entries)
    with open(os.path.join(temp_dir, f"{component_id}_API_Context.svg"), "w", encoding="utf-8",
              newline="\n") as f:
        f.write(svg)

    section32 = build_api_table(core.get("exposedAPIs", []), name_map, mandatory_first=True)
    section33 = build_api_table(core.get("dependentAPIs", []), name_map, mandatory_first=False)
    section34_pub = build_events_table(core.get("publishedEvents", []), name_map)
    section34_sub = build_events_table(core.get("subscribedEvents", []), name_map)

    versions = sorted({r["version"] for r in etom_rows}) or ["*(none)*"]
    sid_versions = sorted({r["version"] for r in sid_rows}) or ["*(none)*"]
    ff_versions = sorted({r["version"] for r in ff_rows}) or ["*(none)*"]
    section51 = ("| Standard | Version(s) |\n|---|---|\n"
                 f"| eTOM | {', '.join(versions)} |\n"
                 f"| SID | {', '.join(sid_versions)} |\n"
                 f"| Functional Framework | {', '.join(ff_versions)} |")

    display_name = _spaced_name(meta["name"])
    md = f"""---
name: {display_name}
---

# {meta['id']} – {display_name}

## 1. Overview

{build_section1(meta)}

## 2. eTOM Processes, SID Data Entities and Functional Framework Functions

### 2.1. eTOM L2 - SID ABEs links

{section23_block}

### 2.2. eTOM business activities

eTOM business activities this ODA Component is responsible for:

{section21}

### 2.3. SID ABEs

SID ABEs this ODA Component is responsible for:

{section22}

### 2.4. Functional Framework Functions

{section24}

## 3. TM Forum Open APIs & Events

The following part covers the APIs and Events; this part is split in 3:
- List of Exposed APIs - This is the list of APIs available from this component.
- List of Dependent APIs - In order to satisfy the provided API, the component could require the usage of
  this set of required APIs.
- List of Events (generated & consumed) - The events which the component may generate are listed in this
  section along with a list of the events which it may consume. Since there is a possibility of multiple
  sources and receivers for each defined event.

### 3.1. API Context Diagram

![API Context diagram]({component_id}_API_Context.svg)

*(SVG source: [{component_id}_API_Context.svg]({component_id}_API_Context.svg) — hand-drawn rather than
PlantUML for this one diagram, since PlantUML's automatic layout couldn't give each API its own straight,
individually-anchored connector at a chosen height. Generated by the `component-specification-documentation`
skill's `scripts/render_api_context_svg.py`.)*

### 3.2. Exposed APIs

{section32}

{exposed_api_block}

### 3.3. Dependent APIs

{section33}

{dependent_api_block}

### 3.4. Events

The diagram illustrates the Events which the component may publish and the Events that the component may
subscribe to and then may receive. Both lists are derived from the APIs listed in the preceding sections.

#### Published Events

{section34_pub}

{published_events_block}

#### Subscribed Events

{section34_sub}

{subscribed_events_block}

## 4. Machine Readable Component Specification

Refer to the ODA Component Directory on the TM Forum website for the machine-readable component
specification files for this component.

## 5. References

### 5.1. TMF Standards related versions

{section51}
"""
    md_path = os.path.join(temp_dir, f"{existing_pdf_stem}.md")
    with open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    report["md_path"] = md_path
    return report


if __name__ == "__main__":
    component_dir = sys.argv[1]
    component_id = sys.argv[2]
    stem = sys.argv[3]
    r = generate(component_dir, component_id, stem)
    print(r)
