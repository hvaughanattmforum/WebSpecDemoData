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

1. Fully resolved Component Specification YAML from the Ready-for-publication repository, unless the user directly supplies a YAML or explicitly requests local-file mode.
2. OpenAPI specifications referenced by the Component Specification.

### Optional Inputs

1. Existing payload files
2. Existing BDD artefacts
3. CHANGE_ME.json

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

### Component Specification Source Rule

The Component Specification YAML is the source of truth for BDD generation.

By default, resolve the Component Specification YAML from the TM Forum Ready-for-publication repository.

Default repository:

https://github.com/tmforum-rand/TMForum-ODA-Ready-for-publication

Default release branch:

v1.1.0

Default raw URL pattern:

```text
https://raw.githubusercontent.com/tmforum-rand/TMForum-ODA-Ready-for-publication/{release}/{CODE}-{ShortName}/Specification/{CODE}-{ShortName}.yaml
```

Example:

https://raw.githubusercontent.com/tmforum-rand/TMForum-ODA-Ready-for-publication/v1.1.0/TMFC005-ProductInventory/Specification/TMFC005-ProductInventory.yaml

Source priority:

1. Component Specification YAML directly provided by the user.
2. Component Specification YAML resolved from the Ready-for-publication repository.
3. Local repository YAML only if the user explicitly requests local-file mode.

Do not use local component specification YAML files by default.

Local YAML files may be stale and must not override the Ready-for-publication repository unless explicitly requested.

When resolving from the Ready-for-publication repository:

- Use the configured release branch.
- Use the exact component folder name.
- Do not guess the folder name if unsure.
- Confirm the exact folder name from the repository tree or ask the user to provide the YAML.

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

In these cases:

- Multiple base payloads may be generated.
- Runtime placeholder names may differ from __VALID_ID__ and __VALID_HREF__.
- Follow the canonical example implementation.

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

## OpenAPI Resolution Rules

OpenAPI specifications are the authoritative source for payload generation.

Before generating any payload:

1. Resolve the POST operation.
2. Resolve the requestBody schema.
3. Resolve all nested $ref definitions recursively.
4. Continue resolution until a fully expanded schema model exists.
5. Generate payloads only from the resolved schema.

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

### Version Fallback Rule

If a usable v5 example cannot be constructed:

1. Build the payload using the v4 schema.
2. Verify compatibility with v5.
3. Reuse the v4 payload.

---

### Resource Mapping Discovery

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

Inspect all available versions referenced in the component specification.

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

## OpenAPI Version Selection Rule

When multiple versions of an API are referenced:

1. Prefer the highest available version.
2. Generate payloads against that version.
3. Verify compatibility with lower supported versions.
4. If compatibility cannot be achieved, document the limitation in README.md.

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

TMF637 product
→ createProduct

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

✓ Resource field path discovered

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