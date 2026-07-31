---
name: write-component-conformance-bdd
description: Generate Component Conformance BDD feature files, payloads, and documentation for TM Forum ODA Components with mandatory dependent APIs. Use this skill when creating or updating BDD artefacts under a component's BDD directory.
---

# Write Component Conformance BDD — Skill Instructions

## Purpose

This skill generates executable Component Conformance BDD artefacts for TM Forum ODA Components.

The generated artefacts must be compatible with the Component CTK execution framework and existing componentTests.js implementation.

The objective is to validate that a component correctly interacts with its mandatory dependent APIs through black-box testing of its exposed APIs.

---

## Scope

### In Scope

- Mandatory dependent APIs
- GET and GET by ID dependency validation
- POST operation validation on exposed APIs
- v4 and v5 Open APIs
- Single dependent API components
- Multiple dependent API components
- Base payload generation
- Target payload generation
- BDD feature generation
- README generation

### Out of Scope

- Optional dependent APIs
- No dependent APIs
- Management APIs
- Security APIs
- Event APIs
- Canvas lifecycle validation
- Operator-specific testing
- Custom step definition generation

---

## Output Structure

All generated artefacts must be placed under the component BDD directory.

Example:

specifications/TMFC007-ServiceOrderManagement/BDD/

Generated structure:

BDD/
├── README.md
├── TMFC007-DependentAPIInteraction.feature
└── payloads/
    ├── service-catalog-0001.json
    ├── service-inventory-0001.json
    ├── service-target-0001.json
    ├── service-target-0002.json
    ├── service-target-0003.json
    └── service-target-0004.json

---

## Input Artefacts

### Mandatory Inputs

1. Component Specification YAML — resolved from the local `specs/` folder first; fetched from the Ready-for-publication repository as fallback.
2. OpenAPI specifications — resolved from the local `specs/` folder first; fetched from the internet as fallback.

### Optional Inputs

1. Existing payload files
2. Existing BDD artefacts
3. CHANGE_ME.json

### Local Specs Folder

The canonical location for all local specification files is:

```
specifications/{CODE}-{ShortName}/specs/
```

Example:

```
specifications/TMFC011-ResourceOrderManagement/specs/
```

This folder must contain:

- The Component Specification YAML: `{CODE}-{ShortName}.yaml`  
  Example: `TMFC011-ResourceOrderManagement.yaml`
- One file per declared API version: `<TMFXXX>-v<version>.<ext>`  
  Examples: `TMF652-v4.json`, `TMF634-v5.yaml`, `TMF634-v4.json`, `TMF639-v4.json`

The skill runner is responsible for populating this folder before invoking the agent. All URLs required for download are available in the `specification[].url` entries for each API in `spec.coreFunction.exposedAPIs` and `spec.coreFunction.dependentAPIs`.

When the `specs/` folder is fully populated, no internet access is required during generation.

## Source Of Truth Priority

When conflicts exist, use the following precedence order:

1. Component Specification YAML (API discovery)
2. OpenAPI Specifications (schema generation)
3. Component CTK Runtime Contract
4. Fully Worked Examples
5. Generation Decision Tree
6. Generated Example Documentation

For payload generation, OpenAPI specifications are authoritative.

Do not derive behavior from README files when it conflicts with the runtime contract.

---

## Reference Artefacts

The following artefacts must be consulted before generating new BDD assets.

### Canonical Examples

TMFC005
- Single mandatory dependent API
- Product Catalog → Product Inventory

TMFC007
- Multiple mandatory dependent APIs
- Service Catalog + Service Inventory → Service Order

TMFC028
- Multi-stage dependency initialization
- Party → Party Role → Supplier

Location:

skills/write-component-conformance-bdd/reference/examples/

These examples are reference implementations.

They are authoritative only for:

- feature structure
- payload naming
- numbering conventions
- README structure
- multi-stage dependency patterns

They are not authoritative for:

- schema structure
- property names
- field types
- array names
- required attributes

OpenAPI specifications always take precedence.

### Runtime Contract

skills/write-component-conformance-bdd/reference/componentTests-contract.md

### Supporting Examples

skills/write-component-conformance-bdd/reference/generated-payload-examples.md

skills/write-component-conformance-bdd/reference/generated-feature-examples.md

### Generation Decision Tree

