# M35 Plan — Audit Closure IV: Structural Decoupling and Module Decomposition

## Milestone identity

- **Milestone:** M35
- **New name:** **Audit Closure IV — Structural Decoupling and Module Decomposition**
- **Phase:** V — Learning Paths, Evidence Surfaces, and Flagship Proof
- **Recommended branch:** `m35-audit-closure-iv-structural-decoupling-module-decomposition`

## Why this milestone exists

Post-M34 audit posture is stronger, but the biggest remaining audit drag items are still structural rather than product-facing:

- persistent **evaluation → state** cross-layer coupling
- several oversized source modules
- one small remaining strict-wrapper inconsistency
- audit-pressure to reduce architectural/code-health debt before public flagship proof work

This milestone is intentionally the **first of two pre-flagship corrective milestones**.

It is **not** Public Flagship Proof Pack work.

## Governance decision to record first

Before product/code changes, update the project arc so the ledger reflects the actual program decision:

### New future arc

- **M35** → **Audit Closure IV — Structural Decoupling and Module Decomposition**
- **M36** → **Audit Closure V — Governance Surface Rationalization and Documentation Density Control**
- **M37** → **Public Flagship Proof Pack**
- **M38** → **SC2 Substrate Review & Expansion Decision**
- **M39** → **Platform Boundary Review & Multi-Environment Charter**

This expands the planned program arc from:

- **38 milestones (M00–M37)**

to:

- **40 milestones (M00–M39)**

## Mandatory `docs/starlab.md` updates at milestone start

Update `docs/starlab.md` immediately, before implementation, so the ledger remains the source of truth.

### Required sections to update

1. **Top status line**
   - Replace the current “M35 — Public Flagship Proof Pack” current-stub language.
   - Make **M35** the current corrective milestone.
   - State that **Public Flagship Proof Pack** has moved to **M37**.

2. **§6 Phase map**
   - Keep **M35**, **M36**, and **M37** inside **Phase V**.
   - Move Phase VI to:
     - **M38** — SC2 Substrate Review & Expansion Decision
     - **M39** — Platform Boundary Review & Multi-Environment Charter

3. **§7 milestone table**
   - Expand planned program arc from **M00–M37** to **M00–M39**
   - Update milestone names and statuses accordingly

4. **§8 milestone intent map**
   - Add/update intent rows for:
     - M35 structural decoupling / module decomposition
     - M36 governance rationalization / ledger density control
     - M37 flagship proof pack
     - M38 substrate review
     - M39 platform boundary review

5. **§11 current milestone**
   - Make **M35** the current corrective milestone
   - Make it explicit that this is a governance decision taken **after** the M35 full audit, even though that audit said the repo could proceed directly to flagship product work
   - Do **not** rewrite history or alter the existing M35 audit files to pretend they recommended this stricter sequence

6. **§12 open decisions**
   - Move **OD-007** target milestone from **M37** to **M39**

7. **§20 score trend placeholder**
   - Extend placeholder rows through **M39**

8. **§23 changelog**
   - Add a governance entry that the program intentionally inserted **two corrective milestones before flagship proof pack** to push audit posture higher
   - Be explicit that this is a deliberate governance choice, not evidence that M35 product work had started

## Required milestone stub/file alignment

Because the planned arc changes, align milestone folders and stub files so governance tests remain truthful.

### Update or create the following

- `docs/company_secrets/milestones/M35/M35_plan.md`
- `docs/company_secrets/milestones/M35/M35_toolcalls.md`

- `docs/company_secrets/milestones/M36/M36_plan.md`
- `docs/company_secrets/milestones/M36/M36_toolcalls.md`

- `docs/company_secrets/milestones/M37/M37_plan.md`
- `docs/company_secrets/milestones/M37/M37_toolcalls.md`

- `docs/company_secrets/milestones/M38/M38_plan.md`
- `docs/company_secrets/milestones/M38/M38_toolcalls.md`

- `docs/company_secrets/milestones/M39/M39_plan.md`
- `docs/company_secrets/milestones/M39/M39_toolcalls.md`

If M36/M37 stubs already exist under the prior naming, update them in place to the new identities.
Create new M38/M39 stubs as needed.

Also update governance tests to match the revised planned arc.

## M35 charter

This milestone should materially improve audit posture by removing the largest remaining **structural** and **code-health** weaknesses that are still worth fixing before flagship proof-pack work.

## In scope

### 1. Remove evaluation → state direct coupling

Target the long-standing coupling:

- `starlab/evaluation/learned_agent_evaluation.py`
- direct import from:
  - `starlab.state.canonical_state_inputs`

Expected outcome:
- no direct evaluation import from `starlab.state.canonical_state_inputs`
- replace with one of:
  - a typed `BundleLoader` protocol
  - callable injection
  - a thinner, more stable internal boundary module

Rules:
- preserve existing behavior
- preserve artifact outputs
- preserve current tests
- keep the replacement enterprise-legible, not clever

### 2. Reduce the largest source-module hotspots

Prioritize decomposition of the biggest modules called out in the audit:

- `starlab/replays/parser_io.py`
- `starlab/replays/replay_slice_generation.py`
- `starlab/observation/observation_reconciliation_pipeline.py`

Preferred target:
- each below **500 lines**

If one cannot reasonably get below 500 without harmful churn:
- still extract the highest-value cohesive helpers
- document the rationale in milestone summary/audit

Guidance:
- extract private helper modules/submodules
- avoid changing public artifact semantics
- avoid sweeping package rearchitecture

