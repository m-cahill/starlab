# Replay imitation baseline contract (v1) — M27

## Purpose

M27 defines the **first deterministic, offline, replay-derived imitation baseline artifact** over the governed **M26** `replay_training_dataset.v1` contract and referenced **M14** replay bundle directories. It trains a **transparent, auditable** baseline model and emits a compact report. It does **not** prove benchmark integrity, leaderboard validity, live SC2 execution, replay parser execution inside M27 modules, replay↔execution equivalence, hierarchical control, **M28** learned-agent evaluation harness semantics, or imitation quality beyond bounded internal fit smoke signals.

**Artifact version:** `starlab.replay_imitation_baseline.v1`  
**Report version:** `starlab.replay_imitation_baseline_report.v1`

## Required inputs

### M26 training dataset

- Must be `starlab.replay_training_dataset.v1`.
- Must carry a stable `dataset_sha256` consistent with canonical JSON hashing rules (M26).
- Must use governed M26 split and label policies (`split_policy_id`, `label_policy_id`).
- Examples must reference only **supplied** governed M14 bundle identities (`bundle_id`, `lineage_root`).

### M14 replay bundles

- Each referenced bundle must be a **complete governed M14** directory: `replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json`, primary M09–M13 JSON, hash verification per M14.
- Bundle `bundle_id` / `lineage_root` must match each example’s `observation_request`.
- Bundles must be sufficient to resolve each example’s `gameloop` and `perspective_player_index` through the **M16 → M18** in-process pipelines (no raw replay bytes, no `replay_raw_parse.json` in M27 product modules).

## Observation materialization (governed path)

M27 **does not** shell out to `emit_canonical_state` or `emit_observation_surface`. It composes:

1. **M16** — `materialize_canonical_state` from `starlab.state.canonical_state_pipeline` over `load_m14_bundle`.
2. **M18** — `materialize_observation_surface` from `starlab.observation.observation_surface_pipeline` over the resulting `canonical_state` + optional `canonical_state_report`.

The small seam `starlab.imitation.replay_observation_materialization` centralizes this path for reuse (e.g. future evaluation milestones).

## Model family

**`starlab.m27.model.observation_signature_majority_v1`**

- Materialize one governed observation instance per M26 example (per `observation_request`).
- Project each observation + canonical state frame into a **bounded context signature** (`feature_policy_id` below).
- On the **training** split only, aggregate counts of `target_semantic_kind` (coarse label) per signature.
- Predict the **majority label** per signature; ties break **lexicographically** by label string.
- If a signature is unseen at inference time, predict the **global majority** label over all **training** labels (same lexicographic tie-break among ties for max count).

## Feature policy

**`starlab.m27.feature.observation_signature_v1`**

Deterministic, bucketed projection (no raw tensors, no high-dimensional arrays):

| Component | Source |
| --------- | ------ |
| `perspective_race` | M18 scalar `race.actual` (normalized lowercase) |
| `opponent_race` | First other player’s `race_actual` in M16 `canonical_state.players` (normalized lowercase), else `unknown` |
| `game_phase_bucket` | Derived from `gameloop`: `very_early` / `early` / `mid` / `late` / `very_late` |
| `supply_used_bucket` | Proxy: `economy.unit_train_events_total` + `economy.structure_train_events_total` from M18 scalars, bucketed |
| `worker_count_bucket` | M16 `army_unit_category_counts.worker` if present, else 0, bucketed |
| `army_count_bucket` | Sum of M18 **self** `entity_rows` counts, bucketed |
| `base_count_bucket` | M16 `economy_summary.structure_train_events_total`, bucketed |
| `visible_enemy_presence_bucket` | Sum of M18 **enemy** `entity_rows` counts, bucketed to none/low/medium/high |
| `upgrade_progress_presence` | `yes` / `no` from M16 `production_summary.tech_upgrades_started_total` |

The **context signature** is the sorted join `key=value` pairs joined by `|`, using the keys above (lexicographic key order).

## Outputs

### `replay_imitation_baseline.json`

Minimal fields:

- `baseline_version`
- `baseline_sha256` — SHA-256 (hex) of the canonical JSON object **without** `baseline_sha256` (same pattern as other hashed STARLAB artifacts)
- `training_dataset_sha256`
- `model_family`
- `feature_policy_id`
- `label_policy_id` (copied from dataset, e.g. M26 coarse label policy)
- `fallback_label`
- `label_vocabulary` — sorted unique labels across all examples
- `signature_table` — deterministic list of rows, lexicographically sorted by `context_signature`:
  - `context_signature`
  - `predicted_label`
  - `training_support`
  - `support_by_label` — object with lexicographically sorted keys
- `warnings` — sorted unique strings (materialization + dataset warnings)
- `non_claims` — sorted (M27 product non-claims)

### `replay_imitation_baseline_report.json`

Minimal fields:

- `report_version`
- `baseline_sha256`
- `training_example_count`, `validation_example_count`, `test_example_count`
- `label_counts` — sorted keys
- `signature_count`
- `fallback_label`
- `agreement_by_split` — **internal smoke metrics only** (agreement rate vs labels on held splits); not benchmark claims
- `fallback_counts_by_split` — optional; counts of predictions that used global fallback (unseen signature)
- `warnings`, `non_claims`

## Deterministic rules

- Canonical JSON emission (`sort_keys=True`, stable indentation as in `starlab.runs.json_util.canonical_json_dumps`).
- Lexicographic sort for `warnings`, `non_claims`, `label_vocabulary`, `signature_table` order, `support_by_label` keys.
- Deterministic feature projection and signature derivation.
- Lexicographic majority tie-break for labels.
- No timestamps in artifacts unless a future milestone adds them under a separate policy.

## Explicit non-claims (reporting posture)

- Not benchmark integrity or leaderboard validity.
- Not live SC2 or new live execution proof in CI.
- Not replay parser execution **inside** M27 `starlab/imitation/` modules (`starlab.replays`, `starlab.sc2`, `s2protocol` are forbidden imports there).
- Not replay↔execution equivalence.
- Not hierarchical control or **M28** learned-agent evaluation harness product code.
- Not **M29+** scope.
- Not a proof of imitation quality beyond bounded internal agreement smoke metrics.

## CLI

```text
python -m starlab.imitation.emit_replay_imitation_baseline \
  --dataset PATH \
  --bundle PATH \
  --bundle PATH \
  --output-dir OUT
```

Repeat `--bundle` for each governed M14 bundle directory referenced by the dataset.
