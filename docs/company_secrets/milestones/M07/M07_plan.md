# M07 Plan — Replay Intake Policy & Provenance Enforcement

**Status: Complete**

## Objective

Build a **narrow, deterministic, CI-safe replay intake gate** for opaque replay files that:

* records declared provenance and redistribution posture,
* enforces an explicit intake policy,
* emits governed JSON artifacts,
* keeps replay parsing and replay semantics **out of scope**.

This milestone is the smallest honest Phase II entry step: it strengthens the replay/data plane without drifting into parser substrate, benchmark claims, or live SC2 execution.

## Resolved constraints

Use these decisions as fixed unless implementation reveals a hard repo-local conflict:

* Treat replay files as **opaque bytes** in M07.
* Keep CI **SC2-free** and **fixture-driven**.
* Do **not** infer legal truth; record operator claims and enforce policy on the declared posture.
* Use a new `starlab/replays/` namespace unless the repo already has a clearly better, consistency-preserving home.
* Reuse M04/M05 artifacts only as **optional evidence inputs**; M07 must still work on standalone opaque replay files.
* Keep the milestone small and reversible; do not pull M08 parser work forward.

## What M07 should prove

M07 should prove, narrowly, that STARLAB can:

* hash an opaque replay file,
* normalize declared replay-intake metadata,
* enforce a deterministic intake-policy decision,
* emit deterministic JSON artifacts for replay intake and provenance posture,
* optionally cross-check supplied M04/M05 lineage artifacts for consistency,
* distinguish local-only use from canonical-review eligibility without parsing the replay.

## What M07 must not claim

M07 must **not** claim:

* replay parser correctness,
* replay semantic extraction,
* build-order or timeline extraction,
* benchmark integrity,
* cross-host portability,
* live SC2 execution in CI,
* final legal certainty about third-party replay rights,
* automatic public redistribution safety.

Those remain outside the milestone boundary.

## Primary deliverables

### 1. Contract document

Create:

* `docs/runtime/replay_intake_policy.md`

This doc should define:

* the M07 contract,
* input expectations,
* output artifact schemas,
* decision statuses,
* required vs advisory checks,
* explicit non-claims,
* relationship to M04, M05, M06, and later M08+ work.

### 2. Intake input contract

Support a validated metadata input file, e.g.:

* `replay_intake_metadata.json`

Recommended schema version:

* `starlab.replay_intake_metadata.v1`

Recommended required fields:

* `schema_version`
* `declared_origin_class`
* `declared_acquisition_channel`
* `declared_provenance_status`
* `declared_redistribution_posture`
* `declared_source_label`

Recommended optional fields:

* `declared_source_reference`
* `operator_note`
* `expected_replay_content_sha256`

Use enums, not free-form policy state, for all decision-driving fields.

### 3. Output artifacts

Emit exactly two governed artifacts.

#### `replay_intake_receipt.json`

Recommended schema version:

* `starlab.replay_intake_receipt.v1`

Purpose:

* canonical record of the replay candidate and normalized declared metadata.

Recommended fields:

* `schema_version`
* `replay_content_sha256`
* `replay_size_bytes`
* `observed_filename`
* `intake_metadata_sha256`
* `normalized_metadata`
* `linked_artifacts`
* `policy_version`

#### `replay_intake_report.json`

Recommended schema version:

* `starlab.replay_intake_report.v1`

Purpose:

* deterministic policy decision and audit-friendly check results.

Recommended fields:

* `schema_version`
* `replay_content_sha256`
* `policy_version`
* `check_results`
* `intake_status`
* `local_processing_allowed`
* `canonical_review_eligible`
* `public_redistribution_allowed`
* `reason_codes`
* `advisory_notes`

## Status model

Use exactly these four statuses:

* `eligible_for_canonical_review`
* `accepted_local_only`
* `quarantined`
* `rejected`

Interpret them as follows:

