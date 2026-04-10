# Deferred issues registry

**Purpose:** Machine-readable, diligence-friendly list of known gaps and exit criteria.  
**Authority:** Subordinate to `docs/starlab.md`. Resolved items remain listed with resolution evidence.

| ID | Issue | Discovered | Deferred to | Reason | Blocker? | Exit criteria |
| -- | ----- | ---------- | ----------- | ------ | -------- | ------------- |
| DIR-003 | Shared `starlab._io` JSON load helper | M32 audit | M34 | DRY refactor deferred to structural milestone | No | Single helper; one error contract; tests green |
| DIR-004 | `test_governance.py` file split | M32 audit | M34 | Large file; non-blocking | No | Multiple modules; same assertions |
| DIR-005 | Narrow non-adapter `except Exception` | M32 audit | M34 | Boundary exceptions preserved | No | Adapters keep BLE001; internal paths narrowed |
| DIR-006 | Dev dependency upper caps + automation | M32 audit | M34 | pip/Dependabot policy | No | Upper bounds in `pyproject.toml` and/or Dependabot config |

## M32 resolutions (populate on closeout)

| ID | Resolution | Evidence |
| -- | ----------- | -------- |
| DIR-008 | Coverage measurement + `coverage.xml` in CI | `.github/workflows/ci.yml`, `[tool.coverage.*]` in `pyproject.toml` |
| DIR-009 | JUnit `pytest-junit.xml` in CI | `.github/workflows/ci.yml` |
| DIR-010 | GitHub Actions pinned to immutable SHAs | `.github/workflows/ci.yml` |
| DIR-011 | `Makefile` developer surface | `Makefile` |

## M33 resolutions

| ID | Resolution | Evidence |
| -- | ----------- | -------- |
| DIR-001 | Parallel CI tiering (`quality`, `smoke`, `tests`, `security`, `fieldtest`) + final `governance` job; workflow name **`CI`** unchanged | `.github/workflows/ci.yml`, `docs/runtime/ci_tiering_field_test_readiness_v1.md` |
| DIR-002 | Smoke vs full-suite posture documented; smoke lane emits JUnit in CI | `ci.yml` `smoke` job, `pytest-smoke-junit.xml` artifact, operating manual + runtime contract |
| DIR-007 | Coverage gate **stable** at **`fail_under = 75.4`** — no CI variance observed; **no** silent threshold change | `pyproject.toml`, M33 scope (ledger + this registry) |
