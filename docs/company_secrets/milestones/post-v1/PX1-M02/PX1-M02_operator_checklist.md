# PX1-M02 — Operator checklist

## Before evaluation (after PR1 merge)

- [ ] Read **`docs/runtime/px1_play_quality_demo_candidate_selection_v1.md`**
- [ ] Confirm **local SC2** / **burnysc2** prerequisites (same posture as **PX1-M01**)
- [ ] Locate **PX1-M01** campaign tree; confirm **weighted refit** joblib path under `phases/optional_weighted_refit/updated_policy/`
- [ ] Emit or copy frozen **`px1_play_quality_protocol.json`** from **`tests/fixtures/px1_m02/protocol_input.json`** via `python -m starlab.sc2.emit_px1_play_quality_protocol`
- [ ] Record opponent profile match configs: `tests/fixtures/px1_m02/match_opponent_profile_scripted_style.json`, `…_heuristic_style.json`

## Evaluation series (local_live_sc2)

- [ ] For **each** opponent profile: run **≥5** M44-style matches per **candidate** with continuity invalidations **≤** protocol allowance
- [ ] Aggregate **≥10** total live matches for the selected path; capture **replay-backed** and **watchable** wins per protocol minima
- [ ] Do **not** treat offline metrics alone as decisive proof

## Artifacts

- [ ] **`px1_play_quality_evidence.json`** + report from observed results
- [ ] **`px1_play_quality_operator_note.md`**
- [ ] **`demo_candidate_selection_declaration.md`** — exactly **`candidate-selected`** or **`no-candidate-selected`**

## Honest closeout

- [ ] If thresholds not met: declare **`no-candidate-selected`**; **do not** open **PX1-M03** automatically
