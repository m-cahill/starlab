# Replay training dataset contract (v1) — M26

## Purpose

M26 defines a **deterministic, offline, replay-derived training-dataset contract** that packages **governed imitation-training examples** as stable references over **already-governed M14 replay bundle artifacts**. It does **not** train a model, prove imitation quality, or extend benchmark-integrity or replay↔execution equivalence claims.

**Artifact version:** `starlab.replay_training_dataset.v1`  
**Report version:** `starlab.replay_training_dataset_report.v1`

## Upstream posture

- One or more **governed M14 replay bundle** directories, each containing `replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json`, and the required M09–M13 primary JSON (plus optional `*_report.json` companions).
- Lineage and `artifact_hashes` in the manifest must match **canonical JSON hashes** of the files on disk (same rule as M14 bundle generation).
- Optional `replay_intake_receipt.json` in the bundle directory: if **absent**, inclusion is allowed and a **`intake_provenance_absent`** warning is recorded; if **present** and `intake_status` is `quarantined` or `rejected`, inclusion **fails hard**.
- No raw replay bytes, no `replay_raw_parse.json`, and no replay parser execution in M26 product modules.

## Outputs

- `replay_training_dataset.json`
- `replay_training_dataset_report.json`

Emission is **canonical JSON** (sorted keys, stable formatting) as elsewhere in STARLAB.

### Dataset identity

`dataset_sha256` is the SHA-256 (hex) of the canonical JSON object **without** the `dataset_sha256` field (same pattern as other STARLAB hashed artifacts).

### Selection policy

`selection_policy_id`: `starlab.m26.selection.timeline_entries_v1`

One training example is emitted per **eligible** `replay_timeline.json` entry:

- `semantic_kind` and `source_stream` are present.
- `gameloop` and `timeline_index` are integers.
- A **perspective player index** is resolved from `player_index`, or from `payload.m_controlPlayerId` (1-based → 0-based by subtracting one when ≥ 1).

### Label policy (coarse, non-claiming)

`label_policy_id`: `starlab.m26.label.coarse_action_v1`

Labels are drawn from a **small coarse action-type vocabulary**, not raw M10 `semantic_kind` strings. If mapping is not conservative and deterministic, the label is **`other`**. Labels do **not** assert legality, executability, or full action-space fidelity.

Approved values: `economy_expand`, `economy_worker`, `production_unit`, `production_structure`, `research_upgrade`, `army_move`, `army_attack`, `scout`, `other`.

Illustrative mapping (implementation may use a subset if fixtures warrant):

| Upstream signal | Coarse label |
| --- | --- |
| `upgrade_completed` | `research_upgrade` |
| `unit_born` | `production_unit` |
| `unit_init` | `production_structure` |
| `unit_type_changed` | `economy_expand` |
| `command_issued` (game stream) | `army_move` |
| `ping_event` | `scout` |
| Other / unmapped | `other` |

### Split policy

`split_policy_id`: `starlab.m26.split.sha256_mod100_v1`

For each `example_id` string:

1. Compute `digest = SHA-256(example_id)` (UTF-8 bytes).
2. Let `bucket = int.from_bytes(digest[:8], byteorder="big", signed=False) % 100`.
3. Assign:
   - `0–79` → `train`
   - `80–89` → `validation`
   - `90–99` → `test`

This yields an **80 / 10 / 10** split, deterministic and independent of bundle input order.

### Example identity

Each row has a unique `example_id`:

`starlab.m26.example.v1:{lineage_root}:{bundle_id}:{perspective_player_index}:{gameloop}:{timeline_index}:{target_semantic_kind}`

Duplicate `example_id` values are a hard error.

### Example ordering

`examples[]` is sorted lexicographically by:

`lineage_root`, `bundle_id`, `perspective_player_index`, `gameloop`, `timeline_index`, `target_semantic_kind`, `example_id`.

### Warnings and non-claims

- `warnings[]` and `non_claims[]` are **sorted lexicographically**.
- Report `non_claims[]` mirrors the dataset’s explicit non-claims (e.g. not model training, not imitation quality, not benchmark integrity, not replay↔execution equivalence, not live SC2, not M27 imitation-baseline training).

## CLI

```bash
python -m starlab.imitation.emit_replay_training_dataset --bundle PATH --bundle PATH --output-dir OUT
```

Each `--bundle` directory must satisfy the M14 bundle layout described above.

## Explicit non-claims

- Not model training or learned-agent capability.
- Not imitation quality or behavioral cloning performance.
- Not benchmark integrity or leaderboard validity.
- Not replay↔execution equivalence.
- Not full action legality or SC2 action-space coverage.
- Not live SC2 or parser certification.
- Not raw replay packaging.
- Not M27 imitation-baseline training product code.
