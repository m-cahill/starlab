# Deferred issues registry

**Purpose:** Machine-readable, diligence-friendly list of known gaps and exit criteria.  
**Authority:** Subordinate to `docs/starlab.md`. Resolved items remain listed with resolution evidence.

| ID | Issue | Discovered | Deferred to | Reason | Blocker? | Exit criteria |
| -- | ----- | ---------- | ----------- | ------ | -------- | ------------- |
| DIR-003 | Shared `starlab._io` JSON load helper | M32 audit | **Resolved (M34)** | DRY refactor deferred to structural milestone | No | `starlab/_io.py`; migrated callers; tests green |
| DIR-004 | `test_governance.py` file split | M32 audit | **Resolved (M34)** | Large file; non-blocking | No | `tests/test_governance_*.py`; `tests/test_governance.py` removed |
| DIR-005 | Narrow non-adapter `except Exception` | M32 audit | **Resolved (M34)** | Boundary exceptions preserved | No | Validation + `docs/audit/broad_exception_boundaries.md` — only approved adapter boundaries remain |
| DIR-006 | Dev dependency upper caps + automation | M32 audit | **Resolved (M34)** | pip/Dependabot policy | No | `pyproject.toml` dev upper bounds; `.github/dependabot.yml` |

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

## M34 resolutions

| ID | Resolution | Evidence |
| -- | ----------- | -------- |
| DIR-003 | Shared internal JSON object loading: `parse_json_object_text`, `load_json_object` | `starlab/_io.py`; migrated `starlab/state`, `starlab/observation`, `starlab/replays`, `starlab/imitation`, `starlab/evaluation`, `starlab/explorer`, `starlab/sc2/evaluate_environment_drift.py` |
| DIR-004 | Governance tests split into `test_governance_docs.py`, `test_governance_ci.py`, `test_governance_milestones.py`, `test_governance_runtime.py` | `tests/test_governance_*.py`; `tests/test_m34_audit_closure.py` |
| DIR-005 | **Documentation/validation closure** — no unjustified non-adapter broad catches; adapter boundaries documented | `docs/audit/broad_exception_boundaries.md`; `starlab/replays/s2protocol_adapter.py`, `starlab/replays/metadata_io.py`, `starlab/sc2/harness.py` |
| DIR-006 | Dev dependency upper bounds + Dependabot (weekly `pip` + `github-actions` on `main`) | `[project.optional-dependencies]` in `pyproject.toml`, `.github/dependabot.yml` |
