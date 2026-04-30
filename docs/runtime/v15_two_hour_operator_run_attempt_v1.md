# V15-M39 — 2-hour operator run attempt (`starlab.v15.two_hour_operator_run_attempt.v1`)

## Governance status

**Phase A (merge-gate) — closed on `main`:** merge commit **`ada97dda5d32bc97541fa4a5386add8b4c241693`** merged **2026-04-30T00:03:14Z** UTC (GitHub **merge commit**). Authoritative GitHub Actions workflow **CI** runs: pull_request head **`e7ef910a9c13ad989e84978a1392073f60dd4e82`** ([`25140098888`](https://github.com/m-cahill/starlab/actions/runs/25140098888); superseded head **`0f9c6475c49d49ef7c4c74f0dfdcd91249246e0c`** — [`25139836736`](https://github.com/m-cahill/starlab/actions/runs/25139836736) — **failure**, coverage gate — **not** merge authority) and merge-boundary push on **`ada97dda…`** ([`25140243730`](https://github.com/m-cahill/starlab/actions/runs/25140243730)). Full PR links and ledger copy: **`docs/starlab-v1.5.md`** / **`docs/starlab.md`**.

**Operator run classification (Phase A):** **`operator_run_not_started_pending_post_merge_authorization`** — the governed **7200-second** operator-local run has **not** been executed; Phase A delivers fixture CI, **`operator_preflight`**, receipt vocabulary, and runtime/docs on `main` only.

**Phase B operator attempt (2026-04-30):** **`operator_preflight_blocked_missing_m38_rehearsal`** — Phase B stopped before **`emit_v15_m39`** **`operator_preflight`** when locating sealed **M38** launch inputs under the operator **`out/`** tree (and no sealed **`v15_two_hour_run_blocker_discovery.json`** to regenerate **M38**). **7200s** subprocess **not** started.

**V15-M40 remediation (operator-local, post–Phase B first attempt):** sealed **M37→M38→M39 preflight** chain **restored** using **real** upstream **M27/M28/M29/M34/M35** JSON on a CUDA/**SC2**-verified **`.venv`** — **`operator_preflight_ready_for_2hour_attempt`**. **7200s** run **not** executed in **M40** — public program posture **`m39_operator_preflight_ready_awaiting_7200s_launch_authorization`** (explicit dual-guard launch decision is **outside** **V15-M40**). **`V15-M40`** **governance** **closed** on `main` per **`docs/starlab-v1.5.md`** **§V15-M40** (merge **`7f16a9a9e996716babc6a7f579e11ecb096a9a72`**; merge-boundary **CI** **`25142983709`** — **success**).

**Next operator action (not executed in M40):** authorize **V15-M39** Phase B **`run_v15_m39_two_hour_operator_run_attempt`** with dual guards, using the **M40-regenerated** sealed **M38** launch bundle ( **`v15_two_hour_run_remediation_launch_rehearsal.json`**, **`v15_m39_launch_command.txt`**, companions) and **`operator_preflight_ready_for_2hour_attempt`** on that station.

**Required public wording:** V15-M39 **Phase A** does **not** execute the **2-hour** run. It does **not** claim benchmark pass, evaluate strength, promote checkpoints, produce scorecard results, execute **T2**/**T3**, run XAI or human-panel evaluation, release a showcase agent, or authorize **v2**. **Phase B** may execute the **7200-second** operator-local run only under explicit operator guards (**`--allow-operator-local-execution`** and **`--authorize-2hour-operator-run`** on the runner). A completed M39 run is **execution evidence**, not benchmark pass, strength evaluation, checkpoint promotion, scorecard result, XAI, human-panel, showcase release, **v2** authorization, or **T2**/**T3** authorization.

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
