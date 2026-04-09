# Baseline evidence pack v1 (M25)

**Version:** `starlab.baseline_evidence_pack.v1`  
**Report version:** `starlab.baseline_evidence_pack_report.v1`

## Purpose

**M25** is a **deterministic, offline, fixture-only interpretive packaging layer** over already-governed Phase IV artifacts. It does **not** introduce new benchmark semantics, new scoring, new tournament rules, new diagnostics logic, benchmark-integrity claims, replay↔execution claims, live SC2, raw replay packaging, or archive/zip transport.

**M25** consumes:

- One or more governed **M21** `scripted_baseline_suite.json` and/or **M22** `heuristic_baseline_suite.json` artifacts.
- One governed **M23** `evaluation_tournament.json` (`starlab.evaluation_tournament.v1`, `fixture_only`).
- One governed **M24** `evaluation_diagnostics.json` (`starlab.evaluation_diagnostics.v1`) that is the diagnostic view of **that** tournament.

**M25** emits:

- `baseline_evidence_pack.json`
- `baseline_evidence_pack_report.json`

**v1** emits **JSON only** — no zip/tar, no copied raw fixtures, no file-bundle transport.

## Required input posture

### Suite artifacts

Each supplied suite file must:

- Parse as a JSON object.
- Match the **M23** tournament’s `source_scorecard_ref` for every entrant that references that suite (by **SHA-256 of canonical JSON** equality with `suite_sha256` in the tournament).
- Share **`benchmark_contract_sha256`** and **`benchmark_id`** with the supplied tournament and diagnostics.
- If **`measurement_surface`** is present, it MUST be `"fixture_only"`.
- If **`measurement_surface`** is absent, **M25** still requires consistency with the **M23** tournament’s `measurement_surface == "fixture_only"` and `evaluation_posture == "fixture_only"` (no new suite semantics; fail if the suite JSON contradicts fixture-only posture where checkable, e.g. explicit non-`fixture_only` fields).

### Tournament

- `tournament_version` MUST be `starlab.evaluation_tournament.v1`.
- `measurement_surface` and `evaluation_posture` MUST be `fixture_only`.
- Every `entrant_id` MUST resolve to exactly one row in the supplied suite artifacts (via `source_scorecard_ref.suite_sha256` matching a supplied suite file’s canonical hash).
- **Duplicate subject coverage:** the pair `(suite_id, subject_id)` across entrants MUST be unique (no two entrants sharing the same suite subject identity).

### Diagnostics

- `diagnostics_version` MUST be `starlab.evaluation_diagnostics.v1`.
- **`benchmark_contract_sha256`**, **`benchmark_id`**, and **`tournament_id`** MUST match the supplied tournament.
- `measurement_surface` and `evaluation_posture` MUST be `fixture_only`.
- The set of **`entrant_id`** values in `entrant_diagnostics` MUST equal the tournament’s entrant set (order may differ; **M25** aligns by tournament standings order for the pack’s `entrants[]`).

**M25** does **not** require a top-level `tournament_sha256` inside **M24** diagnostics. Identity binding uses the strongest fields the governed chain already shares, plus structural entrant alignment.

**Optional (M25-local):** **M25** MAY compute `tournament_sha256` as SHA-256 of the **canonical JSON** representation of the loaded tournament object (same canonicalization as `starlab.runs.json_util.sha256_hex_of_canonical_json`) and record it in outputs — this is **packaging identity**, not a retroactive change to **M24**.

## Output posture

### `baseline_evidence_pack.json` (minimal)

| Field | Meaning |
| ----- | ------- |
| `evidence_pack_version` | `starlab.baseline_evidence_pack.v1` |
| `tournament_sha256` | Canonical JSON hash of the supplied tournament object (M25-local identity). |
| `diagnostics_sha256` | Canonical JSON hash of the supplied diagnostics object. |
| `suite_sha256s` | Sorted list of distinct suite canonical hashes (hex strings) used by the chain. |
| `benchmark_contract_sha256` | From upstream (must be consistent across all inputs). |
| `entrants` | One row per entrant, in **M23 standings order** (see below). |
| `warnings` | Sorted lexicographically. |
| `non_claims` | Sorted lexicographically. |

### `entrants[]` row (minimal)

