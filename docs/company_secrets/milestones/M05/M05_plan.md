# M05 Plan — Canonical Run Artifact v0

**Milestone ID:** M05  
**Title:** Canonical Run Artifact v0  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Status:** **Complete on `main`** ([PR #6](https://github.com/m-cahill/starlab/pull/6); merge commit `bad27db36c135fd772e38dcafa64d6fa59577db0`)  
**Target tag:** `v0.0.5-m05`  
**Branch name:** `m05-canonical-run-artifact-v0` (**merged**; remote **deleted**)

---

## 1. Objective

Establish the first **canonical package boundary** for STARLAB-owned run records by packaging the existing M03 and M04 artifacts into one deterministic, reviewable, CI-safe **canonical run artifact v0**.

M05 should prove that STARLAB can take already-derived records and emit a stable, content-addressed package that becomes the first governed run bundle boundary.

This milestone must **not** claim:

- replay parser correctness
- replay semantic equivalence
- replay event extraction
- new live SC2 execution in CI
- benchmark integrity
- cross-host reproducibility

---

## 2. Scope Lock

### In scope

1. **Contract doc** — `docs/runtime/canonical_run_artifact_v0.md`
2. **Canonical run artifact builder** — `starlab/runs/canonical_run_artifact.py` (deterministic directory bundle)
3. **CLI** — `python -m starlab.runs.build_canonical_run_artifact`
4. **Validation** — coherence across `run_identity.json`, `lineage_seed.json`, `replay_binding.json`
5. **Tests** — unit, CLI, fixture-driven e2e; governance/doc presence
6. **Docs / ledger** — `docs/starlab.md` at closeout; milestone artifacts under `docs/company_secrets/milestones/M05/`

### Out of scope

- replay parser substrate
- replay metadata / timeline / event extraction
- raw replay inclusion in the canonical package
- raw proof/config inclusion in the canonical package
- benchmark semantics
- new SC2 execution proof in CI
- M06 implementation

### Locked implementation choices (2026-04-06)

1. Reject `--output-dir` if it already exists; **no** `--force` / overwrite in M05.
2. Keep `parent_references` as `[]` in the M05 manifest.
3. Golden expected outputs under `tests/fixtures/m05_expected/`.
4. E2e proof derives the full chain through APIs: M02 fixtures → M03 → M04 replay binding → M05 bundle.
5. `included_artifacts` must match the canonical v0 list **exactly** (order-sensitive); silent shape drift is rejected.

---

## 3. Resolved Design Decisions

### A. M05 packages STARLAB-owned records, not raw external assets

Include: `run_identity.json`, `lineage_seed.json`, `replay_binding.json`, bundle manifest, hashes file.  
Do **not** include: raw replay bytes, raw proof JSON, raw match config JSON, maps or other SC2 assets.

### B. M05 consumes M03/M04 artifacts only

CLI accepts only the three JSON paths above plus `--output-dir`. It does **not** accept replay path, proof path, or config path.

### C. M05 is a deterministic directory bundle, not an archive format

No `.zip` / `.tar.gz` in M05.

### D. M05 canonicalizes included JSON on write

Load, validate, re-emit canonical JSON (no blind byte copy).

### E. No timestamps in the canonical artifact manifest

### F. Fail fast on mismatched upstream artifacts

---

## 4. Proposed Artifact Shape

Directory bundle:

```text
canonical_run_artifact/
  manifest.json
  run_identity.json
  lineage_seed.json
  replay_binding.json
  hashes.json
```

---

## 5. Proposed Contract

See `docs/runtime/canonical_run_artifact_v0.md` for:

- `manifest.json` minimum fields (`schema_version` `starlab.canonical_run_artifact.v0`, `bundle_mode` `starlab_owned_records_only`, identity fields, `included_artifacts`, `external_references`, `parent_references` `[]`, `later_milestones`)
- `hashes.json` (`schema_version` `starlab.canonical_run_artifact.hashes.v0`, `artifact_hashes`, `run_artifact_id`)
- `run_artifact_id` derivation: compact canonical JSON over `{ "artifact_hashes": { ... sorted ... }, "kind": "starlab.canonical_run_artifact.v0" }` with `hashes.json` excluded from per-file hashing

---

## 6. Coherence Rules

Validate M03/M04 schemas, cross-field IDs (`run_spec_id`, `execution_id`, `lineage_seed_id`, `proof_artifact_hash`), replay binding internal consistency (`binding_mode`, `replay_binding_id`), and canonical `included_artifacts` list. Output directory must not exist. No partial success claim on validation failure.

---

## 7. CLI

```bash
python -m starlab.runs.build_canonical_run_artifact \
  --run-identity path/to/run_identity.json \
  --lineage-seed path/to/lineage_seed.json \
  --replay-binding path/to/replay_binding.json \
  --output-dir path/to/out
```

Do not import the CLI from package `__init__` (same posture as M03/M04).

---

## 8. Implementation Plan

1. Add `docs/runtime/canonical_run_artifact_v0.md`
2. Add `starlab/runs/canonical_run_artifact.py`, `starlab/runs/build_canonical_run_artifact.py`
3. Add `load_replay_binding` validation in `starlab/runs/replay_binding.py`
4. Tests: `tests/test_canonical_run_artifact.py`, `tests/test_build_canonical_run_artifact_cli.py`, golden `tests/fixtures/m05_expected/`
5. Update `tests/test_governance.py`, `docs/starlab.md` at closeout

---

## 9. End-to-End Evidence Target

Derive M03 from fixtures, M04 from synthetic replay bytes, build M05 bundle twice, confirm identical outputs and `run_artifact_id`.

---

## 10. Acceptance Criteria

1. Contract doc exists and matches implementation  
2. Deterministic directory emission  
3. Stable `run_artifact_id` across repeated runs  
4. Coherence validation rejects mismatched upstream artifacts  
5. Canonical re-emission (not raw copy)  
6. No raw replay bytes or raw proof/config in bundle  
7. CLI tested; CI green  
8. `docs/starlab.md` updated at closeout  
9. M06 remains stub-only until M06 kickoff (no M06 implementation in M05 PR)

---

## 11. Explicit Non-Claims for M05

M05 does **not** prove: replay parser correctness, replay semantic equivalence, replay event extraction, replay provenance finalization, benchmark integrity, cross-host reproducibility, new live SC2 execution in CI.

---

## 12. Candidate File Change List

- `docs/runtime/canonical_run_artifact_v0.md` **(new)**
- `starlab/runs/canonical_run_artifact.py` **(new)**
- `starlab/runs/build_canonical_run_artifact.py` **(new)**
- `starlab/runs/replay_binding.py` **(load_replay_binding)**
- `tests/test_canonical_run_artifact.py` **(new)**
- `tests/test_build_canonical_run_artifact_cli.py` **(new)**
- `tests/fixtures/m05_expected/*` **(new)**
- `tests/test_governance.py`, `tests/test_replay_binding.py`
- `docs/starlab.md`
- `docs/company_secrets/milestones/M05/M05_plan.md`, `M05_toolcalls.md`

---

## 13. CI / Guardrails

Do not add live SC2 to CI, replay parsing, or raw replay bytes in the bundle. Do not weaken required checks. Closeout updates stay minimal; seed M06 stubs only after formal M05 closeout.

---

## 14. Closeout Requirements for Cursor

At closeout: `M05_run1.md`, `M05_summary.md`, `M05_audit.md`; PR-head + post-merge `main` CI green; `docs/starlab.md` with proved/non-claims, ledger row, changelog; `M06` plan/toolcalls stubs if not already present; **no** M06 implementation.

---

## 15. Milestone Summary Target

> M05 proved the first canonical STARLAB run package boundary by deterministically packaging M03 identity records and the M04 replay-binding record into a stable, content-addressed canonical run artifact v0, without parsing replay semantics, shipping raw replay assets, or making benchmark claims.
