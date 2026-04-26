# V15-M16 — Short GPU / environment evidence (runtime)

**Milestone:** `V15-M16`  
**Status:** closed on `main` (see `docs/starlab-v1.5.md` for authoritative program record; [PR #142](https://github.com/m-cahill/starlab/pull/142); merge-boundary `main` CI [`24968604458`](https://github.com/m-cahill/starlab/actions/runs/24968604458))  
**Contract:** `starlab.v15.short_gpu_environment_evidence.v1`

## Dependency on M15

M15 (**`starlab.v15.operator_evidence_collection_preflight.v1`**) closed with **`preflight_plan_ready`**, **`operator_evidence_collection_status: not_started`**, and **v2** not authorized. M16 is the first milestone that may record **operator-local** environment / short-GPU evidence; it does **not** imply M15 collection progressed unless optional **`--m15-preflight-json`** binds an honest M15 artifact by SHA.

## Purpose

Answer: *Is the operator environment sufficiently evidenced for short GPU / environment readiness (bounded), without starting the full long GPU campaign?*

## Emitter

Default (CI-safe fixture):

```bash
python -m starlab.v15.emit_v15_short_gpu_environment_evidence \
  --output-dir out/v15_m16_short_gpu_environment
```

Operator-declared metadata only (no torch execution):

```bash
python -m starlab.v15.emit_v15_short_gpu_environment_evidence \
  --profile operator_declared \
  --output-dir out/v15_m16_short_gpu_environment \
  --operator-environment-json path/to/operator_environment.json
```

Operator-local bounded probe (**dual guards required**):

```bash
python -m starlab.v15.emit_v15_short_gpu_environment_evidence \
  --profile operator_local_short_gpu_probe \
  --output-dir out/v15_m16_short_gpu_environment \
  --allow-operator-local-execution \
  --authorize-short-gpu-probe \
  --device cuda \
  --max-steps 5
```

Optional SHA-only upstream bindings:

```bash
--m02-environment-lock-json <path>
--m07-training-run-receipt-json <path>
--m08-long-gpu-manifest-json <path>
--m15-preflight-json <path>
```

## Emitted files

- `v15_short_gpu_environment_evidence.json` (sealed with `artifact_sha256`)
- `v15_short_gpu_environment_evidence_report.json`
- `v15_short_gpu_environment_checklist.md`

## Profiles

| Profile | CUDA / torch in emit | Use |
| --- | --- | --- |
| `fixture_ci` (default) | No torch import | CI and deterministic wiring |
| `operator_declared` | No GPU code | Normalize/redact declared JSON |
| `operator_local_short_gpu_probe` | Lazy torch import | Bounded tensor steps; **both** `--allow-operator-local-execution` and `--authorize-short-gpu-probe` |

## Upstream binding semantics

- **M02** (`starlab.v15.long_gpu_environment_lock.v1`): canonical JSON SHA only; M02 does **not** authorize a long run.
- **M07** (`starlab.v15.training_run_receipt.v1`): SHA + readonly profile; not reinterpreted as M08 campaign completion.
- **M08** (`starlab.v15.long_gpu_training_manifest.v1`): SHA + manifest role **implementation_preflight_manifest_tooling**; not a completed long run without operator receipts.
- **M15** (`starlab.v15.operator_evidence_collection_preflight.v1`): SHA; requires **`operator_evidence_collection_status: not_started`**, **v2** flags false, full **P0–P14** gates and **S0–S10** sequence rows.

## Readiness gates (G0–G12)

Gate rows are emitted in `readiness_gates` (see artifact). Examples: **G0** M15 preflight bound; **G4–G6** torch/CUDA/GPU posture; **G7** short probe bounded when run; **G12** conservative **`m17_opening_recommendation`**.

## M17 opening recommendation vocabulary

Examples recorded in `m17_opening_recommendation`:

- `blocked_pending_operator_evidence` (default fixture)
- `blocked_cuda_unavailable`
- `blocked_missing_m15_preflight`
- `blocked_missing_rights_or_asset_register_review`
- `ready_for_m17_planning`
- `ready_for_m17_operator_preflight_only`

**M16 must not** emit **`long_gpu_run_authorized: true`**. M17 owns long GPU campaign evidence.

## Public / private boundary

Documented in the JSON `public_private_boundary` map. **Public-safe:** contract IDs, logical names, SHA bindings, gate IDs, non-claims. **Private/local-only:** absolute paths, SC2 install paths, raw media, weights, checkpoints, replays, participant data.

## Register touchpoints

The artifact lists: `docs/rights_register.md`, `docs/training_asset_register.md`, `docs/replay_corpus_register.md`, `docs/model_weight_register.md`, `docs/checkpoint_asset_register.md`, `docs/xai_evidence_register.md`, `docs/human_benchmark_register.md`.

## Non-claims

M16 is **bounded environment / short-GPU evidence** only. It is **not** a completed long GPU run, **not** strong-agent or benchmark proof, **not** XAI or human-panel execution, **not** v2 authorization. See **`docs/starlab-v1.5.md`** (**M16 non-claims** block).

## Closeout expectations

**Closed on `main`** — [PR #142](https://github.com/m-cahill/starlab/pull/142); merge commit `bb7e6e11e800269b63ab80a7ade316dc1165c8a6`; PR-head CI [`24968275296`](https://github.com/m-cahill/starlab/actions/runs/24968275296); merge-boundary `main` CI [`24968604458`](https://github.com/m-cahill/starlab/actions/runs/24968604458). Public closeout documentation may follow in a separate docs commit (recorded in private milestone summary). **`docs/starlab-v1.5.md`** remains authoritative.
