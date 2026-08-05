"""
Fill the missing descriptions in a component's eTOM / Functional Framework lookup files from the official
framework releases.

Implements the standing precedence rule (see SKILL.md and references/diagrams.md):

  1. The component's own TMFCnnn document wins for any id it covers -- even where its wording differs
     from the framework's. A difference is expected, not something to reconcile.
  2. Where the component document has no description, take the framework's default.
  3. Only where neither source has the id does the cell stay `*(no description available)*`.

So this script **only ever replaces placeholder rows**. Existing transcribed descriptions are left
byte-for-byte alone, which is what makes it safe to re-run: filling a gap is not the same as regenerating
a hand-maintained file, and the "never regenerate" rule that protects those files still holds.

Each id is looked up in the release *its own YAML entry pins it to* -- a component's list is routinely
mixed, and the same id can exist in several releases with different wording.

Usage:
    python fill_descriptions_from_frameworks.py --component-dir <TMFCxxx folder> \
        --frameworks <framework releases folder> [--apply]

Without --apply it reports what would change and writes nothing.
"""
import argparse
import glob
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framework_lookup import (escape_cell, load_etom_descriptions, load_ff_descriptions,
                              norm_version)

PLACEHOLDER = "*(no description available)*"


def component_metadata(component_dir):
    matches = [p for p in glob.glob(os.path.join(component_dir, "*.yaml"))]
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one component YAML in {component_dir}, found {len(matches)}")
    with open(matches[0], encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    return doc.get("spec", doc)["componentMetadata"], matches[0]


def parse_entries(entries):
    """[(id, name, version)] from componentMetadata's pipe-delimited strings.

    The name is the second-to-last field rather than index 1: a malformed entry with an extra spliced-in
    field still has its real name immediately before the version."""
    out = []
    for raw in entries or []:
        parts = [p.strip() for p in str(raw).split("|")]
        if len(parts) >= 3:
            out.append((parts[0], parts[-2], parts[-1]))
        elif len(parts) == 2:
            out.append((parts[0], parts[1], ""))
    return out


def fill_file(path, wanted, loader, frameworks, columns, label):
    """Replace placeholder rows in one lookup file. Returns (filled, still_missing, kept)."""
    if not os.path.exists(path):
        print(f"  {label}: no lookup file at {os.path.basename(path)} — nothing to fill")
        return [], [], 0

    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    caches = {}
    filled, missing, kept = [], [], 0
    out = []
    for line in lines:
        m = re.match(r"^\|\s*([0-9][0-9.]*)\s*\|(.*)$", line)
        if not m:
            out.append(line)
            continue
        entry_id, rest = m.group(1), m.group(2)
        if PLACEHOLDER not in rest:
            kept += 1
            out.append(line)
            continue
        version = next((v for (i, _n, v) in wanted if i == entry_id), "")
        if not version:
            missing.append((entry_id, "not in the component YAML"))
            out.append(line)
            continue
        key = norm_version(version)
        if key not in caches:
            try:
                caches[key] = loader(frameworks, version)
            except (FileNotFoundError, RuntimeError) as exc:
                caches[key] = ({}, str(exc), "")
        index, source, _sheet = caches[key]
        rec = index.get(entry_id)
        if not rec or not rec.get("description"):
            missing.append((entry_id, f"absent from {source}"))
            out.append(line)
            continue
        cells = [escape_cell(rec.get(c, "")) or PLACEHOLDER for c in columns]
        out.append(f"| {entry_id} | " + " | ".join(cells) + " |")
        filled.append((entry_id, source))

    if filled:
        sources = sorted({s for _i, s in filled})
        for i, line in enumerate(out):
            if line.startswith("Source:"):
                out[i] = (line.rstrip() + f" Descriptions for {len(filled)} id(s) with no entry in that "
                          f"document were taken from the official framework release each id is pinned "
                          f"to in the component YAML: {', '.join(sources)}.")
                break
    return filled, missing, kept, "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--component-dir", required=True)
    ap.add_argument("--frameworks", required=True,
                    help="folder holding the GB921/GB922/GB1033 releases (ask the user; it is not in "
                         "this repository)")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.frameworks):
        raise SystemExit(f"frameworks folder not found: {args.frameworks}")

    meta, yaml_path = component_metadata(args.component_dir)
    cid = meta["id"]
    diagrams = os.path.join(args.component_dir, "Diagrams")
    print(f"{cid}  ({os.path.basename(yaml_path)})")

    jobs = (
        ("eTOM", f"{cid}_eTOM_Descriptions.md", parse_entries(meta.get("eTOMs")),
         load_etom_descriptions, ["description"]),
        ("Functional Framework", f"{cid}_FF_Descriptions.md",
         parse_entries(meta.get("functionalFrameworkFunctions")),
         load_ff_descriptions, ["description", "af1", "af2"]),
    )

    for label, filename, wanted, loader, columns in jobs:
        path = os.path.join(diagrams, filename)
        result = fill_file(path, wanted, loader, args.frameworks, columns, label)
        if len(result) == 3:
            continue
        filled, missing, kept, text = result
        print(f"  {label}: {kept} kept from the component document, {len(filled)} filled from the "
              f"frameworks, {len(missing)} still missing")
        for entry_id, why in missing:
            print(f"      {entry_id}: {why}")
        if filled and args.apply:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print(f"      wrote {os.path.basename(path)}")

    if not args.apply:
        print("\n(dry run — pass --apply to write)")


if __name__ == "__main__":
    main()
