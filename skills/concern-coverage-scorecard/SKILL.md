---
name: concern-coverage-scorecard
description: Reads any document describing an AI-agent or ODA-component governance artifact — a Kubernetes CRD YAML, a JSON Schema, or a Word/markdown specification like TMF444 or IG1412 — and scores it field-by-field against the twelve governance concerns (Model, Tool, Agent, Data, Registry, Gateways, Security, Performance, Observability, Lifecycle, Documentation, Ontology), then maps each finding onto the specific block it would bind into in the Component v2alpha1 unified schema. Use this whenever the user shares a new spec, CRD, or schema and asks how it covers governance concerns, where its gaps are, how "complete" or "mature" it is, how it compares to another spec, or how it would fit into a shared/unified schema — even if they don't say "scorecard" or name the twelve concerns explicitly. Also trigger on requests like "classify this schema", "what does this cover", or "where would this bind in".
---

# Concern Coverage Scorecard

Takes one document and answers one question, concern by concern: **does this
object actually govern this, or does it just gesture at it?** The output is a
twelve-row table — status, evidence, and which block of the unified schema
that evidence would slot into — plus one line naming what the document would
need to add before it could bind into that schema for real.

This isn't a checklist skill. The judgment call in every row — is this Strong,
Partial, or a Gap — is the actual work, and it only holds up if it's applied
the same way every time. The calibration below came from scoring eight very
different documents (five live Kubernetes CRDs, two documentation templates,
one CI-validation JSON Schema) against the same twelve concerns and finding
out, repeatedly, which judgment calls actually held up and which ones didn't.
Read it before scoring, not after.

## The twelve concerns

| # | Concern | What it actually asks |
|---|---|---|
| 1 | Model | Is a foundation model's identity, provider, and capabilities governed here? |
| 2 | Tool | Is an external function/MCP resource the thing calls governed here? |
| 3 | Agent | Is the calling agent's own identity, runtime, and hosting governed here? |
| 4 | Data | Is an external data/knowledge resource (RAG, vector store, data product) governed here? |
| 5 | Registry | Does this thing get published somewhere so it can be discovered? |
| 6 | Gateways | Is the wire-protocol/invocation surface (routing, discovery) governed here? |
| 7 | Security | Auth, guardrails, credentials, policy enforcement? |
| 8 | Performance | Metrics *targets* — SLAs, acceptance criteria, thresholds to hit? |
| 9 | Observability | Logging, tracing, health/audit signals — what you can *see* at runtime? |
| 10 | Lifecycle | Phase state machine, approval gates, retirement scheduling? |
| 11 | Documentation | Owners, maintainers, manuals, API-spec pointers? |
| 12 | Ontology | Standards-taxonomy alignment — skill IDs, spec lineage, semantic mapping? |

Performance and Observability look like one concern until you score enough
documents — some are strong on live telemetry (logging/metrics/tracing
config) and have nothing resembling an acceptance target, others are the
reverse (a `metrics[]` array of label/threshold pairs with no logging config
anywhere). Same split for Lifecycle and Documentation: a phase/approval state
machine and a pile of owner/manual fields are different kinds of maturity, and
a document is routinely strong on one and empty on the other.

## The target schema

`references/component-v2alpha1-schema.yaml` is the current Component v2alpha1
proposal — a Kubernetes CRD that gives each of the twelve concerns its own
named `<concern>Function` block (`modelFunction`, `toolFunction`,
`agentFunction`, `dataFunction`, `registryFunction`, `securityFunction`,
`performanceFunction`, `observabilityFunction`, `lifecycleFunction`), plus two
concerns that reuse an existing block because they already *are* that block
(`componentMetadata` = Documentation, `coreFunction` = Gateways) and one more
that got its own block once Documentation was narrowed (`ontologyFunction`).

**Read that file fresh every time you use this skill — don't rely on this
description or on memory for the block names.** This proposal is still
actively evolving; the file is the only thing that's authoritative. If the
user gives you a different or newer version of the schema, use that one
instead and say so.

If a field in the document you're scoring doesn't map cleanly onto *any*
existing block, that's a real finding, not a failure on your part — say so
explicitly in that row's evidence, and name it again in the closing line. Two
of the twelve concerns in this proposal (`registryFunction`, `dataFunction`)
were only added *because* an earlier document being scored this way had
fields that didn't fit anywhere else. The schema is supposed to keep
absorbing findings like that, not the other way around.

## Calibration: Strong vs. Partial vs. Gap

Getting this consistent across documents matters more than getting any single
row "right" — a scorecard where every row is Partial because you hedged is
useless for comparison. Use these tests in order; stop at the first one that
fits.

