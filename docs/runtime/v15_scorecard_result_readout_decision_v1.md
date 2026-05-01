# V15-M50 — Scorecard result readout / benchmark pass-fail refusal decision v1 (`starlab.v15.scorecard_result_readout_decision.v1`)

**Milestone:** `V15-M50` — *Scorecard Result Readout / Benchmark Pass-Fail Refusal Decision*  
**Profile:** `starlab.v15.m50.scorecard_result_readout_benchmark_pass_fail_refusal.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m50_scorecard_result_readout_decision`

## Purpose

**V15-M50** is a deterministic scorecard result readout and benchmark pass/fail refusal decision over sealed **V15-M49** bounded scorecard result execution artifacts. It is not benchmark execution, not authoritative benchmark pass/fail, not strength evaluation, and not checkpoint promotion.

**V15-M50 may:**

- Validate sealed **`v15_bounded_scorecard_result_execution.json`** (`starlab.v15.bounded_scorecard_result_execution.v1`) including canonical **`artifact_sha256`** when required by profile.
- Bind upstream **`result_status`**, contract/profile identity, and digest into **`m49_binding`**.
- Summarize bounded **`scorecard_total`** / **`win_rate`** fields when **M49** legitimately emitted them into **`scorecard_readout`** (`bounded_fields_only` remains **true**).

**V15-M50 must not:**

- Emit **`benchmark_passed: true`** or authoritative **`benchmark_failed: true`** as a benchmark ruling.
- Evaluate agent strength or promote/reject a checkpoint as a strength conclusion.
- Invoke **`torch.load`**, load checkpoint blobs, run live SC2, XAI, human-panel workflows, showcase release, **v2** authorization, or **T2–T5** execution (honesty keys remain **false**).

## Inputs

| Input | Description |
| --- | --- |
| Sealed **M49** JSON | **`v15_bounded_scorecard_result_execution.json`** with valid **`artifact_sha256`** (operator_preflight / fixture_ci chain). |
| Optional expected digest | **`--expected-m49-scorecard-result-sha256`** — mismatch → **`scorecard_result_readout_refused`** with **`refused_m49_sha_mismatch`** (artifact emitted; CLI exits **0**, consistent with **V15-M49** house style). |
| Declared envelope | **`operator_declared`**: JSON with **`m49_binding`**, **`declared_m49_execution_summary`** (see below). |

## Profiles

| Profile | Behavior |
| --- | --- |
| **`fixture_ci`** | Runs **M49** `fixture_ci` chain, loads sealed **M49**, emits **M50** JSON + report + brief. CI-safe; no operator paths; no torch; no SC2. |
| **`operator_preflight`** | **`--m49-scorecard-result-json`** (required), **`--output-dir`** (required), optional expected SHA. Validates seal, contract, upstream eligibility. |
| **`operator_declared`** | **`--declared-readout-json`** — redacts path-like strings; validates contract/profile and overclaim guards; **does not** execute gameplay or benchmarks. |

### Declared envelope (operator_declared)

Top-level **`contract_id`** / **`profile_id`** must match **M50**. Required blocks:

- **`m49_binding`**: **`contract_id`**, **`profile_id`**, **`artifact_sha256`** (64-hex), **`status`** (must match summary **`result_status`** when both set).
- **`declared_m49_execution_summary`**: **`result_status`**, **`scorecard_result`**, optional **`warnings`**, honesty-related keys mirrored for **`decide`** (defaults **false**).

## Output artifact names

| File | Role |
| --- | --- |
| **`v15_scorecard_result_readout_decision.json`** | Sealed primary artifact (`artifact_sha256`). |
| **`v15_scorecard_result_readout_decision_report.json`** | Report companion. |
| **`v15_scorecard_result_readout_decision_brief.md`** | Deterministic brief + non-claim footer. |

## Contract IDs

- **`starlab.v15.scorecard_result_readout_decision.v1`**
- **`starlab.v15.m50.scorecard_result_readout_benchmark_pass_fail_refusal.v1`**

## Outcome vocabulary (readout_status)

