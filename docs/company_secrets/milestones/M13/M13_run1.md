# M13 — CI / workflow evidence (run1)

**Milestone:** M13 — Replay Slice Generator  
**Purpose:** Authoritative CI classification for **merge-gate PR-head** vs **merge-boundary `main`** vs non-merge-boundary doc-only runs.

---

## Authoritative PR-head CI (merge gate)

| Field | Value |
| ----- | ----- |
| **PR** | [#14](https://github.com/m-cahill/starlab/pull/14) |
| **Final PR head SHA** | `6231b19cd7067130fd3324dcd3070172333ba766` |
| **Witnessed `pull_request` run** | [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) |
| **Conclusion** | **success** |
| **Workflow** | `CI` — job `governance` (Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks) |

**Authoritative green PR-head CI:** **yes** — a single completed **success** `pull_request` run on the final merge tip `6231b19…` is cited as merge authority for M13.

### Workflow analysis (merge-gate evidence — `workflowprompt.md`)

| Job / check | Required | Purpose | Pass/Fail | Notes |
| ----------- | -------- | ------- | --------- | ----- |
| `governance` | yes | Single job; full gate | **Pass** | Trigger: `pull_request`; branch: `m13-replay-slice-generator` @ `6231b19…` |
| Ruff check | yes | Style / lint | Pass | |
| Ruff format check | yes | Format | Pass | |
| Mypy | yes | Static types | Pass | |
| Pytest | yes | Tests + fixtures | Pass | |
| pip-audit | yes | Supply chain | Pass | |
| CycloneDX SBOM + upload | yes | SBOM artifact | Pass | |
| Gitleaks | yes | Secret scan | Pass | |

**Classification:** **Authoritative PR-head merge-gate evidence** — green final tip before merge; suitable for milestone closure and merge authorization.

**Noise / non-blocking:** runner annotation — GitHub Actions Node.js 20 deprecation notice on action versions (informational; not a failing check).

---

## Authoritative post-merge `main` CI (merge boundary — merge commit)

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `f86e36837e81b8552639c5a885a13a773b96215c` |
| **Workflow run ID** | `24112556177` |
| **Conclusion** | **success** |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24112556177 |
| **Trigger** | `push` to `main` (merge of PR #14) |
| **Merged at (UTC)** | `2026-04-08T01:20:38Z` (GitHub merge timestamp) |

This run is the **witnessed merge-push** for the M13 merge commit **and is green** — no merge-boundary repair commit was required for M13.

**Classification:** **Merge-boundary `main` CI** — first `push` to `main` from merging PR #14.

---

## Merge discipline

| Field | Value |
| ----- | ----- |
| **Merge method** | Merge commit (`gh pr merge 14 --merge`) |
| **Remote branch after merge** | `m13-replay-slice-generator` **deleted** (`--delete-branch`) |

---

## Non-merge-boundary runs (expected)

Closeout / ledger documentation pushes to `main` after this merge boundary may produce additional green `main` runs; those are **not** merge-boundary events unless triggered by a new PR merge. **Authoritative** merge-gate + merge-push evidence for M13 product merge remains PR-head [`24112526047`](https://github.com/m-cahill/starlab/actions/runs/24112526047) + merge-push [`24112556177`](https://github.com/m-cahill/starlab/actions/runs/24112556177).
