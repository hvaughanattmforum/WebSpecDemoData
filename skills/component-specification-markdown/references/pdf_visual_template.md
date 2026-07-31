# PDF visual template

The look of every generated PDF — logo, colors, heading styles, cover page layout — is sampled
directly from a real, currently-published TM Forum component PDF
(`TMFC001 Product Catalog Management v2.2.2.pdf`, from the user's
`OneDrive - TM Forum\ODA Component and Canvas\ODA Components\20260716 Completed Component Docs\`
folder), not guessed or eyeballed from a screenshot. Every color/size/position value below was
extracted from that PDF's actual embedded image and text span data via PyMuPDF (`page.get_images()`,
`page.get_text("dict")` span `color`/`size`/`font`, `page.get_links()`), then implemented in
[scripts/build_pdf.py](../scripts/build_pdf.py). If the template ever needs re-deriving (a rebrand,
a new reference document), redo it the same way — sample the real thing, don't re-guess.

## Logo

The exact logo image is extracted (not redrawn) from the reference PDF's embedded XObject and saved
at [assets/tmforum_logo.png](../assets/tmforum_logo.png) — a transparent-background PNG, aspect
ratio 243:204 (≈1.196:1).

**Extraction gotcha**: the naive approach — `fitz.Pixmap(doc, xref); pix.save(path)` — silently
produces an opaque image with the correct alpha *flag* but garbage (all-black) RGB where the logo
should be transparent. This PDF stores the logo's transparency as a separate soft-mask (SMask)
XObject, not baked into the base image; `Pixmap(doc, xref)` only reads the base image and fills in
a bogus opaque alpha. The fix is to extract both and combine them explicitly:

```python
import fitz
doc = fitz.open(pdf_path)
base = fitz.Pixmap(doc, base_xref)
if base.alpha:
    base = fitz.Pixmap(base, 0)          # drop the bogus alpha PyMuPDF added
smask = fitz.Pixmap(doc, smask_xref)     # the separate soft-mask XObject, grayscale
combined = fitz.Pixmap(base, smask)      # Pixmap(src, mask) applies mask's gray values as alpha
combined.save(out_path)
```

Find `smask_xref` via `doc.extract_image(base_xref)["smask"]` (0 if there's no separate mask, in
which case the naive approach is fine). Confirm success by checking a known-transparent corner
pixel is `(0, 0, 0, 0)`, not `(0, 0, 0, 255)`.

**Placement** (same on every page, including the cover): top-right corner, `70×58.5pt`
(preserving the ~1.196:1 aspect ratio), `60pt` from the right edge, `15pt` from the top. See
`LOGO_W`/`LOGO_H`/`LOGO_MARGIN_RIGHT`/`LOGO_MARGIN_TOP` in `build_pdf.py`.

## Color palette

| Name | Hex | Used for |
|---|---|---|
| TM Forum red | `#C00000` | "TM Forum Component" cover kicker; chapter headings (`##`, e.g. "2. eTOM..."); "Notice"/"Table of Contents" headings; sub-section headings two levels deep (`####`, e.g. "5.2.1 Functional Framework") |
| Dark gray | `#404040` | Cover page title, `TMFCxxx` id, and all cover metadata table text |
| Table header gray | `#EFEFEF` | Background of every table's header row (`<th>`) |
| Black | `#000000` | Body text; section headings one level deep (`###`, e.g. "2.1 eTOM business activities") |

Sampled by cropping small regions of a rendered page and taking the most common non-white pixel
(`PIL.Image` + `collections.Counter`), then cross-checked against the exact span `color` integer
from `page.get_text("dict")` (e.g. `0xc00000`, `0x404040`) — the two methods agreed exactly.

## Heading hierarchy and capitalization

The original alternates red/black by numbering depth — not a strict Title Case rule. Confirmed via
per-span `size`/`font`/`color` on real heading text:

| Level | Example | Style | Capitalization |
|---|---|---|---|
| Unnumbered chapter-level (Notice, Table of Contents) | "Notice" | Red, bold, ~22pt | Title Case |
| Chapter (`##`, `N.`) | "2. eTOM Processes, SID Data Entities and Functional Framework Functions" | Red, bold, ~28pt in the original (22pt in Helvetica here reads equivalently bold) | Title Case, acronyms (eTOM, SID) kept as styled |
| Section (`###`, `N.N`) | "2.1. eTOM business activities" | **Black**, bold, ~12pt | Mixed — most are Title Case ("Exposed APIs", "Functional Framework Functions"), but a few are sentence case in the original ("eTOM business activities", "eTOM L2 - SID ABEs links", "TMF Standards related versions") |
| Sub-section (`####`, `N.N.N`) | "5.2.1. Functional Framework" | **Red** again, bold, ~12pt | Title Case |

This skill's generated headings (in `_batch/build_main_md.py` and the Supplement template) already
mirror the original PDF's exact heading text verbatim, sentence-case exceptions included — see
SKILL.md, "Body structure" ("Mirror the existing PDF's numbered sections"). Don't "fix" those
sentence-case headings to Title Case; they're intentionally kept identical to what's published.
The visual color/weight styling is what `build_pdf.py`'s CSS applies on top, purely from the
heading's markdown level (`##`/`###`/`####`) — it doesn't need to know or care which capitalization
convention a given heading text happens to use.

**Acronyms are always styled as the source YAML/PDF has them** (`eTOM`, `SID`, `API`/`APIs`, `TMF`,
`ODA`) — never re-cased to match surrounding Title Case.

## Front page (cover) layout

Top to bottom, all left-aligned starting at the page's left margin (logo is the only right-aligned
element, see above):

