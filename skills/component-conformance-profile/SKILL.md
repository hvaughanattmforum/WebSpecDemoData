---
name: component-conformance-profile
description: Generate or update the ComponentConformanceProfile markdown document for a TMForum ODA component (TMFCxxx). Use this whenever a component's spec YAML changes (an exposed/dependent API is added, removed, or its `required` flag flips), whenever the user asks for a "conformance profile," asks what a component "must support" or "needs to pass CTK/conformance testing," or mentions ComponentConformanceProfile. Trigger this proactively after editing a component's TMFCxxx-*.yaml even if the user doesn't say "conformance" explicitly — the whole point of this document is to stay in sync with the spec's required-API list.
---

# Component Conformance Profile Generator

## What this produces and why

A markdown file at `specifications/<ComponentFolder>/ComponentConformanceProfile/<ComponentFolder>_Conformance.md`
in the **TMForum-ODA-Component-Specification** repo (this is always the output location, regardless of which repo
the source YAML came from — see "Two possible YAML sources" below).
This is the document implementers and the CTK (conformance test kit) actually get tested against — it's the bridge
between "the spec YAML marks this API `required: true`" and "conformance testing will fail you without it." Because
that translation is the entire reason this file exists separately from the spec, always derive the mandatory/optional
lists straight from the YAML's `required` flags rather than copying an old profile forward — if the flags changed,
the profile must change with them.

## Two possible YAML sources

There are two TMForum repos that can each hold a copy of a component's spec YAML, and they are not always in sync:

1. **TMForum-ODA-Component-Specification** — `specifications/<ComponentFolder>/<ComponentFolder>.yaml`.
   The active authoring repo (feature branches, in-flight PRs). Schema here has been trimmed down over time:
   `specification[].version` is a bare integer (`5`), there's no per-API `name` or `url` field, and as of the
   current `v1.1.0` branch **`securityFunction` has been dropped from the schema entirely**.
2. **TMForum-ODA-Ready-for-publication** — `<ComponentFolder>/Specification/<ComponentFolder>.yaml`.
   The published/release snapshot repo. Schema here is richer: `specification[].version` is a full string
   (`v5.0.0`), each API entry carries its own kebab-case `name` (e.g. `product-catalog-management-api` — a machine
   identifier, NOT the human-readable display name) and, crucially, each `specification[]` entry embeds its own
   `url:` field pointing straight at the swagger doc. It also still has a `securityFunction` block. `spec.coreFunction`
   nests `exposedAPIs`/`dependentAPIs` the same way in both repos, so the walk logic below is identical either way.

**Default to Ready-for-publication as the YAML source** when both are available for the branch you're working on —
it's the more complete/authoritative snapshot (has `securityFunction`, has inline swagger URLs, avoids the
apiIndex.json-churn problem described in step 7). Only fall back to Component-Specification's own YAML when you're
validating in-flight edits on a feature branch that hasn't been published to Ready-for-publication yet, or when the
user is explicitly asking about uncommitted/local changes to the Component-Specification YAML itself. If the two
repos disagree on required-flags for the same nominal version, that's a real cross-repo drift finding — surface it,
don't silently pick one.

## Steps

### 1. Find the component

Locate the YAML per "Two possible YAML sources" above (e.g.
`TMFC001-ProductCatalogManagement/Specification/TMFC001-ProductCatalogManagement.yaml` in Ready-for-publication, or
`specifications/TMFC001-ProductCatalogManagement/TMFC001-ProductCatalogManagement.yaml` in Component-Specification).
This is the only source of truth for what's mandatory — don't infer required-ness from anything else. Regardless of
which repo you read from, always write/compare the output against Component-Specification's
`specifications/<ComponentFolder>/ComponentConformanceProfile/<ComponentFolder>_Conformance.md`.

### 2. Header

Pull `id`, `name`, `version` from `spec.componentMetadata`:

```
# <id> – <name> – v<version>
```

### 3. Mandatory Exposed APIs

Walk `spec.coreFunction.exposedAPIs`. For each entry with `required: true`, resolve its name and swagger URL(s) (see "Resolving API names and swagger URLs" below) and list it:

