# CI / Workflow Analysis — M05 (authoritative PR-head + post-merge `main`)

**Milestone:** M05 — Canonical Run Artifact v0  
**Project:** STARLAB  
**Mode:** Milestone merge gate + post-merge verification

---

## A. PR-head CI (authoritative merge gate)

| Field | Value |
| ----- | ----- |
| **Workflow name** | CI |
| **Run ID** | `24062592376` |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24062592376 |
| **Trigger** | `pull_request` |
| **Branch** | `m05-canonical-run-artifact-v0` |
| **Head SHA (tested)** | `53ace08e2ec9d29c780f31593bd945e82e1dfcac` |
| **Conclusion** | **success** |
| **PR** | [#6](https://github.com/m-cahill/starlab/pull/6) |

### Job inventory (`governance`)

| Step | Required | Pass/Fail |
| ---- | -------- | --------- |
| Ruff check | yes | pass |
| Ruff format check | yes | pass |
| Mypy | yes | pass |
| Pytest | yes | pass |
| pip-audit | yes | pass |
| CycloneDX SBOM | yes | pass |
| Gitleaks | yes | pass |

No `continue-on-error` observed on required steps.

### What this run proves

- **M05 surface** (canonical bundle builder, CLI, `load_replay_binding`, tests + golden fixtures) passes the **same** governance gates as prior milestones: lint, format, typing, tests, supply-chain scans.
- **Fixture portability:** after follow-on commits on the PR branch, **Pytest** passes on **Linux** (previously failed on golden vs. Windows path/CRLF drift; fixed via repo-relative paths + canonical JSON digests for M03 fixture `input_references`).

### What this run does **not** prove

- Replay **parser** correctness, replay **semantic** equivalence, **benchmark** validity, **cross-host** reproducibility, **live SC2** execution in CI, or inclusion of **raw replay / raw proof / raw config** in the canonical bundle — **explicit M05 non-claims** (see `docs/runtime/canonical_run_artifact_v0.md`).

### Verdict (PR-head)

**Merge approved** — required checks green at final PR tip `53ace08…`.

---

## B. Post-merge `main` CI (merge-commit boundary)

| Field | Value |
| ----- | ----- |
| **Workflow name** | CI |
| **Run ID** | `24062610358` |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24062610358 |
| **Trigger** | `push` to `main` |
| **Merge commit** | `bad27db36c135fd772e38dcafa64d6fa59577db0` |
| **Conclusion** | **success** |

**Distinction:** PR-head CI validates the **PR branch tip** before merge. Post-merge CI validates the **merge commit** on `main` (includes merge metadata; should remain green for the same code content).

---

## C. Failed runs (superseded)

Earlier PR-head runs on branch tips **`24062532070`**, **`24062562563`** failed at **Pytest** (golden snapshot vs. Linux path / newline drift). Resolved on tip **`53ace08…`** — **not** used as merge authority.

---

## D. Post-closeout `main` CI (non–merge-boundary)

After M05 milestone artifacts and ledger updates landed on `main` in commit `6edeb8af845d9cbfaed5c329c1c9a3398acac9dd`, CI re-ran on push.

| Field | Value |
| ----- | ----- |
| **Workflow name** | CI |
| **Run ID** | `24062664914` |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24062664914 |
| **Trigger** | `push` to `main` |
| **Commit** | `6edeb8af845d9cbfaed5c329c1c9a3398acac9dd` |
| **Conclusion** | **success** |

**Distinction:** This is **not** the merge-commit boundary (that remains `bad27db…` / run `24062610358`). It confirms docs/governance changes did not break the pipeline.

A subsequent documentation-only push (`ebca1e964c0539c78165bfab72c249a2157402cc`) updated §18/§23 cross-references; CI run **`24062700534`** (**success**) — also **non–merge-boundary**.

---

## E. Next actions

- Proceed to **M06** planning (stubs only) — **no** M06 product implementation until authorized.
