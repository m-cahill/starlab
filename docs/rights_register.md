# Rights register

Living inventory of major surfaces: ownership, terms, redistribution, and risk. Update when assets or dependencies materially change.

| Asset / surface | Type | Source | Owner | License / terms | Redistribution allowed? | Commercial use allowed? | Public / private | Notes / risk | Status |
|-----------------|------|--------|-------|-----------------|-------------------------|-------------------------|------------------|--------------|--------|
| Repository code | code | First-party | Michael Cahill | `LICENSE` (source-available, eval/verification) | No (per `LICENSE`) | No (per `LICENSE`) | Public repo | Evaluation-only clone/run | Initial |
| Repository docs | docs | First-party | Michael Cahill | Same as code unless noted | Same as code | Same as code | Public | — | Initial |
| SC2 client / game dependency surface | dependency | Blizzard | Blizzard | EULA | N/A (don’t redistribute client) | Per EULA | Public discussion only | Untrusted boundary; see `docs/starlab.md` | Open |
| Replay assets | replay | Various / TBD | Various | Varies; often restricted | Unknown unless explicit | Unknown unless explicit | Default private / quarantine | High diligence risk if unclear | Open |
| Map assets | map | Various / TBD | Various | Map-specific + EULA | Often no | Often no | Default private | — | Open |
| Python dev dependencies | dependency | PyPI | Upstream authors | Per-package (see lock/pip list in CI) | Per license | Per license | Declared in SBOM/CI | Track in CI (pip-audit) | Initial |
| Future generated artifacts | artifact | STARLAB tooling | Michael Cahill | TBD at generation | TBD | TBD | TBD | Define in milestone | Deferred |
| Future model weights | model | TBD | TBD | TBD | TBD | TBD | Private default | — | Deferred |

**OD-006 resolution:** This file is the canonical rights register format; `docs/starlab.md` may summarize but defers detail here.
