# Replay build-order & economy extraction (M11)

**Contract:** `starlab.replay_build_order_economy_contract.v1`  
**Profile:** `starlab.replay_build_order_economy.m11.v1`  
**Artifacts:** `replay_build_order_economy.json`, `replay_build_order_economy_report.json`

## Purpose

M11 defines STARLAB’s first governed **build-order and economy plane**: deterministic **build-order steps** and **economy checkpoints** derived from **M10** `replay_timeline.json`, with optional **supplemental** identity from **M08/M10** `replay_raw_parse.json` v2 `raw_event_streams` — **without** claiming combat/scouting (M12), exact resource reconstruction, replay↔execution equivalence, benchmark integrity, or broad upstream parser correctness.

## Non-claims

- **Not** combat, scouting, or visibility windows (M12).
- **Not** exact minerals / gas / larva / energy accounting or full macro simulation.
- **Not** proof that merged timeline order matches true intra-gameloop causality (M10 documents this).
- **Not** legal certification of third-party replay rights.
- **Not** live SC2 execution in CI (fixture-driven default).

## Upstream inputs

### Required (primary governed event plane)

| Input | Role |
| ----- | ---- |
| `replay_timeline.json` | **Required.** M10 public timeline: ordered `entries[]` with `semantic_kind`, `timeline_index`, `source_stream`, `source_event_index`, `gameloop`, optional `player_index`, optional `unit_tag`, `payload`. |

### Optional (lineage / reporting context)

| Input | Role |
| ----- | ---- |
| `replay_timeline_report.json` | Optional SHA linkage and extraction context from M10. |
| `replay_metadata.json` | Optional lineage (hashes copied into M11 artifacts when present). |
| `replay_metadata_report.json` | Optional lineage. |

### Optional (supplemental identity only)

| Input | Role |
| ----- | ---- |
| `replay_raw_parse.json` | Optional **v2** parse with `raw_event_streams`. Used **only** to read non-PII identity fields (e.g. `m_unitTypeName`, `m_upgradeTypeName`) aligned to timeline rows by `(source_stream, source_event_index)`. **Does not** replace the timeline as the event plane. |

**Guardrail:** M11 **must not** import `s2protocol`, invoke the replay parser CLI, or read raw `.SC2Replay` bytes. Only STARLAB-owned JSON artifacts listed here.

### Privacy and M10 scrub (why supplemental raw parse exists)

M10 intentionally **scrubs** free-form strings from public timeline `payload` objects. Build-order classification therefore **cannot** rely on public timeline strings for Blizzard entity names. Supplemental **`replay_raw_parse.json` v2** `raw_event_streams` recover those names **only** for classification, keyed to the same logical events as the timeline.

## Ordering authority (locked)

When both `replay_timeline.json` and supplemental `raw_event_streams` are used:

1. **Timeline ordering wins.** All build-order steps and checkpoints follow **`timeline_index`** (and thus M10’s merge policy already reflected in the timeline file).
2. **Raw event streams are identity-only.** M11 looks up the raw event at `(source_stream, source_event_index)` to read entity/upgrade names. It **must not** reorder, insert, or drop timeline entries based on raw-stream order.

If a lookup key is missing or ambiguous, M11 reports **warnings** and treats identity as unknown rather than guessing.

## Classification taxonomy (M11 profile)

Conservative categories (see implementation catalog):

| `category` | Meaning (M11) |
| ---------- | ---------------- |
| `worker` | Worker units (e.g. SCV, Probe, Drone). |
| `townhall` | Command / Nexus / Hatchery-tier production halls. |
| `gas_structure` | Refinery / Assimilator / Extractor. |
| `supply_provider` | Supply structures / overlord-class supply where catalogued. |
| `production_structure` | Production buildings (Barracks, Gateway, Spawning Pool, …). |
| `tech_structure` | Non-production tech structures (Engineering Bay, Forge, Evolution Chamber, …). |
| `economy_upgrade` | Explicitly catalogued economy-relevant upgrades (narrow). |
| `tech_upgrade` | Explicitly catalogued non-economy upgrades (narrow). |
| `combat_or_other` | Combat units or other entities explicitly listed as such in the catalog. |
| `unknown` | Not in the catalog or not safely classifiable. |

**Rule:** Unknown names are **reported**, not silently mapped.

## Semantic mapping (M11 profile)

From M10 `semantic_kind`:

| `semantic_kind` | Build-order step? |
| ---------------- | ----------------- |
| `unit_init` | Yes for catalogued **structures** — `phase = started`. |
| `unit_born` | Yes for catalogued units/structures — `phase = completed`. |
| `upgrade_completed` | Yes for catalogued upgrades — `phase = completed`. |
| `unit_type_changed` | Only if a **curated morph rule** matches — `entity_kind = morph`, `phase = completed`. |
| `command_issued`, `message_event`, `ping_event`, `unit_owner_changed`, `unit_died`, … | **No** (listed in report as ignored kinds). |

## Economy checkpoint semantics

Checkpoints are **cumulative completed counts** per `player_index`, emitted when a build-order step changes any of:

- workers completed  
- townhalls completed  
- gas structures completed  
- supply providers completed  
- production structures completed  
- tech structures completed  
- economy upgrades completed  

This is **not** a full simulation of banked resources.

## `replay_build_order_economy.json` (summary)

- `build_order_economy_contract_version`, `build_order_economy_profile`, `schema_version`
- `source_timeline_sha256`
- Optional lineage: `source_timeline_report_sha256`, `source_metadata_sha256`, `source_metadata_report_sha256`, `source_raw_parse_sha256` (when supplemental raw parse was used for identity; should match M10 timeline linkage when present)
- `ordering_policy` (string; timeline authority rule)
- `classification_profile` (catalog / morph profile identifiers)
- `players` (minimal player indices observed)
- `build_order_steps[]`: `step_index`, `player_index`, `gameloop`, `source_timeline_index`, `entity_name`, `entity_kind`, `phase`, `category`, optional `unit_tag`
- `economy_checkpoints[]`: `checkpoint_index`, `player_index`, `gameloop`, `source_step_index`, cumulative counters

## `replay_build_order_economy_report.json` (summary)

- `build_order_economy_contract_version`, `build_order_economy_profile`, `schema_version`
- `extraction_status`: `ok` | `partial` | `failed`
- Counts by category / phase / player (deterministic)
- `unclassified_unit_names`, `unclassified_upgrade_names` (sorted)
- `ignored_timeline_semantic_kinds` (sorted)
- `warnings`
- `check_results` (ordered check IDs)

## CLI

```bash
python -m starlab.replays.extract_replay_build_order_economy \
  --timeline replay_timeline.json --output-dir ./out \
  [--raw-parse replay_raw_parse.json] \
  [--timeline-report replay_timeline_report.json] \
  [--metadata replay_metadata.json] [--metadata-report replay_metadata_report.json]
```

Exit codes: `0` success (including partial extraction where applicable), `4` extraction failure, `5` source contract / linkage failure.