- **`scorecard_result_readout_completed`**
- **`scorecard_result_readout_completed_with_warnings`**
- **`scorecard_result_readout_refused`**

## Benchmark pass/fail decision vocabulary

Nested object **`benchmark_pass_fail_decision.decision`**:

- **`benchmark_pass_fail_refused_pending_authoritative_threshold`** — refusal / upstream-not-ready paths.
- **`benchmark_pass_fail_refused_m49_bounded_only`** — bounded **M49** fields summarized; pass/fail still refused.
- **`benchmark_pass_fail_refused_missing_scorecard_results`** — incomplete bounded metrics on upstream success (warnings path).

## Promotion decision vocabulary

**`promotion_decision.decision`**:

- **`promotion_refused_pending_benchmark_pass_fail`**
- **`promotion_refused_m50_readout_only`**

## Refusal vocabulary (examples)

- **`refused_missing_m49_scorecard_result_execution_json`**
- **`refused_m49_contract_invalid`**
- **`refused_m49_sha_mismatch`**
- **`refused_m49_result_refused`**
- **`refused_m49_result_not_ready`**
- **`refused_missing_scorecard_result_fields`**
- **`refused_m49_upstream_overclaim_or_honesty_violation`**
- **`refused_benchmark_pass_claim`**, **`refused_strength_claim`**, **`refused_promotion_claim`**, … (forbidden CLI flags)
- **`refused_invalid_declared_m50_shape`**

## Honesty keys (success emissions)

All remain **false**: **`benchmark_passed`**, **`benchmark_failed`**, **`benchmark_pass_fail_emitted`**, **`strength_evaluated`**, **`checkpoint_promoted`**, **`torch_load_invoked`**, **`checkpoint_blob_loaded`**, **`live_sc2_executed`**, **`xai_executed`**, **`human_panel_executed`**, **`showcase_released`**, **`v2_authorized`**, **`t2_t3_t4_t5_executed`**.

## Examples of allowed readout

- **`scorecard_readout.scorecard_total`** / **`win_rate`** copied from **M49** **`scorecard_result`** when finite and **`win_rate`** ∈ **[0, 1]**.
- **`benchmark_pass_fail_decision.decision`** = **`benchmark_pass_fail_refused_m49_bounded_only`** with reason **`m49_bounded_scorecard_fields_only_not_benchmark_pass_fail`**.

## Examples of forbidden overclaim

- Any **`benchmark_passed: true`** on **M50** artifact.
- **`benchmark_pass_fail_emitted: true`** implying an authoritative ladder ruling.
- **`checkpoint_promoted: true`** or strength language derived only from bounded totals.

## Explicit non-claims

See emitted **`non_claims`** list — includes: bounded readout only; not benchmark execution; not benchmark pass/fail authority; not strength; not promotion; no torch/checkpoint blob loads; no live SC2; no XAI/human/showcase/**v2**/T2–T5; route advisory **`recommended_not_executed`** only.

## Relationship to **V15-M49**

**M49** may emit bounded totals/win-rate **artifact fields** only. **M50** consumes sealed **M49** and records readout **without** upgrading those fields to benchmark pass/fail or promotion evidence.

## Relationship to **V15-M51 / M52 / M53** roadmap

- **V15-M51 — Live Candidate Watchability Harness:** **M50** routes (**`route_to_live_candidate_watchability_harness`**) with **`route_status`** **`recommended_not_executed`** — advisory only.
- **V15-M52 — 12-hour blocker discovery / launch rehearsal:** downstream operational rehearsal; **not** executed by **M50**.
- **V15-M53 — 12-hour operator run attempt:** downstream long-run attempt; **not** executed by **M50**.

## Forbidden CLI flags

Same family as **M49**: **`--claim-benchmark-pass`**, **`--claim-strength`**, **`--promote-checkpoint`**, **`--load-checkpoint`**, **`--run-live-sc2`**, **`--run-xai`**, **`--run-human-panel`**, **`--release-showcase`**, **`--authorize-v2`**, **`--execute-t2`** … **`--execute-t5`** — deterministic refusal emission.
