# 📌 Milestone Summary — M08: Replay Parser Substrate

**Project:** STARLAB  
**Phase:** II — Replay Intake, Provenance, and Data Plane  
**Milestone:** M08 — Replay Parser Substrate  
**Timeframe:** 2026-04-06 → 2026-04-07  
**Status:** Closed  

---

## 1. Milestone Objective

Provide a **governed replay parser substrate**: isolate Blizzard **`s2protocol`** behind a single adapter, deterministically lower parser-native output into JSON-safe STARLAB trees, and emit three governed artifacts (`replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json`) with explicit parse status and ordered checks — **without** claiming broad parser correctness, a public normalized metadata contract (M09), or timeline/event semantics (M10).

---

## 2. Scope Definition

### In Scope

- Contract: `docs/runtime/replay_parser_substrate.md` (`policy_version` `starlab.replay_parser_substrate.v1`)
- Modules: `starlab/replays/parser_models.py`, `parser_interfaces.py`, `parser_normalization.py`, `parser_io.py`, `s2protocol_adapter.py`, `parse_replay.py` (CLI)
- Optional extra: `pip install -e ".[replay-parser]"` for `s2protocol` / `mpyq`; default CI uses fixture adapters without live decode
- Deterministic normalization rules (`starlab.parser_normalization.v1`); unit/CLI/governance tests
- Optional hash linkage to M07 intake receipts/reports and M04 `replay_binding.json`

### Out of Scope

- Broad replay parser correctness; stable **public** normalized metadata (M09)
- Event/timeline semantics, build-order extraction (M10+)
- Replay↔execution semantic equivalence; benchmark integrity; live SC2 execution in CI
- Legal certification of third-party replay rights

---

## 3. Work Executed

- Implemented parser adapter boundary, normalization, artifact assembly, and `parse_replay` CLI
- Added `.gitattributes` and LF-aligned opaque replay fixture handling; regenerated M05 expected goldens where replay bytes participate in hashes
- Extended governance tests for M08 surfaces and M09 stubs; updated CONTRIBUTING and related runtime doc cross-links

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24069974048`](https://github.com/m-cahill/starlab/actions/runs/24069974048) (**success**) — final PR head `a65fabfa7fd76d94a250208fe20c2c4dfdf57105`
- **Authoritative post-merge `main` CI:** [`24070602968`](https://github.com/m-cahill/starlab/actions/runs/24070602968) (**success**) — merge commit `b99233e807177d65737beaba5246efa67a3edce2`
- **PR:** [#9](https://github.com/m-cahill/starlab/pull/9); merged `2026-04-07T07:52:12Z`; remote branch **deleted**

---

## 5. What M08 Proves (narrow)

- **Governed replay parser substrate** with **`s2protocol` isolated** behind `S2ProtocolReplayAdapter`
- **Deterministic lowering** of parser-native structures to JSON-safe `replay_raw_parse.json` (plus receipt/report)
- **Deterministic emission** of `replay_parse_receipt.json`, `replay_parse_report.json`, `replay_raw_parse.json`
- **Raw parser-owned sections** (`header`, `details`, `init_data`, optional `attribute_events`) and **availability / capability flags** for event streams (not semantics)
- **Optional** SHA-256 linkage against M07 intake artifacts and M04 replay binding when paths are supplied

---

## 6. What M08 Does Not Prove

- Broad replay parser correctness; stable normalized replay metadata as a **public** contract (M09)
- Event/timeline semantics (M10); build-order extraction; replay↔execution equivalence
- Benchmark integrity; live SC2 execution in CI; legal certification of replay rights

---

## 7. Exit Criteria

Met — contract + code + tests on `main`, PR #9 merged, authoritative PR-head and post-merge `main` CI green, ledger and milestone artifacts updated.

---

## 8. Final Verdict

**Milestone closed** on `main` in the **narrow parser-substrate** sense documented in `docs/runtime/replay_parser_substrate.md`. **Normalized metadata** and **event semantics** remain explicitly deferred to **M09** and **M10**.

---

## 9. Canonical References

- PR: [#9](https://github.com/m-cahill/starlab/pull/9)
- Merge commit: `b99233e807177d65737beaba5246efa67a3edce2`
- Final PR head: `a65fabfa7fd76d94a250208fe20c2c4dfdf57105`
- Run analysis: `M08_run1.md`
- Audit: `M08_audit.md`
