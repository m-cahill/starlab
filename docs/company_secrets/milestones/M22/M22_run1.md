# M22 CI run 1 — Heuristic Baseline Suite

**Milestone:** M22  
**Purpose:** Authoritative GitHub Actions workflow runs for the M22 merge ([PR #23](https://github.com/m-cahill/starlab/pull/23)).

## Final PR head (merge gate)

* **SHA:** `96aba181f725b1303d54779d48556b7dffd7feb4` (short `96aba18…`)
* **Merged at (UTC):** 2026-04-09T06:50:36Z

## Merge commit

* **SHA:** `470afa84ff80a2d76fb2693bce3a4397e6526afe` (short `470afa8…`)
* **Message:** Merge pull request #23 from m-cahill/m22-heuristic-baseline-suite
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m22-heuristic-baseline-suite` **deleted** after merge (`gh pr merge --delete-branch`)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24176685407`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24176685407

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #23 to `main`; **authoritative** merge-boundary run)
* **headSha:** `470afa84ff80a2d76fb2693bce3a4397e6526afe`
* **Workflow run ID:** `24176717132`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24176717132

## Superseded red PR-head (not merge authority)

* None for M22 (single green PR-head on final tip).

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success**.

## Pytest

* **392** tests passed on authoritative PR-head run (one pre-existing `s2protocol` / `imp` deprecation warning in replay CLI tests — unchanged; not introduced by M22 `starlab/baselines/`).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Workflow identity:** CI · runs `24176685407` (PR) / `24176717132` (`main` push); trigger `pull_request` / `push`; branch `m22-heuristic-baseline-suite` @ `96aba18…` / `main` @ `470afa8…`.
* **Change context:** M22 — fixture-only heuristic baseline suite + embedded M20 scorecards; consumer-certification style proof; not runner/tournament/replay/live SC2.
* **Baseline:** Prior trusted green `main` @ `606579d…` before M22 merge.
* **Step 1 — inventory:** Required merge-blocking job **governance** — Ruff, Ruff format, Mypy, Pytest, pip-audit, SBOM artifact, Gitleaks — all passed on both runs.
* **Step 2 — signal:** Tests exercise new `tests/test_heuristic_baseline_suite.py` + governance; static gates enforce repo policy; no coverage gate beyond test pass.
* **Step 3 — delta:** Touches `starlab/baselines/`, `docs/`, `tests/`; CI signals directly cover changed Python and tests.
* **Step 4 — failures:** None.
* **Step 5 — invariants:** Required checks enforced; milestone scope remains fixture-only emission; no workflow weakening.
* **Step 6 — verdict:** Both runs are **safe to treat as merge authority** for M22: PR-head green on final tip + merge-boundary `main` green on merge commit.
* **Step 7 — next actions:** Record evidence in ledger (this file + `docs/starlab.md`); **M23** remains stub-only.

## Notes

* Any **subsequent** green runs on `main` after this merge push (e.g. doc-only closeout) are **not** merge-boundary authority unless explicitly recorded in §23.
