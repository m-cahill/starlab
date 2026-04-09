# Milestone Audit — M27: Replay-Derived Imitation Baseline

**Audit mode:** DELTA AUDIT  
**Milestone:** M27 — Replay-Derived Imitation Baseline  
**Diff range (illustrative):** `e83a849…` (merge commit of PR #32 / M26) → `49b4582…` (merge commit of PR #33)  
**PR:** [#33](https://github.com/m-cahill/starlab/pull/33)  
**Final PR head:** `65dcd2fbfa1b6e8d05f6db8bebe191f4b8822ccc`  
**Merge commit:** `49b45825b65e56deb5cf991c5f74889e3daf2f59`  
**CI (authoritative PR-head):** [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) — **success**  
**CI (merge-boundary `main`):** [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938) — **success**  
**Superseded (not merge authority):** [`24218859455`](https://github.com/m-cahill/starlab/actions/runs/24218859455) — Ruff format failure on earlier tip  
**Lint/typecheck:** Ruff + Mypy green on authoritative runs  

---

## Summary

M27 adds **deterministic offline replay imitation baseline** packaging over governed **M26** + **M14**: `replay_imitation_baseline.json` + `replay_imitation_baseline_report.json`, runtime documentation, modules + CLI under `starlab/imitation/`, goldens under `tests/fixtures/m27/`, tests including import guard and E2E chain. **No** `starlab.replays`, **no** `starlab.sc2`, **no** `s2protocol` in the listed M27 imitation modules. **No HIGH findings** blocking progression to **M28** stubs. **Benchmark integrity**, **replay↔execution equivalence**, **M28 learned-agent evaluation harness**, and **broad imitation quality** remain **not** proved.

---

## Executive summary (delta-focused)

**Improvements**

- First **Phase V** **trained** artifact (narrow majority-label-per-signature) over **M26** + **M14** with explicit non-claims.
- Reusable **M16 → M18** materialization seam (`replay_observation_materialization`).

**Risks**

- None new beyond inherited offline / fixture posture; `agreement_by_split` is **internal smoke only** — not benchmark claims.

**Most important next action**

- Keep **M28** **stub-only** until chartered; **no** evaluation-harness product code without a new milestone plan.

---

## Findings

### F1 — Narrow claim discipline

- **Observation:** Runtime contract and code emphasize **offline baseline artifact** + **non-claims**; no benchmark integrity or M28 harness semantics.
- **Verdict:** Appropriate.

### F2 — CI truth signal

- **Observation:** Authoritative PR-head [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) and merge-boundary `main` [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938) both **success**; superseded [`24218859455`](https://github.com/m-cahill/starlab/actions/runs/24218859455) documented.
- **Verdict:** Merge gate aligned with milestone discipline.

### F3 — Pre-existing pytest warning (out of M27 scope)

- **Observation:** `DeprecationWarning` from `s2protocol` may still appear in replay CLI tests (unchanged).
- **Verdict:** Not M27-blocking.

---

## Verdict

**M27 delta is governance-consistent, scope-bounded, and CI-backed on authoritative PR-head and merge-boundary `main`.** Proceed with **M28** planning on stub files only; no M28 product code without a new milestone plan.

---

## Machine-readable appendix (JSON)

```json
{
  "milestone": "M27",
  "mode": "DELTA_AUDIT",
  "commit": "49b45825b65e56deb5cf991c5f74889e3daf2f59",
  "verdict": "green",
  "quality_gates": {
    "ci": "pass",
    "tests": "pass",
    "contracts": "pass"
  },
  "issues": [],
  "deferred_registry_updates": ["M28 learned-agent evaluation harness — stub only"]
}
```
