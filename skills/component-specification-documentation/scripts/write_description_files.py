"""Writes the two per-component description files (<ID>_eTOM_Descriptions.md,
<ID>_FF_Descriptions.md) from the JSON produced by extract_descriptions.py, into each
component's real-repo Diagrams/ folder. Same hand-maintained-file convention as the
existing <ID>_eTOM_SID_Links.md: a one-line source note, then a pipe table keyed by ID.
"""
import json
import os

REPO = r"C:\Users\HugoVaughan\source\repos\tmforum-rand\TMForum-ODA-Component-Specification\specifications"

COMPONENTS = {
    "TMFC001": ("TMFC001-ProductCatalogManagement", "TMFC001 Product Catalog Management v2.2.2.docx"),
    "TMFC005": ("TMFC005-ProductInventory", "TMFC005 Product Inventory v1.1.0.docx"),
    "TMFC007": ("TMFC007-ServiceOrderManagement", "TMFC007 Service Order Management v1.3.0.docx"),
    "TMFC008": ("TMFC008-ServiceInventory", "TMFC008 Service Inventory v1.3.0.docx"),
    "TMFC031": ("TMFC031-BillCalculation", "TMFC031_ Bill Calculation Management v3.1.0.docx"),
    "TMFC035": ("TMFC035-PermissionsManagement", "TMFC035 Permissions Management v1.2.0.docx"),
    "TMFC037": ("TMFC037-ServicePerformanceManagement", "TMFC037_ Service Performance Management 1.3.0.docx"),
    "TMFC039": ("TMFC039-AgreementManagement", "TMFC039 Agreement Management v1.2.0.docx"),
    "TMFC040": ("TMFC040-ProductUsageManagement", "TMFC040 Product Usage Management v1.2.0.docx"),
    "TMFC043": ("TMFC043-FaultManagement", "TMFC043_ Fault Management v1.1.0.docx"),
    "TMFC050": ("TMFC050-ProductRecommendation", "TMFC050 Product Recommendation Management v1.2.0.docx"),
    "TMFC054": ("TMFC054-ProductTestManagement", "TMFC054 Product Test Management v1.1.0.docx"),
    "TMFC055": ("TMFC055-ServiceTestManagement", "TMFC055 Service Test Management v1.1.0.docx"),
}


def esc(text):
    return text.replace("|", "\\|")


def write_etom_file(cid, folder, source_name, etom):
    path = os.path.join(REPO, folder, "Diagrams", f"{cid}_eTOM_Descriptions.md")
    lines = [f"# {cid} eTOM Business Activity Descriptions", ""]
    if not etom:
        lines.append(
            f"Source: confirmed empty — transcribed from `{source_name}`'s "
            "\"2.1 eTOM business activities\" table, which has no rows for this component."
        )
        lines.append("")
    else:
        lines.append(f"Source: transcribed from `{source_name}`, section 2.1 (eTOM business activities).")
        lines.append("")
        lines.append("| Identifier | Description |")
        lines.append("|---|---|")
        for ident, desc in etom.items():
            lines.append(f"| {esc(ident)} | {esc(desc)} |")
        lines.append("")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    return path


def write_ff_file(cid, folder, source_name, ff):
    path = os.path.join(REPO, folder, "Diagrams", f"{cid}_FF_Descriptions.md")
    lines = [f"# {cid} Functional Framework Function Descriptions", ""]
    if not ff:
        lines.append(
            f"Source: confirmed empty — transcribed from `{source_name}`'s "
            "\"2.4 Functional Framework Functions\" table, which has no rows for this component."
        )
        lines.append("")
    else:
        lines.append(f"Source: transcribed from `{source_name}`, section 2.4 (Functional Framework Functions).")
        lines.append("")
        lines.append("| Function ID | Function Description | Aggregate Function Level 1 | Aggregate Function Level 2 |")
        lines.append("|---|---|---|---|")
        for fid, entry in ff.items():
            lines.append(
                f"| {esc(fid)} | {esc(entry['description'])} | {esc(entry['agg1'])} | {esc(entry['agg2'])} |"
            )
        lines.append("")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    return path


if __name__ == "__main__":
    data = json.load(open(
        r"C:\Users\HugoVaughan\ClaudeCode\.claude\skills\component-specification-documentation\_batch\descriptions_raw.json",
        encoding="utf-8",
    ))
    for cid, (folder, source_name) in COMPONENTS.items():
        r = data[cid]
        p1 = write_etom_file(cid, folder, source_name, r["etom"])
        p2 = write_ff_file(cid, folder, source_name, r["ff"])
        print(cid, "->", p1)
        print(cid, "->", p2)
