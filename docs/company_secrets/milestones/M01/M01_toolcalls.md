# M01 toolcalls log

Session: 2026-04-06 — M01 (SC2 runtime surface & environment lock): implementation + closeout prep.

---

## Branch and commits

| Item | Value |
|------|--------|
| Branch | `m01-sc2-runtime-surface-env-lock` |
| Implementation commit | `378c86425b63b7b0c048a011644333058a548e80` |
| Base (`origin/main` at branch creation) | `725250018bb09ce84e772ded0c7a184cc7d764ea` |

---

## Pre-push verification (local)

Run on branch `m01-sc2-runtime-surface-env-lock` at `378c86425b63b7b0c048a011644333058a548e80` after docstring line-length fix.

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
| PR head SHA | `378c86425b63b7b0c048a011644333058a548e80` |

---

## Authoritative PR-head CI

| Item | Value |
|------|--------|
| Workflow name | CI |
| Run ID | `24048416111` |
| URL | https://github.com/m-cahill/starlab/actions/runs/24048416111 |
| Event | `pull_request` |
| Conclusion | **success** |
| Merge-gating | Yes — single `governance` job; required checks match repo workflow (Ruff, format, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks) |

Monitored to completion via `gh run watch 24048416111 --exit-status` (exit 0).

---

## Closeout artifacts (this session)

- `M01_run1.md` — workflow analysis
- `M01_summary.md` — milestone summary
- `M01_audit.md` — milestone audit
- `docs/starlab.md` — §1 status, §7 M01 note, §18 PR/CI evidence, changelog PR #2 line
- `README.md` — current status aligned with PR-pending merge

**After merge to `main` (manual):** replace `(pending merge)` merge commit in §18; add post-merge `main` workflow run ID/URL; optionally add changelog line for merge SHA.

---
