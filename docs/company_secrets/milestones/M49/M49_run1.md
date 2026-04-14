# M49 — CI / workflow analysis (final)

**Milestone:** M49 — Full local training / bootstrap campaign charter & evidence protocol  
**Status:** Closed on `main` (see `M49_summary.md` / `M49_audit.md`).

**Narrow proof:** governed **full local training campaign** contract + preflight receipt emitters, runtime doc, fixture tests — **not** execution of a long local operator campaign, **not** merge evidence for hours-long training.

---

## Authoritative PR-head CI (final merge candidate)

| Field | Value |
| ----- | ----- |
| **PR** | [#60](https://github.com/m-cahill/starlab/pull/60) — **M49: Full local training / bootstrap campaign charter & preflight** |
| **Branch** | `m49-full-local-training-campaign-charter` |
| **Final PR head SHA** | `2780de11bccd6a51cba3a1d14b24a0433e776873` |
| **Authoritative PR-head CI** | [`24381305623`](https://github.com/m-cahill/starlab/actions/runs/24381305623) — **success** (`headSha` matches final PR head); all required jobs |

**Superseded / non-authoritative (not merge authority for final head):**

| Run ID | Notes |
| ------ | ----- |
| [`24381216946`](https://github.com/m-cahill/starlab/actions/runs/24381216946) | Ruff format failure — superseded |
| [`24381253831`](https://github.com/m-cahill/starlab/actions/runs/24381253831) | Mypy failure (optional `sc2` import) — superseded; repaired in `2780de1` |

---

## Merge to `main`

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `cad5f2b4ad2a1ef01530efa35d996f513795b0ed` |
| **Merged at (UTC)** | **2026-04-14T04:43:06Z** (GitHub merge; author date **2026-04-13T21:43:06-07:00**) |
| **Branch after merge** | `m49-full-local-training-campaign-charter` **deleted** on `origin` (merge with branch delete) |

---

## Merge-boundary `main` CI (merge commit `cad5f2b…`)

| Run ID | Result | Notes |
| ------ | ------ | ----- |
| [`24381345315`](https://github.com/m-cahill/starlab/actions/runs/24381345315) | **success** | Push to `main` at merge commit `cad5f2b4ad2a1ef01530efa35d996f513795b0ed`; required aggregate **`governance`** and peer jobs **green**. |

---

## Narrow M49 proof (product)

- **Contract:** `full_local_training_campaign_contract.json` / report under `out/training_campaigns/<campaign_id>/` via `python -m starlab.training.emit_full_local_training_campaign_contract`.
- **Preflight:** `campaign_preflight_receipt.json` via `python -m starlab.training.emit_full_local_training_campaign_preflight` (environment / path / identity checks; optional `sc2` presence via `importlib.util.find_spec` — no stub-required import for Mypy).
- **Runtime:** `docs/runtime/full_local_training_campaign_v1.md`; cross-links from Phase VI diligence and M40/M42/M45 runtime docs.
- **Tests:** `tests/test_m49_full_local_training_campaign.py`, governance module list updates.

---

## Explicit non-claims

- **Not** a long local training campaign executed or evidenced as part of M49.
- **Not** new model families, benchmark semantics changes, or live SC2 in CI.
- **Not** `out/` committed to the repository; local campaign outputs remain operator-local.

---

## Annotated tag

- **`v0.0.49-m49`** on merge commit `cad5f2b4ad2a1ef01530efa35d996f513795b0ed` (created and pushed after ledger closeout per release discipline).

---

## Workflow-run analysis (merge-boundary)

Per `docs/company_secrets/prompts/workflowprompt.md` — **signal summary** for [`24381345315`](https://github.com/m-cahill/starlab/actions/runs/24381345315):

| Job / check | Required (merge gate) | Purpose | Pass |
| ----------- | ---------------------- | ------- | ---- |
| `quality` | Yes | Ruff, Mypy | Yes |
| `smoke` | Yes | Pytest smoke | Yes |
| `tests` | Yes | Full pytest + coverage | Yes |
| `security` | Yes | pip-audit, SBOM, Gitleaks | Yes |
| `fieldtest` | Yes | Field-test tier | Yes |
| `flagship` | Yes | Flagship proof pack | Yes |
| `governance` | Yes | Aggregate merge gate | Yes |

**Verdict:** Merge-boundary run is **authoritative** for M49 implementation merge; **merge approved** for this milestone scope.

---

## Post-closeout `main` CI (not merge authority until recorded)

| Field | Value |
| ----- | ----- |
| **Closeout commit** | `dad3268…` — `docs(m49): closeout artifacts, M50 stub, ledger, governance tests` |
| **Push CI** | [`24381499317`](https://github.com/m-cahill/starlab/actions/runs/24381499317) — **success** — ledger + closeout artifacts + tag push — **not** PR #60 merge authority; merge-boundary remains [`24381345315`](https://github.com/m-cahill/starlab/actions/runs/24381345315) on `cad5f2b…`. |
