# V15-M53 — Twelve-hour operator run attempt v1 (`starlab.v15.twelve_hour_operator_run_attempt.v1`)

**Milestone:** `V15-M53` — *12-Hour Operator Run Attempt*  
**Profile surface:** `starlab.v15.m53.twelve_hour_operator_run_attempt.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m53_twelve_hour_operator_run_attempt`  
**Runner:** `python -m starlab.v15.run_v15_m53_twelve_hour_operator_run_attempt`

V15-M53 owns the governed 12-hour operator run attempt. A completed M53 run is training execution evidence only; it is not benchmark pass/fail, not strength evaluation, not checkpoint promotion, not showcase release, not v2 authorization, and not T2–T5 execution.

## Purpose

Either execute a **governed** operator-local SC2-backed candidate-training run targeting **43200 s** wall clock (via the existing **M28** training stack and a **resolved frozen launch command**), or **block** with deterministic reasons. **Phase A** (candidate-watch smoke) must succeed or be explicitly acknowledged skipped before **Phase B** (12-hour attempt) unless operator policy uses the loud skip flag.

## M52 dependency

Binds sealed **`v15_twelve_hour_launch_rehearsal.json`** (**`starlab.v15.twelve_hour_blocker_discovery_launch_rehearsal.v1`**) with canonical **`artifact_sha256`**. Rehearsal status must be operator-ready (e.g. `twelve_hour_launch_rehearsal_ready` or `twelve_hour_launch_rehearsal_ready_with_warnings`). **`stop_resume_plan_frozen`** must be true.

## Phase A — candidate-watch smoke

- **Runner:** `--phase candidate-watch-smoke`  
- **Guards:** `--allow-operator-local-execution` **and** `--authorize-candidate-watch-smoke`  
- **Requires:** `--m51-watchability-json` (M52A upstream), checkpoint path + expected SHA, SC2 root, map, output dir.  
- **Delegates to:** `python -m starlab.v15.run_v15_m52_candidate_live_adapter_spike` (M52A-compatible artifacts under `candidate_watch_smoke/`).

Acceptable sealed M52A **`adapter_status`** values for Phase B include completed / readyish statuses defined alongside **M52A** (see **M52B** `M52A_READYISH` set).

**Skip (loud):** `--acknowledge-skip-candidate-watch-smoke` sets Phase A status to `candidate_watch_smoke_skipped_with_operator_acknowledgment` — **use sparingly**.

## Phase B — 12-hour attempt

- **Runner:** `--phase full-12hour`  
- **Guards:** `--allow-operator-local-execution` **and** `--authorize-12-hour-operator-run`  
- **Requires:** sealed M52 JSON, Phase A artifact path (unless skipped as above), **`--m53-training-launch-command`** pointing to an operator-resolved text file that invokes **M28** with **720** minutes (or equivalent **43200 s** horizon) and **`--max-retained-checkpoints`** (default **256**), plus checkpoint / SC2 / map / output directory.

Training is **not** reimplemented in M53 — it is **orchestration + receipts** around the frozen launch line (same pattern family as **M39** + **M28**).

## Profiles (emitter)

| Profile | Behavior |
| --- | --- |
| `fixture_ci` | CI-safe schema + artifacts; **no** live SC2; **no** checkpoint load; **no** 12-hour run. |
| `operator_preflight` | Validates M52 seal + operator inputs; optional M52A path; optional disk strictness (`--skip-disk-budget-strict` for constrained hosts). |

## Inputs (representative)

- `--m52-launch-rehearsal-json`, optional `--expected-m52-launch-rehearsal-sha256`  
- `--m52a-adapter-spike-json`, optional `--expected-m52a-adapter-spike-sha256`  
- `--candidate-checkpoint-path`, `--expected-candidate-checkpoint-sha256`  
- `--sc2-root`, `--map-path`  
- `--disk-root`, `--estimated-checkpoint-mb`, `--max-retained-checkpoints`  
- Phase B: `--m53-training-launch-command`, `--wall-clock-seconds` (default **43200**), optional `--resume-from`  

Do **not** hardcode private checkpoint paths in-repo; pass path + digest via CLI.

## Output artifacts (operator-local; do not commit)

| File | Role |
| --- | --- |
| `v15_twelve_hour_operator_run_attempt.json` | Sealed primary |
| `v15_twelve_hour_operator_run_attempt_report.json` | Report |
| `v15_twelve_hour_operator_run_attempt_checklist.md` | Checklist |
| `v15_m53_operator_transcript.txt` | Subprocess transcript |
| `v15_m53_telemetry_summary.json` | Telemetry summary |
| `v15_m53_checkpoint_inventory.json` | Checkpoint inventory |

Optional: `candidate_watch_smoke/` (M52A tree); `resume/v15_m53_interruption_receipt.json` on interrupt.

## Contract IDs

- `starlab.v15.twelve_hour_operator_run_attempt.v1`
- `starlab.v15.m53.twelve_hour_operator_run_attempt.v1`

## Forbidden flags (deterministic refusal)

Includes `--claim-benchmark-pass`, `--claim-strength`, `--promote-checkpoint`, `--run-benchmark`, `--run-xai`, `--run-human-panel`, `--release-showcase`, `--authorize-v2`, `--execute-t2` … `--execute-t5`.

## Guardrails

- Only **`--authorize-12-hour-operator-run`** may authorize the 12-hour Phase B training subprocess (not generic over-claim shortcuts).  
- Honesty object keeps benchmark / strength / promotion / XAI / human-panel / showcase / v2 / T2–T5 **false** unless future milestones authorize.

## Stop / resume

On interrupt, M53 may emit **`resume/v15_m53_interruption_receipt.json`**. **`--resume-from`** binds metadata only; full resume semantics follow **M52** stop/resume card and **M28** checkpoint discipline.

## Checkpoint retention

Default **`--max-retained-checkpoints`** **256**; pruning behavior remains **M28**/**M39** family semantics — M53 records and inventories only.

## Telemetry capture

M53 merges **M28** `v15_sc2_backed_t1_candidate_training.json` hints from the output tree where present.

## Public / private boundary

Sealed JSON and summaries are public-safe when path-redacted. Raw checkpoints, full transcripts with secrets, and `docs/company_secrets/**` remain private / non-committed per project policy.

## Non-claims

See emitter `non_claims` list and **`M53 non-claims block`** in `docs/starlab-v1.5.md`.

## Relationship to M54

After M53 **closeout**, seed provisional **V15-M54** privately: either **12-Hour Run Package / Evaluation Readiness** (success path) or **12-Hour Run Remediation Gate** (blocked/failed/interrupted without completion receipt).

---

Ensure all documentation is updated as necessary when changing M53 posture or operator instructions.
