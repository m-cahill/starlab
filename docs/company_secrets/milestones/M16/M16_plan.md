# M16 Plan — Structured State Pipeline

## Milestone identity

* **Milestone:** M16 — Structured State Pipeline
* **Phase:** III — State, Representation, and Perception Bridge
* **Suggested branch:** `m16-structured-state-pipeline`
* **Suggested PR title:** *(set at PR open — e.g. “M16: structured canonical state pipeline”)*
* **Target tag:** `v0.0.16-m16`
* **Status:** **Complete** — closed 2026-04-08; see `M16_summary.md`, `M16_audit.md`, `M16_run1.md`, `M16_toolcalls.md`

## Handoff context (M15 closeout)

M15 closed as **schema-only**: deterministic `canonical_state_schema.json` / report emission and `jsonschema` validation, with **replay-to-state extraction explicitly deferred to M16**. The audit posture is to keep M16 **tightly bounded to pipeline work** and **not** collapse schema (M15), pipeline (M16), and observation (M17) boundaries.

An external draft (`M16_plan_draft.md`) was referenced at handoff; it is **not** in this repository. This document is the **authoritative M16 plan** for the repo.

## Why this milestone exists

M15 proved the **canonical state schema contract** and validation surface, but it did **not** prove replay-to-state extraction. M16 does one thing well: **materialize one deterministic canonical state frame at one requested `gameloop` from governed replay artifacts packaged as an M14 bundle**, while keeping observation surfaces, perceptual bridges, and benchmark claims out of scope.

## Goal

Build the first governed pipeline that consumes an **M14 replay bundle** and emits a **single M15-shaped canonical state artifact** plus a deterministic report for one requested `gameloop`.

## Primary deliverables

1. **Runtime contract doc**
   * Add `docs/runtime/canonical_state_pipeline_v1.md`.
   * Document:
     * required inputs
     * source precedence rules
     * target `gameloop` selection policy
     * field derivation rules
     * deterministic serialization/report rules
     * explicit non-claims

2. **Product modules under `starlab/state/`**
   * Add a narrow, pipeline-only implementation surface, for example:
     * `canonical_state_inputs.py`
     * `canonical_state_derivation.py`
     * `canonical_state_pipeline.py`
     * `emit_canonical_state.py`
   * Keep naming flexible if existing module layout suggests a clearer split, but keep pipeline logic isolated from schema-generation code.

3. **Governed artifacts**
   * Emit:
     * `canonical_state.json`
     * `canonical_state_report.json`
   * `canonical_state.json` must validate against the existing M15 schema artifact (`canonical_state_schema.json` / `build_canonical_state_json_schema()`).
   * `canonical_state_report.json` must include deterministic provenance and derivation evidence.

4. **CLI**
   * Add a small emit CLI, e.g.:
     * `python -m starlab.state.emit_canonical_state --bundle-dir ... --gameloop ... --output-dir ...`
   * The CLI must only materialize **one frame per invocation**.

5. **Fixtures and tests**
   * Add M16 fixtures and golden outputs.
   * Add unit, CLI, and governance coverage for the new pipeline.

## Required input boundary

M16 must treat the **M14 replay bundle** as the canonical upstream packaging boundary.

### Required upstream artifacts

The pipeline should require the governed JSON artifacts packaged by M14, not raw replay bytes:

* `replay_bundle_manifest.json`
* `replay_bundle_lineage.json`
* `replay_bundle_contents.json`
* bundled primary governed replay artifacts from M09–M13:
  * `replay_metadata.json`
  * `replay_timeline.json`
  * `replay_build_order_economy.json`
  * `replay_combat_scouting_visibility.json`
  * `replay_slices.json`

### Hard boundary rules

* **Do not** consume raw `.SC2Replay` bytes.
* **Do not** consume `replay_raw_parse.json`.
* **Do not** add `s2protocol` or parser coupling to M16 modules.
* **Do not** bypass the M14 bundle contract by wiring directly to ad hoc source files in product code.

## Scope

### In scope

* Deterministic materialization of **one** canonical state frame for **one** requested `gameloop`
* Validation of emitted state against the M15 schema
* Conservative field derivation from governed M09–M13 artifacts packaged by M14
* Deterministic report emission with hashes/provenance/warnings
* CLI + fixture-backed tests
* Ledger, summary, audit, and M17 stubs at closeout

