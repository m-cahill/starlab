# Milestone Audit — M21: Scripted Baseline Suite

**Audit mode:** DELTA AUDIT  
**Milestone:** M21 — Scripted Baseline Suite  
**Diff range (illustrative):** `cf1bee9…` (`main` before M21) → `092d00a…` (merge commit of PR #22)  
**PR:** [#22](https://github.com/m-cahill/starlab/pull/22)  
**Final PR head:** `818002e56b512e504c27f12aba8a39bc73627c82`  
**Merge commit:** `092d00a8aff720a1df9cbb1beec1cbf661546953`  
**CI (authoritative PR-head):** [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912) — **success**  
**CI (merge-boundary `main`):** [`24174498486`](https://github.com/m-cahill/starlab/actions/runs/24174498486) — **success**  
**Lint/typecheck:** Ruff + Mypy green on authoritative runs  

---

## Summary

M21 adds a **fixture-only scripted baseline suite** that consumes the M20 benchmark contract: deterministic `scripted_baseline_suite.json` + `scripted_baseline_suite_report.json` with embedded M20-valid scorecards, runtime documentation, CLI, self-contained fixtures/goldens, and tests. **No** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M21 baseline modules (AST import guard). One **non-authoritative** red PR-head run ([`24174444383`](https://github.com/m-cahill/starlab/actions/runs/24174444383)) failed **Ruff format** on `scripted_baseline_scorecards.py` — fixed before merge; **authoritative** merge gate is [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912). **No HIGH findings** blocking progression to **M22** stubs. **Heuristic baselines**, **evaluation runner**, **tournament harness**, **benchmark integrity**, and **replay↔execution equivalence** remain **not** proved.

---

## Findings

### F1 — Narrow claim discipline

- **Observation:** Runtime contract and suite artifacts enforce `fixture_only` measurement surface, scripted subjects only, and scorecard posture locks; ledger and summary explicitly exclude runner/tournament/heuristic work.
- **Interpretation:** Appropriate for first consumer of M20 contract surface without over-claiming.
- **Recommendation:** Keep M22 product-free until explicit M22 plan authorization.
- **Guardrail:** Governance tests for M21 fixtures/modules; import guard test on M21 baseline sources.

### F2 — CI truth signal

- **Observation:** Authoritative PR-head run [`24174468912`](https://github.com/m-cahill/starlab/actions/runs/24174468912) and merge-boundary `main` push run [`24174498486`](https://github.com/m-cahill/starlab/actions/runs/24174498486) both **success**; superseded red run [`24174444383`](https://github.com/m-cahill/starlab/actions/runs/24174444383) documented in `M21_run1.md` as **not** merge authority.
- **Interpretation:** Merge gate and post-merge checks align with prior milestones.
- **Recommendation:** Continue recording superseded red PR-head runs when they precede the final green tip.
- **Guardrail:** Ledger §18 / `M21_run1.md` record both authoritative run IDs and merge commit SHA.

### F3 — Pre-existing pytest warning (out of M21 scope)

- **Observation:** `DeprecationWarning` from `s2protocol` transitive `imp` import may still appear when replay CLI tests run (unchanged from prior milestones).
- **Interpretation:** Environmental; not introduced by `starlab/baselines/`.
- **Recommendation:** Optional future hygiene milestone; not M21-blocking.

---

## Deferred issues registry

| ID | Item | Status |
| -- | ---- | ------ |
| — | M22 heuristic baseline suite | Deferred to M22 (stubs only) |
| — | M23 evaluation runner / tournament harness | Deferred to M23 |

---

## Verdict

**M21 delta is governance-consistent, scope-bounded, and CI-backed on authoritative PR-head and merge-boundary `main`.** Proceed to **M22** planning on stub files only; no M22 product code without a new milestone plan.

**Sign-off posture:** M21 suitable for ledger closeout; **M22** remains **stub-only** for product.