* `eligible_for_canonical_review`: metadata is structurally valid, provenance posture is explicit, redistribution posture is explicit, and any supplied lineage evidence is consistent. This is **not** automatic corpus promotion.
* `accepted_local_only`: structurally valid, but provenance or redistribution posture is incomplete/weak for canonical review.
* `quarantined`: structurally valid input, but explicit policy conflict or unsafe posture exists.
* `rejected`: unreadable replay, invalid metadata, or hard consistency failure.

This aligns M07 with the standing rule that canonical corpus promotion needs explicit provenance and redistribution posture, while still keeping unknown or risky assets out of silent circulation.

## Decision rules

Implement these rules deterministically.

### `rejected`

Return `rejected` when:

* replay file cannot be read,
* metadata schema is invalid,
* `expected_replay_content_sha256` is provided and mismatches,
* a supplied `replay_binding.json` is provided and its replay hash mismatches the observed replay,
* a required linked artifact is malformed.

### `quarantined`

Return `quarantined` when:

* declared redistribution posture is `forbidden`,
* metadata is structurally valid but explicitly conflicts with supplied evidence,
* origin/provenance claims are contradictory in a way that makes normal downstream use unsafe.

### `accepted_local_only`

Return `accepted_local_only` when:

* replay and metadata are structurally valid,
* replay may be used locally/private for controlled experimentation,
* but provenance/redistribution posture is too weak or incomplete for canonical review.

Typical examples:

* provenance is only `asserted`,
* redistribution posture is `unknown`,
* `declared_origin_class="starlab_generated"` is claimed but no consistent M04 replay binding is supplied.

### `eligible_for_canonical_review`

Return `eligible_for_canonical_review` only when:

* replay and metadata are structurally valid,
* provenance posture is explicit and non-conflicting,
* redistribution posture is explicit and non-conflicting,
* any supplied M04/M05 artifacts are consistent,
* and, for `declared_origin_class="starlab_generated"`, a consistent M04 `replay_binding.json` is present.

Also derive:

* `public_redistribution_allowed = true` only if redistribution posture is explicitly `allowed`
* otherwise `false`

## Check model

Use ordered check results similar to M06’s style. Recommended checks:

* `metadata_schema_valid`
* `replay_file_readable`
* `replay_sha256_computed`
* `origin_class_declared`
* `provenance_status_declared`
* `redistribution_posture_declared`
* `expected_hash_match`
* `binding_hash_match`
* `binding_identity_consistent`
* `canonical_review_requirements_met`

Recommended statuses:

* `pass`
* `warn`
* `fail`
* `not_evaluated`

Recommended severities:

* `required`
* `warning`

Keep ordering deterministic.

## Code shape

Recommended new modules:

* `starlab/replays/intake_models.py`
* `starlab/replays/intake_policy.py`
* `starlab/replays/intake_io.py`
* `starlab/replays/intake_cli.py`

Recommended responsibilities:

* `intake_models.py`: dataclasses / typed models / enums / schema helpers
* `intake_policy.py`: pure policy evaluation
* `intake_io.py`: replay hashing, metadata loading, canonical JSON emission
* `intake_cli.py`: CLI entrypoint only

If the repo already has a better-established pattern for contract modules, preserve local consistency rather than forcing these filenames.

## CLI

Create a CLI similar in posture to earlier milestones.

Recommended command:

```bash
python -m starlab.replays.intake_cli \
  --replay path/to/file.SC2Replay \
  --metadata path/to/replay_intake_metadata.json \
  --output-dir path/to/out \
  [--replay-binding path/to/replay_binding.json] \
  [--run-identity path/to/run_identity.json] \
  [--run-artifact-manifest path/to/manifest.json]
```

Recommended exit codes:

* `0` → `eligible_for_canonical_review`
* `2` → `accepted_local_only`
* `3` → `quarantined`
* `4` → `rejected`

That keeps the command useful both as a reporting surface and as a policy gate.

## Tests

Add only fixture-driven tests.

