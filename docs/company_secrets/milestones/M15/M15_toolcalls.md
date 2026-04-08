# M15 toolcalls log

---

## 2026-04-08 — Stub seeded

* **Purpose:** Milestone folder for **M15** (canonical state schema v1) created during **M14** closeout so governance tests can require M15 stub files.
* **Status:** No M15 implementation.

---

## 2026-04-07 — M15 implementation kickoff

* **Purpose:** Replace `M15_plan.md` with full plan; add `starlab/state/` package, runtime contract, fixtures, tests, governance updates (ledger at closeout only per plan).
* **Status:** In progress.

---

## 2026-04-08 — Restore + jsonschema validation

* **Purpose:** Restore working tree to commit `0ebb730` M15 implementation; switch `validate_canonical_state_frame` to **jsonschema** `Draft202012Validator` per locked decision; add `jsonschema` to `pyproject.toml` dependencies; remove duplicate untracked `tests/fixtures/m15/canonical_state_schema.json`.
* **Files:** `pyproject.toml`, `starlab/state/canonical_state_schema.py`
* **Status:** Done — full pytest / ruff / mypy green locally.

---

## 2026-04-08 — CI: Mypy stubs for jsonschema

* **Purpose:** PR #16 CI failed Mypy (`import-untyped` for `jsonschema`); add `types-jsonschema` to `[project.optional-dependencies] dev` in `pyproject.toml`.
* **Status:** Done — full `mypy starlab tests` green locally.
