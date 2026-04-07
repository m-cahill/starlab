# M04 Plan — Replay Binding to Run Identity

**Milestone ID:** M04  
**Title:** Replay Binding to Run Identity  
**Phase:** I — Governance, Runtime Surface, and Deterministic Run Substrate  
**Status:** Complete on `main`  
**Target tag:** `v0.0.4-m04`  
**Branch name:** `m04-replay-binding-to-run-identity`

---

## 1. Objective

Add a **narrow, deterministic, CI-safe replay binding surface** that links a replay file's identity to the existing M03 records:

- `run_spec_id`
- `execution_id`
- `lineage_seed_id`

This milestone must prove that STARLAB can create a stable, reviewable `replay_binding.json` record for a supplied replay file **without** claiming:

- replay parser correctness
- replay semantic extraction
- canonical run artifact v0
- benchmark validity
- cross-host reproducibility

---

## 2. Scope Lock

### In scope

1. **Contract doc**
   - Add `docs/runtime/replay_binding.md`
   - Define the M04 artifact, hashing rules, validation posture, and non-claims

2. **Replay binding record**
   - Add deterministic replay binding logic in `starlab/runs/`
   - Emit `replay_binding.json`

3. **Opaque replay identity**
   - Treat replay input as **opaque file bytes**
   - Compute `replay_content_sha256`
   - Record replay metadata suitable for human review:
     - basename
     - suffix
     - size in bytes

4. **Binding ID derivation**
   - Derive a STARLAB-owned `replay_binding_id` from canonical JSON using existing M03 IDs plus replay content hash

5. **CLI**
   - Add a small CLI for operators, likely:
     - `python -m starlab.runs.bind_replay`
   - CLI should consume existing M03 artifacts plus a replay path and emit `replay_binding.json`

6. **Tests**
   - Unit tests
   - CLI test
   - Fixture-driven end-to-end test
   - Governance/doc presence tests as needed

7. **Docs / ledger closeout**
   - Update `docs/starlab.md`
   - Finalize M04 summary / audit / run analysis
   - Seed M05 stubs only after closeout

### Out of scope

- Replay parser substrate
- Replay metadata extraction beyond opaque file facts
- Replay event/timeline semantics
- Canonical run artifact v0
- New live SC2 execution proof in CI
- Benchmark semantics or leaderboard claims
- Any M05 implementation

---

## 3. Resolved Assumptions

These are resolved up front so Cursor does not need to reopen them unless implementation evidence forces it:

1. **M04 replay identity is content-first**
   - Identity is derived from replay bytes, not absolute paths

2. **Replay is opaque in M04**
   - M04 does not parse `.SC2Replay` semantics
   - A synthetic replay fixture is acceptable in CI

3. **Filename is metadata, not identity**
   - Basename/suffix may be recorded for operator review
   - They should not be required inputs to the replay-binding hash unless implementation evidence strongly justifies it

4. **M03 remains the upstream prerequisite**
   - M04 binds to existing M03 records
   - M04 should not redefine M03 claims

5. **CI remains SC2-free**
   - Use fixtures and synthetic replay bytes in CI
   - Do not add a live SC2 runtime dependency to CI for M04

---

## 4. Proposed Artifact Contract

### New artifact

`replay_binding.json`

### Minimum fields

```json
{
  "schema_version": "starlab.replay_binding.v1",
  "replay_binding_id": "<hex>",
  "run_spec_id": "<hex>",
  "execution_id": "<hex>",
  "lineage_seed_id": "<hex>",
  "proof_artifact_hash": "<hex>",
  "replay_content_sha256": "<hex>",
  "replay_reference": {
    "basename": "example.SC2Replay",
    "suffix": ".SC2Replay",
    "size_bytes": 1234
  },
  "binding_mode": "opaque_content_sha256",
  "parent_references": [],
  "later_milestones": [
    "M05 canonical run artifact v0",
    "M08 replay parser substrate"
  ]
}
```

### Proposed binding hash payload

`replay_binding_id` should be derived from canonical JSON like:

```json
{
  "kind": "starlab.replay_binding.v1",
  "run_spec_id": "<hex>",
  "execution_id": "<hex>",
  "lineage_seed_id": "<hex>",
  "proof_artifact_hash": "<hex>",
  "replay_content_sha256": "<hex>"
}
```

### Important posture

* `replay_content_sha256` is the replay-file identity primitive for M04
* `replay_binding_id` is the STARLAB-owned linkage record
* `replay_reference` is informational metadata, not the identity root

---

## 5. Implementation Plan

### Step 1 — Add the contract doc

Create `docs/runtime/replay_binding.md` with:

* what M04 proves
* what M04 does not prove
* replay identity definitions
* hashing rules
* emitted artifact shape
* relationship to M03 and M05
* worked example using synthetic fixture inputs

### Step 2 — Add replay binding models / helpers

Likely under `starlab/runs/`:

* replay reference model
* replay hash helper
* replay binding record builder
* deterministic writer

Keep this additive and narrow.

### Step 3 — Add CLI

Preferred operator flow:

```bash
python -m starlab.runs.bind_replay \
  --run-identity /path/to/run_identity.json \
  --lineage-seed /path/to/lineage_seed.json \
  --replay /path/to/replay.SC2Replay \
  --output-dir /path/to/out
```

