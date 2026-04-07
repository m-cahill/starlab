# 📌 Milestone Summary — M09: Replay Metadata Extraction

**Project:** STARLAB  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Milestone:** M09 — Replay Metadata Extraction  
**Timeframe:** 2026-04-07 → 2026-04-07  
**Status:** Closed  

---

## 1. Milestone Objective

Define and implement a **stable, deterministic, public replay metadata contract** derived from **M08** `replay_raw_parse.json` (and optional receipt/report linkage), without claiming event/timeline semantics (M10), build-order extraction (M11), or benchmark integrity.

---

## 2. Scope Definition

### In Scope

- Contract: `docs/runtime/replay_metadata_extraction.md`
- Modules: `starlab/replays/metadata_models.py`, `metadata_extraction.py`, `metadata_io.py`, `extract_replay_metadata.py` (CLI)
- Artifacts: `replay_metadata.json`, `replay_metadata_report.json`
- Pure extraction over normalized M08 JSON; **no** `s2protocol` imports in M09
- CI default: fixture-driven; **no** optional `replay-parser` extra required
- Optional governed linkage to `replay_parse_receipt.json` / `replay_parse_report.json`

### Out of Scope

- Event/timeline semantics; tracker/game/message interpretation (M10)
- Build-order / economy (M11)
- Replay↔execution semantic equivalence; benchmark integrity
- Broad Blizzard parser correctness; live SC2 execution in CI
- Legal certification of third-party replay rights

---

## 3. Work Executed

- Implemented pure metadata extraction pipeline, linkage checks, deterministic JSON emission, and CLI
- Added synthetic M08-style fixtures under `tests/fixtures/m09/`
- Extended governance tests for M09 surfaces; locked `M09_plan.md`

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24101861888`](https://github.com/m-cahill/starlab/actions/runs/24101861888) (**success**) — final PR head `3f161dea12a9b7ffb6dbe01c73b01f351a7219da`
- **Authoritative post-merge `main` CI:** [`24101900950`](https://github.com/m-cahill/starlab/actions/runs/24101900950) (**success**) — merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`
- **PR:** [#10](https://github.com/m-cahill/starlab/pull/10); merged `2026-04-07T20:05:59Z`; remote branch **deleted**

---

## 5. What M09 Proves (narrow)

- **Stable normalized replay metadata** as a **public STARLAB contract** (`metadata_contract_version` / `metadata_profile`), derived from **M08** raw parse artifacts
- **Deterministic emission** of `replay_metadata.json` and `replay_metadata_report.json` with extraction status and ordered checks
- **Conservative field mapping** from M08 raw sections (`protocol_context`, `raw_sections`, `event_streams_available`) — smaller surface than full M08 output
- **Optional** SHA-256 linkage against M08 parse receipt/report when paths are supplied

---

## 6. What M09 Does Not Prove

- Event/timeline semantics (M10); build-order extraction (M11)
- Replay↔execution equivalence; benchmark integrity
- Broad parser correctness beyond the M08→M09 mapping; live SC2 in CI; legal certification of replay rights

---

## 7. Exit Criteria

Met — contract + code + tests on `main`, PR #10 merged, authoritative PR-head and post-merge `main` CI green, ledger and milestone artifacts updated.

---

## 8. Final Verdict

**Milestone closed** on `main` in the **narrow metadata-extraction** sense documented in `docs/runtime/replay_metadata_extraction.md`. **Event semantics** remain explicitly deferred to **M10**.

---

## 9. Canonical References

- PR: [#10](https://github.com/m-cahill/starlab/pull/10)
- Merge commit: `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`
- Final PR head: `3f161dea12a9b7ffb6dbe01c73b01f351a7219da`
- Run analysis: `M09_run1.md`
- Audit: `M09_audit.md`
