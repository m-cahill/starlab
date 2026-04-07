# M06 Plan — Environment Drift & Runtime Smoke Matrix

**Milestone ID:** M06  
**Title:** Environment Drift & Runtime Smoke Matrix  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Status:** Complete (on `main`, merge `4953d7a5bbe0713ba82e03ea8f89da49a2f4147a`)  
**Target tag:** `v0.0.6-m06`  
**Branch name:** `m06-environment-drift-runtime-smoke-matrix`

---

## 1. Objective

Establish a **narrow, deterministic, CI-safe environment evidence surface** that:

1. defines a governed **runtime smoke matrix** for the current SC2 runtime boundary, and
2. evaluates an observed environment/probe result against that matrix to produce a deterministic **environment drift report**.

M06 should prove that STARLAB can detect and classify environment drift against declared expectations **without** claiming:

- cross-host reproducibility
- cross-install portability
- replay parser correctness
- replay semantic equivalence
- replay provenance finalization
- benchmark integrity
- new live SC2 execution in CI

This is an **environment evidence** milestone, not a new execution milestone.

---

## 2. Scope Lock

### In scope

1. **Contract doc**
   - Add `docs/runtime/environment_drift_smoke_matrix.md`

2. **Runtime smoke matrix contract**
   - Define a deterministic, versioned smoke-matrix artifact or emitted JSON structure
   - Separate:
     - CI-safe fixture expectations
     - local optional smoke expectations

3. **Environment drift evaluator**
   - Implement deterministic comparison of:
     - observed M01-style probe result
     - governed smoke matrix
     - optional M03 `environment_fingerprint` hint from `run_identity.json`

4. **CLI**
   - Add a small operator-facing CLI for drift evaluation

5. **Tests**
   - Unit tests
   - CLI tests
   - Fixture-driven end-to-end test
   - Governance/doc presence updates as needed

6. **Docs / ledger closeout**
   - Update `docs/starlab.md`
   - Finalize M06 milestone artifacts
   - Seed M07 stubs only after closeout

### Out of scope

- live SC2 execution in CI
- replay intake/provenance tightening (M07)
- replay parser substrate (M08)
- replay metadata/timeline/event extraction
- benchmark semantics / leaderboard claims
- any M07 implementation

---

## 3. Resolved Design Decisions

These decisions are locked up front unless implementation evidence forces a narrow adjustment.

### A. CI remains fixture-driven and SC2-free

M06 must **not** add live SC2 execution to CI.

CI should validate:
- contract shape
- deterministic evaluation logic
- fixture-driven drift classification

### B. Environment drift is evidence, not certification

M06 should produce a **drift report**, not a portability certificate.

It may say:
- pass
- warn
- fail
- not evaluated

It must **not** claim the environment is portable across hosts or installs.

### C. `environment_fingerprint` remains advisory

If `run_identity.json` includes an M03 `environment_fingerprint`, M06 may compare against it, but only as a **hint** / advisory evidence source.

A mismatch should not be framed as proof that execution is invalid across machines.

### D. Host-specific paths are not drift-breaking by default

Absolute paths and user-specific path strings should not be treated as canonical drift roots unless explicitly normalized into a stable comparable field.

Path differences may be recorded as advisory notes, not hard failures, unless a check is explicitly designed around normalized path-stable semantics.

### E. Built-in governed matrix first, no user-defined matrix DSL in M06

M06 should ship with a STARLAB-owned default matrix / profile structure.

Do **not** add a general user-extensible matrix language in M06.

### F. Local smoke expectations are defined, not merge-gated

M06 should define local optional smoke expectations, but they should not become required CI gates.

Optional local operator evidence may be captured later, but it is not required for the milestone to merge.

---

## 4. Proposed Artifacts

### 4.1 Runtime smoke matrix artifact

Proposed emitted file:

`runtime_smoke_matrix.json`

Minimum shape:

