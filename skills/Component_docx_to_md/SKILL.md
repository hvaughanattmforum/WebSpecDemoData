---
name: Component_docx_to_md
description: Convert a .docx (Word) file to Markdown when neither pandoc nor python-docx is available on the machine. Use this whenever a docx-to-markdown conversion is needed and the normal tools (pandoc, python-docx) turn out to be missing and can't be installed (no network/pip access, locked-down machine, etc.) - check for pandoc and python-docx first, and only reach for this skill once you've confirmed neither is usable. Bundles a self-contained Python script that parses the docx's internal XML directly with only the standard library, and captures hard-won gotchas (silently-dropped cover pages/TOCs, silently-dropped hyperlink text, bold-run splitting artifacts) that a naive from-scratch XML parse would rediscover the hard way.
---

# DOCX to Markdown without pandoc or python-docx

A `.docx` file is a ZIP archive of XML files. When `pandoc` and `python-docx`
are both unavailable (offline machine, no pip access, locked-down
environment), you can still get a faithful Markdown conversion - text,
tables, images, and hyperlinks - by parsing `word/document.xml` directly
with the standard library (`zipfile`, `xml.etree.ElementTree`).

**Before using this skill**, actually check for the normal tools - they're
far less work when available:

```bash
pandoc --version
python -c "import docx"   # python-docx
```

If either works, use it instead (`pandoc -t gfm --extract-media=./media file.docx -o file.md`,
or python-docx directly). Only fall back to this skill's script when both
are confirmed missing.

## Usage

```bash
python scripts/docx_to_md.py <input.docx> <output.md>
```

This writes `<output.md>` and a sibling `<output-stem>_media/` folder
containing every image actually referenced in the document, with Markdown
image links (`![](<output-stem>_media/imageN.png)`) inserted at their
original position in the text flow.

After running it, **read the output file** and skim it for the failure
modes below before handing it to the user - the script is a solid default
but not infallible on documents with unusual structure.

## Why a naive XML walk isn't enough

The obvious approach - walk `word/document.xml`'s `<w:body>` for `<w:p>`
(paragraph) and `<w:tbl>` (table) elements, and each paragraph's direct
`<w:r>` (run) children for text - silently drops a surprising amount of
real, visible content. This script's structure exists specifically to avoid
that. If you're extending or rewriting it, preserve these three things:

1. **Cover pages and auto-generated Tables of Contents are wrapped in
   `<w:sdt>`** (structured document tags / content controls). These are
   direct children of `<w:body>`, not paragraphs or tables themselves, so a
   walk that only matches `<w:p>`/`<w:tbl>` at the top level skips their
   entire contents - the document's title, subtitle, and whole TOC just
   vanish with no error. Recurse into `<w:sdt>/<w:sdtContent>` and treat its
   children as if they were direct children of the body. `<w:ins>`/`<w:del>`
   (tracked-change-wrapped blocks) need the same treatment.

2. **Runs are constantly wrapped in `<w:hyperlink>`, `<w:ins>`, `<w:del>`,
   or `<w:smartTag>`** - every TOC entry (wrapped in a hyperlink to the
   bookmark), every `@mention`, every pasted link. Searching a paragraph for
   direct-child `<w:r>` elements only (`p.findall('w:r')`) misses all of
   these - the paragraph looks empty or truncated even though Word renders
   visible text. Recurse through those wrapper tags to find the runs inside
   them. While you're in there, resolve `<w:hyperlink r:id="...">` against
   `word/_rels/document.xml.rels` to get the actual URL and emit a real
   Markdown link instead of plain text - the relationship ID is meaningless
   without it, and the visible text alone was already the main goal.

3. **Word splits one visually-continuous bold or italic phrase across many
   `<w:r>` runs** (revision-ID and spell-check boundaries fragment runs
   even when formatting doesn't change). Wrapping each run's text in `**`
   independently produces `**foo****bar**` instead of `**foobar**`. Collect
   `(text, bold, italic, link_url)` segments first, merge adjacent segments
   that share the same formatting state, *then* wrap in Markdown markers.

## Known limitations

- **Numbered/bulleted list formatting isn't reproduced.** Paragraphs using
  Word's list numbering (`<w:numPr>`) come through as plain paragraphs, not
  `-`/`1.` Markdown list items - the text is preserved but the list
  structure isn't. If a document leans heavily on lists, either accept the
  flattened result (usually fine for read-through content extraction) or
  extend `paragraph_style`/the render loop to check for `<w:numPr>` and
  render list markers.
- **Nested tables** (a table inside a table cell) aren't specially handled;
  their paragraphs get flattened into the containing cell's text via
  `cell_text`'s `<br>`-joining rather than rendered as a nested table. Rare
  in practice.
- **Internal cross-references** (TOC entries linking to a heading elsewhere
  in the same doc, via `<w:anchor>` instead of `r:id`) render as plain text,
  not a Markdown anchor link - there's no external URL to point at, and
  Markdown anchor links aren't reliable across renderers anyway.
- Table rendering always treats the first row as the header row, matching
  pandoc's default behavior - reasonable for the vast majority of Word
  tables, which do use their first row as a header.

If a document trips one of these in a way that matters for the task at
hand, fix it forward in a copy of the script rather than the shipped one
unless the fix is clearly general-purpose (e.g. list rendering would
benefit every future use of this skill; a one-off document quirk wouldn't).
