# M37 — Delta audit (unified template v2)

* **Milestone:** M37 — Audit Closure VI — Coverage Margin Recovery and CI Evidence Hardening  
* **Mode:** DELTA AUDIT  
* **Range:** `08903cf…` (pre-M37 `main` tip) → `d2474bd365290a9c77f854b13d36a5ea1d8777cd` (merge commit)  
* **CI Status:** Green (authoritative PR-head `24271250678`; merge-boundary `24271267848`)  
* **Audit Verdict:** 🟢 — Milescope delivered; one superseded red run explained and fixed before merge; no silent gate weakening.

---

## Executive summary

**Improvements:** Coverage margin restored with honest gate (**78.0**); CI step summary line for coverage TOTAL; `make check`; identity basename fix for cross-platform configs; extensive targeted tests.

**Risks:** `runpy` warnings remain noisy; optional follow-up. Coverage still below **~85%** stretch — correctly **not** claimed.

**Next action:** Charter **M38** on its branch when ready; keep M38 stub-only until then.

---

## Delta map & blast radius

* **Changed:** `tests/`, `pyproject.toml`, `.github/workflows/ci.yml`, `Makefile`, `starlab/runs/identity.py`, ledger/milestone docs.  
* **Risk zones:** CI glue (low), test surface (medium volume, narrow intent), identity hashing (low — backward-compatible basename fix).

---

## Architecture & modularity

### Keep

* Consolidated coverage tests in `test_m37_coverage_targets.py` with clear scope comment.

### Fix now

* None blocking.

### Defer

* `runpy` warning cleanup — track only if CI starts treating warnings as errors.

---

## CI/CD & workflow integrity

* Required jobs: **quality**, **smoke**, **tests**, **security**, **fieldtest**, **governance** — all green on authoritative runs.  
* Actions remain SHA-pinned per existing workflow.  
* **Superseded** run **`24271229377`**: **tests** failed — **root cause:** POSIX `Path` did not treat `\` as separator — **fix:** `_posix_path_name_for_identity` in `starlab/runs/identity.py` (`a38d3a7…`).

---

## Tests & coverage

* Overall coverage on authoritative PR-head: **~80.34%** TOTAL (branch-aware).  
* Touched paths: heavy `tests/` additions; production change minimal (`identity.py`).

---

## Security & supply chain

* No dependency policy change in M37 merge; pip-audit/SBOM/Gitleaks jobs green.

---

## Top issues (max 7)

| ID | Category | Severity | Observation | Recommendation | Guardrail |
| --- | --- | --- | --- | --- | --- |
| CI-001 | CI | Low | Superseded red PR-head `24271229377` | Documented in `M37_run1.md` | Require green on **final** head before merge |

---

## PR-sized action plan

| ID | Task | Acceptance |
| --- | --- | --- |
| A1 | None blocking post-M37 | N/A |

---

## Deferred issues registry (append)

| ID | Issue | Discovered | Deferred To | Reason | Blocker? | Exit |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | runpy RuntimeWarning noise | M37 | M38+ optional | Non-failing | No | Only if CI policy changes |

---

## Score trend (placeholder)

| Milestone | Overall |
| --- | --- |
| M37 | Maintained — governance + CI evidence strengthened |

---

## Flake & regression log

| Item | Status |
| --- | --- |
| Superseded PR-head `24271229377` | Resolved before merge |

---

## Machine-readable appendix

```json
{
  "milestone": "M37",
  "mode": "delta",
  "commit": "d2474bd365290a9c77f854b13d36a5ea1d8777cd",
  "range": "08903cf...d2474bd",
  "verdict": "green",
  "quality_gates": {
    "ci": "pass",
    "tests": "pass",
    "coverage": "pass",
    "security": "pass",
    "workflows": "pass",
    "contracts": "unchanged"
  },
  "issues": ["CI-001"],
  "deferred_registry_updates": ["D1"],
  "score_trend_update": {}
}
```
