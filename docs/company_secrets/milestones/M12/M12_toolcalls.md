# M12 toolcalls log

---

## 2026-04-07 — Stub seeded

* **Purpose:** Milestone folder for **M12** (combat, scouting, and visibility windows) created during **M11** closeout so governance tests can require M12 stub files.
* **Status:** No M12 implementation.

---

## 2026-04-07 — M12 product implementation (branch)

* **Purpose:** Implement combat/scouting/visibility extraction, contract doc, fixtures, tests, narrow `docs/starlab.md` updates.
* **Files:** `starlab/replays/combat_scouting_visibility_*.py`, `extract_replay_combat_scouting_visibility.py`, `docs/runtime/replay_combat_scouting_visibility_extraction.md`, `tests/fixtures/m12/*`, `tests/test_replay_combat_scouting_visibility*.py`, `docs/starlab.md`, `tests/test_governance.py`, `M12_plan.md`.
* **Status:** Implementation complete; merge/closeout pending governance.

---

## 2026-04-07 — Local verification (pre-push)

Commands run from repo root (`c:\coding\starlab`), Windows PowerShell.

| Command | Result |
| --- | --- |
| `pytest -q` | `238 passed`, exit **0** (1 DeprecationWarning from `s2protocol` in unrelated test) |
| `ruff check .` | `All checks passed!`, exit **0** |
| `ruff format --check .` | `85 files already formatted`, exit **0** |
| `mypy starlab tests` | `Success: no issues found in 85 source files`, exit **0** |

**Note:** Earlier mypy failures in `combat_scouting_visibility_extraction.py` (duplicate `name` binding vs combat loop `c` shadowing) were fixed by renaming to `death`/`victim_type` and `identity_name`, and using `step_row`/`cat_raw` for M11 category hints.

---

## 2026-04-07 — Merge + closeout (post-merge)

* **PR:** [#13](https://github.com/m-cahill/starlab/pull/13); final head `59adce3422a840692a4961278c995c5029da43bb`; merge commit `78528958a616177b564e603c193fb0d7f8af734e`; merged `2026-04-07T23:23:48Z`; branch `m12-combat-scouting-visibility-windows` **deleted** on merge.
* **Authoritative green PR-head CI:** [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) (**success**).
* **Merge-boundary `main` CI:** [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513) (**success**).
* **Closeout:** `M12_run1.md`, `M12_summary.md`, `M12_audit.md`, `M12_plan.md` (complete), `docs/starlab.md` ledger, `docs/company_secrets/milestones/M13/` stubs (`M13_plan.md`, `M13_toolcalls.md`).
