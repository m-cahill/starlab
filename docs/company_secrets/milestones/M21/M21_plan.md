# M21 Plan — Scripted Baseline Suite

**Milestone:** M21  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Status:** **Closed** — merged to `main` ([PR #22](https://github.com/m-cahill/starlab/pull/22)); see `M21_run1.md`, `M21_summary.md`, `M21_audit.md`.  
**Recommended branch:** `m21-scripted-baseline-suite` (merged)

## Objective

Prove a narrow, deterministic scripted baseline suite as the first real consumer of the M20 benchmark contract by loading one valid fixture-only benchmark contract, generating a small fixed set of scripted baseline subjects, and emitting a deterministic suite artifact with embedded M20-conformant scorecards, without implementing heuristic baselines, evaluation runner logic, tournament harness behavior, live SC2 execution, or benchmark integrity claims.

## In scope

- `docs/runtime/scripted_baseline_suite_v1.md`
- `starlab/baselines/__init__.py`
- `starlab/baselines/scripted_baseline_models.py`
- `starlab/baselines/scripted_baseline_suite.py`
- `starlab/baselines/scripted_baseline_scorecards.py`
- `starlab/baselines/emit_scripted_baseline_suite.py`
- CLI to emit:
  - `scripted_baseline_suite.json`
  - `scripted_baseline_suite_report.json`
- self-contained fixtures/goldens under `tests/fixtures/m21/`
- `tests/test_scripted_baseline_suite.py`
- governance/doc updates at closeout only

## Locked posture

- input benchmark contract must validate against the M20 contract schema
- input benchmark contract `measurement_surface` must be `fixture_only`
- emitted scorecards must use:
  - `evaluation_posture: fixture_only`
  - `scoring_status: scored`
  - `comparability_status: provisional`
- emitted subject kinds must be `scripted`

## Out of scope

- heuristic baselines
- evaluation runner
- tournament harness
- leaderboard/public ranking
- live SC2 in CI
- replay parsing
- benchmark integrity claims
- replay↔execution equivalence claims
- M22/M23 product code

## Acceptance criteria

- deterministic emission of suite + report
- valid fixture benchmark contract passes
- invalid contract fails correctly
- all embedded scorecards validate against M20 scorecard schema
- no replay/runtime-stack imports in M21 baseline modules
- green local checks and green authoritative CI
- `docs/starlab.md` updated at closeout
- M22 stubs seeded only
