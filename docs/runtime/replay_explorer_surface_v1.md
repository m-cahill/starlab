# Replay explorer / operator evidence surface (v1)

## Purpose

**M31** defines an offline, deterministic **replay explorer evidence surface**: JSON artifacts that let an operator inspect a **frozen M30** hierarchical imitation agent in **replay slice** context, without live SC2, without a web UI, and without claiming benchmark integrity.

## Artifact filenames

| Artifact | Description |
| -------- | ----------- |
| `replay_explorer_surface.json` | Primary evidence surface |
| `replay_explorer_surface_report.json` | Summary counts and policy |

## Identity fields

| Field | Value |
| ----- | ----- |
| `surface_version` | `starlab.replay_explorer_surface.v1` |
| `selection_policy_id` | `starlab.m31.selection.slice_anchor_v1` |
| `report_version` (report only) | `starlab.replay_explorer_surface_report.v1` |

## Inputs

1. **M14 bundle directory** (`--bundle-dir`): must contain governed primary artifacts per M14 (e.g. `replay_bundle_manifest.json`, `replay_metadata.json`, `replay_timeline.json`, `replay_build_order_economy.json`, `replay_combat_scouting_visibility.json`, `replay_slices.json`).
2. **M30 agent** (`--agent-path`): `replay_hierarchical_imitation_agent.json` body compatible with `FrozenHierarchicalImitationPredictor.from_agent_body`.
3. **Materialization:** one **M16 → M18** pass per panel anchor via `materialize_observation_for_observation_request` (bundle id / lineage / gameloop / `perspective_player_index` = slice `subject_player_index`).

## Selection policy (`slice_anchor_v1`)

1. Load `replay_slices.json` from the bundle directory.
2. Optional: if `--slice-id` is set, keep only that slice (must exist).
3. Sort remaining slices by `(start_gameloop ascending, slice_id ascending)`.
4. Take the first `--max-panels` slices (default **5**).
5. For each slice:  
   `anchor_gameloop = (start_gameloop + end_gameloop) // 2`  
   (integer midpoint; must lie in `[start_gameloop, end_gameloop]` for non-empty spans).

## Bounded excerpt policy (fixed)

All excerpts are **within the slice window** `[start_gameloop, end_gameloop]` unless noted.

| Surface | Max items | Distance rule | Output order |
| ------- | --------- | ------------- | ------------ |
| Timeline (M10) | **8** | Among entries with `gameloop` in the slice window, minimize `\|gameloop - anchor_gameloop\|`; ties: `timeline_index` ascending | `gameloop` ascending, then `timeline_index` |
| Economy (M11) | **6** | Among `build_order_steps` with `gameloop` in the slice window, minimize `\|gameloop - anchor_gameloop\|`; ties: `step_index` | `gameloop` ascending, then `step_index` |
| Combat / scouting (M12) | **6** | Union of (a) scouting observations with `gameloop` in the slice window and `subject_player_index == slice.subject_player_index`, and (b) combat windows whose `[start_gameloop, end_gameloop]` intersects the slice window. Distance: for scouting, `\|g - anchor\|`; for combat windows, **0** if `anchor_gameloop` lies inside the window, else distance from `anchor_gameloop` to the nearest window endpoint. Ties: scouting before combat; then `observation_index` or `window_index` | Deterministic sort by `(distance, kind, id)` then cap **6** |
| Canonical state (M16) | **1 frame** | Full materialization at anchor; excerpt is a **bounded projection** (see below) | N/A |
| Observation (M18) | **1 frame** | Same anchor; excerpt is a **bounded projection** | N/A |

**Canonical state excerpt projection:** include `frame_kind`, `gameloop`, `global_context.map_name` (if present), and per `players[]` only: `player_index`, `race_actual`, `economy_summary` (object as-is if present), `army_summary.army_unit_category_counts` (if present).

**Observation excerpt projection:** include `metadata`, and `scalar_features.ordered_entries` truncated to the **first 12** entries (array order preserved).

## Hierarchical trace

Each panel includes one **M29**-compatible trace document from the M30 predictor (`build_trace_document_for_signature`) using **M27** `build_context_signature` over the anchor observation + canonical state.

## Source hashes

Panels and the top-level surface reference upstream identity via manifest / artifact hashes (e.g. `replay_bundle_manifest.json` `artifact_hashes`, `source_replay_identity` or `replay_content_sha256` from governed JSON where defined). Do not embed full upstream files in the surface.

## Explicit non-claims

The surface and report MUST include stable `non_claims` text consistent with:

- Not benchmark integrity or leaderboard validity  
- Not live SC2 or replay↔execution equivalence  
- Not raw SC2 action legality  
- Not full replay coverage (bounded panels only)  
- Not M32 flagship proof-pack semantics  
- Not hosted deployment readiness  

## CLI

`python -m starlab.explorer.emit_replay_explorer_surface`

| Flag | Meaning |
| ---- | ------- |
| `--bundle-dir` | M14 bundle directory (required) |
| `--agent-path` | Path to `replay_hierarchical_imitation_agent.json` (required) |
| `--output-dir` | Directory for both JSON artifacts (required) |
| `--max-panels` | Max panels (default **5**) |
| `--slice-id` | Optional: single slice id |

Exit **0** on success; non-zero on validation or IO errors.
