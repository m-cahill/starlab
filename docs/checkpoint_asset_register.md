# Checkpoint asset register (v1.5)

**Milestone:** `V15-M01` — public register surface only (introduced in M01). **V15-M03** adds the separate `starlab.v15.checkpoint_lineage_manifest.v1` **metadata** contract; it does **not** add rows to this table by itself.

## Purpose

Track **checkpoints** (training saves, including optional optimizer state) that anchor evaluation, promotion, or XAI binds. **V15-M03** defines the `starlab.v15.checkpoint_lineage_manifest.v1` **metadata** contract and receipt shapes (no real weight blobs in CI); that manifest is **not** a substitute for adding **reviewed** public rows here. This register is the **inventory posture** for M01+.

## Scope

- `asset_class`: `checkpoint`.
- Pairs with `starlab.v15.checkpoint_lineage_manifest.v1` (V15-M03) for lineage discipline; the manifest still does **not** require registering real checkpoint blobs in this public table.

## Public / private boundary

Checkpoints default to **local_out** or **external_archive**. Public rows: identifiers + hashes + governing milestone references only.

## Required fields (per row)

See `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md` and `v15_training_asset_registers.json`.

## Current status

**M01:** Surface only; **no** long-run checkpoint lineage claimed. **V15-M03** is **closed** on `main` ([PR #120](https://github.com/m-cahill/starlab/pull/120)) with the `starlab.v15.checkpoint_lineage_manifest.v1` **metadata** contract; this table still has **no** new public **claim** rows (non-claims unchanged—see `docs/runtime/v15_checkpoint_lineage_resume_discipline_v1.md`). **M05 (closed on `main`, [PR #125](https://github.com/m-cahill/starlab/pull/125))** may **reference** checkpoint ids / lineage manifest SHA in the **strong-agent benchmark protocol** (`starlab.v15.strong_agent_scorecard.v1`); M05 does **not** evaluate or promote any checkpoint and does **not** add rows here. **V15-M07** is **closed** on `main` ([PR #129](https://github.com/m-cahill/starlab/pull/129)); it may emit **short** shakedown **checkpoint receipts** in operator-local runs; public row addition is **deferred** unless reviewed. **V15-M08** implementation surface **closed** on `main` ([PR #133](https://github.com/m-cahill/starlab/pull/133)); may add **candidate** checkpoint lineage evidence **locally** only when an operator runs a campaign; public register rows (id/hash, `pending_review`) only after explicit review. **V15-M09** is **closed** on `main` ([PR #135](https://github.com/m-cahill/starlab/pull/135)); defines evaluation/promotion surfaces; **no** checkpoint promoted and **no** public rows added on the default honest path — see **`docs/runtime/v15_checkpoint_evaluation_promotion_v1.md`**. **V15-M10** is **closed** on `main` ([PR #136](https://github.com/m-cahill/starlab/pull/136)) — binds promotion/XAI JSON by SHA for the demonstration surface only; **no** new public **rows** in this table on the default path. **V15-M11** (implementation) adds human-panel **execution** / claim-decision JSON that may **bind** M09 by SHA; **not** a promoted checkpoint in the public default and **not** a new public **row** in this table by default (see **`docs/runtime/v15_human_panel_bounded_benchmark_v1.md`**).

## Current registered assets

| asset_id | asset_class | asset_name | claim_use | review_status | notes |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | *No rows.* |

## Non-claims

M01 did **not** implement resume, rollback testing, or parent/child lineage automation. **V15-M03** defines **metadata-only** lineage and resume/rollback **receipt shapes**; it still does **not** execute trainer resume, does **not** execute rollback, and does **not** verify checkpoint bytes by default—see `docs/runtime/v15_checkpoint_lineage_resume_discipline_v1.md`.
