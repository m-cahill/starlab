# V15-M51 — Live candidate watchability harness v1 (`starlab.v15.live_candidate_watchability_harness.v1`)

**Milestone:** `V15-M51` — *Live Candidate Watchability Harness (M50-bound upstream)*  
**Profile surface:** `starlab.v15.m51.live_candidate_watchability_harness.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m51_live_candidate_watchability_harness`  
**Dual-guarded operator runner:** `python -m starlab.v15.run_v15_m51_live_candidate_watchability_harness`

## Purpose

This harness binds **deterministic bookkeeping** over **sealed V15-M50 scorecard-result readout** JSON and exposes **honest labeling** between **fixture / preflight** (no live SC2 via the emitter defaults) and **optional operator-local live SC2** through a governed runner.

This milestone is explicitly **not** a benchmark harness, **not** benchmark pass/fail authority, **not** strength evaluation, **not** checkpoint promotion evidence, **not** a claim that bounded scorecard totals imply policy quality, **not** a twelve-hour execution surface, **not** XAI or human-panel **execution**, **not** showcase release, **not** **v2** authorization, and **not** **T2–T5**.

## Inputs

| Input | Description |
| --- | --- |
| Sealed **M50** **`v15_scorecard_result_readout_decision.json`** | Required canonical upstream for **`operator_preflight`**, **`operator_declared`** (embedded or sibling seal), **`fixture_ci`** (fixture chain generates M49→M50 under `m50_upstream_fixture/` then validates). |
| Optional expected M50 digest | CLI **`--expected-m50-readout-sha256`** → mismatch → refusal with **`refused_m50_sha_mismatch`** (artifacts still emitted; exit follows house style). |

For **`operator_local_watchability_run`** (runner): **`SC2`** install root, map path (**`.SC2Map`**), **`--candidate-checkpoint-path`** (logical bind; scaffold path uses **BurnySC2** watchability policy, **not** trained **PyTorch→SC2** policy). Dual guards (**`--allow-operator-local-execution`**, **`--authorize-live-candidate-watchability`**) are required.

## Profiles

| Profile | Behavior |
| --- | --- |
| **`fixture_ci`** | Builds M50 fixture subtree, parses sealed **M50**, emits M51 artifacts. **`watchability_status`** **`fixture_schema_only_no_live_sc2`**. **`live_sc2_executed`** **false** on primary honesty block. |
| **`operator_preflight`** | Validates **M50** seal/contract/route (must target **`route_to_live_candidate_watchability_harness`** with **`recommended_not_executed`**); checks upstream honesty (**M50** false keys **must** remain honest). Paths for SC2/map are **presence warnings** only unless running live separately. |
| **`operator_declared`** | Validates declared envelope (**`contract_id`**, **`profile_id`**) and **overclaim guards** (`M51`-listed honesty/overclaim booleans **must not** be **true**). May embed **`sealed_m50`** or load sibling file per CLI. Canonical seal on embedded **M50** may be **`require_canonical_seal`** **false** when supplied from envelope (declared posture). |
| **`operator_local_watchability_run`** | Runner-only profile: optional **BurnySC2** scaffold match when **`--allow-scaffold-watchability-policy`** passed; **`real_candidate_policy_adapter`** is **not** wired → default live path blocked with **`watchability_blocked_missing_candidate_live_policy_adapter`** unless scaffold flag grants **labeled** scaffold policy only. |

## Candidate policy labeling

- **`unavailable_candidate_policy_adapter_missing`** — no governed trained-checkpoint→live-SC2 policy adapter (default).  
- **`scaffold_watchability_policy_not_candidate`** — **M27-class** **`burnysc2_policy`** + passive opponent for macro/scout observation only (**candidate vs scaffold distinction** documented in **`non_claims`**).  
- **`real_candidate_policy_adapter`** — reserved vocabulary for a future wired adapter (**not yet available** in repo).  

## Forbidden CLI flags

The emitter rejects the same forbidden execution / claim surfaces as sibling milestones (benchmark claim, strength, promotion, human-panel/XAI shortcuts, showcase, **v2**, **T2–T5**, **12-hour**). Triggered flags normalize to deterministic refusal receipts.

## Output artifact names

| File | Role |
| --- | --- |
| **`v15_live_candidate_watchability_harness.json`** | Sealed primary (`artifact_sha256`). |
| **`v15_live_candidate_watchability_harness_report.json`** | Report companion. |
| **`v15_live_candidate_watchability_harness_brief.md`** | Deterministic brief + non-claims. |

Operator-local scaffold runs write **`watchability_run/match_execution_proof.json`** (hash-stable proof JSON) beside the artifact tree.

## Outcome vocabulary (watchability_status, examples)

- **`fixture_schema_only_no_live_sc2`**
- **`watchability_preflight_ready`**, **`watchability_preflight_ready_with_warnings`**, **`watchability_preflight_blocked`**
- **`watchability_blocked_missing_candidate_live_policy_adapter`**
- **`scaffold_watchability_run_completed_not_candidate_policy`**
- **`live_candidate_watchability_run_blocked`**, **`live_candidate_watchability_run_failed`**

## Route recommendation

Recommended next route (**advisory**, **`recommended_not_executed`**): **`route_to_12_hour_blocker_discovery_launch_rehearsal`** (**V15-M52** vocabulary placeholder — not executed here).

## Honesty (M51 emission)

Top-level booleans mirrored with **M51** honesty set: benchmark / strength / promotion / **torch.load** / checkpoint blobs / authoritative scorecard-as-benchmark / XAI / human-panel / showcase / **v2** / **T2–T5** / **twelve_hour_run_executed** stay **false** unless the narrow field documents an explicit intentional exception (**live SC2 scaffold** sets **`live_sc2_executed`** **true** on success path only).

