# M20 Plan — Benchmark Contract & Scorecard Semantics

**Milestone:** M20  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Recommended branch:** `m20-benchmark-contract-scorecard-semantics`  
**Status:** **Closed** — merged to `main` via [PR #21](https://github.com/m-cahill/starlab/pull/21) (2026-04-09). See `M20_run1.md`, `M20_summary.md`, `M20_audit.md`.

## Intent

Define the **governed contract surface** for STARLAB benchmarks before any real baseline implementation or tournament execution. M20 proves that STARLAB can emit deterministic, validated schemas for:

- a **benchmark contract**
- a **benchmark scorecard**

This milestone establishes what a benchmark *is*, what a scorecard *means*, how comparability is represented, and how future milestones may populate those structures, without yet implementing baselines or a runner.

## Narrow objective

Implement a contract-only milestone that emits deterministic schema artifacts and validates fixture-backed examples for:

1. **One benchmark definition document**
2. **One benchmark scorecard document**

with explicit vocabulary for:

- subject identity
- evaluation posture
- metric definitions
- aggregation semantics
- gating semantics
- comparability status
- scoring status
- non-claims / warnings

## In scope

### Runtime contract

- `docs/runtime/benchmark_contract_scorecard_v1.md`

### Product code

- `starlab/benchmarks/benchmark_contract_models.py`
- `starlab/benchmarks/benchmark_contract_schema.py`
- `starlab/benchmarks/benchmark_scorecard_schema.py`
- `starlab/benchmarks/emit_benchmark_contracts.py`

### Artifacts per CLI invocation

Emit exactly:

- `benchmark_contract_schema.json`
- `benchmark_contract_schema_report.json`
- `benchmark_scorecard_schema.json`
- `benchmark_scorecard_schema_report.json`

### CLI

```text
python -m starlab.benchmarks.emit_benchmark_contracts \
  --output-dir OUT
```

### Fixtures and tests

- `tests/fixtures/m20/`
- `tests/test_benchmark_contracts.py`

Fixtures include:

- one valid sample benchmark contract JSON
- one valid sample benchmark scorecard JSON
- one invalid contract fixture
- one invalid scorecard fixture
- golden emitted schema/report JSON

## Out of scope

Do **not** add any of the following in M20:

- scripted baselines
- heuristic baselines
- evaluation runner
- tournament harness
- leaderboard pages
- live SC2 execution in CI
- replay parsing
- action legality
- benchmark result generation from real runs
- benchmark integrity claims
- baseline performance claims
- M21/M22/M23 product code

## Recommended contract shape

### 1. Benchmark contract schema

Represent one benchmark definition. Includes at minimum:

- `schema_version`
- `benchmark_id`
- `benchmark_version`
- `benchmark_name`
- `subject_kinds_allowed`
- `measurement_surface`
- `input_requirements`
- `metric_definitions`
- `gating_rules`
- `aggregation_policy`
- `scorecard_schema_ref`
- `non_claims`

### 2. Scorecard schema

Represent one benchmark result surface. Includes at minimum:

- `schema_version`
- `benchmark_id`
- `benchmark_version`
- `benchmark_contract_sha256`
- `subject_ref`
- `evaluation_posture`
- `scoring_status`
- `comparability_status`
- `metric_rows`
- `aggregate_scores`
- `gating_outcomes`
- `warnings`
- `non_claims`

## Required controlled vocabularies

### Scoring status

- `scored`
- `unscored`
- `disqualified`

### Comparability status

- `comparable`
- `provisional`
- `non_comparable`

### Measurement surface

- `fixture_only`
- `replay_only`
- `runtime_execution`
- `hybrid`

### Evaluation posture (distinct from measurement surface)

- `contract_only`
- `fixture_only`
- `replay_backed`
- `runtime_backed`
- `hybrid`

### Subject kinds allowed

- `scripted`
- `heuristic`
- `imitation`
- `hierarchical`
- `rl`
- `human_replay`

## Deterministic ordering rules

Locked in the runtime contract:

- benchmark contract top-level keys serialized with canonical JSON
- metric definitions ordered by stable benchmark contract order
- scorecard metric rows ordered by benchmark metric definition order
- warnings and non-claims sorted lexicographically
- reports sorted and emitted canonically

## Failure conditions

The M20 CLI should fail non-zero for:

- internal schema emission error
- invalid generated schema structure
- invalid example fixtures against emitted schemas
- report emission mismatch vs goldens

## Tests

`tests/test_benchmark_contracts.py` covers:

- deterministic schema emission
- valid benchmark contract fixture passes
- valid scorecard fixture passes
- invalid benchmark contract fixture fails
- invalid scorecard fixture fails
- CLI writes all four artifacts
- no `starlab.replays`, `starlab.sc2`, or `s2protocol` imports in M20 benchmark modules

## Acceptance criteria

M20 is complete only when all of the following are true:

- runtime contract doc exists
- both schemas and both reports emit deterministically
- sample contract and scorecard fixtures validate
- invalid fixtures fail as expected
- no replay/runtime stack imports leak into M20 modules
- local `ruff`, `format`, `mypy`, and `pytest` are green
- authoritative PR-head CI is green
- merge-boundary `main` CI is green
- `docs/starlab.md` is updated at closeout
- M21 is seeded as stubs only

## Copy-paste handoff block

```md
# M20 Plan — Benchmark Contract & Scorecard Semantics

Objective:
Prove a narrow, deterministic contract surface for STARLAB benchmarks by emitting and validating governed schemas for one benchmark definition and one benchmark scorecard, without implementing scripted baselines, heuristic baselines, evaluation runner logic, tournament harness behavior, or benchmark integrity claims.

In scope:
- `docs/runtime/benchmark_contract_scorecard_v1.md`
- `starlab/benchmarks/benchmark_contract_models.py`
- `starlab/benchmarks/benchmark_contract_schema.py`
- `starlab/benchmarks/benchmark_scorecard_schema.py`
- `starlab/benchmarks/emit_benchmark_contracts.py`
- CLI to emit:
  - `benchmark_contract_schema.json`
  - `benchmark_contract_schema_report.json`
  - `benchmark_scorecard_schema.json`
  - `benchmark_scorecard_schema_report.json`
- fixtures/goldens under `tests/fixtures/m20/`
- `tests/test_benchmark_contracts.py`
- governance/doc updates at closeout only

Out of scope:
- scripted baselines
- heuristic baselines
- evaluation runner
- tournament harness
- leaderboard/public ranking
- live SC2 in CI
- replay parsing
- benchmark integrity claims
- M21/M22/M23 product code

Required vocabularies:
- scoring status: `scored`, `unscored`, `disqualified`
- comparability status: `comparable`, `provisional`, `non_comparable`
- measurement surface: `fixture_only`, `replay_only`, `runtime_execution`, `hybrid`

Acceptance criteria:
- deterministic emission of both schemas and both reports
- valid sample benchmark contract fixture passes
- valid sample benchmark scorecard fixture passes
- invalid fixtures fail correctly
- no replay/runtime-stack imports in M20 benchmark modules
- green local checks and green authoritative CI
- `docs/starlab.md` updated at closeout
- M21 stubs seeded only
```
