# M29 CI run 1 — Hierarchical Agent Interface Layer

**Milestone:** M29  
**Purpose:** Authoritative GitHub Actions workflow runs for the M29 merge ([PR #35](https://github.com/m-cahill/starlab/pull/35)).

## Final PR head (merge gate)

* **SHA:** `60554e960a9227202578a3910052acaddf29677a` (short `60554e9…`)
* **Merged at (UTC):** 2026-04-10T01:29:12Z

## Merge commit

* **SHA:** `187d9ddd8e6b5234245923200c3a396d602e7b06` (short `187d9dd…`)
* **Message:** Merge pull request #35 from m-cahill/m29-hierarchical-agent-interface-layer
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m29-hierarchical-agent-interface-layer` **deleted** after merge (or stale remote ref removed)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24221769054`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24221769054

## Superseded red PR-head (not merge authority)

* **Workflow run ID:** `24221737387` — **failure** at **Ruff format** on earlier tip `bcc5e94…` — **not** merge authority; fixed on final tip `60554e9…`.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #35 to `main`; **authoritative** merge-boundary run)
* **headSha:** `187d9ddd8e6b5234245923200c3a396d602e7b06`
* **Workflow run ID:** `24221791088`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24221791088

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success** on authoritative PR-head (`24221769054`) and merge-boundary `main` (`24221791088`).

## Pytest

* **519** tests passed on authoritative PR-head CI [`24221769054`](https://github.com/m-cahill/starlab/actions/runs/24221769054) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged; not introduced by M29 `starlab/hierarchy/` modules).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Workflow identity:** CI · runs `24221769054` (PR) / `24221791088` (`main` push); trigger `pull_request` / `push`; branch `m29-hierarchical-agent-interface-layer` @ `60554e9…` / `main` @ `187d9dd…`.
* **Change context:** M29 — deterministic **offline** **two-level** hierarchical interface JSON Schema + report; worker coarse label enum **M29-owned**, aligned 1:1 to **`starlab.m26.label.coarse_action_v1`**; **`label_policy_id`** on worker response; **no** learned hierarchical agent, **no** benchmark semantics, **no** live SC2, **no** raw action legality claims.
* **Baseline:** Prior trusted green `main` @ M28 merge tip (`1ef6365…`).
* **Step 1 — inventory:** Required merge-blocking job **governance** — all passed on authoritative PR-head and merge-boundary runs.
* **Verdict:** **24221769054** and **24221791088** are **safe to treat as merge authority** for M29: PR-head green on final tip + merge-boundary `main` green on merge commit.

## Post-closeout `main` CI (documentation + ledger only)

* **Commit:** `d1566dd72884a98845bfb760fd1a591a311723f2` (short `d1566dd…`) — ledger §18/§23 + `M29_run1.md` / `M29_summary.md` / `M29_audit.md`; tag `v0.0.29-m29`.
* **Workflow run ID:** `24221851352` — **success** — https://github.com/m-cahill/starlab/actions/runs/24221851352
* **Note:** **not** substitute for M29 **product** merge authority (remains **24221769054** + **24221791088**).
