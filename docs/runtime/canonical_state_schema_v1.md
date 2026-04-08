# Canonical State Schema v1 (M15)

## Purpose

Define a **deterministic, machine-readable JSON Schema** for a single **replay-native state frame** at one `gameloop`, bounded to replay planes already proved in **M09–M14**. M15 proves **schema emission + validation over fixtures** only — **not** replay-to-state extraction (M16), observation semantics (M17), or perceptual bridge behavior (M18).

## Glossary

| Term | Meaning |
| ---- | ------- |
| **Canonical state frame** | One JSON object describing derived state at a single `gameloop`, conforming to `canonical_state_schema.json`. |
| **Schema fingerprint** | SHA-256 (hex) of the canonical JSON serialization of `canonical_state_schema.json`, recorded in `canonical_state_schema_report.json`. |
| **Replay plane** | A governed artifact family (metadata, timeline, build-order/economy, combat/scouting/visibility, slices, bundle/lineage). |
| **Proxy visibility** | Replay-derived visibility signals that are **not** certified fog-of-war truth (M12 non-claim). |

## Schema scope

- **In scope:** One state frame; conservative, replay-derived fields; omission / nullability rules; provenance flags for which planes inform the document.
- **Out of scope:** Sequences, tensors, observation APIs, extraction from replay bundles, `s2protocol`, raw replay bytes, benchmark scorecards, live SC2 in CI.

## State frame definition

A **state frame** is a JSON object with:

- `schema_version` — document format id (`starlab.canonical_state_frame.v1`).
- `frame_kind` — e.g. `replay_snapshot` or `replay_derived`.
- `source` — optional linkage to M14 bundle identity / lineage / replay identity when available.
- `gameloop` — non-negative integer.
- `players` — non-empty array of per-player summaries (see below).
- `global_context` — map-level context (e.g. map name, active slice IDs).
- `provenance` — booleans indicating which replay planes contributed.

## Required vs optional sections

**Required top-level:** `schema_version`, `frame_kind`, `source`, `gameloop`, `players`, `global_context`, `provenance`.

**Per player (required):** `player_index`, `race_actual`, `economy_summary`, `production_summary`, `army_summary`.

**Per player (optional):** `result`, `combat_context`, `scouting_context`, `visibility_context`.

**Source (optional keys):** `source_bundle_id`, `source_lineage_root`, `source_replay_identity`.

**Global context (optional keys):** `map_name`, `active_slice_ids`, `active_combat_window_ids`.

**Provenance (required keys):** all of `uses_metadata_plane`, `uses_timeline_plane`, `uses_build_order_economy_plane`, `uses_combat_scouting_visibility_plane`, `uses_slice_plane`, `uses_replay_bundle_plane`.

## Omission / nullability rules

1. **Omit** optional fields when not derivable from governed replay JSON (M09–M14).
2. Use JSON **`null`** only when a field is applicable but intentionally unresolved — **no guessed defaults**.
3. **Economy:** prefer **counts / categories** over exact mineral/gas bank values (M11 did not prove exact resource reconstruction).
4. **Visibility:** any visibility-related field remains a **non-truth-bearing proxy** (M12 non-claim).
5. **No PII:** no player display names, chat, or similar in the public contract.

## Provenance expectations

`provenance` records **which planes** inform the frame. It does **not** certify parser correctness, legal replay rights, or execution equivalence.

## Deterministic schema emission

- **Contract:** `starlab.canonical_state_schema.v1`
- **Profile:** `starlab.canonical_state_schema.m15.v1`
- Emitted files: `canonical_state_schema.json`, `canonical_state_schema_report.json`.
- JSON is written with **sorted keys**, stable separators, and UTF-8 (see `starlab.runs.json_util.canonical_json_dumps`).
- The report’s `schema_sha256` matches `sha256_hex_of_canonical_json` of the schema object (canonical JSON **without** trailing newline, per existing STARLAB hashing rules).

## Explicit non-claims

M15 proves deterministic canonical state schema v1 and validation over fixture examples. M15 does **not** prove replay-to-state extraction, observation semantics, perceptual bridge behavior, replay↔execution equivalence, benchmark integrity, or live SC2 in CI.

## CLI usage

```text
python -m starlab.state.emit_canonical_state_schema --output-dir DIR
```

Optional example hashes in the report:

```text
python -m starlab.state.emit_canonical_state_schema --output-dir DIR ^
  --example-fixture valid=tests/fixtures/m15/valid_canonical_state_example.json
```

No replay input is required for M15.

## Primary code references

- `starlab/state/canonical_state_schema.py` — JSON Schema builder + subset validator
- `starlab/state/canonical_state_io.py` — report builder, file validation, artifact write
- `starlab/state/emit_canonical_state_schema.py` — CLI
