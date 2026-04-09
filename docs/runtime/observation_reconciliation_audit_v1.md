# Observation Reconciliation Audit v1 (M19)

## Purpose

Define the **deterministic cross-mode audit** between **one** M16 `canonical_state.json` (Mode A) and **one** M18 `observation_surface.json` (Mode B) at the same `gameloop` and `perspective_player_index`, plus optional upstream reports, emitting `observation_reconciliation_audit.json` and `observation_reconciliation_audit_report.json`.

M19 proves **fixture-backed reconciliation classification** — **not** replay parsing in `starlab/observation/`, **not** action legality, **not** benchmark integrity, **not** live SC2 in CI.

## Required inputs

* **`canonical_state.json`** (M16) — semantic upstream for expected observation (M18 derivation replay).
* **`observation_surface.json`** — must validate against the M17 observation JSON Schema (`validate_observation_surface_frame`).

## Optional inputs

* **`canonical_state_report.json`** (M16) — if present: `canonical_state_sha256` must match the SHA-256 of canonical JSON of the loaded `canonical_state.json` (same rule as M18).
* **`observation_surface_report.json`** (M18 materialization report) — if present: when fields are present and well-typed, cross-checks may include `observation_surface_sha256` vs loaded observation, `source_canonical_state_sha256`, `gameloop`, and `perspective_player_index`.

## Exact output filenames (per invocation)

* `observation_reconciliation_audit.json`
* `observation_reconciliation_audit_report.json`

Serialization: **`canonical_json_dumps`** (sorted keys, stable UTF-8, trailing newline).

## Audit status vocabulary

Each audited mapping is classified as one of:

| Status | Meaning |
| ------ | ------- |
| `exact` | Value matches M18 expectation and is a direct carry-through from canonical perspective fields (or faithful omission of zero-valued aggregates). |
| `derived` | Value matches M18 expectation from a deterministic transform (e.g. list lengths, prototype action-mask heuristics). |
| `bounded_lossy` | Value matches expectation but is explicitly bounded / proxy / category-level — not full game truth. |
| `unavailable_by_design` | Representation intentionally omits or nulls a signal (e.g. missing visibility proxy with observation null). |
| `mismatch` | Observation value or structure does not match M18 deterministic expectation from the supplied canonical state. |

## Deterministic ordering rules

* **Scalar audit rows:** `ORDERED_SCALAR_FEATURE_NAMES` in `observation_surface_catalog.py` (M17 catalog order).
* **Entity audit rows:** Same order as `entity_rows.rows` in the observation (mirrors M18 emission order).
* **Spatial audit rows:** Plane order as in `spatial_plane_family.planes`.
* **Action-mask audit rows:** `ACTION_MASK_FAMILY_NAMES` catalog order.
* **Report `failures` and `warnings`:** Sorted lexicographically (stable string keys).

## Report vocabulary

* **`audit_verdict`:** `pass` | `pass_with_warnings` | `fail`
* **`failures`:** Machine-oriented failure keys (identity, provenance, or unexpected `mismatch`).
* **`warnings`:** Bounded / derivation / scalar semantic warnings (not upstream-only).
* **`upstream_warnings`:** Propagated strings from supplied reports (labeled by origin).

## Failure conditions (CLI exit non-zero)

Exit code **2** when:

* Invalid JSON or non-object root.
* Observation fails M17 schema validation.
* Identity/provenance contradiction (gameloop, `source_canonical_state_sha256`, optional report hash fields when supplied and typed).
* Any audited row has `reconciliation_status` **`mismatch`** after representation comparison.
* Internal emission error.

Exit code **0** when `audit_verdict` is `pass` or `pass_with_warnings`.

**Not** a failure: rows classified `bounded_lossy` or `unavailable_by_design` when values match M18 expectation (warnings only).

## Explicit non-claims

M19 does **not** prove:

* Replay bundle loading, replay parsing, or `s2protocol` in M19 modules.
* Action legality, full SC2 action coverage, or benchmark integrity.
* Certified fog-of-war truth or exact banked resources beyond prior bounded planes.
* Replay↔execution equivalence.
* Semantic correctness of spatial planes beyond structural prototype alignment.

## Relation to M15–M18

* **M15:** Canonical state schema only — M19 does not re-validate schema beyond tooling use.
* **M16:** Canonical state frame is the Mode A truth for reconciliation.
* **M17:** Observation contract / schema — Mode B must validate.
* **M18:** Expected observation is the **deterministic M18 derivation** from the same canonical state and `source_canonical_state_sha256`; M19 classifies how the supplied observation aligns with that expectation.

## CLI

```text
python -m starlab.observation.audit_observation_surface \
  --canonical-state PATH \
  --observation-surface PATH \
  --output-dir OUT \
  [--canonical-state-report PATH] \
  [--observation-surface-report PATH]
```
