# Milestone Audit — M23: Evaluation Runner & Tournament Harness

**Audit mode:** DELTA AUDIT  
**Milestone:** M23 — Evaluation Runner & Tournament Harness  
**Diff range (illustrative):** `621277c…` (`main` before M23) → `b8857d2…` (merge commit of PR #24)  
**PR:** [#24](https://github.com/m-cahill/starlab/pull/24)  
**Final PR head:** `f00711a3a2c16573f31492398de59387fe284711`  
**Merge commit:** `b8857d2ccfdb2963d4fd2311f98d02cbe79aa252`  
**CI (authoritative PR-head):** [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) — **success**  
**CI (merge-boundary `main`):** [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940) — **success**  
**Lint/typecheck:** Ruff + Mypy green on authoritative runs  

---

## Summary

M23 adds a **fixture-only evaluation tournament** that consumes the M20 benchmark contract and **M21/M22** governed suite JSON: deterministic `evaluation_tournament.json` + `evaluation_tournament_report.json`, runtime documentation, CLI under `starlab/evaluation/`, goldens under `tests/fixtures/m23/`, and tests including import guard and **M20→M21/M22→M23** chain proof. **No** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M23 evaluation modules. **No** superseded red PR-head runs on the final merge tip. **No HIGH findings** blocking progression to **M24** stubs. **Benchmark integrity**, **replay↔execution equivalence**, **M24 diagnostics**, and **M25 evidence packs** remain **not** proved.

---

## Executive summary (delta-focused)

**Improvements**

- First **evaluation consumer** of M21/M22 suite artifacts under a deterministic harness.
- Explicit tournament non-claims and primary-metric-only decision policy documented in runtime contract.
- E2E test chains M20 contract → M21/M22 emitters → M23 runner.

**Risks**

- None new beyond inherited fixture-only posture (numeric values are not live SC2 performance).

**Most important next action**

- Keep **M24** stub-only until authorized; **no** diagnostics product code without a new milestone plan.

---

## Findings

### F1 — Narrow claim discipline

- **Observation:** Runtime contract and artifacts enforce `fixture_only`, primary-metric pairwise decisions, full metric rows for transparency, and explicit tournament non-claims.
- **Interpretation:** Appropriate for first runner/harness proof without benchmark-integrity leakage.
- **Recommendation:** Hold M24 scope to attribution/diagnostics only when authorized.
- **Guardrail:** Governance tests for M23 fixtures/modules; import guard on `starlab/evaluation/`.

### F2 — CI truth signal

- **Observation:** Authoritative PR-head [`24178571859`](https://github.com/m-cahill/starlab/actions/runs/24178571859) and merge-boundary `main` [`24178615940`](https://github.com/m-cahill/starlab/actions/runs/24178615940) both **success**; no superseded red PR-head on final tip.
- **Interpretation:** Merge gate and post-merge checks align with prior milestones.
- **Recommendation:** Record both run IDs and merge commit SHA in ledger §18 / `M23_run1.md`.
- **Guardrail:** Ledger §23 changelog entry for merge-boundary event.

### F3 — Pre-existing pytest warning (out of M23 scope)

- **Observation:** `DeprecationWarning` from `s2protocol` transitive `imp` import may still appear when replay CLI tests run (unchanged from prior milestones).
- **Interpretation:** Environmental; not introduced by `starlab/evaluation/` M23 modules.
- **Recommendation:** Optional future hygiene milestone; not M23-blocking.

---

## Deferred issues registry

| ID | Item | Status |
| -- | ---- | ------ |
| — | M24 attribution/diagnostics | Deferred to M24 (stubs only) |

---

## Verdict

**M23 delta is governance-consistent, scope-bounded, and CI-backed on authoritative PR-head and merge-boundary `main`.** Proceed with **M24** planning on stub files only; no M24 product code without a new milestone plan.

**Sign-off posture:** M23 suitable for ledger closeout; **M24** remains **stub-only** for product.

---

## Machine-readable appendix (JSON)

```json
{
  "milestone": "M23",
  "mode": "DELTA_AUDIT",
  "commit": "b8857d2ccfdb2963d4fd2311f98d02cbe79aa252",
  "range": "621277c...b8857d2",
  "verdict": "green",
  "quality_gates": {
    "ci": "pass",
    "tests": "pass",
    "coverage": "n/a",
    "security": "pass",
    "workflows": "pass",
    "contracts": "pass"
  },
  "issues": [],
  "deferred_registry_updates": ["M24 diagnostics — deferred"],
  "score_trend_update": {}
}
```
