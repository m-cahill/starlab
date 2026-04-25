# Training asset register (v1.5)

**Milestone:** `V15-M01` — public register surface only (no claim-critical rows in-repo).

## Purpose

Track **training datasets** and derived training artifacts (indices, shards, feature caches) used or proposed for v1.5-scale training with explicit rights, storage, and claim posture.

## Scope

- `asset_class`: `training_dataset`, `label_set`, and related rows that feed the trainer (not raw replay corpora — see `docs/replay_corpus_register.md`).
- Excludes execution of training; excludes environment lock (V15-M02).

## Public / private boundary

Public doc holds **template** rows only. Raw datasets, local paths, and uncleared third-party material stay **private** or **local_only**.

## Required fields (per row)

See `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md` and `v15_training_asset_registers.json` (`required_fields`).

## Current status

**M01:** Register surface defined; **no** production training dataset registered publicly. **V15-M07** **fixture** uses **synthetic** / **fixture** data only; **operator-local** shakedown manifests remain **private** / **local** by default.

## Current registered assets

| asset_id | asset_class | asset_name | claim_use | review_status | notes |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | *No rows; populate only after explicit review and cleared rights posture.* |

## Non-claims

Listing a row in a future revision does **not** assert benchmark integrity, replay↔execution equivalence, or readiness for long GPU claims until gates and reviews say so.
