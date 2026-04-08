# M15 Plan — Canonical State Schema v1

## Milestone identity

**Milestone:** M15 — Canonical State Schema v1  
**Phase:** III — State, Representation, and Perception Bridge  
**Recommended branch:** `m15-canonical-state-schema-v1`

## Objective

Implement a **deterministic, governed canonical state schema v1** for STARLAB’s replay-native state representation layer.

M15 should prove, narrowly, that STARLAB can define and emit a **stable, machine-readable canonical state schema** and validate example state documents against it, without yet building the structured state extraction pipeline itself.

**What M15 should prove:**

* a governed canonical state schema for a single replay-native state frame
* deterministic schema emission and schema fingerprinting
* explicit omission / nullability rules
* fixture-backed validation of valid and invalid state examples

**What M15 must not claim:**

* structured state extraction from replay bundles (that is M16)
* observation surface semantics (that is M17)
* perceptual bridge behavior (that is M18)
* replay↔execution equivalence
* benchmark integrity
* live SC2 in CI
* fog-of-war truth

This keeps M15 aligned with the current ledger: M14 closed Phase II by packaging replay artifacts, and M15 begins Phase III with **schema**, not pipeline.

## Resolved defaults

1. **Primary artifacts**

   * `canonical_state_schema.json`
   * `canonical_state_schema_report.json`

2. **Contract/profile names**

   * Contract: `starlab.canonical_state_schema.v1`
   * Profile: `starlab.canonical_state_schema.m15.v1`

3. **M15 is schema-first, not pipeline-first**

   * M15 defines the canonical schema and validation rules.
   * M15 does **not** build the replay-to-state extraction pipeline.
   * M16 is where the structured state pipeline should materialize this schema from M14 replay bundles.

4. **Schema scope is a single state frame**

   * Define a canonical schema for one **state frame** at one `gameloop`.
   * Do **not** define a full sequence/tensor/observation pipeline in M15.

5. **Schema is bounded to already-proved replay planes**

   * M09 metadata
   * M10 timeline
   * M11 build-order/economy
   * M12 combat/scouting/visibility
   * M13 slices
   * M14 bundle identity / lineage packaging
   * No raw parse-only fields required
   * No hidden game-truth fields

6. **Unknowns are omitted, not invented**

   * Optional fields omitted when not derivable
   * `null` only when a field is applicable but unresolved by design
   * No guessed defaults

## In scope

### 1. Runtime contract doc

Add `docs/runtime/canonical_state_schema_v1.md` with:

* purpose
* glossary
* schema scope
* state frame definition
* required vs optional sections
* omission / nullability rules
* provenance expectations
* deterministic schema emission rules
* explicit non-claims
* CLI usage

### 2. Product code

Create a new `starlab/state/` surface with:

* `starlab/state/canonical_state_models.py`
* `starlab/state/canonical_state_catalog.py`
* `starlab/state/canonical_state_schema.py`
* `starlab/state/canonical_state_io.py`
* `starlab/state/emit_canonical_state_schema.py`

### 3. Deterministic outputs

Emit:

* `canonical_state_schema.json`
* `canonical_state_schema_report.json`

### 4. Example fixtures and validation

Add fixture examples under:

* `tests/fixtures/m15/valid_canonical_state_example.json`
* `tests/fixtures/m15/invalid_canonical_state_example_missing_required.json`
* `tests/fixtures/m15/expected_canonical_state_schema.json`
* `tests/fixtures/m15/expected_canonical_state_schema_report.json`

### 5. Tests

Add:

* `tests/test_canonical_state_schema.py`
* `tests/test_canonical_state_schema_cli.py`

### 6. Governance updates

Update:

* `tests/test_governance.py`
* M15 milestone files during closeout
* `docs/starlab.md` at closeout only

## Out of scope

Do **not** add:

* replay-to-state extraction logic
* time-series/state-sequence generation
* tensorization
* observation API surfaces
* perception bridge logic
* raw replay bytes
* `s2protocol`
* parser invocation
* benchmark labels or scorecards
* live SC2 in CI
* M16 product code

## Proposed schema model

M15 should define a **single canonical state frame** with conservative, replay-derived structure.

### Top-level state frame shape

Recommended top-level sections:

* `schema_version`
* `frame_kind`
* `source`
* `gameloop`
* `players`
* `global_context`
* `provenance`

### `source`

Should support fields like:

* `source_bundle_id` (from M14 bundle identity when available)
* `source_lineage_root` (optional)
* `source_replay_identity` (optional, from metadata lineage when available)

### `players[]`

Each player entry should be conservative and replay-derived, for example:

* `player_index`
* `race_actual`
* `result` (optional)
* `economy_summary`
* `production_summary`
* `army_summary`
* `combat_context` (optional)
* `scouting_context` (optional)
* `visibility_context` (optional, clearly non-truth-bearing)

