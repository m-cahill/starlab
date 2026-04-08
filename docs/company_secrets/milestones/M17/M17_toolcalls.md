# M17 toolcalls log

---

## 2026-04-08 — Stub seeded

* **Purpose:** Milestone folder for **M17** (observation surface contract) created during **M16** closeout so governance tests can require M17 stub files.
* **Status:** No M17 implementation.

---

## 2026-04-08 — M17 implementation kickoff

* **Timestamp:** 2026-04-08 (session)
* **Tool:** `apply_patch` / write
* **Purpose:** Add `docs/runtime/observation_surface_contract_v1.md`, `starlab/observation/` package, CLI, fixtures, tests, governance + ledger updates.
* **Files:** `docs/runtime/observation_surface_contract_v1.md`, `starlab/observation/*.py`, `tests/fixtures/m17/*`, `tests/test_observation_surface_schema.py`, `tests/test_emit_observation_surface_schema_cli.py`, `test_governance.py`, `docs/starlab.md`, `docs/company_secrets/milestones/M17/M17_plan.md`
* **Status:** In progress

---

## 2026-04-08 — M17 implementation complete (local)

* **Timestamp:** 2026-04-08 (session)
* **Tools:** `apply_patch`, `run_terminal_cmd` (pytest / ruff / mypy)
* **Purpose:** Land M17 observation surface contract package, contract doc, fixtures/goldens, tests, governance + ledger updates; seed M18 stubs.
* **Files:** `docs/runtime/observation_surface_contract_v1.md`, `starlab/observation/*.py`, `tests/fixtures/m17/*`, `tests/test_observation_surface_schema.py`, `tests/test_emit_observation_surface_schema_cli.py`, `tests/test_governance.py`, `docs/starlab.md`, `docs/company_secrets/milestones/M17/M17_plan.md`, `docs/company_secrets/milestones/M18/*`
* **Status:** Complete pending merge-boundary PR/CI recording

---

## 2026-04-08 — Branch + local verification (closeout pass)

* **Branch:** `m17-observation-surface-contract` (created from `main`, working tree carried uncommitted M17 implementation).
* **Working tree before branch:** modified `M17_plan.md`, `M17_toolcalls.md`, `docs/starlab.md`, `tests/test_governance.py`; untracked `docs/runtime/observation_surface_contract_v1.md`, `starlab/observation/`, `tests/fixtures/m17/`, M17 tests, `docs/company_secrets/milestones/M18/`.

### Commands run (exact)

```text
python -m ruff check starlab tests
python -m ruff format --check starlab tests
python -m mypy starlab tests
python -m pytest -q
```

### Results (exact)

* **Ruff check:** `All checks passed!`
* **Ruff format:** `120 files already formatted`
* **Mypy:** `Success: no issues found in 120 source files`
* **Pytest:** `310 passed`, `1 warning` in `1.57s` (same run)
* **Warning (noted):** `DeprecationWarning: the imp module is deprecated` from `s2protocol` during `tests/test_parse_replay_cli.py::test_cli_writes_three_json_files` — upstream / optional replay-parser extra; **not** introduced by M17 observation modules.