```json
{
  "schema_version": "starlab.runtime_smoke_matrix.v1",
  "runtime_boundary_label": "<string>",
  "profiles": {
    "ci_fixture": {
      "required_checks": ["probe_schema_valid", "runtime_boundary_label_present"]
    },
    "local_optional": {
      "required_checks": ["probe_schema_valid", "runtime_boundary_label_present"],
      "warning_checks": ["adapter_name_present", "base_build_captured", "data_version_captured"]
    }
  },
  "later_milestones": [
    "M07 replay intake policy & provenance enforcement",
    "M08 replay parser substrate"
  ]
}
```

Notes:

* The exact check names may tighten during implementation.
* The matrix should be deterministic and versioned.
* Prefer a builder-emitted artifact rather than a hand-maintained JSON blob.

### 4.2 Environment drift report artifact

Proposed emitted file:

`environment_drift_report.json`

Minimum shape:

```json
{
  "schema_version": "starlab.environment_drift_report.v1",
  "runtime_boundary_label": "<string>",
  "profile": "ci_fixture",
  "overall_status": "pass",
  "check_results": [
    {
      "check_id": "probe_schema_valid",
      "status": "pass",
      "severity": "required",
      "expected": "valid probe payload",
      "observed": "valid probe payload"
    }
  ],
  "advisory_notes": [],
  "environment_fingerprint_used": false,
  "later_milestones": [
    "M07 replay intake policy & provenance enforcement",
    "M08 replay parser substrate"
  ]
}
```

Recommended statuses:

* `pass`
* `warn`
* `fail`
* `not_evaluated`

Recommended overall-status rule:

* `fail` if any required check fails
* `warn` if no required check fails but one or more warning checks warn/fail
* `pass` if required checks pass and no warnings are raised

---

## 5. Proposed Inputs

### Required input

* observed probe JSON from the M01 runtime/probe surface

### Optional input

* `run_identity.json` from M03, if `environment_fingerprint` is present

### Recommended CLI

```bash
python -m starlab.sc2.evaluate_environment_drift \
  --probe path/to/probe_result.json \
  --output-dir path/to/out
```

Optional extension:

```bash
python -m starlab.sc2.evaluate_environment_drift \
  --probe path/to/probe_result.json \
  --run-identity path/to/run_identity.json \
  --output-dir path/to/out
```

Behavior:

1. load and validate observed probe JSON
2. build deterministic default `runtime_smoke_matrix.json`
3. evaluate observed probe against the chosen profile
4. optionally compare probe fields with `environment_fingerprint`
5. emit deterministic `environment_drift_report.json`

Do not add replay/proof/config inputs in M06.

---

## 6. Implementation Plan

### Step 1 — Add the contract doc

Create `docs/runtime/environment_drift_smoke_matrix.md` describing:

* what M06 proves
* what M06 does not prove
* smoke matrix purpose and profiles
* drift report semantics
* required vs advisory checks
* relationship to M01 environment lock, M03 environment fingerprint, and later milestones
* worked fixture example

### Step 2 — Add matrix/evaluator code

Likely under `starlab/sc2/`:

* `environment_drift.py`
* `runtime_smoke_matrix.py` or equivalent helper module
* stable loaders / validators for observed probe inputs
* deterministic report builder

Keep this additive and narrow.

### Step 3 — Add CLI

Suggested new module:

* `starlab/sc2/evaluate_environment_drift.py`

Avoid importing the CLI from package `__init__`.

### Step 4 — Add fixtures

Prefer adding:

* one valid probe fixture with no drift
* one warning drift fixture
* one failing drift fixture

If needed:

* one `run_identity.json` fixture carrying an `environment_fingerprint`

Keep fixtures small, deterministic, and SC2-free.

### Step 5 — Add tests

At minimum:

1. `tests/test_environment_drift.py`

   * matrix generation stability
   * deterministic report generation
   * required-check failure behavior
   * warning classification behavior
   * optional environment fingerprint comparison behavior

2. `tests/test_evaluate_environment_drift_cli.py`

   * successful report generation
   * deterministic repeated outputs
   * missing file rejection
   * malformed probe rejection
   * invalid run-identity rejection, if optional support is included

3. End-to-end fixture test

   * load probe fixture
   * emit smoke matrix
   * emit drift report
   * verify identical outputs across repeated runs

4. Governance test updates

   * contract doc/module/CLI presence

### Step 6 — Optional local evidence note

