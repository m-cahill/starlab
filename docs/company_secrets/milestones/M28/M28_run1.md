# M28 CI run 1 — Learned-Agent Evaluation Harness

**Milestone:** M28  
**Purpose:** Authoritative GitHub Actions workflow runs for the M28 merge ([PR #34](https://github.com/m-cahill/starlab/pull/34)).

## Final PR head (merge gate)

* **SHA:** `c7ca6e6be8fbd44e39357da82cca857eddbd8eb3` (short `c7ca6e6…`)
* **Merged at (UTC):** 2026-04-10T00:35:30Z

## Merge commit

* **SHA:** `1ef636524269ff77ac26ac37584d43b50e9fcbc6` (short `1ef6365…`)
* **Message:** Merge pull request #34 from m-cahill/m28-learned-agent-evaluation-harness
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m28-learned-agent-evaluation-harness` **deleted** after merge (`gh pr merge --delete-branch`)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24220323130`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24220323130

## Superseded red PR-head (not merge authority)

* None recorded for M28 — single green PR-head on final tip `c7ca6e6…`.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #34 to `main`; **authoritative** merge-boundary run)
* **headSha:** `1ef636524269ff77ac26ac37584d43b50e9fcbc6`
* **Workflow run ID:** `24220357580`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24220357580

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success** on authoritative PR-head (`24220323130`) and merge-boundary `main` (`24220357580`).

## Pytest

* **502** tests passed on authoritative PR-head CI [`24220323130`](https://github.com/m-cahill/starlab/actions/runs/24220323130) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged; not introduced by M28 `starlab/evaluation/` modules).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Workflow identity:** CI · runs `24220323130` (PR) / `24220357580` (`main` push); trigger `pull_request` / `push`; branch `m28-learned-agent-evaluation-harness` @ `c7ca6e6…` / `main` @ `1ef6365…`.
* **Change context:** M28 — deterministic **learned-agent evaluation** + report over **M20** `fixture_only` contract + frozen **M27** + **M26** (held-out **`test`** only) + **M14** bundles; embedded M20 scorecard; **no** M23 tournament, **no** M24/M25 surfaces; explicit non-claims.
* **Baseline:** Prior trusted green `main` @ M27 merge tip (`49b4582…`).
* **Step 1 — inventory:** Required merge-blocking job **governance** — all passed on authoritative PR-head and merge-boundary runs.
* **Verdict:** **24220323130** and **24220357580** are **safe to treat as merge authority** for M28: PR-head green on final tip + merge-boundary `main` green on merge commit.
