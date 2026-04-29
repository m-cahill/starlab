# V15-M31 — Candidate checkpoint evaluation harness gate (runtime)

**Milestone:** `V15-M31`  
**Contract family:** `starlab.v15.candidate_checkpoint_evaluation_harness_gate.v1`  
**Profile:** `starlab.v15.m31.evaluation_harness_dry_run_gate.v1`

## Role

Consumes a sealed **V15-M30** **`starlab.v15.candidate_checkpoint_evaluation_package.v1`** artifact (SC2-backed profile) and emits a **deterministic dry-run gate** showing that STARLAB can validate the package, bind optional **M05** strong-agent protocol metadata at the gate, and construct a **dry-run evaluation plan** without executing benchmarks, matches, or strength measurement.

**Posture:** **`evaluation_harness_ready` ≠ `benchmark_passed`** — the gate only proves metadata routing and checklist construction for a **future** bounded evaluation milestone (e.g. **V15-M32**), not a benchmark result.

## Non-claims

M31 does **not** run live SC2 benchmark matches; does **not** measure strength; does **not** promote checkpoints; does **not** load checkpoint weight blobs; does **not** run XAI or human-panel evaluation; does **not** release showcase agents; does **not** authorize **v2** or **T2**/**T3**; does **not** execute scorecards (only optional protocol metadata bind when supplied).

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| Exactly one of `--fixture-ci` or `--m30-evaluation-package-json` | yes | Mutually exclusive modes |
| `--m30-evaluation-package-json` | when not fixture | Sealed M30 package JSON with profile `starlab.v15.m30.sc2_backed_candidate_checkpoint_evaluation_package.v1` |
| `--m05-scorecard-json` | optional | M05 protocol JSON; if valid, `scorecard_binding_status` = `bound_in_m31`; if omitted, `optional_not_supplied` |
| `--output-dir` | yes | Writable output directory (local `out/**` not committed) |

## Outputs

| File | Purpose |
| --- | --- |
| `v15_candidate_checkpoint_evaluation_harness_gate.json` | Sealed gate JSON |
| `v15_candidate_checkpoint_evaluation_harness_gate_report.json` | Report digest summary |
| `v15_candidate_checkpoint_evaluation_harness_gate_checklist.md` | Gates G0–G8 |

## CLI

```powershell
python -m starlab.v15.emit_v15_m31_candidate_checkpoint_evaluation_harness_gate `
  --fixture-ci `
  --output-dir out\v15_m31\fixture_ci
```

```powershell
python -m starlab.v15.emit_v15_m31_candidate_checkpoint_evaluation_harness_gate `
  --m30-evaluation-package-json <path\to\v15_candidate_checkpoint_evaluation_package.json> `
  --output-dir out\v15_m31\eval_harness_gate1
```

Optional M05:

```powershell
python -m starlab.v15.emit_v15_m31_candidate_checkpoint_evaluation_harness_gate `
  --m30-evaluation-package-json <path\to\v15_candidate_checkpoint_evaluation_package.json> `
  --m05-scorecard-json <path\to\v15_strong_agent_scorecard.json> `
  --output-dir out\v15_m31\eval_harness_gate1
```

## Gate outcomes

- **Success:** `gate_status`: `evaluation_harness_dry_run_ready`, `evaluation_harness_ready`: `true`
- **Blocked:** `gate_status`: `evaluation_harness_refused_with_blockers`, `evaluation_harness_ready`: `false`, sorted `blocked_reasons`

## Dry-run semantics

`dry_run_evaluation_plan` is **constructed, not executed**: no model load, no matches, no scorecard execution results.

## Public / private boundary

Emitters must not copy raw operator absolute paths into public JSON. Upstream string fields that look like local path leaks are replaced with a redacted sentinel in the gate artifact.

## Recommended next

**V15-M32 — Candidate checkpoint evaluation execution** (provisional until chartered) — bounded fixture or operator-authorized evaluation consumes this gate **without** implying promotion or broader claims by default.
