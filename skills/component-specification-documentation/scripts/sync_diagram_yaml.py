"""
Regenerate a component's Diagrams/<ID>_{Exposed_API,Dependant_API}.yaml files from its current main
component YAML, instead of assuming they're already in sync. `<ID>_Events.yaml` is currently accepted
at face value (read, never regenerated) -- see the note in sync_all() and the sync_events() docstring;
that's a temporary, acknowledged decision pending a fix to its id/resources matching, not a design call.

Why this exists: these files are the source for the Exposed API / Dependent API diagrams AND the
display-name lookup used when writing the tables in the generated Markdown. They are maintained as
separate files alongside the main YAML, not auto-derived from it on every edit -- so they can silently
drift (an API added/removed from the main YAML without the Diagrams file being touched, a required flag
flipping, a resource/operation list changing). Regenerate them every time this skill runs, before
treating them as a data source, rather than trusting they're current.

Name resolution: this script never invents a display name. It reuses the existing Diagrams file's
id->name mapping (it already did the hard work of resolving names once) for any id that's still
present, and reports any id that's new (no prior name on file) so it can be resolved by hand (e.g. via
apiIndex.json or the TMF spec) rather than silently left blank or guessed.

Usage: call sync_all(component_dir, component_id) with the path to one component's folder (the one
containing both the main <ComponentID>-<Name>.yaml and the Diagrams/ subfolder) and its ID (e.g.
"TMFC012"). Returns a report dict describing what changed per file, and writes the regenerated files in
place (matching the existing block style / indentation).
"""
import glob
import os
import yaml


class _BlockDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def _dump_yaml(data):
    return yaml.dump(data, Dumper=_BlockDumper, default_flow_style=False, sort_keys=False, indent=2,
                      allow_unicode=True, width=100)


def _write_lf(path, text):
    """Write with LF-only line endings -- Windows text-mode write silently turns \\n into \\r\\n,
    which would make every single line in the file show as changed in git diff even when nothing
    semantically changed."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _load_main_yaml(component_dir):
    matches = glob.glob(os.path.join(component_dir, "*.yaml"))
    matches = [m for m in matches if "Diagrams" not in m]
    if len(matches) != 1:
        raise FileNotFoundError(f"expected exactly one main YAML in {component_dir}, found {matches}")
    with open(matches[0], encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_diagram_yaml(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    inner = text.replace("@startyaml", "").replace("@endyaml", "")
    return yaml.safe_load(inner)


def _load_first_page(diagrams_dir, component_id, base_name):
    """When the unnumbered `<ID>_<base_name>.yaml` doesn't exist, the file may instead be split into
    `_1.yaml`, `_2.yaml`, ... from a previous paginated run -- merge their entries back into one dict
    (under whichever top-level key each page actually has) so sync_api_list()'s old-name resolution
    still sees every previously-resolved id, not just page 1's."""
    paths = sorted(glob.glob(os.path.join(diagrams_dir, f"{component_id}_{base_name}_*.yaml")))
    if not paths:
        return None
    merged = {}
    for path in paths:
        doc = _load_diagram_yaml(path) or {}
        for key, entries in doc.items():
            merged.setdefault(key, []).extend(entries or [])
    return merged


def _name_map(entries):
    """id -> name, from an existing (already name-resolved) Diagrams file's entry list."""
    m = {}
    for e in entries or []:
        if e and e.get("id") and e.get("name"):
            m[e["id"]] = e["name"]
    return m


def _resolve_event(entry, by_resources):
    """Returns (id, name) or (None, None). Main-YAML event entries carry a raw `name` (e.g.
    "ResourceInventory") that does NOT match the diagram file's resolved display name (e.g.
    "Resource Inventory Management API") -- there's no shared string key at all between the two. The
    `resources` list (the event names themselves, e.g. resourceCreateEvent/resourceDeleteEvent/...) is
    the one field that's actually identical between a main-YAML entry and its diagram-file counterpart,
    so match on that instead of on id or name."""
    if entry.get("id"):
        old = by_resources.get(frozenset(entry.get("resources", [])))
        if old:
            return entry["id"], old[1]
        return entry["id"], None
    old = by_resources.get(frozenset(entry.get("resources", [])))
    if old:
        return old
    return None, None


PAGE_THRESHOLD = 60


def paginate_entries(entries, weight_fn, threshold=PAGE_THRESHOLD):
    """Bin-pack `entries` into pages (lists) by a running total of `weight_fn(entry)`, starting a new
    page whenever adding the next whole entry would push the current page's total past `threshold` --
    never splitting a single entry's own operations/event-names list across two pages. If one entry's
    own weight already exceeds `threshold`, it still gets a page to itself rather than being force-split
    (there's nothing safe to cut it into); real diagrams don't hit this since a single API/event group
    rarely has 60+ operations on its own. Returns a list of non-empty pages; a single page (list containing
    the input list) if nothing needs to split -- callers use `len(pages) == 1` to decide whether to keep
    the unnumbered filename or switch to `_1`/`_2`/... suffixes."""
    pages = []
    current, current_weight = [], 0
    for e in entries:
        w = weight_fn(e)
        if current and current_weight + w > threshold:
            pages.append(current)
            current, current_weight = [], 0
        current.append(e)
        current_weight += w
    if current:
        pages.append(current)
    return pages or [[]]


