# Replay timeline & event extraction (M10)

**Contract:** `starlab.replay_timeline_contract.v1`  
**Profile:** `starlab.replay_timeline.m10.v1`  
**Artifacts:** `replay_timeline.json`, `replay_timeline_report.json`

## Purpose

M10 defines STARLAB’s first **governed event plane**: a deterministic, comparable **timeline** derived from parser-owned event streams (`raw_event_streams` on `replay_raw_parse.json` for schema `starlab.replay_raw_parse.v2`), without claiming build-order/economy (M11), combat/scouting semantics, broad parser correctness, or replay↔execution equivalence.

## Non-claims

- **Not** build-order or economy structure (M11).
- **Not** combat outcomes, scouting, or visibility windows (later milestones).
- **Not** proof of full Blizzard event coverage or semantic correctness of upstream decoders.
- **Not** proof of exact **intra-gameloop** causal order across streams. The merge policy below is a **canonical deterministic ordering** for artifacts only.
- **Not** exposure of player display names, raw chat bodies, or other unnecessary free-form text in public timeline payloads.

## Upstream inputs

| Input | Role |
| ----- | ---- |
| `replay_raw_parse.json` | Required. Schema `starlab.replay_raw_parse.v1` or `starlab.replay_raw_parse.v2`. |
| `raw_event_streams` | Optional (v2). M10-owned lowering: decoded `game_events`, `message_events`, `tracker_events` lists (or `null` per stream). Sub-schema `starlab.raw_event_streams.v1`. |
| `replay_parse_receipt.json` / `replay_parse_report.json` | Optional lineage; SHA linkage checks when paths are provided. |
| `replay_metadata.json` / `replay_metadata_report.json` | Optional lineage; SHA linkage checks when paths are provided. |

M08’s historical proof remains: **raw parse blocks + event-stream availability flags**. M10 adds the **lowered event stream bodies** behind the same parser boundary; semantic interpretation is M10 extraction only.

## Glossary

| Term | Meaning |
| ---- | ------- |
| **Raw parse blocks** | M08 `raw_sections` (header, details, init_data, attribute_events). |
| **Raw event streams** | M10-owned decoded lists under `raw_event_streams` (parser lowering, not public semantics). |
| **Normalized metadata** | M09 `replay_metadata.json` (no event bodies). |
| **Normalized timeline entry** | One row in `entries[]` after merge + semantic mapping + privacy scrub. |
| **Event semantic** | The `semantic_kind` field — a small STARLAB enum mapped from Blizzard `_event` typenames. |
| **Strategic derivation** | Build order, economy, combat analysis — **M11+**, not M10. |

## Semantic kinds (M10 profile)

| `semantic_kind` | Typical source (`_event`) |
| ----------------- | ------------------------- |
| `command_issued` | `NNet.Game.SCmdEvent` |
| `unit_init` | `NNet.Replay.Tracker.SUnitInitEvent` |
| `unit_born` | `NNet.Replay.Tracker.SUnitBornEvent` |
| `unit_died` | `NNet.Replay.Tracker.SUnitDiedEvent` |
| `unit_owner_changed` | `NNet.Replay.Tracker.SUnitOwnerChangeEvent` |
| `unit_type_changed` | `NNet.Replay.Tracker.SUnitTypeChangeEvent` |
| `upgrade_completed` | `NNet.Replay.Tracker.SUpgradeEvent` |
| `message_event` | `NNet.Game.SChatMessage` (metadata only; no raw chat text) |
| `ping_event` | `NNet.Game.SPingMessage` |

Unknown `_event` typenames are **not** mapped to semantics; they are listed in `unsupported_event_names` on the report.

## Merge / ordering policy

**`merge_order_policy`** (also embedded in `replay_timeline.json`):

1. Sort by **`gameloop`** ascending.
2. Then by **`source_stream_precedence`**: `game`, `message`, `tracker`.
3. Then by **`source_event_index`** ascending within the stream.

This is a **canonical merge order for artifact determinism**; it does **not** prove exact cross-stream causality within a single gameloop.

## Privacy

- Do **not** emit player display names, clan tags, toon handles, or raw chat strings.
- For chat-like events, emit **`m_string_length`** (or equivalent bounded metadata) instead of message body text.

## `replay_timeline.json` (summary)

- `timeline_contract_version`, `timeline_profile`, `schema_version`
- `replay_content_sha256`, `source_raw_parse_sha256`
- Optional lineage: `source_parse_receipt_sha256`, `source_parse_report_sha256`, `source_metadata_sha256`, `source_metadata_report_sha256`
- `event_streams_available` (copy from raw parse)
- `merge_order_policy`
- `entries[]`: `timeline_index`, `source_stream`, `source_event_index`, `source_event_name`, `gameloop`, `semantic_kind`, optional `player_index`, optional `unit_tag`, `payload`

## `replay_timeline_report.json` (summary)

- `timeline_contract_version`, `timeline_profile`, `schema_version`
- `extraction_status`: `ok` | `partial` | `failed`
- `counts_by_stream`, `counts_by_semantic_kind`
- `unsupported_event_names`, `warnings`
- `check_results` (ordered IDs per `TIMELINE_CHECK_IDS`)

## CLI

```bash
python -m starlab.replays.extract_replay_timeline --raw-parse replay_raw_parse.json --output-dir ./out \
  [--parse-receipt replay_parse_receipt.json] [--parse-report replay_parse_report.json] \
  [--metadata replay_metadata.json] [--metadata-report replay_metadata_report.json]
```

Exit codes: `0` success (including partial extraction), `4` extraction failure, `5` source contract / linkage failure.
