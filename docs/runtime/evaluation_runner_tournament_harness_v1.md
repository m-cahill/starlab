# Evaluation runner & tournament harness — runtime contract v1 (M23)

**Tournament document `tournament_version`:** `starlab.evaluation_tournament.v1`  
**Report document `report_version`:** `starlab.evaluation_tournament_report.v1`

## Purpose and boundary

The **evaluation tournament** is a deterministic, offline artifact that consumes:

1. one validated **M20 benchmark contract** (`measurement_surface` **`fixture_only`**), and  
2. one or more governed **M21 scripted** and/or **M22 heuristic** baseline **suite** JSON artifacts whose embedded scorecards match that contract.

It proves that STARLAB can **flatten** fixture-only scorecards into a **entrant catalog**, run a **minimal round-robin harness**:

* every entrant plays every other entrant once  
* pairings follow **entrant order** (suite order, then subject/scorecard order within each suite)  
* match IDs are deterministic  
* no randomness and no hidden state  

and emit canonical **`evaluation_tournament.json`** + **`evaluation_tournament_report.json`** without claiming benchmark integrity, leaderboard validity, replay↔execution equivalence, live SC2 execution, replay parsing, attribution/diagnostics (M24), or evidence-pack packaging (M25).

## Non-claims (explicit)

- **Not** benchmark integrity or leaderboard validity.  
- **Not** replay↔execution equivalence or any replay-derived scoring.  
- **Not** live SC2 execution, `starlab.replays`, `starlab.sc2`, or `s2protocol` in M23 evaluation modules.  
- **Not** attribution, failure-view diagnostics, or evidence packs (later milestones).  
- **Not** a multi-metric benchmark semantics layer: **pairwise match results** are decided only by the contract’s **`scoring_role: primary`** metric; other metrics are recorded for transparency and tie-break metadata only.

## Inputs

### Benchmark contract

Must pass `validate_benchmark_contract` (M20) and have `measurement_surface == fixture_only`.

### Suite artifacts (M21 / M22)

M23 does **not** introduce new JSON Schemas for suites. Validation is **structural and semantic**, aligned with:

* `docs/runtime/scripted_baseline_suite_v1.md`  
* `docs/runtime/heuristic_baseline_suite_v1.md`  

Checks include:

* `suite_version` is either `starlab.scripted_baseline_suite.v1` or `starlab.heuristic_baseline_suite.v1`  
* `measurement_surface` and `evaluation_posture` are **`fixture_only`**  
* `benchmark_contract_sha256` and `benchmark_id` match the loaded contract  
* embedded `scorecards` validate with `validate_benchmark_scorecard` (M20) and align with `subjects` order and kind  
* `subject_kind` is **`scripted`** for scripted suites and **`heuristic`** for heuristic suites  

All loaded suites must share the same `benchmark_contract_sha256` as the loaded contract.

## Deterministic ordering

* **Suite order** follows CLI `--suite` order.  
* **Entrants** are flattened in that suite order; within a suite, order follows embedded `scorecards` / `subjects`.  
* **Entrant IDs** are `"{suite_id}::{subject_id}"` (unique within the tournament).  
* **Matches** are generated in round-robin order over the entrant list: for indices `i < j`, entrant `i` is **A** and entrant `j` is **B**.  
* **Standings** sort by: (1) tournament points descending, (2) primary-metric tie-break scalar descending (see below), (3) `entrant_id` ascending.  
* **`warnings`** and **`non_claims`** are sorted lexicographically.

## Pairwise comparison policy

* **Decisive:** the first `metric_definitions` entry with `scoring_role == "primary"` (contract order).  
* **Directions:** `maximize` / `minimize` / `none` apply per `optimization_direction`; `none` yields a draw on that metric for comparison purposes.  
* **Draw:** equal primary metric values after applying the direction semantics.  
* **Points:** win **1.0**, draw **0.5** each, loss **0.0**.  
* **Full surface:** each match includes `metric_comparisons` for every contract metric (primary + non-primary) with `better_entrant_id` (or `null` on tie).

## Tie-break (standings)

After points, when two entrants tie on points:

1. **Primary metric tie-break scalar:** for `maximize`, higher raw primary value is better; for `minimize`, lower raw value is better (implemented as `tiebreak_scalar = -value` so higher scalar is better).  
2. If still tied, **`entrant_id` ascending lexicographically.**

## Artifacts

Emitted as canonical JSON (`canonical_json_dumps`: sorted keys, UTF-8, trailing newline).

### `evaluation_tournament.json`

Required top-level fields include:

- `tournament_version`, `tournament_id`, `benchmark_id`, `benchmark_contract_sha256`  
- `measurement_surface` — **`fixture_only`**  
- `evaluation_posture` — **`fixture_only`**  
- `suite_inputs` — ordered list of `{suite_id, suite_path, suite_sha256, suite_version}`  
- `entrants` — ordered catalog (see `source_scorecard_ref` for provenance)  
- `matches` — ordered round-robin results  
- `standings` — ordered table  
- `warnings`, `non_claims` — sorted lexicographically  

### `evaluation_tournament_report.json`

Includes `report_version`, `tournament_verdict` (`pass` on success), `suite_count`, `entrant_count`, `match_count`, `benchmark_contract_sha256`, `failures` (empty on success), `warnings`, `non_claims` (sorted).

## CLI

```text
python -m starlab.evaluation.emit_evaluation_tournament \
  --benchmark-contract PATH \
  --suite PATH \
  --suite PATH \
  --output-dir OUT
```

Invalid inputs fail with non-zero exit.
