# Milestone Audit — M22: Heuristic Baseline Suite

**Audit mode:** DELTA AUDIT  
**Milestone:** M22 — Heuristic Baseline Suite  
**PR / merge / CI:** *TBD — record after merge to `main`*

---

## Summary

M22 adds a **fixture-only heuristic baseline suite** parallel to M21’s scripted suite: deterministic `heuristic_baseline_suite.json` + `heuristic_baseline_suite_report.json` with embedded M20-valid scorecards (`subject_kind: heuristic`), runtime documentation, CLI, fixture-backed goldens (reusing the shared M20 benchmark contract JSON), and tests including AST import guards on M22 baseline modules. **No** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M22 baseline modules.

**Evaluation runner**, **tournament harness** (**M23**), **benchmark integrity**, and **replay↔execution equivalence** remain **not** proved.

---

## Findings

### F1 — Scope discipline

* **Observation:** Heuristic suite mirrors M21’s narrow offline emission pattern; two fixed subjects, one fixture case, explicit suite/scorecard non-claims.
* **Interpretation:** Appropriate second consumer of M20 contract surface without runner or execution claims.

### F2 — Shared benchmark contract fixture

* **Observation:** M22 reuses `tests/fixtures/m21/valid_benchmark_contract.json` (already allows `heuristic` in `subject_kinds_allowed`).
* **Interpretation:** Avoids duplicate contract fixtures; M20 remains the contract authority milestone.

---

## Verdict

**M22 delta is scope-bounded** pending authoritative green PR-head and merge-boundary CI recorded in `M22_run1.md` and §18.
