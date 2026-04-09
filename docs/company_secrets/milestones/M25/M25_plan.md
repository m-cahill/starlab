# M25 Plan — Baseline Evidence Pack

**Milestone:** M25  
**Phase:** IV — Benchmark Contracts, Baselines, and Evaluation  
**Status:** **Complete** — merged to `main` ([PR #31](https://github.com/m-cahill/starlab/pull/31)); merge commit `f03c7bf4337b61ea0f88ff07aa5b4adb2c88850b`; see `M25_run1.md`, `M25_summary.md`, `M25_audit.md`.

## Objective

Prove a deterministic, offline, fixture-only **baseline evidence-pack** layer over the governed Phase IV chain. Keep M25 narrow: it should **package and explain existing governed baseline evidence** from M21/M22 suites, M23 tournament output, and M24 diagnostics output. It should **not** introduce new benchmark semantics, new scoring, benchmark-integrity claims, replay↔execution claims, live SC2, or any new baseline execution surface.

## Scope decisions (locked)

1. **Use governed upstream artifacts only.**
   Required inputs:

   * one or more governed `scripted_baseline_suite.json` / `heuristic_baseline_suite.json` artifacts from M21/M22
   * one governed `evaluation_tournament.json` from M23
   * one governed `evaluation_diagnostics.json` from M24
     Optional companions can be the corresponding `*_report.json` files for warning propagation and hash cross-checks only.

2. **JSON pack, not archive packaging.**
   For v1, emit deterministic JSON artifacts only. Do not add zip/tar/archive semantics, copied raw fixtures, or file-bundle transport concerns.

3. **One pack per governed tournament chain.**
   M25 should package **one** M23 tournament + **one** matching M24 diagnostics artifact + the exact M21/M22 suite artifacts that cover that entrant set.

4. **Diagnostics are required.**
   M25 should not create an "evidence pack without diagnostics" variant in v1. That keeps the milestone small and aligned with the M23 → M24 → M25 progression.

## Deliverables

Add a new runtime contract:

* `docs/runtime/baseline_evidence_pack_v1.md`

Add product code under `starlab/evaluation/`:

* `evidence_pack_models.py`
* `evidence_pack_views.py`
* `emit_baseline_evidence_pack.py`

Emit two artifacts:

* `baseline_evidence_pack.json`
* `baseline_evidence_pack_report.json`

Add fixtures and tests:

* `tests/fixtures/m25/`
* `tests/test_baseline_evidence_pack.py`

Add governance updates:

* `docs/company_secrets/milestones/M25/M25_plan.md` (this file)
* `M25_toolcalls.md`
* closeout files later: `M25_run1.md`, `M25_summary.md`, `M25_audit.md`
* `tests/test_governance.py` update for M25 artifact existence

## Proposed runtime contract

The contract should state that M25 is a **deterministic interpretive packaging layer** over governed Phase IV artifacts, not a new evaluation or ranking milestone.

### Required input posture

Each supplied suite artifact must:

* be a governed M21 or M22 suite artifact
* have `measurement_surface == "fixture_only"` and compatible benchmark identity
* expose subjects used by the supplied M23 tournament entrant set

The supplied tournament must:

* be `starlab.evaluation_tournament.v1`
* be `fixture_only`
* resolve every `entrant_id` back to exactly one provided suite subject

The supplied diagnostics must:

* be `starlab.evaluation_diagnostics.v1`
* be derived from the supplied tournament
* match the tournament identity/hash expected by M24

### Output posture

`baseline_evidence_pack.json` should minimally contain:

* `evidence_pack_version`
* `tournament_sha256`
* `diagnostics_sha256`
* `suite_sha256s`
* `benchmark_contract_sha256`
* `entrants[]`
* sorted `warnings`
* sorted `non_claims`

Each `entrants[]` row should minimally contain:

* `entrant_id`
* `suite_id`
* `subject_id`
* `subject_kind`
* `standing_rank`
* `tournament_points`
* `primary_metric`
* `primary_tiebreak_scalar`
* `wins`
* `losses`
* `draws`
* `failure_views`
* `evidence_refs` back to the upstream suite/tournament/diagnostics rows

`baseline_evidence_pack_report.json` should be a compact summary with:

* `report_version`
* `evidence_pack_sha256`
* `entrant_count`
* `suite_count`
* `subject_kind_counts`
* `failure_view_counts`
* sorted `warnings`
* sorted `non_claims`

### Deterministic rules

* entrant rows follow **M23 standings order**
* suite references are normalized deterministically
* `warnings` and `non_claims` sort lexicographically
* emitted JSON uses the project's canonical JSON conventions
* no timestamps beyond existing canonical project conventions unless absolutely necessary

### Explicit non-claims

* not benchmark integrity
* not leaderboard validity beyond governed upstream artifacts
* not new scoring or re-ranking
* not new diagnostics logic
* not live SC2 or replay execution
* not replay↔execution equivalence
* not raw replay or archive packaging
* not M26 imitation or learning work

## CLI

```text
python -m starlab.evaluation.emit_baseline_evidence_pack \
  --suite PATH \
  --suite PATH \
  --tournament PATH \
  --diagnostics PATH \
  --output-dir OUT
```

Keep CLI inputs simple. Avoid optional modes unless they are required for the contract.

## Implementation sequence

### Slice 1 — contract and fixture design

Author `docs/runtime/baseline_evidence_pack_v1.md` first.

Create a minimal M25 fixture set that reuses the governed M21/M22 → M23 → M24 chain already in repo, then add one negative fixture family for mismatch cases.

### Slice 2 — core models and deterministic views

Implement typed models and builders for:

* source-artifact identity checks
* entrant evidence rows
* failure-view projection
* compact report aggregation

Fail fast on:

* suite/tournament lineage mismatch
* diagnostics/tournament mismatch
* duplicate or unresolved entrant coverage
* inconsistent benchmark contract hashes

### Slice 3 — emitter CLI and goldens

Implement the CLI and emit the two JSON artifacts into an output directory.

Add goldens for:

* happy-path pack
* report counts
* entrant ordering
* failure-view projection stability

### Slice 4 — guards and end-to-end proof

Add:

* chain test from M21/M22 → M23 → M24 → M25
* AST import guard ensuring no `starlab.replays`, `starlab.sc2`, or `s2protocol` in new M25 evaluation modules
* negative tests for hash/identity mismatches
* governance test for required M25 closeout files

## Test plan

1. **Happy path**
   Build an evidence pack from governed fixture-only upstream artifacts and compare against golden outputs.

2. **Lineage mismatch**
   Tournament entrant set cannot be resolved from supplied suites → hard failure.

3. **Diagnostics mismatch**
   Diagnostics derived from a different tournament/hash → hard failure.

4. **Duplicate entrant mapping**
   Same entrant resolved from more than one suite subject → hard failure.

5. **Deterministic ordering**
   Entrants follow M23 standings order; warnings/non-claims sort lexicographically.

6. **Report stability**
   Counts and hashes are stable across repeated runs.

7. **Import guard**
   No forbidden replay/runtime imports in new M25 modules.

8. **End-to-end chain**
   Existing Phase IV chain test expands cleanly through M25 without widening claims.

## Acceptance criteria

* `docs/runtime/baseline_evidence_pack_v1.md` exists and clearly states scope, inputs, outputs, deterministic rules, and non-claims.
* `baseline_evidence_pack.json` and `baseline_evidence_pack_report.json` are emitted deterministically from governed fixture-only upstream artifacts.
* M25 tests are green locally and in CI.
* New M25 modules remain free of `starlab.replays`, `starlab.sc2`, and `s2protocol`.
* No new tournament, diagnostics, or benchmark semantics are introduced.
* `docs/starlab.md` is updated at closeout and continues to present M25 narrowly as packaging, not proof of benchmark integrity.
* M26 remains stub-only after closeout.

## `docs/starlab.md` updates to make during M25 closeout

Add or update:

1. **Phase IV artifact row for M25** — clarify required inputs, primary artifacts, included vs external surface, and explicit non-claims.
2. **Phase IV glossary** — add terms for: evidence pack, evidence row, source artifact identity, pack non-claims.
3. **Current milestone section** — replace stub language with the actual narrow claim and artifact names.
4. **Closeout ledger / changelog** — record authoritative PR-head CI, merge-boundary `main` CI, merge commit SHA, and the exact M25 proof surface.
5. **Governance test note** — extend `tests/test_governance.py` so M25 closeout artifacts are required.

Add a single compact Phase IV "packaging progression" sentence right under the M20–M25 boundary so the chain reads cleanly as **contract/suites → tournament → diagnostics → evidence pack**.

## Paste-ready Cursor implementation prompt

```text
Implement M25 — Baseline Evidence Pack on a fresh milestone branch.

Scope discipline:
- Keep M25 narrow and reversible.
- M25 is a deterministic, offline, fixture-only packaging layer over governed Phase IV artifacts.
- Do not add new tournament semantics, new diagnostics semantics, benchmark-integrity claims, replay↔execution claims, live SC2, or any M26 work.
- Do not import `starlab.replays`, `starlab.sc2`, or `s2protocol` in new M25 evaluation modules.

Authoritative scope:
- Required inputs: one or more governed M21/M22 suite artifacts, one governed M23 `evaluation_tournament.json`, and one governed M24 `evaluation_diagnostics.json` derived from that tournament.
- Outputs:
  - `baseline_evidence_pack.json`
  - `baseline_evidence_pack_report.json`
- Add runtime contract: `docs/runtime/baseline_evidence_pack_v1.md`
- Add product modules under `starlab/evaluation/`:
  - `evidence_pack_models.py`
  - `evidence_pack_views.py`
  - `emit_baseline_evidence_pack.py`
- Add fixtures under `tests/fixtures/m25/`
- Add tests in `tests/test_baseline_evidence_pack.py`

Resolved design decisions:
- JSON artifacts only in v1; no zip/tar/archive packaging.
- Diagnostics are required in v1.
- Pack one governed tournament chain at a time.
- Entrant rows follow M23 standings order.
- `warnings` and `non_claims` sort lexicographically.

Implementation requirements:
1. If `docs/company_secrets/milestones/M25/` does not exist, create it and copy this plan into `M25_plan.md`.
2. Update `M25_toolcalls.md` as you work.
3. Write the runtime contract first.
4. Build deterministic validation for:
   - suite/tournament entrant resolution
   - diagnostics/tournament identity match
   - duplicate entrant coverage
   - benchmark contract hash consistency across supplied artifacts
5. Emit the two M25 artifacts deterministically using canonical JSON conventions already used in the repo.
6. Add goldens and negative tests.
7. Add an AST import guard test for forbidden imports in M25 evaluation modules.
8. Extend the Phase IV chain test through M25.
9. Keep CI green by default. If a CI issue appears, analyze it using `docs/company_secrets/prompts/workflowprompt.md` before choosing the next action.
10. Update `docs/starlab.md` as part of milestone work, not as an afterthought.

Acceptance bar:
- Ruff, MyPy, pytest, and governance tests green.
- Authoritative PR-head CI green before merge.
- Merge-boundary `main` CI green after merge.
- Narrow claim preserved everywhere.
```

## Paste-ready Cursor closeout prompt

```text
M25 implementation is complete. Perform milestone closeout now.

Closeout requirements:
1. Generate the milestone summary using `docs/prompts/summaryprompt.md`.
2. Generate the milestone audit using `docs/prompts/unifiedmilestoneauditpromptV2.md`.
3. Ensure all documentation is updated as necessary.
4. Update `docs/starlab.md` so M25 is fully reflected in:
   - current milestone
   - Phase IV artifact row / glossary
   - closeout ledger
   - changelog
   - any proved/non-proved statements touched by M25
5. Finalize:
   - `docs/company_secrets/milestones/M25/M25_run1.md`
   - `M25_summary.md`
   - `M25_audit.md`
   - `M25_plan.md` (mark complete)
   - `M25_toolcalls.md`
6. Preserve CI truth:
   - record authoritative PR-head CI run ID and final PR head SHA
   - record merge commit SHA
   - record merge-boundary `main` CI run ID
7. Merge the milestone branch only after green CI.
8. Avoid unnecessary post-closeout pushes to `main`. If follow-up work is needed after closeout, create the next milestone branch and carry it there.
9. Create the next milestone folder `docs/company_secrets/milestones/M26/` and seed:
   - `M26_plan.md` stub
   - `M26_toolcalls.md` stub
10. In the closeout note, state clearly what M25 proved and what it still did not prove.
```
