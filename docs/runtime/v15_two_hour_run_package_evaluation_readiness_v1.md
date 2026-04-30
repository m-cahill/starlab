# V15-M41 — Two-hour run package & evaluation readiness (`starlab.v15.two_hour_run_package_evaluation_readiness.v1`)

## Purpose

V15-M41 packages the completed **V15-M39** **7200-second** operator-local SC2-backed T1 continuation / candidate-training run into a governed **evaluation-readiness** bundle. It binds the sealed M39 receipt digest, companion telemetry summary, checkpoint inventory, and transcript **presence/metadata** — **without** loading checkpoint blobs, **without** `torch.load`, and **without** executing benchmarks or promotion logic.

V15-M41 packages the completed V15-M39 two-hour run for future evaluation routing. It does not execute benchmark matches, evaluate strength, promote checkpoints, produce scorecard results, run XAI or human-panel evaluation, release a showcase agent, authorize v2, or execute T2/T3.

## Contract / profile

- **Contract:** `starlab.v15.two_hour_run_package_evaluation_readiness.v1`
- **Profile:** `starlab.v15.m41.two_hour_run_package_evaluation_readiness.v1`
- **Emitter:** `python -m starlab.v15.emit_v15_m41_two_hour_run_package_evaluation_readiness`

## Modes

### 1. Fixture CI (`--fixture-ci`)

- Emits schema-only artifacts for merge-gate CI.
- **`package_status`:** `fixture_schema_only_no_operator_package`
- **`evaluation_ready`:** `false`

### 2. Operator package preflight (`--profile operator_preflight`)

- Requires explicit paths to sealed **`v15_two_hour_operator_run_attempt.json`**, **`v15_m39_telemetry_summary.json`**, **`v15_m39_checkpoint_inventory.json`**, **`v15_m39_operator_transcript.txt`**, plus **`--expected-m39-artifact-sha256`** and **`--expected-final-candidate-sha256`**.
- Validates the M39 canonical seal and that the CLI-expected receipt digest matches the sealed body.
- Confirms **`run_status`** is `two_hour_operator_run_completed_with_candidate_checkpoint`, **`full_wall_clock_satisfied`** is true, retention counters are present, M39 “downstream” claim flags (benchmark, promotion, etc.) remain false, and the final candidate SHA appears in the checkpoint inventory list.
- Does **not** hash large checkpoint files unless **`--authorize-final-checkpoint-file-sha256`** is set alongside **`--final-candidate-checkpoint-path`**.

## Inputs

| Input | Role |
| --- | --- |
| M39 sealed JSON | Primary receipt; canonical `artifact_sha256` must match operator-declared expected digest |
| Telemetry summary JSON | Parsed JSON object; binding evidence |
| Checkpoint inventory JSON | Must list `final_candidate_sha256` under `checkpoint_files[].sha256` |
| Transcript file | Must exist and be non-empty; **contents are not copied** into the sealed M41 JSON |

Path discovery under operator `out/` is a **local workflow**, not required for CI.

## Output artifacts

- `v15_two_hour_run_package_evaluation_readiness.json` (sealed)
- `v15_two_hour_run_package_evaluation_readiness_report.json`
- `v15_two_hour_run_package_evaluation_readiness_checklist.md`
- `v15_m41_evaluation_readiness_packet.md`
- `v15_m41_candidate_checkpoint_index.json`

## Gate pack (P0–P9)

| Gate | Name | Pass condition |
| --- | --- | --- |
| **P0** | M39 receipt bound | JSON readable; canonical seal valid; digest matches CLI expected |
| **P1** | M39 contract valid | `contract_id` / `profile_id` match M39 |
| **P2** | Run completed | `run_status == two_hour_operator_run_completed_with_candidate_checkpoint` |
| **P3** | Wall-clock satisfied | `full_wall_clock_satisfied == true` |
| **P4** | Final candidate present | Receipt + inventory agree on final SHA vs CLI expected |
| **P5** | Retention evidence | Retention counters present in M39 receipt |
| **P6** | Companion evidence | Telemetry + inventory JSON parse; transcript non-empty |
| **P7** | Non-claims preserved | Selected M39 claim-flag keys remain false (benchmark, promotion, v2, T2/T3, etc.) |
| **P8** | Public/private boundary | Emission checked against path-leak heuristics |
| **P9** | Evaluation readiness only | M41 claim flags remain false; status is structural readiness, not benchmark/strength |

