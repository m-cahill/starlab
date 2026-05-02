# STARLAB runtime — V15-M55: Bounded Evaluation Package Preflight v1

**Contract id:** `starlab.v15.bounded_evaluation_package_preflight.v1`  
**Report contract id:** `starlab.v15.bounded_evaluation_package_preflight_report.v1`  
**Milestone:** `V15-M55`  
**Emitter:** `python -m starlab.v15.emit_v15_m55_bounded_evaluation_package_preflight`

## Purpose

**V15-M55** implements a deterministic **package-readiness / preflight** surface over an **operator-declared evaluation package**. It answers:

> Is the declared evaluation package complete, internally bound, policy-aligned, and safe to hand to the next bounded readout step?

It does **not** answer whether a candidate passed evaluation, whether an agent is strong, whether a checkpoint should be promoted, or whether benchmarks, replay↔execution equivalence, ladder performance, or human-panel outcomes hold.

This milestone performs **package preflight only**. It does **not** execute evaluation, score candidates, promote checkpoints, run live SC2, load weights, claim benchmark pass/fail, or produce XAI/human-panel evidence.

## Primary artifacts (public-safe)

| File | Role |
| --- | --- |
| `v15_bounded_evaluation_package_preflight.json` | Sealed main preflight record (`artifact_sha256` over canonical body without that field). |
| `v15_bounded_evaluation_package_preflight_report.json` | Human-oriented deterministic report companion. |

## Canonical upstream (V15-M54)

The sealed **V15-M54** operator package artifact SHA-256 anchor expected on success paths is:

`bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6`

Matching **package id** (declared / validated in `operator_declared`):

`starlab.v15.m54.twelve_hour_run_package.sealed.bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6`

## Profiles

| Profile | Behavior |
| --- | --- |
| `fixture_ci` | Deterministic structural pass; no filesystem dependency on real `out/`; uses canonical M54 anchor placeholders. |
| `operator_preflight` | **Blocked** preflight with `blocked_missing_required_input` when operator evidence is intentionally absent (dry shape). |
| `operator_declared` | Requires explicit CLI declarations and JSON paths; compares operator **upstream M54 SHA** and **package id** to the canonical anchors; hashes JSON metadata files as raw file SHA-256 digests; synthesizes **evaluation package SHA** from manifest + candidate + scorecard digests. |

## Evaluation package SHA binding (operator_declared)

The `--evaluation-package-sha256` value must equal the canonical JSON digest:

`sha256_hex(canonical_json({"candidate_identity_sha256": "...", "evaluation_package_manifest_sha256": "...", "scorecard_or_readout_plan_sha256": "..."}))`

Keys are sorted lexicographically in canonical encoding (STARLAB `canonical_json_dumps` convention).

## Preflight statuses

| Status | Meaning |
| --- | --- |
| `ready_for_bounded_readout` | Structural checks passed; claim flags remain false. |
| `blocked_missing_required_input` | Required operator inputs or files missing. |
| `blocked_identity_mismatch` | Upstream M54 binding or synthesized package SHA inconsistent. |
| `blocked_invalid_sha256` | Malformed SHA-256 operator inputs. |
| `blocked_claim_violation` | Input metadata or honesty breach (e.g. forbidden CLI flags or claim-like JSON). |
| `blocked_private_boundary_violation` | Local-only path hygiene failure in metadata (e.g. `docs/company_secrets`, raw `out/` path segments in file text). |

## Claim flags

All **`claim_flags`** in the main JSON remain **`false`** for **V15-M55**. No downstream milestone may treat **V15-M55** as authorizing evaluation execution, benchmark pass/fail, promotion, strong-agent, human-panel, XAI completion, or **v2** readiness.

## Public / private boundary

* Do **not** commit raw `out/` blobs, checkpoint weights, or `docs/company_secrets/**`.
* Metadata JSON referenced by the CLI is **hashed only**; checkpoint blobs are **not** loaded.

## Non-claims (standing)

* No evaluation execution.
* No benchmark pass/fail.
* No candidate promotion.
* No strong-agent claim.
* No human-panel claim.
* No XAI completion.
* No v2 readiness claim.

## Sample commands

Fixture (CI-safe):

```bash
python -m starlab.v15.emit_v15_m55_bounded_evaluation_package_preflight \
  --profile fixture_ci \
  --output-dir out/v15_m55_fixture
```

Operator declared (all arguments required):

```bash
python -m starlab.v15.emit_v15_m55_bounded_evaluation_package_preflight \
  --profile operator_declared \
  --output-dir out/v15_m55_operator_preflight \
  --evaluation-package-id <id> \
  --evaluation-package-sha256 <synthesized_binding_sha256> \
  --upstream-m54-package-id starlab.v15.m54.twelve_hour_run_package.sealed.bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6 \
  --upstream-m54-package-sha256 bbe08673aa85beb0ae7e51a627a68c67fd95a930176d174d2c60bb96e4a278d6 \
  --evaluation-package-manifest <path-to.json> \
  --candidate-identity <path-to.json> \
  --scorecard-readout-plan <path-to.json>
```

Exit codes: **`0`** success / fixture / forbidden-flag refusal bundle; **`2`** CLI usage or malformed SHA; **`3`** operator **`operator_declared`** preflight blocked.

## Provisional next milestone

**`V15-M56` — Bounded Evaluation Package Readout / Decision** (consume **V15-M55** preflight; emit bounded readout decision; **not** implemented in **V15-M55**).

