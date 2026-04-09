# M18 Plan — Perceptual Bridge Prototype

## Milestone identity

* **Milestone:** M18
* **Name:** Perceptual Bridge Prototype
* **Phase:** III — State, Representation, and Perception Bridge
* **Suggested branch:** `m18-perceptual-bridge-prototype`
* **Target tag:** `v0.0.18-m18`

## Why this milestone exists

M15 proved the **canonical state schema** only. M16 proved **bundle → one canonical state frame**. M17 proved the **agent-facing observation contract** only. M18 is the first milestone allowed to prove a **narrow materialization bridge** from one M16 `canonical_state.json` into one M17-shaped observation instance for one player-relative viewpoint at one `gameloop`.

This milestone must stay small: it proves a **prototype bridge**, not a benchmark-ready perception system, not a tensor stack for training, and not a replay↔execution equivalence claim.

## Objective

Implement a governed, deterministic **prototype observation materialization pipeline** that:

1. consumes exactly one M16 `canonical_state.json`;
2. optionally cross-checks provenance against `canonical_state_report.json`;
3. emits exactly one M17-shaped `observation_surface.json` for one `perspective_player_index`;
4. emits deterministic `observation_surface_report.json`; and
5. validates the emitted observation against the existing M17 schema.

## Narrow claim to prove

**M18 proves:** a deterministic, fixture-backed prototype bridge from one canonical state frame to one player-relative observation frame, with explicit warnings and bounded semantics for fields M16 cannot fully support.

## Explicit non-claims

M18 does **not** prove:

* replay parsing or replay bundle loading in `starlab/observation/`;
* raw `.SC2Replay` bytes, `replay_raw_parse.json`, or `s2protocol` use in M18 modules;
* multi-frame batches, rollout datasets, or sequence tensors;
* benchmark integrity, leaderboard validity, or learned-agent capability;
* replay↔execution equivalence;
* full SC2 action coverage or action legality correctness;
* exact banked minerals/gas truth beyond prior bounded claims;
* certified fog-of-war truth;
* live SC2 in CI.

## Upstream boundary

### Required semantic upstream

* `canonical_state.json` from M16

### Optional provenance upstream

* `canonical_state_report.json` from M16, used only for hash/provenance cross-checks and warning propagation

### Forbidden upstreams in M18 observation modules

* M14 replay bundle files directly
* raw replay bytes
* `replay_raw_parse.json`
* parser adapters / `s2protocol`

## Primary artifacts

Emit exactly these files per invocation:

* `observation_surface.json`
* `observation_surface_report.json`

Serialization must use the repo’s canonical JSON path (sorted keys, stable UTF-8) and validate the observation against the M17 schema.

## Runtime contract doc

Create:

* `docs/runtime/perceptual_bridge_prototype_v1.md`

The contract must define:

* required inputs;
* provenance cross-check rules;
* perspective policy (`perspective_player_index`, 0-based);
* exact output filenames;
* stable ordering rules inherited from M17;
* what is populated vs placeholder/prototype in M18;
* explicit non-claims.

## Product code surface

Add M18 pipeline/materialization modules under `starlab/observation/`:

* `observation_surface_inputs.py`
* `observation_surface_derivation.py`
* `observation_surface_pipeline.py`
* `emit_observation_surface.py`

Keep existing M17 contract modules intact:

* `observation_surface_models.py`
* `observation_surface_catalog.py`
* `observation_surface_schema.py`
* `observation_surface_io.py`
* `emit_observation_surface_schema.py`

## Derivation scope

### 1. Metadata and provenance

Materialize:

* `schema_version`
* `gameloop`
* `perspective_player_index`
* `source_canonical_state_sha256`
* optional `source_bundle_id`
* optional `source_lineage_root`

Rules:

* `source_canonical_state_sha256` must be computed from canonical JSON of the loaded M16 state object.
* If `canonical_state_report.json` is supplied, any reported state hash must match the recomputed state hash, or materialization fails.

### 2. Viewpoint section

Materialize a single player-relative viewpoint using the selected player index.

Rules:

* perspective must be 0-based and valid for the source frame;
* relation labels must remain contract labels (`self`, `ally`, `enemy`, `neutral`);
* visibility posture remains **proxy-bounded**, not fog-of-war truth.

### 3. Scalar features

Populate the M17 ordered scalar feature list from M16 supportable fields only.

Required behavior:

* use `ORDERED_SCALAR_FEATURE_NAMES` from the M17 catalog as the sole ordering source;
* emit every scalar entry in the fixed order;
* derive values only from M16-supported fields;
* default unsupported values conservatively and record warnings in the report.

### 4. Entity rows

Populate **aggregated category rows only** in M18.

