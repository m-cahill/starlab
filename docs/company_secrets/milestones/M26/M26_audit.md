# Milestone Audit — M26: Replay Corpus Governance & Training Dataset Contract

**Audit mode:** DELTA AUDIT  
**Milestone:** M26 — Replay Corpus Governance & Training Dataset Contract  
**Diff range (illustrative):** `f03c7bf…` (merge commit of PR #31 / M25) → `e83a849…` (merge commit of PR #32)  
**PR:** [#32](https://github.com/m-cahill/starlab/pull/32)  
**Final PR head:** `d8d3c4c82fdaab70e2238b40d4a5a7d30b2c230f`  
**Merge commit:** `e83a8493a577c9013d720f1debab009dcf9c464f`  
**CI (authoritative PR-head):** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) — **success**  
**CI (merge-boundary `main`):** [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208) — **success**  
**Lint/typecheck:** Ruff + Mypy green on authoritative runs  

---

## Summary

M26 adds **deterministic offline replay training dataset packaging** over governed **M14** bundle directories: `replay_training_dataset.json` + `replay_training_dataset_report.json`, runtime documentation, modules + CLI under `starlab/imitation/`, goldens under `tests/fixtures/m26/`, and tests including import guard. **No** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in M26 imitation modules. **No HIGH findings** blocking progression to **M27** stubs. **Benchmark integrity**, **replay↔execution equivalence**, **model training**, and **M27 imitation baseline** remain **not** proved.

---

## Executive summary (delta-focused)

**Improvements**

- First **Phase V** dataset contract over **M14** bundles with explicit non-claims (no training, no imitation quality).
- Governance alignment with **35-milestone** arc (M00–M34) and **OD-007** → **M34**.

**Risks**

- None new beyond inherited offline / fixture posture (dataset contract does not certify benchmark integrity or live SC2).

**Most important next action**

- Keep **M27** stub-only until authorized; **no** imitation-baseline product code without a new milestone plan.

---

## Findings

### F1 — Narrow claim discipline

- **Observation:** Runtime contract and code emphasize **dataset contract + corpus governance** only; no model training or evaluation semantics.
- **Interpretation:** Appropriate for a pre-learning substrate without normative imitation authority.
- **Recommendation:** Hold M27 scope to chartered imitation baseline when authorized.
- **Guardrail:** Governance tests for M26 fixtures/modules; import guard on `starlab/imitation/`.

### F2 — CI truth signal

- **Observation:** Authoritative PR-head [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) and merge-boundary `main` [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208) both **success**.
- **Interpretation:** Merge gate and post-merge checks align with milestone discipline.
- **Recommendation:** Record both run IDs and merge commit SHA in ledger §18 / `M26_run1.md`.
- **Guardrail:** Ledger §23 changelog entry for merge + closeout.

### F3 — Pre-existing pytest warning (out of M26 scope)

- **Observation:** `DeprecationWarning` from `s2protocol` transitive `imp` import may still appear when replay CLI tests run (unchanged from prior milestones).
- **Interpretation:** Environmental; not introduced by M26 `starlab/imitation/` modules.
- **Recommendation:** Optional future hygiene milestone; not M26-blocking.

---

## Deferred issues registry

| ID | Item | Status |
| -- | ---- | ------ |
| — | M27 replay-derived imitation baseline | Deferred to M27 (stubs only) |

---

## Verdict

**M26 delta is governance-consistent, scope-bounded, and CI-backed on authoritative PR-head and merge-boundary `main`.** Proceed with **M27** planning on stub files only; no M27 product code without a new milestone plan.

**Sign-off posture:** M26 suitable for ledger closeout; **M27** remains **stub-only** for product.

---

## Machine-readable appendix (JSON)

```json
{
  "milestone": "M26",
  "mode": "DELTA_AUDIT",
  "commit": "e83a8493a577c9013d720f1debab009dcf9c464f",
  "range": "f03c7bf...e83a849",
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
  "deferred_registry_updates": ["M27 imitation baseline — deferred"],
  "score_trend_update": {}
}
```
