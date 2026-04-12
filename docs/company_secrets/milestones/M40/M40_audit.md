# M40 — Delta audit (unified template v2)

* **Milestone:** M40 — Agent Training Program Charter & Artifact Contract  
* **Mode:** DELTA AUDIT  
* **Range:** `c557608066c9e0a35438ebe99a972949c49bfb45` (pre-M40 `main` tip) → `44e8edc5bcce8dc99576bf2be542b273095e5072` (merge commit of PR #51)  
* **CI Status:** Green (authoritative PR-head [`24295050784`](https://github.com/m-cahill/starlab/actions/runs/24295050784); merge-boundary `main` [`24295326123`](https://github.com/m-cahill/starlab/actions/runs/24295326123))  
* **Audit Verdict:** 🟢 — Milestone scope delivered; **M40 is a charter-and-contract milestone, not a training-result milestone.** No benchmark-integrity upgrade; no live SC2; no weights.

---

## Executive summary

**Improvements:** Governed **46-milestone** arc; Phase VI reframed as **M40**–**M45** training track; `starlab.training` emits deterministic **agent training program contract** JSON; ledger/README/architecture aligned; **M39** milestone-table completion enforced in tests; **M41**–**M45** stub folders; **OD-007** deferred beyond active arc.

**Risks:** Low — no new SC2 client boundary; training package is metadata/JSON only in CI. **Superseded** PR-head [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) (Ruff format) is **not** merge authority; resolved before merge.

**Residual:** GitHub Actions **Node 20** deprecation annotations (informational; track outside M40).

---

## Delta map & blast radius

* **Changed:** `docs/starlab.md`, `README.md`, `docs/architecture.md`, `starlab/training/*`, `docs/runtime/agent_training_program_contract_v1.md`, governance tests, milestone stubs **M42**–**M45**, `M41` plan rewrite, `M40` plan.  
* **Risk zones:** Ledger narrative length; governance test strictness on milestone strings. No auth, no deployment.

---

## Architecture & modularity

### Keep

* `starlab.training` as governance umbrella; `starlab.imitation` remains M26/M27 implementation home.

### Fix now

* None blocking post-merge.

### Defer

* Optional actions Node 24 migration when pins updated.

---

## CI/CD & workflow integrity

* Required jobs on **24295050784** and **24295326123**: **quality**, **smoke**, **tests**, **security**, **fieldtest**, **flagship**, **governance** — all success.  
* **Superseded:** [`24295030115`](https://github.com/m-cahill/starlab/actions/runs/24295030115) — **not** merge authority.

---

## Tests & coverage

* **701** tests at PR tip; **`fail_under` 78.0** unchanged.

---

## Security & supply chain

* No dependency changes in M40 merge (product scope).

---

## Top issues (max 7)

| ID | Category | Severity | Observation | Recommendation | Guardrail |
| --- | --- | --- | --- | --- | --- |
| — | — | — | No blocking issues | — | — |

---

## PR-sized action plan

| ID | Task | Acceptance |
| --- | --- | --- |
| A1 | None blocking post-M40 | N/A |

---

## Deferred issues registry (append)

| ID | Issue | Discovered | Deferred To | Reason | Blocker? | Exit |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | GitHub Actions Node 20 deprecation | Pre-M40 | TBD | Upstream runner | No | Pin bump when available |

---

## Score trend (placeholder)

| Milestone | Overall |
| --- | --- |
| M40 | Maintained — governance charter + contract emission |

---

## Flake & regression log

| Item | Status |
| --- | --- |
| M40 PR / main CI | Green PR-head + merge-boundary |

---

## Machine-readable appendix

```json
{
  "milestone": "M40",
  "mode": "delta",
  "merge_commit": "44e8edc5bcce8dc99576bf2be542b273095e5072",
  "pr_head": "be47d913737f322bbf8e9e08a672561c71d322eb",
  "verdict": "green",
  "milestone_kind": "charter_and_contract_not_training_results",
  "quality_gates": {
    "ci_pr_head": "24295050784",
    "ci_main_merge_boundary": "24295326123",
    "superseded_not_authority": "24295030115"
  },
  "non_claims": [
    "no_model_training",
    "no_weights",
    "no_benchmark_integrity",
    "no_live_sc2_ci"
  ]
}
```