### Out of scope

* Observation surface / agent-facing API (M17)
* Perceptual bridge work (M18)
* Multi-frame sequence export
* Tensorization / action masks / observation masks
* Live SC2 in CI
* Raw replay parsing changes
* Replay↔execution equivalence claims
* Benchmark integrity claims
* Exact mineral/gas bank reconstruction
* Certified fog-of-war truth
* Any M17+ product code

## Narrow state model posture for M16

M16 should stay conservative and only populate fields supportable from already-governed upstream artifacts.

### Source precedence

Use this precedence when multiple upstream artifacts are relevant:

1. **M14 bundle metadata/lineage** — packaging identity and provenance only
2. **M09 replay metadata** — static replay/map/player identity fields
3. **M10 replay timeline** — canonical event chronology
4. **M11 build-order/economy** — economy/build-order categorizations and counts where explicitly represented
5. **M12 combat/scouting/visibility** — combat windows, scouting state, visibility proxies
6. **M13 replay slices** — optional contextual slice membership only; never primary state reconstruction input

### Recommended derivation posture

* Reconstruct state by **folding deterministic upstream events/windows up to and including the requested `gameloop`**.
* Treat interval/window membership as active iff the target `gameloop` is inside the documented interval.
* Prefer emitting **counts/categories/proxy visibility** over precise hidden-state claims.
* If an M15 field cannot be supported conservatively from M09–M13 artifacts, emit the schema-valid conservative form rather than inventing data.

## Artifact requirements

### `canonical_state.json`

Required characteristics:

* schema-valid against M15 `canonical_state_schema.json`
* represents exactly one `gameloop`
* deterministic key ordering/serialization
* includes provenance fields linking back to the source M14 bundle
* contains only M16-supported conservative semantics

### `canonical_state_report.json`

Include at minimum:

* `report_version`
* `target_gameloop`
* `source_bundle_id` / lineage root where applicable
* hashes of required source artifacts
* hash of emitted `canonical_state.json`
* hash of M15 schema used for validation
* derivation summary (which upstream artifacts contributed)
* warnings / non-claims / degraded-field notes

## Implementation plan

### Step 1 — Freeze the derivation contract before coding

Add `docs/runtime/canonical_state_pipeline_v1.md` and define:

* required bundle members
* allowed optional members
* exact `gameloop` policy:
  * integer only
  * hard fail if negative or beyond replay length
* source precedence
* field mapping table
* failure conditions
* non-claims

### Step 2 — Add bundle input loader and integrity checks

Implement a loader that:

* reads bundle manifest / contents / lineage
* verifies required members are present
* loads bundled M09–M13 primary artifacts
* checks internal consistency needed for materialization
* fails loudly on missing or inconsistent required inputs

The loader should produce a typed internal input object consumed by derivation code.

### Step 3 — Implement deterministic frame derivation

Implement a pure derivation layer that:

* takes typed bundle inputs + requested `gameloop`
* folds M10/M11/M12 evidence up to target loop
* builds an M15-shaped state object
* avoids any schema generation responsibility
* returns a structure ready for validation + I/O

Keep derivation code side-effect-free so it is easy to unit test.

### Step 4 — Validate and emit artifacts

Implement a pipeline wrapper that:

* validates the state against the existing M15 schema
* emits `canonical_state.json`
* builds and emits `canonical_state_report.json`
* uses deterministic JSON output
* computes stable hashes for report linkage

### Step 5 — Add CLI

The CLI should:

* accept `--bundle-dir`, `--gameloop`, `--output-dir`
* validate inputs early
* produce exactly the two governed M16 artifacts
* exit non-zero on validation/integrity/derivation failure

### Step 6 — Add fixtures and tests

Add fixture-backed tests for:

* deterministic repeat emission from the same bundle + `gameloop`
* schema validation success for emitted `canonical_state.json`
* correct failure on missing required bundle member
* correct failure on out-of-range `gameloop`
* correct handling of lineage/content inconsistency
* CLI happy path
* CLI failure path
* governance expectations for M16 docs/files

### Step 7 — Closeout and ledger discipline

At closeout, update:

