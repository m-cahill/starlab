# Perceptual Bridge Prototype v1 (M18)

## Purpose

Define the **prototype materialization bridge** from **one** M16 `canonical_state.json` to **one** M17-shaped `observation_surface.json` at the same `gameloop`, for **one** `perspective_player_index`, plus deterministic `observation_surface_report.json`.

M18 proves **fixture-backed, deterministic prototype materialization** — **not** replay parsing in `starlab/observation/`, **not** mask legality or full action-space correctness, **not** benchmark integrity, **not** live SC2 in CI.

## Required inputs

* **`canonical_state.json`** (M16) — sole semantic upstream; must validate against the M15/M16 canonical state schema as emitted by the M16 pipeline.

## Optional provenance upstream

* **`canonical_state_report.json`** (M16 pipeline report) — used only for:

  * **Hash cross-check:** `canonical_state_sha256` in the report must equal the SHA-256 (hex) of **canonical JSON** of the loaded `canonical_state.json` object (same algorithm as `sha256_hex_of_canonical_json` in `starlab.runs.json_util`). On mismatch, materialization **fails** (non-zero CLI exit).
  * **Warning propagation:** string entries in `warnings` are copied into the materialization report (labeled as upstream), in addition to M18-local warnings.

## Forbidden upstreams (M18 observation modules)

* M14 replay bundle files directly  
* Raw replay bytes  
* `replay_raw_parse.json`  
* Parser adapters / `s2protocol`

## Perspective policy

* `perspective_player_index` is **0-based** and must refer to an existing `players[].player_index` in the canonical state.
* Exactly **one** player-relative observation frame per CLI invocation.
* Relation labels on entity rows use contract values (`self`, `ally`, `enemy`, `neutral`). M18 emits **`self`** rows from the perspective player’s aggregated army categories and **`enemy`** rows for **other** players only where M16 provides positive category counts (no fabricated neutral rows).

## Outputs (exact filenames)

Per invocation, the materialization CLI writes:

* `observation_surface.json`
* `observation_surface_report.json`

Serialization uses **`canonical_json_dumps`** (sorted keys, stable UTF-8, trailing newline on files).

The observation **must** validate against the **M17** JSON Schema (`build_observation_surface_json_schema`).

## Stable ordering (inherited from M17)

* **Scalar features:** `ORDERED_SCALAR_FEATURE_NAMES` in `observation_surface_catalog.py` — sole order; every name appears once in `scalar_features.ordered_entries`.
* **Entity rows:** deterministic sort — `self` rows first (categories sorted), then **`enemy`** rows per other player in ascending `player_index`, categories sorted within each bucket.
* **Action mask families:** fixed order `ACTION_MASK_FAMILY_NAMES` in the catalog.
* **Spatial planes:** single prototype plane in M18 (structural metadata only).

## What is populated vs prototype (M18)

| Area | M18 posture |
| ---- | ----------- |
| Metadata / provenance | `gameloop`, `perspective_player_index`, `source_canonical_state_sha256` (required); optional `source_bundle_id`, `source_lineage_root`, `source_replay_identity` when present on canonical state |
| Viewpoint | `proxy_bounded` visibility policy; single-player-relative flag |
| Scalar features | Derived from M16-supportable fields; missing visibility proxy uses `null` with a **warning** |
| Entity rows | **`aggregated_category` only**; counts from M16 `army_unit_category_counts` |
| Spatial plane family | **Structural** grid/channel metadata aligned to the M17 example style; **not** map-grounded terrain/control inference |
| Action mask families | **Coarse prototype** `0`/`1` masks from bounded M16 signals — **not** legality |

## Explicit non-claims

M18 does **not** prove:

* Replay bundle loading or replay parsing inside `starlab/observation/`
* Multi-frame batches, tensors, or training datasets
* Action legality, completeness, or dynamic mask generation
* Exact banked minerals/gas or certified fog-of-war truth
* Replay↔execution equivalence or benchmark integrity

## Validation failure conditions

* Invalid JSON, missing players, or unknown `perspective_player_index`
* Optional report present but `canonical_state_sha256` mismatch
* Emitted observation fails M17 `jsonschema` validation

## CLI

```text
python -m starlab.observation.emit_observation_surface \
  --canonical-state PATH \
  --perspective-player-index N \
  --output-dir OUT \
  [--canonical-state-report PATH]
```

## Related documents

* `docs/runtime/observation_surface_contract_v1.md` (M17 contract shape)
* `docs/runtime/canonical_state_pipeline_v1.md` (M16 upstream)
