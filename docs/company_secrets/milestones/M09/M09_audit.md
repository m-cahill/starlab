# Milestone Audit — M09: Replay Metadata Extraction

**Milestone:** M09 — Replay Metadata Extraction  
**Mode:** DELTA AUDIT  
**Range:** `1f0998edb419970a9f3539946a95edaba6cf0946` (pre-merge `main` tip) → `fc9b442d66abe9a2922e93051c7d0a22ccb133d1` (merge commit)  
**CI Status:** Green  
**Audit Verdict:** 🟢 — PR-head and post-merge `main` CI succeeded; scope stayed extraction-only with explicit non-claims in contract and ledger.

---

## Executive Summary

**Improvements**

- **Public metadata contract** (`docs/runtime/replay_metadata_extraction.md`) with explicit raw→normalized field mapping; **no** `s2protocol` in M09 modules.
- **Deterministic two-artifact** emission (`replay_metadata.json`, `replay_metadata_report.json`) with ordered checks and extraction status model.
- **Fixture-first CI** default (synthetic M08-style JSON; no live replay decode required).

**Risks**

- **Upstream replay semantics** remain **untrusted**; M09 maps only what M08 already lowered — it does not certify Blizzard field meaning in the broad sense.
- **Enum / control-value mapping** is conservative; unknowns surface as `unknown` — future real-replay edge cases may need contract revision under M10+ governance if discovered.

**Next action:** Proceed under **M10** for **timeline / event stream semantics** only when M10 plan authorizes; **no** M10 product code until then (stubs only).

---

## Delta Map & Blast Radius

| Area | Change |
| ---- | ------ |
| Contracts | New `docs/runtime/replay_metadata_extraction.md` |
| Code | New `starlab/replays/metadata_*.py`, `extract_replay_metadata.py`; tests + fixtures |
| CI / fixtures | `tests/fixtures/m09/*`; governance expectations |

**Risk zones:** Contract version strings, extraction status rollup, receipt/report linkage edge cases.

---

## Architecture & Modularity

### Keep

- Pure extraction module separate from I/O and CLI.
- Linkage and hash verification in `metadata_io.py` only.

### Fix Now (≤ 90 min)

- None blocking.

### Defer

- Event stream decoding and timeline semantics (**M10**).
- Build-order / economy (**M11**).

---

## CI/CD & Workflow Integrity

- Required **`governance`** job on PR and on `main` push; no weakened gates observed.
- **Authoritative PR-head CI:** run `24101861888` — **success** — commit `3f161dea12a9b7ffb6dbe01c73b01f351a7219da`.
- **Authoritative post-merge `main` CI:** run `24101900950` — **success** — merge commit `fc9b442d66abe9a2922e93051c7d0a22ccb133d1`.

---

## Quality Gates

| Gate | Result |
| ---- | ------ |
| CI Stability | PASS — merge gate green |
| Tests | PASS — extraction + CLI + governance |
| Workflows | PASS — same workflow as prior milestones |
| Contracts | PASS — M09 contract matches artifact field intent |

---

## Top Issues

| ID | Severity | Note |
| -- | -------- | ---- |
| AUD-M09-001 | Low | Optional `s2protocol` deprecation warnings remain in unrelated tests when extra installed — informational |

---

## Deferred Issues Registry (append)

| ID | Issue | Discovered (M#) | Deferred To | Reason |
| -- | ----- | --------------- | ----------- | ------ |
| DEF-M09-001 | Timeline / event semantics | M09 | M10 | Explicitly out of scope per contract |
| DEF-M09-002 | Build-order / economy | M09 | M11 | Explicitly out of scope per contract |

---

## Score Trend (M09)

| Milestone | Arch | Mod | Health | CI | Sec | Perf | DX | Docs | Overall |
| --------- | ---- | --- | ------ | -- | --- | ---- | -- | ---- | ------- |
| M09 | 3.5 | 3.5 | 4.0 | 4.5 | 4.0 | — | 4.0 | 4.5 | 4.3 |

*(Informal; aligns with §20 ledger row.)*

---

## Audit Closure

M09 delta is **governance-aligned** and **evidence-backed**. **HIGH:** none. **MEDIUM:** none. Proceed to **M10** planning stubs only until M10 scope is locked.
