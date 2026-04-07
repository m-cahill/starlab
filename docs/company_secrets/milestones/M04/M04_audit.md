# Milestone Audit — M04: Replay Binding to Run Identity (closed on `main`)

**Audit mode:** DELTA AUDIT (post-merge)  
**Milestone ID:** M04  
**Branch:** `m04-replay-binding-to-run-identity` (**merged**; remote **deleted**)  
**PR:** [#5](https://github.com/m-cahill/starlab/pull/5) — **merged**  
**Final PR head:** `6991978cb35172edda75f721149b1558d7ead226` — PR-head CI [24060734950](https://github.com/m-cahill/starlab/actions/runs/24060734950) — **success**  
**Merge commit:** `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed` — merged **2026-04-07T02:17:04Z** — post-merge `main` CI [24060997255](https://github.com/m-cahill/starlab/actions/runs/24060997255) — **success**  
**Date:** 2026-04-07

---

## 1. Header

- **Milestone:** M04 — Replay Binding to Run Identity  
- **Mode:** DELTA AUDIT  
- **Range:** `main` @ prior tip … `c38de5d920ca9fb18cef46da9be7f0ef812ed7ed` (merge of PR #5)  
- **CI Status:** Green (PR-head + post-merge `main`)  
- **Audit Verdict:** **Green** — M04 remained **below** parser substrate and canonical-run packaging scope; **no** CI guardrail weakening observed.

---

## 2. Executive Summary (Delta-Focused)

**Improvements**

- Deterministic **`replay_binding.json`** contract + implementation path for opaque replay bytes linked to M03 artifacts.
- Fixture-driven, **SC2-free** CI coverage for the new surface (synthetic `.SC2Replay` bytes).
- **CLI** boundary that consumes M03 JSON only (does not reopen M03 proof derivation).

**Risks (managed / explicit)**

- **Semantic gap:** a replay file can bind to M03 IDs without proving it is “the” replay of that execution — **acknowledged non-claim** in contract + ledger.
- **Untrusted replay boundary:** remains **unparsed** in M04; future parser work is **M08+**.

**Single most important next action:** execute **M05** under its own plan — **canonical run artifact v0** — without conflating it with replay parsing.

---

## 3. Delta Map & Blast Radius

**Changed**

- `docs/runtime/replay_binding.md`, `starlab/runs/replay_binding.py`, `starlab/runs/bind_replay.py`, tests + fixture, governance tests, `docs/starlab.md` (closeout).

**Risk zones**

- **Contracts:** new `starlab.replay_binding.v1` artifact — documented and tested.  
- **CI glue:** unchanged workflow; same gates.  
- **Auth / persistence / concurrency:** not touched.

---

## 4. Architecture & Modularity

### Keep

- Clear separation: M03 artifacts are **upstream**; M04 does not recompute `proof_artifact_hash` from raw proof files.
- `starlab.runs` package `__init__` does not import `bind_replay` CLI (mirrors M03 posture).

### Fix Now (≤ 90 min)

- None identified for M04 closeout.

### Defer

- **Canonical packaging** — `M05`  
- **Parser substrate** — `M08`

---

## 5. CI/CD & Workflow Integrity

- Required checks: Ruff, format, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks — **all present and passing** on PR-head and merge push.
- No observed `continue-on-error` or skipped merge gates.

---

## 6. Tests & Coverage (Delta-Only)

- New tests cover: content hash stability, binding ID stability, JSON determinism, CLI success/failure paths, end-to-end repeatability.
- **Coverage tooling:** not a separate enforced metric in this repo; delta is **behavioral** via tests.

---

## 7. Security & Supply Chain

- No new default runtime dependencies in `pyproject.toml`.
- pip-audit / SBOM / Gitleaks: **pass** on CI runs cited.

---

## 8. Top Issues (Max 7)

| ID | Category | Severity | Notes |
|----|----------|----------|-------|
| — | — | — | **No blocking findings** for M04 closeout. |

---

## 9. PR-Sized Action Plan

| ID | Task | Category | Acceptance Criteria | Risk | Est |
|----|------|----------|----------------------|------|-----|
| NEXT-001 | Author **M05** plan + branch | Planning | `M05_plan.md` replaced/extended per governance; no code until authorized | Low | Human |

---

## 10. Deferred Issues Registry

| ID | Issue | Discovered (M#) | Deferred To | Reason | Blocker? | Exit Criteria |
|----|-------|-----------------|-------------|--------|----------|---------------|
| DEF-001 | Replay semantic equivalence | M04 | M08+ | Out of scope for opaque binding | No | Parser + governance milestone proves equivalence claims |

---

## 11. Score Trend

| Milestone | Arch | Mod | Health | CI | Sec | Perf | DX | Docs | Overall |
|-----------|------|-----|--------|----|----|------|----|--------|--------|
| M04 | 3.5 | 3.5 | + | + | + | + | + | + | 4.5 |

*Weighting: qualitative governance signal; M04 matches prior Phase I milestones.*

---

## 12. Flake & Regression Log

| Item | Type | First Seen | Current Status | Last Evidence | Fix/Defer |
|------|------|------------|----------------|---------------|-----------|
| — | — | — | — | — | — |

---

## Machine-readable appendix

```json
{
  "milestone": "M04",
  "mode": "DELTA_AUDIT_POST_MERGE",
  "pr": 5,
  "final_pr_head": "6991978cb35172edda75f721149b1558d7ead226",
  "authoritative_pr_head_ci": "24060734950",
  "merge_commit": "c38de5d920ca9fb18cef46da9be7f0ef812ed7ed",
  "post_merge_main_ci": "24060997255",
  "verdict": "green_closed_on_main",
  "merged_to_main": true,
  "quality_gates": {
    "ci": "pass",
    "tests": "pass",
    "coverage": "not_enforced_repo_wide",
    "security": "pass",
    "workflows": "unchanged",
    "contracts": "documented"
  },
  "issues": []
}
```
