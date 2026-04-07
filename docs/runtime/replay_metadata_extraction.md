# Replay — Metadata Extraction (M09)

**Status:** Governed contract (M09)  
**Metadata contract version:** `metadata_contract_version` `starlab.replay_metadata_contract.v1`  
**Metadata profile:** `metadata_profile` `starlab.replay_metadata_profile.v1`  
**Scope:** Deterministic lowering of **M08** `replay_raw_parse.json` into a **small, stable, public** JSON metadata surface. **No** event/timeline semantics (M10), **no** build-order / economy (M11).

---

## 1. Purpose

This document defines the **M09** replay metadata extraction contract:

- **Inputs:** governed M08 artifacts (`replay_raw_parse.json`, optional `replay_parse_receipt.json`, `replay_parse_report.json`).
- **Outputs:** `replay_metadata.json` and `replay_metadata_report.json`.
- **Boundary:** extraction is **pure** over normalized M08 JSON — **no** replay bytes, **no** `s2protocol` imports, **no** inference from event streams.

**M09 does not prove:** event/timeline semantics, tracker/game/message interpretation, build-order extraction, replay↔execution equivalence, benchmark integrity, broad Blizzard parser correctness, live SC2 in CI, or legal certification of replay rights.

---

## 2. Relationship to other milestones

| Milestone | Relationship |
| --------- | ------------- |
| M08 | **Source of truth** for raw parser-owned sections (`raw_sections`, `protocol_context`, `event_streams_available`). M09 maps a **narrow subset** into normalized metadata. |
| M10 | Owns **event semantics** and timeline interpretation — **out of scope** for M09. |
| M11 | Owns **build-order / economy** — **out of scope** for M09. |

---

## 3. Allowed inputs

| Artifact | Required | Role |
| -------- | -------- | ---- |
| `replay_raw_parse.json` | **Yes** | Canonical M08 envelope (`schema_version` `starlab.replay_raw_parse.v1`). |
| `replay_parse_receipt.json` | Optional | Linkage: `replay_content_sha256` and `raw_parse_sha256` (must match canonical hash of the raw parse object). |
| `replay_parse_report.json` | Optional | Linkage: `replay_content_sha256` must match; `parse_status` should be `parsed` for governed linkage. |

With `--raw-parse` alone, receipt/report checks are **not evaluated** (warning posture in the report).

---

## 4. Output artifacts

### 4.1 `replay_metadata.json`

**Schema:** `starlab.replay_metadata.v1`

| Field | Description |
| ----- | ----------- |
| `schema_version` | `starlab.replay_metadata.v1` |
| `metadata_contract_version` | `starlab.replay_metadata_contract.v1` |
| `replay_content_sha256` | From M08 raw parse; `null` if absent. |
| `source_raw_parse_sha256` | SHA-256 (hex) of **canonical JSON** (no trailing newline) of the full M08 raw parse object — same rule as M08 `raw_parse_sha256`. |
| `parser_family` | From M08 raw parse. |
| `parser_version` | From M08 raw parse. |
| `metadata_profile` | `starlab.replay_metadata_profile.v1` |
| `source_sections_present` | Sorted list of keys under `raw_sections` with non-null values. |
| `metadata` | Normalized metadata object (§5). |

### 4.2 `replay_metadata_report.json`

**Schema:** `starlab.replay_metadata_report.v1`

| Field | Description |
| ----- | ----------- |
| `schema_version` | `starlab.replay_metadata_report.v1` |
| `metadata_contract_version` | `starlab.replay_metadata_contract.v1` |
| `replay_content_sha256` | Echo from M08 when valid. |
| `source_raw_parse_sha256` | Canonical hash of raw parse input. |
| `extraction_status` | `extracted` · `partial` · `source_contract_failed` · `extraction_failed` (§7). |
| `check_results` | Ordered list (§8). |
| `reason_codes` | Machine-readable codes (sorted on emission). |
| `advisory_notes` | Human notes (sorted on emission). |

---

## 5. Normalized `metadata` shape

### 5.1 `protocol`

| Field | Source (M08) | Rules |
| ----- | ------------- | ----- |
| `base_build` | `protocol_context.m_baseBuild`, else `raw_sections.header.m_version.m_baseBuild` | Integer; default `0` if absent. |
| `data_build` | `protocol_context.m_dataBuild`, else `header.m_version.m_dataBuild` | Integer; default `0` if absent. |
| `data_version` | `protocol_context.m_revision`, else `header.m_version.m_revision` | Integer or `null` — **no** guessing. |

### 5.2 `map`

| Field | Source | Rules |
| ----- | ------ | ----- |
| `map_name` | `raw_sections.details.m_title` if string | Else `null`. |

### 5.3 `game`

