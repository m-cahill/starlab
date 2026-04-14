# M47 — CI / workflow analysis (final)

**Milestone:** M47 — Bootstrap Episode Distinctness & Operator Ergonomics  
**Status:** Closed on `main` (see `M47_summary.md` / `M47_audit.md`).

**Governance recharter (2026-04-13 — user-directed):** The prior ledger **M47** stub (**M42** `--contract` path alignment) is **deferred** to **M48** (stub). **M47** is rechartered to **Bootstrap Episode Distinctness & Operator Ergonomics** — formal governance event; see `docs/starlab.md` §23.

---

## Authoritative PR-head CI (final merge candidate)

| Field | Value |
| ----- | ----- |
| **PR** | [#58](https://github.com/m-cahill/starlab/pull/58) — **M47: Bootstrap Episode Distinctness & Operator Ergonomics** |
| **Branch** | `m47-bootstrap-episode-distinctness-ergonomics` |
| **Final PR head SHA** | `4a8fb3e2f7aad95d2cde5b6b77577db25e42e91e` |
| **Authoritative PR-head CI** | [`24374720293`](https://github.com/m-cahill/starlab/actions/runs/24374720293) — **success** (`headSha` matches final PR head); all required jobs |

---

## Merge to `main`

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `ebc5de0864ef6231d13efa741150d73c1ef1b98b` |
| **Merged at (UTC)** | **2026-04-14T00:47:56Z** (GitHub `mergedAt`) |
| **Branch after merge** | `m47-bootstrap-episode-distinctness-ergonomics` **retained** on `origin` (`--delete-branch=false`) |

---

## Merge-boundary `main` CI (merge commit `ebc5de0…`)

| Run ID | Result | Notes |
| ------ | ------ | ----- |
| [`24374756823`](https://github.com/m-cahill/starlab/actions/runs/24374756823) | **success** | Triggered on merge commit `ebc5de0…`; required aggregate **`governance`** and peer jobs **green**. |

---

## Narrow M47 proof (product)

- **Interpretation:** Multi-episode **M45** campaigns: **`episode_count_configured`** ≠ `N` independent samples unless governed identities differ (distinct **`validation_run_sha256`** / **`run_id`**).
- **Per-episode seed:** Default M02 **`seed`** = **`bootstrap_base_seed + episode_index`** via per-episode `bootstrap_match_config.json`.
- **Manifest v2:** **`starlab.m47.episode_manifest.v2`** with **`episode_seed_policy`**, **`distinct_episode_identities`**, collapse **`warnings`**.
- **Surfacing:** **`episode_distinctness`** on sealed **`self_play_rl_bootstrap_run.json`** / report.
- **Operator guidance:** `docs/runtime/self_play_rl_bootstrap_v1.md`.

---

## Explicit non-claims

- **Not** benchmark integrity, **not** sample-diversity proof beyond governed reporting, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder performance.
- **Not** **M42** `--contract` path alignment product — **M48** stub only; **no** M48 implementation in this milestone.

---

## Annotated tag

- **`v0.0.47-m47`** on merge commit `ebc5de0864ef6231d13efa741150d73c1ef1b98b` (created and pushed after ledger closeout commit per release discipline).

---

## Post-closeout / ledger push `main` CI (not merge authority)

| Field | Value |
| ----- | ----- |
| **Closeout commit** | `5dcba2d…` — `docs(m47): closeout ledger, M47 run1/summary/audit, governance tests` |
| **First push CI** | [`24374876505`](https://github.com/m-cahill/starlab/actions/runs/24374876505) — **failure** — **quality** — Ruff **format** check — **not** PR #58 merge authority |
| **Repair commit** | `9a80f7f…` — `style: ruff format test_governance_ci (M47 closeout)` |
| **Repaired `main` CI** | [`24374915005`](https://github.com/m-cahill/starlab/actions/runs/24374915005) — **success** (required jobs including **`governance`**) — ledger/tag/format hygiene — **not** PR #58 merge authority |

**Merge-boundary evidence for PR #58 remains:** [`24374756823`](https://github.com/m-cahill/starlab/actions/runs/24374756823) on merge commit `ebc5de0…`.
