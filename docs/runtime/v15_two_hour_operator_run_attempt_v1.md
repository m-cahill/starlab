# V15-M39 — 2-hour operator run attempt (`starlab.v15.two_hour_operator_run_attempt.v1`)

## Governance status

Milestone **implementation surface** (Phase A): fixture CI, operator preflight, sealed receipt vocabulary, and runtime documentation on `main` following merge of the M39 PR. **7200-second operator execution** is **not** part of merge-gate CI and runs only post-merge when operator policy and **M38** **`m39_launch_ready`** gated artifacts allow.

**Required public wording:** V15-M39 may execute the **7200-second** operator-local run only under explicit operator guards (**`--allow-operator-local-execution`** and **`--authorize-2hour-operator-run`** on the runner). A completed M39 run is **execution evidence**, not benchmark pass, strength evaluation, checkpoint promotion, scorecard result, XAI, human-panel, showcase release, **v2** authorization, or **T2**/**T3** authorization.

## Purpose

Provide a governed receipt surface for the operator-local **7200-second** SC2-backed **M28** T1 continuation / candidate-training attempt using the **V15-M38** frozen launch command/runbook, checkpoint retention/cadence posture, transcript capture, checkpoint inventory, and honest outcome classification.

## Contract / profile

- **Contract:** `starlab.v15.two_hour_operator_run_attempt.v1`
- **Profile:** `starlab.v15.m39.two_hour_operator_run_attempt.v1`
- **Emitter:** `python -m starlab.v15.emit_v15_m39_two_hour_operator_run_attempt`
- **Runner (operator-only):** `python -m starlab.v15.run_v15_m39_two_hour_operator_run_attempt`

## Modes

### 1. `fixture_ci` (`--fixture-ci`)

- Emits schema-only artifacts for CI and governance tests.
- **`run_status`:** `fixture_schema_only_no_operator_run`
- **`two_hour_run_executed`:** `false` — **`two_hour_run_completed`:** `false`

### 2. `operator_preflight` (`--profile operator_preflight`)

- Validates sealed **`v15_two_hour_run_remediation_launch_rehearsal.json`**, **`m39_launch_ready`**, and frozen **`v15_m39_launch_command.txt`** (7200s / 120 min horizon, retention flag, `out/.../v15_m39_2hour_operator_run/` root, venv hint).
- By default probes **CUDA** (via **PyTorch**) and **`sc2`** import; use **`--skip-cuda-sc2-probes`** only in constrained environments (e.g. tests).
- Does **not** start the 2-hour subprocess.

### 3. Operator run (`run_v15_m39_two_hour_operator_run_attempt`)

- Requires dual guards and passing preflight.
- Executes the frozen launch file via **`cmd.exe /C`** from the repository root; streams **`v15_m39_operator_transcript.txt`** (path-like segments redacted for public bundle hygiene).
- Post-run: **`v15_two_hour_operator_run_attempt.json`**, report, checklist, **`v15_m39_telemetry_summary.json`**, **`v15_m39_checkpoint_inventory.json`**.

## Preflight gates (selected)

| Gate | Intent |
| --- | --- |
| Sealed **M38** JSON | Contract + canonical seal + **`m39_launch_ready`** |
| Launch command | Retention / wall-clock / output root / venv hints |
| Expected candidate SHA | Must match the public lineage anchor (**`eac6fc1f…`**) |
| Disk / writable output | Minimum free space policy (operator-tuned) |
| CUDA / SC2 | Optional skips for tests; real attempts should probe |

## Operator launch sequence (summary)

1. Locate or emit **M38** bundle (`v15_two_hour_run_remediation_launch_rehearsal.json`, `v15_m39_launch_command.txt`, runbook, stop/resume card).
2. **`emit_v15_m39_two_hour_operator_run_attempt --profile operator_preflight ...`**
3. If **`operator_preflight_ready_for_2hour_attempt`**, run **`run_v15_m39_two_hour_operator_run_attempt`** with dual guards and frozen paths (Phase B — post-merge).

## Output artifacts

- `v15_two_hour_operator_run_attempt.json` (sealed)
- `v15_two_hour_operator_run_attempt_report.json`
- `v15_two_hour_operator_run_attempt_checklist.md`
- `v15_m39_operator_transcript.txt`
- `v15_m39_telemetry_summary.json`
- `v15_m39_checkpoint_inventory.json`

## Checkpoint retention expectations

Training uses **M28** **`--max-retained-checkpoints`** / **`STARLAB_MAX_RETAINED_CHECKPOINTS`**, cadence flags, pruning telemetry, and final-step persistence (**`sc2_backed_t1_training_execution`**). Receipts should record retention counters when **M28** JSON is discoverable under the output tree.

## Outcome classifications (honest vocabulary)

Examples: **`two_hour_operator_run_completed_with_candidate_checkpoint`**, **`two_hour_operator_run_completed_without_candidate_checkpoint`**, **`two_hour_operator_run_interrupted_partial_receipt`**, **`two_hour_operator_run_failed`**, **`two_hour_operator_run_blocked_preflight`**, plus preflight-only **`operator_preflight_*`** statuses — **not** benchmark or strength labels.

## Relationship to M38

**M38** freezes the launch command and rehearsal posture; **M39** may execute the long run and seal operator receipts. **M39** must not silently mutate the frozen command; deliberate deltas use **`--launch-command-delta-detected`**.

## Relationship to future M40

- **Success-path packaging:** **V15-M40** — *2-Hour Run Package & Evaluation Readiness*
- **Blocked/failed path:** **V15-M40** — *2-Hour Run Remediation / Retry Gate*

## Public/private boundary

Do not commit **`out/`**, weights, raw transcripts with uncleared absolute paths in public narratives, or **`docs/company_secrets/`** operator notes.

## Non-claims

Fixture and honest receipts keep **`non_claims`** aligned with: not benchmark pass, not strength evaluation, not checkpoint promotion, not scorecard results, not **T2**/**T3**, not XAI, human-panel, showcase, or **v2**.

## CLI examples

Fixture CI:

```powershell
python -m starlab.v15.emit_v15_m39_two_hour_operator_run_attempt `
  --fixture-ci `
  --output-dir out/v15_m39_fixture
```

Operator preflight:

```powershell
.\.venv\Scripts\python.exe -m starlab.v15.emit_v15_m39_two_hour_operator_run_attempt `
  --profile operator_preflight `
  --m38-launch-rehearsal-json <path-to-v15_two_hour_run_remediation_launch_rehearsal.json> `
  --m39-launch-command <path-to-v15_m39_launch_command.txt> `
  --expected-candidate-sha256 eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26 `
  --output-dir out/v15_m39_preflight/<run_id>
```

Runner (operator-only; not CI):

```powershell
.\.venv\Scripts\python.exe -m starlab.v15.run_v15_m39_two_hour_operator_run_attempt `
  --allow-operator-local-execution `
  --authorize-2hour-operator-run `
  --m38-launch-rehearsal-json <path> `
  --m39-launch-command <path> `
  --expected-candidate-sha256 eac6fc1f37aa958279a80209822765ecfa6aa2525ed64a8bee88c0ac2be13d26 `
  --target-wall-clock-seconds 7200 `
  --max-retained-checkpoints 256 `
  --output-dir out\v15_m39_2hour_operator_run\<run_id>
```
