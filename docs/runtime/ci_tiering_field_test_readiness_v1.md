# CI tiering and field-test readiness (v1)

**Status:** Operational contract for **M33+**.  
**Authority:** Subordinate to `docs/starlab.md`. Runtime field-test semantics remain aligned with `docs/runtime/replay_explorer_surface_v1.md` and `docs/runtime/clone_to_run_smoke_v1.md`.

## Purpose

Document the **parallel CI topology** for STARLAB, what each tier means, which **artifacts** are produced, and how the **fixture-only field-test** lane relates to merge safety — without claiming live SC2, benchmark integrity, or flagship proof-pack completion.

## Workflow

- **Name:** `CI` (unchanged).  
- **Final required aggregate job:** `governance` — succeeds only if all listed upstream jobs succeed (no `continue-on-error` on required tiers).

## Job tiers

| Job | Role |
| --- | ---- |
| `quality` | Ruff check, Ruff format check, Mypy — fast static signal. |
| `smoke` | `pytest -q -m smoke` — bounded fast subset; JUnit uploaded as `pytest-smoke-junit.xml`. |
| `tests` | Full `pytest` with line coverage gate (`fail_under` in `pyproject.toml`); emits `coverage.xml` and `pytest-junit.xml`. |
| `security` | `pip-audit`, CycloneDX SBOM (`sbom.json`), Gitleaks. |
| `fieldtest` | `make fieldtest` — M31 explorer CLI on **checked-in** fixtures only; uploads **`out/fieldtest/`** as artifact `fieldtest-output`. |
| `governance` | Depends on all of the above; **merge-safe aggregate** (no tests duplicated here). |

## Artifact expectations

| Artifact name | Produced by | Required files |
| ------------- | ----------- | ---------------- |
| `coverage-xml` | `tests` | `coverage.xml` |
| `pytest-junit-xml` | `tests` | `pytest-junit.xml` |
| `pytest-smoke-junit-xml` | `smoke` | `pytest-smoke-junit.xml` |
| `sbom-cyclonedx-json` | `security` | `sbom.json` |
| `fieldtest-output` | `fieldtest` | Directory upload; must contain **`replay_explorer_surface.json`** and **`replay_explorer_surface_report.json`** |

Upload steps use `if-no-files-found: error` where applicable so missing outputs fail the workflow truthfully.

## Field-test outputs

Under `out/fieldtest/` after `make fieldtest`:

- `replay_explorer_surface.json`  
- `replay_explorer_surface_report.json`  

Additional files may appear in that directory; CI uploads the **whole directory** for diligence flexibility.

## Non-claims

- **Not** live StarCraft II or Battle.net in CI.  
- **Not** raw `.SC2Replay` required for the field-test path (fixtures are governed JSON bundles per M31).  
- **Not** benchmark integrity, leaderboard validity, or replay↔execution equivalence.  
- **Not** M34 structural hygiene (shared I/O helpers, large test-file splits, etc.) unless explicitly chartered.  
- **Not** M35 public flagship proof-pack product work.

## Required-check posture

Branch protection should continue to require a truthful green **`CI`** run. The final job name **`governance`** is the intended **single aggregate** check when configuring required status checks by job name — verify repository settings after workflow changes.

## Related documents

- `docs/getting_started_clone_to_run.md`  
- `docs/diligence/field_test_checklist.md`  
- `docs/diligence/field_test_session_template.md`  
- `docs/starlab_operating_manual_v0.md`
