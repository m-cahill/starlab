# V15-M18 — Candidate checkpoint evaluation readiness & refusal contract v1

**Contract id:** `starlab.v15.checkpoint_evaluation_readiness.v1`  
**Milestone:** `V15-M18`  
**Emitter:** `python -m starlab.v15.emit_v15_checkpoint_evaluation_readiness --output-dir <path>`

## 1. Purpose

STARLAB must not infer gameplay strength, promotion, or benchmark outcomes from plumbing-only evidence. This milestone answers a single question:

> Given supplied governance JSON (and optional operator-local inventory), **may** a *future* milestone begin **candidate checkpoint evaluation** under v1.5 rules?

This contract **does not** run evaluation, training, live SC2, or long GPU campaigns. It emits deterministic **readiness / refusal** JSON for auditors and operators.

## 2. Relationship to V15-M17

**V15-M17** delivered long GPU campaign **evidence / preflight** and honest **`not_executed`** receipt stubs where appropriate. Operator-local watchability (e.g. M44/M50-class) may show execution plumbing but **does not** by itself establish a governed **PyTorch** checkpoint candidate. **M18** is the refusal-first gate **before** treating any artifact as evaluation-ready.

## 3. Required inputs (vocabulary)

The readiness artifact lists these **required input names** (presence is evaluated against the operator supplied package):

- `candidate_checkpoint_manifest` — logical manifest (`starlab.v15.candidate_checkpoint_manifest.v1`)
- `candidate_checkpoint_sha256` — declared SHA-256 of the candidate weight file (metadata; M18 does not read blobs in CI)
- `campaign_receipt` — M08-class `starlab.v15.long_gpu_campaign_receipt.v1`
- `training_completion_status` — carried from the receipt / manifest binding
- `checkpoint_lineage_manifest` — M03-class lineage with a row for the candidate
- `environment_manifest` — binding hash on the manifest (`environment_manifest_sha256`)
- `dataset_manifest` — binding hash on the manifest (`dataset_manifest_sha256`)
- `evaluation_protocol` — `evaluation_protocol_id` on the manifest

## 4. Readiness statuses

| Status | Meaning |
| --- | --- |
| `no_candidate_refusal` | No governed candidate package; or watchability-only posture; or receipt `not_executed` / `checkpoint_count: 0` |
| `candidate_evidence_incomplete` | PyTorch candidate indicated but governed receipt, lineage, or manifest bindings are missing |
| `candidate_ready_for_evaluation` | **ready_for_future_evaluation** — structural inputs align; **not** a strength result |
| `invalid_or_unsupported_candidate` | e.g. `.joblib`-only harness bundle, hash mismatch, invalid placeholder SHA |

## 5. Candidate kinds

| Kind | Notes |
| --- | --- |
| `none` | No neural candidate declared |
| `pytorch_checkpoint` | `.pt` / `.pth` primary artifact |
| `sklearn_bundle` | `.joblib` — may support harness / inference plumbing; **not** a promoted neural checkpoint by default |
| `unknown_artifact` | Unrecognized extension |

## 6. Refusal rules (selected)

- No candidate manifest → `no_candidate_refusal`
- `watchability_only` / watchability-only `evidence_classes` → refusal with `watchability_evidence_is_not_candidate_checkpoint_evidence`
- Receipt `campaign_completion_status: not_executed` → refusal
- Receipt `checkpoint_count: 0` → refusal
- `.joblib`-only primary artifact → `invalid_or_unsupported_candidate` (not promoted PyTorch checkpoint)
- Manifest SHA does not match lineage row or campaign `checkpoint_hashes` → `invalid_or_unsupported_candidate`
- Governed completed receipt + lineage row + manifest bindings → `candidate_ready_for_evaluation`

## 7. Accepted evidence classes (readiness only)

Readiness may pass only when evidence classes include, at minimum:

- Governed **completed** M08 campaign receipt (per M09 receipt validator semantics)
- **PyTorch** checkpoint reference with non-placeholder SHA-256
- Lineage manifest row matching `candidate_id` and SHA
- Environment / dataset / evaluation protocol bindings on the manifest

## 8. Non-claims

M18 does **not** claim:

- Checkpoint promoted  
- Strength evaluated  
- Benchmark passed  
- Human panel authorized  
- XAI demonstrated  
- v2 authorized  
- Long GPU campaign completed  

`candidate_ready_for_evaluation` means **inputs are ready for a future evaluation milestone**, not that the candidate is strong.

## 9. Operator-local vs public posture

- Default emit is **CI-safe** (`fixture_default`): no scanning of `out/**`.
- Optional `--local-inspection-root` performs **extension inventory only** (no hashing of weights, no promotion).
- Raw checkpoints, weights, large logs, and `docs/company_secrets/**` remain **private / local** per v1.5 boundary rules.

## 10. Artifacts

- `v15_checkpoint_evaluation_readiness.json` (sealed with `artifact_sha256`)
- `v15_checkpoint_evaluation_readiness_report.json`
