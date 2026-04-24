# Checkpoint asset register (v1.5)

**Milestone:** `V15-M01` — public register surface only.

## Purpose

Track **checkpoints** (training saves, including optional optimizer state) that anchor evaluation, promotion, or XAI binds. Lineage and resume **runtime** are **V15-M03**; this register is the **inventory posture** for M01.

## Scope

- `asset_class`: `checkpoint`.
- Pairs with future `starlab.v15.checkpoint_lineage_manifest.v1` (not implemented in M01).

## Public / private boundary

Checkpoints default to **local_out** or **external_archive**. Public rows: identifiers + hashes + governing milestone references only.

## Required fields (per row)

See `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md` and `v15_training_asset_registers.json`.

## Current status

**M01:** Surface only; **no** long-run checkpoint lineage claimed.

## Current registered assets

| asset_id | asset_class | asset_name | claim_use | review_status | notes |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | *No rows.* |

## Non-claims

M01 does **not** implement resume, rollback testing, or parent/child lineage automation.
