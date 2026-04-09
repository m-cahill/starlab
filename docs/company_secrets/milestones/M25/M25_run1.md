# M25 CI run 1 — Baseline Evidence Pack

**Milestone:** M25  
**Purpose:** Authoritative GitHub Actions workflow runs for the M25 merge ([PR #31](https://github.com/m-cahill/starlab/pull/31)).

## Final PR head (merge gate)

* **SHA:** `b132bfd53f0f31b81f6d2955ca659d5923cdd4b1` (short `b132bfd…`)
* **Merged at (UTC):** 2026-04-09T21:57:32Z

## Merge commit

* **SHA:** `f03c7bf4337b61ea0f88ff07aa5b4adb2c88850b` (short `f03c7bf…`)
* **Message:** Merge pull request #31 from m-cahill/m25-baseline-evidence-pack
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m25-baseline-evidence-pack` **deleted** after merge (`gh pr merge --delete-branch`)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24215322933`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24215322933

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #31 to `main`; **authoritative** merge-boundary run)
* **headSha:** `f03c7bf4337b61ea0f88ff07aa5b4adb2c88850b`
* **Workflow run ID:** `24215360351`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24215360351

## Superseded red PR-head (not merge authority)

| Run ID | Conclusion | Notes |
| ------ | ---------- | ----- |
| [`24215241322`](https://github.com/m-cahill/starlab/actions/runs/24215241322) | failure | Pytest — `test_m25_planned_in_milestone_table` vs ledger **In progress** (fixed in follow-up commit) |
| [`24215286216`](https://github.com/m-cahill/starlab/actions/runs/24215286216) | failure | Ruff E501 — governance test docstring line length (fixed in follow-up commit) |

**Authoritative** merge gate for M25 product is **only** [`24215322933`](https://github.com/m-cahill/starlab/actions/runs/24215322933) on final PR head `b132bfd…`.

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success** on both authoritative PR-head and merge-boundary `main` runs.

## Pytest

* **448** tests passed on authoritative PR-head run (one pre-existing `s2protocol` / `imp` deprecation warning in replay CLI tests — unchanged; not introduced by M25 `starlab/evaluation/` evidence-pack modules).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Workflow identity:** CI · runs `24215322933` (PR) / `24215360351` (`main` push); trigger `pull_request` / `push`; branch `m25-baseline-evidence-pack` @ `b132bfd…` / `main` @ `f03c7bf…`.
* **Change context:** M25 — deterministic **interpretive packaging** over governed **M21/M22** suites + **M23** tournament + **M24** diagnostics; no new tournament/diagnostics semantics; no benchmark integrity; no live SC2; no M26 product.
* **Baseline:** Prior trusted green `main` @ merge-base before PR #31 (M24 closeout tip).
* **Step 1 — inventory:** Required merge-blocking job **governance** — Ruff, Ruff format, Mypy, Pytest, pip-audit, SBOM artifact, Gitleaks — all passed on authoritative PR-head and merge-boundary runs.
* **Step 2 — signal:** Tests exercise `tests/test_baseline_evidence_pack.py` + governance + full suite; static gates enforce repo policy.
* **Step 3 — delta:** Touches `starlab/evaluation/`, `docs/`, `tests/`; CI signals cover changed Python and tests.
* **Step 4 — failures:** None on authoritative runs; superseded red PR-heads documented above.
* **Step 5 — invariants:** Required checks enforced; milestone scope remains interpretive fixture-only packaging; no `starlab.replays` / `starlab.sc2` / `s2protocol` in M25 evaluation modules (test-enforced).
* **Step 6 — verdict:** Both **24215322933** and **24215360351** are **safe to treat as merge authority** for M25: PR-head green on final tip + merge-boundary `main` green on merge commit.
* **Step 7 — next actions:** Ledger closeout (`docs/starlab.md`); **M26** remains stub-only (no product code).

## Milestone closeout (this commit)

Documentation + governance alignment may ship in the same push as `M25_summary.md` / `M25_audit.md` updates on `main` after merge — **not** a substitute for authoritative PR-head **24215322933** for M25 **product** merge authority.

## Notes

* Further **documentation-only** green runs on `main` after this row are **not** merge-boundary events for M25 product unless explicitly recorded in §23 / §18.
