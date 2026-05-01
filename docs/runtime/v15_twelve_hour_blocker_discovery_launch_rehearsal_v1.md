# V15-M52B — Twelve-hour blocker discovery / launch rehearsal v1 (`starlab.v15.twelve_hour_blocker_discovery_launch_rehearsal.v1`)

**Milestone slice:** `V15-M52B` — *12-Hour Blocker Discovery / Launch Rehearsal*  
**Profile surface:** `starlab.v15.m52.twelve_hour_blocker_discovery_launch_rehearsal.v1`  
**Emitter:** `python -m starlab.v15.emit_v15_m52_twelve_hour_launch_rehearsal`  
**Runner:** **None** for the 12-hour run — M52B must **not** execute a twelve-hour job.

## Purpose

Classify **readiness vs blockers** for a governed **twelve-hour operator attempt** (V15-M53): environment, SC2, map, candidate checkpoint, M52A adapter posture, **disk budget**, **checkpoint retention**, **stop/resume**, and **launch command** shape. Emit a **frozen** M53 command template, runbook, checklist, and stop/resume card.

V15-M52 rehearses and freezes the governed 12-hour operator-run path. It does not execute the 12-hour run; V15-M53 owns the 12-hour operator attempt.

## Inputs

| Input | Role |
| --- | --- |
| Sealed **M52A** `v15_candidate_live_adapter_spike.json` | Required for `operator_preflight` (path via `--m52a-adapter-spike-json`). |
| Optional `--expected-m52a-adapter-spike-sha256` | Mismatch → refusal. |
| Optional `--allow-m52a-adapter-blocked-planning` | Allows planning-style rehearsal when M52A ended blocked (warnings posture). |
| Optional M51 / candidate / SC2 / map / disk hints | Enrichment and local inspection only. |

## Profiles

| Profile | Behavior |
| --- | --- |
| `fixture_ci` | Emits all public artifacts; `disk_budget_status`: `fixture_not_inspected`. **No** 12-hour rehearsal execution. |
| `operator_preflight` | Validates M52A + inputs; may inspect disk when `--disk-root` is supplied. |
| `operator_declared` | JSON-only declared envelope (`sealed_m52a` or embedded path); no execution. |

## Output artifacts

| File | Role |
| --- | --- |
| `v15_twelve_hour_launch_rehearsal.json` | Sealed rehearsal summary. |
| `v15_twelve_hour_launch_rehearsal_report.json` | Report companion. |
| `v15_twelve_hour_launch_rehearsal_checklist.md` | Operator checklist. |
| `v15_m53_launch_command.txt` | **Frozen** M53 launch command (placeholders such as `<SC2_ROOT>`). |
| `v15_m53_launch_runbook.md` | Runbook (planning only). |
| `v15_m53_operator_stop_resume_card.md` | Stop/resume / corruption / escalation guidance. |

## Blocker domains

Classify issues under: `environment`, `sc2_runtime`, `map_pool`, `candidate_checkpoint`, `candidate_live_adapter`, `launch_command`, `disk_budget`, `checkpoint_retention`, `telemetry_capture`, `stop_resume`, `operator_authorization`, `public_private_boundary`.

Some blocker vocabulary in the sealed JSON models (`blocked_candidate_not_watchable`, `blocked_stop_resume_plan_missing`, `blocked_launch_command_not_frozen`, `blocked_public_private_boundary_risk`, and related codes) is **reserved** for future operator-local inspections and **may not** be emitted by `fixture_ci` or the current default preflight path. Fixture and CI receipts remain honest about what they actually evaluated.

## Disk budget

- CI fixture: `disk_budget_status = fixture_not_inspected`.
- Operator: when `--disk-root` is supplied, record free space vs estimated retained checkpoints and telemetry overhead; **warn** or **block** honestly. Do not leak private host absolute paths into public summaries beyond operator control of redaction.

## Non-claims

M52B does **not** execute the twelve-hour run; does **not** run benchmarks; does **not** evaluate strength; does **not** promote checkpoints; does **not** run XAI or human-panel; does **not** release showcase; does **not** authorize **v2**; does **not** execute **T2–T5**; does **not** claim candidate skill.

## Forbidden flags

Includes `--execute-12-hour-run` and the same claim/sideshow flags as sibling milestones — deterministic refusal receipts.

## Relationship to V15-M52A / M53

- **M52A** establishes candidate adapter watchability posture. M52B **consumes** sealed M52A JSON.
- **M53** executes or honestly blocks the governed twelve-hour operator attempt using the **frozen** command and plan from this rehearsal.

---

Ensure all documentation is updated as necessary when closing **V15-M52** (M52A + M52B as one milestone).
