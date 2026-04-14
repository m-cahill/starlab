# M50 — CI / workflow analysis (final)

**Milestone:** M50 — Industrial-scale hidden rollout mode & governed campaign execution v1  
**Status:** Closed on `main` (see `M50_summary.md` / `M50_audit.md`).

**Narrow proof:** governed **campaign execution** CLI over M49 contract, **honest** requested vs resolved visibility posture, PID lockfiles, extended execution preflight, heartbeat / stop / quarantine-first resume — **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** ladder/public performance.

---

## Authoritative PR-head CI (final merge candidate)

| Field | Value |
| ----- | ----- |
| **PR** | [#61](https://github.com/m-cahill/starlab/pull/61) — **M50: Industrial-scale hidden rollout mode & governed campaign execution v1** |
| **Branch** | `m50-industrial-hidden-rollout-mode` |
| **Final PR head SHA** | `a6f0b90045a01908d4a57682bd41743826e5d543` |
| **Authoritative PR-head CI** | [`24423972763`](https://github.com/m-cahill/starlab/actions/runs/24423972763) — **success** (`headSha` matches final PR head); required jobs green |

**Superseded / non-authoritative:** none recorded for final head.

---

## Merge to `main`

| Field | Value |
| ----- | ----- |
| **Merge commit SHA** | `a0430d3cd79b23d04c81cca1e11a404f50c4c35b` |
| **Merged at (UTC)** | **2026-04-14T21:48:43Z** (GitHub) |
| **Branch after merge** | `m50-industrial-hidden-rollout-mode` **retained** on `origin` |

---

## Merge-boundary `main` CI (merge commit `a0430d3…`)

| Run ID | Result | Notes |
| ------ | ------ | ----- |
| [`24424616487`](https://github.com/m-cahill/starlab/actions/runs/24424616487) | **success** | Push to `main` at merge commit `a0430d3cd79b23d04c81cca1e11a404f50c4c35b`; required aggregate **`governance`** and peer jobs **green**. |

---

## Narrow M50 proof (product)

- **Executor:** `python -m starlab.training.execute_full_local_training_campaign` — consumes M49 contract; orchestrates M45 `bootstrap_episodes` phases only (refit / M42 / watchable M44 not orchestrated in M50 v1).
- **Visibility:** `resolve_visibility_posture_v1` — requested vs resolved recorded on artifacts; default honest downgrade (e.g. `hidden` → `minimized`) with warnings.
- **Locks:** `.starlab_campaign_output.lock` (campaign root), `.campaign_execution.lock` (execution tree); stale PID detection.
- **Artifacts:** under `out/training_campaigns/<campaign_id>/campaign_runs/<execution_id>/` — `hidden_rollout_campaign_run.json`, manifest, heartbeat, resume state, per-phase M45 outputs.
- **Extended preflight:** `run_campaign_execution_preflight` (maps / SC2 probe / locks when applicable).
- **M45 hook:** `on_episode_complete` on `run_self_play_rl_bootstrap` for supervision.
- **Tests:** `tests/test_m50_campaign_execution.py`; governance alignment.

---

## Explicit non-claims

- **Not** benchmark integrity, replay↔execution equivalence, live SC2 in CI, ladder/public performance.
- **Not** proof that long operator campaigns are automatically informative under current reward posture.
- **Not** `out/` committed; local outputs remain operator-local.

---

## Annotated tag

- **`v0.0.50-m50`** on merge commit `a0430d3cd79b23d04c81cca1e11a404f50c4c35b` (per release discipline).

---

## Workflow-run analysis (merge-boundary)

Per `docs/company_secrets/prompts/workflowprompt.md` — **signal summary** for [`24424616487`](https://github.com/m-cahill/starlab/actions/runs/24424616487):

| Job / check | Required (merge gate) | Purpose | Pass |
| ----------- | ---------------------- | ------- | ---- |
| `quality` | Yes | Ruff, Mypy | Yes |
| `smoke` | Yes | Pytest smoke | Yes |
| `tests` | Yes | Full pytest + coverage | Yes |
| `security` | Yes | pip-audit, SBOM, Gitleaks | Yes |
| `fieldtest` | Yes | Field-test tier | Yes |
| `flagship` | Yes | Flagship proof pack | Yes |
| `governance` | Yes | Aggregate merge gate | Yes |

**Noise:** Node.js 20 deprecation notices on GitHub Actions — informational, **not** merge failures.
