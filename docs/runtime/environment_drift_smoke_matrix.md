# Environment drift and runtime smoke matrix (M06)

This document defines the **M06** contract: a **governed runtime smoke matrix** and **deterministic environment drift report** built on top of the **M01** probe surface and optional **M03** `environment_fingerprint` hint.

**M06 does not add replay parsing, provenance finalization, benchmark semantics, or live SC2 execution in CI.** CI remains **fixture-driven** and **SC2-free**.

---

## What M06 proves

- STARLAB can emit a **deterministic, versioned** `runtime_smoke_matrix.json` describing **CI-safe** and **local optional** check profiles.
- STARLAB can evaluate an **observed M01 probe JSON** against that matrix and emit a **deterministic** `environment_drift_report.json` with explicit per-check status (`pass`, `warn`, `fail`, `not_evaluated`) and an overall status (`pass`, `warn`, `fail`).
- When **`run_identity.json`** is supplied and contains a non-empty **`environment_fingerprint`**, STARLAB can compare **overlapping** fields (`runtime_boundary_label`, `base_build`, `data_version`) as **warning-class** drift signals, while treating **`adapter_name`**, **`platform_string`**, and **`probe_digest`** as **advisory context** (not hard drift roots by default in M06).
- The report includes **`fingerprint_comparison_performed`** (whether a `run_identity` file was loaded) and **`environment_fingerprint_used`** (whether a non-empty fingerprint object was present), so audits can distinguish “no identity file” from “identity file without fingerprint.”

---

## What M06 does not prove

- **Cross-host reproducibility** or **cross-install portability** of SC2 or STARLAB execution.
- **Replay parser correctness**, **replay semantic equivalence**, or **replay event extraction**.
- **Replay provenance finalization** or **intake policy enforcement** (M07+).
- **Benchmark integrity** or leaderboard claims.
- **New live SC2 execution in CI** (CI remains fixture-driven).

`environment_fingerprint` remains a **hint**, not a portability lock (see M03 contract).

---

## Artifacts

### `runtime_smoke_matrix.json`

- **Schema:** `schema_version` = `starlab.runtime_smoke_matrix.v1`
- **`runtime_boundary_label`:** derived from the observed probe’s `spec.control_observation_surface` when valid; otherwise empty string for matrix emission context.
- **`profiles`:**
  - **`ci_fixture`:** required checks only (deterministic CI gate on fixtures).
  - **`local_optional`:** required checks plus **warning-class** checks (e.g. optional capture hints); **not** a merge gate by default.

### `environment_drift_report.json`

- **Schema:** `schema_version` = `starlab.environment_drift_report.v1`
- **`profile`:** `ci_fixture` or `local_optional`
- **`runtime_boundary_label`:** same derivation as the matrix (probe-derived boundary string).
- **`check_results`:** ordered list of checks with `severity` (`required` vs `warning`) and `status`.
- **`advisory_notes`:** sorted strings for fingerprint-only or contextual hints.
- **`fingerprint_comparison_performed`:** `true` if `--run-identity` was provided and parsed.
- **`environment_fingerprint_used`:** `true` if a non-empty `environment_fingerprint` object was present.

---

## Profiles and checks (summary)

| Profile | Role |
| ------- | ---- |
| `ci_fixture` | Default CLI profile; validates required probe + boundary checks on fixtures. |
| `local_optional` | Adds warning-class checks (e.g. optional capture hints, fingerprint-derived adapter name when fingerprint exists). |

**`probe_schema_valid`:** deterministic structural validation of the M01 probe JSON (required keys/types, nested `spec`, and canonical `control_observation_surface` / `replay_decode_surface` values matching `Sc2RuntimeSpec`).

**`runtime_boundary_label_present`:** required check that the probe’s control/observation surface matches the canonical M01 boundary string.

**`adapter_name_present`:** evaluated only from `environment_fingerprint.adapter_name` when a non-empty fingerprint exists; otherwise **`not_evaluated`**. Warning-class.

**Fingerprint overlap checks** (when fingerprint present): `fingerprint_runtime_boundary_match`, `fingerprint_base_build_match`, `fingerprint_data_version_match` — **warning** severity; mismatches contribute to overall **`warn`**, not required CI failure for the default `ci_fixture` profile when run without local-only expectations.

---

## Relationship to other milestones

- **M01:** probe shape and canonical runtime surfaces.
- **M03:** optional `environment_fingerprint` (advisory); compared only as governed evidence, not certification.
- **M07 / M08:** listed under `later_milestones` in emitted JSON; **no** implementation in M06.

---

## CLI

```bash
python -m starlab.sc2.evaluate_environment_drift \
  --probe path/to/probe_result.json \
  --output-dir path/to/out \
  [--run-identity path/to/run_identity.json] \
  [--profile ci_fixture|local_optional]
```

Default **`--profile`** is **`ci_fixture`**.

---

## Worked fixture example (conceptual)

1. Load `tests/fixtures/probe_m06_valid.json` (valid M01 probe surface).
2. Run the CLI with `--profile ci_fixture` and an output directory.
3. Inspect `runtime_smoke_matrix.json` and `environment_drift_report.json`; repeat the command and confirm **byte-identical** outputs for identical inputs.
