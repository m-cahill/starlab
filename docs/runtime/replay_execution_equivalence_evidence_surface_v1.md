# Replay↔execution equivalence evidence surface v1 (M53)

**Contract id:** `starlab.replay_execution_equivalence_evidence.v1`  
**Milestone:** **M53** — *bounded evidence artifacts only* — **not** paired universal equivalence — **not** M54 audit gates.  
**Charter:** `starlab.replay_execution_equivalence_charter.v1` (`docs/runtime/replay_execution_equivalence_charter_v1.md`).  
**See also:** public ledger `docs/starlab.md` (Phase VII profile table, v1 non-claims).

## Purpose

Emit machine-readable **evidence** (`replay_execution_equivalence_evidence.json` + deterministic `replay_execution_equivalence_evidence_report.json`) for **named comparison profiles** that compare **governed** replay-side and execution-side artifacts using **stable join keys** only — **no** filename-only pairing, **no** `passed` / `merge_ready` verdict, **no** M54 acceptance semantics.

## What M53 proves

- Deterministic **evidence** + **report** JSON for a registered **bounded profile** (see `starlab.equivalence.equivalence_profiles`).
- Explicit **pairing_inputs** (explicit artifact paths), **join_key_projection**, **evidence_entries**, **availability_summary**, **mismatch_summary** (M52 vocabulary), and **non_claims**.

## What M53 does not prove

- **Replay↔execution equivalence** as a global or gameplay-semantic theorem.
- **Benchmark integrity**, **live SC2 in CI**, **ladder / public performance**.
- Parser correctness beyond upstream milestones; **M19**-style cross-mode reconciliation is a different family.

## Implemented profile: `starlab.m53.profile.identity_binding_v1`

**Inputs (CLI):** explicit paths to `run_identity.json`, `lineage_seed.json`, `replay_binding.json` — **not** directory discovery.

**Compared:** join keys (`run_spec_id`, `execution_id`, `proof_artifact_hash`, `lineage_seed_id`), `config_hash` agreement between run identity and lineage seed, `replay_binding_id` recomputation, `parent_references` sequence equality, schema-version tokens, **`replay_content_sha256`** on the replay-binding side with execution-side **unavailable_by_design** (M03 does not store opaque replay bytes). **Out of scope** row for gameplay/parser/timeline semantics.

## CLI

```text
python -m starlab.equivalence.emit_replay_execution_equivalence_evidence \
  --profile starlab.m53.profile.identity_binding_v1 \
  --output-dir <dir> \
  --run-identity <path> \
  --lineage-seed <path> \
  --replay-binding <path>
```

Emits `replay_execution_equivalence_evidence.json` and `replay_execution_equivalence_evidence_report.json` deterministically (sorted keys, stable UTF-8).

## M54 boundary

Audit vocabulary, acceptance gates, and merge-bar language **belong to M54**, not this surface.