### Fixtures

Create synthetic opaque replay fixtures, for example:

* `tests/fixtures/replay_m07_sample.SC2Replay`
* `tests/fixtures/replay_m07_generated.SC2Replay`
* `tests/fixtures/replay_m07_metadata_*.json`
* `tests/fixtures/replay_m07_binding_*.json`

These do **not** need to be valid SC2 replays. In M07 they are opaque bytes with realistic filenames.

### Unit tests

Add tests for:

* valid receipt/report emission
* deterministic byte-identical outputs across repeated runs
* local-only downgrade when provenance is incomplete
* quarantine on forbidden redistribution posture
* rejection on invalid metadata
* rejection on replay-binding hash mismatch
* canonical-review eligibility when metadata is explicit and linked evidence is consistent
* sorted `reason_codes` and `advisory_notes`
* stable check ordering

### CLI tests

Add tests for:

* exit code mapping,
* expected file creation,
* repeated-run determinism,
* optional linked-artifact handling.

### Governance tests

Update governance coverage to include:

* M07 contract doc existence,
* M07 milestone files at closeout,
* M08 stub creation during closeout,
* any new public runtime docs linked from the ledger.

## Acceptance criteria

M07 is complete only when all of the following are true:

* `docs/runtime/replay_intake_policy.md` exists and matches implementation.
* The CLI emits deterministic `replay_intake_receipt.json` and `replay_intake_report.json`.
* Fixture-driven tests cover all four intake statuses.
* Optional M04 replay-binding consistency checks work and are tested.
* Required CI checks remain green with no weakening.
* No live SC2 execution is added to CI.
* No replay parser, replay semantic extraction, or benchmark logic is introduced.
* `docs/starlab.md` is updated at closeout with explicit proofs and non-proofs.
* `M07_run1.md`, `M07_summary.md`, and `M07_audit.md` are created.
* `M08_plan.md` and `M08_toolcalls.md` stubs are seeded during closeout.

## Explicit non-claims for the milestone summary/audit

Cursor should repeat these in closeout artifacts:

* M07 proves deterministic replay intake policy enforcement over opaque replay bytes and declared metadata.
* M07 does not prove replay parser correctness, replay semantic extraction, replay equivalence to execution proof, benchmark integrity, or live SC2 execution in CI.
* M07 records declared provenance posture; it does not certify external legal rights as a matter of law.

## Branch and PR guidance

Use a dedicated branch, recommended:

* `m07-replay-intake-policy-provenance-enforcement`

PR title recommendation:

* `M07: replay intake policy and provenance enforcement`

Keep the PR tightly bounded to M07. Do not pull M08 parser scaffolding into the same branch.

## CI guidance

* Preserve the existing green merge-gate posture.
* Do not weaken required checks.
* Keep M07 fixture-driven and SC2-free.
* If a docs-only or ledger-only follow-up is needed **after** M07 closes, carry it on the M08 branch rather than pushing again after the milestone is already closed.

## Closeout instructions for Cursor

At milestone closeout, Cursor should:

1. update `docs/starlab.md`,
2. create `M07_run1.md`, `M07_summary.md`, `M07_audit.md`,
3. mark `M07_plan.md` complete,
4. append `M07_toolcalls.md`,
5. create `docs/company_secrets/milestones/M08/M08_plan.md` stub,
6. create `docs/company_secrets/milestones/M08/M08_toolcalls.md` stub,
7. merge M07 cleanly,
8. create a new branch for M08 if any post-closeout work remains.

---

## Milestone identity

* **Milestone:** M07
* **Title:** **Replay Intake Policy & Provenance Enforcement**
* **Phase:** II — Replay Intake, Provenance, and Data Plane
* **Suggested branch:** `m07-replay-intake-policy-provenance-enforcement`
* **Suggested tag on closeout:** `v0.0.7-m07`

## Policy version (implementation)

* `policy_version` / contract: **`starlab.replay_intake_policy.v1`**
