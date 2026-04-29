# V15-M29 runtime — Full 30-Minute SC2-Backed T1 Candidate Run Gate

## Contract

- **`starlab.v15.full_30min_sc2_backed_t1_run.v1`**

Primary runner (wrapper): `python -m starlab.v15.run_v15_m29_full_30min_sc2_backed_t1_run`

This milestone **delegates** training execution to the **V15-M28** surface (`starlab.v15.sc2_backed_t1_candidate_training.v1`, `run_v15_m28_sc2_backed_t1_candidate_training`) with **opt-in** full-wall-clock flags (`--require-full-wall-clock`, `--disable-loss-floor-early-stop`, `--continue-after-checkpoint`, aligned `--max-wall-clock-minutes` / `--min-wall-clock-minutes`).

## Intent

- Prove **operator-local** execution of SC2 rollout–conditioned candidate training until the **configured wall-clock horizon** elapses (`observed_wall_clock_seconds`), or fail honestly with blocker receipts.
- **Default M28 semantics remain unchanged**: full-horizon behavior is introduced only via explicit CLI flags.

## Non-claims

- No strength benchmark pass, checkpoint promotion, XAI execution, human-panel execution, showcase release, **v2** authorization, T2/T3, or “beats most humans”.
- Candidate checkpoints (`*.pt`) are **hashed receipts only**, `not_promoted_candidate_only`.

## CI vs operator-local

- **`--fixture-only-m29`** (CI-safe) runs bounded M28 fixture wiring and emits paired M29 JSON without long wall-clock posture.

## Operator receipt (example bounded closeout)

When full-wall-clock training completes under the wrapper, expect (among other fields) aligned telemetry such as **`profile`:** **`operator_local_full_wall_clock`**, **`requested_min_wall_clock_seconds`:** **1800**, **`observed_wall_clock_seconds`** matching the requested horizon (within classifier tolerance), **`full_wall_clock_satisfied`:** **true**, **`sc2_backed_features_used`:** **true**, and sealed **`artifact_sha256`** values for the M29 JSON and the delegated M28 JSON in the same output directory. Detailed public record: **`docs/starlab-v1.5.md`** **§V15-M29**.