# M30 CI run 1 — First Learned Hierarchical Agent

**Milestone:** M30  
**Purpose:** Authoritative GitHub Actions workflow runs for the M30 merge ([PR #36](https://github.com/m-cahill/starlab/pull/36)).

## Final PR head (merge gate)

* **SHA:** `2a2744527d74acd953507e5b847ef9ce0a7497d3` (short `2a27445…`)
* **Merged at (UTC):** 2026-04-10T02:55:11Z

## Merge commit

* **SHA:** `1c3a5f63f0ac5f380d3fd1ffcab66ca0d7d422bf` (short `1c3a5f6…`)
* **Message:** Merge pull request #36 from m-cahill/m30-first-learned-hierarchical-agent
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m30-first-learned-hierarchical-agent` **deleted** after merge

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24223946664`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24223946664

## Superseded red PR-head (not merge authority)

* None recorded for M30.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #36 to `main`; **authoritative** merge-boundary run)
* **headSha:** `1c3a5f63f0ac5f380d3fd1ffcab66ca0d7d422bf`
* **Workflow run ID:** `24223976390`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24223976390

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success** on authoritative PR-head (`24223946664`) and merge-boundary `main` (`24223976390`).

## Pytest

* **537** tests passed on authoritative PR-head CI [`24223946664`](https://github.com/m-cahill/starlab/actions/runs/24223946664) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged; not introduced by M30 `starlab/hierarchy/` product modules).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to project CI practice)

* **Workflow identity:** CI · runs `24223946664` (PR) / `24223976390` (`main` push); trigger `pull_request` / `push`; branch `m30-first-learned-hierarchical-agent` @ `2a27445…` / `main` @ `1c3a5f6…`.
* **Change context:** M30 — deterministic **offline** **replay-derived** **two-level** learned hierarchical imitation (`replay_hierarchical_imitation_agent.json` + report); fixed delegate policy **`starlab.m30.delegate.fixed_four_v1`**; traces anchor to **`starlab.hierarchical_agent_interface_trace.v1`**; **no** benchmark semantics, **no** live SC2, **no** M31 product.
* **Baseline:** Prior trusted green `main` @ M29 merge tip (`187d9dd…`).
* **Verdict:** **24223946664** and **24223976390** are **safe to treat as merge authority** for M30: PR-head green on final tip + merge-boundary `main` green on merge commit.
