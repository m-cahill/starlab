# Observation Surface Contract v1 (M17)

## Purpose

Define the **governed agent-facing observation contract** for **exactly one** player-relative **observation frame** at **one** `gameloop`, bound to **M16 canonical state** semantics. M17 proves **deterministic JSON Schema + report emission + fixture validation** — **not** canonical-state→observation materialization, **not** perceptual bridge behavior (M18), **not** replay parsing, **not** benchmark integrity, **not** live SC2 in CI.

## Upstream dependency (required)

M17 observation design is defined **only** against:

* **`canonical_state.json`** (M16 output) — sole semantic upstream for observation field choices and provenance linkage.
* **`canonical_state_report.json`** — provenance reference only (hashes, warnings); not a substitute for `canonical_state.json` content.
* **M15 / M16 runtime contracts** — `docs/runtime/canonical_state_schema_v1.md`, `docs/runtime/canonical_state_pipeline_v1.md`.

M17 **does not** consume raw `.SC2Replay` bytes, `replay_raw_parse.json`, M14 bundles directly in observation modules, or parser adapters.

## One frame, one viewpoint

* Exactly **one** observation JSON document per validation scope.
* Exactly **one** **player-relative** viewpoint per frame: `metadata.perspective_player_index` (0-based).
* `gameloop` in metadata must match the source canonical state frame’s `gameloop` when the observation is presented as derived from that frame.

## Visibility semantics

* Observations use **`proxy_bounded`** visibility policy by default: aligned with M12/M16 **proxy** visibility posture — **not** certified fog-of-war truth.
* Relation labels (`self`, `ally`, `enemy`, `neutral`) apply where relevant to rows and masks; they are **contract labels**, not omniscient game truth.

## Stable ordering rules

* **Scalar features:** `scalar_features.ordered_entries` is an **array** in **catalog-defined name order** (see `observation_surface_catalog.py`). Each entry is `{ "name", "value" }`.
* **Entity rows:** `entity_rows.rows` is ordered; schema allows future per-unit rows; M17 **valid examples** use **aggregated category** rows only where that matches M16 summaries.
* **Spatial planes:** `spatial_plane_family.planes` is ordered; each plane declares **structural** shape metadata (`grid_height`, `grid_width`, `channel_count`, `channel_order`, optional `coordinate_frame`). M17 **does not** bind these dimensions to M09 map metadata.
* **Action mask families:** `action_mask_families.families` follows a **fixed family order** (see catalog). Each family has a JSON-safe mask representation (`ordered_mask_values`: `0`/`1` per ordered slot).

## Action-mask contract posture

* M17 defines **family-level** mask groups with stable names and ordering — **not** full StarCraft II action coverage, **not** legality computation, **not** dynamic mask generation from state.
* Masks are **JSON-safe** integers (`0`/`1`) in declared slot order — **not** an executable action API.

## Deterministic serialization and report rules

* Schema and report emission use `canonical_json_dumps` (sorted keys, stable UTF-8).
* Report includes `schema_sha256` (canonical JSON hash of the schema object) and optional `example_fixture_hashes` for labeled fixtures.

## Explicit non-claims

M17 does **not** prove:

* A canonical-state → observation **projection** implementation (that is **M18+**).
* Perceptual bridge, pixels, or image-space transforms.
* Multi-frame sequences, rollout batches, or datasets.
* Correctness or completeness of action masks beyond **contract shape**.
* Exact mineral/gas bank truth or certified fog-of-war truth (inherits M11/M12/M16 non-claims).
* Replay↔execution equivalence or benchmark integrity.

## Validation failure conditions

* JSON root must be an object matching `observation_surface_schema.json` (Draft 2020-12).
* Required sections and fields as defined in schema; `additionalProperties: false` where specified.
* Breaking deterministic emission (unsorted keys in emitted artifacts) is a contract failure for tooling tests.
