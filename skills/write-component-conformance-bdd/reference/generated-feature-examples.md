# Generated Feature Examples

This document provides examples of generated Component Conformance BDD feature files.
OpenAPI specifications are authoritative for all feature metadata values including operationID, resourceType, and resourceFieldPath.

---

Reference feature examples:

skills/write-component-conformance-bdd/reference/examples/TMFC005
skills/write-component-conformance-bdd/reference/examples/TMFC007
skills/write-component-conformance-bdd/reference/examples/TMFC028

These examples are authoritative for:

- Feature structure
- Examples table structure
- Scenario outline format
- Payload naming conventions
- README formatting

These examples are not authoritative for:

- resourceType values
- operationID values
- resourceFieldPath values
- payload structure

These values must be derived from the Component Specification YAML and OpenAPI specifications.

---

# Resource Field Path Rules

resourceFieldPath must:

- correspond to the actual dependency reference location in the generated target payload
- be compatible with lodash _.set()
- be validated against the generated payload

Examples:

productSpecification

serviceOrderItem[0].service

serviceOrderItem[0].service.serviceSpecification

relatedParty[0]

Do not infer paths from examples.

---

# OperationID Rules

operationID must be derived from the POST operationId of the exposed API.

Examples:

createProduct
createService
createResource
createServiceOrder

Do not infer operationID values from examples.

---

# Resource Type Rules

resourceType must be derived from the exposed API POST resource.

Examples:

product
service
resource
serviceOrder

Do not infer resourceType values from examples.

---

# Example: Multiple Mandatory Dependent APIs

Rule:

For each dependent API:

- Generate one success scenario
- Generate one failure scenario

Each Examples row must reference:

- an existing base payload
- an existing target payload
- a valid resourceFieldPath
- a valid operationID
- a valid resourceType

Rows that cannot be validated must not be generated.

Example:

TMFC007

TMF633
- success
- failure

TMF638
- success
- failure

Result:

4 example rows

---

# Multiple Exposed APIs

If a component contains multiple mandatory exposed APIs:

- Generate a single feature file.
- Include scenarios for all mandatory exposed APIs.
- Generate success and failure rows for each exposed API and dependent API combination.

---

# Feature Generation Principles

1. One feature file per component.
2. One scenario outline per component.
3. One success row per dependency.
4. One failure row per dependency.
5. Reuse existing CTK step definitions.
6. Do not generate JavaScript step definitions.
7. Generate feature metadata (resourceType, operationID, resourceFieldPath) from OpenAPI specifications, not examples.