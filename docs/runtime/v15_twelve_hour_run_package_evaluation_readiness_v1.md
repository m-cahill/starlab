# Runtime — V15-M54 Twelve-Hour Run Package / Evaluation Readiness (`starlab.v15.twelve_hour_run_package_evaluation_readiness.v1`)

## Purpose

V15-M54 packages V15-M53 12-hour training execution evidence and determines readiness for future bounded evaluation package preflight. It does not execute benchmark pass/fail, does not evaluate strength, and does not promote the produced checkpoint.

This milestone emits deterministic readiness artifacts (`v15_twelve_hour_run_package_readiness.json`, reports, checklist, checkpoint binding, manifest). It may verify checkpoint files by **raw SHA-256 over bytes** only — **never** `torch.load`.

## Contract identifiers

- **`starlab.v15.twelve_hour_run_package_evaluation_readiness.v1`**
- **`starlab.v15.m54.twelve_hour_run_package_evaluation_readiness.v1`** (`profile_id`)

## Profiles

### `fixture_ci`

CI-safe schema fixture. Does not load checkpoints, does not read operator `out/` trees.

**Status:** `fixture_schema_only_no_package_evidence`

### `operator_preflight`

Validates sealed **`v15_twelve_hour_operator_run_attempt.json`** and companion artifacts.

**Required:**

- `--m53-run-json`
- `--output-dir`

**Recommended / typical operator invocation also supplies:**

- `--expected-m53-run-sha256` (canonical sealed **`artifact_sha256`** — required for deterministic acceptance)
- `--m53-checkpoint-inventory-json`
- `--m53-telemetry-summary-json`
- `--m53-transcript-path`
- `--phase-a-match-proof-json` (`match_execution_proof.json` from Phase A candidate watch smoke)
- `--final-candidate-checkpoint-path`
- `--expected-final-candidate-checkpoint-sha256`

**Optional:**

- `--raw-m53-file-sha256` — when supplied as valid hex64, compared to **raw file** SHA-256 of `--m53-run-json`; mismatch **blocks**. When omitted, emits **`warning_raw_artifact_hash_missing`** (does **not** block).
- `--expected-phase-a-proof-sha256` — defaults to the ledger anchor for the closed operator proof hash when omitted.

### `operator_declared`

Normalizes and seals operator-supplied **`--declared-readiness-json`** (metadata-first envelope). Intended when paths/hashes are declared locally without full filesystem replay.

## Inputs (operator package)

Typical paths (operator-local `out/`, **not committed**):

```text
out/v15_m53/12hour_attempt_001/v15_twelve_hour_operator_run_attempt.json
out/v15_m53/12hour_attempt_001/v15_m53_checkpoint_inventory.json
out/v15_m53/12hour_attempt_001/v15_m53_telemetry_summary.json
out/v15_m53/12hour_attempt_001/v15_m53_operator_transcript.txt
out/v15_m53/candidate_watch_smoke_001/candidate_watch_smoke/candidate_live_adapter_watch/match_execution_proof.json
out/v15_m53/12hour_attempt_001/m28_training/checkpoints/candidate_checkpoint_step_59858688_final.pt
```

### M53 dependency

Preflight requires:

- **`contract_id`** `starlab.v15.twelve_hour_operator_run_attempt.v1`
- **`profile_id`** `starlab.v15.m53.twelve_hour_operator_run_attempt.v1`
- Canonical **`artifact_sha256`** seal integrity
- **`run_status`** `twelve_hour_operator_run_completed_with_candidate_checkpoint`
- Empty **`blockers`** and **`failure_reasons`**
- **`phase_b_12hour_run.full_wall_clock_satisfied`** **true**
- **`phase_b_12hour_run.final_step_checkpoint_persisted`** **true**

### Phase A proof binding

When `--phase-a-match-proof-json` is supplied, its **raw file SHA-256** must match **`--expected-phase-a-proof-sha256`** (or the ledger anchor default). Missing proof path **blocks** (`blocked_phase_a_proof_missing`).

### Final checkpoint binding

The checkpoint inventory **must** list exactly:

```text
m28_training/checkpoints/candidate_checkpoint_step_59858688_final.pt
```

with SHA-256 **`7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90`** (or the operator-declared produced SHA when hashing the on-disk file).

**Explicit distinction:**

```text
input_candidate_checkpoint_sha256 = 51cea94ed5324087863b246b7b31a21021eba286924aea4609aa09466430a943
produced_candidate_checkpoint_sha256 = 7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90
promotion_status = not_promoted_candidate_only
```

Required statement (also embedded in checklist JSON/report/checklist prose):

