# M50 Plan — Industrial-Scale Hidden Rollout Mode & Governed Campaign Execution v1

## Status

**Closed** on `main` (see `M50_run1.md` / §18).

## Phase

VI

## Milestone title

**M50 — Industrial-Scale Hidden Rollout Mode & Governed Campaign Execution v1**

## Why this milestone exists

STARLAB now has:

* M45 bootstrap
* M47 episode distinctness / operator interpretation
* M48 comparison contract-path alignment
* M49 full local campaign charter + preflight

Operator-local evidence has already shown that the visible `local_live_sc2` path can run real shakedown and tranche-style live bootstrap campaigns, but that visible pop-up execution is not a good default posture for truly large runs.

M50 should turn that into an honest, governed **industrial-scale hidden rollout** surface.

This milestone is **not** trying to solve:

* benchmark integrity
* replay↔execution equivalence
* live SC2 in CI
* ladder/public performance

Those remain separate proof targets after M50.

## Core thesis

STARLAB should support a **non-intrusive / hidden / background** local rollout posture for large operator campaigns while preserving:

* explicit evidence
* output-dir discipline
* repeatable tranches
* clean failure semantics
* resume / recovery semantics
* honest capability reporting

The key word is **honest**:
if true hidden execution is not supported on a given machine or launch path, the system must **say so explicitly**, not pretend.

## Milestone posture

This is a **larger single milestone** with three tightly related deliverable tracks:

### Track A — Hidden rollout capability surface

Define and implement the governed runtime surface for hidden / non-intrusive rollout execution.

### Track B — Governed campaign executor / supervisor

Define and implement a proper campaign execution layer over the M49 charter.

### Track C — Preflight hardening + operator ergonomics

Upgrade readiness checks and operator controls so large local campaigns can run safely.

These three tracks belong together and should land in one milestone.

## In scope

### 1. Hidden rollout runtime contract

Add a new runtime document, recommended:

* `docs/runtime/industrial_hidden_rollout_mode_v1.md`

This doc should define:

* what "hidden rollout" means in STARLAB
* what it does and does not promise
* capability states / fallback states
* how it relates to M44 / M45 / M49
* how visibility posture is recorded
* what counts as successful hidden execution
* what still remains a non-claim

The contract must support **honest degraded modes**, for example:

* requested hidden
* resolved hidden
* resolved minimized
* resolved visible fallback
* unsupported

Do not allow silent fallback that hides the truth from the operator.

### 2. Hidden rollout capability model

Implement a governed capability / posture model, matching existing STARLAB style:

* `TypedDict`
* plain dict assembly
* existing canonical JSON / hashing helpers
* no Pydantic introduction

Recommended concepts:

* `requested_visibility_mode`
* `resolved_visibility_mode`
* `hidden_rollout_supported`
* `hidden_rollout_mechanism_id`
* `capability_warnings`

This should make the system honest about whether it actually achieved a hidden/non-intrusive posture.

### 3. Governed campaign execution artifacts

M49 already defines campaign charter + preflight.
M50 should add the actual **governed campaign execution surface**.

Recommended artifact layout under the M49 campaign root:

* `campaign_runs/<execution_id>/hidden_rollout_campaign_run.json`
* `campaign_runs/<execution_id>/hidden_rollout_campaign_run_report.json`
* `campaign_runs/<execution_id>/campaign_execution_manifest.json`
* `campaign_runs/<execution_id>/campaign_heartbeat.json`
* `campaign_runs/<execution_id>/campaign_resume_state.json`

You may refine names if needed, but keep them consistent and audit-friendly.

These artifacts should bind:

* the M49 campaign contract identity
* the execution id
* the visibility posture actually used
* tranche / stage boundaries
* partial / complete / failed state
* restart / resume lineage
* explicit warnings / caveats

### 4. Campaign executor / orchestrator CLI

Add a real campaign execution surface that consumes the M49 contract and runs the campaign.

Recommended CLI:

* `python -m starlab.training.execute_full_local_training_campaign`

or an equally clear name.

This CLI should:

* consume the M49 contract
* honor tranche structure
* execute shakedown / tranche A / tranche B / thresholded batches
* emit governed execution artifacts
* support graceful resume after interruption
* support safe operator stop behavior
* support explicit hidden rollout request / resolution reporting

### 5. Process locking / output-dir locking / concurrency hygiene

This is mandatory.

M50 must prevent the operator problems already seen in local campaign work:

* overlapping runs
* two processes writing the same output tree
* ambiguous partial state
* unclear rerun authority

Implement:

* one-process-per-output-dir lock
* one active execution lock per execution tree
* explicit quarantine / partial-state handling
* explicit resume semantics
* no silent overwrite of prior failed attempts

### 6. Resume / recovery / quarantine semantics

This is part of the "industrial-scale" requirement.

M50 should support:

* interrupted campaign detection
* partial tranche detection
* canonical resume state
* quarantined failed / partial execution trees
* clear operator guidance about what is canonical vs non-canonical

Do not merely rerun blindly into the same folder.

### 7. Stronger live preflight for campaign execution

M49 preflight must be hardened for real large live campaigns.