If practical and available without destabilizing scope, Cursor may add a small redacted local note or sample under milestone docs demonstrating the evaluator on one local observed probe.

This is **supplemental** only, not a merge gate.

---

## 7. Candidate Checks

Actual checks should remain constrained to fields the current probe surface already exposes, but the expected check classes are:

* probe payload/schema valid
* runtime boundary label present
* adapter name present
* base build captured or explicitly unknown
* data version captured or explicitly unknown
* optional `environment_fingerprint` field alignment
* profile-defined CI-safe smoke expectations
* profile-defined local optional smoke expectations

Do not invent broad new probe semantics unless implementation evidence shows a small additive improvement is necessary.

---

## 8. End-to-End Evidence Target

The authoritative M06 proof surface should be:

1. load a deterministic probe fixture
2. emit the default runtime smoke matrix
3. evaluate the probe against that matrix
4. optionally compare against a fixture-backed `environment_fingerprint`
5. rerun with identical inputs
6. confirm byte-stable or semantically identical deterministic outputs for:

   * `runtime_smoke_matrix.json`
   * `environment_drift_report.json`

This proves governed environment evidence, not runtime portability certification.

---

## 9. Acceptance Criteria

M06 is complete only when all of the following are true:

1. `docs/runtime/environment_drift_smoke_matrix.md` exists and matches implementation
2. `runtime_smoke_matrix.json` is emitted deterministically
3. `environment_drift_report.json` is emitted deterministically
4. required vs advisory drift classification is explicit and tested
5. CI remains SC2-free and fixture-driven
6. no required checks are weakened
7. the milestone does not widen into parser / provenance / benchmark scope
8. `docs/starlab.md` is updated at closeout
9. M07 remains stub-only after M06 closeout

---

## 10. Explicit Non-Claims for M06

The milestone summary, audit, and ledger must explicitly state that M06 does **not** prove:

* cross-host reproducibility
* cross-install portability
* new live SC2 CI execution
* replay parser correctness
* replay semantic extraction
* replay provenance finalization
* benchmark integrity

M06 proves **environment drift evaluation and smoke expectations**, not broad runtime certification.

---

## 11. Candidate File Change List

Expected changes, subject to implementation detail:

* `docs/runtime/environment_drift_smoke_matrix.md` **(new)**
* `starlab/sc2/environment_drift.py` **(new)**
* `starlab/sc2/evaluate_environment_drift.py` **(new)**
* `starlab/sc2/runtime_smoke_matrix.py` **(new, if needed)**
* `tests/test_environment_drift.py` **(new)**
* `tests/test_evaluate_environment_drift_cli.py` **(new)**
* `tests/test_governance.py`
* `tests/fixtures/...` **(new fixtures)**
* `docs/starlab.md`
* milestone docs under `docs/company_secrets/milestones/M06/`

---

## 12. CI / Guardrails

1. do not add live SC2 requirements to CI
2. do not add replay parsing to M06
3. do not turn local smoke expectations into required CI execution
4. do not weaken required checks
5. do not close the milestone before the ledger is updated
6. avoid needless post-closeout churn

   * seed M07 stubs only after M06 is formally closed
   * any follow-up after closeout belongs on the next milestone branch

---

## 13. Closeout Requirements for Cursor

At closeout, Cursor must produce:

* `M06_run1.md`
* `M06_summary.md`
* `M06_audit.md`

And must verify:

* PR-head CI green on the final branch tip
* post-merge `main` CI green on the merge commit
* `docs/starlab.md` updated with:

  * M06 proved claim
  * M06 non-claims
  * closeout ledger row
  * changelog entry
* `docs/company_secrets/milestones/M07/M07_plan.md` stub exists
* `docs/company_secrets/milestones/M07/M07_toolcalls.md` stub exists
* **no M07 implementation** is included

---

## 14. Milestone Summary Target

Desired honest summary line at closeout:

> M06 proved that STARLAB can deterministically evaluate observed runtime/probe evidence against a governed smoke matrix and emit a stable environment drift report, without claiming runtime portability, replay parsing, provenance closure, benchmark integrity, or live SC2 execution in CI.
