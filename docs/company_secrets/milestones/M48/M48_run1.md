# M48 — CI / workflow analysis (final)

**Milestone:** M48 — Learned-agent comparison contract-path alignment  
**Status:** Closed on `main` (see `M48_summary.md` / `M48_audit.md`).

**Deferred from:** Prior **M47** stub topic (recharter **2026-04-13**); **M47** closed separately as **Bootstrap Episode Distinctness & Operator Ergonomics** — see `docs/starlab.md` §23.

---

## Authoritative PR-head CI (final merge candidate)

| Field | Value |
| ----- | ----- |
| **PR** | [#59](https://github.com/m-cahill/starlab/pull/59) — **M48: learned-agent comparison contract-path alignment** |
| **Branch** | `m48-learned-agent-comparison-contract-path-alignment` |
| **Final PR head SHA** | `d94bc02c78bf75605edc4d28473f48cac986e53c` |
| **Authoritative PR-head CI** | [`24375633299`](https://github.com/m-cahill/starlab/actions/runs/24375633299) — **success** (`headSha` matches final PR head); all required jobs |

**Superseded / non-authoritative:** None recorded for final head `d94bc02…` — sole green PR-head run on that tip.

---

## Merge to `main`

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `cdd023cb388ae99c3649978857e07af04c17df50` |
| **Merged at (UTC)** | **2026-04-14T02:21:43Z** (GitHub `mergedAt`) |
| **Branch after merge** | `m48-learned-agent-comparison-contract-path-alignment` **deleted** on `origin` (`gh pr merge --delete-branch`) |

---

## Merge-boundary `main` CI (merge commit `cdd023c…`)

| Run ID | Result | Notes |
| ------ | ------ | ----- |
| [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946) | **success** | Push to `main` at merge commit `cdd023cb388ae99c3649978857e07af04c17df50`; required aggregate **`governance`** and peer jobs **green**. |

---

## Narrow M48 proof (product)

- **M20 benchmark contract path:** CLI **`--benchmark-contract`** (alias **`--contract`**) loads the **M20** benchmark contract JSON used by **M28** / **M42** validation; help text unambiguous.
- **M40 training-program charter:** Optional **`--training-program-contract`** loads on-disk M40 JSON (`verify_training_program_contract_digest` in `starlab.training.training_program_io`); default remains in-process `build_agent_training_program_contract()`.
- **M41 identity alignment:** When **`--m41`** candidates are present, harness compares active M40 charter **`contract_sha256`** / **`program_version`** to each run’s **`training_program_contract_sha256`** / **`training_program_contract_version`** — **strict `ValueError`** on mismatch.

---

## Explicit non-claims

- **Not** benchmark semantics expansion, **not** new M28 metrics, **not** training-track algorithm work.
- **Not** live SC2 in CI, **not** Phase VI integrated test campaign completion.
- **Not** replay↔execution equivalence or benchmark integrity.

---

## Annotated tag

- **`v0.0.48-m48`** on merge commit `cdd023cb388ae99c3649978857e07af04c17df50` (created and pushed after ledger closeout per release discipline).

---

## Workflow-run analysis (merge-boundary)

Per `docs/company_secrets/prompts/workflowprompt.md` — **signal summary** for [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946):

| Job / check | Required (merge gate) | Purpose | Pass |
| ----------- | ---------------------- | ------- | ---- |
| `quality` | Yes | Ruff, Mypy | Yes |
| `smoke` | Yes | Pytest smoke | Yes |
| `tests` | Yes | Full pytest + coverage | Yes |
| `security` | Yes | pip-audit, SBOM, Gitleaks | Yes |
| `fieldtest` | Yes | Field-test tier | Yes |
| `flagship` | Yes | Flagship proof pack | Yes |
| `governance` | Yes | Aggregate merge gate | Yes |

**Verdict:** Merge-boundary run is **authoritative** for M48 closure; **merge approved** for this milestone scope.

---

## Post-closeout `main` CI (not merge authority)

Runs after this closeout commit push (ledger + tag) — **not** PR #59 merge authority; merge-boundary remains [`24377511946`](https://github.com/m-cahill/starlab/actions/runs/24377511946) on `cdd023c…`.
