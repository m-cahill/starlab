# Industrial hidden rollout — operator guide (M50)

## Three surfaces

| Surface | When to use | What it proves |
| ------- | ----------- | -------------- |
| **Visible live validation** | Debugging wiring, qualitative review, short M44 runs | Integration with SC2 locally — **not** benchmark integrity |
| **Visible live tranche work** | Shakedown / tranche A–B style batches when you want to watch | Same as above at larger batch — **not** statistical significance by default |
| **Hidden rollout campaign execution** | Long unattended-style campaigns where pop-up SC2 is undesirable | Governed **execution artifacts**, locks, heartbeat — **not** true headless unless resolved and evidenced |

## Commands (compact)

- **M49 charter + standard preflight:**  
  `python -m starlab.training.emit_full_local_training_campaign_contract`  
  `python -m starlab.training.emit_full_local_training_campaign_preflight`

- **M50 execution preflight (extended):** runs with the campaign executor; writes `campaign_execution_preflight_receipt.json` at the campaign root when used from `execute_full_local_training_campaign`.

- **M50 campaign executor:**  
  `python -m starlab.training.execute_full_local_training_campaign --campaign-contract <path>`

See `docs/runtime/full_local_training_campaign_v1.md` and `docs/runtime/industrial_hidden_rollout_mode_v1.md` for paths and semantics.

## Stop and hygiene

- Drop a **`STOP_REQUEST`** file in `campaign_runs/<execution_id>/` to request graceful stop between phases.
- Do not run two executors against the same campaign output tree; PID lockfiles block overlapping use.

## Remaining proof targets (program default)

Benchmark integrity, replay↔execution equivalence, live SC2 in CI, and ladder/public performance remain **separate** milestones — M50 does not close them.