### `global_context`

May include:

* `map_name` (if available from metadata plane)
* `active_slice_ids` (optional)
* `active_combat_window_ids` (optional)

### `provenance`

Should state which replay planes contribute fields, e.g.:

* `uses_metadata_plane`
* `uses_timeline_plane`
* `uses_build_order_economy_plane`
* `uses_combat_scouting_visibility_plane`
* `uses_slice_plane`
* `uses_replay_bundle_plane` (M14 bundle / lineage)

## Schema rules

1. **Conservative derivation only**

   * Every field must be supportable from already-proved replay artifacts.
   * No full hidden-state or omniscient game-truth semantics.

2. **No exact resource reconstruction claims**

   * M11 explicitly did not prove exact resource reconstruction.
   * So M15 should prefer summaries/counts/categories over exact mineral/gas values.

3. **Visibility remains conservative**

   * M12 visibility signals must not be upgraded into certified fog-of-war truth.
   * Visibility-related fields in the schema must preserve that non-claim.

4. **No player names / raw chat / PII**

   * Stay aligned with the existing public replay metadata/timeline posture.

5. **Deterministic schema fingerprint**

   * `canonical_state_schema_report.json` should include a canonical hash of the emitted schema.

## Suggested report contents

`canonical_state_schema_report.json` should include:

* `contract`
* `profile`
* `schema_sha256`
* `required_top_level_fields`
* `required_player_fields`
* `optional_sections`
* `omission_rules`
* `non_claims`
* `example_fixture_hashes`

## CLI

Recommended CLI:

```text
python -m starlab.state.emit_canonical_state_schema --output-dir DIR
```

No replay input is required in M15. This milestone is about emitting and validating the schema contract, not running the structured state pipeline.

## Acceptance criteria

M15 is done when all of the following are true:

1. `canonical_state_schema.json` and `canonical_state_schema_report.json` are emitted deterministically.
2. The schema validates at least one valid example state and rejects invalid examples.
3. The schema stays conservative relative to what M09–M14 actually proved.
4. No extraction pipeline is introduced in M15.
5. No `s2protocol`, parser CLI, or raw replay bytes are introduced.
6. CLI exists and is covered by tests.
7. Ruff, format, Mypy, Pytest, pip-audit, SBOM, Gitleaks remain green in PR CI.
8. Governance tests reflect M15 files and milestone state.
9. `docs/starlab.md` is updated at closeout with exact M15 proof/non-proof language.
10. M16 stubs are created after closeout.

## Suggested tests

Minimum test matrix:

* deterministic golden schema emission
* deterministic schema report emission
* valid example passes validation
* invalid example fails validation
* omission/nullability rules enforced
* schema fingerprint stable
* CLI success path
* governance path updates

## CI and merge discipline

Keep the established pattern:

* green PR-head `pull_request` CI on final tip
* green merge-boundary `main` CI after merge
* one closeout/doc pass on `main` when possible

If a fix is needed after closeout, carry it on the **M16 branch** instead of repeated `main` churn.

## Explicit non-claims for M15 summary/audit

Use wording close to this at closeout:

> M15 proves deterministic canonical state schema v1 and validation over fixture examples.
> M15 does not prove replay-to-state extraction, observation semantics, perceptual bridge behavior, replay↔execution equivalence, benchmark integrity, or live SC2 in CI.

## Closeout instructions for Cursor

After implementation and green CI:

1. complete `M15_summary.md`, `M15_audit.md`, `M15_run1.md`, `M15_toolcalls.md`, and finalize `M15_plan.md`
2. update `docs/starlab.md` as the canonical ledger
3. record:

   * PR number
   * final PR head SHA
   * authoritative green PR-head CI run ID
   * merge commit SHA
   * merge-boundary `main` CI run ID
4. merge the PR
5. avoid extra post-merge `main` churn beyond one closeout/doc pass
6. seed `docs/company_secrets/milestones/M16/M16_plan.md`
7. seed `docs/company_secrets/milestones/M16/M16_toolcalls.md`
8. if a follow-up fix is needed after closeout, do it on the M16 branch

## Two small improvements to `docs/starlab.md`

At M15 closeout, add:

1. A **Phase III artifact-contract row** for M15, so the canonical schema artifacts are explicitly named in the ledger.
2. A short glossary distinction between:

   * **M15 canonical state schema**
   * **M16 structured state pipeline**
   * **M17 observation surface contract**

That will make the Phase III boundary as clear as the M13/M14 slice-versus-bundle boundary became in Phase II.

## Status

**Implementation in progress** on branch `m15-canonical-state-schema-v1` — ledger and closeout artifacts pending green CI and merge.
