# PV1 post-campaign readout v1 (PV1-M04)

## Purpose

**PV1-M04** adds a **bounded, deterministic readout** over an **existing** `out/training_campaigns/<campaign_id>/` tree — **analysis and aggregation only**. It packages comparative evidence references for audits and handoffs **without** new SC2 execution, new tranche runs, or threshold reinterpretation.

## Inputs

The readout **consumes** artifacts already written under the campaign root (and optional operator markdown at the root):

| Input | Role |
| --- | --- |
| M49 **`full_local_training_campaign_contract.json`** | `campaign_id` and contract anchor (via PV1-M01 scan) |
| **PV1-M01** `campaign_observability_index` / report (computed fresh) | Execution counts, checkpoint paths, watchable counts, `index_status` |
| **`tranche_a_operator_note.md`** | Tranche A posture + `execution_id` (table row) |
| **`tranche_b_operator_note.md`** | Tranche B posture + `execution_id` |
| **`full_run_threshold_declaration.md`** | **`threshold-met`** / **`threshold-not-met`** heading + honest rationale text |

The emitter is:

`python -m starlab.training.emit_pv1_post_campaign_readout --campaign-root <dir> [--output-dir <dir>]`

Default outputs: **`pv1_post_campaign_readout.json`** and **`pv1_post_campaign_readout_report.json`** in `--campaign-root` unless `--output-dir` overrides (useful for CI fixtures).

## Terminology

| Term | Meaning |
| --- | --- |
| **Tranche posture** | Operator-authored **execution** conclusion per tranche from the relevant `tranche_*_operator_note.md` — e.g. **completed within scope**. Distinct from **threshold** posture. |
| **Threshold posture** | Operator-authored full-run outcome from **`full_run_threshold_declaration.md`** — **`threshold-met`** or **`threshold-not-met`** vs the **frozen** PV1 threshold block. |
| **Comparative readout** | One JSON surface tying **Tranche A vs Tranche B** execution references + PV1-M01 inventory + threshold declaration pointers — **not** a new benchmark or ladder scorecard. |

## Allowed readout lessons

Structured **`bounded_lessons`** / **`follow_on_questions`** fields may be filled with **governance- or inspection-level** notes (e.g. separating tranche success from duration semantics). They must **not** read as empirical generalization, global benchmark claims, or ladder/public strength.

## Explicit non-claims

The readout **does not** prove or imply:

- Global benchmark integrity, universal replay↔execution equivalence, ladder/public strength, live SC2 in CI as merge norm, or multi-environment readiness.
- That **`threshold-not-met`** should be reinterpreted without a **new charter / governance decision**.
- Any **new** execution success beyond what **PV1-M02** / **PV1-M03** already established.

## `campaign_result_summary`

The readout includes a stable **`campaign_result_summary`** block (`summary_line` + structured `tuple`) so fresh-chat orientation can recover the **bounded** PV1 outcome without hand-parsing multiple sections — still subject to the same non-claims and to operator-authored source files.
