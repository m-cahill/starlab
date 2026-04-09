# M22 Plan — Heuristic Baseline Suite

**Project:** STARLAB  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Milestone:** M22 — Heuristic Baseline Suite  
**Status:** **Complete** — merged to `main` ([PR #23](https://github.com/m-cahill/starlab/pull/23)); see `M22_run1.md` / `M22_summary.md` / `M22_audit.md`.

## Milestone identity

* **Recommended branch:** `m22-heuristic-baseline-suite`

## Why this milestone exists

M22 is the **second governed consumer** of the M20 benchmark contract surface, following M21’s scripted baseline suite. M21 deferred **heuristic baselines** to M22 and deferred the **evaluation runner / tournament harness** to M23. The ledger keeps M22 under explicit non-claims: no benchmark-integrity claim and no new live SC2 proof in CI. The safest step is a **narrow, deterministic, fixture-only heuristic baseline suite**, not an execution runner.

## Milestone objective

Prove that STARLAB can load one valid **M20 benchmark contract** with `measurement_surface: fixture_only`, validate it, and emit a deterministic **heuristic baseline suite** artifact and companion report with embedded **M20-conformant scorecards** for a fixed small set of **heuristic** subjects.

This milestone proves **representation and governed emission** of heuristic baselines under explicit non-claims. It does **not** prove gameplay execution, replay correctness, tournament semantics, benchmark integrity, or live SC2 evaluation.

## Narrow claim to close

> STARLAB can consume a valid M20 benchmark contract and deterministically emit a fixture-only heuristic baseline suite with embedded, M20-valid scorecards for fixed heuristic subjects.

## Explicit non-claims (must remain in docs, contract, tests, and summary)

* No **benchmark integrity** claim  
* No **leaderboard** or competitive-comparison claim beyond provisional fixture-only scorecards  
* No **evaluation runner** or **tournament harness** (M23)  
* No **live SC2** execution in CI  
* No **replay parsing**, **replay↔execution equivalence**, or **s2protocol** involvement  
* No claim that numeric values reflect real SC2 performance  
* No new measurement surface beyond **`fixture_only`**

## In scope

1. Runtime contract for M22 heuristic suite (`docs/runtime/heuristic_baseline_suite_v1.md`)
2. Deterministic product code under `starlab/baselines/` (`heuristic_baseline_*.py`, `emit_heuristic_baseline_suite.py`)
3. CLI emitter for the M22 suite
4. Self-contained fixtures and goldens (`tests/fixtures/m22/` — reuses `tests/fixtures/m21/valid_benchmark_contract.json` as shared M20 contract consumer)
5. Tests for deterministic emission, failure modes, ordering, and boundary guards
6. Governance / ledger / milestone closeout updates

## Out of scope

1. M23 evaluation runner / tournament harness  
2. Real heuristic execution against SC2 or replay artifacts  
3. `starlab.replays`, `starlab.sc2`, or `s2protocol` imports in M22 baseline modules  
4. Benchmark-integrity certification  
5. Any shift away from fixture-driven CI  
6. Any M23 product code beyond stubs seeded at closeout

## Deliverables

### Contract doc

* `docs/runtime/heuristic_baseline_suite_v1.md`

### Product modules

* `starlab/baselines/heuristic_baseline_models.py`
* `starlab/baselines/heuristic_baseline_suite.py`
* `starlab/baselines/heuristic_baseline_scorecards.py`
* `starlab/baselines/emit_heuristic_baseline_suite.py`

### Artifacts

* `heuristic_baseline_suite.json`
* `heuristic_baseline_suite_report.json`

### Fixtures and tests

* `tests/fixtures/m22/` (input benchmark contract via reuse of `m21/valid_benchmark_contract.json` + expected suite/report goldens)
* `tests/test_heuristic_baseline_suite.py`

### Governance and closeout

* `docs/company_secrets/milestones/M22/M22_plan.md` (this file)
* `docs/company_secrets/milestones/M22/M22_toolcalls.md`
* `docs/company_secrets/milestones/M22/M22_run1.md`
* `docs/company_secrets/milestones/M22/M22_summary.md`
* `docs/company_secrets/milestones/M22/M22_audit.md`
* `docs/starlab.md`
* `tests/test_governance.py`
* Seed **M23** stubs only at closeout

## Runtime contract requirements (summary)

* Input benchmark contract MUST pass `validate_benchmark_contract` and have `measurement_surface == "fixture_only"`.
* Suite: `suite_version` = `starlab.heuristic_baseline_suite.v1`, `suite_id`, `benchmark_id`, `benchmark_contract_sha256`, `measurement_surface`, `evaluation_posture` = `fixture_only`, `subjects`, `fixture_cases`, `scorecards`, `warnings`, `non_claims`.
* Two heuristic subjects: `heuristic_economy_first_v1`, `heuristic_pressure_first_v1` (fixed order).
* One fixture case: `fc_m22_001`.
* Scorecards: `validate_benchmark_scorecard`, `evaluation_posture: fixture_only`, `scoring_status: scored`, `comparability_status: provisional`, `subject_kind: heuristic`, metric row order matches contract `metric_definitions`, sorted `warnings` / `non_claims`.
* Report: `report_version` = `starlab.heuristic_baseline_suite_report.v1`, `suite_verdict` = `pass`, counts, `benchmark_contract_sha256`, `failures` empty on success, sorted `warnings` / `non_claims`.
* Canonical JSON, sorted keys, UTF-8, trailing newline; SHA-256 over canonical contract JSON (no trailing newline in hash input) per `sha256_hex_of_canonical_json`.

## Acceptance criteria

1. `docs/runtime/heuristic_baseline_suite_v1.md` exists and matches implemented behavior  
2. CLI emits deterministic `heuristic_baseline_suite.json` and `heuristic_baseline_suite_report.json`  
3. Input contract valid M20 and `fixture_only`  
4. Embedded scorecards validate under M20 helpers  
5. Tests and goldens cover happy path and guarded failure paths  
6. M22 baseline modules have no forbidden replay/runtime imports  
7. Required CI green on PR head and merge boundary (record in `M22_run1.md`)  
8. `docs/starlab.md` updated for narrow M22 proof and explicit non-claims  
9. M23 seeded as **stubs only**

## Suggested PR title

* `M22: heuristic baseline suite`

## Suggested commit style

* Conventional Commits throughout
