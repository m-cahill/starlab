# Field-test session template

**Purpose:** Record a single engineer or reviewer session validating **fixture-only** STARLAB behavior (no live SC2 required for the path below).  
**Authority:** Subordinate to `docs/starlab.md` and `docs/diligence/field_test_checklist.md`.

Copy this section into a new file or ticket when documenting a session.

---

## Session metadata

| Field | Value |
| ----- | ----- |
| Date (UTC) | |
| Operator / reviewer | |
| Machine OS / shell | |
| Python version (`python --version`) | |
| Repository remote URL | |
| Checkout SHA (full or short) | |
| Branch | |

## Commands executed

List exact commands in order (paste from shell history):

```text

```

## Artifacts and outputs

| Output | Path or CI artifact name | Notes |
| ------ | ------------------------- | ----- |
| Smoke tests | `pytest -q -m smoke` | Exit code |
| Full tests (optional local) | `pytest -q` | Exit code |
| Field-test directory | `out/fieldtest/` or CI **`fieldtest-output`** | Must contain `replay_explorer_surface.json` and `replay_explorer_surface_report.json` |
| Coverage (optional local) | `coverage.xml` | If generated |

## Pass / fail observations

- [ ] `make smoke` or equivalent passed.  
- [ ] `make fieldtest` or equivalent passed; both JSON outputs present and non-empty.  
- [ ] No unexpected dependency or import errors.  

**Failures (if any):**

```text

```

## Bounded non-claims (sign-off)

This session **does not** demonstrate:

- Benchmark integrity or leaderboard-valid results.  
- Live SC2 client correctness or ladder performance.  
- M35 flagship proof-pack completion.  
- Cross-host bitwise reproducibility of floating-heavy local runs.  

## Follow-ups

- Deferred items: see `docs/audit/DeferredIssuesRegistry.md`.  
- CI tier reference: `docs/runtime/ci_tiering_field_test_readiness_v1.md`.
