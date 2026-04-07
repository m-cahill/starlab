# M08 toolcalls log

---

## 2026-04-07 — M08 implementation kickoff

* **Tool:** Write / StrReplace / Shell (planned)
* **Purpose:** Implement replay parser substrate (`starlab.replays` parser modules, contract doc, optional `[replay-parser]` extra), align opaque replay fixture to `replay_m07_generated.SC2Replay` + regenerate M05 goldens, extend governance tests.
* **Files:** `pyproject.toml`, `starlab/replays/*.py`, `docs/runtime/replay_parser_substrate.md`, `tests/*`, `tests/fixtures/m05_expected/*`
* **Timestamp:** 2026-04-07 (session)

---

## 2026-04-07 — M08 implementation complete (pending PR / closeout)

* **Purpose:** Landed M08 parser substrate: `parser_models` / `parser_interfaces` / `parser_normalization` / `parser_io` / `s2protocol_adapter` / `parse_replay` CLI; runtime contract `docs/runtime/replay_parser_substrate.md`; optional extra `replay-parser` (`s2protocol`); governance + unit/CLI tests; replaced missing `synthetic_opaque_test.SC2Replay` usage with `replay_m07_generated.SC2Replay` and regenerated `m05_expected` goldens; seeded `M09` stub milestone files for `test_governance` requirements.
* **Verification:** `pytest`, `ruff check`, `ruff format`, `mypy` — all green in dev workspace.
* **Deferred to milestone closeout (per plan):** `docs/starlab.md` Phase II row + parser glossary, `M08_run1.md` / summary / audit, merge, ledger CI links.

---

## 2026-04-07 — Pre-PR verification (branch + commit)

* **Tool:** Shell — `pytest -q`, `ruff check .`, `ruff format --check .`, `mypy starlab tests` (matches `.github/workflows/ci.yml` for Ruff/Mypy scope; full-repo `ruff check .` per milestone request).
* **Purpose:** Record outcomes before `git commit` / `git push` / PR open on `m08-replay-parser-substrate`.
* **Files:** workspace root.
* **Timestamp:** 2026-04-07 (session)
* **Outcomes (local, Windows):**
  * `python -m pytest -q` → **169 passed**, 1 warning (`s2protocol` `imp` deprecation when optional extra present).
  * `python -m ruff check .` → **All checks passed!**
  * `python -m ruff format --check .` → **59 files already formatted**
  * `python -m mypy starlab tests` → **Success: no issues found in 59 source files**

---

## 2026-04-07 — Git branch, commit, push, PR open

* **Tool:** Shell — `git checkout -b m08-replay-parser-substrate`, `git add`, `git commit`, `git push -u origin m08-replay-parser-substrate`, `gh pr create`
* **Purpose:** Place M08 work on milestone branch and open PR titled **M08: replay parser substrate** (no merge).
* **Files:** full M08 diff as staged.
* **Timestamp:** 2026-04-07 (session)

---

## 2026-04-07 — CI fix: cross-platform opaque replay fixture bytes

* **Tool:** Shell / Write — `.gitattributes`, rewrite `tests/fixtures/replay_m07_*.SC2Replay` with LF-only newlines, regenerate `tests/fixtures/m05_expected/*`.
* **Purpose:** PR-head CI run `24069652969` failed **Pytest** on `test_end_to_end_fixture_chain_matches_golden`: Linux hashed `replay_m07_generated.SC2Replay` as `75d471bb…` while goldens expected `7aa01b43…` (Windows working tree had CRLF). Align repo bytes with LF so CI and dev match.
* **Superseded run:** [`24069652969`](https://github.com/m-cahill/starlab/actions/runs/24069652969) — **failure** at Pytest (manifest/hash drift).
* **Timestamp:** 2026-04-07 (session)

---

## 2026-04-07 — Authoritative merge-gate pair (final)

* **PR:** [#9](https://github.com/m-cahill/starlab/pull/9) — **M08: replay parser substrate**
* **Final PR head SHA (authoritative):** `a65fabfa7fd76d94a250208fe20c2c4dfdf57105`
* **Authoritative PR-head CI run:** [`24069974048`](https://github.com/m-cahill/starlab/actions/runs/24069974048) — **success**
* **Merge commit:** `b99233e807177d65737beaba5246efa67a3edce2` — merged **2026-04-07T07:52:12Z** — **merge method:** merge commit — remote branch **`m08-replay-parser-substrate` deleted**
* **Authoritative post-merge `main` CI:** [`24070602968`](https://github.com/m-cahill/starlab/actions/runs/24070602968) — **success** — commit `b99233e807177d65737beaba5246efa67a3edce2`

**Superseded PR-head / intermediate:** [`24069937757`](https://github.com/m-cahill/starlab/actions/runs/24069937757), [`24069894682`](https://github.com/m-cahill/starlab/actions/runs/24069894682), [`24069835276`](https://github.com/m-cahill/starlab/actions/runs/24069835276), [`24069782159`](https://github.com/m-cahill/starlab/actions/runs/24069782159) — historical greens before final tip; **not** the authoritative merge gate.

* **Superseded (failure):** [`24069652969`](https://github.com/m-cahill/starlab/actions/runs/24069652969) — **failure** (Pytest: M05 golden vs Linux replay hash mismatch; fixed before final tip)

---

## 2026-04-07 — Milestone closeout (documentation push on `main`)

* **Purpose:** `M08_run1.md`, `M08_summary.md`, `M08_audit.md`, `M08_plan.md` (**Status: Complete**), `M08_toolcalls.md` hygiene, `docs/starlab.md` ledger (M08 → M09).
* **Classification:** **Non-merge-boundary** — does not change the M08 merge commit or authoritative post-merge CI `24070602968` on `b99233e…`.
* **Closeout commit `a089f18…`:** CI [`24070704576`](https://github.com/m-cahill/starlab/actions/runs/24070704576) — **failure** (Pytest: governance drift).
* **Fix commit `c3b6f2c…`:** `tests/test_governance.py` — CI [`24070774045`](https://github.com/m-cahill/starlab/actions/runs/24070774045) — **success**.
* **Ledger sync commit `1cca021…`:** CI [`24070813310`](https://github.com/m-cahill/starlab/actions/runs/24070813310) — **success**.

---

## 2026-04-06 — Stub seeded (no implementation)

* **Purpose:** Milestone folder and stub plan created at **M07** closeout per project workflow.
* **Status:** No M08 implementation, tests, or feature code started (confirmed **2026-04-07** after M07 merge to `main`).
