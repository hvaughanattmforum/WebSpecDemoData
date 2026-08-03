"""
Regenerate a component's three Diagrams/<ID>_{Exposed_API,Dependant_API,Events}.yaml files from its
current main component YAML, instead of assuming they're already in sync.

Why this exists: these three files are the source for the Exposed API / Dependent API / Events
diagrams AND the display-name lookup used when writing the tables in the generated Markdown. They are
maintained as separate files alongside the main YAML, not auto-derived from it on every edit -- so
they can silently drift (an API added/removed from the main YAML without the Diagrams file being
touched, a required flag flipping, a resource/operation list changing). Regenerate them every time this
skill runs, before treating them as a data source, rather than trusting they're current.

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
                     "required": e.get("required", False), "specification": e.get("specification", [])}
        new_entries.append(new_entry)
        old_req = next((oe.get("required") for oe in (old_diagram_entries or []) if oe.get("id") == e["id"]), None)
        if old_req is not None and old_req != e.get("required", False):
            report.append(f"{key}: {e['id']} required flag changed {old_req} -> {e.get('required', False)}")
    return new_entries, unresolved, report


def sync_events(main_published, main_subscribed, old_events_doc):
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
    main = _load_main_yaml(component_dir)
    core = main["spec"]["coreFunction"]
    diagrams_dir = os.path.join(component_dir, "Diagrams")

    report = {"changes": [], "unresolved": []}

    exposed_path = os.path.join(diagrams_dir, f"{component_id}_Exposed_API.yaml")
    old_exposed = _load_diagram_yaml(exposed_path)
    new_exposed, unresolved, lines = sync_api_list(
        core.get("exposedAPIs", []), (old_exposed or {}).get("exposedAPIs", []), "exposedAPIs")
    report["changes"] += lines
    report["unresolved"] += [("exposedAPIs", i) for i in unresolved]
    _write_lf(exposed_path, "@startyaml\n" + _dump_yaml({"exposedAPIs": new_exposed}) + "\n@endyaml\n")

    dependant_path = os.path.join(diagrams_dir, f"{component_id}_Dependant_API.yaml")
    old_dependant = _load_diagram_yaml(dependant_path)
    new_dependant, unresolved, lines = sync_api_list(
        core.get("dependentAPIs", []), (old_dependant or {}).get("dependentAPIs", []), "dependentAPIs")
    report["changes"] += lines
    report["unresolved"] += [("dependentAPIs", i) for i in unresolved]
    _write_lf(dependant_path, "@startyaml\n" + _dump_yaml({"dependentAPIs": new_dependant}) + "\n@endyaml\n")

    events_path = os.path.join(diagrams_dir, f"{component_id}_Events.yaml")
    old_events = _load_diagram_yaml(events_path)
    new_pub, new_sub, unresolved, lines = sync_events(
        core.get("publishedEvents", []), core.get("subscribedEvents", []), old_events)
    report["changes"] += lines
    report["unresolved"] += [("events", i) for i in unresolved]
    _write_lf(events_path, "@startyaml\n" + _dump_yaml({"publishedEvents": new_pub, "subscribedEvents": new_sub}) + "\n@endyaml\n")

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
