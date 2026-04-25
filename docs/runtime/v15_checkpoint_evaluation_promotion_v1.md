# V15 — Checkpoint Evaluation and Promotion (v1)

**Milestone:** `V15-M09`  
**Contracts:** `starlab.v15.checkpoint_evaluation.v1`, `starlab.v15.checkpoint_promotion_decision.v1`  
**Profile:** `starlab.v15.checkpoint_evaluation_promotion.v1`  
**Status:** Governance surface; **not** a replacement for a completed long-GPU campaign or strong-agent claim.

**Public closeout (2026-04-25):** M09 **closed** on `main` (implementation [PR #135](https://github.com/m-cahill/starlab/pull/135); merge `eaa928d2177ca3f18caece3c2dac82b474203d08`; **authoritative PR-head CI** [`24942859847`](https://github.com/m-cahill/starlab/actions/runs/24942859847); **merge-boundary `main` CI** [`24942925570`](https://github.com/m-cahill/starlab/actions/runs/24942925570) — **success**). **Closeout status:** **`blocked_missing_m08_campaign_receipt`** — **no** checkpoint promoted; **no** public register rows. **V15-M10** not started; awaits explicit plan approval.

## Purpose

Define deterministic **checkpoint evaluation** and **promotion decision** artifacts for STARLAB v1.5. M09 answers whether a candidate checkpoint is eligible, under recorded evidence, to be treated as a **promoted candidate for downstream v1.5 milestones** (M10+). Promotion here is a **governance routing label**, not “strong agent,” not “release-ready,” and not a benchmark pass.

## Relationship to V15-M08

M08 may produce training manifests, preflight, and (when operator-authorized) campaign execution tooling. M08 does **not** by itself perform checkpoint **promotion** for downstream use. M09 is the first milestone that **names** the evaluation and promotion decision contracts; it must remain honest when **no** completed M08 campaign receipt exists (e.g. public record still **`implementation_ready_waiting_for_operator_run`** for M08).

## Relationship to V15-M10 (XAI)

M09 does not run XAI inference or produce explanation packs. A promotion decision in M09 does not authorize M10; it only allows **planning** a downstream M10+ evidence path if separately approved.

## Relationship to V15-M11 (human panel)

M09 does not run human matches or authorize human-benchmark claims.

## Candidate eligibility (conceptual)

A checkpoint is a serious candidate for evaluation only if required evidence objects exist: M08 training manifest, M08 campaign receipt, checkpoint lineage, candidate metadata with SHA-256, training config, dataset and rights binding, environment lock, and (where applicable) optional protocol JSON bindings. The **default fixture / CI** path has **no** such real evidence; emissions should report **`blocked_missing_m08_campaign_receipt`** (or equivalent) rather than fabricating promotion.

## Required inputs (operator preflight / local dry-run)

Preflight and local-dry-run profiles require paths to the JSON inputs listed in `emit_v15_checkpoint_evaluation` (M08 manifest, M08 campaign receipt, M03 lineage, candidate metadata, M02 environment lock, training config, dataset manifest, rights manifest, optional M05/M04/M06 JSON for SHA-only bindings). M09 only computes **canonical JSON SHA-256** bindings unless a **future** operator explicitly runs an authorized evaluation with blob access (out of scope for default repo paths).

## Evaluation gates (G0–G10)

Gate vocabulary includes: `G0_artifact_integrity` … `G10_non_claim_boundary`. Status values: `pass`, `warning`, `fail`, `blocked`, `not_evaluated`, `not_applicable`. Preflight and `operator_local_evaluation` (dry-run) do **not** set load-smoke to passed without real authorized evaluation.

## Promotion decision vocabulary

Examples: `blocked`, `blocked_missing_m08_campaign`, `blocked_missing_candidate_checkpoint`, `evaluated_not_promoted`, `promoted_candidate_for_downstream_evaluation` (only with explicit future evidence; default emissions in this repository remain non-promoted / blocked for honesty).

## Authorization flags

Both artifacts include the same class of `authorization_flags` (checkpoint / promotion / benchmark / claim / `long_gpu_campaign_completed` / `v2_authorized`). The default path keeps claim-related and benchmark flags **false**.

## Public / private boundary

No raw checkpoint blobs, weights, or private operator paths in committed artifacts. Redaction follows other V15 emitters (paths and contact-like fields).

## Register posture

Public registers get **no** new real rows in M09 unless a future operator supplies evidence and a separate public review approves. Status text may record that the evaluation / promotion **surface** exists without a promoted public asset.

## CLI reference

```bash
python -m starlab.v15.emit_v15_checkpoint_evaluation --output-dir <dir>
```

```bash
python -m starlab.v15.emit_v15_checkpoint_evaluation \
  --profile operator_preflight \
  --m08-training-manifest-json <path> \
  --m08-campaign-receipt-json <path> \
  --checkpoint-lineage-json <path> \
  --candidate-checkpoint-metadata-json <path> \
  --environment-lock-json <path> \
  --training-config-json <path> \
  --dataset-manifest-json <path> \
  --rights-manifest-json <path> \
  --output-dir <dir>
```

```bash
python -m starlab.v15.emit_v15_checkpoint_promotion_decision \
  --evaluation-json <path> \
  --output-dir <dir>
```

## Emitted artifacts

- `v15_checkpoint_evaluation.json` + `v15_checkpoint_evaluation_report.json`  
- `v15_checkpoint_promotion_decision.json` + `v15_checkpoint_promotion_decision_report.json`  

## Non-claims

M09 does not execute the long GPU campaign; does not train checkpoints; does not run the strong-agent benchmark; does not authorize strong-agent, human-benchmark, or v2 claims; does not run human-panel or XAI review; does not commit raw blobs. A promotion decision is **governance metadata**, not a performance claim.

## Blocked / no-candidate closeout

When M08 has not completed a long campaign, an honest M09 result is **blocked** or **not promoted**, with no public register rows. That outcome is **acceptable** and should be reported clearly in `docs/starlab-v1.5.md` and the registers.
