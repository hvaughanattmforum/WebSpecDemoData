# Generated Feature Examples

This document provides examples of generated Component Conformance BDD feature files.

---
Canonical feature examples:

skills/write-component-conformance-bdd/reference/examples/TMFC005
skills/write-component-conformance-bdd/reference/examples/TMFC007
skills/write-component-conformance-bdd/reference/examples/TMFC028

---

# Example: Multiple Mandatory Dependent APIs

Rule:

For each dependent API:

- Generate one success scenario
- Generate one failure scenario

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

# Feature Generation Principles

1. One feature file per component.
2. One scenario outline per component.
3. One success row per dependency.
4. One failure row per dependency.
5. Reuse existing CTK step definitions.
6. Do not generate JavaScript step definitions.