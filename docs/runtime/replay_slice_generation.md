# Replay slice generation (M13)

## Purpose

M13 defines a **deterministic, governed replay slice-definition plane** that derives **addressable temporal spans** from existing governed replay JSON artifacts (`replay_timeline.json`, `replay_build_order_economy.json`, `replay_combat_scouting_visibility.json`) and emits **`replay_slices.json`** and **`replay_slices_report.json`**.

A **slice** in M13 is a **metadata-defined temporal span** over governed artifacts. M13 does **not** clip raw `.SC2Replay` bytes, produce sub-replay files, videos, tensors, or M14-style bundles.

## Glossary

| Term | Meaning |
| ---- | ------- |
| **Slice** | Metadata-defined `[start_gameloop, end_gameloop]` window anchored to an M12 combat window or scouting observation. |
| **Slice family** | `combat_window` or `scouting_observation` (v1 only). |
| **Overlap (M11)** | Build-order step whose `gameloop` falls inside the slice window (inclusive). |
| **Overlap (M12 visibility)** | Context only: visibility window intervals that intersect the slice window. Does **not** upgrade `observation_proxy` to fog-of-war truth. |

## Required inputs

| Artifact | Milestone |
| -------- | --------- |
| `replay_timeline.json` | M10 |
| `replay_build_order_economy.json` | M11 |
| `replay_combat_scouting_visibility.json` | M12 |

## Optional inputs (lineage / enrichment only)

- `replay_timeline_report.json`
- `replay_build_order_economy_report.json`
- `replay_combat_scouting_visibility_report.json`
- `replay_metadata.json` / `replay_metadata_report.json`

Optional metadata may be used for a **conservative** check: if `replay_metadata.json` exposes `metadata.game.game_length_loops`, generation fails when the timeline-derived maximum gameloop exceeds that value.

## Ordering authority

M10 **timeline ordering** remains authoritative. M13 does not read `replay_raw_parse.json` in v1.

## Slice families (v1)

- `combat_window` — one slice per M12 combat window.
- `scouting_observation` — one slice per M12 scouting observation.

There is **no** separate `visibility_window` slice family in M13 v1; visibility contributes **overlap/context** only.

## Padding rules

- `SLICE_PADDING_PRE_LOOPS = 160`
- `SLICE_PADDING_POST_LOOPS = 160`

**Combat:** `start = max(0, combat_window.start_gameloop - 160)`, `end = min(replay_max, combat_window.end_gameloop + 160)`.

**Scouting:** anchor = observation `gameloop` (first-seen); `start = max(0, anchor - 160)`, `end = min(replay_max, anchor + 160)`.

`replay_max_gameloop` is the maximum `gameloop` across M10 timeline `entries`.

## Anchor policy

- **Combat:** `anchor_gameloop` is the **start** of the M12 combat window (not midpoint).
- **Scouting:** `anchor_gameloop` is the observation `gameloop`.

## Lineage rules

Before emitting slices:

1. Canonical-hash the three required upstream JSON objects (`sha256` of deterministic JSON bytes per `starlab.runs.json_util`).
2. Require `replay_build_order_economy.source_timeline_sha256` to match the canonical timeline hash.
3. Require `replay_combat_scouting_visibility.source_timeline_sha256` and `source_build_order_economy_sha256` to match canonical hashes.
4. If upstream embeds non-null `source_*_report_sha256` fields, the corresponding optional report file must be provided and hash-match.

## Determinism and `slice_id`

- Slices are sorted by `(start_gameloop, end_gameloop, slice_kind, sort key)` where the sort key is `cw-{window_index}` or `so-{observation_index}`.
- **`slice_id`** is `sha256` of **canonical JSON** over **stable semantic fields** only: `slice_kind`, span, `anchor_gameloop`, `anchor_ref`, optional player indices, optional `evidence_model` (scouting). It **must not** include:

  - `overlapping_build_order_step_ids`
  - `overlapping_visibility_window_ids`
  - Overlap-derived **tags** (e.g. `proxy_visibility_overlap`)

  This ensures harmless report enrichment or overlap-summary tweaks do not churn IDs.

Tags on the slice record may still include overlap-derived labels for **human/audit context**; they are not part of `slice_id`.

## Explicit non-claims

M13 does **not** prove raw replay clipping, benchmark integrity, replay↔execution equivalence, fog-of-war truth, full simulation, live SC2 in CI, or M14 bundle packaging.

## CLI usage

```text
python -m starlab.replays.extract_replay_slices \
  --timeline PATH \
  --build-order-economy PATH \
  --combat-scouting-visibility PATH \
  --output-dir DIR \
  [--timeline-report PATH] \
  [--build-order-economy-report PATH] \
  [--combat-scouting-visibility-report PATH] \
  [--metadata PATH] \
  [--metadata-report PATH]
```

Exit codes: `0` success; `4` extraction/load failure; `5` contract or lineage failure.
