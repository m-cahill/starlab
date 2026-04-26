# STARLAB v1.5 — V15-M14 Evidence Remediation / Operator Evidence Acquisition (runtime v1)

**Milestone:** `V15-M14` — **closed** on `main` (implementation [PR #140](https://github.com/m-cahill/starlab/pull/140), merge `656c07355dfbe2b02d11128cedf344a466b1a5b2` merged **2026-04-26T19:32:50Z** UTC)  
**Authoritative PR-head CI:** [`24963376499`](https://github.com/m-cahill/starlab/actions/runs/24963376499) (head `b9d16183f35b5011e6764114b2ef35987490b5d6`); **merge-boundary `main` CI:** [`24965189902`](https://github.com/m-cahill/starlab/actions/runs/24965189902) on merge `656c0735…` — **success**  
**Contract:** `starlab.v15.evidence_remediation_plan.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_evidence_remediation_plan`

**Default posture:** `evidence_gap_inventory_only` / `operator_evidence_not_collected` — **not** operator execution; **not** v2 authorization.

## Purpose

V15-M14 converts the **V15-M13 no-go / defer decision** into a **deterministic, auditable remediation plan** and **operator evidence acquisition readiness** surface. It answers: *what evidence is still missing, in what order it should be collected, and under what public/private boundaries* — **without** weakening the M13 decision and **without** claiming that operator work has completed.

- **Relates to M13:** optionally binds `v15_v2_go_no_go_decision.json` (`starlab.v15.v2_go_no_go_decision.v1`) by **canonical JSON SHA-256** when `--m13-v2-decision-json` is supplied.
- **Does not:** read checkpoint blobs or weights; parse replays; run live SC2; run GPU training or shakedown; run benchmarks; run XAI inference; run human-panel logic; fabricate receipts.

## Missing evidence categories (gap inventory)

Ten governed gap ids (see emitted `v15_evidence_remediation_plan.json`):

| Gap id | Intent |
| --- | --- |
| `GAP-01-long-gpu-run-receipt` | Long GPU campaign receipt (M08-class) |
| `GAP-02-checkpoint-lineage` | Lineage and resume discipline (M03-class) |
| `GAP-03-promoted-checkpoint` | Promoted candidate + evaluation (M09-class) |
| `GAP-04-training-scale-provenance` | Training-scale provenance and registers (M01/M02-class) |
| `GAP-05-strong-agent-benchmark` | Executed strong-agent benchmark (M05-class) |
| `GAP-06-replay-native-xai-pack` | Real XAI evidence packs (M04/M10-class) |
| `GAP-07-human-benchmark-evidence` | Human panel execution and claim (M06/M11-class) |
| `GAP-08-showcase-release-evidence` | Showcase release pack (M12-class) |
| `GAP-09-v2-readiness-evidence` | Consolidated package for v2 *reconsideration* (M21-class) |
| `GAP-10-rights-and-asset-clearance` | Rights and asset register review |

## Remediation gates (E0–E13)

| Gate id | Intent |
| --- | --- |
| `E0_m13_decision_context` | M13 no-go context recorded; optional M13 JSON SHA binding |
| `E1_evidence_gaps_enumerated` | All gap ids present |
| `E2_operator_private_acquisition_paths` | Operator-local paths declared (not CI execution) |
| `E3_long_gpu_evidence_requirements` | Long GPU requirements (M08 narrative) |
| `E4_checkpoint_lineage_requirements` | Lineage requirements (M03) |
| `E5_promotion_evaluation_evidence_requirements` | Evaluation/promotion requirements (M09) |
| `E6_xai_evidence_requirements` | XAI requirements (M04/M10) |
| `E7_human_benchmark_evidence_requirements` | Human benchmark requirements (M06/M11) |
| `E8_rights_asset_register_touchpoints` | Register touchpoints; no default claim rows |
| `E9_public_private_boundary_preserved` | Public/private boundary |
| `E10_m15_m21_roadmap_recorded` | Proposed M15–M21 roadmap (labels only) |
| `E11_v2_remains_unauthorized` | v2 not authorized in M14 program posture |
| `E12_no_operator_evidence_fabricated` | No fabricated operator evidence in emit |
| `E13_docs_governance_tests_aligned` | Docs + governance pointers |

Gate status vocabulary: `pass`, `warning`, `fail`, `blocked`, `not_evaluated`, `not_applicable`.

## Proposed roadmap (M15–M21)

| Milestone | Title | Status |
| --- | --- | --- |
| `V15-M15` | Operator Evidence Collection Preflight | proposed / not started |
| `V15-M16` | Short GPU / Environment Evidence Collection | proposed / not started |
| `V15-M17` | Long GPU Campaign Evidence Collection | proposed / not started |
| `V15-M18` | Candidate Checkpoint Evaluation Evidence Collection | proposed / not started |
| `V15-M19` | XAI Evidence Collection and Validation | proposed / not started |
| `V15-M20` | Human / Bounded Human Benchmark Evidence Collection | proposed / not started |
| `V15-M21` | v2 Reconsideration Decision | proposed / not started |

These are **proposed** follow-ons after the M13 no-go posture — **not** started and **not** authorized by M14.

## CLI examples

**Default fixture (CI-safe):**

```bash
python -m starlab.v15.emit_v15_evidence_remediation_plan \
  --output-dir out/v15_m14_evidence_remediation
```

**With M13 decision JSON binding:**

```bash
python -m starlab.v15.emit_v15_evidence_remediation_plan \
  --output-dir out/v15_m14_evidence_remediation \
  --m13-v2-decision-json path/to/v15_v2_go_no_go_decision.json
```

## Emitted files

- `v15_evidence_remediation_plan.json` (sealed with `evidence_remediation_plan_sha256`)
- `v15_evidence_remediation_plan_report.json`
- `v15_operator_evidence_acquisition_runbook.md`

## Public / private boundary

**Public-safe:** contract ids, SHA-256 bindings, gap ids, gate statuses, proposed milestone labels, non-claims.

**Not public in committed artifacts:** raw weights, checkpoint blobs, replay paths, videos, saliency tensors, participant records, private operator notes, unsanitized absolute paths.

## Non-claims (required)

V15-M14 does not train a checkpoint; does not promote a checkpoint; does not execute a long GPU campaign; does not run a short GPU shakedown; does not run benchmarks; does not run live SC2; does not run XAI inference; does not run human-panel matches; does not release a showcase agent; does not authorize v2; does not collect operator evidence; and does not commit model weights, checkpoint blobs, raw replays, videos, saliency tensors, participant records, private operator notes, or private paths.

## Closeout expectations

**Public closeout (recorded on `main`):** **`remediation_plan_ready`**; **`evidence_gap_inventory_only`**; **`operator_evidence_not_collected`**; **v2** **not** authorized; **M15**–**M21** **proposed / not started**; **no** long GPU run, short shakedown, checkpoint promotion, benchmark execution, XAI execution, human-panel execution, or showcase release in M14.

At honest closeout, the public record should state **remediation plan ready** with **operator evidence not collected** unless separately evidenced; **v2** remains **not** authorized on the default M14 path; proposed **M15–M21** remain **proposed** until implemented under separate plans.
