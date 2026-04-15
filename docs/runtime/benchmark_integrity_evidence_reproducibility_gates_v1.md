# Benchmark integrity evidence & reproducibility gates v1 (M56)

**Status:** Governed runtime contract (Phase VII — Trust, Equivalence, Benchmark Integrity, and Release Lock)

## Contract identifiers

| Artifact | Contract id |
| -------- | ------------- |
| Evidence JSON | `starlab.benchmark_integrity_evidence.v1` |
| Evidence report JSON | `starlab.benchmark_integrity_evidence_report.v1` |
| Reproducibility gates JSON | `starlab.benchmark_integrity_reproducibility_gates.v1` |
| Reproducibility gates report JSON | `starlab.benchmark_integrity_reproducibility_gates_report.v1` |

## Bounded scope (M56 v1)

Exactly one scope is implemented:

* **scope_id:** `starlab.m56.scope.fixture_only_baseline_chain_v1`

This scope covers the **fixture-only offline** evaluation chain:

* **M21** `scripted_baseline_suite.json`
* **M22** `heuristic_baseline_suite.json`
* **M23** `evaluation_tournament.json`
* **M24** `evaluation_diagnostics.json`
* **M25** `baseline_evidence_pack.json`

There is **no** directory discovery: all inputs are explicit paths (CLI flags).

## Gate pack

Exactly one gate pack is implemented:

* **gatepack_id:** `starlab.m56.gatepack.fixture_only_baseline_chain_reproducibility_v1`

## Required inputs

| Input | Role |
| ----- | ---- |
| `--scripted-baseline-suite` | M21 artifact path |
| `--heuristic-baseline-suite` | M22 artifact path |
| `--evaluation-tournament` | M23 artifact path |
| `--evaluation-diagnostics` | M24 artifact path |
| `--baseline-evidence-pack` | M25 artifact path |

## Evidence row semantics

Evidence rows use the **M55-reserved** `evidence_class` identifiers:

* `benchmark_contract_identity`
* `corpus_provenance_and_promotion`
* `subject_identity_and_freeze`
* `execution_posture_receipts`
* `score_aggregation_reproducibility`

Row **status** vocabulary:

* `present` — required obligation satisfied for this class within scope
* `missing` — required check failed or inconsistent chain
* `not_applicable` — class does not apply (e.g. corpus promotion in fixture-only happy path)
* `unavailable_by_design` — reserved for future scopes
* `out_of_scope` — reserved for future scopes

Each row includes `source_artifacts`, `canonical_sha256s` (canonical JSON hashes), `observations`, and `residual_non_claims`.

### Corpus promotion posture (fixture-only scope)

For `starlab.m56.scope.fixture_only_baseline_chain_v1`, `corpus_provenance_and_promotion` is normally **`not_applicable`**.

If supplied artifacts contain markers implying **canonical replay-corpus promotion** (e.g. `canonical_replay_corpus` in canonical JSON), the evidence records that implication and the gate pack **fails** this scope.

## CLI

Emit evidence + report:

```bash
python -m starlab.benchmark_integrity.emit_benchmark_integrity_evidence \
  --output-dir <dir> \
  --scripted-baseline-suite <path> \
  --heuristic-baseline-suite <path> \
  --evaluation-tournament <path> \
  --evaluation-diagnostics <path> \
  --baseline-evidence-pack <path>
```

Emit reproducibility gates + report (consumes evidence JSON):

```bash
python -m starlab.benchmark_integrity.emit_benchmark_integrity_gates \
  --evidence <path/to/benchmark_integrity_evidence.json> \
  --output-dir <dir> \
  [--evidence-report <path/to/benchmark_integrity_evidence_report.json>]
```

Optional `--evidence-report` enables a deterministic SHA-256 cross-check against the evidence object.

## Gate result vocabulary

* `pass` / `fail` / `not_evaluable` / `not_applicable`

## Top-level scope status

* `accepted_within_scope` — all applicable predicates pass for this gate pack
* `rejected_within_scope` — at least one predicate fails
* `not_evaluable` — evidence document is not a recognizable M56 evidence object

There is **no** global “benchmark integrity passed” verdict.

## Residual non-claims

* **Benchmark integrity is not globally proved** by M56 evidence or gates.
* M56 does **not** replace **M52–M54** replay↔execution equivalence outcomes.
* M56 does **not** cover learned-subject chains (M27/M28/M41/M42), replay-corpus canonical promotion proofs, live/local evaluation, ladder/public protocols, or merge-bar automation.

## Boundary: M57+

Later milestones (e.g. **M57–M61**) may add additional scopes, corpus governance, live SC2-in-CI posture, ladder/public evaluation, or release lock — **not** implied by M56.
