# M38 — Delta audit (unified template v2)

* **Milestone:** M38 — Audit Closure VII — Public Face Refresh, Governance Rationalization, and Code-Health Tightening  
* **Mode:** DELTA AUDIT  
* **Range:** `caeaeb35f020268a8dffc3f6cfefb6876cca0196` (pre-M38 `main` tip) → `bf6bf4ad29466c5a44d32ec581dae9ee8a20bf96` (merge commit)  
* **CI Status:** Green (authoritative PR-head `24272425346`; merge-boundary `main` `24291882960`)  
* **Audit Verdict:** 🟢 — Milestone scope delivered; documentation + test-hygiene only; no gate weakening.

---

## Executive summary

**Improvements:** README and ledger quick-scan aligned with **M37**-closed / **M39**-next reality; governance test dedup + M07/M37 row coverage; centralized `runpy` warning suppression in tests with regression test.

**Risks:** Low — no production contract or dependency changes. Residual **s2protocol** `DeprecationWarning` in parser tests remains pre-existing.

**Next action:** Charter **M39** on its branch when ready; **M39** stub only in repo until then.

---

## Delta map & blast radius

* **Changed:** `README.md`, `docs/starlab.md`, `tests/runpy_helpers.py`, governance tests, M38 milestone docs under `docs/company_secrets/milestones/M38/`.  
* **Risk zones:** None material — docs + tests only.

---

## Architecture & modularity

### Keep

* `run_module_as_main` isolated under `tests/runpy_helpers.py` (test-only boundary).

### Fix now

* None.

### Defer

* Optional parser upstream deprecation — track outside M38.

---

## CI/CD & workflow integrity

* Required jobs: **quality**, **smoke**, **tests**, **security**, **fieldtest**, **governance** — all green on `24272425346` and `24291882960`.  
* **Superseded** runs: **none** for M38 final head.

---

## Tests & coverage

* **682** tests on authoritative PR-head; **`fail_under`** **78.0** unchanged.  
* New: `tests/test_runpy_helpers.py`; governance param expansion (+2 row checks).

---

## Security & supply chain

* No dependency changes in M38 merge.

---

## Top issues (max 7)

| ID | Category | Severity | Observation | Recommendation | Guardrail |
| --- | --- | --- | --- | --- | --- |
| — | — | — | No blocking issues | — | — |

---

## PR-sized action plan

| ID | Task | Acceptance |
| --- | --- | --- |
| A1 | None blocking post-M38 | N/A |

---

## Deferred issues registry (append)

| ID | Issue | Discovered | Deferred To | Reason | Blocker? | Exit |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | s2protocol `imp` DeprecationWarning | Pre-M38 | TBD | Upstream | No | Parser bump or filter policy |

---

## Score trend (placeholder)

| Milestone | Overall |
| --- | --- |
| M38 | Maintained — docs + test hygiene |

---

## Flake & regression log

| Item | Status |
| --- | --- |
| M38 CI | Green PR-head + merge-boundary |

---

## Machine-readable appendix

```json
{
  "milestone": "M38",
  "mode": "delta",
  "commit": "bf6bf4ad29466c5a44d32ec581dae9ee8a20bf96",
  "range": "caeaeb35...bf6bf4a",
  "verdict": "green",
  "quality_gates": {
    "ci": "pass",
    "tests": "pass",
    "coverage": "pass",
    "security": "pass",
    "workflows": "pass",
    "contracts": "unchanged"
  },
  "issues": [],
  "deferred_registry_updates": ["D1"],
  "score_trend_update": {}
}
```
