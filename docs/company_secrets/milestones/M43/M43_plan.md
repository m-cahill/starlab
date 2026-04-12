# M43 Plan — Hierarchical Training Pipeline v1

**Milestone:** M43  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Status:** In progress — implementation on branch (see `docs/starlab.md` §7 / §11).

## Objective

Deliver the first **governed, local-first hierarchical training pipeline**: deterministic `hierarchical_training_run.json` / `hierarchical_training_run_report.json` under `out/hierarchical_training_runs/<run_id>/`, optional combined `joblib` weights sidecar, M40 contract binding, M29 interface trace schema reference, M30 fixed four-delegate policy, manager + worker **LogisticRegression** (M41-aligned), **delegate_coverage** per delegate, fixture-only CI tests — **without** benchmark-integrity claims, live SC2 in CI, M42 comparison wiring, M44 live-play, or M45 RL.

## Deliverables (tracked)

- `docs/runtime/hierarchical_training_pipeline_v1.md`
- `starlab/hierarchy/hierarchical_training_models.py`, `hierarchical_training_io.py`, `hierarchical_training_pipeline.py`, `emit_hierarchical_training_run.py`
- `tests/test_m43_hierarchical_training_pipeline.py`
- `docs/starlab.md` updates (charter, tables, Start Here, Phase VI)
- `.gitignore`: `out/hierarchical_training_runs/`
- README / `docs/architecture.md` alignment where needed

## Out of scope

Benchmark integrity, replay↔execution equivalence, live SC2 in CI, M42 comparison integration, M44–M45 product work, committed weights, hierarchy depth beyond two levels / adaptive routing.

## Closeout (later)

PR merge to `main`, `M43_summary.md` / `M43_audit.md`, tag `v0.0.43-m43`, authoritative CI recording per project workflow.
