# M12 — CI / workflow evidence (run1)

**Milestone:** M12 — Combat, Scouting, and Visibility Windows  
**Purpose:** Authoritative CI classification for **merge-gate PR-head** vs **merge-boundary `main`** vs non-merge-boundary doc-only runs.

---

## Authoritative PR-head CI (merge gate)

| Field | Value |
| ----- | ----- |
| **PR** | [#13](https://github.com/m-cahill/starlab/pull/13) |
| **Final PR head SHA** | `59adce3422a840692a4961278c995c5029da43bb` |
| **Witnessed `pull_request` run** | [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) |
| **Conclusion** | **success** |
| **Workflow** | `CI` — job `governance` (Ruff check, Ruff format check, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks) |

**Authoritative green PR-head CI:** **yes** — a single completed **success** `pull_request` run on the final merge tip `59adce3…` is cited as merge authority for M12 (restores M11-style merge-gate discipline).

### Workflow analysis (merge-gate evidence — `workflowprompt.md`)

| Job / check | Required | Purpose | Pass/Fail | Notes |
| ----------- | -------- | ------- | --------- | ----- |
| `governance` | yes | Single job; full gate | **Pass** | Trigger: `pull_request`; branch: `m12-combat-scouting-visibility-windows` @ `59adce3…` |
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
| **Merge commit SHA** | `78528958a616177b564e603c193fb0d7f8af734e` |
| **Workflow run ID** | `24109269513` |
| **Conclusion** | **success** |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24109269513 |
| **Trigger** | `push` to `main` (merge of PR #13) |
| **Merged at (UTC)** | `2026-04-07T23:23:48Z` (GitHub merge timestamp) |

This run is the **witnessed merge-push** for the M12 merge commit **and is green** — no merge-boundary repair commit was required for M12.

**Classification:** **Merge-boundary `main` CI** — first `push` to `main` from merging PR #13.

---

## Non-merge-boundary runs (documentation / ledger closeout)

*None recorded for M12 — merge authority is PR-head [`24109242392`](https://github.com/m-cahill/starlab/actions/runs/24109242392) + merge-boundary `main` [`24109269513`](https://github.com/m-cahill/starlab/actions/runs/24109269513). A single post-merge ledger closeout commit may still trigger a green `push` run on `main`; that run is **not** merge-gate authority (see §17 / §23).*

---

## Merge metadata (reference)

| Field | Value |
| ----- | ----- |
| **Merge method** | **Merge commit** (`Merge pull request #13 …`) |
| **Remote branch `m12-combat-scouting-visibility-windows`** | **Deleted** after merge |
