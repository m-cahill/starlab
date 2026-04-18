# PX1-M02 — Protocol freeze (private mirror)

**Authoritative public narrative:** `docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`  
**Authoritative machine freeze:** validated input → **`px1_play_quality_protocol.json`** + report (committed or operator-local per policy).

## Separation of concerns (locked)

1. **Candidate pool** — Coherent policy artifacts from **PX1-M01** only. **Primary:** `optional_weighted_refit/updated_policy/rl_bootstrap_candidate_bundle.joblib` under `campaign_runs/px1_m01_exec_001/`. **One** coherent candidate is **acceptable**; document plainly if there is no second comparable surface.
2. **Opponent profiles** — Two bounded profiles: **`px1_m02_opponent_scripted_style_v1`** and **`px1_m02_opponent_heuristic_style_v1`**, each with a frozen repo-relative **`match_config`** JSON (`tests/fixtures/px1_m02/…`). Labels are **methodological** (bounded harness series), **not** ladder equivalence.
3. **Selection rule** — As in runtime doc and `frozen_parameters.selection_rule` in protocol JSON.

## Frozen parameters (numeric)

| Key | Value |
| --- | ---: |
| minimum_candidates_evaluated | 1 |
| preferred_candidates_evaluated | 2 |
| minimum_distinct_opponent_profiles | 2 |
| minimum_matches_per_candidate_per_opponent_profile | 5 |
| minimum_total_live_matches_for_selected_candidate | 10 |
| minimum_selected_candidate_overall_win_rate | 0.60 |
| minimum_selected_candidate_win_count | 6 |
| minimum_replay_backed_wins_for_selected_candidate | 2 |
| minimum_watchable_wins_for_selected_candidate | 1 |
| minimum_evidence_completeness | complete |
| required_runtime_mode | local_live_sc2 |
| allowed_continuity_invalidations | 0 |

## PX1-M01 anchor

- `campaign_id` = `px1_m01_full_run_2026_04_17_a`
- `execution_id` = `px1_m01_exec_001`

## Non-claims

See protocol JSON `non_claims` array and runtime doc §10.
