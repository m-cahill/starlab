# Replay↔execution equivalence audit & acceptance gates v1 (M54)

**Contract id:** `starlab.replay_execution_equivalence_audit.v1`  
**Milestone:** **M54** — *bounded audit over M53 evidence* — **not** universal replay↔execution equivalence — see `docs/starlab.md`, §11.

**Evidence input:** `starlab.replay_execution_equivalence_evidence.v1` (`docs/runtime/replay_execution_equivalence_evidence_surface_v1.md`).  
**Charter:** `starlab.replay_execution_equivalence_charter.v1` (`docs/runtime/replay_execution_equivalence_charter_v1.md`).

## Purpose

Emit machine-readable **audit** (`replay_execution_equivalence_audit.json` + deterministic `replay_execution_equivalence_audit_report.json`) by **consuming** existing M53 evidence JSON — **not** by rediscovering or recomputing evidence from raw run artifacts.

M54 adds **profile-scoped** acceptance predicates, explicit **gate results**, and descriptive **merge-bar language** fields — **not** GitHub branch-protection automation.

## What M54 audits

- Deterministic **audit** + **report** JSON for a **named gate pack** selected from the evidence `profile_id`.
- **Canonical SHA-256** of the loaded evidence object (`input_evidence_sha256`) — hash of **canonical JSON serialization**, not raw file bytes.
- Optional cross-check against `replay_execution_equivalence_evidence_report.json` when `--evidence-report` is supplied (`evidence_canonical_sha256` must match).
- **Gate pack** `starlab.m54.gatepack.identity_binding_acceptance_v1` for profile `starlab.m53.profile.identity_binding_v1` — predicate-level `gate_results` with statuses `pass` | `fail` | `not_evaluable` | `not_applicable`.
- Top-level **profile_scope_status**: `accepted_within_profile_scope` | `rejected_within_profile_scope` | `not_evaluable`.
- **merge_bar_language**: `would_clear_profile_scope_gate` | `would_block_profile_scope_gate` | `no_profile_scope_decision` (descriptive only).

## What M54 does not mean

- **Not** a proof of **global** replay↔execution equivalence.
- **Not** benchmark integrity, live SC2 in CI, or ladder/public performance claims.
- **Not** replacement for M53 evidence emission; M53 remains the evidence producer, M54 the interpretation layer.
- **Not** repository merge enforcement; `merge_bar_language` is **not** branch protection.

## Relationship to M52 and M53

| Milestone | Role |
| --- | --- |
| **M52** | Charter + mismatch taxonomy + non-claims (contract only). |
| **M53** | Deterministic **evidence** JSON + report for bounded profiles (no audit verdict). |
| **M54** | Deterministic **audit** JSON + report over M53 evidence; first **acceptance gate** pack for `identity_binding_v1`. |

## CLI

```text
python -m starlab.equivalence.emit_replay_execution_equivalence_audit \
  --evidence <path> \
  --output-dir <dir> \
  [--evidence-report <path>]
```

Emits `replay_execution_equivalence_audit.json` and `replay_execution_equivalence_audit_report.json` deterministically (sorted keys, stable UTF-8).

Unknown `profile_id` (no registered M54 gate pack) ⇒ `not_evaluable` at the audit layer.

## M55 boundary

Benchmark integrity charter and evidence gates belong to **M55+**, not this audit surface.
