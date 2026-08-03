# TMFC000 – Component Document Templates

Blank templates for the seven markdown document types found in this `Markdowns` directory. Copy the folder,
rename `TMFC000` to the real component ID and `Component_Name` / `ComponentName` to the real name, then
replace every `<...>` placeholder.

## Templates

| Template | Real-world name pattern | Count in `Markdowns\` |
|---|---|---|
| `TMFC000_Component_Name.md` | `TMFCxxx_<Component_Name>.md` | 35 |
| `TMFC000_Component_Name_Supplement.md` | `TMFCxxx_<Component_Name>_Supplement.md` | 35 |
| `TMFC000-ComponentName_Conformance.md` | `TMFCxxx-<ComponentName>_Conformance.md` | 33 |
| `TMFC000_eTOM_Descriptions.md` | `TMFCxxx_eTOM_Descriptions.md` | 15 |
| `TMFC000_FF_Descriptions.md` | `TMFCxxx_FF_Descriptions.md` | 15 |
| `TMFC000_SID_Descriptions.md` | `TMFCxxx_SID_Descriptions.md` | 1 |
| `TMFC000_eTOM_SID_Links.md` | `TMFCxxx_eTOM_SID_Links.md` | 30 |

## Conventions carried over from the real documents

- **Placeholders** are `<angle brackets>`. Where a cell takes one of a fixed set of values, the options are
  separated by `\|`, e.g. `<Mandatory \| Optional>`.
- **Naming.** The main spec and its supplement use underscored title case
  (`TMFC001_Product_Catalog_Management.md`); the conformance profile uses the hyphenated concatenated form
  (`TMFC001-ProductCatalogManagement_Conformance.md`).
- **Titles** use an en dash: `# TMFC001 – Product Catalog Management`.
- **Missing values** in the main spec's tables are written `*(no description available)*`, not left blank.
  A genuinely empty SID ABE Level 2 cell *is* left blank.
- **Multi-paragraph source text** collapsed into a single table cell is joined with ` / `.
- **Escaped pipes.** Literal `|` inside a table cell (the YAML key columns of the links files) must be
  written `\|`.
- **Images** are referenced as bare sibling filenames (`![...](TMFC001_API_Context.svg)`), each followed by
  an italic source note naming the `.svg`/`.yaml` it came from. Keep image files in the same folder as the
  `.md` that references them.
- **`.svg` vs `.png`.** Hand-drawn SVG is used where PlantUML's automatic layout falls short — the eTOM/SID
  diagram past roughly six elements, and the API context diagram in every case. Everything else is PlantUML
  PNG with a `.yaml` source.
- **Section numbering** is shared between the main spec and the supplement: the main spec ends at 5.1, and
  the supplement resumes at 5.2 and runs through section 6. They are two halves of one document.

## How closely each template matches the set

Measured by comparing every template against every real file of its type, ignoring the H1 title line
(component-specific by design). "Headings" is an exact match on the full heading list; "tables" is an exact
match on every table's column headers.

| Template | Headings | Tables |
|---|---|---|
| `TMFC000_eTOM_SID_Links.md` | 30 / 30 | 30 / 30 |
| `TMFC000_SID_Descriptions.md` | 1 / 1 | 1 / 1 |
| `TMFC000_Component_Name.md` | 35 / 35 | 11 / 35 — see below |
| `TMFC000_eTOM_Descriptions.md` | 15 / 15 | 15 / 15 |
| `TMFC000_FF_Descriptions.md` | 15 / 15 | 15 / 15 |
| `TMFC000-ComponentName_Conformance.md` | 33 / 33 | 33 / 33 (the type carries no tables) |
| `TMFC000_Component_Name_Supplement.md` | 35 / 35 | 35 / 35 |

## Notes on variation in the source set

- The **main spec** section structure is identical across all 35 files (sections 1–5), so the template's
  headings describe the set exactly. Its *tables* do not: sections 2.1 and 2.4 come in three widths, and the
  template shows the widest. 11 specs use the wide form (eTOM with a Description column, FF with Description
  + Aggregate Function L1/L2). 14 use a narrow form (eTOM 3 columns, FF 2 columns). 10 have no table at all,
  just `*(none listed in the component YAML)*`. Section 2.2 is present in
  31 and replaced by that same line in 4. The template records all three forms inline as comments. The other
  six tables (Overview, Exposed APIs, Dependent APIs, both Events tables, Standards versions) are identical
  in all 35 — including the column order, which differs deliberately between Exposed
  (`Mandatory / Optional` then `API Version`) and Dependent (`API Version` then `Mandatory / Optional`).
