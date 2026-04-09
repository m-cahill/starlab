# M27 CI run 1 — Replay-Derived Imitation Baseline

**Milestone:** M27  
**Purpose:** Authoritative GitHub Actions workflow runs for the M27 merge ([PR #33](https://github.com/m-cahill/starlab/pull/33)).

## Final PR head (merge gate)

* **SHA:** `65dcd2fbfa1b6e8d05f6db8bebe191f4b8822ccc` (short `65dcd2f…`)
* **Merged at (UTC):** 2026-04-09T23:45:00Z

## Merge commit

* **SHA:** `49b45825b65e56deb5cf991c5f74889e3daf2f59` (short `49b4582…`)
* **Message:** Merge pull request #33 from m-cahill/m27-replay-derived-imitation-baseline
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m27-replay-derived-imitation-baseline` **deleted** after merge (`gh pr merge --delete-branch`)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24218875847`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24218875847

## Superseded red PR-head (not merge authority)

* **Workflow run ID:** `24218859455` — **failure** at **Ruff format check** on earlier tip `a4c2fc3…`; fixed on tip `65dcd2f…` — **not** merge authority for M27 product.

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #33 to `main`; **authoritative** merge-boundary run)
* **headSha:** `49b45825b65e56deb5cf991c5f74889e3daf2f59`
* **Workflow run ID:** `24218902938`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24218902938

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success** on authoritative PR-head (`24218875847`) and merge-boundary `main` (`24218902938`).

## Pytest

* **482** tests passed on authoritative PR-head CI [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) (one pre-existing `s2protocol` deprecation warning in replay CLI tests — unchanged; not introduced by M27 `starlab/imitation/` modules).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Workflow identity:** CI · runs `24218875847` (PR) / `24218902938` (`main` push); trigger `pull_request` / `push`; branch `m27-replay-derived-imitation-baseline` @ `65dcd2f…` / `main` @ `49b4582…`.
* **Change context:** M27 — deterministic **replay imitation baseline** + report over governed **M26** + **M14** via **M16 → M18** in-process materialization; majority-label-per-signature; explicit non-claims; **no** **M28** evaluation harness product code.
* **Baseline:** Prior trusted green `main` @ M26 closeout tip (`2ccf60e…` / prior merge `e83a849…`).
* **Step 1 — inventory:** Required merge-blocking job **governance** — all passed on authoritative PR-head and merge-boundary runs.
* **Verdict:** **24218875847** and **24218902938** are **safe to treat as merge authority** for M27: PR-head green on final tip + merge-boundary `main` green on merge commit.

## Milestone closeout (non-merge-boundary `main` push)

* **headSha:** `f41ba737855367136083a6c20d471fbff9b70070` (short `f41ba73…`)
* **Workflow run ID:** `24218984682`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24218984682

This run is **documentation + governance + M28 stubs only** — **not** substitute merge authority for M27 **product** — **authoritative** remains PR-head [`24218875847`](https://github.com/m-cahill/starlab/actions/runs/24218875847) + merge-boundary [`24218902938`](https://github.com/m-cahill/starlab/actions/runs/24218902938).