### 3. Clean up strict JSON wrapper inconsistency

Current small inconsistency:
- `dataset_views.py` and `evidence_pack_views.py` wrap shared JSON parsing but raise different exception types for the same root-not-object condition

Expected outcome:
- either:
  - align both to one exception type
  - or introduce a shared strict helper in `_io.py` with a single contract

Rules:
- preserve intended caller ergonomics
- keep error messages stable or clearly improved
- add tests if behavior changes at all

### 4. Keep corrective work honest and bounded

This milestone should improve:
- modularity
- code health
- maintainability

without:
- inventing a service layer
- changing benchmark claims
- broadening runtime scope
- touching live SC2 posture

## Explicit non-goals

Do **not** do any of the following in M35:

- no **Public Flagship Proof Pack** artifacts
- no benchmark-integrity upgrade claims
- no live SC2 in CI
- no operating manual v1 promotion
- no license-standardization work
- no replay-fixture provenance documentation unless needed to keep tests/governance consistent
- no placeholder-directory diligence cleanup unless needed to keep governance tests truthful
- no broad `starlab.services` or `starlab.adapters.registry` architecture work
- no sweeping package moves just to improve aesthetics

## Deliverables

Expected outputs for M35:

### Code
- decoupled evaluation loading boundary
- extracted helpers/private submodules for the targeted large files
- aligned strict JSON wrapper behavior
- any needed new/updated tests

### Docs / governance
- updated `docs/starlab.md`
- updated `docs/company_secrets/milestones/M35/M35_plan.md`
- updated `docs/company_secrets/milestones/M35/M35_toolcalls.md`
- revised future stubs for M36–M39
- updated governance tests reflecting the revised milestone arc

### Closeout artifacts
- `docs/company_secrets/milestones/M35/M35_run1.md`
- `docs/company_secrets/milestones/M35/M35_summary.md`
- `docs/company_secrets/milestones/M35/M35_audit.md`

## Acceptance criteria

M35 is complete only when all of the following are true:

1. `learned_agent_evaluation.py` no longer imports directly from `starlab.state.canonical_state_inputs`
2. the new boundary is typed, tested, and behaviorally equivalent
3. the three priority large modules are materially decomposed; target is `<500` lines each, or documented rationale is provided where that is not achieved safely
4. strict JSON raise-on-error behavior is aligned or centralized with one clear contract
5. governance tests pass under the revised milestone arc (M00–M39)
6. `docs/starlab.md` truthfully reflects:
   - two corrective milestones before flagship proof pack
   - M35 as current milestone
   - M37 as flagship proof pack
   - M38/M39 as shifted Phase VI milestones
7. coverage floor **75.4** is preserved or improved
8. required CI topology remains unchanged and truthful:
   - `quality`
   - `smoke`
   - `tests`
   - `security`
   - `fieldtest`
   - aggregate `governance`
9. `make fieldtest` still passes
10. this milestone remains clearly corrective and does not drift into flagship proof-pack product work

## Recommended implementation order

1. **Ledger first**
   - Update `docs/starlab.md`
   - Update/create M35–M39 milestone stubs
   - Update governance tests for the revised arc

2. **Boundary decoupling**
   - Remove evaluation → state direct import
   - Introduce the typed replacement boundary
   - Add/adjust regression tests

3. **Module decomposition**
   - `parser_io.py`
   - `replay_slice_generation.py`
   - `observation_reconciliation_pipeline.py`

4. **Strict wrapper cleanup**
   - Align or centralize strict JSON error contract

5. **Polish + verification**
   - Ruff / Mypy / pytest / coverage / fieldtest
   - ensure no accidental CI/governance drift

## Validation required

At minimum run:

- `ruff check starlab tests`
- `ruff format --check starlab tests`
- `mypy starlab tests`
- `pytest -q -m smoke`
- `pytest -q`
- `pytest -q --cov=starlab`
- `make fieldtest`

If any artifact shape, error type, or structured output changes:
- add focused regression tests
- document the change in the milestone summary/audit

## Closeout instructions for Cursor

When implementation is complete and CI is green:

1. Generate:
   - `M35_run1.md`
   - `M35_summary.md`
   - `M35_audit.md`

2. Mark `M35_plan.md` complete with:
   - branch
   - PR
   - final PR head SHA
   - authoritative PR-head CI
   - merge-boundary `main` CI
   - tag

3. Update `docs/starlab.md` closeout sections:
   - top status line
   - §7 milestone table
   - §8 intent map
   - §11 current milestone
   - §12 OD-007 target
   - §18 closeout ledger
   - §20 score trend
   - §23 changelog

4. Seed/refresh the next milestone stub only after closeout:
   - M36 should remain the next current stub milestone
   - M37/M38/M39 stubs should already exist and stay aligned

5. Ensure all documentation is updated as necessary.

## Notes on proceeding

This milestone is intentionally **larger than the recent audit-closure milestones**, because it is meant to remove a real chunk of remaining audit drag before public flagship proof work.

The expected sequence after this milestone is:

- **M35** — Audit Closure IV — Structural Decoupling and Module Decomposition
- **M36** — Audit Closure V — Governance Surface Rationalization and Documentation Density Control
- **M37** — Public Flagship Proof Pack
- **M38** — SC2 Substrate Review & Expansion Decision
- **M39** — Platform Boundary Review & Multi-Environment Charter

Do not skip the `docs/starlab.md` update at the start. The ledger must lead the implementation, not lag it.
