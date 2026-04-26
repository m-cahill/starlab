# XAI evidence register (v1.5)

**Milestone:** `V15-M01` — public register surface only.

## Purpose

Inventory **XAI evidence** artifacts (explanation packs, traces, reports) bound to replays and checkpoints for v1.5 demonstration narratives.

## Scope

- `asset_class`: `xai_evidence` (and related `video_or_media` when tied to explanation deliverables).
- **V15-M04** freezes the **XAI evidence contract** (`starlab.v15.xai_evidence_pack.v1`) and fixture emitters — it does **not** register real operator XAI packs in this public table. M01 did **not** freeze the contract.

## Public / private boundary

Public register remains **template-only** in M01. Operator-local packs stay **private** until reviewed; sanitized summaries may be referenced when rights allow.

## Required fields (per row)

See `docs/runtime/v15_training_scale_provenance_asset_registers_v1.md` and `v15_training_asset_registers.json`.

## Current status

**M01:** Surface only; **no** XAI demo completion claimed.

**M04 (closed):** Contract `starlab.v15.xai_evidence_pack.v1` and fixture emitter are on `main`; this table remains **no real rows** — M04 does **not** register operator XAI packs for claim-critical use. **M05 (closed on `main`, [PR #125](https://github.com/m-cahill/starlab/pull/125))** may cite **XAI trace coverage** as a **future scorecard / protocol** requirement; M05 does **not** execute XAI **review** and does **not** add rows. **V15-M10** is **closed** on `main` ([PR #136](https://github.com/m-cahill/starlab/pull/136)) — `starlab.v15.replay_native_xai_demonstration.v1` and **`docs/runtime/v15_replay_native_xai_demonstration_v1.md`** add the **replay-native XAI demonstration/report** surface and deterministic Markdown; default path is **contract / report validation** and **no** new **claim-critical** public table rows; **not** real inference, **not** faithfulness proof; **no** raw XAI media, saliency tensors, or private paths committed by this governance surface. **V15-M11** (implementation) may **bind** M10 JSON by **SHA** for human-panel **H10** gate wiring only; **not** a new public XAI **row** on the default path.

## Current registered assets

| asset_id | asset_class | asset_name | claim_use | review_status | notes |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | *No rows.* |

## Non-claims

XAI artifacts are **governed explanation packs**, not proofs of causal human-like reasoning; see `docs/starlab-v1.5.md`.
