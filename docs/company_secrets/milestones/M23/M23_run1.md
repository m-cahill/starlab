# M23 CI run 1 — Evaluation Runner & Tournament Harness

**Milestone:** M23  
**Purpose:** Authoritative GitHub Actions workflow runs for the M23 merge ([PR #24](https://github.com/m-cahill/starlab/pull/24)).

## Final PR head (merge gate)

* **SHA:** `f00711a3a2c16573f31492398de59387fe284711` (short `f00711a…`)
* **Merged at (UTC):** 2026-04-09T07:41:53Z

## Merge commit

* **SHA:** `b8857d2ccfdb2963d4fd2311f98d02cbe79aa252` (short `b8857d2…`)
* **Message:** Merge pull request #24 from m-cahill/m23-evaluation-runner-tournament-harness
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m23-evaluation-runner-tournament-harness` **deleted** after merge (`gh pr merge --delete-branch`)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24178571859`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24178571859

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #24 to `main`; **authoritative** merge-boundary run)
* **headSha:** `b8857d2ccfdb2963d4fd2311f98d02cbe79aa252`
* **Workflow run ID:** `24178615940`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24178615940

## Superseded red PR-head (not merge authority)

* None for M23 (single green PR-head on final tip).

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success**.

## Pytest

* **413** tests passed on authoritative PR-head run (one pre-existing `s2protocol` / `imp` deprecation warning in replay CLI tests — unchanged; not introduced by M23 `starlab/evaluation/`).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Workflow identity:** CI · runs `24178571859` (PR) / `24178615940` (`main` push); trigger `pull_request` / `push`; branch `m23-evaluation-runner-tournament-harness` @ `f00711a…` / `main` @ `b8857d2…`.
* **Change context:** M23 — fixture-only evaluation tournament from M20 + M21/M22 suite artifacts; round-robin harness; primary metric decides pairwise outcome; consumer-certification style proof; not attribution (M24), evidence pack (M25), replay, live SC2, benchmark integrity.
* **Baseline:** Prior trusted green `main` @ `621277c…` before M23 merge.
* **Step 1 — inventory:** Required merge-blocking job **governance** — Ruff, Ruff format, Mypy, Pytest, pip-audit, SBOM artifact, Gitleaks — all passed on both runs.
* **Step 2 — signal:** Tests exercise `tests/test_evaluation_tournament.py` + governance; static gates enforce repo policy; no coverage gate beyond test pass.
* **Step 3 — delta:** Touches `starlab/evaluation/`, `docs/`, `tests/`; CI signals directly cover changed Python and tests.
* **Step 4 — failures:** None.
* **Step 5 — invariants:** Required checks enforced; milestone scope remains fixture-only; no `starlab.replays` / `starlab.sc2` / `s2protocol` in M23 evaluation modules (test-enforced).
* **Step 6 — verdict:** Both runs are **safe to treat as merge authority** for M23: PR-head green on final tip + merge-boundary `main` green on merge commit.
* **Step 7 — next actions:** Record evidence in ledger (`docs/starlab.md`); **M24** remains stub-only.

## Notes

* Any **subsequent** green runs on `main` after this merge push (e.g. doc-only closeout) are **not** merge-boundary authority unless explicitly recorded in §23.
