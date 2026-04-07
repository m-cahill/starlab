# M03 Plan — Run Identity & Lineage Seed

## Milestone identity

* **Milestone:** M03
* **Title:** **Run Identity & Lineage Seed**
* **Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate
* **Suggested branch:** `m03-run-identity-lineage-seed`
* **Suggested tag on closeout:** `v0.0.3-m03`

## Objective

Build the first **STARLAB-owned run identity layer** on top of the M02 harness proof surface.

M03 should establish deterministic, documented primitives for:

* identifying a run configuration
* identifying a concrete execution result
* linking those together in a minimal lineage seed record
* serializing those records in stable, reviewable, STARLAB-owned artifacts

This milestone should make it possible to say:

> We can assign deterministic STARLAB run identity and lineage seed records to a completed execution proof.
> We still do **not** claim replay binding, replay lineage, or a full canonical run artifact.

## Why M03 is the right next move

M02 already provides a bounded execution harness and a deterministic STARLAB proof artifact, with a same-machine matching `artifact_hash` example recorded in the M02 evidence pack. M03 should build on that exact proof surface and stop there. The ledger already states that **replay capture / binding** and **canonical run artifacts** are still not proved, so M03 needs to stay narrow and seed only the identity and lineage layer.

## Success statement

At M03 closeout, STARLAB should be able to say:

> Given a normalized execution proof artifact and its run config, STARLAB can derive deterministic run identity and lineage seed records in a stable, documented format.
> This proves run identity primitives exist.
> It does **not** yet prove replay binding, replay-based lineage, or canonical run artifact packaging.

## Scope

### In scope

* deterministic run identity models
* deterministic lineage seed models
* stable JSON serialization and hashing for those records
* a small CLI or entrypoint that derives identity/lineage seed artifacts from an execution proof + config
* tests for deterministic identity derivation
* docs for the run identity / lineage seed contract
* ledger and README updates

### Out of scope

* replay file attachment or replay hash binding
* replay metadata parsing
* canonical run artifact v0 packaging
* run registry / database / service infrastructure
* benchmark or evaluation semantics
* any new SC2 execution proof beyond what M02 already established

## Hard guardrails

* **Do not start M04 or M05 inside M03.**
* **Do not introduce replay binding.** That belongs to M04.
* **Do not call the new M03 records the canonical run artifact.** That belongs to M05.
* **Do not weaken CI.**
* **Do not require local SC2 execution for M03.** M03 should operate on existing proof/config artifacts and CI-safe fixtures.
* **Do not over-abstract.** Generic names are acceptable, but the implementation should stay grounded in the current SC2 proof surface.

## Design posture

M03 should distinguish between:

* **run intent / spec identity**
* **execution identity**
* **lineage seed**

Recommended interpretation:

* **Run spec ID** — deterministic identity of the intended run shape
* **Execution ID** — deterministic identity of the realized execution proof
* **Lineage seed ID** — deterministic identity of the STARLAB-owned linkage record tying the two together

This avoids pretending we already have a full canonical run artifact or replay-bound lineage system.

## Required deliverables

### 1) Runtime document

Create:

* `docs/runtime/run_identity_lineage_seed.md`

This doc must include:

* what M03 proves
* what M03 explicitly does not prove
* definitions of:

  * run spec ID
  * execution ID
  * lineage seed ID
* the source inputs used to derive each
* normalization rules
* hashing rules
* relationship to M02 proof artifacts
* relationship to later milestones:

  * M04 replay binding
  * M05 canonical run artifact v0

It should also include one short worked example using the M02 proof surface.

### 2) Run identity code surface

Create a small top-level package, preferably:

* `starlab/runs/`

Recommended files:

* `starlab/runs/models.py`
* `starlab/runs/identity.py`
* `starlab/runs/lineage.py`
* `starlab/runs/writer.py`
* `starlab/runs/__init__.py`

You may add or merge files if the surface stays clean.

Recommended models:

* `RunSpecIdentity`
* `ExecutionIdentity`
* `LineageSeedRecord`
* `EnvironmentFingerprint`
* `ArtifactReference`

Recommended behavior:

* deterministic IDs from normalized inputs
* deterministic JSON serialization
* deterministic hash field generation
* wrapper-agnostic public models
* no SC2 runtime imports in this package

### 3) CLI / entrypoint

Add a small user-facing command such as:

```bash
python -m starlab.runs.seed_from_proof --proof path/to/match_execution_proof.json --config path/to/config.json --output-dir path/to/out
```

It should:

* read a proof artifact
* read the corresponding match config
* optionally read probe/environment metadata if provided
* write out stable STARLAB-owned JSON records

Recommended outputs:

* `run_identity.json`
* `lineage_seed.json`

These are **not** the canonical run artifact. They are M03 seed records only.

### 4) Deterministic identity rules

The milestone should define and implement deterministic identity derivation, for example:

* `run_spec_id` derived from normalized run config + boundary label + interface/horizon/seed/map reference
* `execution_id` derived from normalized execution proof or its `artifact_hash`
* `lineage_seed_id` derived from the normalized seed record tying spec and execution together

Important:

* no timestamps in hashed identity fields
* no absolute user-specific paths in hashed identity input
* normalize path-like references to stable logical map keys or redacted refs where appropriate
* keep deterministic comparison attached to STARLAB-owned normalized content, not raw upstream bytes