```text
The produced checkpoint is bound as a candidate artifact for future evaluation routing. V15-M54 does not promote this checkpoint.
```

### Checkpoint inventory validation

Inventory rows use **`path_relative_to_m39_output_dir`** (legacy field name). The relative path must match the **`m28_training/checkpoints/candidate_checkpoint_step_59858688_final.pt`** suffix **and** the produced SHA.

### Telemetry / transcript validation

- Missing telemetry summary JSON → **`blocked_telemetry_summary_missing`**
- Missing transcript → **`blocked_transcript_missing`**
- Very short transcript or `[redacted]` in body → **`warning_transcript_short_or_redacted`** (warning only if transcript exists)

## Output artifacts

Primary:

```text
v15_twelve_hour_run_package_readiness.json
v15_twelve_hour_run_package_readiness_report.json
v15_twelve_hour_run_package_readiness_checklist.md
v15_m54_candidate_checkpoint_binding.json
v15_m54_evaluation_readiness_manifest.json
```

Optional public-safe brief:

```text
v15_twelve_hour_run_package_readiness_brief.md
```

Do **not** commit raw operator outputs under `out/**`.

## Readiness statuses

- `fixture_schema_only_no_package_evidence`
- `twelve_hour_run_package_ready_for_bounded_evaluation_readiness`
- `twelve_hour_run_package_ready_with_warnings`
- `twelve_hour_run_package_blocked`
- `twelve_hour_run_package_refused`

“Ready for bounded evaluation readiness” is **not** “benchmark ready” and **not** “benchmark passed.”

## Blockers (deterministic samples)

Including but not limited to:

```text
blocked_missing_m53_run_json
blocked_m53_contract_invalid
blocked_m53_sha_mismatch
blocked_m53_not_completed
blocked_m53_has_blockers
blocked_m53_has_failure_reasons
blocked_full_wall_clock_not_satisfied
blocked_final_checkpoint_not_persisted
blocked_final_checkpoint_missing
blocked_final_checkpoint_sha_mismatch
blocked_checkpoint_inventory_missing
blocked_checkpoint_inventory_missing_final_checkpoint
blocked_telemetry_summary_missing
blocked_transcript_missing
blocked_phase_a_proof_missing
blocked_raw_artifact_hash_mismatch
```

## Warnings

```text
warning_m50_upstream_fixture_bounded_only
warning_final_m53_replay_saved_false
warning_transcript_short_or_redacted
warning_phase_a_replay_saved_but_final_m53_replay_false
warning_package_ready_but_not_evaluation
warning_checkpoint_candidate_only_not_promoted
warning_raw_artifact_hash_missing
```

## Forbidden CLI flags (deterministic refusal)

If present on argv, emit refusal receipts (**exit 0**, **`twelve_hour_run_package_refused`**):

```text
--claim-benchmark-pass
--claim-strength
--promote-checkpoint
--run-benchmark
--run-xai
--run-human-panel
--release-showcase
--authorize-v2
--execute-t2
--execute-t3
--execute-t4
--execute-t5
--load-checkpoint-for-evaluation
--torch-load-checkpoint
```

## Public / private boundary

Emitted JSON/checklists must not leak absolute filesystem paths or secrets; paths may appear basename-only where permitted. Preflight transcripts may be operator-local — distribution follows **`docs/public_private_boundary.md`**.

## Non-claims

V15-M54 does **not**:

- Execute benchmark matches or emit benchmark pass/fail
- Evaluate agent strength
- Promote checkpoints (`not_promoted_candidate_only`)
- Invoke **`torch.load`** or load checkpoints for inference evaluation
- Run XAI, human-panel evaluation, showcase release
- Authorize **v2**
- Execute **T2–T5**

## Relationship to V15-M55

When the package is **ready**, routing recommends **`V15-M55 — Bounded Evaluation Package Preflight`** with **`route_status = recommended_not_executed`** (**`route_to_bounded_evaluation_package_preflight`**).

When **blocked**, remediation routing recommends **`V15-M55 — 12-Hour Run Package Remediation`**.

## CLI

```bash
python -m starlab.v15.emit_v15_m54_twelve_hour_run_package_readiness \
  --profile fixture_ci \
  --output-dir <path>
```

## M53 upstream caveat

**M50** upstream remains **`fixture_ci`** bounded posture. The **M53** chain proves governed operator wiring, Phase A live adapter smoke, and 12-hour training execution; it does **not** convert **M49**/**M50** scorecard fields into benchmark pass/fail evidence. This milestone emits **`warning_m50_upstream_fixture_bounded_only`** on preflight packaging paths.
