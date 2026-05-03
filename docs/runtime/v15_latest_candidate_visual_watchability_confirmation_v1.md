# STARLAB runtime — V15-M56A: Latest Candidate Visual Watchability Confirmation v1

**Contract id:** `starlab.v15.latest_candidate_visual_watchability_confirmation.v1`  
**Report contract id:** `starlab.v15.latest_candidate_visual_watchability_confirmation_report.v1`  
**Profile id:** `starlab.v15.m56a.latest_candidate_visual_watchability_confirmation.v1`  
**Milestone:** `V15-M56A`  
**Emitter:** `python -m starlab.v15.emit_v15_m56a_latest_candidate_visual_watchability_confirmation`  
**Runner:** `python -m starlab.v15.run_v15_m56a_latest_candidate_visual_watchability_confirmation`

## Purpose

**V15-M56A** provides a **governed visual watchability confirmation** surface for the **latest** checkpoint produced by the **V15-M53** 12-hour run and packaged under **V15-M54**, **after** **V15-M55** bounded evaluation package preflight.

**Immediate upstream:** sealed **`v15_bounded_evaluation_package_preflight.json`** (**§V15-M55**).

**Cross-check anchors (not substitutes for M55):**

| Anchor | Role |
| --- | --- |
| Canonical sealed **V15-M54** package SHA-256 | `bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6` |
| **V15-M53** sealed run artifact SHA-256 | `18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8` |
| Latest produced candidate checkpoint SHA-256 | `7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90` |

This milestone answers only:

> Can we visually observe (or honestly preflight / declare) watchability for the latest candidate through a governed path, with clean receipts, **without** conflating that with benchmark evidence?

Visual watchability confirmation is **observation evidence only**. It is **not** benchmark execution, not benchmark pass/fail, not strength evaluation, not checkpoint promotion, not XAI, not human-panel evidence, not showcase release, and not v2 readiness.

## Primary artifacts (public-safe)

| File | Role |
| --- | --- |
| `v15_latest_candidate_visual_watchability_confirmation.json` | Sealed main record (`artifact_sha256` over canonical body without that field). |
| `v15_latest_candidate_visual_watchability_confirmation_report.json` | Deterministic report companion. |
| `v15_latest_candidate_visual_watchability_confirmation_checklist.md` | Operator checklist (W0–W9). |

## Profiles

| Profile | Behavior |
| --- | --- |
| `fixture_ci` | Deterministic schema-only path; no live SC2; no `out/` dependency. |
| `operator_preflight` | Validates sealed **M55** (`preflight_status` **must** be `ready_for_bounded_readout`), **M54** JSON seal + canonical package SHA, **M53** seal + canonical run artifact SHA, produced candidate SHA from **M54**, and at least one of **M51** / **M52A** watchability JSON for path binding. |
| `operator_declared` | Validates operator-declared watchability evidence JSON + **M55**; does **not** run SC2. |
| `operator_local_watchability` | Runner entrypoint: refusal by default; optional triple-guard **stub** receipt (no live SC2 in this milestone). Live SC2 remains under **M51** / **M52A** with their own guards. |

## Runner policy

Dual guards (when using the runner):

- `--allow-operator-local-execution`
- `--authorize-visual-watchability-run`

Without a **real** candidate-live adapter (`real_candidate_live_policy_adapter_available()`), the runner **refuses** unless all three are present:

- `--allow-scaffold-watchability-policy`

Refusal status: `watchability_blocked_missing_candidate_live_policy_adapter`.

Stub scaffold receipt (triple guard): `policy_source` = `scaffold_watchability_policy`, `candidate_policy_adapter_status` = `missing`, `visual_confirmation_status` = `visual_watchability_confirmed_with_warnings` — **live SC2 is still not invoked by this runner**; use **`run_v15_m51_live_candidate_watchability_harness`** for bounded live SC2.

## Scaffold vs candidate-live adapter

Do **not** describe outcomes as “the latest candidate played” unless the artifact explicitly distinguishes:

- `candidate_live_adapter` — operator-declared or evidenced adapter path, or  
- `scaffold_watchability_policy` — Burny/M27-style scaffold; **not** the trained candidate policy controlling play.

## Public / private boundary

Do **not** commit raw `out/`, checkpoint blobs, replay files, videos, or `docs/company_secrets/**`. Replay/video metadata references are **local-only** metadata in operator bundles.

## Sample commands

Fixture (CI-safe):

```bash
python -m starlab.v15.emit_v15_m56a_latest_candidate_visual_watchability_confirmation \
  --profile fixture_ci \
  --output-dir out/v15_m56a_fixture
```

Operator preflight (requires operator JSON paths and canonical SHA anchors):

```bash
python -m starlab.v15.emit_v15_m56a_latest_candidate_visual_watchability_confirmation \
  --profile operator_preflight \
  --output-dir out/v15_m56a_preflight \
  --m55-preflight-json <path> \
  --m54-package-json <path> \
  --m53-run-json <path> \
  --expected-m54-package-sha256 bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6 \
  --expected-candidate-sha256 7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90 \
  --m51-watchability-json <path>
```

Operator declared evidence:

```bash
python -m starlab.v15.emit_v15_m56a_latest_candidate_visual_watchability_confirmation \
  --profile operator_declared \
  --output-dir out/v15_m56a_declared \
  --watchability-evidence-json <path> \
  --m55-preflight-json <path> \
  --expected-candidate-sha256 7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90
```

Runner (refusal unless scaffold triple-guard):

```bash
python -m starlab.v15.run_v15_m56a_latest_candidate_visual_watchability_confirmation \
  --allow-operator-local-execution \
  --authorize-visual-watchability-run \
  --allow-scaffold-watchability-policy \
  --m55-preflight-json <path> \
  --output-dir out/v15_m56a_runner_stub
```

Exit codes: **`0`** success; **`2`** CLI usage; **`3`** blocked / refused bundle emitted.

## Non-claims

- No benchmark execution.  
- No benchmark pass/fail.  
- No scorecard results.  
- No strength evaluation.  
- No checkpoint promotion.  
- No XAI completion.  
- No human-panel evaluation.  
- No showcase release.  
- No v2 authorization.  
- No T2–T5 execution.  
- No `torch.load` / checkpoint blob load **for evaluation** via this contract.

## Next milestone

**V15-M56** — *Bounded Evaluation Package Readout / Decision*.
