# V15-M43 — Bounded evaluation gate v1 (`starlab.v15.bounded_evaluation_gate.v1`)

**Milestone:** `V15-M43` — *Bounded Evaluation Gate for 2-Hour Candidate*  
**Profile:** `starlab.v15.m43.bounded_evaluation_gate.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m43_bounded_evaluation_gate`

## Purpose

This surface is an **explicit routing / refusal gate only**. It answers whether a sealed **V15-M42** candidate checkpoint evaluation package is **eligible to enter a future bounded evaluation workflow**, not whether any evaluation passed, whether the candidate is strong, or whether a checkpoint should be promoted.

**Immediate upstream package:** sealed **V15-M42** JSON (`v15_m42_two_hour_candidate_checkpoint_evaluation_package.json` is the canonical main artifact basename; `--m42-package-json` accepts any explicit path).

**Mandatory evaluation-readiness ancestry:** governed **V15-M41** remains mandatory through **M42** bindings in normal operator posture. **V15-M39** remains historical receipt/cross-check context via **M41/M42**, not a free-standing shortcut for readiness claims without **M41**. **V15-M05** benchmark protocol metadata, when supplied, is **routing metadata only** unless a later milestone explicitly executes bounded evaluation — this gate emits **no** scorecard outcomes.

## Artifacts

- `v15_bounded_evaluation_gate.json` — sealed bounded evaluation gate decision (canonical JSON + artifact digest field `artifact_sha256`)
- `v15_bounded_evaluation_gate_report.json` — deterministic report companion over the sealed gate body minus `artifact_sha256`

Fixture bundle (CI fixture profile) additionally writes companion routing fixtures beside the canonical **M42** filename when synthesizing deterministic inputs:

- Benchmark protocol routing JSON (fixture companion)
- Environment manifest routing JSON (**V15-M02** contract envelope; routing-only here)

## Status vocabulary

**Success-like (clean):**

- `bounded_evaluation_gate_ready`

**Success-like (explicit warnings carried from eligible M42 postures — `operator_declared` only):**

- `bounded_evaluation_gate_ready_with_warnings`

**Intermediate / deterministic not-ready rollup:**

- `bounded_evaluation_gate_not_ready` — structured routing prerequisites failed or selective operator-declared missing metadata (benchmark protocol and/or environment manifest missing or invalid).

**Structured refusal statuses (explicit strings in `gate_status` and/or refusal rows):**

- `refused_missing_m42_package`
- `refused_invalid_m42_package`
- `refused_m42_package_not_ready`
- `refused_candidate_not_candidate_only`
- `refused_checkpoint_identity_missing`
- `refused_benchmark_protocol_missing`
- `refused_benchmark_protocol_not_allowed`
- `refused_environment_prerequisite_missing`
- `refused_artifact_prerequisite_missing`
- `refused_disallowed_execution_request`
- `refused_route_out_of_scope`

## Always-present honesty flags (`v15_bounded_evaluation_gate.json`)

Deterministic booleans (**always emitted as `false` on this milestone surface):**

```json
"evaluation_executed": false,
"checkpoint_loaded": false,
"promotion_decision_made": false
```

## Route declaration (never execution)

The gate attaches a deterministic **future route declaration**, for example route id `starlab.v15.m43.route.future_bounded_candidate_eval_v1` with `"route_status": "declared_not_executed"` and enumerated `disallowed_now` execution families (benchmark execution, live SC2 execution, human panel execution, checkpoint promotion).

## Profiles

| Profile | M42 sealed JSON | Benchmark protocol JSON | Environment manifest JSON |
| --- | :---: | :---: | :---: |
| `fixture_ci` | synthesized deterministic bundle | synthesized fixture companion | synthesized fixture companion |
| `operator_preflight` | **required** (`--m42-package-json`) | **required** (`--benchmark-protocol-json`) | **required** (`--environment-manifest-json`) |
| `operator_declared` | **required** | optional (missing → deterministic refusal / not-ready rows) | optional (missing → deterministic refusal / not-ready rows) |

**Strict hygiene:** `fixture_ci` and `operator_preflight` require a **clean** M42 `package_status` of **`package_ready_for_future_candidate_evaluation`**. **`package_ready_with_noncritical_warnings`** may map to **`bounded_evaluation_gate_ready_with_warnings`** **only** under **`operator_declared`**, carrying forward M42 warnings into the summarized `m42_package` subsection — never silently upgraded to clean ready.

Forbidden guardrail CLI flags (never executing code paths; emit `refused_disallowed_execution_request`):

- `--run-benchmark`
- `--execute-evaluation`
- `--load-checkpoint`
- `--promote-checkpoint`

## Non-claims (`non_claims` block)

Emitted gate JSON includes enumerated non-authorizations such as:

- **not** benchmark execution (no bounded benchmark harness invocation here)
- **not** benchmark pass/fail results
- **not** strength evaluation
- **not** checkpoint promotion
- **not** scorecard **results**
- **not** **`torch.load`**
- **not** checkpoint **blob loading**
- **not** live StarCraft II matches
- **not** replay-native **XAI** evidence execution
- **not** human panel execution
- **not** showcase release authorization
- **not** **v2** authorization
- **not** executing **T2/T3/T4/T5** evaluation ladders **here**

**V15-M43 does not authorize benchmark execution.** Passing this gate merely records deterministic routing prerequisites for a potential **future bounded evaluation milestone** chartered separately.
