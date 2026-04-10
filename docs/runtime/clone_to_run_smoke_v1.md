# Clone-to-run smoke contract (v1)

**Status:** Operational contract for M32+ **fixture-only** validation.  
**Authority:** Subordinate to `docs/starlab.md`.

## Purpose

Define a **repeatable** minimum path to show the repository is wired correctly after clone: dev install, fast smoke tests, optional M31 explorer emission on **checked-in** fixtures.

## Required commands (reference)

1. `python -m pip install -e ".[dev]"`  
2. `pytest -q -m smoke` (or `make smoke`)  
3. `python -m starlab.explorer.emit_replay_explorer_surface --bundle-dir tests/fixtures/m31/bundle --agent-path tests/fixtures/m30/replay_hierarchical_imitation_agent.json --output-dir <out>` (or `make fieldtest`)

## Outputs

- Smoke: exit code 0 from pytest.  
- Field test: `replay_explorer_surface.json`, `replay_explorer_surface_report.json` in the chosen output directory.

## Non-claims

- No live SC2 client execution.  
- No benchmark integrity or leaderboard validity.  
- No network or cloud deployment.