skills/write-component-conformance-bdd/reference/generation-decision-tree.md

Use this document to determine which generation pattern applies before selecting payload and feature generation rules.

### Component Specification YAML Schema

ci/component.schema.json

Consult this schema when parsing any Component Specification YAML to understand the exact structure of exposed and dependent API entries, including the `specification` array used for multi-version declarations.

### Component Specification Source Rule

The Component Specification YAML is the source of truth for BDD generation.

Resolution priority:

1. **User-supplied YAML** — if the user directly provides a YAML, use it.
2. **Local `specs/` folder** — check for the file at:
   `specifications/{CODE}-{ShortName}/specs/{CODE}-{ShortName}.yaml`
   If present, use it.
3. **Ready-for-publication repository** — fetch from the remote repository as fallback.

Fallback repository:

https://github.com/tmforum-rand/TMForum-ODA-Ready-for-publication

Fallback release branch:

v1.1.0

Fallback raw URL pattern:

```text
https://raw.githubusercontent.com/tmforum-rand/TMForum-ODA-Ready-for-publication/{release}/{CODE}-{ShortName}/Specification/{CODE}-{ShortName}.yaml
```

Example:

https://raw.githubusercontent.com/tmforum-rand/TMForum-ODA-Ready-for-publication/v1.1.0/TMFC005-ProductInventory/Specification/TMFC005-ProductInventory.yaml

When falling back to the repository:

- Use the configured release branch.
- Use the exact component folder name.
- Do not guess the folder name if unsure.
- Confirm the exact folder name from the repository tree or ask the user to provide the YAML.

---

## API Discovery from Component Specification YAML

Use `ci/component.schema.json` as the authoritative reference for the YAML structure when extracting API information.

### API Location in the YAML

Exposed and dependent APIs are declared under:

```
spec.coreFunction.exposedAPIs
spec.coreFunction.dependentAPIs
```

### API Entry Structure

Each entry in `exposedAPIs` and `dependentAPIs` conforms to the following structure (per the schema):

```yaml
id: TMF641                      # API identifier — use this to identify the API
name: serviceOrderManagement    # Human-readable name
required: true                  # Whether this API is mandatory
specification:                  # Array of version-specific OpenAPI specifications
  - version: 4                  # Version number (number or string)
    url: https://...            # URL to the OpenAPI specification for this version
    apiType: openapi
    path: /tmf-api/serviceOrdering/v4
  - version: 5
    url: https://...
    apiType: openapi
    path: /tmf-api/serviceOrdering/v5
version: 4                      # Top-level version field (may be present in older YAML)
```

The `specification` field is an **array**. Each element is an independent version entry with its own `url` and `version`.

### OpenAPI Specification URL Discovery

To retrieve the OpenAPI specification URL for an API:

1. Locate the API entry by `id` (e.g., `TMF641`) in `exposedAPIs` or `dependentAPIs`.
2. Read the `specification` array.
3. For each entry in the array, the `url` field is the URL to that version's OpenAPI specification.
4. The `version` field in each entry identifies which API version that URL corresponds to.

If the `specification` array is absent or empty, fall back to a top-level `url` field on the API entry if present (older YAML format).

Do not assume a single URL covers all versions. Each `specification` array entry is a distinct version with its own URL.

### Multiple Version Detection

When an API declares more than one version, the `specification` array will contain multiple entries — one per version.

Example:

```yaml
dependentAPIs:
  - id: TMF633
    name: serviceCatalog
    required: true
    specification:
      - version: 4
        url: https://raw.githubusercontent.com/.../TMF633-ServiceCatalog-v4.0.0.swagger.json
      - version: 5
        url: https://raw.githubusercontent.com/.../TMF633-ServiceCatalog.openapi.json
```

When this pattern is present:

1. Collect all entries from the `specification` array.
2. Extract the `version` and `url` from each entry.
3. Apply the OpenAPI Version Selection Rule: prefer the highest version.
4. Fetch the OpenAPI specification from the selected `url`.
5. Apply Version Compatibility Rules when generating payloads.

### Required API Identification

An API is mandatory if and only if its `required` field is `true`.

```yaml
required: true   # mandatory — include in BDD generation
required: false  # optional — skip
```

If the `required` field is absent, treat the API as optional.

---

