# M20 CI run 1 — Benchmark Contract & Scorecard Semantics

**Milestone:** M20  
**Purpose:** Authoritative GitHub Actions workflow runs for the M20 merge ([PR #21](https://github.com/m-cahill/starlab/pull/21)).

## Final PR head (merge gate)

* **SHA:** `5c2233690a3dc6d352dd9b06be16430b3d73b6e8` (short `5c22336…`)
* **Merged at (UTC):** 2026-04-09T04:59:35Z

## Merge commit

* **SHA:** `cf1bee980756b3b59d4db2620c041a23f14eba18` (short `cf1bee9…`)
* **Message:** Merge pull request #21 from m-cahill/m20-benchmark-contract-scorecard-semantics

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24173251270`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24173251270

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #21 to `main`; **authoritative** merge-boundary run — not a later doc-only push)
* **headSha:** `cf1bee980756b3b59d4db2620c041a23f14eba18`
* **Workflow run ID:** `24173270201`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24173270201

## Workflow inventory (both runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success**.

## Pytest

* **357** tests passed on authoritative PR-head run (one pre-existing `s2protocol` / `imp` deprecation warning in replay CLI tests — unchanged; not introduced by M20 `starlab/benchmarks/`).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as M18/M19 audits); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Signal:** Required checks green on final PR head and on merge-boundary `main` push; merge gate and post-merge substrate checks are consistent with prior milestones.
* **Noise:** Node 20 action annotation is informational; does not block merge or change M20 product claims.
* **Milestone posture:** M20 remains **schema emission + validation only**; no replay stack in `starlab/benchmarks/`.

## Notes

* Any **subsequent** green runs on `main` after this merge push (e.g. ledger-only follow-ups) are **not** merge-boundary authority unless explicitly recorded as such in §18.
