# Milestone Summary — M26: Replay Corpus Governance & Training Dataset Contract

**Project:** STARLAB  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Milestone:** M26 — Replay Corpus Governance & Training Dataset Contract  
**Timeframe:** 2026-04-09 → 2026-04-09  
**Status:** Closed  

---

## 1. Milestone Objective

Prove a **deterministic, offline, governed replay-training-dataset layer** over **M14** replay bundle artifacts — **`replay_training_dataset.json`** and **`replay_training_dataset_report.json`** — with corpus selection, deterministic train/validation/test split, and coarse action-type labels — **without** training a model, **without** imitation quality claims, and **without** **M27** imitation-baseline product code.

Without this milestone, STARLAB would lack a **stable, governed dataset contract** for replay-derived examples before any learning milestone.

---

## 2. Scope Definition

### In Scope

- Runtime contract `docs/runtime/replay_training_dataset_v1.md`
- Product modules: `starlab/imitation/dataset_models.py`, `dataset_views.py`, `emit_replay_training_dataset.py`
- Artifacts: `replay_training_dataset.json`, `replay_training_dataset_report.json`
- Fixture-backed goldens under `tests/fixtures/m26/`; tests `tests/test_replay_training_dataset.py`
- AST import guard: no `starlab.replays`, `starlab.sc2`, or `s2protocol` in M26 imitation modules
- Ledger: **35-milestone** program arc (M00–M34); **OD-007** → **M34**

### Out of Scope

- Model training, imitation quality, hierarchical control, benchmark integrity, replay↔execution equivalence, live SC2 in CI, raw replay parsing in `starlab/imitation/`, **M27+** product code beyond stubs

---

## 3. Work Executed

- Implemented deterministic dataset + report construction from governed M14 bundle directories; optional M07 intake checks; canonical JSON + sorted warnings.
- Implemented CLI `python -m starlab.imitation.emit_replay_training_dataset --bundle PATH --output-dir OUT`.
- Extended governance and ledger for Phase V vocabulary and milestone closeout files.

---

## 4. Validation & Evidence

- **PR:** [#32](https://github.com/m-cahill/starlab/pull/32) — merged **2026-04-09T22:50:52Z** (UTC).
- **Final PR head:** `d8d3c4c82fdaab70e2238b40d4a5a7d30b2c230f`
- **Merge commit:** `e83a8493a577c9013d720f1debab009dcf9c464f`
- **Authoritative PR-head CI:** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) — success
- **Merge-boundary `main` CI:** [`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208) — success
- Local / CI: Ruff, Ruff format, Mypy, Pytest (**469** tests after closeout governance additions); one pre-existing `s2protocol` deprecation warning in replay CLI tests (unchanged).

---

## 5. CI / Automation Impact

- No workflow file changes; existing **CI** workflow unchanged.
- **M26** adds tests and `starlab/imitation/` modules; governance extended for milestone closeout files.

---

## 6. Issues & Exceptions

| Issue | Resolution |
| ----- | ---------- |
| — | None blocking on authoritative runs |

---

## 7. Deferred Work

| Item | Deferred to | Notes |
| ---- | ------------- | ----- |
| Replay-derived imitation baseline | M27 | Stub only until authorized |
| Benchmark integrity / replay↔execution equivalence | Future | Explicit non-claims preserved |

---

## 8. Governance Outcomes

- **Provable:** STARLAB can emit deterministic **replay training dataset** + report artifacts over governed **M14** bundles with no forbidden imports in M26 imitation modules (test-enforced).
- **Still not provable:** benchmark integrity, live SC2 in CI, **M27** imitation baseline — unchanged.

---

## 9. Exit Criteria Evaluation

| Criterion | Met |
| --------- | --- |
| Runtime contract + deterministic dataset/report artifacts | Yes |
| Fixture-backed tests; goldens; import guard | Yes |
| Authoritative PR-head CI green | Yes ([`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559)) |
| Merge-boundary `main` CI green | Yes ([`24217178208`](https://github.com/m-cahill/starlab/actions/runs/24217178208)) |
| `docs/starlab.md` updated at closeout | Yes |
| **M27** stub only (no M27 product code) | Yes |

---

## 10. Final Verdict

Milestone objectives met. **M26 closed.** Authorized next planning target: **M27** — Replay-Derived Imitation Baseline (stubs only until authorized).

---

## 11. Authorized Next Step

- **M27 — Replay-Derived Imitation Baseline:** planning stubs under `docs/company_secrets/milestones/M27/`; **no** M27 product code until a dedicated milestone plan and PR.

---

## 12. Canonical References

- PR: https://github.com/m-cahill/starlab/pull/32  
- Final PR head: `d8d3c4c82fdaab70e2238b40d4a5a7d30b2c230f`  
- Merge commit: `e83a8493a577c9013d720f1debab009dcf9c464f`  
- PR-head CI: https://github.com/m-cahill/starlab/actions/runs/24217118559  
- Merge-boundary `main` CI: https://github.com/m-cahill/starlab/actions/runs/24217178208  
- Contract: `docs/runtime/replay_training_dataset_v1.md`  
- Ledger: `docs/starlab.md`  
- Run log: `M26_run1.md`
