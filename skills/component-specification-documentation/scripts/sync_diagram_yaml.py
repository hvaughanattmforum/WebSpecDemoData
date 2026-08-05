"""
Regenerate a component's Diagrams/temp/<ID>_{Exposed_API,Dependant_API,Events,Published_Events,
Subscribed_Events}.yaml files from its current main component YAML, instead of assuming they're already
in sync. Everything this module writes is disposable and rebuilt from scratch on every run -- per
explicit user decision, none of it is a hand-maintained, carried-forward file (unlike the Supplement,
eTOM-SID Links, and eTOM/FF/SID Descriptions files, which live directly under Diagrams/ and this module
never touches).

Why this exists: these files are the source for the Exposed API / Dependent API / Events diagrams AND
the display-name lookup used when writing the tables in the generated Markdown. The API lists are
maintained as separate files alongside the main YAML, not auto-derived from it on every edit -- so they
can silently drift (an API added/removed from the main YAML without the Diagrams file being touched, a
required flag flipping, a resource/operation list changing). Regenerate them every time this skill runs,
before treating them as a data source, rather than trusting they're current.

Name resolution for the API lists: this script never invents a display name. It reuses the existing
Diagrams file's id->name mapping (it already did the hard work of resolving names once) for any id
that's still present, falls back to the main component YAML's own `name` field for that entry (already
present, not derived), and only reports an id as unresolved -- to be resolved by hand (e.g. via
apiIndex.json or the TMF spec) -- if neither source has a name for it, which should be rare.

Events are different, per explicit user decision: there is no name resolution step and no matching
against an old file or against the exposedAPIs/dependentAPIs lists at all -- `sync_events()` is a direct
passthrough of the main YAML's own publishedEvents/subscribedEvents (see `_merge_event_entries`), which
sidesteps the old resources-set matching bug entirely (it used to drop entries and mint fake
`UNRESOLVED-<name>` ids once the main YAML's `resources` drifted from an old Diagrams file's -- confirmed
on TMFC003) rather than trying to fix that matching.

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
    """id -> name, from an existing (already name-resolved) Diagrams file's entry list. A prior
    `UNRESOLVED-<id>` placeholder is deliberately excluded -- it's not a real resolution, and treating
    it as one would lock that placeholder in permanently (every later run would see it as "the existing
    name" and never fall through to the main YAML's real one)."""
    m = {}
    for e in entries or []:
        if e and e.get("id") and e.get("name") and not e["name"].startswith("UNRESOLVED-"):
            m[e["id"]] = e["name"]
    return m


def _merge_event_entries(main_list):
    """Group main-YAML publishedEvents/subscribedEvents entries by their own raw `name` (e.g.
    "ProductOrder"), merging duplicate version entries (a v4 and a v5 block for the same event group)
    into one, with their `resources` lists combined and de-duplicated, order preserved. Per explicit
    user decision, this is a direct passthrough of the main YAML's own event data -- no `id` is invented,
    no cross-referencing against exposedAPIs/dependentAPIs to resolve a "cleaner" display name. Whatever
    the main YAML says is what the Events diagram shows."""
    order = []
    merged = {}
    for e in main_list:
        name = e.get("name", "<unnamed>")
        if name not in merged:
            merged[name] = {"name": name, "resources": []}
            order.append(name)
        for r in e.get("resources", []) or []:
            if r not in merged[name]["resources"]:
                merged[name]["resources"].append(r)
    return [merged[n] for n in order]


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
    old diagram file's id->name map where one exists, falling back to the main YAML entry's own `name`
    field (it already carries one for every entry) rather than fabricating an `UNRESOLVED-<id>`
    placeholder -- there's no reason to treat a name that's already sitting right there in the source of
    truth as missing. `unresolved_ids` (returned) now only fires for the genuinely-pathological case of
    a main YAML entry with no `name` field of its own and no prior resolution either; that should be rare
    and worth flagging by hand. Returns (new_entries, unresolved_ids, report_lines)."""
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
        name = old_names.get(e["id"]) or e.get("name")
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


def sync_events(main_published, main_subscribed):
    """Rebuild the Published/Subscribed Events lists straight from the main YAML every run -- called by
    sync_all() same as the API lists. Per explicit user decision, this is a direct passthrough (see
    `_merge_event_entries`): no matching against an old Diagrams file, no cross-referencing against
    exposedAPIs/dependentAPIs to invent an `id` or a "resolved" display name. The old approach tried to
    carry forward an `id`+resolved-name pair from a previous Diagrams file by matching on the
    `resources` set, which broke silently once that set drifted (confirmed on TMFC003: 3 events dropped,
    9 others got a fabricated `UNRESOLVED-<name>` id) -- rather than fix that matching, the simpler and
    more correct rule is to not resolve anything at all and just emit what the main YAML says."""
    return _merge_event_entries(main_published), _merge_event_entries(main_subscribed)


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

    # Events are regenerated fresh every run too, same as the API lists above -- per explicit user
    # decision, as a direct passthrough of the main YAML's own publishedEvents/subscribedEvents (see
    # sync_events()/`_merge_event_entries`), with no old-file matching and no cross-referencing against
    # exposedAPIs/dependentAPIs.
    new_pub, new_sub = sync_events(core.get("publishedEvents", []), core.get("subscribedEvents", []))
    _write_paginated(diagrams_dir, component_id, "Published_Events", "publishedEvents", new_pub,
                      _event_count, report["changes"], "publishedEvents")
    _write_paginated(diagrams_dir, component_id, "Subscribed_Events", "subscribedEvents", new_sub,
                      _event_count, report["changes"], "subscribedEvents")
    _write_lf(os.path.join(diagrams_dir, f"{component_id}_Events.yaml"),
              "@startyaml\n" + _dump_yaml({"publishedEvents": new_pub, "subscribedEvents": new_sub}) +
              "\n@endyaml\n")

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
