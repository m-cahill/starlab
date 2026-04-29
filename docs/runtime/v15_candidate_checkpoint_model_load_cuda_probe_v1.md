# V15-M33 — Candidate checkpoint model-load and CUDA inference probe (v1)

**Contract:** `starlab.v15.candidate_checkpoint_model_load_cuda_probe.v1`  
**Profile:** `starlab.v15.m33.candidate_checkpoint_model_load_cuda_probe.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m33_candidate_checkpoint_model_load_cuda_probe`

## Purpose

M33 is the first milestone that may **read checkpoint blobs**, **load** a governed **M28/M29**-style PyTorch artifact (`{"model_state_dict": ...}`), and run **one minimal forward pass** on **`cpu`** or **`cuda`**, after **SHA-256** verification against:

1. The **`--expected-candidate-sha256`** CLI argument (must match **M32** `candidate_checkpoint.sha256`), and  
2. The on-disk file hash.

**Load order:** verification of (1) and (2) completes **before** any **`torch.load`** of checkpoint bytes.

M32 execution JSON must be a sealed **`starlab.v15.candidate_checkpoint_evaluation_execution.v1`** with `execution_status` in the completed fixture or operator-local metadata set, with **`benchmark_passed`**, **`strength_evaluated`**, **`checkpoint_promoted`**, and **`scorecard_execution_performed`** all **`false`**.

## Modes

### Fixture CI (`--fixture-ci`)

Emits **`fixture_schema_only_no_checkpoint_blob`**. No M32 file, no checkpoint path, no CUDA requirement.

### Operator-local

Requires:

- `--allow-operator-local-execution`
- `--authorize-candidate-model-load-probe`
- `--m32-evaluation-execution-json`
- `--candidate-checkpoint-path`
- `--expected-candidate-sha256` (must match the **M29-class** public candidate example `eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26` when consuming the default **CI fixture** chain)
- `--device cuda|cpu` (default `cuda`)

Use **`.venv`** Python for **`cuda`** on Windows; default **PATH** Python may be CPU-only (see **M23** ledger).

## Non-claims

M33 does **not** train, run a **72-hour** campaign, run live SC2 matches, execute a benchmark, produce scorecard results, evaluate strength, promote the checkpoint, run XAI, run human-panel evaluation, release a showcase agent, or authorize **v2** / **T2** / **T3**.

## Artifacts

- `v15_candidate_checkpoint_model_load_cuda_probe.json` (sealed)
- `v15_candidate_checkpoint_model_load_cuda_probe_report.json`
- `v15_candidate_checkpoint_model_load_cuda_probe_checklist.md`

## Related

- **`docs/starlab-v1.5.md`** — **§V15-M33**, **M33 non-claims block**
- **`docs/runtime/v15_candidate_checkpoint_evaluation_execution_v1.md`** — upstream **M32**
