# Milestone Summary — M22: Heuristic Baseline Suite

**Project:** STARLAB  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Milestone:** M22 — Heuristic Baseline Suite  
**Status:** *Pending merge — finalize after PR merge and CI*

---

## Objective (narrow claim)

STARLAB can load a valid M20 benchmark contract (`measurement_surface: fixture_only`), validate it, and deterministically emit `heuristic_baseline_suite.json` + `heuristic_baseline_suite_report.json` with embedded M20-valid scorecards for fixed **heuristic** subjects — without evaluation runner, tournament harness, benchmark integrity, replay involvement, or live SC2 in CI.

## Delivered (product)

* `docs/runtime/heuristic_baseline_suite_v1.md`
* `starlab/baselines/heuristic_baseline_models.py`, `heuristic_baseline_suite.py`, `heuristic_baseline_scorecards.py`, `emit_heuristic_baseline_suite.py`
* CLI: `python -m starlab.baselines.emit_heuristic_baseline_suite --benchmark-contract PATH --output-dir OUT`
* Goldens under `tests/fixtures/m22/` (reuses `tests/fixtures/m21/valid_benchmark_contract.json` as shared M20 contract consumer)
* `tests/test_heuristic_baseline_suite.py`

## Evidence

* **PR / CI:** Record authoritative PR-head and merge-boundary workflow runs in `M22_run1.md` after merge.

## Non-claims (preserved)

Benchmark integrity, leaderboard semantics beyond provisional fixture scorecards, evaluation runner (**M23**), live SC2 execution in CI, replay parsing / replay↔execution equivalence, claims that fixture metric values reflect real SC2 performance.

## Next

**M23** — Evaluation runner & tournament harness (**stubs only** until authorized; no M23 product code in M22 closeout).
