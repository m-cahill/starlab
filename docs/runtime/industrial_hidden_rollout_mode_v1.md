# Industrial hidden rollout mode (M50)

**Contract version:** `starlab.industrial_hidden_rollout_mode.v1`  
**Ledger:** `docs/starlab.md`

## Role

M50 defines what **industrial-scale hidden rollout** means in STARLAB: a **non-intrusive / background-friendly** operator posture for long local campaigns, with **honest** reporting of what visibility was **requested** vs what was **actually resolved** on the host.

This is **not** a claim of true headless SC2 on every platform. On Windows especially, **hidden requested → minimized resolved** is a first-class, explicit outcome.

## Visibility modes (normative ordering)

From strongest to weakest:

1. `hidden` — SC2 is not meaningfully visible to the operator (platform-specific; rarely provable without extra evidence).
2. `minimized` — best-effort reduced intrusion (default honest resolution when true hidden is not demonstrated).
3. `visible_fallback` — normal visible execution.
4. `unsupported` — operator or runtime marked visibility as unsupported / invalid request.

## Honesty rules

- **requested_visibility_mode** and **resolved_visibility_mode** are both recorded on execution artifacts.
- **hidden_rollout_supported** is **true** only when the resolved posture is actually `hidden` **and** the mechanism is recorded; otherwise it is **false** even when the run is successful.
- **capability_warnings** must carry explicit downgrade explanations (no silent fallback).

## Relation to other milestones

- **M44 / M45:** Episode execution still uses the M44 harness and M45 bootstrap pipeline; M50 orchestrates and supervises, it does not replace rollout semantics.
- **M49:** Campaign **charter + preflight** remain authoritative for planning. M50 adds **execution** under `campaign_runs/<execution_id>/`.

## What M50 does not prove

- Benchmark integrity  
- Replay↔execution equivalence  
- Live SC2 in CI  
- Ladder / public performance  
- That long campaigns automatically yield strong policies  

## M51 extension (post-bootstrap protocol phases)

**Run version:** `hidden_rollout_campaign_run.json` uses **`starlab.hidden_rollout_campaign_run.v2`** when the executor records **M51** `phase_receipts`.

Optional flag: `--post-bootstrap-protocol-phases` on `python -m starlab.training.execute_full_local_training_campaign`.

**Execution order (strict):** follow `campaign_protocol.phases` in the M49 contract — typically: gate receipts only → `bootstrap_episodes` (always `emit_updated_bundle=False`) → `optional_weighted_refit` (aggregated refit) → `post_refit_m42_comparison` (orchestrated **skip** with `candidate_not_m41_comparison_compatible` until M41 candidates are explicitly bound — no M42 harness extension in M51) → `watchable_m44_validation` (one M44 on **refit** joblib if refit succeeded; **no** silent fallback to original M43 weights).

Per-phase **`phases/<phase_name>/phase_receipt.json`** (`starlab.campaign_phase_receipt.v1`) plus an aggregate `phase_receipts` list on the sealed hidden rollout run.

## References

- `docs/runtime/full_local_training_campaign_v1.md` — M49 campaign root layout  
- `docs/diligence/industrial_hidden_rollout_operator_guide.md` — operator-facing comparison of surfaces  
