# M26 CI run 1 — Replay Corpus Governance & Training Dataset Contract

**Milestone:** M26  
**Purpose:** Authoritative GitHub Actions workflow runs for the M26 merge ([PR #32](https://github.com/m-cahill/starlab/pull/32)).

## Final PR head (merge gate)

* **SHA:** `d8d3c4c82fdaab70e2238b40d4a5a7d30b2c230f` (short `d8d3c4c…`)
* **Merged at (UTC):** 2026-04-09T22:50:52Z

## Merge commit

* **SHA:** `e83a8493a577c9013d720f1debab009dcf9c464f` (short `e83a849…`)
* **Message:** Merge pull request #32 from m-cahill/m26-replay-corpus-training-dataset-contract
* **Merge method:** merge commit (GitHub **Create a merge commit**)
* **Remote branch:** `m26-replay-corpus-training-dataset-contract` **deleted** after merge (`gh pr merge --delete-branch`)

## Authoritative PR-head CI

* **Event:** `pull_request`
* **Workflow run ID:** `24217118559`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24217118559

## Merge-boundary post-merge `main` CI

* **Event:** `push` (merge of PR #32 to `main`; **authoritative** merge-boundary run)
* **headSha:** `e83a8493a577c9013d720f1debab009dcf9c464f`
* **Workflow run ID:** `24217178208`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24217178208

## Superseded red PR-head (not merge authority)

None observed for the final merge tip — **authoritative** merge gate for M26 product is **only** [`24217118559`](https://github.com/m-cahill/starlab/actions/runs/24217118559) on final PR head `d8d3c4c…`.

## Workflow inventory (authoritative + merge-boundary runs)

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — all **success** on both authoritative PR-head and merge-boundary `main` runs.

## Pytest

* **469** tests passed on full local run after M26 closeout tip (one pre-existing `s2protocol` / `imp` deprecation warning in replay CLI tests — unchanged; not introduced by M26 `starlab/imitation/` modules).

## Annotations (informational)

* Node.js 20 deprecation notice on GitHub Actions runners (same class as prior milestones); **not** a failure.

## Workflow analysis (aligned to `docs/company_secrets/prompts/workflowprompt.md`)

* **Workflow identity:** CI · runs `24217118559` (PR) / `24217178208` (`main` push); trigger `pull_request` / `push`; branch `m26-replay-corpus-training-dataset-contract` @ `d8d3c4c…` / `main` @ `e83a849…`.
* **Change context:** M26 — deterministic **replay training dataset** + report over governed **M14** bundle JSON; corpus selection + split + coarse labels; **no** model training; **no** **M27** imitation baseline product.
* **Baseline:** Prior trusted green `main` @ M25 closeout tip (`78ced31…` / merge `f03c7bf…`).
* **Step 1 — inventory:** Required merge-blocking job **governance** — Ruff, Ruff format, Mypy, Pytest, pip-audit, SBOM artifact, Gitleaks — all passed on authoritative PR-head and merge-boundary runs.
* **Step 2 — signal:** Tests exercise `tests/test_replay_training_dataset.py` + governance + full suite; static gates enforce repo policy.
* **Step 3 — delta:** Touches `starlab/imitation/`, `docs/`, `tests/`; CI signals cover changed Python and tests.
* **Step 4 — failures:** None on authoritative runs.
* **Step 5 — invariants:** Required checks enforced; milestone scope remains offline dataset contract over M14 bundles; no `starlab.replays` / `starlab.sc2` / `s2protocol` in M26 imitation modules (test-enforced).
* **Step 6 — verdict:** Both **24217118559** and **24217178208** are **safe to treat as merge authority** for M26: PR-head green on final tip + merge-boundary `main` green on merge commit.
* **Step 7 — next actions:** Ledger closeout (`docs/starlab.md`); **M27** remains stub-only (no imitation-baseline product code).

## Milestone closeout (non-merge-boundary `main` CI)

* **Closeout commit:** `2ccf60ea3a5aa6a4c4106bf9f6372bde06202d41` (short `2ccf60e…`) — message: `docs(m26): milestone closeout — ledger, governance, M27 stubs`
* **Workflow run ID:** `24217359747`
* **Conclusion:** success
* **URL:** https://github.com/m-cahill/starlab/actions/runs/24217359747

Milestone docs (`M26_run1.md`, `M26_summary.md`, `M26_audit.md`, `M26_plan.md`, `M26_toolcalls.md`), ledger §18/§23, governance tests, **M27** stubs — **not** a substitute for authoritative PR-head **24217118559** or merge-boundary **24217178208** for M26 **product** merge authority.

## Notes

* Further **documentation-only** green runs on `main` after the closeout commit are **not** merge-boundary events for M26 product unless explicitly recorded in §23 / §18 — **not** substitute merge authority for PR-head **24217118559** or merge-boundary **24217178208**.
