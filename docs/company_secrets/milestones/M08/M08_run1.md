# M08 — CI / workflow evidence (run1)

**Milestone:** M08 — Replay Parser Substrate  
**Purpose:** Authoritative CI classification for merge gating vs post-merge `main` vs follow-up documentation runs.

---

## Authoritative PR-head CI (merge gate)

| Field | Value |
| ----- | ----- |
| **PR** | [#9](https://github.com/m-cahill/starlab/pull/9) |
| **Final PR head SHA** | `a65fabfa7fd76d94a250208fe20c2c4dfdf57105` |
| **Workflow run ID** | `24069974048` |
| **Conclusion** | **success** |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24069974048 |
| **Trigger** | `pull_request` (CI on PR branch at merge tip) |

This run is the **authoritative merge gate** for the M08 feature branch before merge to `main`.

---

## Authoritative post-merge `main` CI (merge boundary)

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `b99233e807177d65737beaba5246efa67a3edce2` |
| **Workflow run ID** | `24070602968` |
| **Conclusion** | **success** |
| **URL** | https://github.com/m-cahill/starlab/actions/runs/24070602968 |
| **Trigger** | `push` to `main` (merge of PR #9) |
| **Event time (UTC)** | `2026-04-07T07:52:16Z` (workflow start; aligns with merge push) |

This run validates **`main` at the merge commit** immediately after PR #9 landed. It is the **authoritative post-merge `main` CI** for the M08 merge boundary.

**Workflow:** `CI` — job `governance` (Ruff, Mypy, Pytest, pip-audit, CycloneDX SBOM, Gitleaks).

---

## Superseded or non-authoritative PR-head runs

| Run ID | Conclusion | Notes |
| ------ | ---------- | ----- |
| `24069652969` | failure | Pytest: M05 golden vs Linux replay hash (CRLF/LF); fixed before final green tip. **Superseded** — not merge authority. |

Intermediate green runs on the PR branch before the final tip are **historical** only; the **authoritative PR-head** pair is **`a65fabf…` + `24069974048`**.

---

## Non-merge-boundary runs (documentation / ledger closeout)

After the merge commit, any additional `push` to `main` that updates only milestone closeout docs, `docs/starlab.md`, or `M08_toolcalls.md` hygiene **is not** a merge-boundary event.

Those runs (if any) are recorded in `docs/starlab.md` §23 and in the **Non-merge-boundary** subsection below once they exist.

### Non-merge-boundary (doc-only / ledger-only)

**Superseded (not ledger authority):** run [`24070704576`](https://github.com/m-cahill/starlab/actions/runs/24070704576) — **failure** at **Pytest** (`test_current_milestone_is_m08` vs §11 **M09**); fixed by updating `tests/test_governance.py` in the follow-up commit.

*(Green non-merge-boundary run for closeout commits — recorded below after the fix push.)*

---

## Merge metadata (reference)

| Field | Value |
| ----- | ----- |
| **Merged at (UTC)** | `2026-04-07T07:52:12Z` |
| **Merge method** | **Merge commit** (`Merge pull request #9 …`) |
| **Remote branch `m08-replay-parser-substrate`** | **Deleted** (remote ref not found after merge) |
