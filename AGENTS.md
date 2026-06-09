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

### BDD Artefacts

Generate BDD artefacts only under:

specifications/TMFCxxx-*/BDD/

### Runtime Compatibility

Generated artefacts must comply with:

skills/write-component-conformance-bdd/reference/componentTests-contract.md

### Generation Guidance

Before generating new artefacts consult:

1. SKILL.md
2. generation-decision-tree.md
3. componentTests-contract.md
4. Canonical examples

### Canonical Examples

Use the following examples as the primary reference patterns:

- TMFC005
- TMFC007
- TMFC028

located under:

skills/write-component-conformance-bdd/reference/examples/

---

## Guiding Principles

1. Reuse existing CTK patterns.
2. Generate deterministic outputs.
3. Prefer version-tolerant payloads.
4. Use mandatory dependent APIs only.
5. Maintain compatibility with existing CTK execution logic.
6. Follow documented examples before introducing new patterns.