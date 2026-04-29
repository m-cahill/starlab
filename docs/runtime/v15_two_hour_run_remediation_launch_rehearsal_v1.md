# V15-M38 — Two-hour run remediation & launch rehearsal (`starlab.v15.two_hour_run_remediation_launch_rehearsal.v1`)

## Governance status

Milestone **implementation** on branch `v15-m38-two-hour-run-remediation-launch-rehearsal`. Merge commit and authoritative GitHub Actions run IDs are recorded at closeout in `docs/starlab-v1.5.md` and `docs/starlab.md`.

## Purpose

**V15-M38 does not execute the 2-hour run.** It remediates or defers material **V15-M37** blockers, freezes a governed **V15-M39** launch command and runbook, and may perform a **short bounded rehearsal** (filesystem / `nvidia-smi` probe only) when dual-guarded.

## Contract / profile

- **Contract:** `starlab.v15.two_hour_run_remediation_launch_rehearsal.v1`
- **Profile:** `starlab.v15.m38.two_hour_run_remediation_launch_rehearsal.v1`
- **Emitter:** `python -m starlab.v15.emit_v15_m38_two_hour_run_remediation_launch_rehearsal`

## Modes

### 1. `fixture_ci` (`--fixture-ci`)

- Emits schema-only remediation/rehearsal artifacts.
- **`rehearsal_status`:** `fixture_schema_only_no_operator_rehearsal`
- No operator inputs.

### 2. `operator_preflight` (`--profile operator_preflight`)

- **Required:** `--m37-blocker-discovery-json` (sealed M37 JSON).
- **Optional:** `--m37-remediation-map`, `--m37-m39-runbook-draft` (Markdown helpers; weak authority vs sealed JSON).
- Validates seals, classifies blocker resolutions, sets **`m39_launch_ready`** when gates pass.

### 3. `operator_local_rehearsal` (`--profile operator_local_rehearsal`)

- **Requires:** `--allow-operator-local-execution` and `--authorize-m39-launch-rehearsal`
- **Optional:** `--max-rehearsal-seconds` (default 60)
- Bounded scratch write + optional `nvidia-smi -L`; **not** training and **not** SC2.

## Inputs / outputs

**Outputs (all modes write six paths):**

- `v15_two_hour_run_remediation_launch_rehearsal.json`
- `v15_two_hour_run_remediation_launch_rehearsal_report.json`
- `v15_two_hour_run_remediation_launch_rehearsal_checklist.md`
- `v15_m39_launch_runbook.md`
- `v15_m39_launch_command.txt`
- `v15_m39_operator_stop_resume_card.md`

## Relationship to M37 / M39

- **M37:** blocker discovery / readiness audit only.
- **M38:** remediation summary + launch freeze + optional rehearsal.
- **M39:** future operator **7200-second** attempt; **not** executed in M38.

## Checkpoint cadence remediation (code-level)

The **M28** path delegates training to `starlab.v15.sc2_backed_t1_training_execution.run_bounded_rollout_feature_training`, which enforces:

- **`--checkpoint-cadence-updates`** — interval between persisted checkpoints.
- **`--max-retained-checkpoints`** — on-disk cap (prune intermediates; keep first + last semantics via pruning policy).
- **Final-step** checkpoint when the last update is not on a cadence boundary.
- Telemetry: **`checkpoints_written_total`**, **`checkpoints_pruned_total`**, **`checkpoint_retention_max_retained`**.

Default cap may be overridden with **`STARLAB_MAX_RETAINED_CHECKPOINTS`**. **M29** forwards **`--max-retained-checkpoints`** into **M28** when used.

## Telemetry plan

Operator should pair transcript logs with periodic **`nvidia-smi`** samples. M38 JSON includes a **`telemetry_plan`** stub; the frozen launch command points at **`out/v15_m39_2hour_operator_run/<run_id>/`**.

## Stop / resume card

See emitted **`v15_m39_operator_stop_resume_card.md`**. M28 does not define automatic resume; partial runs should be classified explicitly.

## Public / private boundary

Do not commit **`out/`**, **`docs/company_secrets/`**, weights, or private paths. Artifacts must pass STARLAB path-pattern hygiene checks.

## Non-claims

Fixture and honest public paths keep **`claim_flags`** false for: two-hour execution, benchmark pass, strength evaluation, checkpoint promotion, scorecard results, XAI, human-panel, showcase, **v2**, **T2/T3**.

## CLI examples

Fixture CI:

```powershell
python -m starlab.v15.emit_v15_m38_two_hour_run_remediation_launch_rehearsal `
  --fixture-ci `
  --output-dir out/v15_m38_fixture
```

Operator preflight:

```powershell
python -m starlab.v15.emit_v15_m38_two_hour_run_remediation_launch_rehearsal `
  --profile operator_preflight `
  --m37-blocker-discovery-json path\to\v15_two_hour_run_blocker_discovery.json `
  --output-dir out/v15_m38_preflight
```

## Suggested statuses

- `fixture_schema_only_no_operator_rehearsal`
- `launch_rehearsal_blocked_missing_m37_audit`
- `launch_rehearsal_blocked_open_critical_blockers`
- `launch_rehearsal_blocked_checkpoint_cadence_unresolved`
- `launch_rehearsal_blocked_runner_7200s_incompatible`
- `launch_rehearsal_blocked_storage_or_output_policy`
- `launch_rehearsal_completed_with_deferred_noncritical_items`
- `launch_rehearsal_completed_ready_for_m39`
