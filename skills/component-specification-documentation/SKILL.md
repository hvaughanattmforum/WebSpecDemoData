---
name: component-specification-documentation
description: Generate (or refresh) the main TMFCxxx component specification document as Markdown plus a PDF and a Word (.docx) export, with PlantUML and hand-drawn SVG diagrams, for a TMForum ODA component. Use this whenever the user asks for a component's specification, overview document, or "main doc" in Markdown/.md, PDF, or Word/.docx form (as opposed to the ComponentConformanceProfile, which is a different document handled by the component-conformance-profile skill), whenever they mention turning a TMFCxxx PDF/docx into Markdown, or whenever they ask for eTOM/SID diagrams, API context diagrams, or exposed/dependent API/event diagrams for a component. Trigger this proactively when a component's YAML changes in a way that would affect this document (name, description, eTOMs, SIDs, functionalFrameworkFunctions, exposedAPIs, dependentAPIs, publishedEvents, subscribedEvents) — this document should stay in sync with the YAML the same way the conformance profile does.
---

# Component Specification Markdown Generator

## What this produces and why

Two files that together are the source-of-truth-driven counterpart of a component's existing
`TMFCxxx_<Name>.pdf` in **TMForum-ODA-Component-Specification**
(`specifications/<ComponentFolder>/TMFCxxx_<Name>.pdf`), plus a generated PDF and a generated Word
(`.docx`) export that each combine them:

- `Diagrams/TMFCxxx_<Name>.md` — regenerated fresh every run, entirely from YAML. Sections 1–4 and 5.1.
- `Diagrams/TMFCxxx_<Name>_Supplement.md` — hand-maintained, never auto-regenerated once it exists. Sections
  5.2, 5.3, and 6 (Jira References, Further resources, Administrative Appendix) — curated editorial content
  with no YAML equivalent. See "Supplement file" below.