```
## Mandatory Exposed APIs (Require Conformance)

- **TMF620 – Product Catalog Management API**
  Swagger:
  - <url for each specification[].version found>

*(Conformance MUST support one of the specified versions above.)*
```

If no exposed API has `required: true`, write: "There are **no mandatory exposed APIs** specified in this component." — don't skip the section or leave it blank; the absence is itself meaningful information for someone reading the profile.

### 4. Mandatory Dependent APIs

Same process as step 3, but walking `spec.coreFunction.dependentAPIs`, under a `## Mandatory Dependent APIs (Require Conformance)` heading.

### 5. Security Conformance Requirements

Look for `spec.securityFunction` in the component YAML. **As of the current schema, most components no longer have this block at all** — it was part of an older spec format (still visible in `specifications/Template/Component-OAS-Specification-v1beta*_gb.yaml` if you want to see the shape it used to take: `controllerRole`, `exposedAPIs` under `securityFunction`). Handle both cases honestly:

- **If `securityFunction` exists**: write the narrative explaining that the component must either expose the Security APIs listed there or provide a valid `canvasSystemRole`, name which specific API(s) are therefore mandatory, and note any other security-adjacent APIs elsewhere in the spec that are *not* part of `securityFunction` and are therefore ignored for conformance purposes.

  **The real mandatory/ignored rule (confirmed empirically across the checked-in profiles, not just the `required` flag):** `securityFunction.exposedAPIs` typically lists both TMF669 (Party Role Management API) and TMF672 (User Role Permission API), often both marked `required: false` in the YAML. Despite that flag, treat **TMF669 as always mandatory** whenever it's present in `securityFunction` — it's the canvas-identity API — regardless of its `required` value. Treat **TMF672 as present-but-ignored** for conformance purposes unless something else in the spec explicitly marks it required; don't promote it to mandatory just because it sits inside `securityFunction`. This overrides the naive reading of the `required` flag for these two specific APIs. If you encounter a checked-in profile that treats TMF672 (or any other non-TMF669 API in `securityFunction`) as mandatory, that's an anomaly worth flagging to the user rather than silently matching it — don't treat it as evidence the rule above is wrong.

  Follow this shape (adapt the specifics, don't paste this verbatim):

  ```
  ## Security Conformance Requirements

  The Component under test must comply with the Security Function requirements defined in the manifest.
  Specifically, the component must either expose and use the relevant Security APIs defined under the
  `securityFunction`, or provide a valid `canvasSystemRole`.

  In this case, **TMF669 (Party Role Management API)** is present under the Security Function and must
  therefore be treated as **mandatory for conformance**. [...]

  ### Mandatory Security API
  - **TMF669 – Party Role Management API**
    Swagger:
    - <url>
  ```

  **Do not add a "Secrets Management" subsection.** `securityFunction.secretsManagement` (a `sideCar`/port/
  `podSelector` sub-block, present whenever `securityFunction` is present) was tried as a documented subsection here
  and then deliberately dropped — the profile's Security Conformance Requirements section covers the mandatory-API
  narrative only; don't reintroduce secretsManagement reporting unless a future user explicitly asks for it again.

- **If `securityFunction` is absent** (the common case right now): don't invent one. Write a short, honest note instead, e.g. "This component's specification does not define a `securityFunction` block; no additional security-specific conformance requirements apply beyond the Canvas Conformance checks below." Then flag this to the user in your final summary — a missing security function is worth a human noticing, not silently normalizing.

### 6. Canvas Conformance

This section is boilerplate — identical across every component, not derived from the YAML at all. Copy it verbatim
from `references/canvas-conformance-boilerplate.md` rather than re-writing it from memory each time. Keeping it
byte-for-byte identical across components is the point: it's what lets someone diff two components' profiles and
trust that any difference is a real, meaningful difference.

### 7. Resolving API names and swagger URLs

The profile needs, per mandatory API: a human-readable name (`Product Catalog Management API`) and one swagger URL
per `specification[]` entry. How you get these depends on which repo the YAML came from (see "Two possible YAML
sources" above):

**If the YAML came from Ready-for-publication:** each `specification[]` entry already embeds its own `url:` field —
use that directly as the swagger URL, per version, exactly as listed. This is more authoritative than apiIndex.json
(it's what that specific release actually shipped) and sidesteps apiIndex.json's churn problem entirely (its
`swagger` field gets regenerated by CI and the URL format has flip-flopped over time — e.g. the same `TMF620_v5.0.0`
key has pointed at both an `ODA/TMF620_v5.0.0.swagger.json` path and an `OpenApiTable/.../swagger/....oas.yaml` path
across different regenerations, with no semantic difference). You still need a human-readable name though — the
YAML's own `name:` field here is a kebab-case machine identifier (`product-catalog-management-api`), not a display
name, so resolve the display name via `apiIndex.json` (step below) matched by `id` alone; don't derive it by
title-casing the kebab string, that produces things like "Api" instead of "API".

**If the YAML came from Component-Specification** (no inline `url:` field, bare integer version): resolve both name
and URL from `apiIndex.json`:

1. **`apiIndex.json` at the repo root** (`TMForum-ODA-Component-Specification/apiIndex.json`) — this is already
   present in the repo and is the primary source. Keys look like `"TMF620_v5.0.0"` / `"TMF620_v4.1.0"`, each with
   `name` and `swagger` fields. Since the YAML only gives a major version integer, match by prefix: for
   `id: TMF620, version: 5`, look for every key matching `TMF620_v5.*` (there may be more than one minor/patch
   version indexed — include all matches, the same way the real TMFC001 profile lists both a v5.0.0 and a v4.1.0
   swagger URL for TMF620 side by side).
2. **A sibling `TMForum-ODA-Ready-for-publication` checkout, same branch**, if the ID/version isn't found in step 1
   — read the inline `url:` field there the same way as above.
3. **If neither has it**, don't guess a URL or invent a name. List the bare ID and version and add an inline note
   like `<!-- swagger URL not found in apiIndex.json or Ready-for-publication — fill in manually -->` so it's
   visibly incomplete rather than silently wrong.

### 8. CTK Run Configuration (final chapter, embedded in the same document)

The ComponentConformanceProfile tells a human/CTK what's mandatory; the **CTK run configuration** is the JSON that
actually drives the conformance test kit against a deployed instance of the component. Append it as the **last
chapter of the same markdown document** — a `## CTK Run Configuration` heading followed by a fenced ```json code
block — rather than writing it out as a separate `.json` file. It gets carried into the PDF along with everything
else in step 9, and stays version-locked to the same document instead of being a second artifact that can drift out
of sync.

Use this exact shape, changing only the fields called out below — everything else is fixed boilerplate shared
across all components:

```json
{
    "releaseName": "pc-1",
    "component_to_run": "TMFC001",
    "component_namespace": "components",
    "standardComponentPath": "",
    "ctk_name_mapping": {},
    "runExposedOptional": false,
    "runDependentOptional": false,
    "runSecurityOptional": false,
    "ctk_download_urls": "https://raw.githubusercontent.com/tmforum-rand/TMForum-ODA-Component-Specification/refs/heads/v1.1.0/apiIndex.json",
    "standardComponentDownload": {
        "apiBaseUrl": "https://api.github.com",
        "repoOwner": "tmforum-rand",
        "repoName": "TMForum-ODA-Ready-for-publication",
        "gitUrl": "https://raw.githubusercontent.com/tmforum-rand/TMForum-ODA-Ready-for-publication/refs/heads",
        "gitBranch": "v1.1.0",
        "sslVerify": false
    },
    "ctkconfig": {
        "companyName": "TM FORUM",
        "productName": "REFERENCE EXAMPLE PRODUCT CATALOG",
        "productUrl": "https://www.tmforum.org",
        "componentUrl": "https://www.tmforum.org/oda/directory/components-map",
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        "payloads": {
            "TMF669_v4": {
                "PartyRole": {
                    "POST": {
                        "payload": {
                            "name": "TBD"
                        }
                    }
                }
            }
        },
        "rejectUnauthorized": false
    },
    "dependentStubs": {},
    "bddPayloads": {},
    "retrySettings": {
        "maxRetries": 30,
        "retryInterval": 10000
    }
}
```

This example is for **TMFC001-ProductCatalogManagement**. When adapting it for another component:

- **`component_to_run`**: the component's ID (e.g. `TMFC020`).
- **`releaseName`**: a short Helm-release-style slug for the component (e.g. `pc-1` for Product Catalog — follow
  the same abbreviated style, don't just reuse `pc-1` for a different component).
- **`ctkconfig.productName`**: a human-readable product/component name matching the component under test, not a
  copy-paste of "REFERENCE EXAMPLE PRODUCT CATALOG".
- **`ctkconfig.payloads`**: keyed by `<API-ID>_v<major>` (e.g. `TMF669_v4`), then by resource name (e.g.
  `PartyRole`), then by HTTP method, with a `payload` body for that operation. Populate this per the component's own
  mandatory APIs (see steps 3-5 above for what's mandatory) — don't leave last component's payload keys in place.
  When you don't have a live schema/example to source a realistic payload body from, put `"TBD"` in place of the
  actual field values rather than inventing plausible-looking data — this keeps the gap visible instead of silently
  wrong.
- **Everything else stays fixed** across components: `component_namespace`, `standardComponentPath`,
  `ctk_name_mapping`, the three `run*Optional` flags, `standardComponentDownload` (repo owner/name/URLs — always
  `tmforum-rand`/`TMForum-ODA-Ready-for-publication` for the standard spec, `TMForum-ODA-Component-Specification`
  for `ctk_download_urls`'s `apiIndex.json`), both branches (**`v1.1.0`**, matching the YAML source branch used
  throughout this skill — don't reuse an older branch like `v1beta4` just because an old example used it),
  `headers`, `rejectUnauthorized`/`sslVerify`, `dependentStubs`, `bddPayloads`, and `retrySettings`.

### 9. Write the file (and its PDF)

Output to `specifications/<ComponentFolder>/ComponentConformanceProfile/<ComponentFolder>_Conformance.md`, creating
the `ComponentConformanceProfile` directory if needed. If a profile already exists there, show the user what
changed (which APIs became mandatory/optional, security requirements changed) rather than silently overwriting —
that diff *is* the useful signal this whole skill exists to surface.

Alongside the `.md`, also produce a `.pdf` version at the same path with a `.pdf` extension (e.g.
`TMFC001-ProductCatalogManagement_Conformance.pdf` next to the `.md`) — the CTK and non-technical reviewers consume
the PDF, so it must stay in sync with the markdown every time the markdown changes, not be generated once and
forgotten.

Convert with a small Python script (this environment doesn't have `pandoc` or `wkhtmltopdf` installed, but pure-Python
`markdown` + `xhtml2pdf` work with no external binaries and have been verified against a real generated profile):

```bash
pip install --quiet markdown xhtml2pdf   # only needed once per environment
python - <<'EOF'
import markdown
from xhtml2pdf import pisa

src = "specifications/<ComponentFolder>/ComponentConformanceProfile/<ComponentFolder>_Conformance.md"
out = src.rsplit(".", 1)[0] + ".pdf"

with open(src, encoding="utf-8") as f:
    html_body = markdown.markdown(f.read(), extensions=["tables", "fenced_code"])

html = f"""<html><head><meta charset="utf-8">
<style>
body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; }}
h1 {{ font-size: 18pt; }}
h2 {{ font-size: 14pt; margin-top: 16pt; }}
h3 {{ font-size: 12pt; }}
code {{ font-family: Courier, monospace; }}
</style></head><body>{html_body}</body></html>"""

with open(out, "wb") as f:
    result = pisa.CreatePDF(html, dest=f)
assert result.err == 0, "PDF conversion failed"
EOF
```

If `markdown`/`xhtml2pdf` can't be installed in a given environment (no network access, etc.), fall back to whatever
markdown-to-PDF tool is actually available there (`pandoc -o out.pdf in.md`, a browser's print-to-PDF, etc.) rather
than skipping the PDF silently — but call out in your summary which method you used, since output fidelity (tables,
page breaks) can differ between tools.

## After generating

Summarize what changed in plain terms — "TMF701 dropped to optional, TMF671 is now mandatory, no security function
defined" — rather than just confirming the file was written. If step 5 hit the "no securityFunction" case, or step 7
hit the "couldn't resolve" case, call those out explicitly so the user can decide whether that's expected or a gap
worth fixing upstream.
