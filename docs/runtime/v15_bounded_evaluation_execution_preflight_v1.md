# V15-M44 — Bounded evaluation execution preflight v1 (`starlab.v15.bounded_evaluation_execution_preflight.v1`)

**Milestone:** `V15-M44` — *Bounded Candidate Evaluation Execution Preflight / Dry-Run Harness*  
**Profile:** `starlab.v15.m44.bounded_evaluation_execution_preflight.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m44_bounded_evaluation_execution_preflight`

## Purpose

1. **V15-M44 consumes sealed V15-M43 gate JSON.** Upstream artifact: `v15_bounded_evaluation_gate.json` (`starlab.v15.bounded_evaluation_gate.v1` / `starlab.v15.m43.bounded_evaluation_gate.v1`).

2. **V15-M44 is dry-run / preflight only.** It validates that a deterministic future bounded-evaluation execution plan can be assembled without invoking execution surfaces chartered elsewhere.

3. **V15-M44 does not authorize or execute benchmark work.** Passing this milestone produces planning metadata only (`benchmark_execution_performed` and related booleans remain `false`).

4. **`bounded_evaluation_execution_preflight_ready` means future execution preflight ready, not benchmark pass.** Any “ready” status is bookkeeping for downstream chartering—not an outcome claim about matches, strength, or promotion.

5. **`bounded_evaluation_gate_ready` from M43 remains routing eligibility only.**  
   **M44 treats M43 bounded_evaluation_gate_ready as routing eligibility only.** It is not benchmark success, evaluation execution, strength evaluation, scorecard production, or checkpoint promotion.

6. **All execution/load/promotion booleans emitted by M44 remain `false`** (see sealed JSON), including the carried-forward M43 honesty posture fields **(`m43_evaluation_executed`, `m43_checkpoint_loaded`, `m43_promotion_decision_made`)**.

7. **V15-M44 does not use `torch.load`.**

8. **V15-M44 does not load checkpoint blobs.**

9. **V15-M44 does not run live StarCraft II.**

10. **Future evaluation execution requires a separately chartered milestone** (for example a planned V15-M45 execution surface). M44 does not open that surface by itself.

## Artifacts

- `v15_bounded_evaluation_execution_preflight.json` — sealed preflight record (`artifact_sha256`)
- `v15_bounded_evaluation_execution_preflight_report.json` — report companion over the sealed body minus `artifact_sha256`
- `v15_bounded_evaluation_execution_preflight_checklist.md` — machine-generated checklist (not benchmark execution evidence)

## Profiles

| Profile | `v15_bounded_evaluation_gate.json` | `--dry-run-plan-json` | `--evaluation-environment-json` |
| --- | :---: | :---: | :---: |
| `fixture_ci` | synthesized via upstream M43 fixture bundle | synthesized (in-memory envelope) | synthesized (M43 fixture env) |
| `operator_preflight` | **required** | **required** (embeds `scorecard_protocol`) | **required** |
| `operator_declared` | **required** | **required** | **required** |

**Strict profiles:** `fixture_ci` and `operator_preflight` accept only **clean** M43 `bounded_evaluation_gate_ready`. **`bounded_evaluation_gate_ready_with_warnings`** may yield **`bounded_evaluation_execution_preflight_ready_with_warnings`** only under **`operator_declared`**, with warnings carried forward—never silently upgraded to clean ready.

## Dry-run plan semantics

The `dry_run_plan` block is **declarative and non-executing** (`plan_status`: `constructed_not_executed`). It records planned future artifact filenames, a declared future ladder stage label, metadata-only scorecard/protocol posture, and **metadata-only** environment/protocol prerequisite bindings. M44 does **not** revalidate full M02 or M05 semantics—only structural acceptability of supplied routing metadata for a future plan.

## Forbidden CLI flags

Never execute; emit deterministic refusal rows and keep all execution booleans `false`:

- `--run-benchmark`, `--execute-evaluation`, `--load-checkpoint`, `--run-live-sc2`, `--promote-checkpoint`, `--produce-scorecard-results`, `--run-xai`, `--run-human-panel`, `--release-showcase`, `--authorize-v2`

`--load-checkpoint` maps to `refused_checkpoint_load_request`. `--run-live-sc2` maps to `refused_live_sc2_request`. Other forbidden flags map to `refused_disallowed_execution_request`.

## Non-claims

M44 does **not** execute bounded benchmark matches, produce scorecard **results**, evaluate strength, promote checkpoints, invoke `torch.load`, load checkpoint blobs, run live SC2, run XAI, run human-panel evaluation, release a showcase agent, authorize v2, or execute T2–T5 ladders. **`bounded_evaluation_execution_preflight_ready` is not benchmark success.**

## ensure all documentation is updated as necessary

At milestone closeout, update the V15 ledger (`docs/starlab-v1.5.md`) and minimal pointers in `docs/starlab.md` per program discipline.
