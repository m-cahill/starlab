# Milestone Summary — M27: Replay-Derived Imitation Baseline

**Project:** STARLAB  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Milestone:** M27 — Replay-Derived Imitation Baseline  
**Timeframe:** 2026-04-09 → 2026-04-09  
**Status:** Closed  

---

## 1. Milestone Objective

Prove the **first deterministic, offline, replay-derived trained imitation baseline artifact** — **`replay_imitation_baseline.json`** and **`replay_imitation_baseline_report.json`** — over the governed **M26** `replay_training_dataset.v1` contract and referenced **M14** replay bundle directories, using **in-process M16 → M18** materialization only, with **explicit non-claims** (not benchmark integrity, not live SC2, not **M28** learned-agent evaluation harness semantics).

---

## 2. Scope Definition

### In Scope

- Runtime contract `docs/runtime/replay_imitation_baseline_v1.md`
- Product: `baseline_models.py`, `baseline_features.py`, `baseline_fit.py`, `emit_replay_imitation_baseline.py`, `replay_observation_materialization.py` under `starlab/imitation/`
- Model family `starlab.m27.model.observation_signature_majority_v1`; feature policy `starlab.m27.feature.observation_signature_v1`
- Fixtures `tests/fixtures/m27/`; tests `tests/test_replay_imitation_baseline.py` (import guard, E2E M26→M27)
- AST import guard: no `starlab.replays`, `starlab.sc2`, or `s2protocol` in listed M27 imitation modules

### Out of Scope

- Benchmark integrity, leaderboard validity, live SC2 in CI, replay↔execution equivalence, hierarchical control, **M28** evaluation harness product code, strong imitation quality claims beyond internal `agreement_by_split` smoke metrics

---

## 3. Work Executed

- Implemented bounded context signatures, majority-label fit with lexicographic tie-break, global fallback, deterministic JSON artifacts.
- Implemented materialization seam (`replay_observation_materialization`) composing `load_m14_bundle` → `materialize_canonical_state` → `materialize_observation_surface` (no CLI shell-outs).
- CLI: `python -m starlab.imitation.emit_replay_imitation_baseline --dataset PATH --bundle PATH --output-dir OUT`.

---

## 4. Validation & Evidence

- **PR:** [#33](https://github.com/m-cahill/starlab/pull/33) — merged **2026-04-09T23:45:00Z** (UTC).
- **Final PR head:** `65dcd2fbfa1b6e8d05f6db8bebe191f4b8822ccc`
- **Merge commit:** `49b45825b65e56deb5cf991c5f74889e3daf2f59`
- **Authoritative PR-head CI:** [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) — success (**superseded** red PR-head [`24218859455`](https://github.com/m-cahill/starlab/actions/runs/24218859455) — Ruff format — **not** merge authority)
- **Merge-boundary `main` CI:** [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938) — success
- **482** pytest on authoritative PR-head CI; one pre-existing `s2protocol` deprecation warning in replay CLI tests (unchanged).

---

## 5. CI / Automation Impact

- No workflow file changes; existing **CI** workflow unchanged.

---

## 6. Issues & Exceptions

| Issue | Resolution |
| ----- | ---------- |
| Ruff format on first PR tip | Fixed in `65dcd2f…`; authoritative run **24218875847** |

---

## 7. Deferred Work

| Item | Deferred to | Notes |
| ---- | ------------- | ----- |
| Learned-agent evaluation harness | **M28** | Stub-only after M27 closeout |
| Benchmark integrity / replay↔execution equivalence | Future | Explicit non-claims preserved |

---

## 8. Governance Outcomes

- **Provable:** STARLAB can emit deterministic **replay imitation baseline** + report over governed **M26** + **M14** with forbidden-import discipline in M27 imitation modules (test-enforced).
- **Still not provable:** benchmark integrity, live SC2 in CI, **M28** harness, hierarchical agents, broad “learning capability” beyond the narrow M27 artifact.

---

## 9. Exit Criteria Evaluation

| Criterion | Met |
| --------- | --- |
| Runtime contract + deterministic baseline/report artifacts | Yes |
| Fixture-backed tests; goldens; import guard | Yes |
| Authoritative PR-head CI green | Yes ([`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847)) |
| Merge-boundary `main` CI green | Yes ([`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938)) |
| `docs/starlab.md` updated at closeout | Yes |
| **M28** stub only (no M28 product code in M27) | Yes |

---

## 10. Final Verdict

M27 **closed**: **first narrow, replay-derived, trained imitation baseline artifact** is **proved on `main`** under explicit non-claims. **Current milestone** advances to **M28** (Learned-Agent Evaluation Harness — **stub-only** for product code until chartered).