| Field | Meaning |
| ----- | ------- |
| `entrant_id` | From **M23**. |
| `suite_id` | From **M23** entrant. |
| `subject_id` | From **M23** entrant. |
| `subject_kind` | From **M23** entrant. |
| `standing_rank` | From **M23** standings (`rank`). |
| `tournament_points` | From **M23** standings (`points`). |
| `primary_metric` | Primary metric value for the entrant (from **M23** standings / **M24** entrant diagnostics — same fixture-only value). |
| `primary_tiebreak_scalar` | From **M23** standings (`primary_metric_tiebreak_scalar`). |
| `wins`, `losses`, `draws` | From **M23** standings. |
| `failure_views` | **Entrant-scoped projection** of **M24** `failure_views` (see below). |
| `evidence_refs` | **Identity-first** cross-references (see below). |

**Standings order:** iterate **M23** `standings[]` in array order (which is **M23**’s sorted tournament order: points descending, then tie-break, then `entrant_id`).

### `failure_views` (per entrant)

A **reduced** list — **not** the full **M24** diagnostics object and **not** counts-only. Each item is a stable object:

| Field | Required | Meaning |
| ----- | -------- | ------- |
| `failure_view_id` | yes | Stable id (see enum below). |
| `is_present` | yes | Whether this interpretive surface applies to this entrant. |
| `summary` | yes | Short human-readable explanation (deterministic string from **M25**). |
| `supporting_match_ids` | no | Match ids when the surface is match-scoped (e.g. draw-on-primary). |
| `supporting_standing_context` | no | Small structured hint (e.g. which **M24** bucket). |

**Stable `failure_view_id` values** (align with **M24** `failure_views` buckets):

- `starlab.m25.failure_view.zero_win_entrant`
- `starlab.m25.failure_view.lowest_points_entrant`
- `starlab.m25.failure_view.draw_equal_primary_metric`
- `starlab.m25.failure_view.standings_used_tiebreak_scalar`
- `starlab.m25.failure_view.standings_used_lexicographic_tiebreak`

Sort each entrant’s `failure_views` list by `(failure_view_id, summary, repr(supporting_match_ids))` for determinism.

### `evidence_refs` (per entrant)

**More than hashes-only; less than full row duplication.**

```json
{
  "suite_ref": {
    "suite_id": "<from M23 entrant>",
    "suite_version": "<from source_scorecard_ref.suite_version>",
    "subject_id": "<from M23 entrant>",
    "subject_kind": "<from M23 entrant>"
  },
  "tournament_ref": {
    "tournament_version": "<from M23 tournament_version>",
    "entrant_id": "<from M23>",
    "standing_rank": <int rank from standings>
  },
  "diagnostics_ref": {
    "diagnostics_version": "starlab.evaluation_diagnostics.v1",
    "entrant_id": "<from M23>"
  }
}
```

### `baseline_evidence_pack_report.json` (minimal)

| Field | Meaning |
| ----- | ------- |
| `report_version` | `starlab.baseline_evidence_pack_report.v1` |
| `evidence_pack_sha256` | Canonical JSON hash of the **pack** object (computed **without** embedding this field in the pack). |
| `entrant_count` | Number of entrants. |
| `suite_count` | Number of distinct suite hashes in `suite_sha256s`. |
| `subject_kind_counts` | Map of `subject_kind` → count. |
| `failure_view_counts` | Map of `failure_view_id` → number of entrant rows for which that view is present (`is_present == true`). |
| `warnings` | Sorted lexicographically. |
| `non_claims` | Sorted lexicographically. |

## Deterministic rules

- **JSON:** `starlab.runs.json_util.canonical_json_dumps` for on-disk emission.
- **`warnings` / `non_claims`:** sorted lexicographically.
- **`suite_sha256s`:** sorted lexicographically.
- **`entrants[]`:** **M23** `standings[]` order.
- No timestamps beyond existing project conventions unless strictly necessary.

## Explicit non-claims

- Not benchmark integrity.
- Not leaderboard validity beyond governed upstream artifacts.
- Not new scoring or re-ranking.
- Not new diagnostics logic.
- Not live SC2 or replay execution.
- Not replay↔execution equivalence.
- Not raw replay or archive packaging.
- Not **M26** imitation or learning work.

## CLI

```text
python -m starlab.evaluation.emit_baseline_evidence_pack \
  --suite PATH \
  --suite PATH \
  --tournament PATH \
  --diagnostics PATH \
  --output-dir OUT
```

Repeat `--suite` for each suite file (e.g. one M21 + one M22).
