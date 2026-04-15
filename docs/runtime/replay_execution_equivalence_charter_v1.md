# Replay↔execution equivalence charter v1 (M52)

**Contract id:** `starlab.replay_execution_equivalence_charter.v1`  
**Milestone:** **M52** — *charter and machine-readable boundary only* — **not** paired proof — **closed** on `main` (see `docs/starlab.md`, §18).  
**See also:** public ledger `docs/starlab.md` (Phase VII, v1 boundary, remaining proof-track map). **M53 evidence surface:** `docs/runtime/replay_execution_equivalence_evidence_surface_v1.md`.

## Purpose

Define a **bounded** claim surface for comparing **replay-derived** STARLAB artifacts with **execution-derived** artifacts (for example M02 `match_execution` proof JSON and derived run identity), without asserting that replays and executions are globally equivalent.

This document intentionally precedes **M53** (evidence surface) and **M54** (audit gates). **M52** establishes vocabulary, non-claims, and mismatch taxonomy alignment with emitted JSON.

## What M52 proves

- A **deterministic charter artifact** (`replay_execution_equivalence_charter.json`) and companion **report** (`replay_execution_equivalence_charter_report.json`) with explicit **non_claims**.
- Agreement between this markdown contract and the JSON **schema_version** / field names **where listed**.

## What M52 does not prove

- **No** statement that replay bytes semantically match live or harness execution for arbitrary games.
- **No** end-to-end certification of parser correctness beyond whatever upstream milestones already claim.
- **No** benchmark integrity, ladder performance, or match outcome semantics.
- **No** replacement for M19 cross-mode reconciliation (replay-derived canonical state vs observation).

## Bounded claim surface

1. **Profile-gated comparisons:** Future paired runs select a named **comparison profile** (versioned) that lists which artifact families participate (timeline slices, BOE rows, identity keys, execution proof fields, etc.).
2. **Stable join keys:** Pairing uses STARLAB-governed ids (`run_identity`, `lineage_seed`, `replay_content_sha256` binding, charter-declared slice ids) — never ad hoc filenames alone.
3. **Explicit handling of absence:** See **Availability classes** and **Mismatch taxonomy** in the JSON; “missing” may be **out_of_scope** or **unavailable_by_design**, not automatically **mismatch**.

## Upstream artifacts (typical)

- Replay side: M04 binding + governed replay parse / planes as required by the profile (M08–M14 chain).
- Execution side: M02 proof JSON, M03 identity/lineage where applicable.
- Optional: M16+ derived state only if the profile explicitly includes them.

## Comparison identity rules (summary)

- **Single pairing per profile instance:** if multiple candidates match join keys, emit **identity_mismatch** / governance failure — no silent choice.
- **Schema compatibility:** compared JSON must list compatible `schema_version` values for the profile.
- **Deterministic ordering:** where the charter requires ordered comparison, use lexicographic / stable sort keys defined by the profile spec in M53.

## Mismatch taxonomy (normative)

| Kind | Meaning |
|------|---------|
| `missing_counterpart` | Expected paired element missing on one side under the profile. |
| `identity_mismatch` | Join key collision or incompatible identity projection. |
| `ordering_mismatch` | Order-sensitive comparison failed under profile ordering rules. |
| `count_mismatch` | Cardinality or multiset counts differ where they must agree. |
| `bounded_semantic_divergence` | Values differ inside a chartered semantic partial-order (evidence, not necessarily a harness bug). |
| `unavailable_by_design` | Absence is allowed by contract on that side. |
| `out_of_scope` | Difference recorded but excluded from equivalence claims for this profile. |

## Future obligations (M53 / M54)

- **M53:** Deterministic **evidence** artifacts for bounded profiles; still **no** universal equivalence theorem.
- **M54:** **Audit** vocabulary + **acceptance gates** that map evidence to merge-bar language only when predicates pass; residual gaps remain explicit **non_claims**.

## CLI

```text
python -m starlab.equivalence.emit_replay_execution_equivalence_charter --output-dir <dir>
```

Emits `replay_execution_equivalence_charter.json` and `replay_execution_equivalence_charter_report.json` deterministically (sorted keys, stable UTF-8).
