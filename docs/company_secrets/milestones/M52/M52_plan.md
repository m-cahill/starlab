# M52 Plan — V1 Endgame Recharter & Replay↔Execution Equivalence Charter v1

**Status:** **Closed** on `main` ([PR #63](https://github.com/m-cahill/starlab/pull/63); merge commit `c80a47bedcc5e607e45381d401411d9aa5e2f10b`; tag **`v0.0.52-m52`**). Branch `m52-v1-endgame-recharter-replay-execution-charter` **deleted** after merge.  
**Phase:** VII — Trust, Equivalence, Benchmark Integrity, and Release Lock

## Milestone title

**M52 — V1 endgame recharter & replay↔execution equivalence charter v1**

## Why this milestone now

M51 completed the post-bootstrap orchestration surface and explicitly left the larger proof targets unresolved. The ledger had M52 as a placeholder only. This milestone locks the **remaining v1 arc**, revises the public ledger to match intent, and starts the first hard proof track with a **charter milestone** rather than jumping into broad implementation claims.

## Objective

1. **Recharter v1** from “governed substrate release” into the remaining **SC2 foundation-completion arc** (**M52**–**M61**).
2. Add the planned **M52**–**M61** milestones to `docs/starlab.md` (table, intent map, quick scan, changelog, v1/v2 boundary).
3. Deliver a bounded, deterministic **replay↔execution equivalence charter surface** with explicit non-claims, mismatch taxonomy, and future acceptance criteria — **not** the paired proof itself yet.

## Phase VII (preferred; locked)

**Phase VII — Trust, Equivalence, Benchmark Integrity, and Release Lock** — milestones **M52**–**M61**. Phase VI (**M40**–**M51**) remains the closed training/execution track.

## In scope

### 1. Recharter the public ledger (`docs/starlab.md`)

- Planned arc **62 milestones (M00–M61)**.
- Replace M52 stub posture with real M52 charter + Phase VII + **M53**–**M61** rows (M52 active; **M53**–**M61** stub/planned).
- Intent map entries **M52**–**M61**; quick scan; changelog; compact **remaining v1 proof-track map**; **v2 begins after M61** note.
- **Wording:** do **not** overclaim proof; preserve present-tense non-claims; say targets are **planned within the remaining v1 arc**.

### 2. M52–M61 roadmap (names locked)

| Milestone | Name |
| --------- | ---- |
| **M52** | V1 Endgame Recharter & Replay↔Execution Equivalence Charter v1 |
| **M53** | Replay↔Execution Equivalence Evidence Surface v1 |
| **M54** | Replay↔Execution Equivalence Audit & Acceptance Gates v1 |
| **M55** | Benchmark Integrity Charter & Split-Governance Controls v1 |
| **M56** | Benchmark Integrity Evidence & Reproducibility Gates v1 |
| **M57** | Narrow Live SC2 in CI Charter & Controlled Runner v1 |
| **M58** | Live SC2 in CI Hardening & Cost Guardrails v1 |
| **M59** | Ladder/Public Evaluation Protocol & Evidence Surface v1 |
| **M60** | Audit Hardening & v2 Readiness v1 |
| **M61** | SC2 Foundation Release Lock & v1 Proof Pack |

### 3. Charter surface (code + runtime doc)

- **`docs/runtime/replay_execution_equivalence_charter_v1.md`**
- **`starlab/equivalence/`** (small): `equivalence_models.py`, `equivalence_charter.py`, `emit_replay_execution_equivalence_charter.py`
- Emits: `replay_execution_equivalence_charter.json`, `replay_execution_equivalence_charter_report.json`
- CLI: `python -m starlab.equivalence.emit_replay_execution_equivalence_charter --output-dir <dir>`

### 4. Mismatch taxonomy (minimum)

`missing_counterpart`, `identity_mismatch`, `ordering_mismatch`, `count_mismatch`, `bounded_semantic_divergence`, `unavailable_by_design`, `out_of_scope`

### 5. Governance tests

Arc length, table rows, intent map, runtime doc on governance list, v1 boundary honesty, deterministic charter emission.

## Out of scope

No paired replay↔execution proof; no benchmark-integrity implementation; no live SC2 in CI; no ladder reporting; no Minecraft / AURORA; no broad unrelated audit; no v2 product work.

## Acceptance criteria

1. `docs/starlab.md` reflects arc through **M61**.
2. Ledger distinguishes **not proved today**, **planned in remaining v1**, **v2 after M61**.
3. Runtime charter doc exists.
4. Deterministic charter/report JSON surface exists.
5. Governance tests enforce table / intent / arc / honesty.
6. CI green without weakening checks.
7. No proof claims beyond charter scope.

## Suggested branch name

`m52-v1-endgame-recharter-replay-execution-charter`

## Closeout (when authorized)

Per `.cursorrules` and `docs/company_secrets/prompts/` (or canonical `docs/prompts/`): verify CI, summary, audit, tag, merge, seed **M53** folder.
