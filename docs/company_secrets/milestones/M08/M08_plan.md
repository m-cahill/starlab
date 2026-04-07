# M08 Plan — Replay Parser Substrate

## Objective

Stand up a **narrow, governed replay parser substrate** for STARLAB that can take a replay already admitted through M07-style governance, route it through the canonical replay decode boundary, and emit deterministic, audit-friendly parse artifacts for later milestones.

M08 should prove the **parser surface exists** and is usable as a governed substrate. It should **not** yet prove normalized metadata semantics, event/timeline interpretation, build-order extraction, benchmark validity, or live SC2 execution in CI.

## Resolved constraints

These are fixed unless implementation reveals a hard repo-local conflict.

* The canonical replay decode boundary remains **`s2protocol`**.
* Keep M08 **small** and **substrate-only**. Do not pull M09 metadata extraction, M10 timeline extraction, or M11 build-order logic forward.
* CI must remain **fixture-driven** and must **not** add live SC2 execution.
* Do **not** commit unclear-rights third-party replay bytes merely to satisfy parser tests.
* Prefer deterministic parser-output fixtures and adapter-level tests in CI.
* If a legally safe local replay is available, a **local smoke note** may be recorded as evidence, but it is **not** the merge gate by default.
* Reuse M03/M04/M05/M07 governed artifacts where that reduces drift and keeps one canonical interpretation of prior JSON contracts.   

## What M08 should prove

M08 should prove, narrowly, that STARLAB can:

* invoke a governed replay parser boundary through an explicit adapter,
* lower parser-native output into deterministic, JSON-safe STARLAB artifacts,
* bind parser output back to replay identity already established by replay bytes / prior receipts,
* emit deterministic parse artifacts suitable for downstream consumption by M09 and M10,
* distinguish parse success from unsupported protocol / parser-unavailable / parse-failed conditions.

## What M08 must not claim

M08 must **not** claim:

* replay parser correctness in the broad sense,
* stable semantic interpretation of parser output,
* normalized replay metadata as a public contract,
* event/timeline semantics,
* build-order extraction,
* replay↔execution semantic equivalence,
* benchmark integrity,
* cross-host portability,
* live SC2 execution in CI,
* legal certification of replay rights.

Those remain out of scope and should be repeated in summary, audit, and ledger closeout.  

## Primary deliverables

### 1. Contract document

Create:

* `docs/runtime/replay_parser_substrate.md`

This doc should define:

* the M08 parser substrate contract,
* parser boundary and adapter model,
* input expectations,
* output artifact schemas,
* parse status model,
* normalization rules for parser-native objects,
* deterministic failure/reporting behavior,
* explicit non-claims,
* relation to M07 intake, M09 metadata extraction, and M10 timeline extraction.

### 2. Parser boundary

Introduce a clear adapter boundary under `starlab/replays/`.

Recommended shape:

* `starlab/replays/parser_models.py`
* `starlab/replays/parser_interfaces.py`
* `starlab/replays/parser_normalization.py`
* `starlab/replays/parser_io.py`
* `starlab/replays/s2protocol_adapter.py`
* `starlab/replays/parse_replay.py`

Responsibilities:

* `parser_models.py`: enums, dataclasses, schema constants
* `parser_interfaces.py`: parser protocol / adapter interface only
* `parser_normalization.py`: deterministic lowering of parser-native objects to JSON-safe STARLAB objects
* `parser_io.py`: artifact assembly, file IO, replay hashing, linkage checks
* `s2protocol_adapter.py`: the concrete `s2protocol` implementation, isolated behind the interface
* `parse_replay.py`: CLI only

If the repo already has a stronger local naming pattern, preserve consistency over these exact filenames.

### 3. Artifacts

Emit exactly three governed artifacts.

#### `replay_parse_receipt.json`

Recommended schema version:

* `starlab.replay_parse_receipt.v1`

Purpose:

* canonical record of parser invocation and linkage to replay identity.

Recommended fields:

* `schema_version`
* `replay_content_sha256`
* `observed_filename`
* `parser_family`
* `parser_version`
* `parse_input_artifacts`
* `raw_parse_sha256`
* `policy_version`
* `parser_contract_version`

