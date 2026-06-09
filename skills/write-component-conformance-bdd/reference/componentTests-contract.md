# Component CTK Runtime Contract

## Purpose

This document defines the runtime contract expected by the Component CTK implementation.

Generated BDD artefacts must comply with this contract.

---

# Feature File Contract

Generated feature files must use the existing CTK step definitions.

The Scenario Outline structure must remain unchanged.

Example:

```gherkin
Scenario Outline: Test dependent API interactions with different payloads

  Given the CTK target component "<componentUnderTest>" with exposed API ID "<exposedApiId>" and dependent API ID "<dependentApiId>" has been installed successfully

  And the supporting stub "<dependentComponent>" for API "<dependentAPI>" has been installed successfully

  Given the dependent API stub "<dependentAPI>" is initialized with the payload defined in file "<basePayload>"

  When a "<resourceType>" with "<resourceFieldPath>" on payload defined in file "<targetPayload>" is created in API "<exposedAPI>" expecting "<expectedResponse>"

  Then expected response for operation "<operationID>" should be "<expectedResponse>"
```

---

# Required Example Columns

Generated Examples tables must contain the following columns.

| Column |
|----------|
| componentUnderTest |
| dependentComponent |
| resourceType |
| exposedApiId |
| exposedAPI |
| dependentApiId |
| dependentAPI |
| basePayload |
| targetPayload |
| resourceFieldPath |
| operationID |
| expectedResponse |

Do not add or remove columns.

---

# Payload Placeholder Contract

Success payloads must contain:

```json
{
  "id": "__VALID_ID__",
  "href": "__VALID_HREF__"
}
```

TMFC028 specific:

```json
{
  "id": "__VALID_PARTY_ID__",
  "href": "__VALID_PARTY_HREF__"
}
```

These values are replaced dynamically at runtime.

Failure payloads must contain:

```json
{
  "id": "non-existent-id",
  "href": "non-existent-href"
}
```

---

# Runtime Injection Contract

The CTK injects dependent resource identifiers using lodash.

Example:

```javascript
_.set(payload, `${resourceFieldPath}.id`, this.dependentAPI_ID);
_.set(payload, `${resourceFieldPath}.href`, this.dependentAPI_HREF);
```

Therefore resourceFieldPath must always be a valid lodash path.

---

# Resource Field Path Examples

Valid examples:

```text
productSpecification

serviceSpecification

serviceOrderItem[0].service

serviceOrderItem[0].service.serviceSpecification

relatedParty[0]
```

---

# Base Payload Contract

Base payloads are used to create resources in dependent APIs.

Requirements:

- Must be valid POST payloads
- Must create a resource successfully
- Must not contain runtime placeholders
- Must not contain hardcoded IDs unless required by the API

---

# Target Payload Contract

Target payloads are used against exposed APIs.

Requirements:

- Must contain dependency reference
- Must contain valid placeholders for success scenarios
- Must contain invalid identifiers for failure scenarios
- Must remain compatible with componentTests.js runtime replacement

---

# OperationID Contract

operationID must match the POST operationId of the exposed API.

Examples:

| Resource | operationId |
|-----------|------------|
| product | createProduct |
| service | createService |
| serviceOrder | createServiceOrder |
| resource | createResource |

---

# Version Contract

Generated artefacts must be version-tolerant whenever possible.

One feature file should support:

- v4 implementation
- v5 implementation

The CTK runtime determines which version is deployed.

---

# Multi stage dependency pattern
Some dependent APIs require initialization of another dependent resource first.

Example:

Party
→ PartyRole
→ Supplier

The generated BDD may require multiple base payloads before the target payload can be executed.

Note: Multi-stage dependency setup may require CTK support beyond the default single basePayload step. Use TMFC028 as the canonical example when generating this pattern.