# Replay — Intake Policy & Provenance (M07)

**Status:** Governed contract (M07)  
**Policy version:** `starlab.replay_intake_policy.v1`  
**Scope:** Opaque replay bytes + declared operator metadata; **no** replay parsing, **no** semantic extraction (M08+).

---

## 1. Purpose

This document defines the **M07** contract for STARLAB replay intake: a **narrow, deterministic, CI-safe replay intake gate** that:

- records **operator-declared** provenance and redistribution posture (not legal truth);
- enforces a **deterministic** intake-policy decision;
- emits **two** governed JSON artifacts (`replay_intake_receipt.json`, `replay_intake_report.json`);
- optionally cross-checks **M04** `replay_binding.json` and **M05** `manifest.json` / `run_identity.json` when supplied.

**M07 does not prove:** replay parser correctness, replay semantic extraction, build-order/timeline extraction, benchmark integrity, cross-host portability, live SC2 execution in CI, or final legal certainty about third-party replay rights.

---

## 2. Relationship to other milestones

| Milestone | Relationship |
| --------- | ------------- |
| M04 | Optional `replay_binding.json` — **opaque** `replay_content_sha256`; must match observed replay when supplied. |
| M05 | Optional `manifest.json` (`starlab.canonical_run_artifact.v0`) — must agree with `replay_binding.json` on shared identity fields when supplied. |
| M03 | Optional `run_identity.json` — must agree with `replay_binding.json` on shared fields when supplied. |
| M06 | Independent; no replay intake semantics. |
| M08+ | Parser substrate — **out of scope** for M07. |

---

## 3. Input: `replay_intake_metadata.json`

**Schema version:** `starlab.replay_intake_metadata.v1`

### Required fields

| Field | Type | Notes |
| ----- | ---- | ----- |
| `schema_version` | string | Must be `starlab.replay_intake_metadata.v1`. |
| `declared_origin_class` | enum | See §6. |
| `declared_acquisition_channel` | enum | See §6. |
| `declared_provenance_status` | enum | See §6. |
| `declared_redistribution_posture` | enum | See §6. |
| `declared_source_label` | string | Non-empty human label. |

### Optional fields

| Field | Type | Notes |
| ----- | ---- | ----- |
| `declared_source_reference` | string or null | |
| `operator_note` | string or null | |
| `expected_replay_content_sha256` | string or null | 64 lowercase hex; if present, must match observed replay SHA-256. |

---

## 4. Output artifacts

### 4.1 `replay_intake_receipt.json`

**Schema version:** `starlab.replay_intake_receipt.v1`

Purpose: canonical record of the replay candidate and normalized declared metadata.

| Field | Description |
| ----- | ----------- |
| `schema_version` | `starlab.replay_intake_receipt.v1` |
| `replay_content_sha256` | SHA-256 of replay bytes (or `null` if unreadable). |
| `replay_size_bytes` | Size in bytes (or `null`). |
| `observed_filename` | Basename of replay path. |
| `intake_metadata_sha256` | Hash of normalized metadata (or best-effort hash of raw input if invalid). |
| `normalized_metadata` | Object or `null` if metadata invalid. |
| `linked_artifacts` | SHA-256 of optional linked files (`replay_binding.json`, `run_identity.json`, `run_artifact_manifest.json`). |
| `policy_version` | `starlab.replay_intake_policy.v1` |

### 4.2 `replay_intake_report.json`

**Schema version:** `starlab.replay_intake_report.v1`

Purpose: deterministic policy decision and audit-friendly check results.

| Field | Description |
| ----- | ----------- |
| `schema_version` | `starlab.replay_intake_report.v1` |
| `replay_content_sha256` | SHA-256 of replay bytes (or `null`). |
| `policy_version` | `starlab.replay_intake_policy.v1` |
| `check_results` | Ordered list (see §5). |
| `intake_status` | One of four statuses (see §7). |
| `local_processing_allowed` | Boolean. |
| `canonical_review_eligible` | Boolean. |
| `public_redistribution_allowed` | Boolean. |
| `reason_codes` | Sorted list of machine-readable codes. |
| `advisory_notes` | Sorted list of human-readable notes. |

---

## 5. Check model

Checks are emitted in **fixed order** (see `starlab.replays.intake_models.CHECK_IDS`).

| `check_id` | Role |
| ---------- | ---- |
| `metadata_schema_valid` | Metadata parses and validates. |
| `replay_file_readable` | Replay bytes readable. |
| `replay_sha256_computed` | SHA-256 computed. |
| `origin_class_declared` | Declared origin enum valid. |
| `provenance_status_declared` | Declared provenance enum valid. |
| `redistribution_posture_declared` | Declared redistribution enum valid. |
| `expected_hash_match` | `expected_replay_content_sha256` vs computed (if provided). |
| `binding_hash_match` | `replay_binding.replay_content_sha256` vs computed (if binding supplied). |
| `binding_identity_consistent` | Optional `run_identity` / `manifest` vs `replay_binding`. |
| `canonical_review_requirements_met` | Summary of final `intake_status`. |

**Status values:** `pass`, `warn`, `fail`, `not_evaluated`.  
**Severity values:** `required`, `warning`.

---

## 6. Metadata enums

### `declared_origin_class`

`starlab_generated`, `external`, `ladder_derived`, `third_party`, `unknown`

### `declared_acquisition_channel`

`direct_capture`, `download`, `generated`, `operator_supplied`, `unknown`

### `declared_provenance_status`

`asserted`, `verified`, `unknown`

### `declared_redistribution_posture`

`allowed`, `forbidden`, `unknown`

---

## 7. Intake status model

| Status | Meaning |
| ------ | ------- |
| `eligible_for_canonical_review` | Structurally valid; explicit provenance + redistribution posture; optional evidence consistent; **not** automatic corpus promotion. |
| `accepted_local_only` | Structurally valid; local/private experimentation acceptable; posture too weak for canonical review. |
| `quarantined` | Valid input but **forbidden** redistribution, **evidence conflict**, or unsafe contradiction. |
| `rejected` | Unreadable replay, invalid metadata, hash mismatch, malformed linked artifact, or hard failure. |

See `docs/starlab.md` — **Intake status glossary** for auditor-facing definitions.

---

## 8. CLI

```bash
python -m starlab.replays.intake_cli \
  --replay path/to/file.SC2Replay \
  --metadata path/to/replay_intake_metadata.json \
  --output-dir path/to/out \
  [--replay-binding path/to/replay_binding.json] \
  [--run-identity path/to/run_identity.json] \
  [--run-artifact-manifest path/to/manifest.json]
```

**Exit codes:** `0` → `eligible_for_canonical_review`; `2` → `accepted_local_only`; `3` → `quarantined`; `4` → `rejected`.

---

## 9. Implementation references

- `starlab/replays/intake_models.py` — schema + parsing  
- `starlab/replays/intake_policy.py` — pure policy evaluation  
- `starlab/replays/intake_io.py` — I/O + artifact assembly  
- `starlab/replays/intake_cli.py` — CLI entrypoint  
- `starlab/runs/replay_binding.py` — `load_replay_binding`  
- `starlab/runs/canonical_run_artifact.py` — `load_canonical_manifest` for M05 `manifest.json`  

---

## 10. Explicit non-claims

- M07 proves **deterministic** intake policy enforcement over **opaque** replay bytes and **declared** metadata.
- M07 does **not** prove replay parser correctness, replay semantic extraction, replay equivalence to execution proof, benchmark integrity, or live SC2 execution in CI.
- M07 records **declared** provenance posture; it does **not** certify external legal rights as a matter of law.
