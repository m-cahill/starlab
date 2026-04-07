# Replay — Parser Substrate (M08)

**Status:** Governed contract (M08)  
**Policy / contract:** `policy_version` `starlab.replay_parser_substrate.v1`  
**Parser contract version:** `parser_contract_version` `starlab.replay_parser_contract.v1`  
**Scope:** Deterministic lowering of **raw** parser output into STARLAB JSON artifacts; **no** normalized public metadata contract (M09). **M10** may extend `replay_raw_parse.json` with an optional **`raw_event_streams`** payload (schema `starlab.replay_raw_parse.v2`) decoded behind the same adapter boundary — **public timeline semantics** remain **M10 extraction**, not M08 proof claims.

---

## 1. Purpose

This document defines the **M08** replay parser substrate contract:

- a single **adapter boundary** (`ReplayParserAdapter`) isolating optional Blizzard **`s2protocol`** (+ MPQ reader **`mpyq`**);
- deterministic **normalization** of parser-native Python values into JSON-safe trees;
- three governed artifacts: `replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json`;
- a small **parse status** model and **ordered check** list suitable for audit;
- explicit **non-claims** so later milestones (M09–M11) do not over-read M08.

**M08 does not prove:** broad parser correctness, stable semantic interpretation of Blizzard structures, benchmark integrity, replay↔execution equivalence, cross-host portability, live SC2 execution in CI, or legal certification of replay rights.

---

## 2. Relationship to other milestones

| Milestone | Relationship |
| --------- | ------------- |
| M01 | Canonical replay decode boundary remains **`s2protocol`** (see `docs/runtime/sc2_runtime_surface.md`). |
| M07 | Optional `replay_intake_receipt.json` / `replay_intake_report.json`; hash linkage only — intake report is **advisory** unless extended elsewhere. |
| M04 | Optional `replay_binding.json` — `replay_content_sha256` must match observed replay when supplied. |
| M09 | Owns **stable normalized replay metadata** derived from raw sections — **out of scope** for M08. |
| M10 | Owns **decoded event stream lowering** (`raw_event_streams`) when emitted, plus **public timeline contract** in M10 modules — M08’s standing claim remains **availability flags** + raw sections; interpret M08 historical text as **not** requiring event bodies until v2. |

---

## 3. Dependency posture

- Install optional extra: `pip install -e ".[replay-parser]"` (declares `s2protocol`; pulls **`mpyq`**).
- CI default install (`pip install -e ".[dev]"`) does **not** include `s2protocol`; tests use **fixture adapters** without claiming live decode in CI.
- **Do not** import `s2protocol` outside `starlab/replays/s2protocol_adapter.py`.

---

## 4. Parser boundary

- **Interface:** `ReplayParserAdapter` (`starlab.replays.parser_interfaces`) — `parser_family`, `parser_version`, `dependency_available`, `parse_replay_file`.
- **Implementation:** `S2ProtocolReplayAdapter` in `starlab/replays/s2protocol_adapter.py` only.
- **CLI:** `python -m starlab.replays.parse_replay --replay … --output-dir …` with optional linkage flags (see §8).

---

## 5. Normalization rules (`normalization_profile`)

Profile constant: `starlab.parser_normalization.v1`.

- Object keys sorted lexicographically; nested dicts recurse.
- `tuple` → `list` (elements normalized).
- `bytes` / `bytearray` → lowercase **hex** string (two hex digits per byte).
- `enum.Enum` → enum **name** string (stable).
- `float`: reject non-finite values (no NaN / Infinity in STARLAB JSON).
- Unsupported types → explicit failure (`NormalizationError`).

---

## 6. Output artifacts

### 6.1 `replay_parse_receipt.json`

**Schema:** `starlab.replay_parse_receipt.v1`

| Field | Description |
| ----- | ----------- |
| `schema_version` | `starlab.replay_parse_receipt.v1` |
| `replay_content_sha256` | SHA-256 of replay bytes (hex) or `null` if unreadable. |
| `observed_filename` | Basename of `--replay` path. |
| `parser_family` | Adapter family (e.g. `s2protocol`). |
| `parser_version` | Adapter/library version string. |
| `parse_input_artifacts` | Map of optional input filenames → SHA-256 of file contents (or `null`). |
| `raw_parse_sha256` | SHA-256 of canonical JSON (**no trailing newline**) of `replay_raw_parse.json` body. |
| `policy_version` | `starlab.replay_parser_substrate.v1` |
| `parser_contract_version` | `starlab.replay_parser_contract.v1` |