1. `TM Forum Component` — red, bold, ~20pt, ~90pt from the top of the page.
2. Component display name (e.g. "Product Catalog Management") — dark gray `#404040`, bold, ~24pt,
   ~24pt below the kicker.
3. A large gap (~180pt) — the original leaves this whitespace deliberately; don't fill it with
   anything.
4. `TMFCxxx` id — dark gray, bold, ~13pt.
5. A bordered 3-row × 2-column table, all cells dark gray `#404040` bold ~10.5pt, `#999999` 1px
   borders:

   | | |
   |---|---|
   | Maturity Level: `<derived>` | Team Approved Date: `<publicationDate, DD-Mon-YYYY>` |
   | Release Status: `<status, capitalized>` | Approval Status: `<derived>` |
   | Version `<version>` | IPR Mode: RAND |

No italic running-title on the cover page itself (that starts on the Notice page onward) — see
"Running header" below. Field derivation rules (`Maturity Level`, `Approval Status`) are unchanged
from before this template pass — see SKILL.md, "Cover page & Notice".

## Notice page

Unchanged content-wise from the existing `NOTICE_TEXT` constant in `build_pdf.py`, styled with the
same red `<h1>Notice</h1>` heading. Two links now point at their real targets (extracted from the
original PDF's link annotations via `page.get_links()`), rather than being plain text:
- "TM FORUM IPR Policy" → `http://www.tmforum.org/IPRPolicy/11525/home.html`
- "www.tmforum.org" → `http://www.tmforum.org/`

## Table of Contents page

Red `<h1>Table of Contents</h1>`, then the existing dotted-leader two-column layout (unchanged
mechanically — see `_build_toc_html` in `build_pdf.py`).

## Running header and footer (every page)

Applied by `_apply_page_chrome()` in `build_pdf.py` as a single post-processing pass over the fully
merged PDF (cover + notice + ToC + body already combined) — not per-render-pass CSS. This is
deliberate: the cover/notice, ToC, and body are three separate `xhtml2pdf` renders merged together
afterward with PyMuPDF, so there's no single pass where a page-number tag could know the final,
true "page N of M" across the whole assembled document. Doing it as a direct-draw pass over the
merged result sidesteps that — see the function's docstring for the full reasoning.

- **Logo**: top-right, every page including the cover (position above).
- **Running title** (`TMFCxxx <Display Name> vX.Y.Z`, italic, ~9pt, black, top-left ~`(60, 40)`
  from the page's top-left): every page **except** the cover, which carries the title as its own
  large heading instead.
- **Footer** (~9pt, black, ~40pt from the bottom): `© TM Forum <year>. All Rights Reserved.` at the
  left margin, `Page N of M` right-aligned to the right margin — on every page, including the cover.

`@page` margins in `BASE_CSS` (`margin-top: 100pt`, `margin-bottom: 60pt`, `60pt` left/right) exist
specifically to leave clearance for this overlay — if the margins shrink, check that body text
doesn't collide with the logo/header/footer before shipping.

## Tables

Every table gets a light-gray `#EFEFEF` header row (`th { background-color: ... }`) and `#999999`
1px borders throughout — matches the original's own table styling, sampled the same way as the
heading colors.

## Font

The original uses **Aptos** (Microsoft 365's current default, replacing Calibri) throughout,
confirmed via span `font` names (`Aptos`, `Aptos,Bold`). This template deliberately does **not**
try to match that font — `xhtml2pdf` only reliably supports its built-in base-14 fonts
(Helvetica/Arial, Times, Courier) without embedding a `.ttf` and registering it, which is extra
fragility for a font-exactness detail nobody asked for. Helvetica/Arial bold at the sizes above
reads as an equivalent visual weight/hierarchy. If pixel-perfect font matching ever becomes a real
requirement, embedding Aptos (or a metrically-similar open font) via `pisaContext` font
registration is the way to do it — not attempted here.
