# Heuristic baseline suite — runtime contract v1 (M22)

**Suite document `suite_version`:** `starlab.heuristic_baseline_suite.v1`  
**Report document `report_version`:** `starlab.heuristic_baseline_suite_report.v1`

## Purpose and boundary

The **heuristic baseline suite** is a deterministic, offline artifact that binds a single validated **M20 benchmark contract** to a fixed small set of **heuristic** baseline subjects and **fixture-only** scorecards. It proves that STARLAB can consume the M20 contract surface end-to-end (load → validate → emit governed JSON) without claiming benchmark integrity, replay correctness, replay↔execution equivalence, scripted baseline emission (that is **M21**), an evaluation runner, or a tournament harness.

## Relation to other milestones

| Milestone | Role |
| --------- | ---- |
| **M20** | Benchmark contract + scorecard JSON Schemas and validation helpers. |
| **M21** | Scripted baseline suite + embedded scorecards — **not** heuristics. |
| **M22** | Heuristic baseline suite + embedded scorecards (this contract). |
| **M23** | Evaluation runner / tournament harness (out of scope for M22). |

## Required benchmark contract posture (M22)

The input benchmark contract instance MUST:

1. Pass `validate_benchmark_contract` (M20 JSON Schema + `non_claims` lexicographic order).
2. Have `measurement_surface` equal to **`fixture_only`**.

Any other `measurement_surface` value MUST cause the M22 emitter to fail (non-zero exit).

## Suite artifact (`heuristic_baseline_suite.json`)

Emitted as canonical JSON (sorted object keys; UTF-8; trailing newline per `canonical_json_dumps`).

### Top-level fields

| Field | Semantics |
| ----- | --------- |
| `suite_version` | Constant `starlab.heuristic_baseline_suite.v1`. |
| `suite_id` | Stable identifier for this suite shape (M22 demo suite). |
| `benchmark_id` | Copied from the input contract. |
| `benchmark_contract_sha256` | SHA-256 (hex) of the input contract under canonical JSON (no trailing newline in hash input). |
| `measurement_surface` | Copied from the input contract; MUST be `fixture_only` for M22. |
| `evaluation_posture` | Suite-level summary: **`fixture_only`** for M22 (aligned with embedded scorecards). |
| `subjects` | Ordered catalog of heuristic subjects (see below). |
| `fixture_cases` | Ordered catalog of fixture evaluation cases (see below). |
| `scorecards` | One M20-conformant scorecard per subject, ordered to match `subjects`. |
| `warnings` | Sorted lexicographically. |
| `non_claims` | Sorted lexicographically; explicit suite-level non-claims. |

### Subject catalog semantics

Each subject entry MUST include at least:

- `subject_id` — stable string identifier (M22 uses a fixed deterministic pair).
- `subject_kind` — **`heuristic`** for M22.

`subjects` array order is the **fixed M22 suite subject order** (not alphabetical).

### Fixture case semantics

Each fixture case entry MUST include at least:

- `case_id` — stable identifier.

`fixture_cases` array order is the **fixed M22 fixture case order**. M22 uses exactly **one** fixture case as a minimal deterministic catalog.

### Scorecard semantics (embedded)

Each embedded scorecard MUST:

- Validate with `validate_benchmark_scorecard` (M20 schema + `warnings` / `non_claims` order).
- Use `benchmark_contract_sha256` equal to the suite’s `benchmark_contract_sha256`.
- Use `evaluation_posture` **`fixture_only`**, `scoring_status` **`scored`**, `comparability_status` **`provisional`**.
- Use `subject_ref.subject_kind` **`heuristic`** and `subject_ref.subject_id` matching the corresponding subject.
- List `metric_rows` in the same order as `metric_definitions` on the input contract.
- List `warnings` and `non_claims` sorted lexicographically.

M22 does **not** assert that numeric values reflect real StarCraft II play; they are **deterministic fixture values**.

## Suite report (`heuristic_baseline_suite_report.json`)

| Field | Semantics |
| ----- | --------- |
| `report_version` | Constant `starlab.heuristic_baseline_suite_report.v1`. |
| `suite_verdict` | `pass` if emission completed and all validations succeeded; otherwise emission fails before write. |
| `subject_count` | Number of subjects (2 in M22). |
| `fixture_case_count` | Number of fixture cases (1 in M22). |
| `scorecard_count` | Number of embedded scorecards (2 in M22). |
| `benchmark_contract_sha256` | Same as the suite artifact. |
| `failures` | Empty on success; reserved for structured failure messages if extended later. |
| `warnings` | Sorted lexicographically. |
| `non_claims` | Sorted lexicographically. |

## Deterministic ordering rules

- **`subjects`:** fixed M22 subject order.
- **`fixture_cases`:** fixed M22 fixture case order.
- **`scorecards`:** same order as `subjects`.
- **`metric_rows`:** same order as the input contract’s `metric_definitions`.
- **`warnings` and `non_claims`:** sorted lexicographically (suite, report, and each scorecard).
- **JSON serialization:** canonical (`sort_keys=True`) for all emitted artifacts.

## Explicit non-claims

The suite and report carry **suite-level** non-claim identifiers (stable URIs). They do **not** exhaust all limits of the system; they bound M22’s honest posture. Embedded scorecards also carry scorecard-level non-claims per M20 practice.

## Failure conditions (CLI)

The M22 CLI MUST exit non-zero when:

- the benchmark contract file is not valid JSON;
- the contract fails `validate_benchmark_contract`;
- `measurement_surface` is not `fixture_only`;
- any generated scorecard fails `validate_benchmark_scorecard`;
- an internal emission error occurs.
