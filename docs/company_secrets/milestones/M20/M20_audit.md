# Milestone Audit — M20: Benchmark Contract & Scorecard Semantics

**Audit mode:** DELTA AUDIT  
**Milestone:** M20 — Benchmark Contract & Scorecard Semantics  
**Diff range (illustrative):** `a6c1f50…` (`main` before M20) → `cf1bee9…` (merge commit of PR #21)  
**PR:** [#21](https://github.com/m-cahill/starlab/pull/21)  
**Final PR head:** `5c2233690a3dc6d352dd9b06be16430b3d73b6e8`  
**Merge commit:** `cf1bee980756b3b59d4db2620c041a23f14eba18`  
**CI (authoritative PR-head):** [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) — **success**  
**CI (merge-boundary `main`):** [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) — **success**  
**Lint/typecheck:** Ruff + Mypy green on authoritative runs  

---

## Summary

M20 adds **governed benchmark contract and scorecard JSON Schemas** plus deterministic reports, runtime documentation, CLI emission, and fixture/golden tests. New `starlab/benchmarks/` modules do not import `starlab.replays`, `starlab.sc2`, or `s2protocol` (AST import guard). **No HIGH findings** blocking progression to **M21** stubs. **Benchmark integrity**, **replay↔execution equivalence**, and **baselines** remain **not** proved (unchanged).

---

## Findings

### F1 — Phase IV boundary clarity

- **Observation:** Ledger + runtime doc distinguish contract/schema work from M21–M23 execution and baselines; scorecard vocabulary (`scored` / `unscored` / `disqualified`, comparability states) does not assert benchmark validity.
- **Interpretation:** Appropriate for a contract-first milestone.
- **Recommendation:** Keep M21 product-free until explicit plan authorization.
- **Guardrail:** Governance tests + import-pattern test on M20 benchmark sources.

### F2 — CI truth signal

- **Observation:** Authoritative PR-head run [`24173251270`](https://github.com/m-cahill/starlab/actions/runs/24173251270) and merge-boundary `main` push run [`24173270201`](https://github.com/m-cahill/starlab/actions/runs/24173270201) both **success**; informational Node.js 20 deprecation annotation only (non-blocking).
- **Interpretation:** Merge gate and post-merge checks align with prior milestones.
- **Recommendation:** Track Node/action upgrades under future hygiene if still relevant mid-2026.
- **Guardrail:** Ledger §18 records both run IDs with merge commit SHA.

### F3 — Pre-existing pytest warning (out of M20 scope)

- **Observation:** `DeprecationWarning` from `s2protocol` transitive `imp` import may still appear when replay CLI tests run (unchanged from prior milestones).
- **Interpretation:** Environmental; not introduced by `starlab/benchmarks/`.
- **Recommendation:** Optional future hygiene milestone; not M20-blocking.

---

## Deferred issues registry

| ID | Item | Status |
| -- | ---- | ------ |
| — | M21 scripted baseline suite | Deferred to M21 |

---

## Verdict

**M20 delta is governance-consistent, scope-bounded, and CI-backed on authoritative PR-head and merge-boundary `main`.** Proceed to **M21** planning on stub files only; no M21 product code without a new milestone plan.

**Sign-off posture:** M20 suitable for ledger closeout; **M21** remains **stub-only**.
