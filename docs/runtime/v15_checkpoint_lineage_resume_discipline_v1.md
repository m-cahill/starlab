# STARLAB v1.5 (V15-M03) — Checkpoint Lineage and Resume Discipline v1

**Contract id:** `starlab.v15.checkpoint_lineage_manifest.v1`  
**Milestone:** V15-M03  
**Type:** Runtime narrative and governance (metadata contracts only; no training execution on this path)

## Purpose of V15-M03

V15-M03 establishes a **deterministic, fixture-safe** surface for **checkpoint identity**, **parent/child lineage**, **binding** to environment lock / dataset / model-config references, and **interruption / resume / rollback** receipt shapes—**before** GPU shakedown (**V15-M07**) or a long training campaign.

## Relationship to V15 long GPU run gates (A–G)

- **Gate D — Checkpoints** (hashing, lineage, resume, rollback, promotion states) is the primary consumer of this milestone.
- **Gates A–C** and **E–G** are **not** satisfied by the M03 manifest alone; the manifest may **reference** M02 environment material but does not prove operator environment readiness.

## Relationship to V15-M01 (registers) and M02 (environment lock)

- **M01** public registers (including the checkpoint **register** doc) list **governance** requirements for claim-critical use; M03 does **not** add real checkpoint rows to public tables.
- **M02** `starlab.v15.long_gpu_environment_lock.v1` may be **bound** by canonical SHA-256 of an on-disk JSON file via `--environment-lock-json` (metadata binding only; not proof the operator long-run environment is valid).

## Checkpoint lineage model

Each checkpoint is a **metadata row** with: identity, role, storage/path disclosure, optional SHA-256 reference, parent link, run binding, and promotion state. The manifest distinguishes:

1. **Metadata declared** — fields present in JSON.
2. **Checkpoint bytes verified** — only when `hash_verification_status` is `verified_external` and the status is read as an **externally attested** claim (M03 does not read weight files).
3. **Lineage graph** — `parent_checkpoint_id` must refer to an existing `checkpoint_id` in the same manifest, or be `null` for a root.

## Resume discipline model

- **Resume receipts** are **metadata objects** with verification status vocabulary.
- **M03** sets `resume_execution_verified: false` at the manifest root regardless of operator-declared `resume_verification_status` (including `verified_external`); the latter is pass-through and does **not** mean M03 executed or witnessed resume.

## Interruption / rollback receipt shapes

See emitted JSON: `interruption_receipts`, `resume_receipts`, `rollback_receipts`. In **fixture** profile, **fixture** verification statuses mean **schema/wiring** only, not a real training event. For **operator_declared** input, default posture is `declared_only` or `not_executed` unless the operator states otherwise; `rollback_execution_verified` at root stays **false**.

## Vocabularies

Emitted manifests include: `lineage_manifest_status_vocabulary`, `promotion_status_vocabulary`, `hash_verification_status_vocabulary`, `resume_verification_status_vocabulary`, `rollback_verification_status_vocabulary`, `storage_posture_vocabulary`, `path_disclosure_vocabulary`, and related fields. Exact lists are in the emitted `v15_checkpoint_lineage_manifest.json`.

## Public / private posture

- **Fixture profile** is CI-safe: no local paths, no reads of real checkpoints.
- **Operator-declared** input may be redacted: strings resembling absolute paths are replaced with the literal `<REDACTED_ABSOLUTE_PATH>` in public JSON output.
- **Never** commit private lineage JSON, operator paths, or weight blobs in the public merge path.

## Fixture vs operator-declared evidence

| Mode | `lineage_manifest_status` (typical) | Meaning |
| --- | --- | --- |
| `fixture_ci` | `fixture_only` | Deterministic metadata for wiring tests |
| `operator_declared` (complete) | `operator_declared_complete` | All required fields present; enums valid; lineage graph consistent |
| `operator_declared` (partial) | `operator_declared_incomplete` | Missing or invalid metadata |

## Non-claims (M03)

V15-M03 defines and emits the checkpoint lineage and resume-discipline **surface**. It may validate fixture metadata and may normalize supplied operator-declared checkpoint lineage metadata, but it does **not** create checkpoint blobs, does **not** verify checkpoint bytes by default, does **not** execute trainer resume, does **not** execute rollback, does **not** promote a strong checkpoint, does **not** run evaluation, does **not** execute GPU training or shakedown, does **not** authorize a long GPU run, does **not** approve real assets for claim-critical use, does **not** open v2, and does **not** open PX2-M04/PX2-M05.

A **checkpoint lineage manifest** is not a proof that checkpoint bytes exist unless the hash verification status says so under a **declared verification path**.

A **resume receipt** is not proof that training resumed unless the resume verification status says so under a **declared verification path**, and M03 does not independently verify that path.

`long_gpu_run_authorized` in the M03 contract is always **false**.

## CLI reference

```bash
python -m starlab.v15.emit_v15_checkpoint_lineage_manifest --output-dir <path> \
  [--profile fixture_ci|operator_declared] \
  [--lineage-json <path>] \
  [--environment-lock-json <path>]
```

- Default: `--profile fixture_ci` (no GPU, no SC2, no checkpoint file reads).
- `operator_declared` **requires** `--lineage-json`.
- `--lineage-json` top-level keys (only): `profile`, `training_run_id`, `environment_lock_reference`, `dataset_reference`, `model_config_reference`, `checkpoints`, `interruption_receipts`, `resume_receipts`, `rollback_receipts`, `operator_notes`.
- Unknown top-level keys are **rejected**.

## Emitted files

- `v15_checkpoint_lineage_manifest.json` — contract + `checkpoint_lineage_manifest_sha256` seal
- `v15_checkpoint_lineage_manifest_report.json` — report + counts + digest

## Implementation note

V15-M03 creates **checkpoint metadata and lineage discipline**, not checkpoint runtime execution in the trainer.

## Governance closure (V15-M03 on `main`)

**V15-M03** is **closed** on `main` as of [PR #120](https://github.com/m-cahill/starlab/pull/120) (merge `47a3fcb0a58ad6280dadc8967297774ed94ab4ad`, **2026-04-25**). Closure records the **metadata contract** and **merge/CI** evidence, per `docs/starlab-v1.5.md`. It does **not** assert on-disk **checkpoint byte** verification, **trainer resume** execution, or **rollback** execution; it does **not** imply a checkpoint was **promoted** as strong. **`long_gpu_run_authorized`** remains **false** in the M03 contract.
