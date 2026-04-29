# V15-M37 — Two-hour run blocker discovery (`starlab.v15.two_hour_run_blocker_discovery.v1`)

## Purpose

**V15-M37 does not execute the 2-hour run.** It discovers blockers and readiness gaps for a future **V15-M39** operator-local attempt (**7200 seconds** SC2-backed T1 continuation / candidate-training posture aligned with the **M29/M34** candidate lineage).

**M39 is intended** to be a **2-hour SC2-backed T1 continuation / candidate-training run** from that lineage, **not** a benchmark-pass or strength claim.

## Contract / profile

- **Contract:** `starlab.v15.two_hour_run_blocker_discovery.v1`
- **Profile:** `starlab.v15.m37.two_hour_run_operator_readiness_audit.v1`
- **Emitter:** `python -m starlab.v15.emit_v15_m37_two_hour_run_blocker_discovery`

## Modes

### Fixture CI (`--fixture-ci`)

Emit deterministic artifacts with **`audit_status`** **`fixture_schema_only_no_operator_audit`**. Suitable for merge-gate CI (schema, sealing, governance tests).

### Operator audit (`--profile operator_audit`)

Requires **`--allow-operator-local-inspection`** to probe git workspace hygiene, disk free space (against **`--min-free-disk-gb`**), CUDA/torch/sc2/`nvidia-smi` posture when safe.

Supply sealed lineage JSON paths as documented by the emitter CLI.

## Inputs

Minimum operator narrative binds:

- **`--m29-full-run-json`** — sealed M29 full-run JSON (cadence extrapolation prefers JSON fields over ledger constants).
- **`--m34-cuda-probe-json`** — sealed **M33/M34** CUDA probe JSON (`starlab.v15.candidate_checkpoint_model_load_cuda_probe.v1`).
- **`--m35-readiness-json`** — sealed M35 readiness JSON.

Optional enrichment:

- **`--m36-smoke-execution-json`** — if supplied, validated/bound; if omitted, **`m36_smoke_execution_binding_status`** is **`optional_not_supplied`** (informational-only blocker).

Optional checkpoint presence:

- **`--candidate-checkpoint-path`** — existence check only (no `torch.load`).
- **`--authorize-checkpoint-file-sha256`** — fingerprint `.pt` file SHA when explicitly authorized.

## Blocker categories

Covers workspace/git hygiene, private governance surface posture (existence-only — **no** prompt contents emitted), CUDA/Python environment, SC2 import surface, candidate SHA lineage across sealed JSON, artifact seals, runner ↔ **7200s** horizon posture (including **M29** **1800s** horizon classifier discovery), checkpoint cadence / storage extrapolation, disk/output posture, stop/resume keyword scan (non-exhaustive), telemetry planning hints.

## Gate pack R0–R12

**R0** Workspace · **R1** Private governance · **R2** CUDA · **R3** SC2 import · **R4** Candidate identity · **R5** Artifact chain/seals · **R6** Runner **7200s** compatibility · **R7** Checkpoint cadence · **R8** Disk/retention · **R9** Stop/resume posture · **R10** Monitoring · **R11** Runbook draft emitted · **R12** Non-claims / claim flags false.

Statuses follow the emitter vocabulary (**pass** / **fail** / **unknown** / operator-only gates).

## Artifact outputs

- `v15_two_hour_run_blocker_discovery.json`
- `v15_two_hour_run_blocker_discovery_report.json`
- `v15_two_hour_run_blocker_discovery_checklist.md`
- `v15_m38_remediation_map.md`
- `v15_m39_candidate_runbook_draft.md`

## Operator command examples

Fixture CI:

```powershell
python -m starlab.v15.emit_v15_m37_two_hour_run_blocker_discovery `
  --fixture-ci `
  --output-dir out/v15_m37_fixture
```

Operator audit (illustrative):

```powershell
python -m starlab.v15.emit_v15_m37_two_hour_run_blocker_discovery `
  --profile operator_audit `
  --allow-operator-local-inspection `
  --expected-candidate-sha256 eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26 `
  --m29-full-run-json <path> `
  --m34-cuda-probe-json <path> `
  --m35-readiness-json <path> `
  --target-wall-clock-seconds 7200 `
  --output-dir out/v15_m37_operator_audit
```

## Relationship to M36

**M36** remains the governed smoke execution/refusal bookkeeping surface (**not** the two-hour run). **M37** may optionally bind sealed **M36** JSON when supplied.

## Relationship to M38 and M39

- **V15-M37:** blocker discovery / readiness audit (**this milestone**).
- **V15-M38:** remediation + launch rehearsal (**future**).
- **V15-M39:** optional operator-local **7200s** attempt (**future**).

## Checkpoint cadence risk

When **M29-equivalent** cadence extrapolates to extremely large checkpoint counts for **7200s**, **V15-M37** emits **`checkpoint_cadence_too_high`** unless explicit retention/pruning controls are detected in-scanner — **M38** owns remediation.

## Public/private boundary

Operator-local paths may feed validation but must stay **redacted** from emissions via existing STARLAB path hygiene checks.

## Non-claims

The sealed JSON **`claim_flags`** remain **false** for benchmark execution/pass, strength evaluation, checkpoint promotion, scorecards, XAI, human-panel, showcase, **v2**, **T2/T3**, and executed two-hour runs.
