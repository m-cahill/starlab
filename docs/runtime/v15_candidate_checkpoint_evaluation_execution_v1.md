# V15-M32 — Bounded candidate checkpoint evaluation execution (runtime)

**Milestone:** `V15-M32`  
**Contract family:** `starlab.v15.candidate_checkpoint_evaluation_execution.v1`  
**Profile:** `starlab.v15.m32.bounded_candidate_evaluation_execution.v1`

## Role

Consumes a sealed **`§V15-M31`** **`starlab.v15.candidate_checkpoint_evaluation_harness_gate.v1`** artifact (**dry-run gate**) and emits a **bounded evaluation execution** receipt (**fixture** or **metadata-only operator-local**). Proves the STARLAB pipeline can proceed **`§V30` package → `§M31` harness gate → `§M32` bounded execution** artifact emission **without** claiming benchmark pass, strength evaluation, checkpoint promotion, live tournaments, checkpoint blob load, or CUDA inference.

**Important nuance:** bounded evaluation execution **≠ strong-agent benchmark pass.** **`evaluation_execution_performed`**: **`true`** only denotes bounded harness/metadata execution (**fixture** path included).

## Execution levels

| Level | Mode | Checkpoint blobs loaded |
| --- | --- | --- |
| **1 — Fixture** | `--fixture-ci` with deterministic synthetic **`§V31`** internally (**matches **`§M31`** fixture pipeline**) | No |
| **2 — Operator-local metadata** | `--m31-harness-gate-json` + `--execution-mode metadata_only` (default for this path) | No |

**V15-M33** is the intended first **checkpoint blob / model-load / CUDA inference probe** milestone (explicit operator authorization; no strength claim by default). **M32** does **not** load weights or run SC2 matches.

## Non-claims

M32 does **not** pass or execute **strong-agent** benchmarks; does **not** produce scorecard **results**; does **not** measure strength; does **not** promote checkpoints; does **not** load checkpoint weight blobs; does **not** run live SC2 evaluation; does **not** run XAI or human-panel evaluation; does **not** release showcase agents; does **not** authorize **v2** or **T2**/**T3**. Scorecard protocol status is **inherited from the M31 gate** (`inherited_from_m31_*`).

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Exactly one of `--fixture-ci` or `--m31-harness-gate-json` | yes | Mutually exclusive |
| `--m31-harness-gate-json` | when not fixture | Canonical sealed **`v15_candidate_checkpoint_evaluation_harness_gate.json`** from **`§V15-M31`** |
| `--execution-mode` | optional | With **`--fixture-ci`**: **`fixture`** or omit (defaults fixture). With **`--m31-harness-gate-json`**: **`metadata_only`** or omit (defaults metadata-only). |
| `--max-evaluation-cases` | optional | Default **`1`** (bounded cap; metadata/fixture probe only). |
| `--output-dir` | yes | Writable output directory (**`out/**`** local-only — **not committed**) |

Operator-local **`§V31`** JSON paths must exist as supplied — **no** silent substitution with fixture paths.

## Outputs

| File | Purpose |
| --- | --- |
| `v15_candidate_checkpoint_evaluation_execution.json` | Sealed execution JSON |
| `v15_candidate_checkpoint_evaluation_execution_report.json` | Report digest summary |
| `v15_candidate_checkpoint_evaluation_execution_checklist.md` | Checklist gates |

## CLI

Fixture CI (**deterministic **`§V31`** internally → **`§M32`** bounded execution**):

```powershell
python -m starlab.v15.emit_v15_m32_candidate_checkpoint_evaluation_execution `
  --fixture-ci `
  --output-dir out\v15_m32\fixture_ci
```

Operator-local **`§V31`** harness gate (**canonical seal verified dynamically — operator digest ≠ fixture anchor unless running the same fixture chain**):

```powershell
python -m starlab.v15.emit_v15_m32_candidate_checkpoint_evaluation_execution `
  --m31-harness-gate-json out\v15_m31\evaluation_harness_dry_run1\v15_candidate_checkpoint_evaluation_harness_gate.json `
  --output-dir out\v15_m32\candidate_evaluation_execution_run1
```

## Execution outcomes

| Status | Meaning |
| --- | --- |
| **`candidate_evaluation_execution_fixture_completed`** | **`--fixture-ci`** success |
| **`candidate_evaluation_execution_operator_local_metadata_completed`** | Valid sealed **`§V31`** consumed without checkpoint blob load |
| **`candidate_evaluation_execution_refused_with_blockers`** | Validation/blocker refusal (**sorted **`blocked_reasons`**) |

## Blockers (representative)

**`blocked_invalid_m31_contract`**, **`blocked_invalid_m31_profile`**, **`blocked_m31_gate_not_ready`**, **`blocked_m31_claim_flags_inconsistent`**, **`blocked_m31_candidate_checkpoint_*`**, **`blocked_m31_dry_run_plan_missing`**, **`blocked_private_path_leak_detected`**, etc. — see governance tests and emitter validation.

## Public / private boundary

Emitters must not copy raw operator absolute paths into public JSON. Content resembling forbidden local path patterns triggers refusal / hygiene rebuild where applicable (**`§M31`** / **`§M30`** path discipline applies upstream).

## Relationship to **`§V30`** / **`§V31`**

**`§V31`** consumes **`§V30`** sealed packages (**dry-run plan only). **`§M32`** consumes **`§V31`** (**execution harness step** — still **not** benchmark execution).

## Recommended next (**provisional**)

**V15-M33 — Candidate checkpoint model-load and CUDA inference probe** — first governed checkpoint blob / **`torch`** load (**dual-guard**), **explicit operator authorization**, **no** benchmark / promotion claim by default.
