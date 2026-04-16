# Live SC2 in CI — hardening & cost guardrails v1 (M58)

**Status:** **M58** — **closed** on `main` — hardens the **closed M57** bounded live-SC2-in-CI path — **not** global proof of live SC2 as a merge gate; **not** ladder/public evaluation (**M59** stub). See `docs/starlab.md` §1 / §11 / §18 / §23 and tag **`v0.0.58-m58`** on merge commit `3a6f13910dc8056cb0d88161796dd5fe7888629d` ([PR #69](https://github.com/m-cahill/starlab/pull/69)).

## Purpose

**M58** adds **policy**, **preflight receipts**, and **workflow guardrails** around the same narrow surface **M57** established: one **runner profile** (`starlab.m57.runner_profile.m44_single_validation_v1`), **M43** hierarchical candidates with explicit weights only, **M44** as the only live execution substrate, and **optional** manual **`workflow_dispatch`** automation — **without** widening claim boundaries.

## Definitions

### Hardening

**Hardening** (M58 sense) means: explicit **timeouts**, **artifact retention ceilings**, **fleet label checks**, **concurrency posture**, **attempt limits**, **advisory locking** with surfaced denial, **preflight validation** before the controlled runner, and **explicit confirmation** for `local_live_sc2` — all recorded in deterministic JSON artifacts.

### Cost guardrails

**Cost guardrails** (M58 sense) means: bounded **wall-clock** budget per workflow invocation, bounded **artifact retention** for uploaded CI artifacts, **no matrix expansion**, **no automatic retries** at the workflow layer, and **at most one** execution attempt per invocation in policy (enforced by workflow design + receipts).

### Guardrail profile

Exactly **one** profile is defined:

| Field | Value |
| ----- | ----- |
| `guardrail_profile_id` | `starlab.m58.guardrail_profile.m57_single_validation_cost_guardrails_v1` |
| `runner_profile_id` | `starlab.m57.runner_profile.m44_single_validation_v1` (unchanged; **not** a second runner profile) |

## Preflight receipt

Contract id: **`starlab.live_sc2_in_ci_preflight_receipt.v1`**

The preflight validates (when applicable): workflow trigger, runner labels against the repo’s **self-hosted / starlab-sc2** allowlist posture, M43 candidate class, weights path presence, match-config **adapter** vs **runtime mode**, timeout/retention budgets, explicit live confirmation for `local_live_sc2`, advisory **lock acquisition**, and (for **`local_live_sc2` only**) SC2 binary probe outcome. For **`fixture_stub_ci`**, the SC2 probe is **not** run — recorded as **not applicable**.

### Receipt statuses (`preflight_status`)

| Status | Meaning |
| ------ | ------- |
| `cleared` | All checks passed; controlled runner may run. |
| `failed_preconditions` | Policy or prerequisite violation (e.g. missing confirmation, probe failure, bad adapter). |
| `skipped_by_policy` | Reserved for explicit policy skips (distinct from M57 controlled-runner `skipped_by_policy`). |
| `lock_denied` | Advisory lock could not be acquired while another holder is active. |

## Workflow posture

- **`workflow_dispatch` only** — not `pull_request`, not default `push` merge authority.
- **`permissions: contents: read`** unless a future milestone proves stricter need.
- **Concurrency** group limits overlapping runs; **cancel-in-progress** is **false** to avoid aborting an in-flight bounded run without operator intent.
- **Job timeout:** 30 minutes (guardrail-aligned).
- **Artifact upload retention:** 7 days.

## Static guardrails artifact

Contract id: **`starlab.live_sc2_in_ci_hardening_guardrails.v1`**

CLI:

```bash
python -m starlab.sc2.emit_live_sc2_in_ci_guardrails --output-dir <dir>
```

## Preflight CLI

```bash
python -m starlab.sc2.emit_live_sc2_in_ci_preflight \
  --m43-run <path> \
  --weights <path> \
  --match-config <path> \
  --runtime-mode fixture_stub_ci|local_live_sc2 \
  --workflow-trigger workflow_dispatch \
  --runner-labels "<os>,self-hosted,starlab-sc2" \
  --timeout-minutes 30 \
  --artifact-retention-days 7 \
  --live-sc2-confirmed true|false \
  --output-dir <dir>
```

## Explicit non-claims

- **Not** making live SC2 a **required** merge gate.
- **Not** proving **global** live-SC2-in-CI operational maturity.
- **Not** replacing **M52–M54** replay↔execution equivalence or **M55–M56** benchmark-integrity claims.
- **Not** **M59** ladder/public evaluation protocol.

## Boundary: M58 vs M59

**M58** hardens **M57**. **M59** owns ladder/public evaluation protocol & evidence — see ledger.
