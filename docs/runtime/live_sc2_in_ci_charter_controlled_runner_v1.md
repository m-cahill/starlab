# Live SC2 in CI — bounded charter & controlled runner v1 (M57)

**Status:** M57 — narrow governance surface; **not** global proof of live SC2 in CI.

## Purpose

This document defines what STARLAB means by **bounded live SC2 in CI** for the **M57** milestone: a **charter**, **deterministic JSON artifacts**, and **one** controlled runner profile that wraps the existing **M44** local live-play validation harness.

It is **not** a substitute for **M58** (hardening, cost guardrails, fleet posture).

## Definitions

### Live SC2 in CI (bounded, M57)

**Live SC2 in CI (M57 sense)** means: an **opt-in**, **non-required** automation path (CLI or manual GitHub Actions `workflow_dispatch`) that may invoke **M44** with `runtime_mode=local_live_sc2` on a **self-hosted, SC2-capable** runner, using the **M43** hierarchical candidate + explicit weights sidecar, and **bounded** to **one** validation run per invocation under profile **`starlab.m57.runner_profile.m44_single_validation_v1`**.

### Default merge CI

**Default required CI** remains **fixture-only** (CPU paths, no live SC2 client). M57 **does not** add a required live-SC2 check to the merge boundary.

### Controlled runner

The **controlled runner** is the **`starlab.sc2`** module path that:

1. Validates the **M43** candidate (`hierarchical_training_run` v1 + weights).
2. Records **requested** vs **resolved** runtime mode and runner posture in a **receipt** JSON.
3. Calls **`run_local_live_play_validation`** (M44) — **no reimplementation** of the live-play harness.
4. Enforces **no silent downgrade** from `local_live_sc2` to `fixture_stub_ci` (if live prerequisites are not met, the run **fails** or **skips by explicit policy** — never a silent stub success as “live”).

## Supported runner profile (exactly one)

| Field | Value |
| ----- | ----- |
| `runner_profile_id` | `starlab.m57.runner_profile.m44_single_validation_v1` |
| Meaning | One bounded M44 validation; one candidate; one output directory; one replay-binding chain; one artifact bundle; one explicit `fixture_stub_ci` vs `local_live_sc2` decision |

## Supported candidate class

- **M43** hierarchical training run (`starlab.hierarchical_training_run.v1`) with **`weights`** sidecar / joblib path **explicitly** resolved.
- **Not in scope:** M41 flat runs, M45 refit bundles as primary candidates, or other classes.

## Runtime modes (M44 alignment)

| Mode | Match adapter | Use |
| ---- | ------------- | --- |
| `fixture_stub_ci` | `fake` | Deterministic CI / tests; stub replay bytes |
| `local_live_sc2` | `burnysc2` | Local SC2; requires SC2 install / probe prerequisites |

## Preconditions for `local_live_sc2`

- **`burnysc2`** match config (adapter `burnysc2`).
- SC2 install / binary discoverable per **`starlab.sc2.env_probe`** (`run_probe()` — narrow presence signal).
- Optional **skip-by-policy**: `--skip-live-when-prereqs-missing` or env **`STARLAB_M57_SKIP_LIVE_WHEN_PREREQS_MISSING=1`** emits a **`skipped_by_policy`** receipt instead of failing.

## Explicit non-claims (M57)

- **Not** proving live SC2 in CI as a **default** merge-gate norm.
- **Not** global benchmark integrity, **not** replay↔execution equivalence, **not** ladder/public performance.
- **Not** cost ceilings, queues, retries — **M58**.
- **Not** branch-protection or required-check changes.

## Artifacts (deterministic)

- Contract **`starlab.live_sc2_in_ci_charter.v1`** — `live_sc2_in_ci_charter.json` + `live_sc2_in_ci_charter_report.json`
- Contract **`starlab.live_sc2_in_ci_controlled_runner_receipt.v1`** — `live_sc2_in_ci_controlled_runner_receipt.json` + `live_sc2_in_ci_controlled_runner_receipt_report.json`

### CLIs

```bash
python -m starlab.sc2.emit_live_sc2_in_ci_charter --output-dir <dir>
python -m starlab.sc2.run_live_sc2_in_ci_controlled_runner \
  --m43-run <path> \
  --weights <path> \
  --match-config <path> \
  --output-dir <dir> \
  --runtime-mode fixture_stub_ci|local_live_sc2
```

## Boundary: M57 vs M58

| Milestone | Scope |
| --------- | ----- |
| **M57** | Charter + one controlled runner profile + receipts + optional manual workflow |
| **M58** | Hardening, cost guardrails, broader operational controls for live SC2-in-CI |

## References

- M44: `docs/runtime/local_live_play_validation_harness_v1.md`
- Ledger: `docs/starlab.md` (Phase VII, §11)
