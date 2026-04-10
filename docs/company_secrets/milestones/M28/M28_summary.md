# Milestone Summary — M28: Learned-Agent Evaluation Harness

**Project:** STARLAB  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Milestone:** M28 — Learned-Agent Evaluation Harness  
**Timeframe:** 2026-04-10  
**Status:** Closed  

---

## 1. Milestone Objective

Prove a **deterministic, offline** evaluation harness that consumes:

- one governed **M20** `fixture_only` benchmark contract (v1 metrics: `accuracy`, `macro_f1`, `fallback_rate`, `example_count`);
- one frozen **M27** `replay_imitation_baseline.json`;
- the matching **M26** `replay_training_dataset.json`;
- referenced **M14** bundle directories (exact set — no extras);

and emits **`learned_agent_evaluation.json`** and **`learned_agent_evaluation_report.json`** with an embedded **M20-compatible** scorecard. Held-out evaluation uses **`split == "test"`** only (governed M26 assignments).

---

## 2. Scope Definition

### In Scope

- Runtime contract `docs/runtime/learned_agent_evaluation_harness_v1.md`
- Product: `learned_agent_models.py`, `learned_agent_metrics.py`, `learned_agent_evaluation.py`, `emit_learned_agent_evaluation.py` under `starlab/evaluation/`; `replay_imitation_predictor.py` under `starlab/imitation/`; **`baseline_fit`** refactored to use the predictor
- In-process **M16 → M18** materialization via `replay_observation_materialization` (no replay parsing in M28 evaluation modules)
- CLI: `python -m starlab.evaluation.emit_learned_agent_evaluation`
- Fixtures `tests/fixtures/m28/`; tests `tests/test_learned_agent_evaluation.py` (E2E, failure paths, AST import guard)
- **M29** stub only (`M29_plan.md`, `M29_toolcalls.md`) — **no** M29 product code

### Out of Scope / Non-Claims

- Benchmark integrity, leaderboard validity, live SC2 execution, replay↔execution equivalence
- M23 tournament, M24 diagnostics, M25 evidence pack semantics
- Retraining, hierarchical agents, M29+ product surfaces
- **No** `starlab.replays`, `starlab.sc2`, or `s2protocol` in listed M28 `starlab/evaluation/` modules

---

## 3. Work Executed

- Implemented compatibility checks, test-split evaluation, metrics (accuracy, macro F1, fallback rate, example count), deterministic JSON emission, embedded scorecard with `subject_ref` = frozen baseline (`subject_kind` imitation).
- Recorded merge authority: [PR #34](https://github.com/m-cahill/starlab/pull/34); PR-head [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130); merge-boundary [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580).

---

## 4. Validation & Evidence

- **PR:** [#34](https://github.com/m-cahill/starlab/pull/34) — merged **2026-04-10T00:35:30Z** (UTC).
- **Final PR head:** `c7ca6e6be8fbd44e39357da82cca857eddbd8eb3`
- **Merge commit:** `1ef636524269ff77ac26ac37584d43b50e9fcbc6`
- **Authoritative PR-head CI:** [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) — success
- **Merge-boundary `main` CI:** [`24220357580`](https://github.com/m-cahill/starlab/actions/runs/24220357580) — success
- **502** pytest on authoritative PR-head CI; one pre-existing `s2protocol` deprecation warning in replay CLI tests (unchanged).

---

## 5. What Remains Not Proved

Benchmark integrity, live SC2 in CI as a product claim, replay↔execution equivalence, strong imitation quality beyond the explicit metrics and non-claims, M23–M25 evaluation-chain semantics for this harness.

---

## 6. Next Milestone

**M29** — Hierarchical Agent Interface Layer — **stub-only** until chartered; no M29 product code in M28.
