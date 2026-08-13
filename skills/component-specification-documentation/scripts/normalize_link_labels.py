"""
ONE-OFF MIGRATION SCRIPT -- not part of the regular generation pipeline, and never called from
build_main_md.py or run_all.py. It was run exactly once (2026-08-13) per explicit user instruction to
bring every component's `<ID>_eTOM_SID_Links.md` onto one consistent label style, and is not meant to
run again as a routine step of regenerating a component's document set. A normal `generate()`/
`refresh_links_file()` run only ever touches the `YAML eTOM`/`YAML SID` cross-reference columns (see
"Every time an existing Links file is read..." in references/diagrams.md) -- it never rewrites the
`eTOM activity`/`SID ABE` label columns this script targets, so there is no risk of a routine run
silently re-normalizing anything. Keep it that way: don't wire this script into generate() or run_all.py,
and don't re-run it as a matter of course -- only if the user explicitly asks for another repo-wide
label-style pass (e.g. after a batch of new components is added with their own inconsistent styles).

Normalizes the first two (hand-maintained) columns of every component's `<ID>_eTOM_SID_Links.md` --
`eTOM activity` and `SID ABE` -- to one consistent style across the whole repo, per that instruction:
  - eTOM activity: bare activity name only, no "L2 -"/"L3 -" prefix and no leading numeric ID. A
    combined box (multiple activities merged into one visual box) keeps its " / " join, just with each
    piece reduced to its bare name.
  - SID ABE: entity name plus its own ABE/BE suffix (matching whichever suffix the underlying YAML
    token itself carries -- not force-normalized to always "ABE").

Only rows whose `YAML eTOM`/`YAML SID` cross-reference is already resolved (not `**NO MATCH**`) are
touched -- there's no reliable ground truth to re-derive a label from for a row that's still flagged,
so those are left exactly as they are, same as everything else in the file (Direction, any second
schema-deviation table, surrounding prose).

Usage: python normalize_link_labels.py [specifications_dir]
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_main_md import _split_row_cells

_SUFFIX_RE = re.compile(r"[ _](ABE|BE)$")


def _unescape(cell):
    return cell.replace("\\|", "|")


def canonical_etom_label(yaml_etom_cell):
    names = []
    for raw in _unescape(yaml_etom_cell).split("; "):
        parts = raw.split("|")
        if len(parts) < 2:
            return None
        names.append(parts[-2].replace("_", " "))
    return " / ".join(names)


def canonical_sid_label(yaml_sid_cell):
    raw = _unescape(yaml_sid_cell)
    if ";" in raw:
        return None  # a combined-box SID reference -- rare; leave it as hand-authored
    parts = raw.split("|")
    abe_tokens = parts[1:-1]
    if not abe_tokens:
        return None
    leaf = abe_tokens[-1]
    m = _SUFFIX_RE.search(leaf)
    suffix = m.group(1) if m else "ABE"
    base = _SUFFIX_RE.sub("", leaf).replace("_", " ")
    return f"{base} {suffix}"


def normalize_file(links_path):
    text = open(links_path, encoding="utf-8").read()
    all_lines = text.splitlines()
    lines, in_table, start = [], False, None
    for i, l in enumerate(all_lines):
        if l.strip().startswith("|"):
            if not in_table:
                start = i
            in_table = True
            lines.append(l)
        elif in_table:
            break
    if len(lines) < 3:
        return 0
    end = start + len(lines)

    changed = 0
    new_table_lines = lines[:2]
    for line in lines[2:]:
        cells = _split_row_cells(line)
        if len(cells) < 5:
            new_table_lines.append(line)
            continue
        etom_cell, sid_cell, direction, yaml_etom, yaml_sid = cells[:5]

        new_etom = etom_cell
        if "NO MATCH" not in yaml_etom:
            canon = canonical_etom_label(yaml_etom)
            if canon and canon != etom_cell:
                new_etom = canon
                changed += 1

        new_sid = sid_cell
        if "NO MATCH" not in yaml_sid and "external" not in yaml_sid:
            canon = canonical_sid_label(yaml_sid)
            if canon and canon != sid_cell:
                new_sid = canon
                changed += 1

        new_table_lines.append(f"| {new_etom} | {new_sid} | {direction} | {yaml_etom} | {yaml_sid} |")

    new_lines = all_lines[:start] + new_table_lines + all_lines[end:]
    with open(links_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(new_lines) + "\n")
    return changed


if __name__ == "__main__":
    specs_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    total = 0
    for path in sorted(glob.glob(os.path.join(specs_dir, "*", "Diagrams", "*_eTOM_SID_Links.md"))):
        n = normalize_file(path)
        if n:
            print(f"{path}: {n} label(s) normalized")
        total += n
    print(f"\nTotal: {total} labels normalized")
