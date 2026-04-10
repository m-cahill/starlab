# Getting started — clone to run

**Audience:** Engineers validating a fresh checkout on **fixture data only** (no live SC2 required for the paths below).

## Prerequisites

- **Python 3.11** (see `requires-python` in `pyproject.toml`).
- Git.

## Clone and install

```bash
git clone https://github.com/m-cahill/starlab.git
cd starlab
python -m pip install --upgrade pip setuptools
python -m pip install -e ".[dev]"
```

On Windows PowerShell, use the same commands (replace `python` with `py -3.11` if needed).

## Verify quality gates

Locally, mirror the CI **`quality`** + **`tests`** jobs:

```bash
ruff check starlab tests
ruff format --check starlab tests
mypy starlab tests
pytest -q
```

Or with **Make** (Git Bash / POSIX):

```bash
make install-dev
make lint
make typecheck
make test
```

CI splits these into parallel **`quality`**, **`smoke`**, **`tests`**, **`security`**, **`fieldtest`**, and a final **`governance`** aggregate — see `docs/runtime/ci_tiering_field_test_readiness_v1.md`.

## Fast smoke lane

```bash
make smoke
# equivalent:
pytest -q -m smoke
```

## Field test (M31 explorer on fixtures)

Emits `replay_explorer_surface.json` and `replay_explorer_surface_report.json` under `out/fieldtest/`:

```bash
make fieldtest
```

Equivalent commands:

```bash
python -m starlab.explorer.emit_replay_explorer_surface \
  --bundle-dir tests/fixtures/m31/bundle \
  --agent-path tests/fixtures/m30/replay_hierarchical_imitation_agent.json \
  --output-dir out/fieldtest
```

## Coverage (local)

```bash
make coverage
# writes coverage.xml when pytest-cov runs with xml reporter; see pyproject.toml
```

## What is proved vs not

- **Proved:** artifact contracts merged per milestone, with CI (lint, types, tests, pip-audit, SBOM, secret scan).  
- **Not proved by default:** benchmark integrity, live SC2 in CI, flagship proof pack — see `docs/starlab.md` non-claims.

Further detail: `docs/runtime/clone_to_run_smoke_v1.md`, `docs/diligence/field_test_checklist.md`.