## Fully Worked Examples

Before generating artefacts, inspect the fully worked examples under:

skills/write-component-conformance-bdd/reference/examples/

Use these examples as canonical output patterns.

Available examples:

- TMFC005: single mandatory dependent API
- TMFC007: multiple mandatory dependent APIs
- TMFC028: multi-stage dependency setup

Generated artefacts should follow the same structure, naming conventions, feature format, payload placeholder usage, and README documentation style.

---

## Generation Pipeline

Generation must follow the following sequence:

Resolve Component Specification
↓
Apply Generation Decision Tree (skills/write-component-conformance-bdd/reference/generation-decision-tree.md)
↓
Resolve Exposed API OpenAPI Specification
↓
Resolve Dependent API OpenAPI Specifications
↓
Fully Resolve POST Request Schemas
↓
Resolve All Nested $ref Definitions
↓
Identify Dependency Resource References
↓
Generate Base Payloads
↓
Generate Target Payloads
↓
Validate Generated Payloads Against Schemas
↓
Generate Feature File
↓
Generate README
↓
Run Validation Checklist

Do not skip any stage.

---

## Dependent API Selection Rules

### Rule 1

Use only dependent APIs where:

required: true

Ignore optional dependent APIs.

### Rule 2

For each mandatory dependent API, select the first resource that:

- Supports GET
- Supports GET /id
- Can be created using a POST operation in the dependent API specification

Examples:

TMF620 → productSpecification

TMF633 → serviceSpecification

TMF634 → resourceSpecification

TMF638 → service

TMF669 → partyRole

### Rule 3

If multiple resources exist:

Use the first listed resource only when it satisfies all selection criteria.

If multiple candidate resources satisfy the criteria:

1. Prefer the resource referenced by the exposed API schema.
2. Otherwise use the first listed resource.

### No Dependency Rule

If a component has no mandatory dependent APIs:

- Do not generate a DependentAPIInteraction feature.
- Do not generate payloads.
- Generate README.md explaining that no mandatory dependent API validation is required.

## Multi-Stage Dependency Rule

Some components require creation of intermediate dependent resources before the final dependent resource can be created.

Example:

TMFC028

Party
→ PartyRole
→ Supplier

In these cases the Scenario Outline structure differs from the standard pattern.

### Multi-Stage Scenario Outline Structure

```gherkin
  Scenario Outline: Test dependent API interactions with different payloads
    Given the CTK target component "<componentUnderTest>" with exposed API ID "<exposedApiId>" and dependent API ID "<dependentApiId>" has been installed successfully
    And the supporting stub "<dependentComponent>" for API "<dependentAPI>" has been installed successfully
    Given the target component exposed API "<exposedAPI>" is initialized with the payload defined in file "<basePayload>"
    Given the dependent API stub "<dependentAPI>" is initialized with the payload defined in file "<basePayload2>"
    When a "<resourceType>" with "<resourceFieldPath>" on payload defined in file "<targetPayload>" is created in API "<exposedAPI>" expecting "<expectedResponse>"
    Then expected response for operation "<operationID>" should be "<expectedResponse>"

  Examples:
    | componentUnderTest | dependentComponent | resourceType | exposedApiId | exposedAPI | dependentApiId | dependentAPI | basePayload | basePayload2 | targetPayload | resourceFieldPath | operationID | expectedResponse |
```

Key differences from the standard pattern:

1. `basePayload` initializes the **exposed API** (not the dependent stub): `Given the target component exposed API "<exposedAPI>" is initialized with the payload defined in file "<basePayload>"`
2. `basePayload2` initializes the **dependent API stub**: `Given the dependent API stub "<dependentAPI>" is initialized with the payload defined in file "<basePayload2>"`
3. The Examples table has an extra `basePayload2` column (13 columns total).

### Multi-Stage Placeholder Names

Multi-stage base payloads use different placeholder names to distinguish the intermediate resource from the final dependency.

Stage 1 base payload (`basePayload`): standard resource — no placeholders.

Stage 2 base payload (`basePayload2`): references the stage 1 resource using named placeholders:

```json
{
  "id": "__VALID_PARTY_ID__",
  "href": "__VALID_PARTY_HREF__"
}
```

Target payload (`targetPayload`): references the final dependent resource using the standard placeholders:

