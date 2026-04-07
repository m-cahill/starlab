# Replay combat, scouting, and visibility extraction (M12)

**Contract:** `starlab.replay_combat_scouting_visibility_contract.v1`  
**Profile:** `starlab.replay_combat_scouting_visibility.m12.v1`  
**Artifacts:** `replay_combat_scouting_visibility.json`, `replay_combat_scouting_visibility_report.json`

## Purpose

M12 defines STARLAB’s first governed **combat / scouting / visibility** plane as **pure extraction** over governed upstream JSON:

- **Required:** `replay_timeline.json` (M10) and `replay_build_order_economy.json` (M11).
- **Optional:** lineage artifacts, metadata, and `replay_raw_parse.json` v2 for supplemental identity, position, and (only when clearly present) visibility-related fields.

M12 **does not** import `s2protocol`, invoke parser CLIs, or read raw `.SC2Replay` bytes.

## Glossary

| Term | Meaning |
| ---- | ------- |
| **Combat window** | A contiguous cluster of `unit_died` timeline rows (sorted by `timeline_index`), where the gameloop gap between consecutive deaths in the cluster does not exceed **`combat_window_gap_loops`** (fixed **160** gameloops in this profile). Not a full battle simulator. |
| **Scouting observation** | A deterministic **first-seen** signal for a governed category (e.g. first townhall, first gas structure, first army-line unit) for a **subject** `player_index`, emitted in timeline order. |
| **Explicit visibility** | Visibility state or transitions **directly** supported by governed upstream fields. M12 uses this label **only** when such fields are unambiguous; otherwise emit **no** explicit-visibility window. |
| **Observation proxy** | A conservative **presence interval** derived from repeated timeline mentions of a `unit_tag` (first to last gameloop). **Not** true fog-of-war truth and **not** implied when `observer_player_index` is absent. |

### Observation proxy guardrail (non-claims)

If a visibility window is emitted from timeline presence (including repeated observations) but **lacks** direct observer identity from governed artifacts, the window remains labeled **`observation_proxy`** and **must not** be read as certified fog-of-war state. Proxies describe **replay-visible presence intervals** under M12 rules, not player mental models or omniscient game truth.

## Non-claims

- **Not** benchmark integrity, replay↔execution equivalence, or exact damage modeling.
- **Not** tactical strength scoring, build-order judgment, or strategy labels (“all-in”, “timing attack”, …).
- **Not** full fog-of-war reconstruction; **`observation_proxy`** is not omniscient visibility.
- **Not** legal certification of third-party replay rights.
- **Not** live SC2 execution in CI (fixture-driven default).

## Upstream inputs

### Required

| Input | Role |
| ----- | ---- |
| `replay_timeline.json` | **Primary event order.** `entries[]` with `semantic_kind`, `timeline_index`, `gameloop`, optional `player_index`, optional `unit_tag`, `source_stream`, `source_event_index`. |
| `replay_build_order_economy.json` | **Governed macro plane** from M11: `build_order_steps` and lineage hashes; consumed **as JSON** (do not re-derive full macro classification from scratch when M11 already emitted it). |

### Optional (lineage / reporting)

| Input | Role |
| ----- | ---- |
| `replay_timeline_report.json` | Optional SHA linkage from M10. |
| `replay_build_order_economy_report.json` | Optional SHA linkage from M11. |
| `replay_metadata.json` / `replay_metadata_report.json` | Optional lineage hashes. |

### Optional (supplemental only)

| Input | Role |
| ----- | ---- |
| `replay_raw_parse.json` v2 | `raw_event_streams` for **non-PII** identity (`m_unitTypeName`, …), **optional** `m_x`/`m_y` for centroids, and fields that **directly** encode visibility when clearly present. **Does not** replace timeline ordering. |

## Ordering authority

1. **Timeline ordering wins** (`timeline_index` / M10 merge policy already reflected in the file).
2. **M11** supplies governed macro context and per-step categories where applicable.
3. **Raw parse** is supplemental for identity, position, and explicit visibility fields only — **never** for reordering events.

Integrity check: `replay_build_order_economy.source_timeline_sha256` **must** match the canonical SHA-256 of the `replay_timeline.json` object used for extraction.

## Combat window model

- **Anchor:** `unit_died` entries only (victim `player_index` from timeline entry / payload).
- **Clustering:** sort deaths by `timeline_index`; start a new window when `current.gameloop - previous.gameloop > combat_window_gap_loops` (**160** fixed for `starlab.replay_combat_scouting_visibility.m12.v1`).
- **Fields:** per-window death counts, `players_involved`, `deaths_by_player`, `losses_by_role` (M12 catalog roles), optional `location_centroid` when raw events provide `m_x`/`m_y` for deaths; otherwise `location_model: "omitted"`.

## Scouting observation model

- **First-seen** signals include: `enemy_townhall_first_seen`, `enemy_expansion_first_seen` (second distinct townhall **unit_tag** per subject when tags exist; else event-count fallback), `enemy_gas_first_seen`, `enemy_production_first_seen`, `enemy_tech_first_seen`, `enemy_army_first_seen` (one bucket per subject for **army** / **scout** / **detector** first appearance — first qualifying unit wins).
- **`observer_player_index`:** omitted unless directly supportable from governed artifacts (M12 does **not** infer observer from ladder slot or 1v1 layout).
- **`evidence_model`:** `timeline_plus_raw` | `timeline_plus_macro` | `timeline_only` (see implementation).

## Visibility window model

- **Default in M12:** `observation_proxy` for `unit_tag`-keyed presence intervals from `unit_born`, `unit_init`, `unit_died`, `unit_type_changed` rows that carry the same tag.
- **`explicit_visibility`:** emit **only** when a governed upstream field clearly supports it; otherwise omit or use proxy.
- **`subject_player_index`:** omitted if no player can be resolved without guessing.

## Classification (M12 catalog)

Separate governed catalog `starlab.combat_scouting_visibility_catalog.m12.v1` (M12-owned). Reuses M11 macro mappings where appropriate; adds narrow **scout** / **detector** / **army** roles. Unknown entity names are **reported**, not silently dropped.

## Determinism

Fixed `combat_window_gap_loops`, deterministic sorts, stable JSON via `canonical_json_dumps` for file emission.

## CLI

`python -m starlab.replays.extract_replay_combat_scouting_visibility` — see `--help`.