Rules:

* no fake per-unit rows;
* use `row_kind="aggregated_category"` (or the exact catalog-supported equivalent);
* derive from M16 summary counts only;
* populate optional per-entity fields only where truly supportable; otherwise omit them;
* keep ordering deterministic.

This preserves the future-capable M17 row contract while keeping M18 honest about current upstream limits.

### 5. Spatial plane family

Materialize a **minimal prototype** spatial plane family.

Rules:

* emit declared shape metadata and channel ordering;
* keep shapes structural and internally consistent;
* do not claim binding to replay/map-native dimensions as a semantic proof;
* values may be prototype placeholders or conservative coarse projections where supportable;
* report must explicitly mark prototype plane semantics.

Minimum acceptable M18 posture:

* the spatial plane family is present and schema-valid;
* it is deterministic;
* it does not imply unavailable positional truth.

### 6. Action mask families

Materialize a **prototype family-level mask set** for the fixed M17 family order.

Families should remain the M17 family-level set, e.g.:

* `no_op`
* `selection`
* `camera_or_view`
* `production`
* `build`
* `unit_command`
* `research_or_upgrade`

Rules:

* stable family order only from the M17 catalog;
* `ordered_mask_values` must be JSON-safe integers (`0`/`1`);
* values may be coarse prototype derivations from M16 summaries or conservative placeholders;
* do not claim legality or completeness;
* report must state mask limitations explicitly.

## CLI

Add a materialization CLI:

    python -m starlab.observation.emit_observation_surface \
      --canonical-state PATH \
      --perspective-player-index N \
      --output-dir OUT \
      [--canonical-state-report PATH]

Behavior:

* exactly one observation instance per invocation;
* non-zero exit on load, bounds, provenance mismatch, or schema-validation failure.

## Fixtures

Create fixture set under:

* `tests/fixtures/m18/`

Required fixtures:

* source `canonical_state.json` copied or derived from the M16 golden fixture
* optional matching `canonical_state_report.json`
* golden `expected_observation_surface.json`
* golden `expected_observation_surface_report.json`

The valid observation golden should be **source-informed by the M16 golden fixture**, but treated as the governed prototype output for M18, not as a promise of future algorithmic completeness.

## Tests

Add:

* `tests/test_observation_surface_pipeline.py`

Coverage should include:

1. successful load/materialization from canonical state;
2. golden observation match;
3. deterministic repeated emission;
4. invalid `perspective_player_index` hard failure;
5. optional report hash mismatch hard failure;
6. schema validation of emitted observation;
7. CLI success path;
8. CLI failure path;
9. governance assertions for M18 modules / fixtures / runtime contract doc.

## Governance + docs updates during implementation

Update as needed during implementation:

* `docs/starlab.md` current milestone narrative remains M18 planned/current until closeout
* `tests/test_governance.py`
* `docs/company_secrets/milestones/M18/M18_toolcalls.md`

Do **not** pre-close M18 in the ledger before PR/CI/merge evidence exists.

## Acceptance criteria

M18 is complete only when all of the following are true:

1. `docs/runtime/perceptual_bridge_prototype_v1.md` exists and matches implementation.
2. `starlab/observation/` contains the new M18 pipeline/materialization modules.
3. CLI emits exactly one `observation_surface.json` + `observation_surface_report.json` per invocation.
4. Emitted observation validates against the M17 schema.
5. Fixture-backed goldens exist under `tests/fixtures/m18/`.
6. Tests cover success, determinism, provenance mismatch, bounds errors, and CLI.
7. `ruff check starlab tests` passes.
8. `mypy starlab tests` passes.
9. `pytest` passes.
10. No replay parsing, replay bundle loading, or `s2protocol` imports are introduced in M18 observation modules.
11. No benchmark, legality, or agent-capability claims are added.

## Implementation notes for Cursor

* Reuse existing M17 catalog/schema definitions rather than redefining the contract.
* Keep derivation code pure over loaded JSON objects wherever possible.
* Prefer explicit warnings in `observation_surface_report.json` over silent placeholder behavior.
* Keep prototype semantics narrow and well-labeled.
* Do not widen the milestone into training, benchmark, or M19 reconciliation work.

## Suggested closeout posture

At closeout, `docs/starlab.md` should say M18 proves a **prototype materialization bridge** from M16 canonical state to one M17-shaped observation instance, while **M19** remains the milestone for broader cross-mode reconciliation and audit.

## Suggested next-milestone stub after closeout

Seed only stubs for:

* `docs/company_secrets/milestones/M19/M19_plan.md`
* `docs/company_secrets/milestones/M19/M19_toolcalls.md`

No M19 product code should be added during M18.
