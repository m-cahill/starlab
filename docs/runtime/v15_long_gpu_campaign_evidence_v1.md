# V15-M17 — Long GPU Campaign Evidence (v1)

**Milestone:** V15-M17  
**Status:** V15-M17 — **closed** on `main` (implementation [PR #143](https://github.com/m-cahill/starlab/pull/143); **authoritative PR-head CI** [`24971298575`](https://github.com/m-cahill/starlab/actions/runs/24971298575); **merge-boundary `main` CI** [`24971687346`](https://github.com/m-cahill/starlab/actions/runs/24971687346) on merge `d52e411c1b3900b481ee80e599716b547d1dcbcb` — **success**). **Public posture:** long GPU campaign **evidence / preflight** metadata surface **ready**; real training remains **M08** `run_v15_long_gpu_campaign` with operator guards. **M17** does **not** assert a real long campaign **executed** unless **separate** M08-consistent **receipts** exist.  
**Contract:** `starlab.v15.long_gpu_campaign_evidence.v1`  
**Campaign execution receipt (when a real run exists):** `starlab.v15.long_gpu_campaign_receipt.v1` (M08 family; M17 does not define a second receipt contract)

## Purpose

M17 collects **governed** metadata and **preflight** evidence so an operator can run the **first** serious long local GPU training campaign with:

- M16 short GPU / environment success bound by **canonical JSON SHA-256** (no hardcoded private SHA in public code; validate file contents)
- explicit **L0–L15** readiness gates
- a deterministic **evidence** JSON + runbook + closeout checklist
- honest **non-claims** and register touchpoints
- a documented handoff to **M08** `python -m starlab.v15.run_v15_long_gpu_campaign` for actual execution (M17’s emitter does **not** run the trainer)

## Dependency on M16

**Operator preflight** (`--profile operator_preflight`) requires `--m16-short-gpu-environment-json` pointing at a successful M16 `v15_short_gpu_environment_evidence.json` with:

- `contract_id` = `starlab.v15.short_gpu_environment_evidence.v1`
- `profile` = `operator_local_short_gpu_probe`
- `evidence_status` = `operator_local_probe_success`
- `operator_local_execution_performed` = true, `short_gpu_probe_performed` = true, `short_gpu_probe_result` = `success`
- `m17_opening_recommendation` ∈ {`ready_for_m17_planning`, `ready_for_m17_operator_preflight_only`}
- `long_gpu_run_authorized` = false, `v2_authorized` = false, `v2_recharter_authorized` = false
- `cuda_available` = true, `torch_imported` = true (when used for M17 preflight) — at the artifact **root**, **or** the same two booleans may be read from **`torch_cuda_summary`** when the top-level fields are **absent** (actual M16 `operator_local_short_gpu_probe` emit shape). This is validation-only metadata, **not** a long-GPU or v2 **claim**.

Public documentation may state that **operator-local M16 short GPU probe evidence exists and is referenced privately by SHA** without publishing raw private paths.

## Emitter command (fixture / CI-safe)

```bash
python -m starlab.v15.emit_v15_long_gpu_campaign_evidence --output-dir out/v15_m17_long_gpu_campaign/fixture
```

## Emitter command (operator preflight)

```bash
python -m starlab.v15.emit_v15_long_gpu_campaign_evidence \
  --profile operator_preflight \
  --output-dir out/v15_m17_long_gpu_campaign/preflight_001 \
  --m16-short-gpu-environment-json <path_to_m16_v15_short_gpu_environment_evidence.json>
```

## Operator-local guards profile (no training in M17)

Records triple-guard acknowledgment and emits an **M08-shaped** not-executed **receipt stub**; still **does not** invoke the training executor:

```bash
python -m starlab.v15.emit_v15_long_gpu_campaign_evidence \
  --profile operator_local_long_gpu_campaign \
  --output-dir out/v15_m17_long_gpu_campaign/run_001 \
  --m16-short-gpu-environment-json <path_to_m16_json> \
  --allow-operator-local-execution \
  --authorize-long-gpu-campaign \
  --confirm-private-artifacts \
  --planned-wall-clock-hours 12
```

## Long GPU execution (M08, not M17)

After M08 `emit_v15_long_gpu_training_manifest` preflight and sealed `campaign_plan.json` match:

```bash
python -m starlab.v15.run_v15_long_gpu_campaign \
  --campaign-manifest-json <v15_long_gpu_training_manifest.json> \
  --campaign-plan-json <campaign_plan.json> \
  --output-root <out/v15_m08_campaigns/...> \
  --allow-operator-local-execution \
  --authorize-long-gpu-campaign
```

## Emitted files (M17)

| File | Role |
| --- | --- |
| `v15_long_gpu_campaign_evidence.json` | Sealed M17 evidence / preflight record |
| `v15_long_gpu_campaign_evidence_report.json` | Report over evidence JSON |
| `v15_long_gpu_campaign_runbook.md` | Operator runbook (governance) |
| `v15_long_gpu_campaign_closeout_checklist.md` | Closeout checklist template |
| `v15_long_gpu_campaign_receipt.json` / `v15_long_gpu_campaign_receipt_report.json` | **Only** for `operator_local_long_gpu_campaign`: M08 receipt contract, `not_executed` stub (guards only) |

## Profiles

- **`fixture_ci`:** No training, no GPU, no M16 file; placeholder SHA; `campaign_evidence_status: fixture_only`.
- **`operator_preflight`:** Validates M16 file; records SHA + sanitized summary; `campaign_evidence_status: operator_preflight_ready`; does **not** run the campaign.
- **`operator_declared`:** Normalizes operator-supplied JSON with path redaction; does **not** execute training.
- **`operator_local_long_gpu_campaign`:** Triple CLI guards + M16 path; **no** training; optional M08 receipt **stub** with `not_executed` posture.

## M16 binding semantics

Canonical JSON **SHA-256** is computed from parsed JSON and stored in the M17 evidence artifact. The implementation **must not** require one fixed global SHA; invalid or incomplete M16 files **fail** with a clear `ValueError` / CLI error.

## Readiness gates L0–L15

Gate rows use `default_status`, `gate_id`, `name`, and `notes` (not legacy `status` / `summary` fields). See emitted JSON for the full table. **L1** is `not_evaluated` in pure fixture mode; **pass** when M16 is bound in preflight.

## Campaign duration policy

Duration is **manifest-driven** (M08 `campaign_plan.json`). Suggested first governed run: e.g. 12h planned, 24h hard stop, checkpoint cadence 30–60m (declared in plan, not hard-coded as the only option in code).

## Stop / resume / interruption

Real runs must produce honest interruption/resume/failure records per M08 runbook. M17’s fixture path does not simulate these.

## M18 dependency

M18 owns **candidate checkpoint evaluation** evidence. M17 should leave enough lineage pointers (policy fields) for M18 to consume checkpoint IDs, hashes, config hash, and environment SHA references.

## Public / private boundary

**Public-safe:** contract IDs, gate IDs, status enums, SHA-256 bindings, sanitized GPU summaries when intended for disclosure.  
**Private by default:** weights, checkpoint blobs, full logs, tensorboard, raw absolute paths, SC2 install paths, hostnames, usernames, uncritical operator notes, videos, saliency tensors, participant data.

## Register touchpoints

`docs/rights_register.md`, `docs/training_asset_register.md`, `docs/replay_corpus_register.md`, `docs/model_weight_register.md`, `docs/checkpoint_asset_register.md`, `docs/xai_evidence_register.md`, `docs/human_benchmark_register.md` — **touchpoints only** unless a later milestone adds reviewed rows.

## Non-claims

M17 is **not** a strong-agent pass, not a human benchmark, not XAI proof, not showcase release, not v2 authorization, not checkpoint promotion, and not a claim that a long run completed unless backed by M08 receipts and honest closeout. See **`docs/starlab-v1.5.md`** (M17 non-claims block).

## Closeout (on `main`)

`docs/starlab-v1.5.md` and this file record [PR #143](https://github.com/m-cahill/starlab/pull/143) merge/CI: **no** real long campaign **executed** in the **implementation** PR/CI; **V15-M18**–**V15-M21** **proposed**; **M17** public closeout: evidence/preflight **surface** only. Optional **public** doc-only follow-up commits may add revision metadata after merge (same as other V15 milestones).
