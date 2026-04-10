# Milestone Audit — M28: Learned-Agent Evaluation Harness

**Audit mode:** DELTA AUDIT  
**Milestone:** M28 — Learned-Agent Evaluation Harness  
**Diff range (illustrative):** `49b4582…` (M27 merge) → `1ef6365…` (M28 merge)  
**PR:** [#34](https://github.com/m-cahill/starlab/pull/34)  
**Final PR head:** `c7ca6e6be8fbd44e39357da82cca857eddbd8eb3`  
**Merge commit:** `1ef636524269ff77ac26ac37584d43b50e9fcbc6`  
**CI (authoritative PR-head):** [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) — **success**  
**CI (merge-boundary `main`):** [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580) — **success**  
**Superseded (not merge authority):** none recorded for M28  
**Lint/typecheck:** Ruff + Mypy green on authoritative runs  

---

## Summary

M28 adds **offline learned-agent evaluation** for a **frozen M27** baseline against a governed **M20** `fixture_only` contract, **M26** dataset, and **M14** bundles, with held-out **`test`** split only. Artifacts: `learned_agent_evaluation.json` + `learned_agent_evaluation_report.json`; embedded M20 scorecard; runtime `docs/runtime/learned_agent_evaluation_harness_v1.md`. **No** widening into M23 tournament, M24 diagnostics, or M25 evidence pack. **No** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in listed M28 evaluation modules (AST-tested). **M29** remains **stub-only** — no M29 product code. **Benchmark integrity**, **live SC2**, **replay↔execution equivalence** remain **not** proved.

---

## Executive summary (delta-focused)

**Improvements**

- First **bounded** Phase V **evaluation** bridge from frozen imitation baseline to M20 scorecard surface (offline, fixture-driven CI).

**Risks**

- None new beyond inherited non-claims; evaluation metrics are **not** benchmark-integrity claims.

**Most important next action**

- Charter **M29** on stub files; land product work on **`m29-…`** branch per governance.

---

## Findings

### F1 — Scope discipline

- **Observation:** M28 does not import tournament/diagnostics/evidence-pack modules; contract is `fixture_only` + imitation subject; CLI rejects extra bundles.
- **Verdict:** Appropriate.

### F2 — CI truth signal

- **Observation:** Authoritative PR-head [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) and merge-boundary `main` [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580) both **success**.
- **Verdict:** Merge gate aligned with milestone discipline.

### F3 — Forbidden-import posture

- **Observation:** `tests/test_learned_agent_evaluation.py` AST-guards listed M28 evaluation modules against `starlab.replays`, `starlab.sc2`, `s2protocol`.
- **Verdict:** Consistent with prior evaluation milestones.

### F4 — Pre-existing pytest warning (out of M28 scope)

- **Observation:** `DeprecationWarning` from `s2protocol` may still appear in replay CLI tests (unchanged).
- **Verdict:** Not M28-blocking.

---

## Verdict

**M28 delta is governance-consistent, scope-bounded, and CI-backed on authoritative PR-head and merge-boundary `main`.** Proceed with **M29** planning on stub files; no M29 product code without a chartered M29 plan.

---

## Machine-readable appendix (JSON)

```json
{
  "milestone": "M28",
  "mode": "DELTA_AUDIT",
  "commit": "1ef636524269ff77ac26ac37584d43b50e9fcbc6",
  "verdict": "green",
  "quality_gates": {
    "ci": "pass",
    "tests": "pass",
    "contracts": "pass"
  },
  "issues": [],
  "deferred_registry_updates": ["M29 hierarchical agent interface — stub only"]
}
```