- **Widening a narrow spec** is only worth doing where the description files hold real prose. Check before
  converting: in some files the `Description` column merely repeats the name, with an Alignment Note reading
  "Added to description because present in YAML" — those rows exist to record a YAML entry, not to carry
  description text, and widening against them just duplicates the Name column. TMFC046 is the example (2 of 2
  eTOM rows and 13 of 14 FF rows are name-only), and it was deliberately left narrow for that reason.
  TMFC002 was widened because its description files carry genuine prose in every row; 8 of its 25 Functional
  Framework rows had no matching description entry and so read `*(no description available)*`, which is the
  convention the other wide specs already use.
- The **conformance profile** now matches in all 33 files. Nine (TMFC002, TMFC006, TMFC007, TMFC008,
  TMFC012, TMFC023, TMFC029, TMFC036, TMFC043) were rebuilt to this shape: their API data was carried over
  unchanged, and the `Canvas Conformance` / `Configuration Conformance` boilerplate was copied verbatim from
  an existing profile — that block is byte-identical across all 33, so treat it as fixed text and never
  retype it. Two things to know about those nine: each had declared **TMF672 mandatory**, which the canonical
  rule reverses (TMF672 under `securityFunction` is ignored for conformance, leaving TMF669 as the sole
  mandatory security API); and none had a CTK block, so their `releaseName` / `productName` were derived from
  the convention the other profiles follow (component initials + `-1`; `REFERENCE EXAMPLE <NAME>`) and are
  worth confirming against the real CTK release names.
- The **supplement** was the most fragmented type — 35 files across **22 distinct heading structures** — and
  has been normalised so all 35 now share the single skeleton above. The conversion was lossless: every line
  of body text from every file survives, verified line by line. What changed:
  - Per-framework Jira headings became **bold labels** inside 5.2, preserving order and content. 17 files
    had them, variously as `#### 5.2.1. eTOM`, unnumbered `#### eTOM`, or promoted to their own `5.2`–`5.6`.
    An empty framework block is written `*(none currently listed)*`.
  - Acknowledgements moved from `#### 6.1.3.` to `### 6.2.` in 5 files.
  - 8 files had no Jira section; they now carry 5.2 with the standard
    "No open Jira issues currently listed for this component." line.
  - 3 files had no Further resources section; they now carry 5.3 with `*(none currently listed)*`. Nothing
    was asserted about those components that their source did not say.
  - Column 2 of the Version History table is `Date` in all 35. TMFC010 and TMFC012 previously headed it
    `Date Modified`, which was inconsistent both with the other 33 and with their own Release History table
    (that one is `Date Modified` in all 35, and was left as is). Only the two header cells changed; no row
    data was touched.

  The 35 supplements now share one heading signature and one table signature — the type is fully uniform.
  When reconciling two versions of the same supplement, content wins over numbering.
- The **description files** now match on both headings and columns. Two historical notes: TMFC003 and TMFC014
  had eTOM and FF files containing a header row and no data, and those four stubs were deleted rather than
  left to read as though the content had been transcribed; and TMFC002 used its own
  `ID | Name | Description | Source` scheme, since converted — its `Name` column became `Document Name`, and
  its uniform `Source` value (`v2.1.1 PDF`, already stated in the file's header line) was replaced by the
  template's `Version` and `Alignment Notes`. Because the source document recorded no per-row framework
  release and made no YAML comparison, `Version` carries the eTOM / Functional Framework release declared in
  TMFC002's own specification section 5.1 (v23.0 for both) and `Alignment Notes` reads
  `*(not assessed)*` — neither value is asserted beyond what the sources support. A note at the top of each
  file records this. `TMFC002_SID_Descriptions.md` keeps its `Source` column: it is the only file of its
  type, and the SID template was derived from it.
- The **eTOM_SID_Links** template matches all 30.
- **Legitimately empty tables** should still carry the template's table, with prose above it saying why it is
  empty. `TMFC035_eTOM_Descriptions.md` and `TMFC035_eTOM_SID_Links.md` are the worked examples: that
  component has no eTOM business activities at all (`componentMetadata.eTOMs` is `[]`), so both files explain
  that and then present the standard header row with no data. This keeps the file structurally identical to
  its peers without implying the content was simply never filled in — which is the failure mode described
  next.
- **Coverage gaps.** Not every component has every document type: 35 main specs and supplements against 33
  conformance profiles and 30 eTOM/SID links files, and only 15 each of the eTOM and FF description files.
  `SID_Descriptions` exists for TMFC002 alone.
- **Empty tables.** A file whose table has a header row and no data rows is ambiguous — it reads as
  transcribed-and-empty when it usually means never-transcribed. `TMFC003_eTOM_SID_Links.md` is currently in
  that state (113 B, header only). Prefer either real rows, or prose explaining why there are none, as
  `TMFC035_eTOM_SID_Links.md` does.
