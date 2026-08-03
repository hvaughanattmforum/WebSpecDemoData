"""
Align a component's eTOM and Functional Framework entry names to the official framework JSON definitions.

`componentMetadata.eTOMs` and `.functionalFrameworkFunctions` hold pipe-delimited `id|Name|version`
strings, and the framework JSON carries a `token` field that is exactly that underscore form
(`Customer_Order_Change_Management`). Alignment is therefore a direct token-to-token comparison -- no
prose matching, no fuzzy logic, and case-sensitive, which matters: one real mismatch was
`Retro-active_order_orchestration` against `Retro-active_Order_Orchestration`, differing only in case and
invisible to a case-insensitive check.

Each id is looked up in the release *its own entry pins it to*. Two situations are reported and left
untouched rather than "fixed", because in both the id is the suspect part and only a human knows what was
intended:

* **The id is absent from its pinned release** -- either the id is wrong or it names something never
  published (TMFC003's function 720 appears in no release from v23.0 to v26.0).
* **The id is listed more than once** in the component's own metadata. Correcting the names would collapse
  the entries into duplicates and erase the evidence that one of them is mis-numbered.

This edits the definitive component YAML, so it is dry-run by default. Per the skill's own convention,
record what changed as a note in the Supplement file's 5.3 section afterwards.

Usage:
    python align_framework_names.py --component-dir <TMFCxxx folder> \
        --frameworks <framework releases folder> [--apply]
"""
import argparse
import glob
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framework_lookup import load_definitions, norm_version


def find_yaml(component_dir):
    matches = glob.glob(os.path.join(component_dir, "*.yaml"))
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one component YAML in {component_dir}, found {len(matches)}")
    return matches[0]


def parse_entries(entries):
    out = []
    for raw in entries or []:
        parts = [p.strip() for p in str(raw).split("|")]
        if len(parts) >= 3:
            out.append({"raw": str(raw), "id": parts[0], "token": parts[-2], "version": parts[-1]})
    return out


def check(entries, frameworks, family, label):
    caches = {}
    matched, changes, absent, level_issues = 0, [], [], []

    # An id listed more than once in the component's own metadata is a data-quality defect, and aligning
    # its name would hide rather than help. Real case: TMFC003 on v1.1.0 lists eTOM 1.3.3.12.1 twice, as
    # Manage_Customer_Order_Fallout and Manage_Customer_Order_Delivery. The framework says that id is
    # Manage Customer Order Fallout -- so the second entry's *id* is wrong, not its name. Renaming it
    # would produce two byte-identical entries and quietly erase the evidence that an activity was
    # mis-numbered. Report these and change nothing; resolving them needs a human who knows which
    # activity was intended.
    counts = {}
    for e in entries:
        counts[e["id"]] = counts.get(e["id"], 0) + 1
    duplicates = {i for i, n in counts.items() if n > 1}

    for e in entries:
        if e["id"] in duplicates:
            continue
        key = norm_version(e["version"])
        if key not in caches:
            try:
                caches[key] = load_definitions(frameworks, family, e["version"])
            except FileNotFoundError as exc:
                caches[key] = ({}, str(exc), [])
        index, source, conflicts = caches[key]
        if conflicts:
            level_issues.append(f"{source}: duplicate ids disagree: {', '.join(conflicts[:5])}")
        rec = index.get(e["id"])
        if not rec:
            absent.append((e["id"], e["version"], source))
            continue
        token = str(rec.get("token") or "").strip()
        if not token:
            absent.append((e["id"], e["version"], f"{source} (no token field)"))
        elif token == e["token"]:
            matched += 1
        else:
            changes.append({**e, "new": token, "display": rec.get("name", ""), "source": source})
        # the skill infers eTOM level from id depth; the JSON states it, so cross-check the rule
        if family == "etom_json" and rec.get("level") is not None:
            inferred = len(e["id"].split(".")) - 1
            if int(rec["level"]) != inferred:
                level_issues.append(
                    f"{e['id']}: level inferred {inferred} but framework says {rec['level']}")
    print(f"  {label}: {matched} already match, {len(changes)} to change, {len(absent)} not in the "
          f"pinned release"
          + (f", {len(duplicates)} skipped as duplicate id(s)" if duplicates else ""))
    for dup in sorted(duplicates):
        names = [e["token"] for e in entries if e["id"] == dup]
        print(f"      {dup:>10}  DUPLICATE ID, listed {counts[dup]} times as {', '.join(names)}")
        print(f"      {'':>10}  left untouched: one of these entries has the wrong id, so correcting "
              f"names here would create identical rows and hide the defect")
    for c in changes:
        print(f"      {c['id']:>10}  {c['token']}  ->  {c['new']}    [{c['display']}]")
    for entry_id, version, source in absent:
        print(f"      {entry_id:>10}  absent from {source} (pinned {version}) — left unchanged")
    for issue in dict.fromkeys(level_issues):
        print(f"      note: {issue}")
    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--component-dir", required=True)
    ap.add_argument("--frameworks", required=True,
                    help="folder holding the framework JSON definitions (ask the user; it is not in "
                         "this repository)")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.frameworks):
        raise SystemExit(f"frameworks folder not found: {args.frameworks}")

    yaml_path = find_yaml(args.component_dir)
    with open(yaml_path, encoding="utf-8") as f:
        raw_text = f.read()
    meta = (yaml.safe_load(raw_text).get("spec") or yaml.safe_load(raw_text))["componentMetadata"]
    print(f"{meta['id']}  ({os.path.basename(yaml_path)})")

    all_changes = []
    all_changes += check(parse_entries(meta.get("eTOMs")), args.frameworks, "etom_json", "eTOM")
    all_changes += check(parse_entries(meta.get("functionalFrameworkFunctions")),
                         args.frameworks, "ff_json", "Functional Framework")

    if not args.apply:
        print("\n(dry run — pass --apply to rewrite the component YAML)")
        return
    if not all_changes:
        print("\nnothing to apply")
        return

    text = raw_text
    for c in all_changes:
        # anchor on the whole pipe-delimited entry, and require exactly one occurrence, so only the
        # intended list is touched -- the same token could plausibly appear elsewhere in the file
        old_entry = f"- {c['id']}|{c['token']}|{c['version']}"
        new_entry = f"- {c['id']}|{c['new']}|{c['version']}"
        if text.count(old_entry) != 1:
            raise SystemExit(f"expected exactly one {old_entry!r}, found {text.count(old_entry)} — "
                             f"aborting without writing")
        text = text.replace(old_entry, new_entry)
    with open(yaml_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"\nrewrote {len(all_changes)} entr{'y' if len(all_changes) == 1 else 'ies'} in "
          f"{os.path.basename(yaml_path)}")
    print("Record this in the Supplement file's 5.3 section, per the skill's convention.")


if __name__ == "__main__":
    main()