## Relationship to M39

M39 produces the sealed operator receipt and companion files after a completed Phase B run. M41 **consumes** those artifacts as evidence and classifies **structural** readiness for future evaluation packaging — **not** benchmark pass or checkpoint strength.

## Relationship to M40

**V15-M40** restored the M37→M38→M39 preflight chain; it did **not** execute the **7200-second** training subprocess. The completed Phase B run and sealed receipt (`artifact_sha256` **`675ae631ff2fa8a9f71f2c03a93f3abbffbfe0c45fcb49a59c933920330b010c`** on the public record) are **M39** outcomes that M41 packages.

## Candidate checkpoint index

The index records both SHA-256 roles:

- **`source_candidate_lineage_anchor`** — public lineage anchor entering the continuation path (`eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26`).
- **`final_two_hour_candidate_checkpoint`** — SHA produced by the completed **7200s** run (ledger example: `51cea94ed5324087863b246b7b31a21021eba286924aea4609aa09466430a943`).

Both remain **candidate-only** and **not promoted** unless a later milestone says otherwise.

## Evaluation-readiness semantics

- **`package_ready_for_future_evaluation`** means the evidence bundle is **structurally** consistent and bound for **future** evaluation routing — **not** that evaluation ran or passed.
- **`package_ready_with_noncritical_warnings`** may be used when optional metadata (e.g. optional checkpoint path without file hash) produces non-blocking warnings.

## Public/private boundary

Do not copy raw absolute paths or full operator `out/` trees into public JSON fields. Operator-local paths belong in private notes only (e.g. under `docs/company_secrets/` locally, never committed).

## Non-claims

M41 does **not** claim: benchmark pass, strength evaluation, checkpoint promotion, scorecard results, T2/T3, XAI execution, human-panel execution, showcase release, or v2 authorization.

## Status vocabulary (selected)

- `fixture_schema_only_no_operator_package`
- `package_blocked_missing_m39_receipt`
- `package_blocked_invalid_m39_receipt`
- `package_blocked_m39_not_completed`
- `package_blocked_missing_candidate_checkpoint_inventory`
- `package_blocked_missing_telemetry_summary`
- `package_blocked_missing_transcript`
- `package_blocked_candidate_sha_mismatch`
- `package_ready_for_future_evaluation`
- `package_ready_with_noncritical_warnings`

## CLI examples

Fixture (CI):

```powershell
python -m starlab.v15.emit_v15_m41_two_hour_run_package_evaluation_readiness `
  --fixture-ci `
  --output-dir out/v15_m41_fixture
```

Operator preflight (paths and SHAs supplied explicitly):

```powershell
.\.venv\Scripts\python.exe -m starlab.v15.emit_v15_m41_two_hour_run_package_evaluation_readiness `
  --profile operator_preflight `
  --m39-run-json <path-to-v15_two_hour_operator_run_attempt.json> `
  --m39-telemetry-summary-json <path-to-v15_m39_telemetry_summary.json> `
  --m39-checkpoint-inventory-json <path-to-v15_m39_checkpoint_inventory.json> `
  --m39-transcript <path-to-v15_m39_operator_transcript.txt> `
  --expected-m39-artifact-sha256 675ae631ff2fa8a9f71f2c03a93f3abbffbfe0c45fcb49a59c933920330b010c `
  --expected-final-candidate-sha256 51cea94ed5324087863b246b7b31a21021eba286924aea4609aa09466430a943 `
  --output-dir out/v15_m41_operator_package/<run_id>
```

## Provisional next

- **Success path:** `V15-M42_candidate_checkpoint_evaluation_package_from_two_hour_run`
- **Blocked / remediation path:** `V15-M42_2Hour_Run_Package_Remediation`
