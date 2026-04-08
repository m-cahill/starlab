# Replay bundle & lineage contract (M14)

**Status:** Governed contract (M14)  
**Bundle contract:** `starlab.replay_bundle_contract.v1`  
**Bundle profile:** `starlab.replay_bundle.m14.v1`  
**Scope:** Deterministic **packaging manifest** and **lineage record** over already-governed Phase II replay JSON artifacts. **Not** a replay binary format, **not** an archive requirement, **not** raw replay ingestion.

---

## 1. Purpose

M14 defines how STARLAB turns **five primary governed replay artifacts** (M09–M13) plus **optional secondary report artifacts** into:

- `replay_bundle_manifest.json` — explicit membership, hashes, `bundle_id`, `lineage_root`, exclusions, determinism notes  
- `replay_bundle_lineage.json` — machine-readable **graph** of required replay-plane nodes (M09–M14) plus optional contextual M07/M08 ancestry  
- `replay_bundle_contents.json` — compact **inventory** (roles, primary vs report, policy exclusions) — not a second manifest

M14 does **not** prove: raw replay clipping, replay↔execution equivalence, benchmark integrity, live SC2 in CI, fog-of-war truth, simulation correctness, or state-schema semantics.

---

## 2. Glossary

| Term | Meaning |
| ---- | ------- |
| **Primary governed data artifact** | One of the five required JSON files: `replay_metadata.json`, `replay_timeline.json`, `replay_build_order_economy.json`, `replay_combat_scouting_visibility.json`, `replay_slices.json`. |
| **Secondary report artifact** | Optional `*_report.json` companion when present (e.g. `replay_slices_report.json`). Clearly separated from primary data in the manifest. |
| **Bundle** | The governed **description** of which JSON artifacts belong together, with hashes and lineage — **not** a zip/tar requirement in v1. |
| **Slice (M13)** | Metadata-defined temporal span in `replay_slices.json` — **not** bundle packaging. |
| **`bundle_id`** | SHA-256 over canonical JSON of `{contract, profile, lineage_root, generation_parameters, included_milestones}` — **deterministic packaging identity**, not execution-equivalence or legal provenance of replay rights. |
| **`lineage_root`** | SHA-256 over sorted primary artifact hashes — ties bundle identity to governed evidence only. |

---

## 3. Bundle vs slice distinction

- **M13** emits **slice definitions** (`replay_slices.json`) from M10–M12 JSON.  
- **M14** **packages** the **governed replay artifact plane** (M09–M13 primary JSON) into a portable bundle record.  
- M14 **must not** conflate slice semantics with bundle membership policy.

---

## 4. Required inputs

| Artifact | Milestone |
| -------- | --------- |
| `replay_metadata.json` | M09 |
| `replay_timeline.json` | M10 |
| `replay_build_order_economy.json` | M11 |
| `replay_combat_scouting_visibility.json` | M12 |
| `replay_slices.json` | M13 |

## 5. Optional inputs

| Artifact | Role |
| -------- | ---- |
| `replay_metadata_report.json` | Secondary report |
| `replay_timeline_report.json` | Secondary report |
| `replay_build_order_economy_report.json` | Secondary report |
| `replay_combat_scouting_visibility_report.json` | Secondary report |
| `replay_slices_report.json` | Secondary report |
| `replay_intake_receipt.json` (via CLI) | **Optional contextual lineage only** (M07) — **not** a bundle member |
| `replay_parse_receipt.json` (via CLI) | **Optional contextual lineage only** (M08) — **not** a bundle member |

M05 `manifest.json` / `hashes.json`, `replay_binding.json`, and other run-plane artifacts are **not** bundle members in M14 v1; they may appear only as optional lineage context if wired later.

---

## 6. Lineage model

- **Required proof surface (lineage):** M09 → M10 → M11 → M12 → M13 → M14 bundle node.  
- **Optional contextual ancestry:** M07 intake and/or M08 parse substrate nodes may appear when optional receipts are supplied. They are labeled **contextual ancestry** and **`proof_surface_required: false`** — not required for M14 success.  
- **Edges** encode the primary replay-plane chain; secondary report nodes are listed but are not interposed into that chain unless a future milestone extends the graph.

---

## 7. Included vs excluded surfaces

**Included (v1):** governed JSON listed in the manifest with explicit hashes.

**Excluded by policy (v1):**

- Raw `.SC2Replay` bytes  
- `replay_raw_parse.json` and parser-native blobs  
- Clipped sub-replays, video, images (unless a later milestone authorizes)  
- Zip/tar archives (not required in v1)

---

## 8. Determinism rules

- Canonical JSON + SHA-256 per `starlab.runs.json_util` (no trailing newline in hash input).  
- All manifest and lineage lists sorted deterministically.  
- `bundle_id` and `lineage_root` exclude wall-clock timestamps and local paths.  
- Bundle membership is **explicit** — no directory glob sweep for unknown files.

---

## 9. Manifest fields (summary)

| Field | Role |
| ----- | ---- |
| `contract` / `profile` / `schema_version` | Versioning |
| `bundle_id` | Deterministic packaging identity |
| `bundle_created_from` | Caller-provided provenance string (e.g. fixture name) |
| `primary_artifacts` | Ordered list of the five primary filenames |
| `secondary_report_artifacts` | Sorted list of included report filenames |
| `artifact_hashes` | Sorted map filename → sha256 |
| `lineage_root` | Hash over primary hashes |
| `generation_parameters` | Catalog / generator parameters |
| `included_milestones` | M09–M13 |
| `exclusions` | Policy list |
| `determinism_notes` | Short fixed string |
| `source_replay_identity` | Optional `replay_content_sha256` from metadata when present |

---

## 10. Non-claims

M14 proves deterministic **bundle packaging and lineage contract v1** over governed replay JSON.

M14 does **not** prove raw replay clipping, replay↔execution equivalence, benchmark integrity, live SC2 in CI, canonical state semantics, or legal certification of third-party replay rights.

---

## 11. CLI usage

```text
python -m starlab.replays.extract_replay_bundle --input-dir DIR --output-dir OUT \
  [--bundle-created-from STR] \
  [--optional-intake-receipt PATH] [--optional-parse-receipt PATH]
```

`DIR` must contain the five primary JSON files. Optional `*_report.json` files in `DIR` are picked up when present. Outputs: `replay_bundle_manifest.json`, `replay_bundle_lineage.json`, `replay_bundle_contents.json`.

Exit codes: `0` success; `4` load failure; `5` lineage validation failure.
