# Evaluation diagnostics & failure views — runtime contract v1 (M24)

**Diagnostics document `diagnostics_version`:** `starlab.evaluation_diagnostics.v1`  
**Report document `report_version`:** `starlab.evaluation_diagnostics_report.v1`

## Purpose and boundary

**M24** is a deterministic, **offline**, **fixture-only** **interpretive** layer over one governed **M23** `evaluation_tournament.json`. It explains how standings and pairwise results relate to the recorded tournament artifact — **without** changing M23 scoring, pairing, or standings semantics.

**M24 is not** a new benchmark semantics layer.

## Required input posture

The input **`evaluation_tournament.json`** must:

- use `tournament_version` **`starlab.evaluation_tournament.v1`** (M23),
- have `measurement_surface == "fixture_only"` and `evaluation_posture == "fixture_only"`,
- pass M24 structural + semantic validation (no new JSON Schema for the tournament in M24),
- preserve benchmark identity via `benchmark_contract_sha256` and suite provenance as emitted by M23.

## Outputs

Emitted as canonical JSON (`canonical_json_dumps`: sorted keys, UTF-8, trailing newline).

1. **`evaluation_diagnostics.json`** — entrant diagnostics, match diagnostics, standing explanations, failure views, sorted `warnings` / `non_claims`.
2. **`evaluation_diagnostics_report.json`** — compact verdict + counts + sorted `warnings` / `non_claims`.

## Non-claims (explicit)

- **Not** benchmark integrity or general leaderboard validity.  
- **Not** replay-derived evidence, live SC2 execution, or replay parsing.  
- **Not** replay↔execution equivalence.  
- **Not** root-cause attribution **outside** the recorded tournament artifact.  
- **Not** evidence-pack bundling (**M25**).  
- **Not** a normative re-ranking: diagnostics **explain** M23 outcomes; they do **not** “fix” or override them.

## Deterministic rules

- Entrant diagnostics follow **M23 entrant order**.  
- Match diagnostics follow **M23 match order**.  
- Standing explanations follow **M23 standings order**.  
- `warnings` and `non_claims` are sorted **lexicographically**.  
- No randomness, no hidden state, no new timestamps beyond existing canonical conventions.

## CLI

```text
python -m starlab.evaluation.emit_evaluation_diagnostics \
  --tournament PATH \
  --output-dir OUT
```

Invalid inputs fail with non-zero exit.
