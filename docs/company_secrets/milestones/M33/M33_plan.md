# M33 Plan — Audit Closure II: CI Tiering, Architecture Surface, and Field-Test Readiness

## Milestone identity

| Field | Value |
| ----- | ----- |
| **Milestone** | M33 |
| **Name** | Audit Closure II — CI Tiering, Architecture Surface, and Field-Test Readiness |
| **Phase** | V — Learning Paths, Evidence Surfaces, and Flagship Proof |
| **Recommended branch** | `m33-audit-closure-ii-ci-tiering-field-test-readiness` |

## Goal

Prove that STARLAB can run its required checks through an **explicit, truthful, parallel CI topology** while also exercising a **fixture-only field-test path in CI** and tightening the architecture / operator documentation surface for diligence and handoff.

This is a corrective hardening milestone, not a flagship proof-pack milestone.

## Why M33 exists

M32 established the operational floor: measured coverage + gate, `coverage.xml` / `pytest-junit.xml`, SHA-pinned actions, smoke lane, `Makefile`, clone-to-run / field-test docs, architecture overview, draft operating manual scaffold, public deferred issues registry.

M33 closes the next corrective layer without widening into structural refactors or flagship proof work. It consumes M32 deferred items:

- **DIR-001** — CI job splitting / parallel tiering  
- **DIR-002** — broader smoke vs quality marker posture  
- **DIR-007** — coverage gate re-baseline **only if noisy** (default: no change)

## What M33 should prove

1. Required CI checks are exposed as **separate, parallel, truthful jobs** without weakening branch protection.  
2. STARLAB has distinct **smoke**, **full test**, **security**, and **fixture-only field-test** lanes.  
3. The **field-test path** runs in CI on checked-in fixtures; outputs are uploaded as artifacts (`out/fieldtest/` including required JSON).  
4. Architecture and operating-manual surfaces let an engineer or reviewer quickly understand package boundaries, CI tiers, fixture-only field-test procedure, and common failure modes.  
5. The coverage gate is either confirmed stable or explicitly re-baselined with rationale (default: **stable at 75.4**).

## What M33 must not claim

- M34 structural hygiene closure  
- M35 flagship proof pack completion  
- Benchmark integrity  
- Live SC2 execution in CI  
- Operating manual promotion to canonical / v1  
- Deployment or service-layer productization  
- Replay↔execution equivalence  

## Primary deliverables

### Workflow / CI surface

- `.github/workflows/ci.yml` — explicit parallel jobs + final `governance` aggregator  
- Artifacts: `coverage.xml`, `pytest-junit.xml`, smoke JUnit, SBOM, **`fieldtest-output`** (`out/fieldtest/`)

### Contract / documentation

- **Create:** `docs/runtime/ci_tiering_field_test_readiness_v1.md`  
- **Create:** `docs/diligence/field_test_session_template.md`  
- **Update:** `docs/architecture.md`, `docs/starlab_operating_manual_v0.md`, `docs/getting_started_clone_to_run.md`, `docs/runtime/clone_to_run_smoke_v1.md`, `docs/diligence/field_test_checklist.md`, `docs/starlab.md`

### Governance / tests

- CI topology tests; field-test artifact tests; smoke posture; coverage policy; doc existence; M33 charter / no M34–M35 creep  

## Recommended CI topology

- Workflow name **`CI`**; final job **`governance`** (`needs` all upstream jobs).  
- Jobs: **`quality`** (Ruff, format, Mypy), **`smoke`** (`pytest -m smoke` + JUnit artifact), **`tests`** (full pytest + coverage + JUnit), **`security`** (pip-audit, CycloneDX, Gitleaks), **`fieldtest`** (`make fieldtest`, verify JSON, upload `out/fieldtest/`), **`governance`** (aggregate).

**Rules:** SHA-pinned actions; no `continue-on-error` on required jobs; `if-no-files-found: error` on uploads; do not mute failures for speed.

## Field-test scope

- Fixture-only, offline, no raw `.SC2Replay` in CI path, no live SC2, no benchmark claim.  
- CI asserts `replay_explorer_surface.json` and `replay_explorer_surface_report.json` under `out/fieldtest/`.

## Coverage policy

- Default: **keep `fail_under = 75.4`** unless CI proves noise; document any re-baseline in ledger + `DeferredIssuesRegistry.md`.

## Explicit deferrals to M34

Shared `starlab._io`, `test_governance.py` split, narrowing non-adapter `except Exception`, dependency automation, operating-manual promotion prep — unless a tiny unavoidable fix.

## Acceptance criteria

- CI runs as explicit parallel tiers; `governance` remains merge-safe.  
- Smoke, tests, security, fieldtest visible and green on authoritative PR-head.  
- Field-test directory uploaded as CI artifact.  
- Architecture + operating manual v0 materially expanded; session template exists.  
- `docs/starlab.md` updated honestly for M33 scope.  
- **No** M34 structural-hygiene product work; **no** M35 flagship proof-pack work.

## Closeout (after merge + green CI)

Generate `M33_run1.md`, `M33_summary.md`, `M33_audit.md`; update `M33_plan.md`, `M33_toolcalls.md`, `docs/starlab.md`; tag `v0.0.33-m33`; seed **M34** stubs only.

## Expected proof sentence

M33 proves STARLAB’s required checks can run in explicit, truthful CI tiers with a fixture-only field-test artifact path and expanded architecture / operator guidance — not M34 structural hygiene, not M35 flagship proof-pack work, not live SC2 in CI, and not benchmark-integrity proof.

---

**Status:** Implementation per this charter (replace prior stub).