#### `replay_parse_report.json`

Recommended schema version:

* `starlab.replay_parse_report.v1`

Purpose:

* deterministic parser status and ordered check results.

Recommended fields:

* `schema_version`
* `replay_content_sha256`
* `parser_family`
* `parser_version`
* `parse_status`
* `check_results`
* `reason_codes`
* `advisory_notes`

#### `replay_raw_parse.json`

Recommended schema version:

* `starlab.replay_raw_parse.v1`

Purpose:

* deterministic, JSON-safe raw parser envelope for downstream milestones.

Recommended top-level fields:

* `schema_version`
* `replay_content_sha256`
* `parser_family`
* `parser_version`
* `protocol_context`
* `raw_sections`
* `event_streams_available`
* `normalization_profile`

### 4. Raw parse scope

Keep the raw parse envelope intentionally narrow and non-semantic.

Recommended `raw_sections`:

* `header`
* `details`
* `init_data`

Optional only if already cheaply available and deterministic through the adapter:

* `attribute_events`

Do **not** normalize these into public replay metadata in M08. M08 may capture raw blocks; M09 will own stable metadata extraction.

For event streams, M08 should expose **availability / capability**, not normalized timeline semantics. Example:

* `game_events_available`
* `message_events_available`
* `tracker_events_available`

## Normalization rules

M08's real technical value is deterministic lowering of parser-native output. Define this clearly.

Recommended rules:

* dictionaries sorted by key,
* tuples converted to lists,
* bytes lowered deterministically to lowercase hex strings,
* enums lowered to strings,
* unsupported objects rejected explicitly,
* no NaN / Infinity,
* deterministic handling for absent sections,
* no timestamps generated by STARLAB during normalization beyond explicit artifact metadata if needed.

This should be the main pure logic surface of the milestone and heavily unit tested.

## Status model

Use a small parse status model.

Recommended statuses:

* `parsed`
* `unsupported_protocol`
* `parser_unavailable`
* `parse_failed`
* `input_contract_failed`

Interpretation:

* `parsed`: parser ran and raw parse artifact was emitted
* `unsupported_protocol`: replay could be read but the decoder could not support the replay's protocol/build
* `parser_unavailable`: required parser dependency / adapter unavailable
* `parse_failed`: adapter invoked but parse failed
* `input_contract_failed`: linked artifact mismatch or malformed input before parse could be trusted

## Check model

Emit ordered checks similar to M06/M07.

Recommended checks:

* `replay_file_readable`
* `replay_sha256_computed`
* `parser_dependency_available`
* `parser_adapter_selected`
* `intake_receipt_hash_match`
* `binding_hash_match`
* `parse_attempted`
* `raw_sections_normalized`
* `raw_parse_emitted`

Recommended statuses:

* `pass`
* `warn`
* `fail`
* `not_evaluated`

Recommended severities:

* `required`
* `warning`

## Input linkage

M08 should support replay parsing with optional governance linkage.

Recommended CLI inputs:

```bash
python -m starlab.replays.parse_replay \
  --replay path/to/file.SC2Replay \
  --output-dir path/to/out \
  [--intake-receipt path/to/replay_intake_receipt.json] \
  [--intake-report path/to/replay_intake_report.json] \
  [--replay-binding path/to/replay_binding.json]
```

Linkage rules:

* If `--intake-receipt` is supplied, replay hash must match.
* If `--replay-binding` is supplied, `replay_content_sha256` must match.
* `--intake-report` is advisory context only unless you deliberately need it for a required consistency check.
* M08 should still be usable on a replay file alone for controlled local experimentation, but governed linkage should be preferred when prior artifacts exist.

## Dependency posture

Introduce the parser dependency carefully.

Recommended posture:

* `s2protocol` is the only canonical parser substrate in M08.
* Keep it isolated behind the adapter boundary.
* Do not spread parser-specific imports across the repo.
* If dependency pinning is added or changed, record the boundary update in the contract doc and ledger closeout.

## Tests

Keep CI fixture-driven.

### Fixtures

