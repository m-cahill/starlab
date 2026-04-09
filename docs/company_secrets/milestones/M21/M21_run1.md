# M21 CI run 1 — Scripted Baseline Suite

**Milestone:** M21  
**Purpose:** Authoritative GitHub Actions workflow runs for the M21 merge ([PR #22](https://github.com/m-cahill/starlab/pull/22)).

## Final PR head (merge gate)

* **SHA:** `818002e56b512e504c27f12aba8a39bc73627c82` (short `818002e…`)
* **Merged at (UTC):** 2026-04-09T05:41:36Z

## Merge commit

* **SHA:** `092d00a8aff720a1df9cbb1beec1cbf661546953` (short `092d00a…`)
* **Message:** Merge pull request #22 from m-cahill/m21-scripted-baseline-suite

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24174468912`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24174468912

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #22 to `main`; **authoritative** merge-boundary run — not a later doc-only push)
* **headSha:** `092d00a8aff720a1df9cbb1beec1cbf661546953`
* **Workflow run ID:** `24174498486`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24174498486

## Superseded red PR-head (not merge authority)

* **Workflow run ID:** `24174444383` — **failure** at **Ruff format check** (`scripted_baseline_scorecards.py` would be reformatted; fixed on tip `818002e…`; **not** merge authority).

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success**.

## Pytest

* **371** tests passed on authoritative PR-head run (one pre-existing `s2protocol` / `imp` deprecation warning in replay CLI tests — unchanged; not introduced by M21 `starlab/baselines/`).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as M18–M20 audits); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Signal:** Required checks green on final PR head and on merge-boundary `main` push; merge gate and post-merge substrate checks are consistent with prior milestones.
* **Noise:** Node 20 action annotation is informational; does not block merge or change M21 product claims.
* **Milestone posture:** M21 remains **fixture-only scripted baseline suite + embedded M20 scorecards**; no heuristics, runner, tournament harness, benchmark integrity, replay↔execution equivalence, or live SC2 in CI.

## Notes

* Any **subsequent** green runs on `main` after this merge push (e.g. ledger-only follow-ups) are **not** merge-boundary authority unless explicitly recorded as such in §23.