| Field | Source | Rules |
| ----- | ------ | ----- |
| `game_length_loops` | `raw_sections.details.m_gameDurationLoops` if integer | Else `null`. **Do not** infer from tracker/game events. |
| `player_count` | `len(raw_sections.details.m_playerList)` if list | Else `0`. |
| `event_streams_available` | Copy of M08 `event_streams_available` (booleans) | Default all `false` if missing. |

### 5.4 `players`

Ordered by **`player_index` ascending** (stable sort).

| Field | Source | Rules |
| ----- | ------ | ----- |
| `player_index` | `m_workingSetSlotId` if integer, else list index | |
| `player_kind` | `m_control` | Enum mapping (§6). |
| `race_requested` | `m_race` | Enum mapping (§6). |
| `race_actual` | `m_race` | Same as requested unless `random` → actual `unknown` (no dual-race inference). |
| `result` | `m_result` | Enum mapping (§6). |

Non-dict entries in `m_playerList` are skipped; skipping triggers **ambiguous** posture for the player-metadata check.

---

## 6. Enum mappings (conservative)

Values are **only** mapped from explicit M08 fields. Unrecognized values → `unknown` (or `null` for nullable fields).

### `player_kind` (`human` · `computer` · `observer` · `unknown`)

- **String** (normalized enum name from M08): substring match on `HUMAN` / `COMPUTER` / `OBSERVER` after normalizing.
- **Integer `m_control`:** `1` → `human`, `2` → `computer`, `3` → `observer` (fixture-oriented; unknown otherwise).

### `race_requested` (`terran` · `zerg` · `protoss` · `random` · `unknown`)

- Lowercase string match: `terran`, `zerg`, `protoss`, substring `random`.

### `race_actual` (`terran` · `zerg` · `protoss` · `unknown`)

- Same as race string, but `random` maps to **`unknown`** for actual.

### `result` (`win` · `loss` · `tie` · `unknown`)

- **String:** `win`/`victory`, `loss`/`defeat`, `tie`/`draw`/`undecided`.
- **Integer:** `1` → win, `2` → loss, `3` → tie (conservative default table).

---

## 7. Extraction status

| Status | Meaning |
| ------ | ------- |
| `extracted` | Required sections present; core metadata and player rows complete; no ambiguous player rows. |
| `partial` | Artifacts emitted; some sections missing or fields `null`/`unknown`, or ambiguous player mapping. |
| `source_contract_failed` | Schema/hash failure, or receipt/report linkage mismatch, or `parse_status` ≠ `parsed` when report supplied. |
| `extraction_failed` | Malformed JSON load, or unexpected extraction error. |

---

## 8. Check model

Checks appear in fixed order (`METADATA_CHECK_IDS` in `starlab.replays.metadata_models`):

| `check_id` | Role |
| ---------- | ---- |
| `raw_parse_schema_valid` | `schema_version` is `starlab.replay_raw_parse.v1`. |
| `replay_hash_present` | `replay_content_sha256` is 64 hex chars. |
| `source_raw_parse_sha256_computed` | Hash computed for linkage (always evaluated on load). |
| `parse_receipt_hash_match` | If receipt provided: replay + raw hashes match. |
| `parse_report_status_parsed` | If report provided: replay hash + `parse_status` = `parsed`. |
| `required_sections_present` | `header`, `details`, `init_data` all non-null in `raw_sections`. |
| `core_metadata_extracted` | Protocol + game blocks structurally complete. |
| `player_metadata_extracted` | Player list well-formed; **warn** if ambiguous mapping. |
| `metadata_emitted` | Output artifacts written. |

**Status:** `pass` · `warn` · `fail` · `not_evaluated`  
**Severity:** `required` · `warning`

---

## 9. CLI

```bash
python -m starlab.replays.extract_replay_metadata \
  --raw-parse path/to/replay_raw_parse.json \
  --output-dir path/to/out \
  [--parse-receipt path/to/replay_parse_receipt.json] \
  [--parse-report path/to/replay_parse_report.json]
```

**Exit codes:** `0` extracted or partial · `4` extraction_failed · `5` source_contract_failed

---

## 10. Explicit non-claims

- M09 proves a **stable normalized metadata contract** derived from **M08** artifacts.
- M09 does **not** prove event/timeline semantics, build-order extraction, benchmark integrity, replay↔execution equivalence, or live SC2 execution in CI.
- Raw sections are still **parser-owned**; M09 only defines a **smaller public projection**.

---

## 11. Implementation references

- `starlab/replays/metadata_models.py` — schema constants, check IDs  
- `starlab/replays/metadata_extraction.py` — pure field mapping  
- `starlab/replays/metadata_io.py` — load, linkage, write  
- `starlab/replays/extract_replay_metadata.py` — CLI  
