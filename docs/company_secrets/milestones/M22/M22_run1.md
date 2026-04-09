# M22 CI run 1 — Heuristic Baseline Suite

**Milestone:** M22  
**Purpose:** Authoritative GitHub Actions workflow runs for the M22 merge (PR **TBD** — record after merge to `main`).

## Final PR head (merge gate)

* **SHA:** *TBD* — update after merge
* **Merged at (UTC):** *TBD*

## Merge commit

* **SHA:** *TBD*
* **Message:** *TBD*

## Authoritative PR-head CI

* **Workflow run ID:** *TBD*
* **Conclusion:** *TBD*
* **URL:** *TBD*

## Merge-boundary post-merge `main` CI

* **Workflow run ID:** *TBD*
* **Conclusion:** *TBD*
* **URL:** *TBD*

## Workflow inventory

Single job **governance**: Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM upload, Gitleaks — expected **success** on final PR head and merge-boundary push.

## Notes

* Replace *TBD* fields after the M22 PR merges with authoritative PR-head and merge-boundary run IDs (see `docs/company_secrets/prompts/workflowprompt.md`).
* Any subsequent green `main` runs after the merge push (ledger-only follow-ups) are **not** merge-boundary authority unless recorded in §23.
