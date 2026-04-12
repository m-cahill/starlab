# M45 Plan — Self-Play / RL Bootstrap v1

**Milestone:** M45  
**Phase:** VI — Governed Agent Training, Comparison, and Local Validation  
**Branch:** `m45-self-play-rl-bootstrap-v1`  
**Status:** Complete (merged to `main`; see `M45_run1.md` / §18)

## Objective

Deliver the first governed **self-play / RL bootstrap** surface: consume an **M43** hierarchical candidate + local weights, reuse the **M44** harness for rollout collection, emit deterministic **`self_play_rl_bootstrap_run.json`** / **`self_play_rl_bootstrap_run_report.json`**, optionally perform one **conservative weighted re-fit** (sklearn, same family as M43), and write a **local-only** updated joblib bundle.

## Locked defaults

- **Primary package:** `starlab.training`
- **Runtime substrate:** `starlab.sc2` (M44)
- **Update:** single weighted re-fit; `starlab.m45.update.weighted_logistic_refit_v1`
- **Bootstrap mode:** single-candidate default; `mirror_self_play_local` not implemented in v1
- **Episodes:** CLI; default **1** (`fixture_stub_ci`), **5** (`local_live_sc2`)
- **Reward:** `starlab.m45.reward.validation_outcome_v1`

## Deliverables

- `docs/runtime/self_play_rl_bootstrap_v1.md`
- `starlab/training/` M45 modules + `emit_self_play_rl_bootstrap_run`
- `tests/test_m45_self_play_rl_bootstrap.py`
- Ledger / README / architecture updates
- `docs/diligence/phase_vi_integrated_test_campaign.md` (post‑M45 prep only)

## Non-claims

No benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder performance, repo weights, or full integrated campaign execution **as M45 proof**.
