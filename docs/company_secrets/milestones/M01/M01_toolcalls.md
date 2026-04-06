# M01 toolcalls log

Session: 2026-04-06 — M01 (SC2 runtime surface & environment lock): implementation + closeout prep.

---

## Branch and commits

| Item | Value |
|------|--------|
| Branch | `m01-sc2-runtime-surface-env-lock` |
| Implementation commit (first push) | `378c86425b63b7b0c048a011644333058a548e80` |
| Closeout commit (current PR tip) | `260c4e022db06a4e02f2827ec1efec8fa9b3c992` |
| Base (`origin/main` at branch creation) | `725250018bb09ce84e772ded0c7a184cc7d764ea` |

---

## Pre-push verification (local)

Run on branch `m01-sc2-runtime-surface-env-lock` at `378c86425b63b7b0c048a011644333058a548e80` after docstring line-length fix (implementation); closeout commit `260c4e0…` is docs-only — same Ruff/Mypy/pytest surface.

| Command | Result |
|---------|--------|
| `ruff check .` | All checks passed! |
| `ruff format --check .` | 8 files already formatted |
| `mypy starlab tests` | Success: no issues found in 8 source files |
| `pytest` / `pytest -q` | 32 passed |
| `python -W error -m starlab.sc2.env_probe` | Exit 0; JSON probe output; no warnings |

**Note:** Repository CI workflow uses `ruff check starlab tests` (not `ruff check .`). Full-repo `ruff check .` was used for M01 pre-push parity; one E501 in `starlab/__init__.py` was fixed (wrapped docstring) so `ruff check .` passes.

Probe CLI: output is always JSON; there is no separate `--json` flag. Invocation recorded: `python -W error -m starlab.sc2.env_probe` (strict warnings).

---

## Push and PR

| Item | Value |
|------|--------|
| PR | [#2](https://github.com/m-cahill/starlab/pull/2) |
| Title | M01: SC2 runtime surface decision and environment lock |
| PR head SHA (current) | `260c4e022db06a4e02f2827ec1efec8fa9b3c992` |

---

## Authoritative PR-head CI (current tip)

Two PR-head runs executed:

| Run | Commit | Run ID | URL | Conclusion |
|-----|--------|--------|-----|------------|
| A (implementation) | `378c864…` | `24048416111` | https://github.com/m-cahill/starlab/actions/runs/24048416111 | success |
| B (closeout docs) | `260c4e0…` | `24048498203` | https://github.com/m-cahill/starlab/actions/runs/24048498203 | success |

**Authoritative for merge gating at current PR tip:** **Run B** — `24048498203` on `260c4e022db06a4e02f2827ec1efec8fa9b3c992`.

| Item | Value |
|------|--------|
| Workflow name | CI |
| Event | `pull_request` |
| Merge-gating | Yes — single `governance` job |

Monitored: `gh run watch 24048416111 --exit-status` and `gh run watch 24048498203 --exit-status` (both exit 0).

---

## Closeout artifacts (this session)

- `M01_run1.md` — workflow analysis (runs A + B)
- `M01_summary.md` — milestone summary
- `M01_audit.md` — milestone audit
- `docs/starlab.md` — §1 status, §7 M01 note, §18 PR/CI evidence, changelog PR #2 line
- `README.md` — current status aligned with PR-pending merge

**After merge to `main` (manual):** replace `(pending merge)` merge commit in §18; add post-merge `main` workflow run ID/URL; optionally add changelog line for merge SHA.

---

## Ledger alignment (2026-04-06)

`docs/starlab.md` §18 now lists **three** witnessed green PR-head runs on PR #2 (`378c864…` / `24048416111`, `260c4e0…` / `24048498203`, `88b06db…` / `24048576545`). GitHub PR #2 is authoritative for the **current** tip OID at merge time.

**Merge gate:** confirm the latest green PR-head CI run on [PR #2](https://github.com/m-cahill/starlab/pull/2) before merging (`gh pr view 2 --json statusCheckRollup,headRefOid`). Do not rely on a fixed OID in this log after further pushes.

---

## Merge to `main` (2026-04-06)

| Item | Value |
|------|--------|
| PR state | **MERGED** |
| Merge method | **Merge commit** (not squash) |
| Merge commit | `4a916033f55c6b8c4a582f985233a64ca039ead3` |
| Merged at (GitHub) | `2026-04-06T20:26:27Z` |
| Remote branch deleted | **Yes** (`m01-sc2-runtime-surface-env-lock` — 404 on GitHub API) |
| Post-merge `main` CI | Run `24049637412` — **success** — https://github.com/m-cahill/starlab/actions/runs/24049637412 |
| `main` tip after merge | `4a916033f55c6b8c4a582f985233a64ca039ead3` (same as merge commit until further commits) |

Ledger updated in `docs/starlab.md` §18 and changelog on `main` in the same closeout commit as this appendix.

---