```json
{
  "id": "__VALID_ID__",
  "href": "__VALID_HREF__"
}
```

Use the canonical TMFC028 example for exact placeholder names and injection order.

### Multi-Stage Payload Naming

For multi-stage dependencies, base payloads are named to reflect their role in the setup sequence rather than the standard `<domain>-<resource>-0001.json` pattern. Follow the TMFC028 canonical example exactly.

---

## Exposed API Selection Rules

### Rule 1

Use only exposed APIs where:

required: true

Ignore optional exposed APIs.

### Rule 2

Generate dependency validation scenarios for every mandatory exposed API.

### Rule 3

If multiple mandatory exposed APIs exist, generate scenarios for each exposed API.

### Rule 4

Generate a single feature file per component.

If multiple mandatory exposed APIs exist, include scenarios for all mandatory exposed APIs within the same feature file.

---

## OpenAPI Spec File Resolution Rule

For each API version declared in the component specification, resolve the OpenAPI spec file using the following priority:

1. **Local `specs/` folder** — look for the file at:
   `specifications/{CODE}-{ShortName}/specs/<TMFXXX>-v<version>.<ext>`
   Example: `specifications/TMFC011-ResourceOrderManagement/specs/TMF634-v5.yaml`
   If the file exists, use it.
2. **Internet fetch** — fetch from the `url` field in the matching `specification` array entry as fallback.
3. **Failure** — if neither is available, stop generation for that API version, document the gap in README.md, request the skill runner to supply the missing file, and apply the Version Fallback Rule.

Apply this resolution priority independently for each declared version of each API. A local file for v4 does not substitute for a missing v5 file — attempt to resolve each version separately.

When the local `specs/` folder is fully populated, no internet access is required during generation.

---

## OpenAPI Resolution Rules

OpenAPI specifications are the authoritative source for payload generation.

Before generating any payload:

1. Apply the OpenAPI Spec File Resolution Rule to obtain the spec for each required version.
2. Resolve the POST operation.
3. Resolve the requestBody schema.
4. Resolve all nested $ref definitions recursively.
5. Continue resolution until a fully expanded schema model exists.
6. Generate payloads only from the resolved schema.

Do not generate payloads solely from:

- examples
- sample payloads
- README documentation
- naming conventions
- previously generated payloads

Examples may be used only to choose realistic sample values after the schema structure, field names, types, and required fields have been resolved.

---

## Schema-Driven Payload Rule

All payload content must be derived from the resolved OpenAPI schema.

The following must never be inferred:

- property names
- array names
- object structure
- field types
- required attributes
- enum values

These must always be resolved from the schema.

Examples are not authoritative.

Schema definitions always override examples.

---

## Payload Validation Rules

Every generated payload must be validated against the resolved schema before generation completes.

Verify:

- required fields exist
- property names exist
- nested objects exist
- array names match schema
- scalar types match schema
- enum values are valid
- object hierarchy matches schema

If validation still fails after regeneration:

- Stop generation.
- Report the validation failure.
- Do not emit BDD artefacts that violate schema requirements.

---

## Scalar Type Validation Rule

Generated payload values must match OpenAPI scalar types.

Examples:
Schema:
```yaml
priority:
  type: integer
```

Valid:
```json
{
  "priority": 1
}
```
Invalid:
```json
{
  "priority": "1"
}
```

The generator must validate all scalar types before finalizing payloads.

---

## Array Name Verification Rule

Array names must be resolved directly from the schema.

Do not infer array names from:

- other TM Forum APIs
- examples
- naming conventions

Examples:

Correct:
```json
{
  "orderItem": []
}
```

Incorrect:
```json
{
  "resourceOrderItem": []
}
```

if the schema defines orderItem.

---

## Schema Ambiguity Rule

If the schema cannot be fully resolved:

Do not:

- guess field names
- guess array names
- guess object hierarchy
- guess types
- copy structures from another TM Forum API

Instead:

- document the unresolved section
- report the issue in README.md
- request human review

---

## Base Payload Generation Rules

### Purpose

Create a valid resource in the dependent API.

Base payloads are always generated from the dependent API POST schema.

### Rule 1

Locate the POST operation for the selected dependent resource.

### Rule 2

Resolve:
- requestBody
- schema
- examples for sample values only

### Rule 3

