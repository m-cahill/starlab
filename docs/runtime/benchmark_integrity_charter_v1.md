# Benchmark integrity charter v1 (M55)

**Contract id:** `starlab.benchmark_integrity_charter.v1`  
**Milestone:** **M55** — *charter, vocabulary, and split-governance controls only* — **not** benchmark-integrity proof — see `docs/starlab.md` (Phase VII, remaining proof-track map).  
**See also:** public ledger `docs/starlab.md`. **M56 (stub/planned):** reproducibility evidence and benchmark-integrity **gates** — **not** introduced in M55.

## Purpose

Define a **bounded** meaning of **benchmark integrity** for STARLAB: which governance surfaces must not be conflated (benchmark definition vs corpus promotion vs subject identity vs execution posture vs aggregation/publication vs acceptance authority), and what evidence classes remain **obligations for M56+** without claiming they are satisfied today.

This document precedes **M56** (evidence + reproducibility gates). **M55** does **not** subsume **M52–M54** (replay↔execution equivalence — **closed** on `main`).

## What M55 proves

- A **deterministic charter artifact** (`benchmark_integrity_charter.json`) and companion **report** (`benchmark_integrity_charter_report.json`) with explicit **non_claims** and six **split_governance_controls** (one machine-readable entry per family).
- Agreement between this markdown contract and the JSON **contract_id** / **schema_version** / field names **where listed**.

## What M55 does not prove

- **No** verdict that STARLAB benchmarks are reproducible, comparable, or “passing” in a governance sense.
- **No** rerun or recomputation of benchmark results; **no** corpus promotion or relabeling.
- **No** live SC2 in CI, ladder protocol, or public leaderboard claims.
- **No** merge-bar or branch-protection automation keyed off benchmark integrity.
- **No** replacement for **M52–M54** equivalence evidence, audits, or gate packs (different Phase VII track).

## Split governance (summary)

| Family | Owns (intent) |
| ------ | ------------- |
| Benchmark definition | Contract id/version, score semantics, allowed subject classes; runners must not silently redefine scores. |
| Corpus promotion | Replay/map/label provenance, intake status, canonical vs local-only/quarantined posture. |
| Subject identity freeze | Baseline/candidate identity, bundle/run hashes, artifact version freeze; no silent substitution. |
| Execution posture | Fixture vs local vs live boundaries; no fixture passed off as live proof. |
| Score aggregation / publication | Aggregation semantics ownership; diagnostics cannot out-claim the contract. |
| Acceptance authority | Who may describe integrity status vs enforced gates; **M55** introduces **no** acceptance verdict. |

## Future obligations (M56)

- Deterministic **evidence** rows for: benchmark contract identity, corpus provenance, subject freeze, execution posture receipts, score aggregation reproducibility (see JSON `evidence_classes_reserved_for_m56`).
- Optional **gate packs** that evaluate evidence — **chartered in M56**, not in M55.

## CLI

```text
python -m starlab.benchmark_integrity.emit_benchmark_integrity_charter --output-dir <dir>
```

Emits `benchmark_integrity_charter.json` and `benchmark_integrity_charter_report.json` deterministically (sorted keys, stable UTF-8).
