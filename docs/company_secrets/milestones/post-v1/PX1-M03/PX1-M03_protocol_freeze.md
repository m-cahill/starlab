# PX1-M03 — Protocol freeze (remediation evaluation)

**Authoritative public contract:** `docs/runtime/px1_candidate_strengthening_demo_readiness_v1.md`

**Deterministic artifacts (repo emitters):**

- `px1_demo_readiness_protocol.json` / `px1_demo_readiness_protocol_report.json`
- After reruns: `px1_demo_readiness_evidence.json` / `px1_demo_readiness_evidence_report.json`

**Frozen evaluation minima** (align with runtime doc — do not lower win thresholds vs PX1-M02 v2):

- `minimum_candidates_evaluated = 1`
- `minimum_distinct_opponent_profiles = 2`
- `minimum_matches_per_candidate_per_opponent_profile = 5`
- `minimum_total_live_matches_for_selected_candidate = 10`
- `minimum_selected_candidate_overall_win_rate = 0.60`
- `minimum_selected_candidate_win_count = 6`
- `minimum_replay_backed_wins_for_selected_candidate = 2`
- `minimum_watchable_wins_for_selected_candidate = 1`
- `minimum_evidence_completeness = complete`
- `required_runtime_mode = local_live_sc2`
- `allowed_continuity_invalidations = 0`

**Demo-readiness additions:** Evidence must show early action-family diversity, macro beyond worker spam, at least one movement/combat-related family, and honest declaration outcome.

**Rule:** **PX1-M04 does not open automatically** from PX1-M03 closeout.
