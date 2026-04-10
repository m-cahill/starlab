# Hierarchical agent interface — v1 (M29)

## Purpose

This contract defines the **first governed, deterministic, offline** interface for a **two-level** StarCraft II research hierarchy in STARLAB:

1. A **manager** selects exactly one **delegate** (worker) from a bounded catalog for one **frame-scoped** decision point.
2. A **worker** returns a **bounded semantic decision** expressed in the **coarse semantic label** space (see below).

**M29** is **contract-first**: it specifies JSON shapes and validation rules only. **M30** is the first milestone allowed to instantiate a **learned** hierarchical agent against this interface.

## Scope (v1)

- **Exactly two levels**: one manager decision, one worker response per trace.
- **Offline only**: no live SC2 execution, no runtime action legality, no action masks.
- **Frame-scoped**: one hierarchical decision per replay-derived **decision point** identified by `frame_ref` (bundle identity + lineage + gameloop + perspective player).
- **No training** in M29: no policy fitting, no dataset materialization from this contract alone.
- **No benchmark semantics**: this contract does not define leaderboard, tournament, or evaluation harness behavior.
- **Worker output** terminates in the **M29-owned JSON Schema enum** of coarse semantic labels, explicitly aligned **1:1** with the existing **`starlab.m26.label.coarse_action_v1`** vocabulary (`target_semantic_kind` in M26/M27/M28). The field **`label_policy_id`** on `worker_response` must be **`starlab.m26.label.coarse_action_v1`** so the policy family is visible without coupling validation to a particular M27 artifact file.

## Non-claims

- Not a learned hierarchical policy (that is **M30+**).
- Not benchmark integrity, not replay↔execution equivalence.
- Not raw SC2 actions or Blizzard API legality.
- Not multi-worker routing beyond selecting **one** delegate in v1.
- Not more than two hierarchy levels.

## Artifacts

| Artifact | Role |
| -------- | ---- |
| `hierarchical_agent_interface_schema.json` | JSON Schema (draft 2020-12) for a **trace document** with root `schema_version` + `hierarchical_decision_trace`. |
| `hierarchical_agent_interface_schema_report.json` | Deterministic report: schema hash, coarse label enum listing, `label_policy_id` anchor, non-claims, optional example fixture hashes. |

**Schema version string:** `starlab.hierarchical_agent_interface_schema.v1`  
**Report version string:** `starlab.hierarchical_agent_interface_schema_report.v1`  
**Trace document `schema_version`:** `starlab.hierarchical_agent_interface_trace.v1`

## CLI

```bash
python -m starlab.hierarchy.emit_hierarchical_agent_interface --output-dir OUT
```

Optional repeated `--example-fixture LABEL=PATH` records SHA-256 of example JSON files in the report.

## Product modules (M29)

- `starlab/hierarchy/hierarchical_interface_models.py` — constants and coarse label enum (aligned to M26 policy).
- `starlab/hierarchy/hierarchical_interface_schema.py` — JSON Schema builder + validation helpers.
- `starlab/hierarchy/hierarchical_interface_io.py` — schema/report emission.
- `starlab/hierarchy/emit_hierarchical_agent_interface.py` — CLI.

**Import discipline:** M29 product modules must not import `starlab.replays`, `starlab.sc2`, or `s2protocol` (AST-tested).