If examples exist:

Use examples only to populate sample values.

Do not derive structure, field names, required attributes,
or field types from examples.

Schema definitions always take precedence.

### Rule 4

Otherwise:

Build a minimum viable payload using required fields.

### Rule 5

Remove:

- id
- href

unless explicitly required.

### Rule 6

Generate one base payload per dependent resource.

Examples:

product-catalog-0001.json

service-catalog-0001.json

service-inventory-0001.json

resource-catalog-0001.json

party-role-0001.json

---

## Target Payload Generation Rules

### Purpose

Validate dependent API interactions through the exposed API.

Target payloads are always generated from the exposed API POST schema.

### Target Payload Construction Workflow

1. Resolve the POST request schema of the exposed resource.
2. Identify mandatory attributes.
3. Build the minimum valid payload.
4. Locate the dependent resource reference path.
5. Insert __VALID_ID__ and __VALID_HREF__ placeholders.
6. Generate a corresponding invalid variant using non-existent values.

### Rule 1

Locate the POST operation for the exposed resource.

### Rule 2

Identify the schema path where the dependent resource is referenced.

### Rule 3

Generate:

One valid payload

One invalid payload

per dependent resource.

### Valid Reference Pattern

```json
{
  "id": "__VALID_ID__",
  "href": "__VALID_HREF__"
}
```

### Invalid Reference Pattern

```json
{
  "id": "non-existent-id",
  "href": "non-existent-href"
}
```

### Rule 4

Generate exactly:

- 1 success payload
- 1 failure payload

for each dependent resource.

### Placeholder Rules

Success payloads must use:

__VALID_ID__
__VALID_HREF__

These placeholders are replaced dynamically by componentTests.js.

Do not generate actual IDs or href values in success payloads.

Failure payloads must use:

non-existent-id
non-existent-href

### Exposed Schema Strictness Rule

Target payloads must be generated strictly from the exposed API POST request schema.

Do not infer target payload property names from similar APIs or canonical examples.

Canonical examples are guidance only. They must not override the exposed API schema.

Before finalizing a target payload:

- verify every top-level property exists in the exposed POST schema
- verify each nested property path exists in the resolved schema
- verify scalar field types match the schema
- verify array names match the schema exactly
- verify resourceFieldPath is derived from the actual payload path

If a generated field does not exist in the exposed API POST schema, remove or correct it.
Schema validation must be performed before and after placeholder insertion where placeholders are used. Placeholder values may be treated as schema-valid strings for id and href fields.

### Dependency Reference Verification Rule

Before generating target payloads:

1. Confirm the dependent resource type exists in the exposed API schema.
2. Confirm the dependent reference object is present.
3. Confirm the reference contains an identifier field.
4. Confirm the reference path is reachable from the POST payload root.

Only then generate success and failure payloads.

If the target payload cannot be validated against the exposed POST request schema, do not generate the feature row for that dependency. Report the unresolved validation issue in README.md.

If the base payload cannot be validated against the dependent API POST schema, do not generate scenarios for that dependent resource. Report the validation issue in README.md.

---

## Resource Mapping Discovery

The skill must recursively inspect the exposed API POST schema.

Goal:

Find where the dependent resource type is referenced.

Examples:

TMF620 ProductSpecification
→ ProductSpecificationRef

TMF633 ServiceSpecification
→ ServiceSpecificationRef

TMF634 ResourceSpecification
→ ResourceSpecificationRef

TMF669 PartyRole
→ RelatedParty

TMF638 Service
→ ServiceRefOrValue
→ serviceOrderItem[0].service

TMF633 ServiceSpecification
→ ServiceSpecificationRef
→ serviceOrderItem[0].service.serviceSpecification

---
## Resource Field Path Discovery Rules

Generate lodash-compatible resource paths.

Examples:

productSpecification

serviceSpecification

serviceOrderItem[0].service

serviceOrderItem[0].service.serviceSpecification

relatedParty[0]

The generated path must be compatible with:

_.set(payload, `${resourceFieldPath}.id`, value)

If the dependent resource reference path cannot be determined from the exposed API schema:

- Do not guess.
- Do not infer from naming conventions.
- Report the unresolved path in the README.
- Request human review.

---

## Resource Field Path Verification Rule

resourceFieldPath must be derived from the generated target payload.

