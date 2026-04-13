# M46 — CI / workflow analysis (final)

**Milestone:** M46 — Bounded Live Validation Final-Status Semantics  
**Status:** Closed on `main` (see `M46_summary.md` / `M46_audit.md`).

---

## Authoritative PR-head CI (final merge candidate)

| Field | Value |
| ----- | ----- |
| **PR** | [#57](https://github.com/m-cahill/starlab/pull/57) — **M46: Bounded live validation final_status semantics (Option A)** |
| **Branch** | `recharter/m44-bounded-live-final-status-semantics` |
| **Final PR head SHA** | `ddb18f4cf5e74af2cf3a0f657b66911c93bb97a8` |
| **Authoritative PR-head CI** | [`24332563005`](https://github.com/m-cahill/starlab/actions/runs/24332563005) — **success** (`headSha` matches final PR head); all required jobs |

**Superseded PR-head (not merge authority for final head `ddb18f4…`):** [`24332502917`](https://github.com/m-cahill/starlab/actions/runs/24332502917) — success on **`a100849…`** (earlier ledger-only tip; **not** final merge candidate).

---

## Merge to `main`

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `b925130d2e6bb9b2586139b17d100285e89b8e54` |
| **Merged at (UTC)** | **2026-04-13T18:12:03Z** (GitHub `mergedAt`) |
| **Branch after merge** | `recharter/m44-bounded-live-final-status-semantics` **retained** on `origin` (`--delete-branch=false`) |

---

## Merge-boundary `main` CI (merge commit `b925130…`)

| Run ID | Result | Notes |
| ------ | ------ | ----- |
| [`24359249759`](https://github.com/m-cahill/starlab/actions/runs/24359249759) | **failure** | Triggered on merge commit `b925130…`; **`security`** job — `pip-audit` reported **pytest** `CVE-2025-71176` (fix versions **≥9.0.3**). Required aggregate **`governance`** did not pass. |

This is **M46 product merge** evidence: **red merge-boundary** on first push — analogous to **M10** merge-push Mypy failure (see §18 / `M10` row).

---

## Repaired green `main` CI (not M46 product scope)

| Field | Value |
| ----- | ----- |
| **Commit** | `1b7b25ea22392a709bec726ce0827913d18cdca7` — `ci: pytest>=9.0.3 for pip-audit (CVE-2025-71176); M34 bound check <10` |
| **Workflow run** | [`24359357370`](https://github.com/m-cahill/starlab/actions/runs/24359357370) — **success** (required jobs: `quality`, `smoke`, `tests`, `security`, `fieldtest`, `flagship`, `governance`) |

**Role:** **CI hygiene / dependency repair** — **not** M46 bounded-status product semantics; **not** merge authority for PR #57 (PR-head authority remains **`24332563005`** on `ddb18f4…`).

---

## Post-closeout / ledger push `main` CI (not merge authority)

| Field | Value |
| ----- | ----- |
| **Commit** | `1b33acde84f0b719a6228507559b492b164f98b3` — docs closeout (`M46_run1` / summary / audit, §7 / §11 / §18 / §23, **M47** stub, governance tests) |
| **Workflow run** | [`24359543409`](https://github.com/m-cahill/starlab/actions/runs/24359543409) — **success** (required jobs: `quality`, `smoke`, `tests`, `security`, `fieldtest`, `flagship`, `governance`) |

**Role:** **Documentation / governance closeout** — **not** PR #57 merge authority; merge-boundary evidence remains [`24359249759`](https://github.com/m-cahill/starlab/actions/runs/24359249759) on `b925130…` (**failure**) + repaired green [`24359357370`](https://github.com/m-cahill/starlab/actions/runs/24359357370).

---

## Narrow M46 proof (product)

- **Option A:** Bounded **burnysc2** runs that record `bounded_exit` in the execution proof `status_sequence` emit **`match_execution.final_status="ok"`** (governed validation-contract completion at step cap).
- Literal SC2 **`Result`** preserved as **`sc2_game_result`** on `match_execution_proof.json` and (when present) on **`match_execution`** in `local_live_play_validation_run.json`.
- **M45** reward gate (`final_status == "ok"`) aligns with fixture/fake without claiming match victory.

---

## Explicit non-claims

- **Not** game victory, **not** ladder strength, **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI.
- **M42** `--contract` path mismatch (**M40** charter JSON vs **M20** benchmark contract) remains a **separate follow-on** (see **M47** stub).

---

## Annotated tag

- **`v0.0.46-m46`** on merge commit `b925130d2e6bb9b2586139b17d100285e89b8e54` (created and pushed after closeout commit `1b33acd…`; tag documents M46 merge boundary per release discipline).
