---
name: Component-data-Harvest
description: Cross-check and fill a TMForum ODA component's eTOM/Functional-Framework references against the official published TM Forum framework releases (GB921 eTOM, GB1033 Functional Framework, GB922 SID). Use this whenever a component's `componentMetadata.eTOMs`/`.functionalFrameworkFunctions` names might not match the official framework's token spelling/casing, or when a component's `<ID>_eTOM_Descriptions.md`/`<ID>_FF_Descriptions.md` lookup files (used by the component-specification-documentation skill's 2.1/2.4 tables) have `*(no description available)*` gaps that an official framework release could fill. Not the same job as component-specification-documentation — that skill builds the document; this one harvests/validates data from TM Forum's own published releases to feed it.
---

# Component data harvest (eTOM / Functional Framework alignment and description backfill)

## What this is for

Three scripts, none of which write to a component's YAML or description files without `--apply`, that
read the **official TM Forum framework releases** (spreadsheets + JSON definitions covering GB921 eTOM,
GB1033 Functional Framework, GB922 SID — every release from v23.0 to v26.0) and check/fill a component's
own data against them:

- **`scripts/framework_lookup.py`** — shared library, not run directly. Resolves which release file to
  read (filenames vary by release, e.g. `GB1033F_Functional_Framework_Excel_v25.5.xlsx` vs
  `GB1033_..._Excel_v23.0.0.xlsx` — matched by family pattern + version prefix, not exact filename) and
  parses it into an id-keyed dict. `load_definitions()` reads the JSON token/name/level definitions;
  `load_ff_descriptions()`/`load_etom_descriptions()`/`load_sid_abe_descriptions()` read the prose
  description spreadsheets.
- **`scripts/align_framework_names.py`** — checks (and, with `--apply`, corrects) a component's
  `eTOMs`/`functionalFrameworkFunctions` entry names against the framework's own `token` field. Alignment
  is exact token comparison, not fuzzy matching — case matters (`Retro-active_order_orchestration` vs
  `Retro-active_Order_Orchestration` was a real, otherwise-invisible mismatch). An id absent from its
  pinned release, or listed more than once in the component's own metadata, is reported and left
  untouched — both are cases where the *id* itself is the suspect part, and only a human should decide
  what was meant.
- **`scripts/fill_descriptions_from_frameworks.py`** — fills `*(no description available)*` placeholder
  rows in a component's `<ID>_eTOM_Descriptions.md`/`<ID>_FF_Descriptions.md` from the framework's own
  description spreadsheets, per the standing precedence rule (component's own published doc wins where it
  has a description; the framework spreadsheet is only the fallback default). Never touches an
  already-populated row — filling a gap isn't the same as regenerating a hand-maintained file, so this is
  safe to re-run.

## Why this is a separate skill from component-specification-documentation

`component-specification-documentation` *consumes* the description lookup files these scripts help fill,
and documents the same precedence rule from the consuming side (see that skill's `references/diagrams.md`,
"eTOM/Functional Framework descriptions"). But generating the document and harvesting/validating data
against TM Forum's own published releases are different jobs with different inputs (a frameworks folder
that lives *outside* this repo, not component YAML) — kept separate so neither skill's description has to
cover both.

## Usage

All three take `--component-dir <TMFCxxx folder>` and `--frameworks <folder>` (the frameworks folder is
**not part of this repository** — it's the published TM Forum releases; ask the user for its path rather
than guessing or hard-coding one, since a stale path fails silently and makes descriptions look genuinely
absent). Both write-capable scripts default to a dry run; pass `--apply` to actually rewrite:

```
python align_framework_names.py --component-dir <dir> --frameworks <dir> [--apply]
python fill_descriptions_from_frameworks.py --component-dir <dir> --frameworks <dir> [--apply]
```

After an `--apply` run of `align_framework_names.py`, record what changed as a note in the component's
Supplement file's 5.3 section (Further resources), per the component-specification-documentation skill's
own convention for editorial provenance notes.

## One release per entry, not one release per run

A component's `eTOMs`/`functionalFrameworkFunctions` list is routinely mixed across releases (e.g. 39
entries at `v25.5` and 2 at `v23.0` in the same list) — both scripts look each id up in the release *its
own entry is pinned to*, never one blanket release for the whole run. The same id can carry different
wording (or even a different token) across releases, so a single-workbook lookup would silently return the
wrong revision for part of the list.
