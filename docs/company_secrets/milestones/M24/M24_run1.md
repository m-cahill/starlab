# M24 CI run 1 — Attribution, Diagnostics, and Failure Views

**Milestone:** M24  
**Purpose:** Authoritative GitHub Actions workflow runs for the M24 merge ([PR #27](https://github.com/m-cahill/starlab/pull/27)).

## Final PR head (merge gate)

* **SHA:** `5caf1fbdbe7f7441fc2c8144efc3b18a37682779` (short `5caf1fb…`)
* **Merged at (UTC):** 2026-04-09T21:00:08Z

## Merge commit

* **SHA:** `7b4d3b4603dc40fe2ade33e1c943a0efd40ca5a4` (short `7b4d3b4…`)
* **Message:** Merge pull request #27 from m-cahill/m24-evaluation-diagnostics-failure-views
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m24-evaluation-diagnostics-failure-views` **deleted** after merge (`gh pr merge --delete-branch`)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24213046380`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24213046380

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #27 to `main`; **authoritative** merge-boundary run)
* **headSha:** `7b4d3b4603dc40fe2ade33e1c943a0efd40ca5a4`
* **Workflow run ID:** `24213094531`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24213094531

## Superseded red PR-head (not merge authority)

* None for M24 (single green PR-head on final tip).

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success**.

## Pytest

* **436** tests passed on authoritative PR-head run (one pre-existing `s2protocol` / `imp` deprecation warning in replay CLI tests — unchanged; not introduced by M24 `starlab/evaluation/` modules).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Workflow identity:** CI · runs `24213046380` (PR) / `24213094531` (`main` push); trigger `pull_request` / `push`; branch `m24-evaluation-diagnostics-failure-views` @ `5caf1fb…` / `main` @ `7b4d3b4…`.
* **Change context:** M24 — deterministic **interpretive** diagnostics over one governed **M23** `evaluation_tournament.json`; no new tournament scoring semantics; no evidence-pack (**M25**); no replay, live SC2, benchmark integrity.
* **Baseline:** Prior trusted green `main` @ `4fd8e3567646d4b8dc014adb70d320f731adf36c` (first parent of M24 merge commit) before M24 merge.
* **Step 1 — inventory:** Required merge-blocking job **governance** — Ruff, Ruff format, Mypy, Pytest, pip-audit, SBOM artifact, Gitleaks — all passed on both runs.
* **Step 2 — signal:** Tests exercise `tests/test_evaluation_diagnostics.py` + governance + full suite; static gates enforce repo policy.
* **Step 3 — delta:** Touches `starlab/evaluation/`, `docs/`, `tests/`; CI signals cover changed Python and tests.
* **Step 4 — failures:** None.
* **Step 5 — invariants:** Required checks enforced; milestone scope remains interpretive fixture-only consumer; no `starlab.replays` / `starlab.sc2` / `s2protocol` in M24 evaluation modules (test-enforced).
* **Step 6 — verdict:** Both runs are **safe to treat as merge authority** for M24: PR-head green on final tip + merge-boundary `main` green on merge commit.
* **Step 7 — next actions:** Record evidence in ledger (`docs/starlab.md`); **M25** remains stub-only (no product code in this closeout).

## Milestone closeout PR (non-merge-boundary for product)

Documentation and governance alignment landed in [PR #28](https://github.com/m-cahill/starlab/pull/28) (merged **2026-04-09T21:05:11Z** UTC; merge commit `5590f544cb29e7ad14fcbf5398903995b27da95c`; tip `49f175d108ec3bb9eaed7044be92471994c9b79e`).

* **PR-head CI:** [`24213306545`](https://github.com/m-cahill/starlab/actions/runs/24213306545) (**success**)
* **Merge-push `main` CI:** [`24213308716`](https://github.com/m-cahill/starlab/actions/runs/24213308716) (**success**)

These runs are **not** substitute merge authority for M24 **product** code — **authoritative** M24 product merge evidence remains **PR-head** [`24213046380`](https://github.com/m-cahill/starlab/actions/runs/24213046380) + **merge-boundary** [`24213094531`](https://github.com/m-cahill/starlab/actions/runs/24213094531) above.

## Notes

* Further **documentation-only** green runs on `main` after this row are **not** merge-boundary events for M24 product unless explicitly recorded in §23 / §18.
