# Milestone Summary — M30: First Learned Hierarchical Agent

**Project:** STARLAB  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Milestone:** M30 — First Learned Hierarchical Agent  
**Timeframe:** 2026-04-10 (merge)  
**Status:** **Closed on `main`** ([PR #36](https://github.com/m-cahill/starlab/pull/36); merge commit `1c3a5f63f0ac5f380d3fd1ffcab66ca0d7d422bf`; **authoritative PR-head** [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664); **merge-boundary `main`** [`24223976390`](https://github.com/m-cahill/starlab/actions/runs/24223976390))

## 1. What M30 proved

M30 proves the **first deterministic, offline, replay-derived learned hierarchical imitation agent** in STARLAB:

* **Manager:** majority delegate per bounded observation **context signature** (training split).
* **Worker:** majority coarse semantic label per **(delegate, signature)** (training split).
* **Delegate partition:** fixed checked-in policy **`starlab.m30.delegate.fixed_four_v1`** — exactly four delegates (`economy`, `production`, `combat`, `information`); **not** learned from data.
* **Traces:** emitted documents use **`schema_version`** = `starlab.hierarchical_agent_interface_trace.v1` and validate against the **M29** hierarchical interface JSON Schema.
* **Report:** includes **`governed_asset_classes`** distinguishing code, dataset (hashed M26), replays (M14 bundles), derived labels, and delegate policy; **split agreement metrics** are **internal smoke only**, not benchmark claims.

**Fixture honesty:** the stock **M26** CI fixture predominantly exercises **production** and **information** delegates in training data; **economy** and **combat** delegates are still represented in the fixed mapping and in fallback / proof-trace paths — see tests and `select_proof_trace_examples` (unseen signature trace).

## 2. Primary artifacts

| Artifact | Role |
| -------- | ---- |
| `replay_hierarchical_imitation_agent.json` | Frozen agent: `agent_version` `starlab.replay_hierarchical_imitation_agent.v1`, tables, fallbacks, policy ids, non-claims |
| `replay_hierarchical_imitation_agent_report.json` | Counts, split metrics (smoke), `governed_asset_classes`, `report_version` `starlab.replay_hierarchical_imitation_agent_report.v1` |

## 3. Exact inputs

* Governed **M26** `replay_training_dataset.json` (fixture: `tests/fixtures/m26/…`).
* Referenced **M14** bundle directories (materialization path).
* **M16 → M18** observation materialization seam (`starlab.imitation.replay_observation_materialization`).
* **M27** feature policy **`starlab.m27.feature.observation_signature_v1`** (context signatures).
* Fixed **M30** delegate policy **`starlab.m30.delegate.fixed_four_v1`** (`starlab/hierarchy/delegate_policy.py`).

## 4. Explicit non-claims

* **No** benchmark integrity or leaderboard validity.
* **No** live StarCraft II execution in CI (fixture-driven only).
* **No** raw SC2 action legality or legality masks.
* **No** replay↔execution equivalence.
* **No** M31 replay explorer / operator evidence surface (reserved for **M31**).
* **No** flagship proof-pack semantics (**M32**).
* **No** M31 product code in this milestone.

## 5. Delivered (implementation)

* `docs/runtime/replay_hierarchical_imitation_agent_v1.md`
* `starlab/hierarchy/delegate_policy.py`, `hierarchical_agent_models.py`, `hierarchical_agent_fit.py`, `hierarchical_agent_predictor.py`, `emit_replay_hierarchical_imitation_agent.py`
* `tests/fixtures/m30/`, `tests/test_replay_hierarchical_imitation_agent.py`

## 6. Next milestone

**M31** — Replay Explorer / Operator Evidence Surface — **stub-only** (`M31_plan.md`, `M31_toolcalls.md`) until chartered; **no** M31 product code at M30 closeout.

---

*Summary aligned with milestone closeout practice; CI evidence cross-checked with `M30_run1.md` and ledger §18 / §23.*
