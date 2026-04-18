# PX1-M03 — Execution readiness checklist

Before authoritative remediation reruns (operator-local):

- [ ] Local SC2 install + maps discoverable (`discover_under_maps_dir` as in v2 fixtures)
- [ ] M43 run dir + M51 refit `rl_bootstrap_candidate_bundle.joblib` paths resolve
- [ ] Match configs: `tests/fixtures/px1_m02/match_opponent_profile_*_v2.json` include `burnysc2_policy`: `px1_m03_hybrid_v1`
- [ ] Emit protocol: `python -m starlab.sc2.emit_px1_demo_readiness_protocol --input <fixture> --output-dir <protocol_dir>`
- [ ] Commands documented in runtime doc / operator checklist
- [ ] Proof surfaces: `match_execution_proof.json` includes `live_action_tallies` + `live_action_behavior_summary` when hybrid runs

**Series root (suggested):** under `out/training_campaigns/px1_m01_full_run_2026_04_17_a/` with a new `px1_m03_*` folder (operator-chosen suffix).