### 5) Environment fingerprint seed

Introduce a minimal environment fingerprint model that can capture what is known from M01/M02 without overpromising stability.

Suggested fields:

* runtime boundary label
* adapter name
* base build if known
* data version if known
* platform string if intentionally included
* optional probe hash / normalized probe digest

This fingerprint should be clearly documented as:

* helpful for lineage
* not a portability guarantee
* not a full environment lock replacement

### 6) Tests

Add CI-safe tests for:

* deterministic identity derivation from the same inputs
* changed config changes `run_spec_id`
* changed proof changes `execution_id`
* stable serialization of `run_identity.json`
* stable serialization of `lineage_seed.json`
* CLI help / basic end-to-end fixture flow
* governance alignment

Recommended files:

* `tests/test_run_identity.py`
* `tests/test_lineage_seed.py`
* `tests/test_runs_cli.py`
* extend `tests/test_governance.py`

Use fixtures, not live SC2 execution.

A good fixture source is a synthetic or redacted M02-style proof/config pair kept under normal test fixtures.

Add lightweight test fixtures under `tests/fixtures/`, for example:

* `m02_match_config.json`
* `m02_match_execution_proof.json`

These should be small, sanitized, and sufficient for deterministic tests.

Do **not** make tests depend on the tracked milestone evidence files under `docs/company_secrets/...`; keep tests self-contained.

## Required `docs/starlab.md` updates

`docs/starlab.md` remains the canonical public ledger and must be updated during M03 work and again at closeout. Since artifact schemas and public record shapes are contract-affecting surfaces, keep the ledger explicit about what changed and what did not.

### Early-in-branch updates

Update §11 so M03 is clearly the active implementation milestone on the branch if needed.

Add `docs/runtime/run_identity_lineage_seed.md` to the “Start Here” governance-doc list once it exists.

Do **not** yet mark replay binding or canonical run artifacts as proved.

### Closeout updates

At M03 closeout:

* §7 milestone table:

  * M03 → Complete
  * M04 → Planned / next
* §10 proved vs not yet proved:

  * add or update a line for **run identity + lineage seed primitives**
  * keep replay binding and canonical run artifacts explicitly unproved
* §11 current milestone:

  * switch to **M04 — Replay Binding to Run Identity**
* §18 milestone closeout ledger:

  * add PR / merge / CI evidence
* §20 score trend:

  * add M03 score
* §23 changelog:

  * add M03 closeout entry

### Suggested `starlab.md` improvement

M03 is a good time to improve the “Proved vs not yet proved” area by splitting the current execution layer into clearer subclaims:

* runtime boundary + environment lock
* deterministic match harness
* run identity primitives
* replay binding
* canonical run artifact

That will make later audits cleaner.

## Recommended file outputs

Recommended emitted M03 records:

### `run_identity.json`

Should include, at minimum:

* schema/version
* run spec ID
* execution ID
* proof artifact hash
* config hash
* adapter name
* runtime boundary label
* seed
* normalized map reference
* interface summary
* bounded horizon
* optional environment fingerprint

### `lineage_seed.json`

Should include, at minimum:

* schema/version
* lineage seed ID
* run spec ID
* execution ID
* input references
* artifact references
* parent references (likely empty in M03)
* notes on what later milestones may bind

Again: these are **seed** records, not the canonical run artifact.

## Implementation sequence

1. Write `docs/runtime/run_identity_lineage_seed.md`
2. Define models for run identity and lineage seed
3. Implement deterministic identity derivation
4. Implement stable writers
5. Add CLI / entrypoint
6. Add self-contained fixtures
7. Add CI-safe tests
8. Update ledger/docs
9. Run CI and keep scope tight

## Acceptance criteria

M03 is done only if all of the following are true:

1. `docs/runtime/run_identity_lineage_seed.md` exists and clearly defines the M03 contract
2. STARLAB can derive deterministic run identity and lineage seed records from a proof artifact + config
3. The emitted M03 JSON records serialize deterministically
4. Same inputs produce the same IDs and same record hashes
5. Changed config or changed proof changes the appropriate IDs
6. CI is green without requiring local SC2 execution
7. `docs/starlab.md` is updated truthfully
8. M03 does **not** claim replay binding or canonical run artifact v0

## Evidence requirements

Required evidence for closeout:

* green PR-head CI
* green post-merge `main` CI
* milestone summary
* milestone audit
* updated ledger
* deterministic test evidence for IDs / seed records

Optional but useful:

* one worked example in docs showing an M02 proof/config turned into M03 seed records
* a redacted sample `run_identity.json` in milestone artifacts if it helps explain the output shape

## Closeout instructions for Cursor

At closeout:

* create the milestone summary using:

  * `docs/company_secrets/prompts/summaryprompt.md`
* create the milestone audit using:

  * `docs/company_secrets/prompts/unifiedmilestoneauditpromptV2.md`
* analyze the authoritative workflow run using:

  * `docs/company_secrets/prompts/workflowprompt.md`
* ensure all documentation is updated as necessary
* seed the next milestone stubs for **M04**
* do not begin M04 implementation

## Final guidance

M03 should feel like a clean substrate milestone:

* small
* deterministic
* enterprise-grade
* schema-conscious
* explicit about later boundaries

It should make M04 easier, not partially do M04 early.
