# M43 — Delta audit (unified template v2)

* **Milestone:** M43 — Hierarchical Training Pipeline v1  
* **Mode:** DELTA AUDIT  
* **Range:** `main` pre-M43 merge tip → `8850e378a584c9821eeab3e8c72bc499d590b308` (merge commit of PR #54)  
* **CI Status:** Green (authoritative PR-head [`24300864558`](https://github.com/m-cahill/starlab/actions/runs/24300864558); merge-boundary `main` [`24301419897`](https://github.com/m-cahill/starlab/actions/runs/24301419897))  
* **Audit Verdict:** 🟢 — First **governed hierarchical training run** pipeline delivered with explicit **non-claims**; **not** benchmark integrity, **not** replay↔execution equivalence, **not** live SC2 in CI, **not** M42 comparison integration, **not** M44 live-play or M45 RL.

---

## Executive summary

**Improvements:** Deterministic **`hierarchical_training_run.json`** / **`hierarchical_training_run_report.json`** under `out/hierarchical_training_runs/`; sklearn **LogisticRegression** manager + per-delegate workers; **M40** contract binding; **M29** trace schema linkage; **M30** fixed four-delegate policy; **delegate_coverage** reporting; optional combined `joblib` sidecar; fixture-only CI tests. **M41**-aligned feature encoding (one-hot context signature).

**Risks:** Low — no live SC2; weights **not** in repo. **Superseded** PR-head runs on earlier heads — **not** merge authority for final tip `ffc4284…` (see `M43_run1.md`).

**Residual:** GitHub Actions **Node 20** deprecation annotations (informational).

---

## Superseded PR-head runs (clarity)

| Run ID | Role |
| ------ | ---- |
| [`24300864558`](https://github.com/m-cahill/starlab/actions/runs/24300864558) | **Authoritative** for final PR head `ffc4284…` |
| [`24300836922`](https://github.com/m-cahill/starlab/actions/runs/24300836922), [`24300809086`](https://github.com/m-cahill/starlab/actions/runs/24300809086), [`24300781928`](https://github.com/m-cahill/starlab/actions/runs/24300781928), [`24300750817`](https://github.com/m-cahill/starlab/actions/runs/24300750817) | **Superseded** — intermediate greens only |

---

## Delta map & blast radius

* **Changed:** `starlab/hierarchy/*` (training pipeline), `docs/runtime/hierarchical_training_pipeline_v1.md`, ledger/README/architecture, `.gitignore`, governance test, `tests/test_m43_*`.  
* **Risk zones:** `starlab.hierarchy` training path only; no replay parser or SC2 client changes in listed M43 modules.

---

## Architecture & modularity

### Keep

* Reuse of `collect_imitation_example_rows` + `parse_context_signature_to_feature_dict` — consistent with M41.
* Single combined `joblib` bundle — parallel to M41 sidecar pattern.

### Fix now

* None blocking post-merge.

### Defer

* M44 live-play harness; M45 RL; optional Actions Node 24 migration.

---

## CI/CD & workflow integrity

* Required jobs on **24300864558** and **24301419897**: **quality**, **smoke**, **tests**, **security**, **fieldtest**, **flagship**, **governance** — all success.

---

## Tests & coverage

* Full suite + M43 fixture tests; **`fail_under` 78.0** unchanged.

---

## Security & supply chain

* No new dependencies added by M43 beyond existing sklearn usage; pip-audit / SBOM / Gitleaks green on merge-boundary `main`.

---

## Top issues (max 7)

| ID | Category | Severity | Observation | Recommendation | Guardrail |
| --- | --- | --- | --- | --- | --- |
| — | — | — | No blocking issues | — | — |

---

## PR-sized action plan

| ID | Task | Acceptance |
| --- | --- | --- |
| A1 | None blocking post-M43 | N/A |

---

## Machine-readable appendix

```json
{
  "milestone": "M43",
  "mode": "delta",
  "merge_commit": "8850e378a584c9821eeab3e8c72bc499d590b308",
  "pr_head": "ffc428454939702fbe9c100ace9e109ee0c51605",
  "authoritative_pr_head_ci": "24300864558",
  "merge_boundary_main_ci": "24301419897",
  "superseded_pr_head_runs": [
    "24300836922",
    "24300809086",
    "24300781928",
    "24300750817"
  ],
  "verdict": "green",
  "milestone_kind": "first_governed_hierarchical_training_pipeline_not_benchmark_or_live_play"
}
```