* `docs/starlab.md`
* `docs/company_secrets/milestones/M16/M16_run1.md`
* `M16_summary.md`
* `M16_audit.md`
* `M16_plan.md` (status complete)
* `M16_toolcalls.md`
* `tests/test_governance.py`

Seed **M17 stubs only**:

* `docs/company_secrets/milestones/M17/M17_plan.md`
* `docs/company_secrets/milestones/M17/M17_toolcalls.md`

## Acceptance criteria

1. `canonical_state.json` and `canonical_state_report.json` are emitted deterministically from an M14 bundle + requested `gameloop`.
2. `canonical_state.json` validates against the existing M15 schema artifact.
3. Product code consumes only governed M14-packaged replay artifacts; no raw replay bytes, no `replay_raw_parse.json`, no `s2protocol`.
4. One invocation emits **one frame only**.
5. Fixture-backed tests cover happy path, integrity failures, range failures, CLI, and determinism.
6. Required CI remains green with no workflow weakening.
7. Ledger and milestone artifacts accurately record that M16 proves **pipeline materialization only**, not observation or perception surfaces.

## Explicit non-claims to preserve

M16 does **not** prove:

* an observation surface contract
* tensors / batched state / sequences
* action masks
* perceptual bridge behavior
* live SC2 execution in CI
* replay↔execution equivalence
* benchmark integrity
* exact resource bank reconstruction
* true fog-of-war certification

## CI / audit guardrails

* Do not weaken any required checks.
* Prefer **no new runtime dependencies** unless strictly necessary.
* If typing support or dependency fixes are needed, land them in the same milestone branch before merge.
* Treat the **authoritative** merge signal as green PR-head CI on the final tip plus green merge-boundary `main` CI.
* Avoid repeated closeout-only churn on `main`; if follow-up fixes are discovered after closeout, carry them on the next milestone branch.

## Suggested closeout prompt for Cursor

At milestone closeout, do all of the following explicitly:

1. Generate `M16_summary.md` and `M16_audit.md` using the standard company prompts.
2. Update `docs/starlab.md` with:
   * M16 proved/not-proved text
   * Phase III artifact row for M16
   * milestone table status
   * current milestone → M17
   * closeout ledger row
   * score trend row/note
   * changelog entry
3. Update `tests/test_governance.py` for M16 complete and M17 stub presence.
4. Merge the milestone branch only after green PR-head CI.
5. Confirm merge-boundary `main` CI.
6. Seed M17 stub files only.
7. If any post-closeout fix is needed, create it on the next milestone branch rather than adding needless doc-only churn to the closed milestone.

## `docs/starlab.md` improvements during M16 closeout

When M16 closes, improve the ledger by adding:

* a compact glossary entry distinguishing **canonical state frame materialization** from **observation surface contract**
* an explicit note that M16 consumes **M14 bundles as the packaging boundary**
* a brief field-precedence note for M09/M10/M11/M12 contributions to M16 state derivation

## Implementation defaults (freeze in contract doc)

These are **defaults for M16 implementation**; `docs/runtime/canonical_state_pipeline_v1.md` remains authoritative and may refine them.

* **`replay_derived`:** M16-emitted frames use `frame_kind: "replay_derived"` (replay snapshotting of live state is not in scope).
* **Player index:** Canonical state `players[].player_index` uses **0-based** indices to satisfy the M15 schema (`minimum: 0`). Normalize from upstream 1-based SC2-style indices where present.
* **Replay length for `gameloop` range checks:** Define `replay_length_loops` as the **maximum** of `metadata.game.game_length_loops` (when present and non-negative) and the maximum `gameloop` among M10 timeline `entries` (when present). Reject `--gameloop` if `gameloop < 0` or `gameloop > replay_length_loops`. If the two sources disagree materially, treat as an integrity failure or document a deterministic resolution in the contract doc (prefer failing loudly over silent pick).

## Suggested PR checklist

* [ ] Contract doc `docs/runtime/canonical_state_pipeline_v1.md`
* [ ] Pipeline modules under `starlab/state/` (no schema builder changes in pipeline path)
* [ ] CLI `python -m starlab.state.emit_canonical_state`
* [ ] Fixtures + golden `canonical_state.json` / `canonical_state_report.json`
* [ ] Tests: unit, CLI, governance
* [ ] No new runtime deps unless justified in `pyproject.toml` and audit
