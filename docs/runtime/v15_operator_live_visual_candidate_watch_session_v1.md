# STARLAB runtime — V15-M57A: Operator Live Visual Candidate Watch Session v1

**Contract id:** `starlab.v15.operator_live_visual_candidate_watch_session.v1`  
**Report contract id:** `starlab.v15.operator_live_visual_candidate_watch_session_report.v1`  
**Profile id:** `starlab.v15.m57a.operator_live_visual_candidate_watch_session.v1`  
**Milestone:** `V15-M57A`  
**Emitter:** `python -m starlab.v15.emit_v15_m57a_operator_live_visual_candidate_watch_session`  
**Runner:** `python -m starlab.v15.run_v15_m57a_operator_live_visual_candidate_watch_session`

## Purpose

**V15-M57A** is the first milestone oriented toward an **operator-local visual watch session** for the **latest** checkpoint from **V15-M53** / **V15-M54**, **after** the **V15-M56** bounded readout, and **before** the **V15-M57** governed evaluation execution charter / dry-run gate.

It **reuses governance posture from V15-M56A** (contract style, claim flags, scaffold labeling, public/private boundary language) but is a **separate surface**: its own contracts, artifacts, emitter, and runner.

**Upstream context:** optional sealed **§V15-M55** preflight, **§V15-M54** / **§V15-M53** cross-checks, optional **§V15-M56A** context JSON (non-gating). **Honesty:** if no real candidate-live adapter path is available, the runner records **`candidate_live_visual_watch_blocked_missing_adapter`** (or an explicit scaffold path) — **do not** invent adapter behavior.

**Cross-check anchors:**

| Anchor | Role |
| --- | --- |
| Canonical sealed **V15-M54** package SHA-256 | `bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6` |
| **V15-M53** sealed run artifact SHA-256 | `18a1e6c39bb372c3f7edc595919963d12442467a74dd329e56f7cf0d0c816ec8` |
| Latest produced candidate checkpoint SHA-256 | `7c91a4b7cec6b14d160c00bec768c4fb3199bd8bf0228b2436bd7fbc5dc6ea90` |

## What M57A does **not** claim

- Not benchmark execution, benchmark pass/fail, scorecard totals, or strength evaluation.  
- Not checkpoint promotion, XAI, human-panel, showcase, **v2**, or **T2–T5**.  
- **M57A** does not introduce new **`torch.load`** or checkpoint-to-policy wiring; **`--prefer-candidate-live-adapter`** delegates to **V15-M52A** where that loading already exists under its guards.

## Primary artifacts (public-safe)

| File | Role |
| --- | --- |
| `v15_operator_live_visual_candidate_watch_session.json` | Sealed main record (`artifact_sha256` over canonical body without that field). |
| `v15_operator_live_visual_candidate_watch_session_report.json` | Deterministic report companion. |
| `v15_operator_live_visual_candidate_watch_session_checklist.md` | Operator checklist. |

## Profiles

| Profile | Behavior |
| --- | --- |
| `fixture_ci` | Deterministic schema-only; no live SC2; no `out/` dependency. |
| `operator_preflight` | Structural preflight over optional upstream JSON + canonical SHA anchors. |
| `operator_declared` | Validates operator-declared session body + seals; does **not** run SC2. |

## Runner policy (operator-local only)

Dual guards (always):

- `--allow-operator-local-execution`
- `--authorize-live-visual-watch-session`

**Candidate adapter path:** `--prefer-candidate-live-adapter` runs the existing **`run_v15_m52_candidate_live_adapter_spike`** delegate; seal and classification follow **M52A** honesty ( **`candidate_live_visual_watch_completed`** only when that path actually ran with evidence of candidate control).

**Without** the adapter flag: **`--allow-scaffold-watchability-policy`** is required; the runner delegates to **`run_v15_m51_live_candidate_watchability_harness`** — classification **`scaffold_visual_watch_completed_not_candidate_policy`**.

**Blocked** when the candidate path is requested but unavailable: **`candidate_live_visual_watch_blocked_missing_adapter`**.

Forbidden CLI (emitter/runner refusal): benchmark/strength/promotion-style flags listed in the contract models (`--claim-benchmark-pass`, `--promote-checkpoint`, etc.).

## Replay and metadata (local `out/`)

When live SC2 actually runs, save replay under **`out/`** when possible and record metadata fields (replay reference, map, opponent mode, steps, action count, duration, result, optional `replay_sha256`). **Do not** commit raw replays; public artifacts may include **relative** references or hashes only — no private absolute path leakage.

## Sample commands

Fixture (CI-safe):

```bash
python -m starlab.v15.emit_v15_m57a_operator_live_visual_candidate_watch_session \
  --profile fixture_ci \
  --output-dir out/v15_m57a_fixture
```

Operator preflight / declared paths follow the emitter’s `--help` for required JSON inputs and `--candidate-checkpoint` binding on the runner.

## Route advisory

**`route_to_v15_m57_governed_evaluation_execution_charter_dry_run_gate`** · **`recommended_not_executed`** until **§V15-M57** is executed under its own charter.
