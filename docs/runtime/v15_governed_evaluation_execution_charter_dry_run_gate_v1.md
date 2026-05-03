# STARLAB runtime — V15-M57: Governed Evaluation Execution Charter / Dry-Run Gate v1

**Contract id:** `starlab.v15.governed_evaluation_execution_charter.v1`  
**Report contract id:** `starlab.v15.governed_evaluation_execution_charter_report.v1`  
**Profile id:** `starlab.v15.m57.governed_evaluation_execution_charter_dry_run_gate.v1`  
**Milestone:** `V15-M57`  
**Emitter:** `python -m starlab.v15.emit_v15_m57_governed_evaluation_execution_charter`  

**Runner:** _(none — emitter only.)_

## Purpose

**V15-M57** defines and validates a **governed evaluation execution charter / dry-run gate** for a **future** bounded candidate-adapter evaluation attempt. It consumes:

- **§V15-M56** as governance route authority (optional JSON; **notice** if absent, **block** if supplied but invalid).
- **V15-M57A-OP1** as operator evidence that the **M52A candidate-live adapter** path can run **live SC2** with replay saved — **watchability readiness only**, **not** benchmark competence.

**V15-M57 defines and validates a governed evaluation execution charter / dry-run gate only.** It does not execute evaluation, compute benchmark pass/fail, produce scorecard results, evaluate strength, promote checkpoints, invoke `torch.load`, load checkpoint blobs, run live SC2, run GPU inference, run XAI, run human-panel evaluation, release a showcase agent, authorize v2, or execute T2–T5.

**M57A-OP1 proved watchability adapter viability, not benchmark competence.**

## Canonical OP1 anchors (strict `operator_preflight` / `operator_declared`)

Operator-supplied sealed **M57A** / **M52A** JSON digests must match:

| Field | SHA-256 |
| --- | --- |
| `V15-M57A` watch session `artifact_sha256` | `1b2b8704743354540e8f389a847315aa2bd8c8ead47b63edd81cd91a61df430c` |
| `V15-M52A` adapter spike `artifact_sha256` | `7458f5c370be4b04465a2d4f9d85321b313c34ef0ab0e6d48124ff0dadd7fa47` |
| `replay_sha256` (from M57A `artifact_references`) | `c0d88e54cdbc7eed7df27ddfcb4ae7e1b642993287a7e75c83d755097fbd89fa` |

Mismatch → `blocked_m57a_op1_anchor_mismatch`, `blocked_m52a_op1_anchor_mismatch`, or `blocked_replay_anchor_mismatch`, as applicable.

## Candidate identity

Latest produced candidate checkpoint SHA-256 only: `7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90`.

Related public anchors: M54 package `bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6`; M53 run artifact `18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8`.

## M57A classification gate

Only **`candidate_live_visual_watch_completed`** is accepted for the “ready” path, with:

- `candidate_policy_control_confirmed` = **true**  
- `policy_source` = **`candidate_live_adapter`**  
- `live_sc2_invoked` = **true**  
- `replay_saved` = **true**  

**`scaffold_visual_watch_completed_not_candidate_policy`** → `blocked_m57a_scaffold_only_not_candidate_adapter` (or `blocked_m57a_not_candidate_live_watch_completed`).

## Seal verification

For `m57a-watch-session-json`, `m52a-adapter-json`, and optional `m56-readout-json`: recompute `artifact_sha256` as the SHA-256 of the canonical JSON body **without** the `artifact_sha256` field; must equal the embedded seal. Failure → `blocked_invalid_artifact_seal`.

**`match_execution_proof.json`:** optional; does **not** use M57-style seals; validate `artifact_hash` (64 hex), `final_status` = `ok`, `map_logical_key` includes `Waterfall`, and **optional** `action_count` consistency with M57A.

## Chartered evaluation scope (frozen)

- **Evaluation class:** `bounded_candidate_adapter_evaluation_smoke`  
- **Baseline:** `passive_or_scripted_baseline`  
- **Map:** `Maps/Waterfall.SC2Map` (single-map initial pool)  
- **Horizon:** `game_step` 8, `max_game_steps` 2048 (from M57A-OP1 observed default)  
- **Replay:** required for future execution milestone; raw replays **not** committed in M57  

**Allowed metrics (future):** live SC2 executed, replay saved, action / step / observation counts, adapter status, SC2 result metadata, refusal status.

**Forbidden in M57:** benchmark pass/fail, strength score, promotion decision, human-panel claim, v2 authorization.

## Primary artifacts

| File | Role |
| --- | --- |
| `v15_governed_evaluation_execution_charter.json` | Sealed charter (`artifact_sha256` over canonical body without that field). |
| `v15_governed_evaluation_execution_charter_report.json` | Report companion. |
| `v15_governed_evaluation_execution_charter_checklist.md` | Operator checklist (C0–C11). |
| `v15_m58_candidate_evaluation_dry_run_command.txt` | **PLANNED_NOT_EXECUTED** template for **V15-M58** (omitted when charter blocked). |

The charter JSON `dry_run_gate` includes `dry_run_command_status` = **`planned_not_executed`**, `m58_runner_exists_in_m57` = **false**, `execution_authorized_in_m57` = **false**.

## Profiles

| Profile | Behavior |
| --- | --- |
| `fixture_ci` | Deterministic synthesis; canonical OP1 digests as anchors; **no** `out/` reads; **no** `torch.load`; emits M58 command template. |
| `operator_preflight` | Strict seal + OP1 anchor validation on M57A + M52A; optional M56 + match proof. |
| `operator_declared` | Validates declared bindings + M57A file; rejects overclaims and private path leakage. |

## Route

`route_to_v15_m58_bounded_candidate_adapter_evaluation_execution_attempt` · `recommended_not_executed` · next **§V15-M58**.

## Strongest allowed claim

V15-M57 defines and validates a governed evaluation execution charter / dry-run gate for a future bounded candidate-adapter evaluation attempt, using the successful V15-M57A-OP1 candidate-live visual watch as evidence that the candidate adapter path can run live SC2. It does not execute evaluation or authorize benchmark/pass/promotion claims.

## Standing non-claims

No evaluation execution. No benchmark execution. No benchmark pass/fail. No scorecard results. No strength evaluation. No checkpoint promotion. No checkpoint rejection as a strength decision. No torch.load in M57. No checkpoint blob loading in M57. No live SC2 in M57. No GPU inference in M57. No XAI execution. No human-panel evaluation. No showcase release. No v2 authorization. No T2–T5 execution. No raw out/, replay, video, checkpoint, or private operator evidence committed.
