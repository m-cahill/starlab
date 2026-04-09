# M24 Plan — Attribution, Diagnostics, and Failure Views

**Milestone:** M24  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Status:** Active — product implementation authorized.

## Objective

**M24** is the **first diagnostic consumer** of the Phase IV evaluation chain. It consumes a valid **M23** `evaluation_tournament.json` and emits a deterministic, offline **diagnostic view pack** that explains:

- how tournament standings were derived,
- how each entrant’s results break down match-by-match,
- where wins, losses, and draws came from under the benchmark contract,
- what fixture-only limitations and non-claims still apply.

**Strictly offline and fixture-only.** No benchmark-integrity claims, no replay↔execution equivalence, no live SC2, no replay parsing, no new baseline emitters, no new tournament semantics, no evidence-pack packaging (**M25**).

## Narrow claim

STARLAB can load one valid **M23** `evaluation_tournament.json`, validate it against the governed M20–M23 posture, derive deterministic **attribution, diagnostics, and failure-view artifacts**, and emit governed canonical JSON outputs that explain tournament outcomes **without changing tournament semantics**.

## Product surface

- Runtime contract: `docs/runtime/evaluation_diagnostics_failure_views_v1.md`
- Modules: `starlab/evaluation/diagnostics_models.py`, `diagnostics_views.py`, `emit_evaluation_diagnostics.py`
- Artifacts: `evaluation_diagnostics.json`, `evaluation_diagnostics_report.json`
- Tests: `tests/fixtures/m24/`, `tests/test_evaluation_diagnostics.py`
- Governance: `tests/test_governance.py`, `docs/starlab.md`, milestone closeout artifacts when merged

## Validation posture

No new JSON Schema for M23 input in M24. Structural + semantic validation only (version, fixture-only posture, required fields, internal consistency, ordering).

## Definition of done

See acceptance criteria in the milestone brief: contract + deterministic artifacts + goldens + E2E chain test through M24 + import guard + quality gates + ledger updates + **M25 stubs only**.
