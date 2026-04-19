# 📌 Milestone Summary — PX1-M03: Candidate Strengthening & Demo Readiness Remediation

**Project:** STARLAB  
**Phase:** Post-PV1 (PX1)  
**Milestone:** PX1-M03 — Candidate Strengthening & Demo Readiness Remediation  
**Timeframe:** Opening [PR #90](https://github.com/m-cahill/starlab/pull/90) (2026-04-18) → closeout [PR #91](https://github.com/m-cahill/starlab/pull/91) (2026-04-19)  
**Status:** Closed  

---

## 1. Milestone Objective

Provide **corrective remediation** after **PX1-M02** closed honestly with **`no-candidate-selected`**: strengthen the bounded **`local_live_sc2`** candidate surface, freeze a **PX1-M03** remediation protocol, and run a fresh evaluation under **unchanged frozen minima** so governance could record either **`demo-ready-candidate-selected`** or **`no-demo-ready-candidate-within-scope`**.

---

## 2. Scope Definition

### In Scope

- Same primary candidate id: **`px1_m01_weighted_refit_rl_bootstrap_v1`** (no derived id).
- Frozen **`px1_demo_readiness_*`** protocol input and deterministic emitters; bounded hybrid live action surface (PR #90).
- Operator-local **`local_live_sc2`** evaluation series under **`evaluation_series_id`** `px1_m03_eval_post_watchable_capture_2026_04_19` (10 matches, 5+5 opponent profiles).
- Replay-backed wins; **≥1** watchable win (win + non-null **`optional_media_registration`** on the same run).
- Optional media on the counted watchable run ultimately registered against operator-local **`out/px1_m03_operator_watchable.mp4`** (registration metadata re-sealed on the same winning run directory **`runs/scripted_01`** — **not** a fabricated win).

### Out of Scope

- **PX1-M04** (governed demo proof pack / winning video) — **not** opened by this milestone.
- **v2** — **not** opened.
- New industrial campaign; ladder/public strength; default CI live SC2 proof.

---

## 3. Work Executed

- **Code / protocol (PR #90):** Runtime doc, emitters, hybrid policy wiring, fixtures, governance tests — already on `main`.
- **Operator-local:** Remediation reruns; authoritative series root  
  `out/training_campaigns/px1_m01_full_run_2026_04_17_a/px1_m03_eval_series_post_watchable_capture_2026_04_19`  
  with **`demo_readiness_declaration.md`** = **`demo-ready-candidate-selected`**.
- **Media registration cleanup:** Watchable win **`scripted_01`** — **`optional_media_registration`** updated to the **real** captured file path + content hash (run body re-sealed per **`validation_run_sha256`** rules).
- **Governance closeout (this PR):** `docs/starlab.md`; **`PX1-M03_summary.md`** / **`PX1-M03_audit.md`** / **`PX1-M03_run2.md`**; runtime doc status note.

---

## 4. Validation & Evidence

- Aggregates in **`evidence/px1_m03_evaluation_input.json`**: **6** overall wins, **6** replay-backed wins, **1** watchable win, **`selection.status`**: **`demo-ready-candidate-selected`**.
- Evidence bundle **`px1_demo_readiness_evidence.json`** satisfies frozen threshold evaluation (**`satisfies_frozen_thresholds`: true**).
- Operator artifacts remain **local-first** (`out/`); **not** default CI proof.

---

## 5. CI / Automation Impact

- Closeout PR is **documentation / ledger** only; default **`ci.yml`** expected **green** — see **`PX1-M03_run2.md`**.

---

## 6. Issues & Exceptions

- **PX1-M02** negative outcome remains **historical** — **not** reinterpreted.
- **Optional:** Early watchable registration used a tiny placeholder file; **closeout** aligns registration with **real** **`out/px1_m03_operator_watchable.mp4`** on the **same** winning run.

---

## 7. Deferred Work

- **PX1-M04** — explicit charter only.
- **PX1-M05** — optional; not opened.
- **v2** — explicit recharter only.

---

## 8. Governance Outcomes

- **PX1-M03** **closed** with a **successful** frozen-protocol remediation outcome: **`demo-ready-candidate-selected`**.
- **`current milestone`** = **None** until a new **`PX1-MNN`** is chartered.
- **PX1-M04** / **v2** remain **unopened** by this closeout.

---

## 9. Exit Criteria Evaluation

| Criterion | Met |
| --- | --- |
| Frozen minima satisfied with honest declaration | **Met** — **`demo-ready-candidate-selected`** |
| Same candidate id | **Met** |
| Replay-backed + watchable gates | **Met** |
| No automatic **PX1-M04** | **Met** |

---

## 10. Final Verdict

**PX1-M03** objectives for corrective demo-readiness remediation are **met**. Safe to record closure; **PX1-M04** requires **separate** authorization.

---

## 11. Authorized Next Step

**None** auto-authorized. Next **PX1** work (**PX1-M04** or other) requires **explicit** charter; **v2** requires **explicit** recharter.

---

## 12. Canonical References

- PR #90 (open PX1-M03 / protocol freeze)
- PR #91 (governance closeout — this change set)
- `docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`
- Operator-local series root (see §3)
- `PX1-M03_protocol_freeze.md`, `PX1-M03_remediation_rationale.md`, `PX1-M03_run1.md`