def _operation_count(api_entry):
    """Total leaf `GET`/`POST`/... operations across every version/resource of one exposedAPIs or
    dependentAPIs entry -- the actual driver of how tall its box renders in the @startyaml diagram."""
    total = 0
    for version in api_entry.get("specification", []) or []:
        for resource in version.get("resources", []) or []:
            for ops in (resource.values() if isinstance(resource, dict) else []):
                total += len(ops or [])
    return total


def _event_count(event_entry):
    """Total event names in one publishedEvents/subscribedEvents entry's `resources` list."""
    return len(event_entry.get("resources", []) or [])


def _write_paginated(diagrams_dir, component_id, base_name, key, entries, weight_fn, report, label):
    """Write `entries` as one or more `@startyaml` files, splitting per `paginate_entries()` once the
    running operation/event count passes PAGE_THRESHOLD. Below the threshold this writes the single
    unnumbered `<ID>_<base_name>.yaml`, unchanged from before pagination existed. Above it, writes
    `<ID>_<base_name>_1.yaml`, `_2.yaml`, ... and deletes any stale numbered (or unnumbered) file left
    over from a previous run with a different page count, so a shrinking diagram doesn't leave an orphan
    behind."""
    pages = paginate_entries(entries, weight_fn)
    unnumbered = os.path.join(diagrams_dir, f"{component_id}_{base_name}.yaml")
    numbered = lambda i: os.path.join(diagrams_dir, f"{component_id}_{base_name}_{i}.yaml")

    keep = set()
    if len(pages) == 1:
        _write_lf(unnumbered, "@startyaml\n" + _dump_yaml({key: pages[0]}) + "\n@endyaml\n")
        keep.add(unnumbered)
    else:
        totals = [sum(weight_fn(e) for e in page) for page in pages]
        report.append(f"{label}: split into {len(pages)} diagrams ({' + '.join(map(str, totals))} = "
                       f"{sum(totals)} total, over the {PAGE_THRESHOLD}-per-diagram threshold)")
        for i, page in enumerate(pages, start=1):
            path = numbered(i)
            _write_lf(path, "@startyaml\n" + _dump_yaml({key: page}) + "\n@endyaml\n")
            keep.add(path)

    stale = set(glob.glob(os.path.join(diagrams_dir, f"{component_id}_{base_name}*.yaml"))) - keep
    for path in stale:
        os.remove(path)
        report.append(f"{label}: removed stale {os.path.basename(path)} (page count changed)")


def _specification_without_urls(specification):
    """Strip the `url` field from every version block before it goes into a Diagrams file. These
    `@startyaml` files are rendered directly as diagram boxes (PlantUML draws the nested YAML verbatim),
    so a `url` here isn't just inert metadata -- it prints the full swagger link as diagram text. Per
    standing instruction, the Exposed/Dependent API diagrams must never show API URLs; only the main
    component YAML (and its own table) carries them."""
    return [{k: v for k, v in version.items() if k != "url"} for version in (specification or [])]


def sync_api_list(main_entries, old_diagram_entries, key):
    """Rebuild an exposedAPIs/dependentAPIs list: current main-YAML entries, names resolved from the
    old diagram file's id->name map. Returns (new_entries, unresolved_ids, report_lines)."""
    old_names = _name_map(old_diagram_entries)
    old_ids = {e["id"] for e in (old_diagram_entries or []) if e.get("id")}
    new_ids = {e["id"] for e in main_entries}

    report = []
    removed = old_ids - new_ids
    added = new_ids - old_ids
    if removed:
        report.append(f"{key}: removed (no longer in main YAML): {sorted(removed)}")
    if added:
        report.append(f"{key}: added (new in main YAML): {sorted(added)}")

    unresolved = []
    new_entries = []
    for e in main_entries:
        name = old_names.get(e["id"])
        if not name:
            unresolved.append(e["id"])
            name = f"UNRESOLVED-{e['id']}"
        new_entry = {"id": e["id"], "name": name, "apiSDO": e.get("apiSDO", "tmForum"),
                     "required": e.get("required", False),
                     "specification": _specification_without_urls(e.get("specification", []))}
        new_entries.append(new_entry)
        old_req = next((oe.get("required") for oe in (old_diagram_entries or []) if oe.get("id") == e["id"]), None)
        if old_req is not None and old_req != e.get("required", False):
            report.append(f"{key}: {e['id']} required flag changed {old_req} -> {e.get('required', False)}")
    return new_entries, unresolved, report


