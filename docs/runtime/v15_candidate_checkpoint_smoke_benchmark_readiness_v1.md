# V15-M35 — Candidate checkpoint smoke benchmark readiness (v1)

**Contract:** `starlab.v15.candidate_checkpoint_smoke_benchmark_readiness.v1`  
**Profile:** `starlab.v15.m35.candidate_checkpoint_smoke_benchmark_readiness.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m35_candidate_checkpoint_smoke_benchmark_readiness`

## Purpose

M35 is a **readiness / refusal** gate between a sealed **M33** CUDA model-load probe and **any future** smoke-benchmark **execution** path. It validates **metadata and seals only** — **no** checkpoint blob I/O and **no** `torch.load` on the M35 code path.

When preconditions are satisfied, the strongest allowed posture is **`smoke_benchmark_ready_for_future_execution`** — meaning the operator may **route** the candidate into a **separately chartered** benchmark runner; it is **not** a **`benchmark_passed`** claim.

## Modes

### Fixture CI (`--fixture-ci`)

Emit **`fixture_schema_only_no_benchmark_execution`**. No M33 file required. Default merge-gate / honest public posture.

### Operator preflight (`--m33-cuda-probe-json`)

Requires a readable sealed **`v15_candidate_checkpoint_model_load_cuda_probe.json`** (M33). Gates include:

- Contract / profile and **`candidate_model_load_cuda_probe_completed`**
- **`cuda_probe_performed`** and **`device_observed`** **`cuda`** (when readiness is granted)
- Candidate **SHA-256** consistency (**explicit** `--expected-candidate-sha256` or public record default)

Optional **`--m05-scorecard-json`:** validates **`starlab.v15.strong_agent_scorecard.v1`** protocol JSON when supplied; invalid JSON blocks with **`smoke_benchmark_readiness_blocked_invalid_scorecard_protocol_json`**.

## Non-claims

M35 **does not** execute benchmark matches; **does not** produce scorecard **results**; **does not** evaluate strength; **does not** promote the checkpoint; **does not** run a **72-hour** campaign; **does not** assert live SC2 evaluation outcomes; **does not** run XAI or human-panel evaluation; **does not** release a showcase agent; **does not** authorize **v2** or **T2** / **T3**.

## Artifacts

- `v15_candidate_checkpoint_smoke_benchmark_readiness.json` (sealed)
- `v15_candidate_checkpoint_smoke_benchmark_readiness_report.json`
- `v15_candidate_checkpoint_smoke_benchmark_readiness_checklist.md`

## Public closeout (ledger)

**Closed on `main`:** [PR #171](https://github.com/m-cahill/starlab/pull/171); merge commit **`3bf3fa461e07f023869d511525883a6066f2451c`**; **authoritative PR-head CI** [`25129363401`](https://github.com/m-cahill/starlab/actions/runs/25129363401) (head **`159723009b82c11c86961617d7860add624ae1e0`**); **merge-boundary `main` CI** [`25129578504`](https://github.com/m-cahill/starlab/actions/runs/25129578504) — **success**. **Merge method:** GitHub **merge commit** (**not** squash/rebase). **Superseded failed runs:** none recorded as merge authority for the merged PR-head tip.

**Strongest allowed claim (unchanged):** this contract emits **readiness/refusal** showing whether the **M34** CUDA-probed candidate checkpoint is **structurally ready** for a **future** smoke-benchmark **execution** surface — **readiness does not equal** benchmark execution, benchmark pass, strength evaluation, or checkpoint promotion.

## Related

- **`docs/starlab-v1.5.md`** — **§V15-M35**, **M35 non-claims block**
- **`docs/runtime/v15_candidate_checkpoint_model_load_cuda_probe_v1.md`** — upstream **M33**
