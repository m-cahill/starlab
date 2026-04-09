# Milestone Audit — M22: Heuristic Baseline Suite

**Audit mode:** DELTA AUDIT  
**Milestone:** M22 — Heuristic Baseline Suite  
**Diff range (illustrative):** `606579d…` (`main` before M22) → `470afa8…` (merge commit of PR #23)  
**PR:** [#23](https://github.com/m-cahill/starlab/pull/23)  
**Final PR head:** `96aba181f725b1303d54779d48556b7dffd7feb4`  
**Merge commit:** `470afa84ff80a2d76fb2693bce3a4397e6526afe`  
**CI (authoritative PR-head):** [`24176685407`](https://github.com/m-cahill/starlab/actions/runs/24176685407) — **success**  
**CI (merge-boundary `main`):** [`24176717132`](https://github.com/m-cahill/starlab/actions/runs/24176717132) — **success**  
**Lint/typecheck:** Ruff + Mypy green on authoritative runs  

---

## Summary

M22 adds a **fixture-only heuristic baseline suite** that consumes the M20 benchmark contract: deterministic `heuristic_baseline_suite.json` + `heuristic_baseline_suite_report.json` with embedded M20-valid scorecards (`subject_kind: heuristic`), runtime documentation, CLI, shared benchmark contract fixture (`tests/fixtures/m21/valid_benchmark_contract.json`), goldens under `tests/fixtures/m22/`, and tests. **No** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M22 baseline modules (AST import guard). **No** superseded red PR-head runs on the final merge tip. **No HIGH findings** blocking progression to **M23** stubs. **Evaluation runner**, **tournament harness** (**M23**), **benchmark integrity**, and **replay↔execution equivalence** remain **not** proved.

---

## Executive summary (delta-focused)

**Improvements**

- Second M20 contract consumer (heuristic subjects) with deterministic fixture emission and CI-backed tests.
- Explicit suite/scorecard non-claims and import boundary guard consistent with M21.
- Phase IV ledger clarity: M20 contract / M21–M22 fixture-only emitters / M23 runner boundary.

**Risks**

- None new beyond inherited M20/M21 posture (fixture values are not real SC2 performance claims).

**Most important next action**

- Keep **M23** stub-only until authorized; **no** runner product code without a new milestone plan.

---

## Findings

### F1 — Narrow claim discipline

- **Observation:** Runtime contract and suite artifacts enforce `fixture_only` measurement surface, heuristic subjects only, and scorecard posture locks; ledger and summary exclude runner/tournament/replay work.
- **Interpretation:** Appropriate for second consumer of M20 contract surface without over-claiming.
- **Recommendation:** Keep M23 product-free until explicit M23 plan authorization.
- **Guardrail:** Governance tests for M22 fixtures/modules; import guard test on M22 baseline sources.

### F2 — CI truth signal

- **Observation:** Authoritative PR-head run [`24176685407`](https://github.com/m-cahill/starlab/actions/runs/24176685407) and merge-boundary `main` push run [`24176717132`](https://github.com/m-cahill/starlab/actions/runs/24176717132) both **success**; no superseded red PR-head on final tip.
- **Interpretation:** Merge gate and post-merge checks align with prior milestones.
- **Recommendation:** Continue recording superseded red PR-head runs when they precede the final green tip.
- **Guardrail:** Ledger §18 / `M22_run1.md` record both authoritative run IDs and merge commit SHA.

### F3 — Pre-existing pytest warning (out of M22 scope)

- **Observation:** `DeprecationWarning` from `s2protocol` transitive `imp` import may still appear when replay CLI tests run (unchanged from prior milestones).
- **Interpretation:** Environmental; not introduced by `starlab/baselines/` M22 modules.
- **Recommendation:** Optional future hygiene milestone; not M22-blocking.

---

## Deferred issues registry

| ID | Item | Status |
| -- | ---- | ------ |
| — | M23 evaluation runner / tournament harness | Deferred to M23 (stubs only) |

---

## Verdict

**M22 delta is governance-consistent, scope-bounded, and CI-backed on authoritative PR-head and merge-boundary `main`.** Proceed to **M23** planning on stub files only; no M23 product code without a new milestone plan.

**Sign-off posture:** M22 suitable for ledger closeout; **M23** remains **stub-only** for product.

---

## Machine-readable appendix (JSON)

```json
{
  "milestone": "M22",
  "mode": "DELTA_AUDIT",
  "commit": "470afa84ff80a2d76fb2693bce3a4397e6526afe",
  "range": "606579d...470afa8",
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
  "deferred_registry_updates": ["M23 runner/harness — deferred"],
  "score_trend_update": {}
}
```
