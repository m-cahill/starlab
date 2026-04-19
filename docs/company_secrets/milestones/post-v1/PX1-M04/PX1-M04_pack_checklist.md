# PX1-M04 — Demo proof pack checklist

Use this list to verify the **governed demo proof pack** before closeout (PR2). Large files stay **operator-local** unless explicitly committed.

**Closeout:** All required items verified operator-locally before governance closeout merge — see **`PX1-M04_summary.md`**.

## References (required)

- [x] **Primary canonical run** documented in **`PX1-M04_canonical_demo_selection.md`** (run directory label + `run_id` / `validation_run_sha256` from sealed JSON).
- [x] **Replay** path resolvable from canonical run directory (`replay/validation.SC2Replay` per sealed JSON).
- [x] **Optional media:** path + `sha256` + `size_bytes` match **`local_live_play_validation_run.json`** for the designated watchable demo run (**`out/px1_m03_operator_watchable.mp4`**).
- [x] **PX1-M03 declaration** line **`demo-ready-candidate-selected`** in the authoritative series root.
- [x] **PX1-M03 evidence** JSON (`px1_demo_readiness_evidence.json`) + evaluation input path recorded in selection memo or pack freeze.

## Narrative (required)

- [x] **Proof boundaries** paragraph: what the demo shows / does not show (no ladder, no benchmark universality, no v2) — **`docs/runtime/px1_governed_demo_proof_pack_v1.md`** §5.
- [x] **Traceability** one-liner: **PX1-M03** series root and **`px1_m03_eval_post_watchable_capture_2026_04_19`** — selection memo §Authoritative PX1-M03 source.

## Optional

- [ ] Backup winning run (second label) if documented.
- [ ] Operator-readable summary paragraph for reviewers.

## Non-goals (confirm empty)

- [x] No new remediation PRs bundled as “PX1-M04.”
- [x] No **v2** / **PX1-M05** opening claims.
