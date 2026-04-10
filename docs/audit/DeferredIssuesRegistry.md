# Deferred issues registry

**Purpose:** Machine-readable, diligence-friendly list of known gaps and exit criteria.  
**Authority:** Subordinate to `docs/starlab.md`. Resolved items remain listed with resolution evidence.

| ID | Issue | Discovered | Deferred to | Reason | Blocker? | Exit criteria |
| -- | ----- | ---------- | ----------- | ------ | -------- | ------------- |
| DIR-001 | CI job splitting / parallel tiering | M32 full audit | M33 | Scope: M32 keeps single job + artifacts | No | Required checks unchanged; wall-clock reduced; documented tier layout |
| DIR-002 | Broader smoke vs quality marker posture | M32 | M33 | M32 seeds smoke lane only | No | Markers documented; optional nightly in M33 |
| DIR-003 | Shared `starlab._io` JSON load helper | M32 audit | M34 | DRY refactor deferred to structural milestone | No | Single helper; one error contract; tests green |
| DIR-004 | `test_governance.py` file split | M32 audit | M34 | Large file; non-blocking | No | Multiple modules; same assertions |
| DIR-005 | Narrow non-adapter `except Exception` | M32 audit | M34 | Boundary exceptions preserved | No | Adapters keep BLE001; internal paths narrowed |
| DIR-006 | Dev dependency upper caps + automation | M32 audit | M34 | pip/Dependabot policy | No | Upper bounds in `pyproject.toml` and/or Dependabot config |
| DIR-007 | Coverage gate re-baseline if noisy | M32 | M33 | Only if CI shows variance — else closed in M32 | No | Stable gate or documented waiver in ledger |

## M32 resolutions (populate on closeout)

| ID | Resolution | Evidence |
| -- | ----------- | -------- |
| DIR-008 | Coverage measurement + `coverage.xml` in CI | `.github/workflows/ci.yml`, `[tool.coverage.*]` in `pyproject.toml` |
| DIR-009 | JUnit `pytest-junit.xml` in CI | `.github/workflows/ci.yml` |
| DIR-010 | GitHub Actions pinned to immutable SHAs | `.github/workflows/ci.yml` |
| DIR-011 | `Makefile` developer surface | `Makefile` |
