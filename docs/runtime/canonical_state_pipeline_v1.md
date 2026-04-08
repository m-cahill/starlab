# Canonical State Pipeline v1 (M16)

## Purpose

Define the **governed product contract** for materializing **exactly one** M15-shaped **canonical state frame** at one requested `gameloop` from a **complete M14 replay bundle** (governed JSON only). M16 proves **deterministic pipeline materialization + validation + report emission** — **not** an observation API (M17), perceptual bridge (M18), replay↔execution equivalence, benchmark integrity, or live SC2 in CI.

## Glossary

| Term | Meaning |
| ---- | ------- |
| **M14 replay bundle** | Directory (or equivalent layout) containing `replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json`, and the primary M09–M13 artifacts listed below, plus optional secondary `*_report.json` members referenced by the manifest hash inventory. |
| **Canonical state frame materialization** | Emitting `canonical_state.json` that validates against M15 `canonical_state_schema.json` for one `gameloop`. Distinct from any **observation surface contract** (M17), which defines agent-facing views and masks. |
| **replay_length_loops** | `max(metadata.game.game_length_loops, max timeline entry gameloop)` when both are available; used only for **range validation** of `--gameloop`. A warning is recorded if the two sources differ. |

## Required inputs

### Bundle packaging (M14)

* `replay_bundle_manifest.json`
* `replay_bundle_lineage.json`
* `replay_bundle_contents.json`

### Primary governed replay artifacts (M09–M13)

* `replay_metadata.json`
* `replay_timeline.json`
* `replay_build_order_economy.json`
* `replay_combat_scouting_visibility.json`
* `replay_slices.json`

### Secondary reports

Optional files may appear in `artifact_hashes` (e.g. `replay_metadata_report.json`, `replay_slices_report.json`). They participate in **hash verification** and **lineage checks** when present.

## Hard exclusions

* **No** raw `.SC2Replay` bytes.
* **No** `replay_raw_parse.json`.
* **No** `s2protocol` or other parser imports in M16 modules.
* **No** loading primary artifacts from paths **outside** the bundle directory layout enforced by the manifest hash inventory (product code must not bypass the bundle contract).

## Integrity and precedence

1. **M14 manifest / lineage / contents** — packaging identity; `bundle_id` and `lineage_root` must be mutually consistent across the three files.
2. **Per-file hashes** — every entry in `manifest.artifact_hashes` must match `sha256_hex_of_canonical_json` of the loaded JSON object.
3. **Replay-plane lineage** — `verify_replay_plane_lineage` must succeed for the loaded primary objects and optional reports (same rules as M14 bundle generation).
4. **Recomputed roots** — `lineage_root` and `bundle_id` must match recomputation from primary hashes + `generation_parameters` (same algorithms as M14).

Source precedence for **field derivation** (when multiple planes apply):

1. M14 bundle identity fields (bundle id, lineage root, replay identity hash).
2. M09 metadata — map name, player roster, race, result.
3. M10 timeline — temporal upper bound and event ordering context (not re-parsed here).
4. M11 build-order / economy — train counts, structure counts, checkpoint hints, queue heuristics.
5. M12 combat / scouting / visibility — combat window IDs, scouting observation counts, visibility proxy level.
6. M13 slices — **membership only** (`slice_id` active for the target loop); slices do not reconstruct hidden game state.

## Target `gameloop` policy

* Integer **≥ 0**.
* Must satisfy `gameloop <= replay_length_loops`.
* **Hard fail** if out of range or negative.

## Emitted artifacts

| File | Role |
| ---- | ---- |
| `canonical_state.json` | One state frame; validates against M15 JSON Schema (`build_canonical_state_json_schema`). |
| `canonical_state_report.json` | Deterministic provenance: schema hash, state hash, source artifact hashes, warnings, non-claims. |

Serialization uses `canonical_json_dumps` (sorted keys, stable UTF-8).

## Explicit non-claims

M16 does **not** prove:

* observation tensors, batched sequences, or action masks;
* perceptual bridge behavior;
* replay↔execution equivalence;
* benchmark integrity;
* exact banked minerals/gas;
* certified fog-of-war truth.

## CLI

```text
python -m starlab.state.emit_canonical_state --bundle-dir DIR --gameloop N --output-dir OUT
```

Exactly **one** frame per invocation; non-zero exit on load, lineage, range, or validation failure.
