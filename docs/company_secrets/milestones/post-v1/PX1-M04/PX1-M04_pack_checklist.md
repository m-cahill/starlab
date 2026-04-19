# PX1-M04 — Demo proof pack checklist

Use this list to verify the **governed demo proof pack** before closeout (PR2). Large files stay **operator-local** unless explicitly committed.

## References (required)

- [ ] **Primary canonical run** documented in **`PX1-M04_canonical_demo_selection.md`** (run directory label + `run_id` / `validation_run_sha256` from sealed JSON).
- [ ] **Replay** path resolvable from canonical run directory (e.g. `px1_m03_validation.SC2Replay` or equivalent).
- [ ] **Optional media:** path + `sha256` + `size_bytes` match **`local_live_play_validation_run.json`** for the designated watchable demo run (e.g. **`out/px1_m03_operator_watchable.mp4`**).
- [ ] **PX1-M03 declaration** line **`demo-ready-candidate-selected`** in the authoritative series root.
- [ ] **PX1-M03 evidence** JSON (`px1_demo_readiness_evidence.json`) + evaluation input path recorded in selection memo or pack freeze.

## Narrative (required)

- [ ] **Proof boundaries** paragraph: what the demo shows / does not show (no ladder, no benchmark universality, no v2).
- [ ] **Traceability** one-liner: which **PX1-M03** series root and **evaluation_series_id**.

## Optional

- [ ] Backup winning run (second label) if documented.
- [ ] Operator-readable summary paragraph for reviewers.

## Non-goals (confirm empty)

- [ ] No new remediation PRs bundled as “PX1-M04.”
- [ ] No **v2** / **PX1-M05** opening claims.
