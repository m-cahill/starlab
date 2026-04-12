# 📌 Milestone Summary — M41: Replay-Imitation Training Pipeline v1

**Project:** STARLAB  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Milestone:** M41 — Replay-Imitation Training Pipeline v1  
**Timeframe:** 2026-04-11 (implementation) → 2026-04-12 (merge to `main`)  
**Status:** Closed  

---

## 1. Milestone Objective

STARLAB needed a **governed, deterministic, local-first** path from governed **M26** training datasets and **M14** bundles to **training run artifacts** and optional **local-only** model weights, without implying benchmark superiority or live-play results. Without M41, Phase VI would lack a **first** replay-imitation **training pipeline** surface aligned with **M40** and bounded **non-claims**.

> Without M41, the program would have a training-program charter (**M40**) but no governed **training run** emission path for replay-imitation over M27-style features.

---

## 2. Scope Definition

### In Scope

- `starlab.imitation`: `replay_imitation_training_models.py`, `replay_imitation_training_io.py`, `replay_imitation_training_pipeline.py`, `emit_replay_imitation_training_run.py`.
- Refactor: `collect_imitation_example_rows` in `baseline_fit.py` (shared row collection).
- Dependency: `scikit-learn>=1.3,<2` in `pyproject.toml`.
- Artifacts: `replay_imitation_training_run.json`, `replay_imitation_training_run_report.json`; optional local `joblib` weights + recorded SHA (not committed).
- Feature schema and M40 contract binding fields in run/report.
- Runtime: `docs/runtime/replay_imitation_training_pipeline_v1.md`.
- Tests: `tests/test_m41_replay_imitation_training_pipeline.py`; governance/doc alignment.
- Ledger/README/architecture updates on branch; closeout on `main` post-merge.

### Out of Scope

- Benchmark-integrity or replay↔execution equivalence claims.
- Live SC2 in CI; GPU training in CI; weights in repository.
- **M42** comparison-harness product implementation.
- Ladder / live-play superiority claims.

---

## 3. Work Executed

- **[PR #52](https://github.com/m-cahill/starlab/pull/52)** merged to `main` (merge commit `5e0add12dd8f4b3a9b4dd31023319cc1999f826b`; final PR head `7c092eda7fe6554a2168968ffddbe37e929159e4`).
- Deterministic sklearn **logistic regression** over one-hot encoded M27 **context_signature** components; train/val split metrics in report.
- `.gitignore` for local `out/training_runs/` outputs where appropriate.

---

## 4. Validation & Evidence

- **Authoritative PR-head CI:** [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733) — success (all required jobs).
- **Superseded** intermediate green PR-head runs on the feature branch — **not** merge authority for final head; listed in `M41_run1.md`.
- **Merge-boundary `main` CI:** [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820) on merge commit `5e0add12…` — success.
- **Local validation (non-authoritative for public quality):** fixture dataset `tests/fixtures/m26/replay_training_dataset.json`; materialized M14 bundle under `out/training_runs/_m14_governed_bundle`; JSON-only and weights-enabled runs; on-disk SHA matched JSON for weights mode.

---

## 5. CI / Automation Impact

- No new CI jobs; M41 validated via existing **`tests`** lane (fixture-only CPU path).
- No gate weakening; `fail_under` unchanged.

---

## 6. Issues & Exceptions

- **Superseded** intermediate PR-head runs — **not** final merge authority; see `M41_run1.md`.
- **Node 20** deprecation annotations on Actions — informational (pre-existing).

---

## 7. Deferred Work

- **M42**–**M45** product milestones — stub until each closes on `main`.
- Optional Actions Node 24 migration — outside M41.

---

## 8. Governance Outcomes

- **First governed replay-imitation training pipeline** on `main`: bounded artifacts, explicit non-claims, no weights in repo.
- Feature schema and M40 contract linkage recorded in emitted JSON.

---

## 9. Exit Criteria Evaluation

| Criterion | Met / Partial / Not | Evidence |
| --- | --- | --- |
| Deterministic run + report emission | Met | Code + tests + runtime doc |
| Governed M26/M14 consumption | Met | Pipeline + tests |
| Optional local weights + hash | Met | Runtime + local validation |
| CI green at merge | Met | `24297208733`, `24297269820` |
| No benchmark-integrity / live-play claims | Met | Docs + artifacts |

---

## 10. Final Verdict

Milestone objectives met. **M41** is closed on `main` with authoritative CI and bounded non-claims. Safe to proceed to **M42** planning only (no M42 product work implied).

---

## 11. Authorized Next Step

- **M42** — Learned-Agent Comparison Harness v1 — **stub / planned** until implemented and closed on `main` with its own CI evidence.

---

## 12. Canonical References

- Merge commit: `5e0add12dd8f4b3a9b4dd31023319cc1999f826b`
- PR: [#52](https://github.com/m-cahill/starlab/pull/52)
- PR-head CI: [`24297208733`](https://github.com/m-cahill/starlab/actions/runs/24297208733)
- Merge-boundary `main` CI: [`24297269820`](https://github.com/m-cahill/starlab/actions/runs/24297269820)
- Documents: `docs/runtime/replay_imitation_training_pipeline_v1.md`, `docs/company_secrets/milestones/M41/M41_plan.md`, `M41_run1.md`, `M41_audit.md`
- Tag: **`v0.0.41-m41`** on merge commit `5e0add12…`
