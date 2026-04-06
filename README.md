# STARLAB

**Strategic Testing, Analysis, Replay, and Learning Lab**

STARLAB is a governed, replay-native RTS research program that begins with **StarCraft II** and aims to build a reproducible, benchmarkable, evidence-first substrate for hierarchical, perception-grounded, multi-agent research.

---

## What STARLAB is

STARLAB is being built as a **lab-first research substrate**, not a one-off bot project.

Its purpose is to make serious RTS research more:

- replay-native
- benchmarkable
- evidence-driven
- auditable
- transferable

The near-term goal is not “train the strongest possible agent.”  
The near-term goal is to establish a credible lab surface that can support:

- deterministic artifacts
- replay-linked evidence
- benchmark scorecards
- multiple agent styles over time

---

## What STARLAB is not

STARLAB is not:

- a ladder-first bot effort
- a monolithic super-agent project
- a consumer game product
- a modding platform
- a generic benchmark wrapper without governance

The lab is primary.  
Any agent built inside it is secondary to the substrate.

---

## Why StarCraft II

StarCraft II is the initial proving ground because it naturally combines:

- partial observability
- long-horizon planning
- macro and micro control
- adversarial multi-agent dynamics
- real-time execution pressure
- rich replay structure

That makes it an unusually strong environment for a research substrate whose focus is not just performance, but reproducibility and evaluation quality.

---

## Project posture

STARLAB follows a few core principles:

- systems problem first, agent problem second
- benchmark integrity before leaderboard optics
- evidence before hype
- small reversible milestones over sprawling implementation
- honest non-claims over vague ambition

The project is also being built to be **clean enough to buy**: legible, ownable, defensible, maintainable, and low-friction to diligence if it ever becomes a strategic asset.

---

## Program shape

The current high-level program shape is:

1. **Foundation & Environment Lock**  
2. **Replay & Data Plane**  
3. **State & Representation**  
4. **Evaluation & Baselines**  
5. **Learning Agents & Showcase**  
6. **Platform Expansion** *(only if earned)*

STARLAB is intentionally **SC2-first**. Multi-environment expansion is a later possibility, not a starting assumption.

---

## Strategic value framing

STARLAB is being approached as a strategic research substrate with a staged value ladder:

- **Tier 1:** Prototype / Early Lab
- **Tier 2:** Full Lab Substrate
- **Tier 3:** Multi-Environment-Capable Substrate
- **Tier 4:** Community Benchmark Standard
- **Tier 5:** Strategic Internal Asset
- **Tier 6:** Field-Defining Platform

These are planning lenses, not promises. The realistic early path is:

**career signal → strategic internal leverage → platform leverage**.

---

## Current status

**Status:** Post-M00 — next: M01 (environment lock)

STARLAB has completed governance bootstrap (M00): canonical ledger, governance docs, minimal CI, and deployment **posture** (Netlify / Render targets; no live deploys).

Up next:

- environment lock and runtime baseline (M01)

---

## Source of truth

The primary living project record is:

- **`docs/starlab.md`**

That file should be treated as the canonical public ledger for:

- current milestone status
- phase structure
- risks and open decisions
- milestone closeouts
- public evidence posture

Other supporting docs should stay aligned to it.

---

## Documentation map

| Document | Role |
| -------- | ---- |
| `README.md` | Public front door |
| `docs/starlab.md` | Canonical project ledger / living source of truth |
| `docs/starlab-vision.md` | Moonshot / long-range thesis |
| `docs/bicetb.md` | Acquisition, diligence, licensing, and boundary discipline |
| `docs/public_private_boundary.md` | Public vs protected surfaces |
| `docs/replay_data_provenance.md` | Replay/data interim policy |
| `docs/rights_register.md` | Rights and provenance inventory |
| `docs/branding_and_naming.md` | Naming and brand diligence |
| `docs/deployment/deployment_posture.md` | Future Netlify / Render posture (not active deployment) |
| `CONTRIBUTING.md` | Contribution expectations |
| `SECURITY.md` | Security reporting |
| `docs/company_secrets/milestones/` | Milestone plans, toolcalls, audits, summaries (tracked; other `company_secrets` subfolders are gitignored) |

---

## Repository principles

This repository should aim to be:

- evidence-first
- milestone-driven
- acquisition-aware
- legible to future maintainers
- explicit about what is proved and what is not

---

## Local environment note

Where relevant, local testing is expected to use an **RTX 5090 Blackwell**.

---

## Contributing

See `CONTRIBUTING.md` for **Python 3.11**, virtualenv, and commands that match **GitHub Actions CI** (Ruff, Mypy, Pytest, pip-audit).

Contribution policy, licensing posture, and ownership/provenance rules should be made explicit before broad external contribution is encouraged.

Until then, the default expectation is:

- clear authorship
- traceable changes
- no ambiguous-origin core contributions
- milestone-scoped work
- documentation updates with meaningful project changes

---

## License

**Copyright 2026 Michael Cahill**

⚠️ This repository is source-available for research transparency only.
It is not open source.
Use is limited to evaluation and verification as described in the LICENSE.

---

## Current objective

The current objective is simple:

> Build a credible RTS research lab before trying to build a headline-grabbing agent.
