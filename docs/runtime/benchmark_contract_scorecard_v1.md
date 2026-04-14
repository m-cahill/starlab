# Benchmark contract & scorecard — runtime contract v1 (M20)

**Contract family:** `starlab.benchmark_contract.v1` / `starlab.benchmark_scorecard.v1`  
**Profile:** `starlab.benchmark_contract.m20.v1` / `starlab.benchmark_scorecard.m20.v1`  
**Document `schema_version` values:** `starlab.benchmark_contract.v1` / `starlab.benchmark_scorecard.v1`

## Purpose and boundary

### Benchmark contract

A **benchmark contract** document defines one benchmark: allowed subject kinds, measurement surface, inputs, metric definitions, gating rules, aggregation policy, and a reference to the scorecard schema. It is a **governance and comparability** surface, not a proof of benchmark validity, replay correctness, or runtime truth.

### Scorecard

A **benchmark scorecard** document records one evaluation result against a benchmark: subject identity, how the result was produced (`evaluation_posture`), scoring and comparability status, metric rows aligned to the contract, aggregates, gating outcomes, warnings, and explicit non-claims. It does **not** assert benchmark integrity, fair comparison across heterogeneous runs, or replay↔execution equivalence unless separately proved.

## Relation to other milestones

| Milestone | Role |
| --------- | ---- |
| **M20** | JSON Schemas + reports for benchmark contract and scorecard; fixture validation; CLI emission. **No** baselines, **no** runner, **no** tournament harness. **M42** binds comparison metrics via **`--benchmark-contract`** (M20 benchmark JSON), not the M40 training-program charter — see `docs/runtime/learned_agent_comparison_harness_v1.md`. |
| **M21** | Scripted baseline suite (out of scope for M20). |
| **M22** | Heuristic baseline suite (out of scope for M20). |
| **M23** | Evaluation runner and tournament harness (out of scope for M20). |

## Required vs optional fields

Emission uses **JSON Schema Draft 2020-12** with `additionalProperties: false` on each object. All fields listed as **required** in the emitted schemas are mandatory on instances. Optional fields appear only where the schema allows `null` or omits a key per object rules.

## Controlled vocabularies

### Scoring status (`scoring_status`)

| Value | Meaning |
| ----- | ------- |
| `scored` | Metric values are populated under the contract’s scoring rules. |
| `unscored` | No scored metric values (e.g. contract-only or not yet evaluated). |
| `disqualified` | Subject or run excluded from scored comparison (policy or gating). |

### Comparability status (`comparability_status`)

| Value | Meaning |
| ----- | ------- |
| `comparable` | Results may be compared under stated assumptions (still not a proof of benchmark integrity). |
| `provisional` | Comparison is tentative or incomplete. |
| `non_comparable` | Results must not be treated as comparable across subjects or runs. |

### Measurement surface (`measurement_surface`)

Describes what the **benchmark definition** is defined over (contract document).

| Value | Meaning |
| ----- | ------- |
| `fixture_only` | Defined over static or fixture inputs only. |
| `replay_only` | Defined over replay-derived artifacts. |
| `runtime_execution` | Defined over live execution / harness (not required in CI for M20). |
| `hybrid` | Combines more than one surface. |

### Evaluation posture (`evaluation_posture`)

Describes how a **given scorecard** was produced (result document). **Distinct** from `measurement_surface`.

| Value | Meaning |
| ----- | ------- |
| `contract_only` | Schema/contract exercise only; no real benchmark run. |
| `fixture_only` | Produced from fixtures or canned inputs. |
| `replay_backed` | Produced using replay-derived artifacts. |
| `runtime_backed` | Produced using live or harness execution. |
| `hybrid` | Mixed provenance. |

### Subject kinds allowed (`subject_kinds_allowed` / `subject_ref.subject_kind`)

`scripted`, `heuristic`, `imitation`, `hierarchical`, `rl`, `human_replay` (see emitted schema enums).

## Metric definitions

Each metric definition includes at minimum: `metric_id`, `display_name`, `unit`, `optimization_direction`, `aggregation_method`, `scoring_role`. Semantics are defined for **consistent future scoring**, not for claiming a particular game or replay truth in M20.

## Aggregation and gating semantics

- **Aggregation policy** on the benchmark contract describes how aggregate scores are intended to be formed (policy kind and notes).
- **Gating rules** on the contract define rule ids, descriptions, and severity (`hard` / `soft`).
- **Gating outcomes** on the scorecard record per-rule pass/fail (and optional detail).

## Deterministic ordering rules

1. **Canonical JSON:** All emitted STARLAB JSON uses sorted keys, UTF-8, stable separators (see `starlab.runs.json_util.canonical_json_dumps`).
2. **Benchmark contract instance:** Top-level keys follow the canonical JSON sort when serialized; logical field order for authors is documented in schema reports as `deterministic_key_order_benchmark_instance`.
3. **Metric definitions:** Order is the **array order** in `metric_definitions`; it is the stable order for scoring and scorecard rows.
4. **Scorecard `metric_rows`:** Must list one row per benchmark metric in the **same order** as `metric_definitions` in the paired contract (validated in tests when both are loaded).
5. **`warnings` and `non_claims`:** Must be sorted **lexicographically** (validated beyond JSON Schema).
6. **Schema reports:** Example fixture hashes are keyed in sorted order; vocabulary lists are sorted where emitted as arrays.

## Explicit non-claims

M20 does **not** prove:

- Benchmark integrity or anti-cheat guarantees.
- Replay↔execution equivalence.
- Baseline or agent performance claims.
- Validity of leaderboard or tournament results.

Schema reports carry default `non_claims` strings; documents may carry additional non-claim strings.

## CLI

```text
python -m starlab.benchmarks.emit_benchmark_contracts --output-dir OUT
```

Writes:

- `benchmark_contract_schema.json`
- `benchmark_contract_schema_report.json`
- `benchmark_scorecard_schema.json`
- `benchmark_scorecard_schema_report.json`

When `tests/fixtures/m20/` fixtures are present, reports include SHA-256 hashes of example valid/invalid fixtures.

## Failure semantics

The CLI exits non-zero on internal emission errors, invalid emitted schema structure, or I/O failures. Validation of user documents is performed by tests and by consumers using `jsonschema`; invalid fixtures are expected to fail validation.