### 6.2 `replay_parse_report.json`

**Schema:** `starlab.replay_parse_report.v1`

| Field | Description |
| ----- | ----------- |
| `schema_version` | `starlab.replay_parse_report.v1` |
| `replay_content_sha256` | Same as receipt. |
| `parser_family` | Same as receipt. |
| `parser_version` | Same as receipt. |
| `parse_status` | One of §7. |
| `check_results` | Ordered list (§9). |
| `reason_codes` | Machine-readable codes (sorted in emission). |
| `advisory_notes` | Human notes (sorted in emission). |

### 6.3 `replay_raw_parse.json`

**Schema:** `starlab.replay_raw_parse.v1`

| Field | Description |
| ----- | ----------- |
| `schema_version` | `starlab.replay_raw_parse.v1` |
| `replay_content_sha256` | Observed replay hash. |
| `parser_family` | Adapter family. |
| `parser_version` | Adapter version. |
| `protocol_context` | Narrow build context (e.g. `m_baseBuild`) or `null` if absent. |
| `raw_sections` | `header`, `details`, `init_data`, optional `attribute_events` — **normalized** trees, not public metadata. |
| `event_streams_available` | Booleans: `game_events_available`, `message_events_available`, `tracker_events_available`, `attribute_events_available`. |
| `normalization_profile` | `starlab.parser_normalization.v1` |

---

## 7. Parse status model

| Status | Meaning |
| ------ | ------- |
| `parsed` | Adapter succeeded; normalized raw parse envelope emitted. |
| `unsupported_protocol` | Replay readable but no protocol for replay build. |
| `parser_unavailable` | Optional dependency not importable (e.g. CI without extra). |
| `parse_failed` | Adapter invoked but decode failed (corrupt MPQ, decode error, normalization failure). |
| `input_contract_failed` | Intake receipt or binding hash mismatch / malformed linkage before parse. |

---

## 8. CLI

```bash
python -m starlab.replays.parse_replay \
  --replay path/to/file.SC2Replay \
  --output-dir path/to/out \
  [--intake-receipt path/to/replay_intake_receipt.json] \
  [--intake-report path/to/replay_intake_report.json] \
  [--replay-binding path/to/replay_binding.json]
```

**Exit codes:** `0` parsed · `2` unsupported_protocol · `3` parser_unavailable · `4` parse_failed · `5` input_contract_failed.

---

## 9. Check model

Checks appear in fixed order (`PARSE_CHECK_IDS` in `starlab.replays.parser_models`):

| `check_id` | Role |
| ---------- | ---- |
| `replay_file_readable` | Replay bytes readable. |
| `replay_sha256_computed` | Content hash computed. |
| `parser_dependency_available` | Optional imports available. |
| `parser_adapter_selected` | Adapter identity recorded. |
| `intake_receipt_hash_match` | If intake receipt provided, `replay_content_sha256` matches. |
| `binding_hash_match` | If binding provided, `replay_content_sha256` matches. |
| `parse_attempted` | Adapter invoked when dependencies available and contract passed. |
| `raw_sections_normalized` | Normalization succeeded for success path. |
| `raw_parse_emitted` | `replay_raw_parse.json` body produced (empty envelope allowed on failure paths). |

**Status:** `pass` · `warn` · `fail` · `not_evaluated`  
**Severity:** `required` · `warning`

---

## 10. Explicit non-claims

- M08 proves a **governed parser substrate** and **deterministic lowering** of raw parser-owned sections into STARLAB JSON.
- M08 does **not** prove replay parser correctness in the broad sense, replay semantic extraction, benchmark integrity, replay↔execution equivalence, or live SC2 execution in CI.
- Raw sections are **parser-owned** blobs for downstream milestones; they are **not** yet a stable public metadata API.

---

## 11. Implementation references

- `starlab/replays/parser_models.py` — schema constants, check IDs  
- `starlab/replays/parser_interfaces.py` — adapter protocol  
- `starlab/replays/parser_normalization.py` — normalization  
- `starlab/replays/parser_io.py` — orchestration and artifact assembly  
- `starlab/replays/s2protocol_adapter.py` — **only** `s2protocol` imports  
- `starlab/replays/parse_replay.py` — CLI  
