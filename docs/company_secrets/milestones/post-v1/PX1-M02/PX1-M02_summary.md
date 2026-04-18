# 📌 Milestone Summary — PX1-M02: Play-Quality Evaluation & Demo Candidate Selection

**Project:** STARLAB  
**Phase:** Post-PV1 (PX1)  
**Milestone:** PX1-M02 — Play-Quality Evaluation & Demo Candidate Selection  
**Timeframe:** Opening [PR #88](https://github.com/m-cahill/starlab/pull/88) (2026-04-18) → closeout [PR #PR_PLACEHOLDER](https://github.com/m-cahill/starlab/pull/PR_PLACEHOLDER) (2026-04-18)  
**Status:** Closed  

---

## 1. Milestone Objective

Establish whether a **bounded**, **replay-backed**, **local_live_sc2** evaluation under the **frozen protocol profile v2** could justify selecting **one** coherent demo candidate from the **PX1-M01** campaign pool (**primary:** post-bootstrap weighted-refit joblib) — and record an honest **`candidate-selected`** or **`no-candidate-selected`** outcome. **Protocol profile v1** remains **historical / audit-only** (non-discriminating for meaningful play-quality). **Protocol v2** is the **authoritative corrective** evaluation basis (substantive horizon, replay save, M43→M44 live actions).

**PX1-M01** proved **industrial full-run threshold-met** — **not** play-quality or demo selection; **PX1-M02** evaluates play-quality **separately**.

---

## 2. Scope Definition

### In Scope

- Frozen **protocol v2** input (`tests/fixtures/px1_m02/protocol_input_v2.json`), bounded opponent profiles (scripted + heuristic v2 fixtures), one candidate (`px1_m01_weighted_refit_rl_bootstrap_v1`).
- **Authoritative operator-local** final series: `out/training_campaigns/px1_m01_full_run_2026_04_17_a/px1_m02_eval_series_final` — **10** **`local_live_sc2`** matches (**5**+**5**), replay bytes saved, **`no-candidate-selected`** (bounded harness macro + semantic actions; **0** wins).
- Public runtime **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`**; deterministic protocol/evidence emitters; governance tests; ledger closeout.

### Out of Scope

- **PX1-M03** (governed demo/video proof), **v2** (product arc), ladder/public strength, CI-as-default live SC2 proof.
- Fabricating a second candidate for optics.

---

## 3. Deliverables (observed)

| Deliverable | Evidence |
| --- | --- |
| Protocol v2 emission + evidence | `px1_m02_eval_series_final/protocol/`, `evidence/px1_play_quality_evidence.json` (+ reports) |
| Evaluation input + declaration | `evidence/px1_m02_evaluation_input.json`, `demo_candidate_selection_declaration.md` = **`no-candidate-selected`** |
| Operator note | `px1_play_quality_operator_note.md` in series root |
| Governance closeout | `docs/starlab.md`; this summary; `PX1-M02_audit.md`; `PX1-M02_run2.md` |

---

## 4. Explicit Non-Claims

- **Not** demo/video proof (**PX1-M03** does not open automatically).
- **Not** ladder or global benchmark integrity.
- **Not** **v2** readiness.
- **Not** a claim that the evaluated candidate is strategically strong — outcome was **`no-candidate-selected`**.

---

## 5. Outcome

**PX1-M02** **closed** on `main`. **`current milestone`** = **None**. **`PX1-M03`–`PX1-M04`** remain **planned / not yet opened**. **v2** remains **not** opened.
