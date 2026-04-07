# Milestone Audit — M08: Replay Parser Substrate

**Milestone:** M08 — Replay Parser Substrate  
**Mode:** DELTA AUDIT  
**Range:** `8bf82d40ff99fab5b293c6a47b830a7e27ed8636` (pre-merge `main` tip) → `b99233e807177d65737beaba5246efa67a3edce2` (merge commit)  
**CI Status:** Green  
**Audit Verdict:** 🟢 — PR-head and post-merge `main` CI succeeded; scope stayed substrate-only with explicit non-claims in contract and ledger.

---

## Executive Summary

**Improvements**

- Clear **adapter boundary** for `s2protocol` (`starlab/replays/s2protocol_adapter.py`); imports constrained by contract and governance tests.
- **Deterministic normalization** and **three-artifact** emission path with ordered checks and parse status model.
- **Fixture-first CI** default (no mandatory live decode in default `dev` install).

**Risks**

- **Upstream replay stack** remains an **untrusted boundary** (documented in `docs/starlab.md` §10); M08 does not certify Blizzard decode semantics.
- **Optional** `replay-parser` extra introduces `s2protocol` deprecation noise locally; CI does not require it for merge authority.

**Next action:** Proceed under **M09** for **stable normalized replay metadata** contract only when M09 plan authorizes it; no M09 product code until then (stubs only).

---

## Delta Map & Blast Radius

| Area | Change |
| ---- | ------ |
| Contracts | New `docs/runtime/replay_parser_substrate.md` |
| Code | New `starlab/replays/*` parser modules + CLI; tests |
| CI / fixtures | `.gitattributes`, M05 golden updates for cross-OS replay hashing |

**Risk zones:** Contracts (schemas/version strings), CI glue (fixture determinism), dependency optional extra.

---

## Architecture & Modularity

### Keep

- Adapter protocol + single concrete `s2protocol` implementation file.
- Pure normalization module with explicit rejection of non-finite floats and unsupported types.

### Fix Now (≤ 90 min)

- None blocking; optional follow-up: pin or silence `s2protocol` `imp` deprecation outside STARLAB scope.

### Defer

- Normalized public metadata schema (**M09**).
- Event stream decoding semantics (**M10**).

---

## CI/CD & Workflow Integrity

- Required **`governance`** job on PR and on `main` push; no weakened gates observed.
- **Authoritative PR-head CI:** run `24069974048` — **success** — commit `a65fabfa7fd76d94a250208fe20c2c4dfdf57105`.
- **Authoritative post-merge `main` CI:** run `24070602968` — **success** — merge commit `b99233e807177d65737beaba5246efa67a3edce2`.

---

## Quality Gates

| Gate | Result |
| ---- | ------ |
| CI Stability | PASS — merge gate green |
| Tests | PASS — new logic covered with unit/CLI tests |
| Workflows | PASS — same workflow as prior milestones |
| Contracts | PASS — M08 contract matches artifact field intent |

---

## Top Issues

| ID | Severity | Note |
| -- | -------- | ---- |
| AUD-001 | Low | Upstream `s2protocol` deprecation warnings when optional extra installed — informational |

---

## Deferred Issues Registry (append)

| ID | Issue | Discovered (M#) | Deferred To | Reason |
| -- | ----- | --------------- | ----------- | ------ |
| DEF-M08-001 | Public normalized replay metadata contract | M08 | M09 | Explicitly out of scope per contract |
| DEF-M08-002 | Timeline / event semantics | M08 | M10 | M08 exposes availability only |

---

## Score Trend (M08)

| Milestone | Arch | Mod | Health | CI | Sec | Perf | DX | Docs | Overall |
| --------- | ---- | --- | ------ | -- | --- | ---- | -- | ---- | ------- |
| M08 | 3.5 | 3.5 | 4.0 | 4.5 | 4.0 | — | 4.0 | 4.5 | 4.3 |

*(Informal; aligns with §20 ledger row.)*

---

## Machine-Readable Appendix

```json
{
  "milestone": "M08",
  "mode": "delta",
  "commit": "b99233e807177d65737beaba5246efa67a3edce2",
  "range": "8bf82d4...b99233e",
  "verdict": "green",
  "quality_gates": {
    "ci": "pass",
    "tests": "pass",
    "coverage": "pass",
    "security": "pass",
    "workflows": "pass",
    "contracts": "pass"
  },
  "issues": [],
  "deferred_registry_updates": ["DEF-M08-001", "DEF-M08-002"],
  "score_trend_update": { "milestone": "M08", "overall": 4.3 }
}
```
