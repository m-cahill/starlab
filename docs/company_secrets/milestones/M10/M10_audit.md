# Milestone Audit — M10: Timeline & Event Extraction

**Milestone:** M10 — Timeline & Event Extraction  
**Mode:** DELTA AUDIT  
**Range:** `fc9b442d66abe9a2922e93051c7d0a22ccb133d1` (M09 merge on `main`) → `cb3e581f70f85653477081eb1ef4772229f05983` (M10 merge commit); Mypy repair `cf2074e10ec8a38b22bd7b75ffeb4ec22a71485b` (green `main`)  
**CI Status:** Green on `main` after repair (`24104197912`); merge-push on merge commit failed Mypy (`24104111851`)  
**Audit Verdict:** — **M10 scope** delivered with explicit non-claims; merge-gate PR-head CI not completed green on final tip (cancelled run only); **governance green** restored on repair commit.

---

## Executive Summary

**Improvements**

- **Public timeline contract** (`docs/runtime/replay_timeline_event_extraction.md`) with deterministic `replay_timeline.json` / `replay_timeline_report.json` and merge policy.
- **Parser boundary extension** for optional `raw_event_streams` on `replay_raw_parse.json` v2 without re-opening M08’s narrow substrate claim as broad semantic proof.
- **Fixture-first CI** for timeline extraction (synthetic raw-parse JSON paths).

**Risks**

- **Merge timing vs PR CI:** final PR-head workflow was cancelled; authority for “green before merge” is weaker than prior milestones — mitigated by post-merge repair and green `main` on `cf2074e…`.
- **Upstream event semantics** remain partially opaque; M10 maps conservatively and documents non-claims.

**Next action:** Proceed under **M11** for build-order / economy only per plan; **no** M11 product code without milestone governance.

---

## Delta Map & Blast Radius

| Area | Change |
| ---- | ------ |
| Contracts | `docs/runtime/replay_timeline_event_extraction.md` |
| Code | `starlab/replays/timeline_*.py`, `extract_replay_timeline.py`, parser adapter / `parser_io` v2 paths |
| CI / fixtures | `tests/fixtures/m10/*`; timeline tests |

**Risk zones:** Merge policy stability, v1 vs v2 raw parse shapes, governance expectations on §11 current milestone.

---

## Architecture & Modularity

### Keep

- Pure extraction separate from I/O; deterministic canonical JSON hashing.
- `s2protocol` remains isolated in the adapter; timeline does not import it.

### Fix Now (≤ 90 min)

- None blocking after Mypy repair on `main`.

---

## CI & Evidence Posture

| Check | Result |
| ----- | ------ |
| Merge-push on `cb3e581…` | Failed Mypy — documented |
| Repair `cf2074e…` | Green `24104197912` — authoritative for current `main` |

---

## Verdict

**Narrow M10 claims** are consistent with code and contracts; **broad strategic or upstream-semantic claims** are appropriately excluded. Closeout artifacts and ledger updated; **current milestone** advanced to **M11** (stub).