**Strong** — the document actually governs this, not just touches it:
- A required field, an enum-constrained state machine, or a validation rule
  (CEL, JSON Schema `required`, whatever the format supports) ties directly to
  this concern, *and*
- it's a complete-enough contract to act on: a full logging+metrics+tracing
  block counts, a bare `metrics: {type: object}` placeholder doesn't.

**Partial** — a real field exists, but one of these is true:
- It's a **cross-reference**, not ownership. `AgentConfig.modelRef` doesn't
  govern Model — it just names a model the agent depends on. Credit the
  awareness, don't credit ownership.
- It's a **single loosely-typed field or free-text string** with no
  enforcement behind it — a `status: string` with no enum, a `description`
  field that happens to mention something relevant.
- It's **mechanism with no policy, or policy with no mechanism** — a metrics
  *scrape endpoint* exists but nothing declares a target to hit (that's
  Observability-strong, Performance-gap, not both Partial); a
  `guardrails.required: true` flag with no enforcement engine behind it.

**Gap** — nothing addresses it, or the only thing present is an explicit
placeholder (`{"type": ["array", "object"]}`, an empty object with no
properties). A placeholder is a *clearer* Gap signal than pure absence — it
means the original author saw the concern and deliberately deferred it.

**Two things that are NOT weaknesses, so don't downgrade a rating over them:**
- An **open string pattern instead of a closed enum** (`provider: {type:
  string, pattern: "^[a-z][a-z0-9-]*$"}` rather than `enum: [aws, azure,
  gcp]`) is usually a deliberate "open contract" design letting the ecosystem
  add providers without a schema change. Score the concern on what the field
  *governs*, not on whether the vocabulary is closed.
- A concern that's **structurally absent by design** — a shared indirection
  object (like a Registry CRD) has no reason to carry Model/Tool/Agent fields
  of its own — is a Gap like any other, but say *why* in the evidence line
  ("none by design — it's the indirection layer, not a governed asset")
  instead of implying the document forgot something.

## Process

1. **Read the target schema** (`references/component-v2alpha1-schema.yaml`,
   or whatever the user supplied) and list its top-level `<concern>Function`
   blocks. This is your mapping target for step 3.
2. **Read the input document completely** before scoring anything. Partial
   reads produce confidently wrong Gaps — a field that answers a concern is
   often three sections away from where you'd expect it.
3. **Score all twelve concerns**, one row each: status (Strong/Partial/Gap),
   evidence (the actual field path(s), one line, cite exact names, not
   paraphrases), target block (which `<concern>Function` this evidence would
   move into, or "no clean match" if step 1's list has nothing that fits).
4. **Write the synthesis line** — not a summary of the table, a specific
   instruction: what's the single highest-value thing this document would
   need to add before it could bind into the target schema? Name the gap that
   matters most, not every gap.

## Output format

Open with one line identifying what was scored (document name, format, and
source if known — e.g. `AIGatewayConfig · Kubernetes CRD (draft) v1alpha1 ·
ai-canvas-architecture`), then the table, then the synthesis line:

```markdown
**<Document name>** — <format> · <version/source if known>

| Concern | Status | Evidence | Target block |
|---|---|---|---|
| Model | STRONG | `dependentAIModels[]`, `trafficSplitStrategy` | `modelFunction` |
| Tool | GAP | Needs a tool identity/registration surface — nothing here touches it | `toolFunction` |
| ... | ... | ... | ... |

**Strong: <n>/12**

**To bind in:** <one or two sentences — the single highest-value gap to close, not a restated list of every row.>
```

If a row's evidence spans multiple fields, cite all of them (`guardrails.*,
jwtAuth.*`) rather than picking one arbitrarily. If nothing in the document
addresses a concern for a structural reason (see calibration above), say so
in the evidence rather than leaving it terse ("Needs X").

## Worked example (abbreviated)

Scoring `AIGatewayConfig` (a real draft CRD from `ai-canvas-architecture`)
against this schema produced:

| Concern | Status | Evidence |
|---|---|---|
| Model | STRONG | `dependentAIModels[]`, `trafficSplitStrategy`, `gateway.shim.defaultModelOverride` |
| Security | PARTIAL | `guardrails.*`, `jwtAuth.*` declared, but no validation rule enforces them |
| Performance | GAP | `guardrails.{maxTokens, temperature}` are safety knobs, not performance targets |
| Observability | PARTIAL | `observability.{enabled, integrations[]}` — a real block, but entries are thin (name/host/auth only) |

Note the Security/Performance/Observability split: three different verdicts
for three closely-related concerns in the same document, because each test in
the calibration section landed differently for each one. That's the
signal this skill exists to surface — a single "governance maturity" score
would have erased exactly the distinction that mattered.
