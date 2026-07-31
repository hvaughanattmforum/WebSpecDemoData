"""
Compare two versions of a TM Forum ODA component specification PDF and write a change report to
Diagrams/TMFCnnn_<Name>_v<old>_vs_v<new>_difference.md.

The report is a semantic comparison, not a text diff: entries are matched by their own identifiers
(eTOM activity id, Functional Framework function id, SID ABE names, TMF API id, event name) so that
re-pagination, re-worded prose and re-laid-out tables don't masquerade as changes.

Two rules keep the output trustworthy, and they matter more than any formatting choice here:

1. **Never report a section as emptied when it simply wasn't tabulated.** The older documents present
   Events as a diagram with no table at all, and one states its SID ABEs as the single word "none". A
   naive set difference turns both into "every entry removed", which is a false alarm a reviewer would
   have to chase. Where one side has no table, the report says so and compares nothing.

2. **Don't report detail the extraction can't stand behind.** Resource and operation text sometimes
   can't be recovered cleanly from a PDF (see extract_spec_pdf.py). APIs are therefore compared on
   identity, name, mandatory/optional and version set -- all reliable -- while resource-level detail is
   summarised with an explicit caveat rather than diffed row by row.

Usage:
    python build_difference.py <old.pdf> <new.pdf> [--out <path.md>]
    python build_difference.py --component-dir <TMFCxxx folder>      # discovers the two PDFs
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_spec_pdf import extract

ABSENT = "*(not tabulated in this version)*"


def _vkey(v):
    return [int(p) for p in re.findall(r"\d+", v or "0")]


def discover(component_dir):
    """The two specification PDFs for a component: the published one(s) at the component root plus any
    generated copy under Diagrams/. Ordered oldest to newest by version."""
    found = {}
    for path in (glob.glob(os.path.join(component_dir, "*.pdf"))
                 + glob.glob(os.path.join(component_dir, "Diagrams", "*.pdf"))):
        m = re.search(r"v(\d+\.\d+\.\d+)", os.path.basename(path))
        if not m:
            continue
        found.setdefault(m.group(1), path)          # root copy wins over the Diagrams duplicate
    if len(found) < 2:
        raise SystemExit(f"need two versioned PDFs in {component_dir}, found: "
                         f"{sorted(found) or 'none'}")
    versions = sorted(found, key=_vkey)
    return found[versions[0]], found[versions[-1]]


def _table(header, rows):
    if not rows:
        return ["*(none)*", ""]
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    out += ["| " + " | ".join(str(c or "") for c in r) + " |" for r in rows]
    return out + [""]


def _keyed(records, key):
    return {key(r): r for r in records}


def _compare_keyed(old, new, key, label_fn, fields, old_has, new_has):
    """Added / removed / changed for one section. Returns (lines, counts)."""
    if not old_has or not new_has:
        side = "the old document" if not old_has else "the new document"
        return [f"{ABSENT[:-1]} in {side}; no comparison possible.*", ""], (0, 0, 0)

    o, n = _keyed(old, key), _keyed(new, key)
    added = [n[k] for k in n if k not in o]
    removed = [o[k] for k in o if k not in n]
    changed = []
    for k in n:
        if k not in o:
            continue
        diffs = [(f, o[k].get(f, ""), n[k].get(f, "")) for f in fields
                 if (o[k].get(f, "") or "") != (n[k].get(f, "") or "")]
        if diffs:
            changed.append((k, n[k], diffs))

    lines = []
    lines.append(f"**Added ({len(added)})**")
    lines += _table(["Key", "Detail"], [[label_fn(r), r.get(fields[0], "")] for r in added])
    lines.append(f"**Removed ({len(removed)})**")
    lines += _table(["Key", "Detail"], [[label_fn(r), r.get(fields[0], "")] for r in removed])
    lines.append(f"**Changed ({len(changed)})**")
    rows = []
    for k, rec, diffs in changed:
        for field, was, now in diffs:
            rows.append([label_fn(rec), field, _trim(was), _trim(now)])
    lines += _table(["Key", "Field", "Old", "New"], rows)
    return lines, (len(added), len(removed), len(changed))


def _trim(text, n=160):
    text = re.sub(r"\s+", " ", str(text or "")).strip().replace("|", r"\|")
    return text if len(text) <= n else text[: n - 1] + "…"


def _api_summary(records):
    """Collapse per-resource rows into one entry per API, which is the level this comparison can
    actually stand behind."""
    apis = {}
    for r in records:
        if not r.get("id"):
            continue
        a = apis.setdefault(r["id"], {"id": r["id"], "name": r.get("name", ""),
                                      "flag": r.get("flag", ""), "versions": set(),
                                      "resources": set(), "rows": 0, "confident": 0})
        a["rows"] += 1
        a["confident"] += 1 if r.get("resource_confident") else 0
        if r.get("version"):
            a["versions"].add(r["version"])
        if r.get("resource") and r.get("resource_confident"):
            a["resources"].add(r["resource"])
        a["name"] = a["name"] or r.get("name", "")
        a["flag"] = a["flag"] or r.get("flag", "")
    for a in apis.values():
        # The older documents have no Version column at all, so an API there states no version. Per
        # standing instruction those are taken to be version 4, which is what makes a version
        # comparison meaningful instead of reporting every retained API as "blank -> 4, 5". The
        # assumption is recorded on the record so the report can state it rather than imply the
        # version was read from the page.
        a["version_assumed"] = not a["versions"]
        if a["version_assumed"]:
            a["versions"] = {"4"}
        a["version_list"] = ", ".join(sorted(a["versions"], key=_vkey))
        a["resource_list"] = ", ".join(sorted(a["resources"]))
    return apis


def _compare_apis(old, new, old_has, new_has, title, old_seen=(), new_seen=()):
    if not old_has or not new_has:
        side = "the old document" if not old_has else "the new document"
        return [f"*Not tabulated in {side}; no comparison possible.*", ""], (0, 0, 0)

    o, n = _api_summary(old), _api_summary(new)
    # An id printed in the other document's section text is present there even if no row parsed for it,
    # so it is not an addition or a removal -- it is missing detail. Claiming otherwise would send a
    # reviewer looking for a change that never happened.
    added = sorted(set(n) - set(o) - set(old_seen))
    removed = sorted(set(o) - set(n) - set(new_seen))
    unparsed = sorted((set(n) - set(o)) & set(old_seen) | (set(o) - set(n)) & set(new_seen))
    lines = []
    lines.append(f"**APIs added ({len(added)})**")
    lines += _table(["API", "Name", "Mandatory / Optional", "Version(s)"],
                    [[k, n[k]["name"], n[k]["flag"], n[k]["version_list"]] for k in added])
    lines.append(f"**APIs removed ({len(removed)})**")
    lines += _table(["API", "Name", "Mandatory / Optional"],
                    [[k, o[k]["name"], o[k]["flag"]] for k in removed])

    rows = []
    assumed = []
    for k in sorted(set(o) & set(n)):
        for field, label in (("name", "Name"), ("flag", "Mandatory / Optional"),
                             ("version_list", "Version(s)")):
            was, now = o[k].get(field, ""), n[k].get(field, "")
            # only claim a change where both sides actually say something -- a blank on one side means
            # that document didn't state it, which is not the same as a change
            if was and now and was != now:
                rows.append([k, label, _trim(was), _trim(now)])
        if o[k].get("version_assumed"):
            assumed.append(k)
    lines.append(f"**Changed on retained APIs ({len(rows)})**")
    lines += _table(["API", "Field", "Old", "New"], rows)
    retained = len(set(o) & set(n))
    note = f"*{retained} API(s) present in both versions."
    if assumed:
        note += (f" The old document has no Version column, so its APIs are taken to be version 4 "
                 f"({len(assumed)} of {retained}).")
    if unparsed:
        note += (f" {', '.join(unparsed)} appear in both documents' section text but a table row could "
                 f"only be parsed in one, so they are reported as neither added nor removed.")
    lines += [note + "*", ""]
    return lines, (len(added), len(removed), len(rows))


def build(old_pdf, new_pdf, out_path=None):
    old, new = extract(old_pdf), extract(new_pdf)
    if _vkey(old["version"]) > _vkey(new["version"]):
        old, new = new, old
        old_pdf, new_pdf = new_pdf, old_pdf

    cid = new["component_id"] or old["component_id"] or "TMFCxxx"
    display = (new["overview"].get("component_name") or old["overview"].get("component_name")
               or cid).strip()
    if out_path is None:
        stem = re.sub(r"\s+", "_", display) or cid
        out_path = os.path.join(os.path.dirname(os.path.abspath(new_pdf)),
                                f"{cid}_{stem}_v{old['version']}_vs_v{new['version']}_difference.md")
        if os.path.basename(os.path.dirname(out_path)).lower() != "diagrams":
            alt = os.path.join(os.path.dirname(os.path.abspath(new_pdf)), "Diagrams")
            if os.path.isdir(alt):
                out_path = os.path.join(alt, os.path.basename(out_path))

    has = lambda d, sect, coll: (sect in d["sections_found"]) and bool(d[coll])

    L = [f"# {cid} – {display}", "",
         f"## Specification differences: v{old['version']} → v{new['version']}", "",
         "| | Old | New |", "|---|---|---|",
         f"| Version | {old['version']} | {new['version']} |",
         f"| Source file | `{old['source_file']}` | `{new['source_file']}` |",
         f"| Pages | {old['pages']} | {new['pages']} |"]
    for field, label in (("release_status", "Release Status"), ("maturity_level", "Maturity Level"),
                         ("approval_status", "Approval Status"),
                         ("team_approved_date", "Team Approved Date")):
        ov, nv = old["cover"].get(field, ""), new["cover"].get(field, "")
        if ov or nv:
            L.append(f"| {label} | {ov or '—'} | {nv or '—'} |")
    L.append("")

    counts = {}

    L += ["## 1. Overview", ""]
    rows, unread = [], []
    for field, label in (("description", "Description"), ("function_block", "ODA Function Block")):
        ov, nv = old["overview"].get(field, ""), new["overview"].get(field, "")
        # same both-sides rule as the API fields: a blank means that document's value couldn't be read,
        # which is not a change
        if ov and nv and ov != nv:
            rows.append([label, _trim(ov, 400), _trim(nv, 400)])
        elif not ov or not nv:
            unread.append(label)
    L += _table(["Field", "Old", "New"], rows) if rows else ["*No change.*", ""]
    if unread:
        L += [f"*Not compared ({', '.join(unread)}): the value could not be read from one of the two "
              f"documents.*", ""]

    L += ["## 2.1 eTOM business activities", ""]
    body, counts["eTOM"] = _compare_keyed(
        old["etoms"], new["etoms"], lambda r: r["id"],
        lambda r: f"{r['id']} {r.get('name','')}".strip(), ["name", "description"],
        has(old, "etoms", "etoms"), has(new, "etoms", "etoms"))
    L += body

    L += ["## 2.2 SID ABEs", ""]
    if not has(old, "sids", "sids"):
        # The old document stating "none" is a positive assertion that it owned no SID ABEs, so
        # everything the new document lists is genuinely an addition -- not merely uncomparable.
        note = next((n for n in old["notes"] if "SID ABEs" in n), "")
        L += [f"**Added ({len(new['sids'])})**"]
        L += _table(["SID ABE Level 1", "SID ABE Level 2"],
                    [[s["l1"], s["l2"]] for s in new["sids"]])
        L += ["**Removed (0)**", "*(none)*", "",
              "*The old document listed no SID ABEs"
              + (f" — its 2.2 table states \"none\"" if note else "")
              + ", so every entry above is new.*", ""]
        counts["SID"] = (len(new["sids"]), 0, 0)
    else:
        body, counts["SID"] = _compare_keyed(
            old["sids"], new["sids"], lambda r: (r["l1"], r["l2"]),
            lambda r: f"{r['l1']} / {r['l2']}".strip(" /"), ["definition"],
            True, has(new, "sids", "sids"))
        L += body

    L += ["## 2.4 Functional Framework Functions", ""]
    body, counts["FF"] = _compare_keyed(
        old["ffs"], new["ffs"], lambda r: r["id"],
        lambda r: f"{r['id']} {r.get('name','')}".strip(), ["name", "description", "af1", "af2"],
        has(old, "ffs", "ffs"), has(new, "ffs", "ffs"))
    L += body

    L += ["## 3 Exposed APIs", ""]
    body, counts["Exposed APIs"] = _compare_apis(
        old["exposed_apis"], new["exposed_apis"],
        has(old, "exposed_apis", "exposed_apis"), has(new, "exposed_apis", "exposed_apis"),
        "Exposed",
        old.get("api_ids_seen", {}).get("exposed_apis", []),
        new.get("api_ids_seen", {}).get("exposed_apis", []))
    L += body

    L += ["## 3 Dependent APIs", ""]
    body, counts["Dependent APIs"] = _compare_apis(
        old["dependent_apis"], new["dependent_apis"],
        has(old, "dependent_apis", "dependent_apis"), has(new, "dependent_apis", "dependent_apis"),
        "Dependent",
        old.get("api_ids_seen", {}).get("dependent_apis", []),
        new.get("api_ids_seen", {}).get("dependent_apis", []))
    L += body

    L += ["## 3 Events", ""]
    old_ev = has(old, "published_events", "published_events") or has(old, "subscribed_events",
                                                                     "subscribed_events")
    new_ev = has(new, "published_events", "published_events") or has(new, "subscribed_events",
                                                                     "subscribed_events")
    if not old_ev:
        pub = sum(len(e["events"]) for e in new["published_events"])
        sub = sum(len(e["events"]) for e in new["subscribed_events"])
        L += [f"**Added ({pub + sub})** — {pub} published across "
              f"{len(new['published_events'])} API(s), {sub} subscribed across "
              f"{len(new['subscribed_events'])} API(s)", ""]
        L.append("**Published**")
        L += _table(["API", "Name", "Version(s)", "Events"],
                    [[e["id"], e["name"], e["version"], _trim(", ".join(e["events"]), 300)]
                     for e in new["published_events"]])
        L.append("**Subscribed**")
        L += _table(["API", "Name", "Version(s)", "Events"],
                    [[e["id"], e["name"], e["version"], _trim(", ".join(e["events"]), 300)]
                     for e in new["subscribed_events"]])
        L += ["**Removed (0)**", "*(none)*", "",
              "*The old document presents its Events section as a diagram with no table, so these are "
              "additions relative to what that document tabulated. Unlike the SID section, its diagram "
              "may well have depicted events, so this is not evidence that none existed.*", ""]
        counts["Events"] = (pub + sub, 0, 0)
    else:
        rows = []
        for label, ok, nk in (("Published", "published_events", "published_events"),
                              ("Subscribed", "subscribed_events", "subscribed_events")):
            o = {e["id"]: set(e["events"]) for e in old[ok]}
            n = {e["id"]: set(e["events"]) for e in new[nk]}
            for api in sorted(set(o) | set(n)):
                gained = sorted(n.get(api, set()) - o.get(api, set()))
                lost = sorted(o.get(api, set()) - n.get(api, set()))
                if gained or lost:
                    rows.append([label, api, _trim(", ".join(gained), 200) or "—",
                                 _trim(", ".join(lost), 200) or "—"])
        L.append(f"**Event changes by API ({len(rows)})**")
        L += _table(["Direction", "API", "Added", "Removed"], rows)
        counts["Events"] = (len(rows), 0, 0)

    L += ["## 5.1 TMF Standards related versions", ""]
    rows = []
    for std in sorted(set(old["standards"]) | set(new["standards"])):
        ov, nv = old["standards"].get(std, ""), new["standards"].get(std, "")
        if ov != nv:
            rows.append([std, ov or "—", nv or "—"])
    L += _table(["Standard", "Old", "New"], rows) if rows else ["*No change.*", ""]

    # summary placed near the top once the counts are known
    summary = ["## Summary of changes", "",
               "| Section | Added | Removed | Changed |", "|---|---|---|---|"]
    for name, (a, r, c) in counts.items():
        summary.append(f"| {name} | {a} | {r} | {c} |")
    summary.append("")
    insert_at = L.index("## 1. Overview")
    L = L[:insert_at] + summary + L[insert_at:]

    L += ["## Extraction caveats", "",
          "This comparison is derived from the two PDFs by structured extraction, so it is only as "
          "good as what could be read back out of them. Anything listed here limits how far the "
          "findings above should be trusted.", ""]
    caveats = []
    for tag, doc in (("old", old), ("new", new)):
        for note in doc["notes"]:
            caveats.append(f"- **v{doc['version']}** ({tag}): {note}")
    caveats.append("- API comparison is at API level (identity, name, mandatory/optional, versions). "
                   "Per-resource and per-operation rows are not diffed, because a mis-detected table "
                   "column boundary in a PDF can interleave two cells' characters and silently corrupt "
                   "resource names.")
    caveats.append("- Where a document states no API version (the older layout has no Version column), "
                   "its APIs are taken to be version 4. That is a stated assumption, not something read "
                   "from the page.")
    caveats.append("- A field is only reported as changed when both documents state a value for it. A "
                   "blank on one side means that document did not record it, which is not evidence of a "
                   "change.")
    L += caveats + [""]

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(L)).rstrip("\n") + "\n"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return out_path, counts, old, new


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("old_pdf", nargs="?")
    ap.add_argument("new_pdf", nargs="?")
    ap.add_argument("--component-dir")
    ap.add_argument("--out")
    args = ap.parse_args()

    if args.component_dir:
        old_pdf, new_pdf = discover(args.component_dir)
    elif args.old_pdf and args.new_pdf:
        old_pdf, new_pdf = args.old_pdf, args.new_pdf
    else:
        ap.error("give two PDFs or --component-dir")

    print(f"old: {os.path.basename(old_pdf)}")
    print(f"new: {os.path.basename(new_pdf)}")
    out, counts, old, new = build(old_pdf, new_pdf, args.out)
    print(f"\nwrote {out}")
    for name, (a, r, c) in counts.items():
        print(f"  {name:<16} +{a} -{r} ~{c}")
    for doc, tag in ((old, "old"), (new, "new")):
        for note in doc["notes"]:
            print(f"  caveat ({tag}): {note}")


if __name__ == "__main__":
    main()