Recommended fixtures:

* parser-output fixtures representing raw adapter returns for header/details/init_data
* malformed parser payload fixtures
* unsupported-protocol fixtures
* parser-unavailable fixtures

Avoid committing unclear-rights raw replays solely for CI.

If a legally safe first-party replay exists and is acceptable to commit, it may be used, but do not assume that path.

### Unit tests

Add tests for:

* normalization of bytes / tuples / enums / nested dicts
* deterministic JSON emission across repeated runs
* ordered check emission
* hash/linkage mismatch handling
* status transitions for all parse statuses
* unsupported object rejection

### CLI tests

Add tests for:

* expected file creation
* exit code mapping
* deterministic output on repeated runs
* optional linkage inputs

### Governance tests

Update `tests/test_governance.py` to require:

* `docs/runtime/replay_parser_substrate.md`
* M08 module surfaces
* parser fixtures
* M08 milestone files
* M09 stub creation during closeout

### Optional local evidence

If a legally safe local replay is available outside the repo, add a local-only evidence note under `docs/company_secrets/milestones/M08/` showing one adapter-backed parse smoke.

This should be:

* explicitly non-merge-gate,
* clearly labeled local/manual,
* narrow in claims,
* redacted as needed.

## Acceptance criteria

M08 is complete only when all of the following are true:

* `docs/runtime/replay_parser_substrate.md` exists and matches implementation.
* The parser boundary exists and isolates `s2protocol`.
* The CLI emits deterministic `replay_parse_receipt.json`, `replay_parse_report.json`, and `replay_raw_parse.json`.
* Deterministic normalization of parser-native structures is tested.
* CI remains fixture-driven and does not add live SC2 execution.
* No M09 metadata normalization contract is introduced.
* No M10 timeline/event semantic contract is introduced.
* `docs/starlab.md` is updated at closeout with explicit proofs and non-proofs.
* `M08_run1.md`, `M08_summary.md`, and `M08_audit.md` are created.
* `M09_plan.md` and `M09_toolcalls.md` stubs are seeded during closeout.

## Explicit non-claims for summary / audit / ledger

Cursor should repeat these at closeout:

* M08 proves a governed replay parser substrate and deterministic lowering of raw parser output into STARLAB artifacts.
* M08 does not prove replay parser correctness in the broad sense, replay semantic extraction, benchmark integrity, replay↔execution equivalence, or live SC2 execution in CI.
* M08 exposes raw parser-owned sections for downstream use; it does not yet define stable normalized metadata or event semantics.

## Branch and PR guidance

Recommended branch:

* `m08-replay-parser-substrate`

Recommended PR title:

* `M08: replay parser substrate`

Keep the PR tightly bounded to M08. Do not pull M09 metadata extraction into the same branch.

## CI guidance

* Preserve required checks.
* Do not weaken governance or security posture.
* Keep M08 fixture-driven by default.
* Avoid extra post-closeout pushes unless a true correction is needed.
* If documentation-only follow-up becomes necessary after closeout, carry it on the M09 branch rather than reopening M08 unnecessarily.

## Closeout instructions for Cursor

At milestone closeout, Cursor should:

1. update `docs/starlab.md`,
2. create `M08_run1.md`, `M08_summary.md`, `M08_audit.md`,
3. mark `M08_plan.md` complete,
4. append `M08_toolcalls.md`,
5. create `docs/company_secrets/milestones/M09/M09_plan.md` stub,
6. create `docs/company_secrets/milestones/M09/M09_toolcalls.md` stub,
7. merge M08 cleanly,
8. create a new branch for M09 if any post-closeout work remains.

## Post-closeout `docs/starlab.md` improvements

Two improvements to make at M08 closeout:

1. Add a compact **Phase II artifact-contract row** for M08 in the existing table showing `replay_parse_receipt.json`, `replay_parse_report.json`, and `replay_raw_parse.json`.
2. Add a small **parser glossary** distinguishing raw parse blocks, normalized metadata, and event semantics so M09/M10 don't drift terminologically.

## Status

**Active** — replaced stub plan at **M08** kickoff (**2026-04-07**).
