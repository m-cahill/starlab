# M32 Plan — Audit Closure I: Coverage, Clone-to-Run Baseline, and Operating Manual Scaffold

## Milestone identity

- **Milestone:** M32
- **Name:** Audit Closure I — Coverage, Clone-to-Run Baseline, and Operating Manual Scaffold
- **Phase:** V
- **Branch (merged):** `m32-audit-closure-coverage-clone-run-manual-scaffold` → [PR #38](https://github.com/m-cahill/starlab/pull/38), merge commit `cf7219911a208da584537b4c08ab5811fa3f67de`
- **Status:** **Complete on `main`** — see `M32_run1.md`, `M32_summary.md`, `M32_audit.md`; tag `v0.0.32-m32` on merge commit

## Mandatory governance change at milestone start

Before product work, update the future program arc in `docs/starlab.md` so the ledger reflects the corrective program honestly.

### Recharter the future milestones

Revise the planned arc from **35 milestones (M00–M34)** to **38 milestones (M00–M37)**.

Use this exact remap:

- **M32** → **Audit Closure I — Coverage, Clone-to-Run Baseline, and Operating Manual Scaffold**
- **M33** → **Audit Closure II — CI Tiering, Architecture Surface, and Field-Test Readiness**
- **M34** → **Audit Closure III — Structural Hygiene, Deferred-Issue Closure, and Operating Manual Promotion Prep**
- **M35** → **Public Flagship Proof Pack** *(renamed from old M32)*
- **M36** → **SC2 Substrate Review & Expansion Decision** *(renamed from old M33)*
- **M37** → **Platform Boundary Review & Multi-Environment Charter** *(renamed from old M34)*

### Required ledger updates for the recharter

Update at the start of M32:

- overall status / milestone arc language
- milestone table
- milestone intent map
- Phase V progression compact table
- Phase VI progression compact table
- current milestone section
- any references to "35 milestones (M00–M34)" → "38 milestones (M00–M37)"
- **OD-007** target milestone from **M34** → **M37**
- add a changelog entry for the governance recharter

### Important historical rule

Do **not** rewrite or blur any closed-milestone facts for **M00–M31**.
Only update future-planned milestone numbering / naming and the current milestone charter.

---

## Goal

Raise STARLAB's audit floor immediately by proving that:

1. test behavior is **measured and surfaced** in CI,
2. a new engineer can **clone the repo, install it, and run a truthful fixture-based smoke path**,
3. STARLAB has the first usable **architecture / quickstart / field-test / operating-manual scaffold** suitable for diligence and field testing.

This milestone is a corrective hardening milestone, not a flagship proof-pack milestone.

---

## Why M32 exists

M32 exists because the repo is governance-strong but still missing key enterprise-grade operational surfaces:

- coverage measurement / visibility
- machine-readable test-result artifacts
- clone-to-run / field-test onboarding
- public architecture overview
- an operating-manual scaffold
- a deferred-issues register tied to the audit program

M32 should fix the highest-leverage gaps without widening into large structural refactors or proof-pack work.

---

## What M32 should prove

M32 proves a **truthful clone-to-run baseline** and **quality visibility baseline** for STARLAB:

- CI emits measurable **coverage** and **JUnit** test artifacts
- repo documentation tells an engineer exactly how to install and run the system on fixture data
- a small, repeatable **smoke path** exists for clone validation
- STARLAB has a draft operating manual structure aligned to project authority rules
- the corrective milestone program is recorded honestly in the ledger

---

## What M32 must not claim

M32 must explicitly **not** claim:

- benchmark integrity
- live SC2 execution in CI
- flagship proof-pack completion
- M33 / M34 structural closure
- web deployment readiness
- buyer-ready production operations beyond the documented clone-to-run and fixture smoke posture
- comprehensive operating manual completion (this is a scaffold / v0 draft only)

---

## Primary deliverables

### Documentation

Create or update:

- `docs/architecture.md`
- `docs/getting_started_clone_to_run.md`
- `docs/runtime/clone_to_run_smoke_v1.md`
- `docs/diligence/field_test_checklist.md`
- `docs/starlab_operating_manual_v0.md`
- `docs/audit/DeferredIssuesRegistry.md`

### Developer / operator surface

Create or update:

- `Makefile`

Recommended targets:

- `make install-dev`
- `make smoke`
- `make test`
- `make coverage`
- `make lint`
- `make typecheck`
- `make audit`
- `make fieldtest`

### CI outputs

Add truthful CI artifact publication for:

- `coverage.xml`
- `pytest-junit.xml`

If practical and green on the authoritative PR head, also add a truthful low-water coverage gate derived from the measured baseline.
If not practical without destabilizing CI, record the measured baseline and defer the blocking threshold to **M33** with explicit rationale.

---

## Operating manual scaffold shape (required in M32)

`docs/starlab_operating_manual_v0.md` should be a **draft**, not yet the top authority.

It should explicitly say:

- **Status:** Draft / non-canonical operating manual scaffold
- **Authority:** subordinate to `docs/starlab.md` and runtime contracts until later promotion

Use a concise operating-manual structure with sections like:

1. Executive identity
2. What STARLAB is / is not
3. Core mental model / system flow
4. Architecture overview
5. Installation and quick reference
6. Clone-to-run smoke procedure
7. Common failure modes / debugging
8. Governance and authority hierarchy
9. Frozen vs changing surfaces
10. Field-test checklist
11. Extension guidance
12. Source-of-truth references

M32 should **seed** this manual, not fully finish it.

### Promotion path (plan now, do not fully execute now)

- **M32:** create `docs/starlab_operating_manual_v0.md` scaffold
- **M33:** expand operator workflows / troubleshooting / field-test learnings
- **M34:** evaluate promotion to `v1` if the corrective program has stabilized

---

## Deferred issues registry (required in M32)

Create `docs/audit/DeferredIssuesRegistry.md`.

Seed it from the current codebase audit with a small, testable registry for unresolved items.
At minimum, include:

- coverage gate finalization
- CI tiering / job split
- shared `_io` extraction
- governance test splitting
- broad internal exception narrowing
- dev dependency upper bounds / dependency automation

For each issue include:

- ID
- Issue
- Discovered
- Deferred To
- Reason
- Blocker?
- Exit Criteria

Resolved issues should remain visible with resolution evidence once closed.

---

## Narrow implementation sequence

### Step 0 — Replace the M32 stub and recharter the future arc

- replace `docs/company_secrets/milestones/M32/M32_plan.md` stub with this adapted plan
- update `docs/starlab.md` future milestone arc from M32–M34 to M32–M37
- keep historical facts for M00–M31 unchanged

### Step 1 — Coverage measurement and CI artifacts

Add:

- `pytest-cov` to dev dependencies
- coverage configuration in `pyproject.toml`
- JUnit XML emission
- CI upload for `coverage.xml`
- CI upload for `pytest-junit.xml`

Also:

- pin GitHub Actions in CI to immutable SHAs where practical
- keep CI truthful and green

### Step 2 — Smoke / field-test developer surface

Add:

- pytest smoke marker registration
- a small smoke subset over fixture-backed tests
- `Makefile` commands that map to real repo workflows
- `make fieldtest` that exercises a representative fixture-based product path

`make fieldtest` should use existing checked-in fixtures and existing product CLIs, not live SC2.

Recommended representative path:
- install dev deps
- run smoke tests
- run one representative fixture-based CLI path over a current proved surface (for example the M31 explorer path)

### Step 3 — Clone-to-run quickstart docs

Create:

- `docs/getting_started_clone_to_run.md`
- `docs/runtime/clone_to_run_smoke_v1.md`
- `docs/diligence/field_test_checklist.md`

These docs must be concrete and command-driven.
They should tell an engineer how to:

- clone the repo
- install dependencies
- run lint / typecheck / tests
- run the smoke path
- run one representative product CLI against fixtures
- find the outputs
- know what is and is not proved

### Step 4 — Architecture overview doc

Create `docs/architecture.md`.

Keep it compact and useful:

- one diagram of major packages and dependencies
- one table describing each package
- one short section on untrusted boundaries
- one short section on source-of-truth docs
- one short section on how milestones map to the codebase

### Step 5 — Operating manual v0 scaffold

Create `docs/starlab_operating_manual_v0.md`.

This should be practical enough that a field tester or engineer can orient themselves quickly, but still clearly marked as a draft operating surface.

### Step 6 — Deferred issues registry

Create `docs/audit/DeferredIssuesRegistry.md`.

Record what M32 fixes now and what is intentionally deferred to M33 / M34.

### Step 7 — Tests and governance alignment

Add or update tests for:

- smoke marker configuration
- `Makefile` targets or equivalent command surface presence
- clone-to-run docs referenced files / commands exist
- new docs are included in governance doc lists where appropriate
- future milestone renumbering is reflected honestly in governance expectations

---

## Required tests

At minimum, add:

1. **coverage config test / CI wiring validation**
   Ensure coverage and JUnit outputs are configured and artifact-uploaded.

2. **smoke marker test**
   Ensure smoke markers are registered and a bounded smoke subset exists.

3. **fieldtest command test**
   Ensure the documented field-test command path runs on fixture data.

4. **quickstart / docs existence test**
   Verify `docs/architecture.md`, `docs/getting_started_clone_to_run.md`, `docs/runtime/clone_to_run_smoke_v1.md`, `docs/diligence/field_test_checklist.md`, and `docs/starlab_operating_manual_v0.md` exist.

5. **governance renumbering test**
   Verify the program arc now reflects:
   - M32 corrective milestone
   - M33 corrective milestone
   - M34 corrective milestone
   - M35 flagship proof pack
   - M36 substrate review
   - M37 platform boundary review

6. **current milestone test**
   Ensure `docs/starlab.md` marks M32 as current and chartered accordingly.

7. **no M35 product creep test (governance expectation)**
   Ensure M32 stays corrective and does not land flagship proof-pack product work.

---

## Acceptance criteria

M32 is complete only when all of the following are true:

- the future program arc is rechartered honestly from **35 milestones (M00–M34)** to **38 milestones (M00–M37)**
- M32 is renamed to the corrective milestone above
- old future milestones are shifted to:
  - M35 flagship proof pack
  - M36 substrate review
  - M37 platform boundary review
- CI emits **coverage.xml** and **pytest-junit.xml** artifacts
- GitHub Actions references are pinned more defensively
- `make smoke` and `make fieldtest` exist and are truthful
- an engineer can follow `docs/getting_started_clone_to_run.md` and run the repo on fixture data
- `docs/architecture.md` exists and is accurate
- `docs/starlab_operating_manual_v0.md` exists with draft-authority language
- `docs/diligence/field_test_checklist.md` exists
- `docs/audit/DeferredIssuesRegistry.md` exists with testable exit criteria
- CI is green on authoritative PR-head and merge-boundary `main`
- **no** M35 flagship proof-pack product code lands in M32

---

## Explicit deferrals to later corrective milestones

### M33 should take

- CI job splitting / parallel tiering
- broader smoke vs quality posture
- deeper field-test hardening
- architecture surface expansion if needed
- stronger coverage enforcement if M32 only measures

### M34 should take

- shared `_io` extraction
- governance test file split
- exception narrowing outside adapter boundaries
- dependency automation / remaining audit cleanup
- operating manual promotion-prep

### M35 should remain

- the renamed flagship proof pack milestone
- separate from corrective hardening work

---

## CI / guardrail notes

- Preserve CI truthfulness.
- Do not soften enforcement with `continue-on-error`.
- Prefer minimal required CI churn in M32.
- Keep the milestone narrow and corrective.
- Do not turn M32 into the flagship proof pack.
- Ensure all documentation is updated as necessary.

---

## Ledger sections that must be touched in M32

Update `docs/starlab.md` at least in:

- overall status
- Phase V compact progression
- Phase VI compact progression
- milestone table
- intent map
- current milestone section
- open decisions (OD-007 target shift)
- closeout requirements if any new operating-manual / field-test rule is added
- changelog

Do the future-arc truth alignment **early** in M32, not only at closeout.

---

## Closeout instructions for Cursor

After M32 is merged with authoritative green CI:

1. Generate:
   - `docs/company_secrets/milestones/M32/M32_run1.md`
   - `docs/company_secrets/milestones/M32/M32_summary.md`
   - `docs/company_secrets/milestones/M32/M32_audit.md`

2. Update:
   - `docs/company_secrets/milestones/M32/M32_plan.md`
   - `docs/company_secrets/milestones/M32/M32_toolcalls.md`
   - `docs/starlab.md`

3. Tag:
   - `v0.0.32-m32`

4. Create next stub only:
   - `docs/company_secrets/milestones/M33/M33_plan.md`
   - `docs/company_secrets/milestones/M33/M33_toolcalls.md`

5. Do **not** land M33 product code in the M32 closeout branch.

---

## Suggested PR title

`M32: audit closure I coverage clone-to-run manual scaffold`

## Expected narrow proof sentence for eventual summary

"M32 proves STARLAB's first truthful clone-to-run and quality-visibility baseline: coverage and JUnit artifacts in CI, a fixture-backed smoke / field-test path for a fresh engineer checkout, an architecture overview, a draft operating manual scaffold, and a machine-readable deferred-issues register — not the flagship proof pack, not benchmark integrity, and not live SC2."
