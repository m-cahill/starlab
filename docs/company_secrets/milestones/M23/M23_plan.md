# M23 Plan — Evaluation Runner & Tournament Harness

**Milestone:** M23  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Status:** **Closed** — merged to `main` ([PR #24](https://github.com/m-cahill/starlab/pull/24)); see `M23_summary.md`, `M23_audit.md`, `M23_run1.md`.

## Objective

Prove the **first governed evaluation consumer** of the benchmark surface by loading one valid **M20** benchmark contract together with governed **M21** scripted and **M22** heuristic fixture-only baseline suite artifacts, then deterministically emitting **`evaluation_tournament.json`** and **`evaluation_tournament_report.json`** under explicit non-claims.

## Delivered (product)

* Runtime contract: `docs/runtime/evaluation_runner_tournament_harness_v1.md`
* Modules: `starlab/evaluation/` (`evaluation_runner_models.py`, `evaluation_runner.py`, `tournament_harness.py`, `emit_evaluation_tournament.py`)
* CLI: `python -m starlab.evaluation.emit_evaluation_tournament --benchmark-contract PATH --suite PATH ... --output-dir OUT`
* Fixtures: `tests/fixtures/m23/expected_*.json`
* Tests: `tests/test_evaluation_tournament.py` (goldens, validation, ordering, import guard, **M20→M21/M22→M23** E2E)

## Locked semantics (summary)

* Pairwise **win/loss/draw** from **`scoring_role: primary`** metric only; full metric comparison rows recorded.
* Points: **1.0 / 0.5 / 0.0** (win / draw / loss).
* Suite validation: **structural** (no new suite JSON Schema in M23).
* **No** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M23 evaluation modules.

## Closeout

* **Merged:** 2026-04-09T07:41:53Z (UTC) — PR #24 — merge commit `b8857d2ccfdb2963d4fd2311f98d02cbe79aa252`
* **Authoritative PR-head CI:** [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859)
* **Merge-boundary `main` CI:** [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940)