def sync_events(main_published, main_subscribed, old_events_doc):
    """NOT currently called by sync_all() -- see the note there. Kept in place (not deleted) because the
    matching approach is right in principle, just broken for components whose main-YAML event entries
    have no `id` and whose `resources` set no longer matches the existing Diagrams file's (TMFC003:
    3 events dropped, 9 others got an UNRESOLVED-<name> id when this was last actually run). Fix the
    matching, then re-wire this back into sync_all()."""
    old_pub = (old_events_doc or {}).get("publishedEvents", [])
    old_sub = (old_events_doc or {}).get("subscribedEvents", [])
    by_resources = {}
    for e in old_pub + old_sub:
        if e.get("id") and e.get("resources"):
            by_resources[frozenset(e["resources"])] = (e["id"], e.get("name"))

    report = []
    unresolved = []

    def rebuild(main_list, old_list, label):
        new_list = []
        old_ids = {e["id"] for e in old_list if e.get("id")}
        seen_ids = set()
        for e in main_list:
            rid, rname = _resolve_event(e, by_resources)
            if not rid:
                unresolved.append(e.get("name", "<unnamed>"))
                rid = f"UNRESOLVED-{e.get('name', 'unknown')}"
            if not rname:
                rname = e.get("name")  # fall back to the raw main-YAML name if nothing better is known
            seen_ids.add(rid)
            new_list.append({"id": rid, "name": rname, "resources": e.get("resources", [])})
        gone = old_ids - seen_ids
        if gone:
            report.append(f"{label}: removed (no longer in main YAML): {sorted(gone)}")
        return new_list

    new_pub = rebuild(main_published, old_pub, "publishedEvents")
    new_sub = rebuild(main_subscribed, old_sub, "subscribedEvents")
    return new_pub, new_sub, unresolved, report


def sync_all(component_dir, component_id):
    """`component_dir` is the component root (holding the main YAML and the Diagrams/ folder), same as
    always. The three Diagrams/<ID>_*.yaml files this writes/reads now live in Diagrams/temp/, not
    Diagrams/ itself -- per explicit user decision, everything this skill regenerates from scratch each
    run belongs in temp/, not alongside the .docx and hand-maintained files. Call
    build_pdf.reset_temp_dir() before this if you want a guaranteed-clean temp/ (recommended at the
    start of a full regeneration, so no stale prior-run file survives)."""
    main = _load_main_yaml(component_dir)
    core = main["spec"]["coreFunction"]
    diagrams_dir = os.path.join(component_dir, "Diagrams", "temp")
    os.makedirs(diagrams_dir, exist_ok=True)

    report = {"changes": [], "unresolved": []}

    # Old files are read from whichever of the unnumbered or numbered forms currently exists, so name
    # resolution (_name_map) keeps working across a run that changes the page count either direction.
    exposed_path = os.path.join(diagrams_dir, f"{component_id}_Exposed_API.yaml")
    old_exposed = _load_diagram_yaml(exposed_path) or _load_first_page(diagrams_dir, component_id, "Exposed_API")
    new_exposed, unresolved, lines = sync_api_list(
        core.get("exposedAPIs", []), (old_exposed or {}).get("exposedAPIs", []), "exposedAPIs")
    report["changes"] += lines
    report["unresolved"] += [("exposedAPIs", i) for i in unresolved]
    _write_paginated(diagrams_dir, component_id, "Exposed_API", "exposedAPIs", new_exposed,
                      _operation_count, report["changes"], "exposedAPIs")

    dependant_path = os.path.join(diagrams_dir, f"{component_id}_Dependant_API.yaml")
    old_dependant = _load_diagram_yaml(dependant_path) or _load_first_page(diagrams_dir, component_id, "Dependant_API")
    new_dependant, unresolved, lines = sync_api_list(
        core.get("dependentAPIs", []), (old_dependant or {}).get("dependentAPIs", []), "dependentAPIs")
    report["changes"] += lines
    report["unresolved"] += [("dependentAPIs", i) for i in unresolved]
    _write_paginated(diagrams_dir, component_id, "Dependant_API", "dependentAPIs", new_dependant,
                      _operation_count, report["changes"], "dependentAPIs")

    # Events are deliberately NOT synced here -- per-component `_Events.yaml` files are accepted at face
    # value (read as-is, never regenerated) until sync_events()'s id/resources matching is fixed. It
    # currently drops entries and mints UNRESOLVED-<name> ids for components whose main-YAML event
    # entries carry no `id` and whose `resources` set has drifted from the existing Diagrams file (found
    # on TMFC003) -- a real bug, acknowledged, deferred rather than silently corrupting the file on every
    # run. This is a temporary decision, not a permanent design call -- revisit once that's fixed.
    events_path = os.path.join(diagrams_dir, f"{component_id}_Events.yaml")
    if not os.path.exists(events_path):
        report["changes"].append(
            "events: no existing Events.yaml and event sync is currently disabled (see sync_events "
            "docstring) -- this file needs to be authored by hand for a brand-new component")

    return report


if __name__ == "__main__":
    import sys
    component_dir = sys.argv[1]
    component_id = sys.argv[2]
    report = sync_all(component_dir, component_id)
    print("Changes found:")
    for line in report["changes"]:
        print(" -", line)
    if not report["changes"]:
        print(" (none -- Diagrams files already matched the main YAML)")
    if report["unresolved"]:
        print("Unresolved ids/names (no prior name on file -- resolve manually):")
        for group, item in report["unresolved"]:
            print(" -", group, ":", item)
