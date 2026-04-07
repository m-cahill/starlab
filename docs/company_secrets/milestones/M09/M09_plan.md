# M09 Plan — Replay Metadata Extraction

## Objective

Define and implement a **stable, deterministic, public replay metadata contract** derived from **M08 raw parse artifacts**, without pulling forward event/timeline semantics, build-order extraction, or benchmark claims.

M09 should take the parser-owned raw sections proven in M08 and lower them into a **small, auditable, governed metadata surface** that downstream milestones can rely on.

## Resolved constraints

These decisions are fixed unless implementation reveals a hard repo-local conflict:

* M09 consumes **M08 artifacts**, not raw replay bytes directly, by default.
* M09 must **not** invoke `s2protocol` or reintroduce parser-specific imports outside the M08 adapter boundary.
* CI remains **fixture-driven** and does **not** require the optional `replay-parser` extra.
* M09 owns **stable normalized replay metadata** only.
* M10 still owns **event/timeline semantics**.
* M11 still owns **build-order / economy extraction**.
* Keep the milestone **small** and **schema-first**.
* Prefer `null` / `unknown` over field omission once a metadata field is part of the public contract.

## What M09 should prove

M09 should prove, narrowly, that STARLAB can:

* consume governed **M08** replay parse artifacts,
* deterministically extract a **stable normalized metadata contract**,
* emit governed metadata JSON suitable for downstream milestones,
* distinguish full extraction from partial extraction and source-contract failure,
* preserve clear separation between:

  * raw parser-owned sections,
  * normalized metadata,
  * deferred event semantics.

## What M09 must not claim

M09 must **not** claim:

* event/timeline semantics,
* tracker/game/message event interpretation,
* build-order extraction,
* replay↔execution semantic equivalence,
* benchmark integrity,
* broad parser correctness,
* live SC2 execution in CI,
* legal certification of replay rights.

Those remain outside the milestone boundary and should be repeated in summary, audit, and ledger closeout.

## Primary deliverables

### 1. Contract document

Create:

* `docs/runtime/replay_metadata_extraction.md`

This doc should define:

* the M09 metadata contract,
* allowed source artifacts,
* normalized field definitions,
* enum/value rules,
* ordering / nullability rules,
* extraction status model,
* check model,
* explicit non-claims,
* relation to M08 raw parse substrate and M10 event semantics.

### 2. Code surface

Recommended modules under `starlab/replays/`:

* `metadata_models.py`
* `metadata_extraction.py`
* `metadata_io.py`
* `extract_replay_metadata.py`

Responsibilities:

* `metadata_models.py`: schema constants, enums, dataclasses, check IDs
* `metadata_extraction.py`: pure extraction from M08 raw parse envelope to normalized metadata
* `metadata_io.py`: source loading, linkage verification, report assembly, artifact emission
* `extract_replay_metadata.py`: CLI only

If the repo already has a slightly better local naming pattern, preserve consistency over exact filenames.

### 3. Governed artifacts

Emit exactly **two** artifacts.

#### `replay_metadata.json`

Recommended schema version:

* `starlab.replay_metadata.v1`

Purpose:

* the stable normalized replay metadata contract.

Recommended top-level fields:

* `schema_version`
* `metadata_contract_version`
* `replay_content_sha256`
* `source_raw_parse_sha256`
* `parser_family`
* `parser_version`
* `metadata_profile`
* `source_sections_present`
* `metadata`

#### `replay_metadata_report.json`

Recommended schema version:

* `starlab.replay_metadata_report.v1`

Purpose:

* deterministic extraction status and ordered checks.

Recommended fields:

* `schema_version`
* `metadata_contract_version`
* `replay_content_sha256`
* `source_raw_parse_sha256`
* `extraction_status`
* `check_results`
* `reason_codes`
* `advisory_notes`

## Metadata contract shape

Keep the normalized metadata surface **small and defensible**.

Recommended `metadata_contract_version`:

* `starlab.replay_metadata_contract.v1`

Recommended `metadata_profile`:

* `starlab.replay_metadata_profile.v1`

Recommended normalized shape inside `metadata`:

```json
{
  "protocol": {
    "base_build": 0,
    "data_build": 0,
    "data_version": null
  },
  "map": {
    "map_name": null
  },
  "game": {
    "game_length_loops": null,
    "player_count": 0,
    "event_streams_available": {
      "game_events_available": false,
      "message_events_available": false,
      "tracker_events_available": false,
      "attribute_events_available": false
    }
  },
  "players": [
    {
      "player_index": 0,
      "player_kind": "unknown",
      "race_requested": "unknown",
      "race_actual": "unknown",
      "result": "unknown"
    }
  ]
}
```

This is a recommended contract shape, not a verbatim schema requirement, but the milestone should stay close to it.

## Field rules

### Protocol fields

Normalize only stable replay-level fields already available from M08 raw blocks:

* `base_build`
* `data_build`
* `data_version`

Use `null` when absent and do **not** infer values heuristically.

### Map fields

For M09, keep this minimal:

* `map_name`

No richer map semantics, map classification, or external map resolution.

### Game fields

Normalize only:

* `game_length_loops`
* `player_count`
* `event_streams_available`

Do **not** derive timeline semantics or replay-phase summaries.

### Player fields

Normalize only:

* `player_index`
* `player_kind`
* `race_requested`
* `race_actual`
* `result`

Keep players in deterministic order by `player_index`.

Do **not** introduce display-oriented or personally identifying fields into the public metadata contract in M09 unless implementation reveals an already-governed necessity. Raw parser blocks remain the place for richer raw details.

## Enum/value rules

Recommended enums:

### `player_kind`

* `human`
* `computer`
* `observer`
* `unknown`

### `race_requested`

* `terran`
* `zerg`
* `protoss`
* `random`
* `unknown`

### `race_actual`

* `terran`
* `zerg`
* `protoss`
* `unknown`

### `result`

* `win`
* `loss`
* `tie`
* `unknown`

Map source values conservatively. If source data is missing or ambiguous, use `unknown`, not guesswork.

## Source artifact inputs

M09 should prefer M08 outputs as inputs.

Recommended CLI:

```bash
python -m starlab.replays.extract_replay_metadata \
  --raw-parse path/to/replay_raw_parse.json \
  --output-dir path/to/out \
  [--parse-receipt path/to/replay_parse_receipt.json] \
  [--parse-report path/to/replay_parse_report.json]
```

### Linkage rules

* `--raw-parse` is required.
* If `--parse-receipt` is supplied:

  * `replay_content_sha256` must match,
  * `source_raw_parse_sha256` must match the receipt’s `raw_parse_sha256`.
* If `--parse-report` is supplied:

  * `replay_content_sha256` must match,
  * `parse_status` should be `parsed`; otherwise treat as source-contract failure or advisory failure per the defined contract.
* M09 should remain usable with `--raw-parse` alone for controlled local work, but governed linkage should be preferred.

## Extraction rules

This is the real technical center of M09.

The extraction layer should be **pure** and **deterministic**.

Rules:

* consume only normalized M08 raw parse JSON,
* do not inspect replay bytes directly,
* do not invoke the parser adapter,
* do not infer semantics from event streams,
* use explicit field mapping from raw sections,
* preserve deterministic ordering,
* use `null` / `unknown` rather than omission once the contract is defined,
* reject unsupported source shapes explicitly.

## Status model

Recommended `extraction_status` values:

* `extracted`
* `partial`
* `source_contract_failed`
* `extraction_failed`

Interpretation:

* `extracted`: normalized metadata artifact emitted with required core fields extracted successfully
* `partial`: artifact emitted, but some normalized fields remain `null` / `unknown` because source sections were absent or ambiguous
* `source_contract_failed`: raw parse / receipt / report linkage invalid or inconsistent
* `extraction_failed`: unexpected extraction failure or unsupported source shape

## Check model

Use ordered checks similar to M07/M08.

Recommended checks:

* `raw_parse_schema_valid`
* `replay_hash_present`
* `source_raw_parse_sha256_computed`
* `parse_receipt_hash_match`
* `parse_report_status_parsed`
* `required_sections_present`
* `core_metadata_extracted`
* `player_metadata_extracted`
* `metadata_emitted`

Recommended statuses:

* `pass`
* `warn`
* `fail`
* `not_evaluated`

Recommended severities:

* `required`
* `warning`

Suggested posture:

* `raw_parse_schema_valid`, `replay_hash_present`, `source_raw_parse_sha256_computed`, `required_sections_present`, `core_metadata_extracted`, `metadata_emitted` → `required`
* `parse_receipt_hash_match`, `parse_report_status_parsed`, `player_metadata_extracted` → `warning` or `required` depending on actual contract choice, but stay conservative and explicit

## Tests

Keep CI fixture-driven.

### Fixtures

Add M09 source fixtures based on M08-style artifacts, for example:

* valid `replay_raw_parse.json`
* valid `replay_parse_receipt.json`
* valid `replay_parse_report.json`
* partial raw parse variants with missing sections
* ambiguous player metadata variants
* source-contract mismatch fixtures

Do **not** require `s2protocol` to be installed in CI.

### Unit tests

Add tests for:

* deterministic extraction from valid raw parse input
* `null` / `unknown` behavior when source fields are absent
* player ordering determinism
* enum mapping correctness
* fixed `source_sections_present` ordering
* report ordering and reason/advisory sorting
* rejection of malformed source shapes

### CLI tests

Add tests for:

* expected file creation
* exit code mapping
* repeated-run determinism
* receipt/report linkage checks
* partial extraction behavior

### Governance tests

Update `tests/test_governance.py` to require:

* `docs/runtime/replay_metadata_extraction.md`
* M09 module surfaces
* M09 fixture coverage
* M09 milestone files
* M10 stub creation during closeout

## Acceptance criteria

M09 is complete only when all of the following are true:

* `docs/runtime/replay_metadata_extraction.md` exists and matches implementation.
* `replay_metadata.json` and `replay_metadata_report.json` are emitted deterministically.
* The metadata contract is explicitly stable and smaller than raw M08 parser output.
* M09 consumes M08 artifacts rather than re-invoking parser logic by default.
* CI remains fixture-driven and does not require live SC2 execution.
* No M10 event/timeline semantic contract is introduced.
* No M11 build-order logic is introduced.
* `docs/starlab.md` is updated at closeout with explicit proofs and non-proofs.
* `M09_run1.md`, `M09_summary.md`, and `M09_audit.md` are created.
* `M10_plan.md` and `M10_toolcalls.md` stubs are seeded during closeout.

## Explicit non-claims for summary / audit / ledger

Cursor should repeat these at closeout:

* M09 proves a stable normalized replay metadata contract derived from M08 raw parse artifacts.
* M09 does not prove event/timeline semantics, build-order extraction, benchmark integrity, replay↔execution equivalence, or live SC2 execution in CI.
* M09 narrows raw parser-owned structures into a public metadata contract; it does not certify the full semantic truth of Blizzard replay structures in the broad sense.

## Branch and PR guidance

Recommended branch:

* `m09-replay-metadata-extraction`

Recommended PR title:

* `M09: replay metadata extraction`

Keep the PR tightly bounded to M09. Do not pull M10 event semantics or M11 build-order work into the same branch.

## CI guidance

* Preserve required checks.
* Do not weaken governance or security posture.
* Keep M09 fixture-driven by default.
* Avoid extra post-closeout pushes unless a true correction is needed.
* If a documentation-only follow-up becomes necessary after closeout, carry it on the M10 branch rather than reopening M09 unnecessarily.

## Closeout instructions for Cursor

At milestone closeout, Cursor should:

1. update `docs/starlab.md`,
2. create `M09_run1.md`, `M09_summary.md`, `M09_audit.md`,
3. mark `M09_plan.md` complete,
4. append `M09_toolcalls.md`,
5. create `docs/company_secrets/milestones/M10/M10_plan.md` stub,
6. create `docs/company_secrets/milestones/M10/M10_toolcalls.md` stub,
7. merge M09 cleanly,
8. create a new branch for M10 if any post-closeout work remains.

---

Two `docs/starlab.md` improvements are worth making once M09 closes: add a compact **Phase II artifact-contract row** for M09 showing `replay_metadata.json` and `replay_metadata_report.json`, and extend the current parser glossary with a short **metadata field glossary** that distinguishes replay identity fields, map/game metadata, player metadata, and still-deferred event semantics. That will make the M08→M09→M10 boundary easier to audit and harder to blur.

---

**Status:** Locked — implementation authorized (2026-04-07).