Add checks for at least:

* map discoverability
* SC2 root resolution
* optional `STARLAB_SC2_MAPS_DIR`
* hidden rollout capability detection
* Python executable / dependency readiness for the chosen execution surface
* process collision detection
* output-dir cleanliness / lock safety

The key requirement:
a green preflight for a hidden live campaign should be much closer to meaning "this can really start."

### 8. Operator controls

Add simple but enterprise-grade operator controls, for example:

* stop-request file or equivalent graceful stop signal
* heartbeat timestamp updates
* stage / tranche progress tracking
* bounded summary for long runs

These controls should support real unattended campaigns without requiring constant manual babysitting.

### 9. Runtime / operator docs

Update at minimum:

* `docs/runtime/full_local_training_campaign_v1.md`
* `docs/runtime/self_play_rl_bootstrap_v1.md`
* new `docs/runtime/industrial_hidden_rollout_mode_v1.md`

Also add one concise operator-facing guide, for example:

* `docs/diligence/industrial_hidden_rollout_operator_guide.md`

This guide should distinguish:

* visible live validation
* visible live tranche work
* hidden rollout campaign execution
* when each is appropriate
* what each does and does not prove

### 10. Governance / ledger posture

Update `docs/starlab.md` during implementation only as needed for truthful "in progress" posture.

At closeout, ensure the ledger explicitly distinguishes:

* visible live validation path
* hidden rollout campaign path

Also add a compact "remaining v1 proof targets" note if it improves clarity:

* benchmark integrity
* replay↔execution equivalence
* live SC2 in CI
* ladder/public performance

## Out of scope

M50 must **not** expand into:

* benchmark integrity proof
* replay↔execution equivalence proof
* live SC2 in CI
* ladder/public performance
* new reward-policy redesign
* new RL algorithm family
* M42 comparison redesign
* weighted refit reinterpretation
* cluster / distributed training across multiple machines
* committing `out/`

## Expected implementation style

Lock these decisions unless a strong reason emerges:

* follow current repo style (`TypedDict`, plain dicts, current JSON helpers)
* do not introduce Pydantic
* preserve enterprise-grade audit posture
* prefer explicit artifacts over hidden state
* prefer explicit failure over silent fallback

## Recommended branch name

`m50-industrial-hidden-rollout-mode`

## Acceptance criteria

M50 is done when all of the following are true:

1. There is a governed runtime contract for hidden / non-intrusive rollout mode.
2. There is a real campaign execution CLI that consumes the M49 contract.
3. Execution artifacts record requested vs resolved visibility posture honestly.
4. Output-dir locking prevents overlapping campaign execution.
5. Resume / recovery semantics are explicit and test-covered.
6. Preflight is materially stronger for live hidden campaign readiness.
7. Runtime and operator docs clearly distinguish visible vs hidden rollout posture.
8. CI remains fixture-only and green.
9. `docs/starlab.md` is updated at closeout as the living source of truth.
10. Nothing in M50 overclaims benchmark integrity, replay↔execution equivalence, live SC2 in CI, or ladder strength.

## Validation posture

### Required CI / local validation

* `ruff check`
* `mypy`
* full `pytest -q`
* fixture-first tests for:

  * hidden capability bookkeeping
  * lock semantics
  * resume / recovery
  * output-dir collision prevention
  * preflight readiness / failure cases
  * governance docs

### Operator-local validation

Expected if environment permits, but not the sole merge gate:

* one hidden/non-intrusive shakedown
* optional bounded hidden tranche demonstration
* operator notes under `out/`
* no `out/` commits

The repo merge should still stand on code/docs/tests/CI, with operator-local evidence reported honestly.

## Non-claims

M50 does **not** prove:

* benchmark integrity
* replay↔execution equivalence
* live SC2 in CI
* ladder/public performance
* broad RL product strength
* that huge campaigns are automatically informative under current reward posture

M50 only proves, narrowly:

* STARLAB can run governed local campaign execution in an honest hidden/non-intrusive posture with supervision, locking, and recovery semantics

## Suggested sequencing inside the milestone

### Phase 1

Docs + models + capability semantics

### Phase 2

Execution CLI + artifacts + lock semantics

### Phase 3

Resume / quarantine / stop / heartbeat controls

### Phase 4

Preflight hardening + docs integration

### Phase 5

Tests + local validation + PR / CI / closeout

## Closeout reminder

When M50 is eventually closed:

* create the milestone summary using `docs/company_secrets/prompts/summaryprompt.md`
* create the milestone audit using `docs/company_secrets/prompts/unifiedmilestoneauditpromptV2.md`
* use `docs/company_secrets/prompts/workflowprompt.md` for workflow-run analysis when applicable
* **ensure all documentation is updated as necessary**
* update `docs/starlab.md`
* seed `M51_plan.md` and `M51_toolcalls.md`

## One explicit recommendation

Do not let M50 silently promise "true headless" if the platform only supports a weaker hidden or non-intrusive posture.

The milestone should be judged on:

* honesty
* governance
* execution discipline
* industrial-scale operator ergonomics

not on pretending the platform can do more than it really can.
