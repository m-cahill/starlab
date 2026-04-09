# M23 Plan — Evaluation Runner & Tournament Harness

**Milestone:** M23  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Status:** **Implementation** on branch `m23-evaluation-runner-tournament-harness` (merge + CI **pending**).

## Objective

Prove the **first governed evaluation consumer** of the benchmark surface by loading one valid **M20** benchmark contract together with governed **M21** scripted and **M22** heuristic fixture-only baseline suite artifacts, then deterministically emitting **`evaluation_tournament.json`** and **`evaluation_tournament_report.json`** under explicit non-claims.

## Delivered (product)

* Runtime contract: `docs/runtime/evaluation_runner_tournament_harness_v1.md`
* Modules: `starlab/evaluation/` (`evaluation_runner_models.py`, `evaluation_runner.py`, `tournament_harness.py`, `emit_evaluation_tournament.py`)
* CLI: `python -m starlab.evaluation.emit_evaluation_tournament --benchmark-contract PATH --suite PATH ... --output-dir OUT`
* Fixtures: `tests/fixtures/m23/expected_*.json`
* Tests: `tests/test_evaluation_tournament.py` (goldens, validation, ordering, import guard, **M20→M21/M22→M23** E2E)

## Locked semantics (summary)

* Pairwise **win/loss/draw** from **`scoring_role: primary`** metric only; full metric rows recorded.
* Points: **1.0 / 0.5 / 0.0** (win / draw / loss).
* Suite validation: **structural** (no new suite JSON Schema in M23).
* **No** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M23 evaluation modules.

## Closeout (pending merge)

* Fill **PR #**, **SHAs**, **authoritative CI** in `docs/starlab.md` §3 / §18 / §23.
* Generate `M23_run1.md`, `M23_summary.md`, `M23_audit.md` per company prompts.
