# V15-M52A — Candidate live adapter spike v1 (`starlab.v15.candidate_live_adapter_spike.v1`)

**Milestone slice:** `V15-M52A` — *Candidate-to-Live Policy Adapter Spike*  
**Profile surface:** `starlab.v15.m52a.candidate_to_live_policy_adapter_spike.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m52_candidate_live_adapter_spike`  
**Operator runner:** `python -m starlab.v15.run_v15_m52_candidate_live_adapter_spike`

## Purpose

Bind **sealed V15-M51** live candidate watchability harness JSON and attempt the **smallest honest** bridge from an **operator-declared candidate checkpoint** into a **bounded** live StarCraft II loop using a **minimal safe action vocabulary**. This answers whether the checkpoint can be **loaded and connected** for **watchability**, not whether the agent is strong.

V15-M52A is a candidate-to-live policy adapter spike for watchability only. It is not benchmark execution, not benchmark pass/fail, not strength evaluation, not checkpoint promotion, and not the 12-hour run.

## Inputs

| Input | Role |
| --- | --- |
| Sealed **M51** `v15_live_candidate_watchability_harness.json` | Required upstream; must recommend `route_to_12_hour_blocker_discovery_launch_rehearsal` with `recommended_not_executed`. |
| Optional `--expected-m51-watchability-sha256` | Mismatch → `refused_m51_sha_mismatch`. |
| Optional enrichment | M39/M42/M41/M33 paths (best-effort parse where wired). |

**Operator adapter spike** additionally requires: checkpoint path, expected checkpoint SHA256, SC2 root, map path, dual guards (`--allow-operator-local-execution`, `--authorize-candidate-live-adapter-spike`).

## Profiles

| Profile | Behavior |
| --- | --- |
| `fixture_ci` | Builds M51 fixture subtree, emits M52A JSON/report/brief. **No** `torch.load`, **no** live SC2. Status: `fixture_schema_only_no_candidate_adapter_execution`. |
| `operator_preflight` | Validates M51 seal, route, honesty; optional checkpoint / SC2 / map presence hints. |
| `operator_declared` | Declared envelope with embedded sealed M51. |
| `operator_local_adapter_spike` | **Runner only:** may `torch.load` **only** with dual guards and SHA verification; live BurnySC2 with policy `v15_m52a_candidate_projection_spike_policy_v1`. |

## Output artifacts

| File | Role |
| --- | --- |
| `v15_candidate_live_adapter_spike.json` | Sealed primary (`artifact_sha256`). |
| `v15_candidate_live_adapter_spike_report.json` | Report companion. |
| `v15_candidate_live_adapter_spike_brief.md` | Brief + non-claims. |

Optional under `candidate_live_adapter_watch/` after a live run: `match_execution_proof.json`, `replay/`, `operator_watch_note.md`.

## Contract identifiers

- `starlab.v15.candidate_live_adapter_spike.v1`
- `starlab.v15.m52a.candidate_to_live_policy_adapter_spike.v1`

## Action vocabulary (eight)

```text
no_op
select_idle_worker
build_worker
build_supply_depot
build_barracks
train_marine
move_camera_or_army
scout_enemy_start
```

## Projection model

```text
candidate_output_projection = provisional_safe_action_projection_v1
```

A deterministic projection derives a step-wise action index from checkpoint tensor fingerprints combined with coarse game-state scalars. It is **not** a full policy interpretation.

## Adapter labels

Distinctions:

```text
real_candidate_live_adapter_spike
scaffold_watchability_policy_not_candidate
candidate_live_adapter_blocked
fixture_no_live_adapter
```

## Torch / checkpoint guardrails

- Fixture / emitter default paths: **no** `torch.load`.
- Runner invokes `torch.load` **only** with:
  - `--allow-operator-local-execution`
  - `--authorize-candidate-live-adapter-spike`
  - On-disk SHA256 matching `--expected-candidate-checkpoint-sha256`
- Failures are recorded as `refused_candidate_model_load_failed` (or blocked statuses), never as benchmark or promotion outcomes.

## Live SC2 guardrails

- Uses the existing **BurnySC2** harness with **passive** second bot (watchability posture).
- Bounded `game_step` / `max_game_steps`; optional replay save.
- SC2 and map paths are operator-supplied; **do not** commit private absolute paths to public artifacts.

## Relationship to M51

M51 may run a **scaffold** policy labeled `scaffold_watchability_policy_not_candidate`. M52A is the **separate**, explicitly labeled **candidate** adapter path. Do not confuse scaffold watchability with candidate checkpoint behavior.

## Relationship to M52B / M53

- **M52B** rehearses the **twelve-hour launch** package (this document’s `route_recommendation` remains advisory, `recommended_not_executed`).
- **M53** may perform the actual **twelve-hour operator run attempt** if separately authorized.

## Non-claims

The JSON `non_claims` field enumerates refusal to treat this spike as benchmark pass/fail, strength, promotion, XAI, human-panel, showcase, **v2**, **T2–T5**, or the **12-hour run**.

## Forbidden flags (deterministic refusal)

Includes `--claim-benchmark-pass`, `--claim-strength`, `--promote-checkpoint`, `--run-benchmark`, `--run-xai`, `--run-human-panel`, `--release-showcase`, `--authorize-v2`, `--execute-t2` … `--execute-t5`, `--execute-12-hour-run`.

---

**Reference (operator-local, not hardcoded in repo):** an example known-good M39 final 2-hour candidate digest is `51cea94ed5324087863b246b7b31a21021eba286924aea4609aa09466430a943` when that lineage is locally available; always pass path + expected SHA via CLI.