- `TMFCxxx_<Name>.pdf` **at the component root** and `Diagrams/TMFCxxx_<Name>.docx` — generated on every
  run from the two `.md` files above, see "Also produce a PDF" and "Also produce a Word document (.docx)"
  below. These two land in different places, both deliberate: the PDF has an official, published
  location to overwrite (the component root, where the original PDF already lived), so it's written
  straight there and never has a standing copy in `Diagrams/`. The `.docx` has no such pre-existing
  official location — no component has an official `.docx` today — so it's a working artifact that lives
  in `Diagrams/` only, not something this skill writes anywhere else. Revisit that if it ever changes
  (e.g. if a component's official spec starts being published as `.docx` too). Everything else either
  script needs — the main `.md` itself, every diagram source/image, rasterization caches, mid-assembly
  render passes — goes into `Diagrams/temp/` instead — see "`Diagrams/temp/`" under "Also produce a PDF"
  below.

The main `.md` lives inside the component's `Diagrams/temp/` folder — disposable build output, not a
standalone checked-in deliverable — while its Supplement stays hand-maintained directly in `Diagrams/`
itself, not at the component root next to the main YAML. See "Where the data lives" below for why and what
that means for image/source paths inside the main `.md`.

**The original PDF is no longer needed to generate this document at all** — not for structure, not for
cover/notice boilerplate, not for chapters 5/6. Every fact that used to come from reading the old PDF now
comes from either the component YAML (cover metadata, chapters 1–4, 5.1) or the hand-maintained Supplement
file (5.2, 5.3, 6). This means the skill now works for a component that never had a published PDF at all —
seed a new Supplement file from [templates/Supplement_Template.md](templates/Supplement_Template.md) rather
than needing an existing document to extract from. (An existing PDF is still a *convenient* one-time source
when first authoring a Supplement file for a component that already has one — see "Supplement file" below —
but it's a starting point to copy from, not something the generation process depends on.)

Every fact in the generated `.md` (name, description, eTOM/SID/Functional-Framework references, exposed/
dependent APIs, events) must be read fresh from the component's YAML files, never copied from an old PDF's
text — the whole point of regenerating this document is to catch and reflect YAML drift, not preserve
whatever a document happened to say the last time it was published.

## Where the data lives

Everything for one component sits under `specifications/<ComponentFolder>/` in
**TMForum-ODA-Component-Specification** (`https://github.com/tmforum-rand/TMForum-ODA-Component-Specification`,
branch `v1.1.0`):

- `<ComponentFolder>.yaml` — the main component spec (`componentMetadata`, `coreFunction.exposedAPIs`,
  `coreFunction.dependentAPIs`, `coreFunction.publishedEvents`, `coreFunction.subscribedEvents`). This is
  the primary source for almost everything in the document.
- `Diagrams/<ComponentID>_Exposed_API.yaml`, `Diagrams/<ComponentID>_Dependant_API.yaml`,
  `Diagrams/<ComponentID>_Events.yaml` — pre-existing PlantUML `@startyaml`/`@endyaml` files, one per
  diagram, maintained alongside the main YAML for every component. Unlike the main YAML, these already
  carry a resolved human-readable `name` next to each API `id` (e.g. `id: TMF620` /
  `name: Product Catalog Management API`) — use that as your name-resolution source for API display names
  in both the diagrams and the tables, since it's more direct than cross-referencing `apiIndex.json`.

  **Always regenerate the Exposed/Dependent API files from the current main YAML before using them —
  every run, not just when drift is suspected.** They're separately maintained, not auto-derived from the
  main YAML on every edit, so they can silently drift (an API added/removed without the Diagrams file
  being touched, a `required` flag flipping, a resource/operation list changing) — treating them as
  trustworthy-as-is was the previous approach, and it isn't safe. Use
  [scripts/sync_diagram_yaml.py](scripts/sync_diagram_yaml.py):

  ```python
  import sys
  sys.path.insert(0, "<path to this skill's scripts/ folder>")
  from sync_diagram_yaml import sync_all

  report = sync_all(component_dir, "TMFC012")  # component_dir = the folder holding the main YAML + Diagrams/
  ```

  This rebuilds the Exposed/Dependent API files' entry lists fresh from `coreFunction.exposedAPIs` /
  `.dependentAPIs`, reusing the *existing* Diagrams file's `id → name` resolutions (it already did that
  work once) where one exists, falling back to that same main-YAML entry's own `name` field otherwise —
  never inventing a name from nothing. It reports what changed (entries added/removed, `required` flips)
  and any id that has no name in *either* place — resolve those by hand (e.g. via `apiIndex.json` or the
  TMF spec) rather than leaving a placeholder in the file; this should now be rare, since the main YAML
  carries a `name` for essentially every entry.

  **`<ComponentID>_Events.yaml` is regenerated fresh by `sync_all()` every run**, same as the Exposed/
  Dependent API files — it is *not* one of the hand-maintained files (Links/Descriptions/Supplement)
  and is never carried forward as a trusted cache. Per explicit user decision, `sync_events()` does not
  try to resolve an `id` or a "cleaner" display name for each event group at all — no matching against
  an old Diagrams file, no cross-referencing against `exposedAPIs`/`dependentAPIs`. It's a direct
  passthrough of the main YAML's own `publishedEvents`/`subscribedEvents`: entries with the same raw
  `name` are merged (duplicate version blocks combined into one, `resources` de-duplicated), and that
  raw `name` is what the diagram shows — nothing more. This deliberately sidesteps the old
  resources-set matching bug (confirmed on TMFC003: it used to drop 3 events and mint fake
  `UNRESOLVED-<name>` ids for 9 others once the main YAML's `resources` drifted from an old Diagrams
  file) rather than fixing that matching — the simpler passthrough has nothing to drift against.

  This does reformat the files (consistent 2-space indent throughout, replacing whatever hand/tool-authored
  indentation was there before) — mention that in your summary so a real diff doesn't come as a surprise,
  but don't try to preserve the old formatting; correctness matters more here than byte-for-byte history.
  Write with `newline="\n"` explicitly — a plain Windows text-mode write silently turns every `\n` into
  `\r\n`, which would make every single line show as changed in git diff even when content didn't change
  (the repo's `core.autocrlf=true` handles the local-checkout line-ending presentation on its own).

  **These files, and therefore the Exposed/Dependent API diagrams rendered from them, must never show an
  API's `url`.** `sync_diagram_yaml.py`'s `sync_api_list()` strips the `url` field from every
  `specification` version block before writing (`_specification_without_urls()`) — these `@startyaml`
  files are rendered verbatim as diagram boxes, so a `url` here isn't inert metadata, it prints the full
  swagger link as diagram text. The main YAML and the 3.2/3.3 tables are unaffected; this only concerns
  what the diagram itself displays. If you ever hand-edit one of these three Diagrams files instead of
  going through the sync script, strip `url` the same way before saving.
- `TMFCxxx_<Name>.pdf` — **only needed for one specific, one-time, component-by-component task, and only if
  `Diagrams/<ComponentID>_eTOM_SID_Links.md` doesn't exist yet**: manually reading off the eTOM–SID link
  diagram to seed that Links file (see [references/diagrams.md](references/diagrams.md), "eTOM–SID
  diagram") — that one diagram genuinely can't be derived from YAML. Once the Links file exists for a
  component, this original PDF is irrelevant to that diagram too, same as everything else: cover metadata
  is YAML-derived (see "Cover page & Notice" below) and chapters 5.2/5.3/6 live in the hand-maintained
  Supplement file (see "Supplement file" below), seeded from this PDF only the first time, if one already
  exists for the component. This original PDF lives at the component root, separate from the generated
  `.md`/Supplement/Links/diagrams below during generation — but see "Naming/overwrite behavior" further
  down: once the fresh PDF is built, it overwrites this file at the component root as the final step,
  per standing user instruction. It isn't a static, permanently-untouched artifact.
- `Diagrams/<ComponentID>_eTOM_Descriptions.md`, `Diagrams/<ComponentID>_SID_Descriptions.md`, and
  `Diagrams/<ComponentID>_FF_Descriptions.md` — three more hand-maintained, read-only data sources, same
  status as the Links file above. `componentMetadata.eTOMs`, `.SIDs`, and `.functionalFrameworkFunctions`
  carry only an ID/name/version, never prose — the descriptive text (and, for Functional Framework
  Functions, the two Aggregate Function Level columns; for SID ABEs, a separate Level 1 and Level 2
  definition) only exists in the officially-published component document or the official framework
  spreadsheets, transcribed once into these files. See "eTOM/Functional Framework descriptions" in
  [references/diagrams.md](references/diagrams.md) for the exact format and the lookup-by-ID rule for
  sections 2.1/2.4, and "SID descriptions" for section 2.2's variant of the same rule.
- `Diagrams/temp/TMFCxxx_<Name>.md` — the generated main document, living inside `Diagrams/temp/` as a
  sibling of the diagram source/image files it references (see "`Diagrams/temp/`" under "Also produce a
  PDF" below for why this is disposable build output, not a standalone checked-in deliverable). This means
  every image/source reference inside it is a bare filename (`TMFC001_eTOM_SID.svg`), not
  `Diagrams/TMFC001_eTOM_SID.svg` or `temp/TMFC001_eTOM_SID.svg` — don't add either prefix back in, the
  `.md` and the assets it references are in the same directory. `Diagrams/TMFCxxx_<Name>_Supplement.md`,
  `Diagrams/<ComponentID>_eTOM_SID_Links.md`, and the three description files above stay one level up, in
  `Diagrams/` itself, since they're hand-maintained rather than regenerated. See "Supplement file" below for
  the Supplement file, "eTOM–SID diagram" and "eTOM/Functional Framework descriptions" in
  [references/diagrams.md](references/diagrams.md) for the Links/Descriptions files, and "Write the file"
  below for the main `.md`'s exact output path.

**Local repo**: this is normally already cloned at
`C:\Users\HugoVaughan\source\repos\tmforum-rand\TMForum-ODA-Component-Specification`, checked out on
`v1.1.0`, authenticated via `gh` (account `hvaughanattmforum`, already logged in — `gh auth status`
confirms it). Read directly from this local clone; only reach for `git fetch`/`gh api` if the component
you need isn't present locally or the branch is stale. There's also frequently a synced copy under the
user's OneDrive (`OneDrive - TM Forum\Apps\ODA Component Editor\TMForum-ODA-Component-Specification-1.1.0\`)
— treat the git clone as authoritative if the two ever disagree, since OneDrive is a snapshot from an
external editor tool, not the git history.

## Front matter

The generated Markdown's YAML front matter carries exactly one field, from `componentMetadata` in the
main YAML — nothing else (no id, version, date, or description; the description already lives in the body's
1. Overview table, and adding more fields un-asked invites them going stale relative to the body):

```yaml
---
name: <human-readable component name>
---
```

`componentMetadata.name` in the YAML is a concatenated identifier (e.g. `ProductInventory`), not the
spaced display form used in the document title (`Product Inventory`). Convert it by inserting a space
before every uppercase letter that follows a lowercase letter (`ProductInventory` → `Product Inventory`,
`ServiceOrderManagement` → `Service Order Management`). Don't use `componentMetadata.id` (`TMFC005`) here —
that belongs in the document's `#` heading, not the front matter.

## Body structure

Mirror the existing PDF's numbered sections, but derive every value from YAML per the mapping below.
Drop the PDF's cover page and copyright/notice boilerplate — the description already lives in the body's
1. Overview table, and the notice text is legal boilerplate the PDF-generation tool re-adds at publication
time, not something this Markdown needs to own.

`# <componentMetadata.id> – <display name>`

### 1. Overview
A short table or bullet list: Component Name, ID, Description, ODA Function Block — from
`componentMetadata.name` (spaced), `.id`, `.description`, `.functionalBlock`.

### 2. eTOM Processes, SID Data Entities and Functional Framework Functions
Three tables, each parsed from a `componentMetadata` list of pipe-delimited strings. Read
[references/diagrams.md](references/diagrams.md) section "Parsing componentMetadata lists" for the exact
splitting rules (level inference from ID depth, `_ABE` stripping, etc.) — don't improvise your own
parsing, since the level-inference rule in particular is easy to get subtly wrong.

**Descriptions (2.1, 2.2, and 2.4)**: `componentMetadata.eTOMs`, `.SIDs`, and `.functionalFrameworkFunctions`
never carry prose — that text (and, for Functional Framework Functions, the two Aggregate Function Level
columns; for SID ABEs, separate Level 1 and Level 2 definitions) comes from
`Diagrams/<ComponentID>_eTOM_Descriptions.md` / `Diagrams/<ComponentID>_SID_Descriptions.md` /
`Diagrams/<ComponentID>_FF_Descriptions.md`, hand-maintained lookup files transcribed once from the
officially-published component doc (gap-filled from the official framework spreadsheets) — see
"eTOM/Functional Framework descriptions" and "SID descriptions" in
[references/diagrams.md](references/diagrams.md) for the exact format and the ID-matching rule. **Check
whether the relevant file(s) exist for the component before writing the 2.1/2.2/2.4 tables**:
- If they exist, add a `Description` column to 2.1 (looked up by eTOM identifier); `SID ABE L1 Definition` /
  `SID ABE L2 Definition` columns to 2.2 (looked up by the same SID ABE Level 1/Level 2 names the row itself
  resolves to — see "SID descriptions" for the exact matching rule, since there's no single YAML ID to key
  on here the way there is for 2.1/2.4); and `Function Description` / `Aggregate Function Level 1` /
  `Aggregate Function Level 2` columns to 2.4 (looked up by Function ID) — matching the shape of the
  officially-published document's own tables.
- If a file doesn't exist yet for this component, build it from the framework spreadsheets (below) rather
  than emitting YAML-only columns.

**Description precedence — the standing rule, and it applies identically to eTOM (2.1) and Functional
Framework (2.4)**:

1. **The component document wins.** If the component's own `TMFCnnn` doc has a description for an ID, keep
   it — even when the framework spreadsheet's wording for that same ID differs. The component doc's text
   was written/curated for this component and takes precedence; a difference is not a defect to reconcile.
2. **Otherwise take the framework spreadsheet's default.** If the `TMFCnnn` doc has no description for an
   ID (the ID postdates the published doc, or the component was never published), look the ID up in the
   official framework spreadsheet and use that as the default.
3. **Only if neither source has it** does the cell get `*(no description available)*` — never a blank and
   never a guess. This should now be rare, and when it happens it usually means the ID doesn't exist in any
   framework release at all (i.e. a dangling YAML reference worth flagging in your chat summary).

The framework spreadsheets are on disk and cover every release, so **"this component was never published,
so it can't have prose" is no longer a valid outcome** — see "Sourcing descriptions from the framework
spreadsheets" in [references/diagrams.md](references/diagrams.md) for the folder, the per-release lookup
rule, and the sheet/column gotchas.

Whichever source a cell came from, don't add an inline note in the document explaining it (see "Handling
YAML/PDF disagreement" below — provenance belongs in the lookup file's own `Source:` line and in your chat
summary, not the document body).

Then the **eTOM L2 – SID ABEs links** diagram — see [references/diagrams.md](references/diagrams.md).

### 3. TM Forum Open APIs & Events
- **3.1 API Context Diagram** — placed first, right after the section's intro bullets and before the
  detailed subsections that follow, since it's the whole-component overview and reads best before the
  itemized tables. See "The API context diagram is different" below.
- **3.2 Exposed APIs** — table from `coreFunction.exposedAPIs` (ID, name from the Diagrams file, mandatory/
  optional from `required`, version, resources, operations), followed by the Exposed API diagram.
- **3.3 Dependent APIs** — same shape from `coreFunction.dependentAPIs`, followed by the Dependent API
  diagram.
- **3.4 Events** — two tables (Published, Subscribed) from `coreFunction.publishedEvents` /
  `.subscribedEvents`, followed by **two separate diagrams** (Published Events, Subscribed Events) — not
  one combined diagram. See [references/diagrams.md](references/diagrams.md) for exactly how to split the
  existing combined `Diagrams/<ComponentID>_Events.yaml` into the two.

**Multi-value cells (3.2/3.3's Resources and Operations columns, 3.4's event-name column): one entry per
line, joined with `<br>`, never comma-space-joined.** E.g. a resource's operations render as
`GET<br>GET /id<br>POST<br>PATCH<br>DELETE`, not `GET, GET /id, POST, PATCH, DELETE`; a resource list as
`productOffering<br>productOfferingPrice<br>productSpecification`; an event-name cell the same way, one
event per line. This is a new line **within the same cell**, not a new table row — every other column on
that row (ID, name, mandatory/optional, version) still applies to the whole multi-line cell as one row, the
same grouping as before, just readable instead of wrapped. `<br>` is plain HTML and renders correctly as a
line break in the `.md` (GitHub/most Markdown viewers honor it inside a table cell), the PDF (passed
through by `markdown` untouched, rendered by `xhtml2pdf`), and the `.docx` (`build_docx.py`'s `_parse_inline`
turns `<br>`/`<br/>` into a `{"break": True}` run, which `build_docx_scroll.py`'s `_add_runs` turns into a
same-paragraph line break via `run.add_break()` — not a second table row or a second paragraph). Both
scripts' column-width weighting (`_cell_text_len` in `build_pdf.py`, `_cell_weight`/`_col_widths_pct` in
`build_docx.py`) measures the **longest individual line** in a `<br>`-joined cell, not the concatenated
total — sizing the column to what actually needs to fit on one line now that entries stack vertically
instead of flowing inline.

### 4. Machine Readable Component Specification
A fixed pointer sentence to the ODA Component Directory on the TM Forum website — this section has never
been YAML-derived and never varies by component; it's a constant, not something to look up per component.

### 5. References — 5.1 only; 5.2/5.3 live in the Supplement file
**5.1 TMF Standards related versions** is the one part of chapter 5 that belongs in the main `.md` — it's
YAML-derived, so it stays in sync with everything else in the document. Derive it from the version suffix
on each `componentMetadata.eTOMs` / `.SIDs` / `.functionalFrameworkFunctions` entry (e.g. `v24.0`, `v25.0`),
one row per standard. If SIDs are on a newer version than eTOM/Functional Framework (as is genuinely the
case for some components right now), show that difference rather than flattening it to match old prose —
that's a real, useful signal, not noise.

5.2 (Jira References) and 5.3 (Further resources) have no YAML equivalent — they live in the Supplement
file instead (see "Supplement file" below). Don't emit them in the main `.md` at all.

### 6. Administrative Appendix — entirely in the Supplement file
The whole of chapter 6 (Document History, Acknowledgements) is editorial/publication metadata with no YAML
source — it lives entirely in the Supplement file (see "Supplement file" below), not the main `.md`.

## Supplement file (chapters 5.2, 5.3, and 6)

`specifications/<ComponentFolder>/Diagrams/TMFCxxx_<Name>_Supplement.md` (same directory as the main `.md` —
i.e. the component's `Diagrams/` folder, not the component root — same base filename as the main `.md` plus
`_Supplement`) holds chapters 5.2 (Jira References), 5.3 (Further resources), and 6 (Administrative Appendix
— Document History, Acknowledgements). This content has no YAML source and is
genuinely curated/editorial — per explicit user instruction, it's split out into its own file specifically
so a human can edit it directly without that edit being at risk of being silently overwritten the next time
this skill regenerates the main `.md`.

Files maintained through the Component Specification Studio app's "Document History" tab start with their
own `---`-delimited front matter (`name`/`version`, mirrored live from `componentMetadata` — display-only in
that app, regenerated on every save rather than hand-edited). `scripts/build_pdf.py` strips it before
concatenation, same as the main `.md`'s front matter, so it never appears in the rendered PDF.

**Never regenerate or overwrite an existing Supplement file as part of running this skill.** Once it
exists, treat it exactly like the Diagrams-file inputs the *other* direction — a data source you read, not
an output you write. If the user asks to update Jira references, add a document-history row, etc., edit the
Supplement file directly as its own small task; don't regenerate it from scratch as a side effect of
refreshing the main `.md`.

**Creating a new Supplement file** (a component being documented for the first time with this skill):
- If the component already has an existing official `TMFCxxx_<Name>.pdf`, seed the new file by reading that
  PDF's chapters 5.2/5.3/6 and transcribing them — this is the one remaining legitimate use of an old PDF,
  a **one-time authoring aid**, not an ongoing dependency. Do this once; from then on the Supplement file is
  the source, and the PDF is irrelevant to future runs.
- If there's no existing PDF at all (a genuinely new component), start from
  [templates/Supplement_Template.md](templates/Supplement_Template.md) instead — copy it to
  `TMFCxxx_<Name>_Supplement.md` and fill in real content, deleting the template's placeholder comments and
  any subsection that ends up with nothing real to say (don't leave a subsection with only placeholder text
  or an empty table row in the final file).

**Assembly**: `scripts/build_pdf.py` concatenates the main `.md` (through 5.1) with the Supplement file
(5.2 onward) before rendering, so the final PDF reads as one continuous document — see "Also produce a
PDF" below. The two `.md` files themselves stay physically separate; nothing merges them on disk.

## Handling YAML/PDF disagreement

Because the YAML is the source of truth and the PDF is just structural scaffolding, don't be alarmed when
generated content differs from the old PDF's numbers or wording (e.g. a SID ABE table that splits
differently, or a standards-version table that no longer shows one flat version for everything) — that's
expected and is the reason to regenerate in the first place. Do call it out **in your chat summary to the
user** when you generate the doc, the same way the conformance-profile skill surfaces mandatory/optional
drift, so a genuine upstream YAML mistake (as opposed to an intentional update) gets a chance to be noticed.

**None of this belongs inline in the generated document, in any form — no exceptions.** Per explicit user
feedback (which required stripping this kind of commentary back out of TMFC005/010/012's generated `.md`
after it had already crept in, as both `>` blockquotes and ordinary paragraphs, including the ones this
SKILL.md used to call "structural" — e.g. "description text isn't part of the component YAML"), never write
an aside into the `.md` body explaining a field, a casing convention, why a column is empty or a table is
sparser than the old PDF, comparing this component to another one already tested, or flagging a "pattern
confirmed across components." The document is a spec, not an annotated diff or a running log of this
skill's own testing notes. Just emit the columns/values you *can* derive and stop — don't add a one-line
explanation for what you left out or why. Everything of that kind goes in your chat summary to the user
instead, every time you generate or refresh the document.

**Patterns confirmed across more than one component** (TMFC005 and TMFC010 so far) — still worth naming in
your summary each time since they're genuine data points, but don't treat them as newly-discovered
anomalies specific to whichever component you're on:
- eTOM and Functional Framework versions tend to lag a full version behind SID (e.g. `v23.0`/`v23.0` vs
  `v25.0`), while the old PDF's standards-version table usually shows one flat, stale version for all
  three. Recurring, not a one-off.
- A component's `Diagrams/<ID>_Dependant_API.yaml` *sometimes* spells a v4 resource with British spelling
  (`organisation`) where the main component YAML's v4 entry for the same resource uses American spelling
  (`organization`) — seen identically in TMFC005 and TMFC010's `TMF632` (Party) dependency. **Not
  universal**, though: TMFC012's `TMF632` entry spells it `organization` consistently in both files, at
  both v4 and v5. Check each component's own Diagrams file rather than assuming the mismatch recurs; when
  it does, use the main YAML's spelling for the table and let the diagram (verbatim from its own file)
  show whatever it shows.
- A component depending on a narrower slice of its own exposed API (e.g. TMFC005, TMFC010, and TMFC012 all
  list their own primary API in `dependentAPIs` too, with fewer operations) is a recurring, apparently
  intentional pattern, not a data error to flag as broken.
- `componentMetadata.status` and `.functionalBlock` are two different fields with two different, both
  intentional, casing conventions — don't flag them matching or looking similar as an error.
  `.status` is the component's position in the *lifecycle* and is **never capitalized** (e.g. `production`,
  lowercase). `.functionalBlock` is a *classification* of the component's type and is **always
  capitalized** (e.g. `Production`, a category name, not a lifecycle state — it happens to read the same as
  a lowercase `.status` value in some components, which is what looked like a bug in earlier testing, but
  isn't one). Render each field's value with its own casing exactly as it appears in the YAML — don't
  normalize one to match the other.

## Diagrams

Five diagram types are needed; each has a different data source and a different amount of skill-specific
construction. Read [references/diagrams.md](references/diagrams.md) before generating any of them — it has
the exact PlantUML patterns, the ball/socket lollipop syntax, and (for the eTOM–SID diagram specifically)
the `Diagrams/<ComponentID>_eTOM_SID_Links.md` check-first step — the one-time manual PDF-inspection step
only runs the first time that file doesn't exist yet.

Quick map:
| Diagram | Section | Source |
|---|---|---|
| API context | 3.1 (placed before the other 3.x subsections — see below) | built fresh, purely from YAML — **hand-drawn SVG, not PlantUML** (see below) |
| Exposed API | 3.2 | `Diagrams/<ID>_Exposed_API.yaml`, used near-verbatim (PlantUML `@startyaml`) — **split into `_1`/`_2`/... once the total operation count passes 60**, see "Splitting oversized Exposed/Dependent API and Events diagrams" below |
| Dependent API | 3.3 | `Diagrams/<ID>_Dependant_API.yaml`, used near-verbatim (PlantUML `@startyaml`) — same 60-operation split rule (TMFC003's is a real example, 160 operations across 3 pages) |
| Published Events / Subscribed Events | 3.4 | `Diagrams/<ID>_Events.yaml`, split into two (PlantUML `@startyaml`) — each of those two can itself further split past 60 event names, same rule |
| eTOM–SID links | 2.3 | built fresh from `Diagrams/<ID>_eTOM_SID_Links.md`'s 5-column table (`eTOM activity \| SID ABE \| Direction \| YAML eTOM \| YAML SID`) — the first 3 columns are hand-maintained and seeded once from the existing PDF's diagram image, never re-derived from the PDF after that; the last 2 are a derived YAML cross-reference, refreshed on every read (see references/diagrams.md). `Direction` is always exactly `bidirectional` / `activity produces` / `activity consumes`. PlantUML `@startuml` if the diagram has **6 or fewer** total eTOM+SID elements, otherwise **hand-drawn SVG** (see below). For any SID ABE flagged `external (cross-component)`, look up which component it's depicted under in the repo-root `docs/Common_Links/Common_Component_SID_owner_Links.md` — matched by `Domain\|ABE[\|BE]` token path, ignoring the version suffix on both sides (that file's data is treated as true for every framework version, not just the one its own row is pinned to) — see "Which component a cross-component SID ABE is depicted under" in references/diagrams.md |

**Every diagram gets its own standalone source file in `Diagrams/`**, following the existing naming
convention: `.yaml` for the three `@startyaml` data diagrams (Exposed/Dependent API, and the two new
Published/Subscribed Events splits), `.puml` for the eTOM–SID diagram when it's small enough to stay
PlantUML, and `.svg` for the API context diagram and (once past the size threshold) the eTOM–SID diagram
too (see why below). Don't inline diagram source directly in the Markdown body — write the source file
first, then reference it.

### Rendering PlantUML sources (four of the five diagrams)

There's no local PlantUML renderer in this environment (no `java`, no `plantuml` CLI/jar), but there is
network access, so render each `.yaml`/`.puml` source via the public PlantUML server and save the PNG next
to its source in `Diagrams/`:

```python
import plantuml, httplib2

h = httplib2.Http()
with open("Diagrams/<ComponentID>_<Diagram>.puml", encoding="utf-8") as f:
    src = f.read()
url = "http://www.plantuml.com/plantuml/img/" + plantuml.deflate_and_encode(src)
resp, content = h.request(url, "GET")
# retry once or twice on non-200 / non-PNG-magic-bytes before giving up — the public server occasionally
# hiccups, and the `plantuml` package's own exception path has a bug that masks the real HTTP error
assert resp.status == 200 and content[:4] == b"\x89PNG"
with open("Diagrams/<ComponentID>_<Diagram>.png", "wb") as f:
    f.write(content)
```

Then embed the rendered image in the Markdown body with a link back to its source, e.g.:

```markdown
![Exposed API diagram](TMFC005_Exposed_API.png)

*(PlantUML source: [TMFC005_Exposed_API.yaml](TMFC005_Exposed_API.yaml))*
```

No `Diagrams/` prefix on either path — the main `.md` lives inside `Diagrams/` itself (see "Where the data
lives" above), so the image/source files are plain siblings, not a subfolder reference.

This sends diagram source (component/API names and structure — no sensitive data) to a third-party public
service; that's an appropriate default for this content since these are published TM Forum standards
documents, but confirm with the user before doing this for anything else. If a local renderer becomes
available later, prefer it — same source files, same output paths, just point at a local server URL
instead of `www.plantuml.com`.

**Check the rendered image before wiring it into the document**, especially for the eTOM–SID diagram — a
naive hub-and-spoke layout with many nodes fans out into an unreadably wide single row. Chain same-category
nodes with hidden edges (`A -[hidden]d- B`) to force them into a vertical stack instead; see
[references/diagrams.md](references/diagrams.md) for a worked example.

**Size threshold: switch the eTOM–SID diagram to SVG once it has more than 6 total elements.** Count
eTOM boxes (after L2 collapsing, see `references/diagrams.md`) plus SID boxes together — once that count
exceeds 6, plain PlantUML `@startuml` rectangle/database layout reliably becomes visually messy (lines
crossing, boxes reordering unpredictably), the same class of layout problem the API context diagram has.
Below the threshold, PlantUML stays fine and is simpler — don't switch pre-emptively. Above it, use
[scripts/render_etom_sid_svg.py](scripts/render_etom_sid_svg.py) instead of `@startuml` (see
[references/diagrams.md](references/diagrams.md) for the worked example — TMFC010's 6 eTOM + 4 SID = 10
elements crosses the threshold).

### Splitting oversized Exposed/Dependent API and Events diagrams

A different size problem from the eTOM–SID one above: `@startyaml` doesn't have a messy-layout failure
mode (it's just a literal nested-list renderer, not a Graphviz layout), but a component with enough APIs
or events simply produces a box too tall to read comfortably on one page — this is a page-fit problem, not
a visual-clarity one. **Once the total operation count (Exposed/Dependent API) or event-name count
(Published/Subscribed Events) across all entries passes 60, split into multiple `@startyaml` files** —
`<ID>_Exposed_API_1.yaml`, `_2.yaml`, ... (same for `Dependant_API`, and independently for each of the
Published/Subscribed Events halves) — each rendered and embedded as its own image, in order, under the
same subsection.

**`sync_diagram_yaml.py` does this automatically for the Exposed/Dependent API files** via
`paginate_entries()`: walk the API list in order, keep a running total of `_operation_count(entry)`, and
start a new page whenever adding the next whole entry would push the current page's total past 60 — never
splitting a single API's own operations across two pages, even if that API alone has more than 60 (it just
gets a page to itself; there's nothing safe to cut it into). Below the threshold this writes the plain
unnumbered `<ID>_Exposed_API.yaml`/`<ID>_Dependant_API.yaml` exactly as before pagination existed — no
behavior change for the common case. `_write_paginated()` also removes any stale numbered (or unnumbered)
file left from a previous run whose page count has since changed, so a diagram that shrinks back under the
threshold doesn't leave an orphaned `_2.yaml`/`_2.png` behind. TMFC003's `Dependant_API` diagram (160
operations total) is a real example, currently split into 3 pages of 56/59/45 — see
[references/diagrams.md](references/diagrams.md) for the worked embedding.

**Events auto-split the same way**, via the same `sync_all()` call (see "Where the data lives" above) —
`_write_paginated()` applies the 60-event-name threshold to `publishedEvents`/`subscribedEvents`
independently, producing `<ID>_Published_Events_1.yaml`/`_2.yaml`/... (or `_Subscribed_Events_...`)
exactly like the Exposed/Dependent API split, with no manual step needed.

When embedding multiple pages, number them in the caption (`Dependent API diagram (1 of 3)`) and say in the
first page's caption that it continues — see the worked `.md` snippet in
[references/diagrams.md](references/diagrams.md). Don't add any other commentary about *why* it's split
(see "Handling YAML/PDF disagreement" above — this kind of explanation belongs in your chat summary, the
"(1 of 3)"/"split across N diagrams" caption text is the one narrow exception since it's necessary for a
reader to understand the document structure, not analysis of the data).

### The API context diagram is different: generated SVG, not PlantUML

This diagram needs each API drawn as a **straight line individually anchored** to its own point on the
component box (dependent APIs down the left edge, exposed APIs down the right edge) — PlantUML/Graphviz's
automatic layout cannot do this; it bundles every same-side edge toward roughly one attachment point on the
box no matter what layout hints are applied (confirmed through several failed attempts: per-edge
`-left-`/`-right-` direction hints, `together{}` grouping, hidden-edge chaining — all either misplaced nodes
or left the lines converging to one spot). So this one diagram is generated directly with exact coordinates
instead of being literal PlantUML source. Use
[scripts/render_api_context_svg.py](scripts/render_api_context_svg.py):

```python
import sys
sys.path.insert(0, "<path to this skill's scripts/ folder>")
from render_api_context_svg import build_svg

svg = build_svg(
    component_id="TMFC005", component_name="Product Inventory",
    dependent_apis=[{"id": "TMF620", "name": "Product Catalog Management API"}, ...],
    exposed_apis=[{"id": "TMF637", "name": "Product Inventory Management API"}, ...],
    etom_entries=["1.2.11\nProduct Inventory Management", ...],   # \n for a second line
    sid_entries=["Product and Offering\nInstance / Product", ...],
)
with open("Diagrams/<ComponentID>_API_Context.svg", "w", encoding="utf-8") as f:
    f.write(svg)
```

Save the `.svg` in `Diagrams/` alongside the others, and embed it directly (`![...](<ID>_API_Context.svg)`,
no `Diagrams/` prefix — see "Where the data lives" above) — SVG renders natively in Markdown viewers, so no
PNG conversion is required for the `.md` itself. The PDF/docx pipelines do each need a raster copy (neither
can rasterize inline `.svg` directly) — call `build_pdf.py`'s `_svg_to_png()` rather than hand-rolling this;
it caches the result in `Diagrams/temp/` (see "`Diagrams/temp/`" under "Also produce a PDF" below), shared
between both scripts so the conversion only happens once per SVG:

```python
from build_pdf import _svg_to_png

png_path = _svg_to_png("Diagrams/<ID>_API_Context.svg")   # -> Diagrams/temp/<ID>_API_Context.png
```

Internally this is `svglib → reportlab → pymupdf` (pure Python, no native cairo dependency — there's no
working `cairosvg`/`rsvg-convert` in this environment either):

```python
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import fitz  # PyMuPDF

drawing = svg2rlg("Diagrams/<ID>_API_Context.svg")
renderPDF.drawToFile(drawing, "_tmp.pdf")          # svglib->reportlab needs a PDF step, not direct-to-PNG
doc = fitz.open("_tmp.pdf")
doc[0].get_pixmap(dpi=150).save("Diagrams/temp/<ID>_API_Context.png")
```

Always look at the rendered result before finalizing — screenshot it (a local `python -m http.server` plus
the Browser pane works if `file://` navigation is blocked) or convert to PNG and view it directly. **Do
this by actually running the `svglib → reportlab → pymupdf` conversion above and viewing that output**, not
just the raw SVG in a browser — `svglib` silently drops SVG `<marker>` elements (used for arrowheads)
entirely, with no error, so a diagram that uses `<marker>` can look perfect in a browser and render with
every arrowhead missing once it goes through this pipeline (discovered building the eTOM–SID SVG variant,
see `references/diagrams.md`). If a diagram needs arrowheads, draw them as explicit filled `<polygon>`
shapes instead of `<marker>` — `render_etom_sid_svg.py`'s `_arrowhead()` is a worked example.

## Write the file

Output to `specifications/<ComponentFolder>/Diagrams/temp/<same base filename as the existing PDF>.md` —
**inside `Diagrams/temp/`, not `Diagrams/` itself.** This corrects an earlier version of this section: the
main `.md`, the three diagram-source files (Exposed/Dependant API, Events), and every diagram image
(`.svg`/`.png`) are all disposable, skill-generated build output now, regenerated from scratch on every run
— only the `.docx`, the Supplement file, the eTOM–SID Links file, and the three Descriptions files stay
directly under `Diagrams/` as the hand-maintained/persistent set. See "`Diagrams/temp/`" under "Also produce
a PDF" below for the full rationale, and call `scripts/build_pdf.reset_temp_dir(diagrams_dir)` **first**,
before generating anything else, so a stale file from a previous run can't survive and get read back as
current. If a version of the `.md` already exists from a previous run, diff against it and summarize what
changed (new/removed eTOM or SID entries, API mandatory/optional flips, new events) in your chat summary —
don't bother preserving the old file itself, since nothing treats it as a source of truth.

## Cover page & Notice (PDF only, generated entirely from YAML)

The PDF's cover page and Notice page are built by `scripts/build_pdf.py` directly from
`componentMetadata` — no original PDF involved, per explicit user instruction. Field mapping (all fixed
rules, not guesses — confirmed against real values in TMFC005/010/012's YAML):

| Cover field | Source |
|---|---|
| Component name / TMFCxxx ID | `componentMetadata.name` (spaced), `.id` |
| Maturity Level | derived from `.status`: `preview` or `production` → `General Availability (GA)`; `roadmap` → `Beta`; `backlog` → `Alpha` |
| Team Approved Date | `componentMetadata.publicationDate`, formatted `DD-Mon-YYYY` |
| Release Status | `componentMetadata.status`, capitalized for display (`production` → `Production`) |
| Approval Status | derived from `.status`: `production` → `TM Forum Approved`; `preview` → `Team Approved`; `roadmap` or `backlog` → `Not yet approved` |
| Version | `componentMetadata.version` verbatim (this is the component's own version, e.g. `1.1.4` — deliberately not the same as the spec-suite branch version like `v1.1.0`) |
| IPR Mode | fixed constant `RAND` — not read from anywhere |
| Copyright year | the year portion of `componentMetadata.publicationDate` |

The Notice page's legal boilerplate text is a **fixed constant** (`NOTICE_TEXT` in `build_pdf.py`) — it's
identical across every TM Forum component document, so there's nothing to derive per component. See
`_maturity_level()` / `_approval_status()` / `NOTICE_TEXT` in [scripts/build_pdf.py](scripts/build_pdf.py)
for the exact implementation.

**Visual design** (logo, color palette, heading capitalization/color hierarchy, cover page layout,
running header/footer) is a separate concern from the field mapping above and is fully specified in
[references/pdf_visual_template.md](references/pdf_visual_template.md) — read that before touching
any of `build_pdf.py`'s CSS, the cover/notice HTML, or `_apply_page_chrome()`. Every value in it
(colors, sizes, positions) was sampled directly from a real published component PDF, not guessed —
don't hand-tune a color or position without checking that file first, and update it (not just the
code) if the source-of-truth reference document ever changes. The TM Forum logo itself is a real
extracted asset at [assets/tmforum_logo.png](assets/tmforum_logo.png), not redrawn — reuse that file
as-is; don't regenerate or approximate the logo from scratch.

## Also produce a PDF, with the diagrams visible

Alongside the `.md` + Supplement `.md`, also render a `.pdf` version that combines both into one document
with the diagrams embedded as images (not just linked), using
[scripts/build_pdf.py](scripts/build_pdf.py):

```python
import sys
sys.path.insert(0, "<path to this skill's scripts/ folder>")
from build_pdf import build_pdf

build_pdf("specifications/<ComponentFolder>/Diagrams/temp/<same base filename as the existing PDF>.md")
```

`yaml_path` and `supplement_path` are both auto-discovered if not passed explicitly: `yaml_path` by globbing
for the one `*.yaml` file in the **component root, two directories up from the main `.md`** (since the
`.md` now lives in `Diagrams/temp/`, not `Diagrams/` — one level up from the `.md` lands in `Diagrams/`
itself, full of unrelated diagram-source `.yaml` files and the hand-maintained `.md`s, so the search has to
go up a second level to reach the component root and find the single main component YAML), `supplement_path`
by appending `_Supplement.md` to the main `.md`'s base name **in `Diagrams/`** (one level up from the `.md`
itself, since the Supplement stays hand-maintained and never moved into `temp/`). `build_pdf()` raises
immediately if the Supplement file doesn't exist yet (with a message pointing at the template) rather than
silently producing an incomplete PDF.

This is pure-Python (`markdown` + `xhtml2pdf`, same pairing the sibling `component-conformance-profile`
skill already uses, no `pandoc`/`wkhtmltopdf` needed, plus `pyyaml` for reading `componentMetadata`). On
top of the base conversion, `build_pdf.py` does five things this document specifically needs:

1. **SVG → PNG for the PDF pass only.** `xhtml2pdf` can't rasterize `.svg` directly, so it rewrites `.svg`
   image references to their sibling `.png` (generating that PNG first via the `svglib → reportlab →
   pymupdf` pipeline above if it doesn't already exist) before conversion. The `.md` file itself keeps its
   `.svg` references untouched for viewers that render SVG natively.
2. **Every table's column widths are optimized, content-proportionally.** `xhtml2pdf`'s own automatic
   table-column-width algorithm is unreliable — confirmed on two real tables (2.2 SID ABEs, 6.1.1 Version
   History) where it collapsed a column to near-zero width and the text overlapped the next column or ran
   off the page edge. Neither `table-layout: fixed` nor `<colgroup>` fixes this (both are silently ignored)
   — the only thing that works is an explicit `width:%` inline style on every `<th>`/`<td>`. `build_pdf.py`
   computes this from each column's actual content length (capped, with a floor so no column starves) and
   injects it into every table in the document automatically — don't hand-tune widths per table.
3. **Cover, Notice, and a fresh table of contents are generated, not copied from anywhere.** See "Cover
   page & Notice" above for the cover/notice fields. The ToC is built from this document's own actual
   `##`/`###`/`####` heading structure (across the concatenated main `.md` + Supplement content) — not
   copied from any prior document, since section numbering can legitimately differ (this document adds a
   3.1 API Context Diagram subsection an old PDF never had). Page numbers are computed by rendering the
   body once, locating each heading via `page.search_for()`, then rendering the cover+notice and the ToC to
   find out how many pages each actually takes and folding that back into the offset (a short fixed-point
   loop — the ToC's own size affects where the body starts, which is why this can't be computed in one
   pass). The ToC ends up as a plain two-column table with a dotted-underline leader — a plain CSS
   `float: right` looked right in isolation but xhtml2pdf's `float` support doesn't actually push the
   element to the margin, it left the page number glued next to the heading text, so don't use that
   approach here again.
4. **Main `.md` + Supplement `.md` are concatenated before rendering.** The two files stay physically
   separate on disk (see "Supplement file" above) — `build_pdf.py` just joins their text in memory for this
   one rendering pass so the final PDF reads as one continuous document, with 5.1 (main `.md`) flowing
   directly into 5.2 (Supplement) with no visible seam.
5. **The TM Forum logo, running title, and footer are stamped on afterward, in one pass over the
   fully merged PDF** (`_apply_page_chrome()`), not baked into any of the three individual xhtml2pdf
   renders. See [references/pdf_visual_template.md](references/pdf_visual_template.md) for the full
   visual spec this implements and why the "stamp after merging" ordering matters (in short:
   cover+notice, ToC, and body are three separately-paginated renders merged together afterward, so
   only a post-merge pass can know the true final "Page N of M").

**Naming/overwrite behavior**: `build_pdf()`'s default `out_path` (when not passed explicitly) writes
straight to the component root, sharing the main `.md`'s base filename — **directly overwriting the
officially-published `TMFCxxx_<Name>.pdf`.** This is the PDF's *only* destination; per explicit user
instruction, it does not stop in `Diagrams/` or `Diagrams/temp/` along the way, and there is no separate
copy-to-root step to perform afterward — `build_pdf()` already wrote there. This is standard practice for
this skill, not a one-off — confirmed repeatedly across many components in one session (individually at
first, then via a direct standing instruction to do it by default going forward) rather than something to
re-ask permission for on every run. Do still confirm with the user before writing anything into the real
repo at all if this is the *first* time running the skill for a repo/user that hasn't established this
pattern — the "just overwrite root by default" behavior applies once a user has confirmed it for their
repo, not as a blanket default for every user of this skill.

**`Diagrams/temp/`: where every non-hand-maintained asset this skill generates now lives, including the main
`.md` itself.** This is a correction to an earlier version of this section, which under-scoped `temp/` to
only three narrow caching concerns — the actual, current behavior (see `reset_temp_dir()` in
[scripts/build_pdf.py](scripts/build_pdf.py), and `_find_component_yaml()`/`build_pdf()`/
`build_docx_scroll()`'s shared `md_path` → `Diagrams/temp/` → `Diagrams/` → component-root path-climbing
logic, which only works if the `.md` actually lives there) is broader: **everything this skill produces
that isn't hand-maintained goes in `temp/`**, wiped and recreated fresh at the start of every full
regeneration via `reset_temp_dir(diagrams_dir)` — never trusted as a carry-over cache, so a stale leftover
from an interrupted or superseded run can't silently survive:
- The main `.md` itself.
- The three diagram-source files (`<ID>_Exposed_API.yaml`, `<ID>_Dependant_API.yaml`, `<ID>_Events.yaml`,
  plus any paginated `_1.yaml`/`_2.yaml`/... variants) written by `sync_diagram_yaml.py`'s `sync_all()`.
- Every diagram image: the API context SVG, the Exposed/Dependent/Events PlantUML-rendered PNGs, the
  eTOM–SID diagram (`.puml` or `.svg` depending on the size threshold) and its rendered image, and the
  SVG→PNG rasterization cache (`_svg_to_png()`) both the PDF and docx pipelines share.
- `build_pdf()`'s three mid-assembly render passes (`_body_tmp.pdf`, `_front_tmp.pdf`, `_toc_tmp.pdf`).
- `build_docx.py`'s (superseded, reference-only) JSON payload handoff to `build_docx.js`.

Only four things stay directly under `Diagrams/` itself, never touched by a regeneration: the **`.docx`**
(the one real deliverable that lives there — see below) and the three/four **hand-maintained** files —
Supplement, eTOM–SID Links, and the eTOM/SID/FF Descriptions files. The two real deliverables overall stay
exactly what they were before `temp/` existed: the PDF at the component root, and the `.docx` in `Diagrams/`
itself — `temp/` doesn't change either of those, it just means the main `.md` and every diagram are now
intermediate build state feeding those two outputs, not standalone checked-in artifacts in their own right.
Add `Diagrams/temp/` to the repo's `.gitignore` if it isn't already there, so a regeneration doesn't dump
dozens of disposable files into every `git status`.

## Also produce a Word document (.docx)

Alongside the `.md` + Supplement `.md` + PDF, also generate a `.docx` export from the same source content
(main `.md` through 5.1, concatenated with the Supplement file for 5.2 onward), using
[scripts/build_docx_scroll.py](scripts/build_docx_scroll.py):

```python
import sys
sys.path.insert(0, "<path to this skill's scripts/ folder>")
from build_docx_scroll import build_docx_scroll

build_docx_scroll("specifications/<ComponentFolder>/Diagrams/<base filename>.md")
```

**The `.docx` must match the Confluence/Scroll export format TM Forum actually publishes** — not a
look invented here. That format's identity lives in its *styles* (`Title`, `Subline Header`,
`SublineHeader Level2`, auto-numbered `Heading 1-3`, `Scroll Table Normal`, `Scroll Panel`) and in the
numbering definitions those Heading styles point at, so `build_docx_scroll.py` **templates from a real
export** rather than re-declaring any of it: it opens
[assets/scroll_export_template.docx](assets/scroll_export_template.docx), strips the body, and appends
generated content using the template's own styles. Everything visual then matches by construction.

Five things this implies, each of which was a real bug before it was handled:
- **Clear `w:sdt` as well as `w:p`/`w:tbl`.** Word wraps a table-of-contents field in a structured
  document tag, so clearing only paragraphs and tables leaves the *template's* ToC at the top of the
  generated document.
- **Strip the leading section number from every heading.** The template's Heading styles auto-number, so
  emitting `1. Overview` renders as `1. 1. Overview`. The shared `.md` keeps literal numbers because the
  PDF needs them; only this script strips them.
- **Shift heading levels down one.** Markdown `##` is a top-level numbered section, which the export
  styles as `Heading 1` (its "Overview" is Heading 1, not Heading 2). The `#` document title is emitted
  separately with the `Title` style.
- **Force `outlineLvl` 9 on the Title and Subline paragraphs.** Those styles carry an outline level, so a
  `TOC \o "1-3"` field otherwise lists the document title and subtitle as if they were sections.
- **Override `tblLook` to enable only `firstRow`.** `Scroll Table Normal` also defines a *first column*
  format (bold, coloured) that Word applies by default, which makes the leading data cell of every table
  look like a heading.

Deliberate differences from the reference export, all by explicit user decision — don't "fix" them back:
- **No cover table and no Notice page in the `.docx`.** The PDF is the published artifact and keeps that
  furniture; the `.docx` mirrors the export, which has neither.
- **A `Version` column is kept on the 3.x API tables.** The export has none and therefore cannot show
  that TMF701 exposes `processFlow`/`taskFlow` at v4 but `process`/`task` at v5 — it silently shows only
  v4.
- **The Events section keeps two diagrams and two tables.** The export has a single combined diagram and
  no tables, which drops every event name from the document.
- The export's "Exported on `<timestamp>`" line is **not** reproduced: it is an export artifact, and a
  changing timestamp would make every regeneration show as a diff.

`yaml_path` and `supplement_path` auto-discover the same way `build_pdf()`'s do (see "Also produce a PDF"
above). Note `_find_component_yaml()` takes the `.md`'s **directory**, not its path — passing the file
makes it glob `Diagrams/` and fail on the diagram-source `.yaml` files.

[scripts/build_docx.py](scripts/build_docx.py) + [scripts/build_docx.js](scripts/build_docx.js) are the
superseded docx-js implementation, kept only for reference; `build_docx_scroll.py` reuses its Markdown
block parser (`_parse_blocks`) and needs no Node.js.

**Why a native Word table of contents rather than the PDF's page-computation dance**: `build_pdf.py` has to
render the body once, locate every heading by searching rendered pages, then fold that back into a ToC
render in a fixed-point loop — all because xhtml2pdf's three separately-paginated render passes (cover+
notice, ToC, body) have no shared page-numbering context until merged. Word doesn't have that problem: the
`.docx` uses a real `TableOfContents` field (`headingStyleRange: "1-3"`, built from the document's own
Heading1–3 styles) that Word computes and keeps up to date itself whenever the document is opened or
printed — no manual page-location code needed on this side at all. The doc's own H1 title deliberately
does *not* use a Heading style (same as `build_pdf.py`'s `_extract_headings` skipping the H1) so it doesn't
show up as a spurious ToC entry.

**Markdown parsing is deliberately narrow, not a general CommonMark parser**: `build_docx.py`'s
`_parse_blocks` only understands the specific subset this skill's own `.md`/Supplement generation actually
produces — headings (`#`-`####`), pipe tables, image lines (optionally followed by an italic caption
paragraph), bullet lists (including a `"  - "` nested level and plain-text continuation lines), and inline
`**bold**`/`` `code` ``. If the Supplement file (hand-edited by a person) ever grows Markdown outside that
subset — nested numbered lists, blockquotes, inline links meant to stay clickable — extend the parser
rather than assuming it degrades gracefully; right now it flattens anything it doesn't recognize into a
plain paragraph, and markdown links are deliberately flattened to their display text everywhere (relative
paths to diagram source files aren't meaningful as Word hyperlinks).

**Table column widths** use the same content-proportional weighting `build_pdf.py` computes for xhtml2pdf
(a column's width scales with the longest cell text it holds, capped and floored) — computed once in
`build_docx.py` and passed through as a `colWidthsPct` list per table, rather than re-implemented in
JavaScript.

**Diagrams**: SVG sources (the API context diagram, and the eTOM–SID diagram once past the size threshold)
are converted to PNG via the same `_svg_to_png` helper `build_pdf.py` uses — imported directly, not
duplicated — so both exports share one cached PNG per SVG rather than rendering it twice.

**No "publish to component root" step for the `.docx`** — see "Where the data lives" above. It stays in
`Diagrams/` as a working artifact; there's no pre-existing official `.docx` per component the way there is
a PDF, so there's nothing to overwrite. Don't add a copy-to-root step unless a component's official spec
starts being published as `.docx` too.

**Verifying a generated `.docx`**: there's no LibreOffice on this machine, so the `docx` skill's usual
`soffice.py --convert-to pdf` verification path doesn't work here. Use Word itself via COM automation
instead — open the file, force a field update (so the ToC page numbers are current), export to PDF, then
render that PDF's pages to PNG and look at them:

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open($docxPath)
$doc.Fields.Update()
$doc.Repaginate()
$doc.SaveAs([ref]$pdfPath, [ref]17)   # 17 = wdFormatPDF
$doc.Close([ref]0)
$word.Quit()
```

then `fitz.open(pdfPath)` + `page.get_pixmap(dpi=110).save(...)` per page, same as reviewing any other
generated PDF in this skill.

## After generating

Summarize in plain terms: what changed relative to any previous version of the main `.md` (new/removed
eTOM or SID entries, API mandatory/optional flips, new events, etc.), confirm whether the Supplement
file already existed (untouched) or had to be created fresh this run (from an old PDF's chapters 5.2/5.3/6,
or from the template if there was no prior PDF), confirm the root PDF was overwritten with the freshly
built one (per "Naming/overwrite behavior" above), and confirm the `.docx` was (re)generated in `Diagrams/`.
