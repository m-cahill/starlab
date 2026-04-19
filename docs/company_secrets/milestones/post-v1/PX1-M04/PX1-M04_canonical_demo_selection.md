# PX1-M04 — Canonical demo selection

**Status:** **Closed** with **PX1-M04** governance closeout — selection **unchanged** (packaging milestone — **not** new remediation).  
**Candidate id (unchanged):** `px1_m01_weighted_refit_rl_bootstrap_v1`  

---

## Authoritative PX1-M03 source

- **Evaluation series id:** `px1_m03_eval_post_watchable_capture_2026_04_19`
- **Series root (operator-local):**  
  `out/training_campaigns/px1_m01_full_run_2026_04_17_a/px1_m03_eval_series_post_watchable_capture_2026_04_19`
- **Declaration:** `demo_readiness_declaration.md` = **`demo-ready-candidate-selected`**

---

## Primary canonical winning run

| Field | Value |
| --- | --- |
| **Run directory label** | `scripted_01` |
| **`run_id`** (sealed JSON) | `3123a93de6b383612941625d758d4127198a3e37a1a8232c6622e819b7e9798a` |
| **`validation_run_sha256`** (sealed JSON) | `a2cd3d2f1ceeb69f55feeda591c737e69f8b1ff8fee02f04aaba98bb60f953ae` |
| **Opponent profile** | `px1_m02_opponent_scripted_style_v1` (first watchable win chronology in series driver) |
| **Sealed run JSON** | `…/runs/scripted_01/local_live_play_validation_run.json` |
| **Result** | `match_execution.sc2_game_result` = **Victory** |
| **Watchable** | Yes — non-null **`optional_media_registration`** on same run |
| **Replay file** | `…/runs/scripted_01/replay/validation.SC2Replay` (relative to run directory; basename **`validation.SC2Replay`** per sealed JSON `replay.replay_file`) |

**Rationale:** This run is the **designated watchable win** for the successful PX1-M03 series: it combines a **replay-backed victory** with **registered optional media** aligned to the operator-captured video used for governance (**`out/px1_m03_operator_watchable.mp4`** after registration cleanup). It is the clearest single traceable chain for demo packaging.

---

## Operator-captured video (canonical reference)

- **Path (operator-local):** `out/px1_m03_operator_watchable.mp4`
- **Role:** Optional media tied to the watchable winning run; content hash recorded in **`optional_media_registration`** inside the sealed run JSON (source of truth).

---

## Backup run (optional)

Not selected for PR1. Additional wins exist in the same series (e.g. heuristic profile); any future backup designation must be recorded here with rationale.

---

## Non-claims

- **Not** a claim of optimal strategy or maximum win rate.
- **Not** a substitute for **PX1-M03** remediation evidence — **PX1-M03** closed that chapter; **PX1-M04** only **packages** references.
