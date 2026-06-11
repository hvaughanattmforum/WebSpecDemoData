# AGENTS.md

## Repository Purpose

This repository contains TM Forum ODA Component Specifications and supporting artefacts used to generate Component Conformance Test Kit (CTK) Behaviour-Driven Development (BDD) assets.

The primary objective is to maintain component specifications and generate executable BDD artefacts that validate interoperability between exposed APIs and mandatory dependent APIs.

---

## Repository Structure

### Component Specifications

specifications/TMFCxxx-/Specification/

Contains the source ODA Component specification YAML files.

### Generated BDD Artefacts

specifications/TMFCxxx-/BDD/

Contains:

- Feature files
- Payloads
- README documentation

generated for Component Conformance testing.

### Agent Skills

skills/write-component-conformance-bdd/

Contains:

- SKILL.md
- Runtime contracts
- Decision trees
- Reference examples
- Generation guidance

### Agents

.github/agents/

Contains specialized agents that generate and maintain repository artefacts.

---

## Rules

### Component Specifications

Do not modify component specification YAML files unless explicitly requested.

### Component Specification Source

By default, resolve Component Specifications from the TM Forum Ready-for-publication repository.

Source priority:

1. User-supplied specification
2. Ready-for-publication repository
3. Local repository copy only when explicitly requested

Do not use local specification files by default because they may be stale.

### BDD Artefacts

Generate BDD artefacts only under:

specifications/TMFCxxx-*/BDD/

### Runtime Compatibility

Generated artefacts must comply with:

skills/write-component-conformance-bdd/reference/componentTests-contract.md

### OpenAPI Authority

For payload generation:

1. Component Specification YAML is authoritative for API discovery.
2. OpenAPI specifications are authoritative for payload structure.
3. Examples may only be used for sample values.

Do not derive payload structure, field names, field types, array names, required attributes, or object hierarchy from examples.

### Payload Validation

Before emitting any payload:

- Resolve the OpenAPI POST request schema.
- Resolve all nested $ref definitions.
- Validate generated payloads against the resolved schema.
- Verify property names.
- Verify array names.
- Verify scalar types.
- Verify required attributes.

Do not emit payloads that fail schema validation.

### Feature Consistency Validation

Before emitting a feature file:

- Verify resourceFieldPath exists in the generated target payload.
- Verify operationId matches the exposed API POST operation.
- Verify resourceType matches the exposed API POST resource.
- Verify each Examples row references existing payload files.

Do not emit feature rows that reference unresolved payload paths.

### Generation Guidance

Before generating new artefacts consult:

1. SKILL.md
2. generation-decision-tree.md
3. componentTests-contract.md
4. Canonical examples

### Canonical Examples

Use the following examples as reference implementations for:

- feature structure
- payload naming
- numbering conventions
- README structure
- dependency setup patterns

Do not use canonical examples as authority for:

- payload structure
- property names
- field types
- array names
- required attributes

OpenAPI specifications always take precedence.

Examples:
- TMFC005
- TMFC007
- TMFC028

located under:

skills/write-component-conformance-bdd/reference/examples/

---

### Generation Workflow

Generation must follow:

Component Specification
→ OpenAPI Resolution
→ Full $ref Resolution
→ Dependency Discovery
→ Payload Generation
→ Payload Schema Validation
→ Feature Generation
→ Feature Consistency Validation
→ README Generation
→ Final Validation

---

## Guiding Principles

1. Reuse existing CTK patterns.
2. Generate deterministic outputs.
3. Prefer version-tolerant payloads.
4. Use mandatory dependent APIs only.
5. Maintain compatibility with existing CTK execution logic.
6. Follow documented examples before introducing new patterns.