Behavior:

* load and validate M03 artifacts
* compute replay content SHA-256
* derive `replay_binding_id`
* write deterministic `replay_binding.json`

Avoid importing the CLI from package `__init__`, same posture as M03.

### Step 4 — Add fixtures

Prefer this fixture strategy:

* reuse M03 proof/config fixtures where possible
* generate M03 artifacts in test setup rather than committing redundant copies
* commit **one** synthetic replay fixture, clearly marked as synthetic and not a Blizzard replay

If existing M03 fixtures are awkward for replay-flow testing, add a **dedicated M04 fixture set** rather than mutating M03 fixtures.

### Step 5 — Add tests

Add at minimum:

1. `tests/test_replay_binding.py`

   * replay content hash is stable
   * binding ID is stable
   * writer emits deterministic JSON

2. `tests/test_bind_replay_cli.py`

   * CLI writes expected artifact
   * failure mode coverage for bad paths / malformed upstream artifacts

3. End-to-end fixture test

   * derive M03 artifacts
   * bind synthetic replay
   * verify identical outputs across repeated runs

4. Governance test updates

   * doc presence / ledger references if existing governance suite covers them

### Step 6 — Update docs and ledger on closeout

At closeout update:

* `docs/starlab.md` §10
* `docs/starlab.md` §11
* `docs/starlab.md` §18
* `docs/starlab.md` §20
* `docs/starlab.md` §23

---

## 6. End-to-End Evidence Target

M04 should have one clear CI-safe end-to-end proof:

1. Generate or load valid M03 identity artifacts
2. Bind a synthetic replay file
3. Emit `replay_binding.json`
4. Re-run with identical inputs
5. Observe identical `replay_content_sha256` and identical `replay_binding_id`

This is the authoritative M04 proof surface.

---

## 7. Acceptance Criteria

M04 is complete only when all of the following are true:

1. `docs/runtime/replay_binding.md` exists and matches implementation
2. `replay_binding.json` is emitted deterministically from fixture-driven inputs
3. `replay_binding_id` is stable across repeated runs with identical inputs
4. Replay binding correctly references:

   * `run_spec_id`
   * `execution_id`
   * `lineage_seed_id`
   * `proof_artifact_hash`
5. CLI is tested and green
6. Pytest, Ruff, format, MyPy, pip-audit, SBOM, Gitleaks remain green
7. No required checks are weakened
8. `docs/starlab.md` is updated at closeout
9. M04 summary and audit explicitly state the **narrow claim**
10. M05 remains stub-only after M04 closeout

---

## 8. Explicit Non-Claims for M04

The milestone summary, audit, and ledger must explicitly state that M04 does **not** prove:

* replay parser correctness
* replay semantic equivalence to execution proof
* replay event extraction
* canonical run artifact v0
* benchmark integrity
* cross-host reproducibility
* new live SC2 runtime execution in CI

---

## 9. Candidate File Change List

Expected changes, subject to implementation detail:

* `docs/runtime/replay_binding.md` **(new)**
* `starlab/runs/replay_binding.py` **(new)**
* `starlab/runs/bind_replay.py` **(new)**
* `starlab/runs/__init__.py` *(only if needed; avoid CLI import side effects)*
* `tests/test_replay_binding.py` **(new)**
* `tests/test_bind_replay_cli.py` **(new)**
* `tests/fixtures/...synthetic replay fixture...` **(new)**
* `tests/test_governance.py` *(if governance assertions need extension)*
* `docs/starlab.md`
* milestone docs under `docs/company_secrets/milestones/M04/`

---

## 10. CI / Guardrails

1. **Do not add a new CI workflow unless truly necessary**

   * Prefer extending existing `CI`

2. **Do not add live SC2 requirements to CI**

   * M04 must remain fixture-driven

3. **Do not weaken required checks**

   * No `continue-on-error`
   * No coverage carve-outs without explicit audit rationale

4. **Do not close the milestone before the ledger is updated**

   * `docs/starlab.md` is the living public ledger

5. **Avoid needless post-closeout churn**

   * Keep closeout commits minimal
   * Seed M05 stubs only after M04 is formally closed
   * Any follow-up work after closeout belongs on the next branch

---

## 11. Closeout Requirements for Cursor

At milestone closeout, Cursor must produce:

* `M04_run1.md`
* `M04_summary.md`
* `M04_audit.md`

And must verify:

* PR-head CI green on the final branch tip
* post-merge `main` CI green on the merge commit
* `docs/starlab.md` updated with:

  * M04 proved claim
  * M04 non-claims
  * closeout ledger row
  * changelog entry
* `docs/company_secrets/milestones/M05/M05_plan.md` stub exists
* `docs/company_secrets/milestones/M05/M05_toolcalls.md` stub exists
* **no M05 implementation** is included

---

## 12. Milestone Summary Target

Desired honest summary line at closeout:

> M04 proved narrow, deterministic replay binding at the level of replay file content identity linked to existing M03 run identity / lineage seed records, using CI-safe fixture inputs. M04 did not prove replay parsing, replay semantics, or canonical run artifact packaging.
