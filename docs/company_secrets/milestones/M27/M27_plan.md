# M27 Plan — Replay-Derived Imitation Baseline

**Milestone:** M27  
**Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof  
**Status:** **Complete** — merged to `main` ([PR #33](https://github.com/m-cahill/starlab/pull/33)); **M28** seeded as stub-only.

## Objective

Prove the **first deterministic, offline, replay-derived imitation baseline artifact** over the governed **M26** training dataset contract. M27 trains and emits **one narrow, transparent baseline model** plus a compact report, using only already-governed replay-side surfaces. It does **not** widen into benchmark claims, live SC2, hierarchy, or the broader evaluation semantics reserved for **M28**.

## Scope decisions (locked)

1. **One baseline family only:** `starlab.m27.model.observation_signature_majority_v1`
2. **Inputs:** one governed `replay_training_dataset.json` (M26) + governed **M14** bundle directories referenced by the dataset; no new replay parser or raw replay dependencies in M27 imitation modules.
3. **Materialization:** M14 bundle → **M16** canonical state → **M18** observation surface via **programmatic** pipeline calls (not CLI shell-outs).
4. **Train an artifact, not an evaluation framework:** internal split-agreement smoke metrics only in the report; **not** benchmark claims.
5. **M28 stub-only:** no learned-agent evaluation harness product code in M27.

## Deliverables

- Runtime contract: `docs/runtime/replay_imitation_baseline_v1.md`
- Product: `starlab/imitation/` — `baseline_models.py`, `baseline_features.py`, `baseline_fit.py`, `emit_replay_imitation_baseline.py`, `replay_observation_materialization.py` (materialization seam)
- Artifacts: `replay_imitation_baseline.json`, `replay_imitation_baseline_report.json`
- Fixtures: `tests/fixtures/m27/` (goldens; reuse `tests/fixtures/m14/` for upstream bundle inputs in tests)
- Tests: `tests/test_replay_imitation_baseline.py` (import guard, negatives, E2E M26→M27)
- Governance: `tests/test_governance.py` updates; ledger `docs/starlab.md` updates
- Closeout (post-merge): `M27_run1.md`, `M27_summary.md`, `M27_audit.md`

## Locked design

- **Feature policy:** `starlab.m27.feature.observation_signature_v1` (bucketed projection; see contract)
- **Tie-break:** lexicographic on label string for equal support counts
- **Fallback:** global majority label on training split
- **Forbidden imports** in new M27 imitation modules listed above: `starlab.replays`, `starlab.sc2`, `s2protocol`

## CLI

```text
python -m starlab.imitation.emit_replay_imitation_baseline \
  --dataset PATH \
  --bundle PATH \
  --output-dir OUT
```

## Definition of done

- Contract + code + tests + governance green (Ruff, Mypy, pytest, CI).
- Narrow claim preserved: trained baseline artifact only; explicit non-claims everywhere.

**Closeout (2026-04-09):** Authoritative PR-head CI [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847); merge-boundary `main` [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938); merge commit `49b45825b65e56deb5cf991c5f74889e3daf2f59`. `M27_run1.md`, `M27_summary.md`, `M27_audit.md` recorded; ledger `docs/starlab.md` updated; current milestone → **M28** (stub).
