# Replay hierarchical imitation agent v1 (M30)

## Purpose

Define the **offline**, **replay-derived**, **two-level** learned hierarchical imitation agent artifact for STARLAB Phase V. This milestone instantiates the **M29** hierarchical agent interface trace schema (`starlab.hierarchical_agent_interface_trace.v1`) with a **deterministic** manager (signature → delegate) and worker ((delegate, signature) → coarse semantic label) fit from governed training data.

## Non-claims

This contract does **not** assert:

- benchmark integrity or leaderboard validity
- live StarCraft II execution
- raw SC2 action legality or action masks
- replay↔execution equivalence
- hierarchical policy optimality beyond majority tables
- M31 replay explorer or flagship proof-pack semantics

Agreement metrics in the companion report are **internal smoke only**, not benchmark claims.

## Inputs

- One governed **M26** `replay_training_dataset.json` (`dataset_version` = `starlab.replay_training_dataset.v1`)
- Referenced **M14** bundle directories (manifest / lineage / contents + primary JSON artifacts)
- Observation materialization via the existing **M16 → M18** in-process seam (`starlab.imitation.replay_observation_materialization`)
- Bounded context signatures via **M27** feature policy `starlab.m27.feature.observation_signature_v1`

## Delegate policy

- **Policy id:** `starlab.m30.delegate.fixed_four_v1` (checked-in mapping; not learned from data)
- **Delegates (exactly four):** `combat`, `economy`, `information`, `production`
- **Coarse labels** (`starlab.m26.label.coarse_action_v1`) map to delegates as implemented in `starlab.hierarchy.delegate_policy`

## Primary artifacts

| File | Role |
|------|------|
| `replay_hierarchical_imitation_agent.json` | Frozen agent: signature tables, fallbacks, policy ids, non-claims |
| `replay_hierarchical_imitation_agent_report.json` | Counts, split agreement metrics (smoke), governed asset class notes |

## Trace linkage

Emitted hierarchical decision traces use `schema_version` = `starlab.hierarchical_agent_interface_trace.v1` and validate against the **M29** JSON Schema emitted as `hierarchical_agent_interface_schema.json`.

## Import discipline

M30 product modules under `starlab/hierarchy/` listed for this milestone must **not** import `starlab.replays`, `starlab.sc2`, or `s2protocol`.

## CLI

```bash
python -m starlab.hierarchy.emit_replay_hierarchical_imitation_agent \
  --dataset path/to/replay_training_dataset.json \
  --bundle path/to/m14_bundle_dir \
  --output-dir path/to/out
```
