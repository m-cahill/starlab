# V15-M58 — Bounded Candidate Adapter Evaluation Execution Attempt (v1 runtime)

## Purpose

This milestone consumes the **V15-M57 governed evaluation execution charter**
(`starlab.v15.governed_evaluation_execution_charter.v1`; artifact
`v15_governed_evaluation_execution_charter.json`) and executes a tightly bounded,
governed **candidate-live adapter** evaluation-smoke path.

V15-M58 is a bounded candidate-adapter evaluation execution attempt. It may execute live SC2
only under explicit operator guards, using the **M52A** candidate-live adapter path and the latest
candidate checkpoint. It does not compute benchmark pass/fail, produce scorecard results, evaluate
strength, or promote the checkpoint.

## Contract identifiers

```text
starlab.v15.bounded_candidate_adapter_evaluation_execution.v1
starlab.v15.bounded_candidate_adapter_evaluation_execution_report.v1
starlab.v15.m58.bounded_candidate_adapter_evaluation_execution_attempt.v1
```

## Emitters / runners

```text
python -m starlab.v15.emit_v15_m58_bounded_candidate_adapter_evaluation_execution
python -m starlab.v15.run_v15_m58_bounded_candidate_adapter_evaluation_execution_attempt
```

## Anchors (public ledger)

Upstream M57 merge anchor and M57A-OP1 evidence digests remain as recorded in **`docs/starlab-v1.5.md`**.
Latest candidate checkpoint SHA (not promoted):

```text
7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90
```

## Delegation posture

Operator-local execution **subprocess delegates** to
`starlab.v15.run_v15_m52_candidate_live_adapter_spike` with dual M52A guards intact. The M58 emitter
CLI does **not** run SC2 or invoke `torch.load`.

## Guards (operator-local execution)

Dual guards:

```text
--allow-operator-local-execution
--authorize-bounded-candidate-adapter-evaluation
```

## Baseline / map / horizon

* Baseline classes: **`passive_or_scripted_baseline`** or **`burnysc2_passive_bot`** normalize to **`burnysc2_passive_bot`**.
* Map: **`Maps/Waterfall.SC2Map`** (Waterfall filesystem path checked for `Waterfall` in name on preflight).
* Horizon initial: **`game_step=8`**, **`max_game_steps=2048`**, **`attempt_count`**: 1 default, max 3.

## Replay policy

Replay save is required for operator-local bounded execution (`--save-replay`).

## Allowed metrics only

Completion / refusal, replay SHA (local), adapter status, bounded action / observation /
SC2-completion metadata emitted by M52A. No benchmark ladder, strength, promotion, showcase, v2, or **T2–T5**.

## Route to V15-M59

M59 consumes **bounded-only** receipts; no benchmark-pass/fail is derived here unless separately chartered:

```text
route_to_v15_m59_evaluation_readout_benchmark_pass_fail_refusal_or_threshold_decision — recommended_not_executed
```

## Public/private boundary

Transcript under `out/` is local-only (`v15_m58_operator_transcript.txt`). Raw replays,
checkpoints, and private operator surfaces are never merge-gated or committed artifacts.
