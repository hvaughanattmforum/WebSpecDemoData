"""Regenerates the 2.1 (eTOM business activities) and 2.4 (Functional Framework Functions)
tables of a component's main .md from the CURRENT YAML plus the <ID>_eTOM_Descriptions.md /
<ID>_FF_Descriptions.md lookup files, adding the Description (and, for FF, Aggregate Function
Level 1/2) columns those files hold. Only touches those two tables — everything else in the
.md (2.2, 2.3, 3.x, 5.1, etc.) is left byte-for-byte untouched.

Regenerating from YAML (not just patch-adding a column to the existing table) matters here:
a few of these 13 components' checked-in main .md still show "*(none listed in the component
YAML)*" for 2.1/2.4 from when their YAML's eTOMs/functionalFrameworkFunctions were empty — the
YAML has since been filled in (real upstream drift-fix, not something this script caused), so
the placeholder needs to become a real table now, not just gain a column.
"""
import glob
import os
import re
import sys

import yaml

# This skill lives inside the specification repository (skills/<name>/scripts/), so the specifications
# folder is three levels up -- no absolute path needed, and the script works from any clone.
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "specifications"))

COMPONENTS = {
    "TMFC001": "TMFC001-ProductCatalogManagement",
    "TMFC005": "TMFC005-ProductInventory",
    "TMFC007": "TMFC007-ServiceOrderManagement",
    "TMFC008": "TMFC008-ServiceInventory",
    "TMFC031": "TMFC031-BillCalculation",
    "TMFC035": "TMFC035-PermissionsManagement",
    "TMFC037": "TMFC037-ServicePerformanceManagement",
    "TMFC039": "TMFC039-AgreementManagement",
    "TMFC040": "TMFC040-ProductUsageManagement",
    "TMFC043": "TMFC043-FaultManagement",
    "TMFC050": "TMFC050-ProductRecommendation",
    "TMFC054": "TMFC054-ProductTestManagement",
    "TMFC055": "TMFC055-ServiceTestManagement",
}

NO_DESC = "*(no description available)*"


def esc(text):
    return text.replace("|", "\\|").strip()


def parse_description_file(path, key_col):
    """Returns {id: {col_name: value}} from a Descriptions.md file, or {} if 'confirmed empty'."""
    if not os.path.exists(path):
        return {}
    text = open(path, encoding="utf-8").read()
    lines = [l for l in text.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return {}
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    out = {}
    for line in lines[2:]:  # skip header + separator
        cells = [c.strip().replace("\\|", "|") for c in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        ident = row.get(key_col, "").strip()
        if ident:
            out[ident] = row
    return out


def load_yaml_lists(yaml_path):
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    meta = data["spec"]["componentMetadata"] if "spec" in data else data["componentMetadata"]
    return meta.get("eTOMs") or [], meta.get("functionalFrameworkFunctions") or []


def parse_etom_entries(etoms):
    rows = []
    for entry in etoms:
        parts = entry.split("|")
        ident, name = parts[0], parts[1]
        level = "L" + str(len(ident.split(".")) - 1)
        name = name.replace("_", " ")
        rows.append((ident, level, name))
    return rows


def parse_ff_entries(ffs):
    rows = []
    for entry in ffs:
        parts = entry.split("|")
        fid, name = parts[0], parts[1]
        name = name.replace("_", " ")
        rows.append((fid, name))
    return rows


def build_etom_table(rows, desc_lookup):
    if not rows:
        return "*(none listed in the component YAML)*"
    lines = ["| Identifier | Level | Business Activity Name | Description |", "|---|---|---|---|"]
    for ident, level, name in rows:
        desc = desc_lookup.get(ident, {}).get("Description", "")
        desc = esc(desc) if desc else NO_DESC
        lines.append(f"| {ident} | {level} | {name} | {desc} |")
    return "\n".join(lines)


def build_ff_table(rows, desc_lookup):
    if not rows:
        return "*(none listed in the component YAML)*"
    lines = [
        "| Function ID | Function Name | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |",
        "|---|---|---|---|---|",
    ]
    for fid, name in rows:
        entry = desc_lookup.get(fid, {})
        desc = esc(entry.get("Function Description", "")) or NO_DESC
        agg1 = esc(entry.get("Aggregate Function Level 1", "")) or NO_DESC
        agg2 = esc(entry.get("Aggregate Function Level 2", "")) or NO_DESC
        lines.append(f"| {fid} | {name} | {desc} | {agg1} | {agg2} |")
    return "\n".join(lines)


SECTION_21_RE = re.compile(
    r"(### 2\.1\. eTOM business activities\n\neTOM business activities this ODA Component is responsible for:\n\n)"
    r"(.*?)"
    r"(\n\n### 2\.2\.)",
    re.DOTALL,
)
SECTION_24_RE = re.compile(
    r"(### 2\.4\. Functional Framework Functions\n\n)"
    r"(.*?)"
    r"(\n\n## 3\.)",
    re.DOTALL,
)


def process(cid, folder, dry_run=True):
    comp_dir = os.path.join(REPO, folder)
    diagrams_dir = os.path.join(comp_dir, "Diagrams")
    yaml_path = glob.glob(os.path.join(comp_dir, "*.yaml"))[0]
    md_candidates = [
        f for f in glob.glob(os.path.join(diagrams_dir, "*.md"))
        if not re.search(r"(Supplement|Links|Descriptions)\.md$", f)
    ]
    assert len(md_candidates) == 1, (cid, md_candidates)
    md_path = md_candidates[0]

    etom_desc = parse_description_file(os.path.join(diagrams_dir, f"{cid}_eTOM_Descriptions.md"), "Identifier")
    ff_desc = parse_description_file(os.path.join(diagrams_dir, f"{cid}_FF_Descriptions.md"), "Function ID")

    etoms, ffs = load_yaml_lists(yaml_path)
    etom_rows = parse_etom_entries(etoms)
    ff_rows = parse_ff_entries(ffs)

    new_etom_table = build_etom_table(etom_rows, etom_desc)
    new_ff_table = build_ff_table(ff_rows, ff_desc)

    text = open(md_path, encoding="utf-8").read()

    m21 = SECTION_21_RE.search(text)
    m24 = SECTION_24_RE.search(text)
    if not m21 or not m24:
        print(f"!! {cid}: section regex did not match (2.1 match={bool(m21)}, 2.4 match={bool(m24)})")
        return

    old_21 = m21.group(2)
    old_24 = m24.group(2)
    changed_21 = old_21.strip() != new_etom_table.strip()
    changed_24 = old_24.strip() != new_ff_table.strip()

    new_text = SECTION_21_RE.sub(lambda m: m.group(1) + new_etom_table + m.group(3), text, count=1)
    new_text = SECTION_24_RE.sub(lambda m: m.group(1) + new_ff_table + m.group(3), new_text, count=1)

    print(f"{cid}: 2.1 changed={changed_21} ({len(etom_rows)} rows, {len(etom_desc)} descriptions available) | "
          f"2.4 changed={changed_24} ({len(ff_rows)} rows, {len(ff_desc)} descriptions available)")

    if not dry_run and (changed_21 or changed_24):
        with open(md_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)
        print(f"   -> wrote {md_path}")


if __name__ == "__main__":
    dry = "--apply" not in sys.argv
    for cid, folder in COMPONENTS.items():
        process(cid, folder, dry_run=dry)
    if dry:
        print("\n(dry run — pass --apply to write changes)")