Verification procedure:

1. Locate the dependency reference object in the generated payload.
2. Determine the exact path to the object containing:

```json
{
  "id": "__VALID_ID__",
  "href": "__VALID_HREF__"
}
```

3. Verify:

_.set(payload, `${resourceFieldPath}.id`, value)
_.set(payload, `${resourceFieldPath}.href`, value)

updates the intended object.

If verification fails:

* regenerate the path
* do not guess

This prevents incorrect paths.

---

## OperationID Rule

Use the operationId defined on the POST operation of the exposed resource.

Examples:

TMF641 serviceOrder
→ createServiceOrder

TMF637 product
→ createProduct

---

## Resource Type Rule

resourceType must be the resource name associated with the exposed API POST operation.

resourceType must be derived from the POST operation resource path
or POST request schema.

Do not infer resourceType from examples.

Examples:

TMF637 product
→ product

TMF638 service
→ service

TMF639 resource
→ resource

TMF641 serviceOrder
→ serviceOrder

---

## Feature File Naming Rules

Pattern:

TMFCxxx-DependentAPIInteraction.feature

Examples:

TMFC005-DependentAPIInteraction.feature

TMFC007-DependentAPIInteraction.feature

TMFC008-DependentAPIInteraction.feature

TMFC012-DependentAPIInteraction.feature

TMFC028-DependentAPIInteraction.feature

---

## Feature File Template

Use the existing Component CTK contract.

Required tag:

@tmfcxxx

Example:

```gherkin
@tmfc007

Feature: Dependent API interaction testing for TMFC007 - Service Order

  Scenario Outline: Test dependent API interactions with different payloads  
    Given the CTK target component "<componentUnderTest>" with exposed API ID "<exposedApiId>" and dependent API ID "<dependentApiId>" has been installed successfully
    And the supporting stub "<dependentComponent>" for API "<dependentAPI>" has been installed successfully
    Given the dependent API stub "<dependentAPI>" is initialized with the payload defined in file "<basePayload>"
    When a "<resourceType>" with "<resourceFieldPath>" on payload defined in file "<targetPayload>" is created in API "<exposedAPI>" expecting "<expectedResponse>"
    Then expected response for operation "<operationID>" should be "<expectedResponse>"

  Examples:
    | componentUnderTest | dependentComponent   | resourceType  | exposedApiId  | exposedAPI   | dependentApiId | dependentAPI          | basePayload                | targetPayload             | resourceFieldPath                                      | operationID        | expectedResponse |
    | tmfc007            | serviceCatalog       | serviceOrder  | TMF641        | serviceOrder | TMF633         | serviceSpecification  | service-catalog-0001.json  | service-target-0001.json  | serviceOrderItem[0].service.serviceSpecification       | createServiceOrder | success          |
    | tmfc007            | serviceCatalog       | serviceOrder  | TMF641        | serviceOrder | TMF633         | serviceSpecification  | service-catalog-0001.json  | service-target-0002.json  | serviceOrderItem[0].service.serviceSpecification       | createServiceOrder | failure          |
    | tmfc007            | serviceInventory     | serviceOrder  | TMF641        | serviceOrder | TMF638         | service               | service-inventory-0001.json| service-target-0003.json  | serviceOrderItem[0].service                            | createServiceOrder | success          |
    | tmfc007            | serviceInventory     | serviceOrder  | TMF641        | serviceOrder | TMF638         | service               | service-inventory-0001.json| service-target-0004.json  | serviceOrderItem[0].service                            | createServiceOrder | failure          |
```

Do not generate custom step definitions.

### Feature Column Derivation

Before populating the Examples table, derive each column value as follows:

| Column | Source |
|--------|--------|
| `componentUnderTest` | Component code in lowercase (e.g., `tmfc007`) |
| `dependentComponent` | `name` field of the dependent API entry in the component specification YAML |
| `resourceType` | Resource name of the exposed API POST operation, derived from the OpenAPI spec |
| `exposedApiId` | `id` field of the exposed API entry in the component specification YAML (e.g., `TMF641`) |
| `exposedAPI` | Resource path/name of the exposed API POST operation (e.g., `serviceOrder` for `POST /serviceOrder`) |
| `dependentApiId` | `id` field of the dependent API entry in the component specification YAML (e.g., `TMF633`) |
| `dependentAPI` | Resource name selected from the dependent API OpenAPI spec (e.g., `serviceSpecification`) |
| `basePayload` | Generated base payload filename |
| `targetPayload` | Generated target payload filename |
| `resourceFieldPath` | lodash-compatible path to the dependency reference in the target payload |
| `operationID` | `operationId` of the POST operation in the exposed API OpenAPI spec |
| `expectedResponse` | `success` or `failure` |

