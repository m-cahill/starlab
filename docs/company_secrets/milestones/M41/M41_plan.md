# M41 Plan — Replay-Imitation Training Pipeline v1

**Milestone:** M41  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Status:** In progress (implementation branch)

---

## Intent

Deliver the **first governed local-first replay-imitation training pipeline**: deterministic **`replay_imitation_training_run.json`** + **`replay_imitation_training_run_report.json`**, optional **local-only** `joblib` weights referenced by hash, binding to **M40** via `training_program_contract_version` + `training_program_contract_sha256`. Implementation: **`starlab.imitation`** (sklearn logistic regression on M27 `context_signature` one-hot features). **Not** benchmark integrity, **not** live SC2 in CI, **not** GPU training in CI.

---

## Locked defaults (implementation)

- **Dependency:** `scikit-learn` (pinned in `pyproject.toml`).
- **Model:** `LogisticRegression` (CPU, deterministic seed).
- **Features:** M27 `build_context_signature` seam → parse → one-hot (`DictVectorizer`); fixed feature names in `feature_schema`.
- **Run ID:** deterministic hash from identity payload; optional `--run-id` override.
- **Weights:** `joblib` sidecar under `weights/`; not in repo.

---

## Slices

- **A:** Artifact contract — runtime `docs/runtime/replay_imitation_training_pipeline_v1.md`.
- **B:** Pipeline modules — `replay_imitation_training_models.py`, `replay_imitation_training_io.py`, `replay_imitation_training_pipeline.py`, `emit_replay_imitation_training_run.py`.
- **C:** CI — `tests/test_m41_replay_imitation_training_pipeline.py` (fixture path; no weights in repo).
- **D:** Ledger — `docs/starlab.md` on-branch charter (no §18 merge evidence until closeout).

---

## Out of scope

M42–M45 product work, benchmark-integrity upgrades, public weights, ladder claims.

---

## Acceptance

See user-facing milestone spec; closeout: `M41_summary.md`, `M41_audit.md`, tag `v0.0.41-m41` after merge to `main`.
