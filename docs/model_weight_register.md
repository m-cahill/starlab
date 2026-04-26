# Model weight register (v1.5)

**Milestone:** `V15-M01` — public register surface only.

## Purpose

Record **model weights** and exported parameter blobs used in v1.5 narrative (training candidates, baselines, promotion targets) with content hashes and storage posture.

## Scope

- `asset_class`: `model_weight`.
- Large binaries are **not** committed; public rows use **hash references** and governing docs only.

## Public / private boundary

Default **private** / **local_only** storage. Public table may list **sanitized** references (hash, contract id, milestone) — never raw paths that leak operator layout unless intentionally public.

## Required fields (per row)

See `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md` and `v15_training_asset_registers.json`.

## Current status

**M01:** Surface only; **no** promoted showcase weights registered publicly. **V15-M07** is **closed** on `main` ([PR #129](https://github.com/m-cahill/starlab/pull/129)); it may still produce **operator-local** shakedown weights/checkpoints under `out/` when run by an operator; the public register remains **no** real **claim-critical** **rows** unless explicitly reviewed and approved. **V15-M08** implementation surface **closed** on `main` ([PR #133](https://github.com/m-cahill/starlab/pull/133)); **`implementation_ready_waiting_for_operator_run`**. May produce **candidate** weight hashes **locally** only when an operator runs training; public rows (sanitized hash only, `pending_review`) require explicit approval — default remains **no rows**. **V15-M09** is **closed** on `main` ([PR #135](https://github.com/m-cahill/starlab/pull/135)); adds checkpoint evaluation / promotion **governance** only; **no** new public model-weight **rows** by default. **V15-M10** is **closed** on `main` ([PR #136](https://github.com/m-cahill/starlab/pull/136)) — replay-native XAI **demonstration** metadata; does **not** add weight or checkpoint-blob **rows** on the default path. **V15-M11** (implementation) is an execution / **claim-decision** metadata surface; **not** a training-asset or weight-blob **claim**; default remains **no** new public **rows**.

## Current registered assets

| asset_id | asset_class | asset_name | claim_use | review_status | notes |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | *No rows.* |

## Non-claims

A hash in this register does **not** assert strength, benchmark passage, or claim-critical approval until evaluation milestones record evidence under frozen protocols.