`dependentComponent` is a short camelCase identifier for the dependent component stub. Derive it as follows:

1. Read the `name` field of the matching entry in `spec.coreFunction.dependentAPIs`.
2. If the `name` is already a short camelCase identifier (e.g., `serviceCatalog`, `serviceInventory`), use it directly.
3. If the `name` is a hyphenated full API name (e.g., `resource-catalog-management-api`), derive the short form:
   - Remove trailing `-management-api`, `-management`, or `-api` suffixes.
   - Convert the remaining hyphen-separated words to camelCase.
   - Example: `resource-catalog-management-api` → remove `-management-api` → `resource-catalog` → `resourceCatalog`
   - Example: `resource-inventory-management-api` → remove `-management-api` → `resource-inventory` → `resourceInventory`

The result must match the style of the canonical examples: `productCatalog`, `serviceCatalog`, `serviceInventory`, `resourceCatalog`, `resourceInventory`.

`exposedAPI` is the resource name from the POST operation path (the segment after the last `/`), not the API name or ID.

---

## Payload Naming Rules

### Base Payloads

Pattern:

<domain>-<resource>-0001.json

Examples:

product-catalog-0001.json

service-catalog-0001.json

service-inventory-0001.json

resource-catalog-0001.json

party-role-0001.json

### Target Payloads

Pattern:

<domain>-target-xxxx.json

Examples:

product-target-0001.json

product-target-0002.json

service-target-0001.json

service-target-0002.json

service-target-0003.json

service-target-0004.json

### Numbering Rules

Success payloads:

0001
0003
0005

Failure payloads:

0002
0004
0006

### Numbering Algorithm

For each dependent API:

valid payload = next odd number

invalid payload = next even number

Examples:

Dependent API 1:
0001 valid
0002 invalid

Dependent API 2:
0003 valid
0004 invalid

---

## Version Compatibility Rules

Default Mode:

Use the highest available OpenAPI version as the primary schema for generation, then validate compatibility against lower versions where possible.

### Rule 1

Inspect all versions available in the component specification.

Multiple versions are declared as multiple entries in the `specification` array of the API entry (see API Discovery from Component Specification YAML). Iterate the full `specification` array to collect all declared versions and their URLs before selecting a primary version.

### Rule 2

Generate payloads compatible with both v4 and v5 whenever possible.

### Rule 3

Generate the smallest payload that satisfies:

- v4 schema requirements
- v5 schema requirements

If both versions are available, the payload must successfully validate against both versions whenever possible.

### Rule 4

Generate a single feature file per component.

Do not generate version-specific feature files unless explicitly requested.

### API Version Scenario Rule

Do not generate separate scenarios for v4 and v5 versions of the same API.

Generate a single dependency validation scenario set per exposed API and dependent API combination.

The CTK runtime determines which API version is deployed and executes the same BDD artefacts against that implementation.

### OpenAPI Version Selection Rule

When multiple versions of an API are referenced (i.e., the `specification` array contains more than one entry):

1. Collect all entries from the `specification` array; each entry has a `version` and a `url`.
2. Select the entry with the highest `version` value as the primary OpenAPI specification.
3. Fetch the OpenAPI specification from the selected entry's `url`.
4. Generate payloads against the highest-version schema.
5. Fetch and verify compatibility against lower-version schemas where other `specification` entries exist.
6. If compatibility cannot be achieved across all declared versions, document the limitation in README.md.

### Version Fallback Rule

If a usable payload cannot be constructed from the highest available version:

1. Build the payload using the next lower version schema.
2. Verify compatibility with the higher version.
3. Reuse the lower-version payload if compatible.
4. Document the fallback in README.md if full compatibility cannot be achieved.

### Cross-Version Required Field Comparison Rule

When spec files for multiple versions are available, explicitly compare the `required` arrays of the POST request schema between versions before generating payloads.

