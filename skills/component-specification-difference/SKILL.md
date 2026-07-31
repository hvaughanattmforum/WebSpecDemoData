---
name: component-specification-difference
description: >
  Compare two versions of a TM Forum ODA component specification PDF (TMFCnnn) and write a
  section-by-section change report as Diagrams/TMFCnnn_<Name>_v<old>_vs_v<new>_difference.md. Use this
  whenever the user asks what changed between two versions of a component specification, wants a diff /
  difference / comparison / changelog / "what's new" for a TMFCnnn component, mentions a _difference.md
  file, or has just regenerated a component document and wants to see how it differs from the published
  one. Trigger it even when the user says "compare", "diff" or "what changed" without naming a file
  format, and proactively offer it right after a component's specification PDF has been regenerated,
  since a reviewer approving the new version needs to see the delta rather than read 40 pages twice.
---

# Component specification version difference

## What this produces

One Markdown file per comparison, written next to the component's other generated documents:

```
specifications/<ComponentFolder>/Diagrams/TMFCnnn_<Name>_v<old>_vs_v<new>_difference.md
```

Both versions appear in the filename so several comparisons can coexist (v1.1.1 vs v2.0.0 alongside
v2.0.0 vs v3.1.0) without overwriting each other.

The report is a **semantic** comparison, not a text diff. Entries are matched on their own identifiers —
eTOM activity id, Functional Framework function id, SID ABE names, TMF API id, event name — so that
re-pagination, reworded prose and re-laid-out tables don't masquerade as changes. A raw text diff of two
of these documents is almost pure noise; a reviewer needs "these 14 eTOM activities were dropped", not
"line 812 rewrapped".

## How to run it

Two PDFs, or point it at the component folder and let it find them:

```bash
python scripts/build_difference.py --component-dir specifications/TMFC003-ProductOrderDeliveryOrchestrationAndManagement
python scripts/build_difference.py old.pdf new.pdf [--out path.md]
```

`--component-dir` collects every versioned PDF at the component root and under `Diagrams/`, then compares
the lowest version against the highest. Which is old and which is new is decided by version number, not
by argument order or filename — passing them the wrong way round still produces the right report.

To inspect what was extracted from a single document before comparing (useful when a section looks wrong):

```bash
python scripts/extract_spec_pdf.py <spec.pdf> [--json out.json]
```

## Structure of the report

Follow this shape. It front-loads the summary because the first question a reviewer asks is "how much
changed, and where", and only then "what exactly".

```markdown
# TMFCnnn – <Component Name>
## Specification differences: v<old> → v<new>
<table: version, source file, pages, and any cover fields that differ — release status, maturity,
 approval status, team approved date>
## Summary of changes
<table: section | added | removed | changed>
## 1. Overview
## 2.1 eTOM business activities
## 2.2 SID ABEs
## 2.4 Functional Framework Functions
## 3 Exposed APIs
## 3 Dependent APIs
## 3 Events
## 5.1 TMF Standards related versions
## Extraction caveats
```

Section headings carry no version numbers of their own, because the two documents may number the same
content differently — one generation puts the API context diagram in its own 3.1 subsection and numbers
Exposed APIs 3.2, another has no such subsection. The report names the content, not the numbering.

## The two rules that make this trustworthy

A comparison that cries wolf is worse than none, because every false finding costs a reviewer real time
to chase down and erodes their trust in the true ones. Two rules do most of that work, and both are
implemented in `build_difference.py`:

**1. Count entries as added when the prior document didn't have them — and say on what basis.** Where the
old document had nothing, the new document's entries are additions and the summary carries a number, not a
shrug. But distinguish the two ways "nothing" arises, because they support different claims:

- The old document **asserts absence** — its 2.2 table states the single word "none". Everything the new
  document lists is unambiguously new; report it as Added and cite the "none".
- The old document **simply didn't tabulate it** — its Events section is a diagram with no table. Still
  report the new entries as Added, since they weren't in the prior document's content, but note that the
  additions are relative to what that document tabulated and that its diagram may have depicted events.
  This is not evidence that none existed.

What to avoid is the unqualified claim in the second case: presenting 82 events as added while implying the
old component published none would misrepresent the older document.

**2. Only claim a change where both documents state a value.** A blank on one side means that document
didn't record the field — not that it changed. The older layout has no Version column at all, so
comparing versions naively reported all nine retained dependent APIs as `blank → 4, 5`: nine fabricated
findings. Per standing user instruction, **an API in a document with no Version column is taken to be
version 4**, and the report says so explicitly rather than letting an assumption read as an extracted
fact.

## What can and cannot be extracted reliably

Reliable, and compared in full: cover metadata, the 2.1 eTOM table, 2.2 SID ABEs, 2.4 Functional
Framework functions, 5.1 standards versions, and API presence / name / mandatory-optional / versions.

Not reliable, and deliberately not diffed row by row: **per-resource and per-operation API detail**. When
`find_tables()` mis-places a column boundary, pymupdf interleaves the two neighbouring cells' characters
by x position — `productOfferingPrice` and `GET` come back as `productOfferingP` + `ricGeET` — and that is
not recoverable afterwards. The extractor flags such rows (`resource_confident: false`) and the report
states how many were affected instead of reporting a truncated name as a change.

Before adjusting the extractor, read [references/pdf_extraction.md](references/pdf_extraction.md). It
records the failure modes these documents actually exhibit and, importantly, one approach that looked
right and made things worse — worth knowing before spending an hour rediscovering it.

## After generating

Say in the chat summary what the headline changes are and, separately, what the report could not
establish. The caveats section exists so the document is honest on its own, but a reviewer reading your
message shouldn't have to scroll to the bottom to learn that resource-level detail wasn't compared.

Sanity-check at least the counts before handing it over: the arithmetic should close. If the old document
had 22 Functional Framework functions and the new one has 41, then `retained + added` must equal 41 and
`retained + removed` must equal 22. When that doesn't add up, the extraction lost rows and the report is
understating or overstating something — investigate rather than shipping it.