Fields that are required in the higher version but not in the lower version must be included in the generated payload to ensure cross-version compatibility.

Apply this comparison for every object in the schema that is present in the generated payload, not just the top-level schema.

### `@type` Discriminator Rule

TM Forum v5 OpenAPI schemas promote `@type` to a mandatory discriminator field on resource creation. v4 schemas typically do not require it.

When generating base or target payloads that will be used against APIs declaring a v5 specification:

1. Check whether `@type` appears in the `required` array of the POST request schema for the v5 spec.
2. If required, include `"@type": "<ResourceClassName>"` in the payload.
3. The value must be the concrete class name of the resource being created (e.g., `"ResourceSpecification"` for TMF634, `"Resource"` for TMF639).

When the v5 spec file is unavailable and the v4 schema is used as fallback, apply the following defensive rule:

- If the API declares a v5 version in the component specification YAML, include `"@type": "<ResourceClassName>"` in the generated payload regardless of whether the v5 spec was successfully retrieved.
- Document in README.md that `@type` was added defensively due to an inaccessible v5 spec.

The resource class name is the PascalCase name of the resource (e.g., the resource selected from the dependent API, capitalised: `productSpecification` → `"ProductSpecification"`, `service` → `"Service"`).

---

## README Generation Rules

Generate README.md under the BDD folder.

Include:

- Component Name
- Exposed APIs
- Mandatory Dependent APIs
- Generated Payloads
- Generated Scenarios

Example:

Component: TMFC007

Exposed API:
- TMF641 Service Order Management

Mandatory Dependent APIs:
- TMF633 Service Catalog
- TMF638 Service Inventory

Generated Scenarios:
1. Valid ServiceSpecification reference
2. Invalid ServiceSpecification reference
3. Valid Service reference
4. Invalid Service reference

Dependent Resource Mapping:

TMF633 Service Catalog
Resource: serviceSpecification
Field Path: serviceOrderItem[0].service.serviceSpecification

TMF638 Service Inventory
Resource: service
Field Path: serviceOrderItem[0].service

Operation Mapping:

TMF641 serviceOrder
→ createServiceOrder

---

## Generated Artefact Audit

Before generation completes verify:

Payload Audit

- All payloads validate against schema
- All required fields present
- All scalar types valid
- All array names valid
- All nested references resolved

Dependency Audit

- Dependent resource exists
- resourceFieldPath verified
- placeholder injection verified

Feature Audit

- Examples table matches runtime contract
- operationId verified
- resourceType verified

README Audit

- mappings match generated payloads
- operationIds match OpenAPI specifications

---

## Validation Checklist

Before generation completes verify:

✓ Mandatory exposed API found

✓ Mandatory dependent API found

✓ Dependent resource selected

✓ POST operation identified

✓ Resource field path resolved

✓ Placeholder injection path validated

✓ Generated payloads are compatible with componentTests.js placeholder injection logic

✓ OperationId identified

✓ Base payload generated

✓ Target payload generated

✓ Success scenario generated

✓ Failure scenario generated

✓ Compatible with componentTests.js

✓ Generated artefacts conform to documented examples and runtime contracts

✓ OpenAPI POST schema fully resolved

✓ All nested $ref definitions resolved

✓ Generated payload validated against schema

✓ Property names verified

✓ Array names verified

✓ Scalar types verified

✓ Required fields verified

✓ Dependency reference verified

✓ resourceFieldPath verified against payload

✓ resourceType verified against POST operation

✓ operationId verified against POST operation

✓ target payload schema matches POST requestBody schema

✓ No payload structure derived solely from examples

✓ `@type` field included in base payloads where v5 spec requires it or where a v5 version is declared and the spec was inaccessible

✓ Cross-version required field comparison performed where multiple spec versions are available

✓ README mappings match generated payloads

---

## Key Principles

1. Reuse existing CTK execution patterns.
2. Generate executable artefacts, not examples.
3. Use mandatory dependent APIs only.
4. Prefer version-tolerant payloads.
5. Generate one feature file per component.
6. Generate deterministic file names.
7. Do not create new step definitions.
8. Do not test Canvas or operator internals.
9. Generate README documentation for all outputs.
10. Ensure all generated artefacts can be consumed by the Component CTK without modification.