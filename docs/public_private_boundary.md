# Public / private boundary

## Purpose

STARLAB separates **public surfaces** (credibility, standards, evidence philosophy) from **protected surfaces** (implementation leverage and acquisition optionality). This document records the current split and how it may change.

## Why separation matters

Unclear boundaries create diligence risk: unclear IP ownership, accidental over-disclosure, or ambiguous contributor rights. The project follows the “clean enough to buy” posture in `docs/bicetb.md`.

## Public surfaces (current)

Committed in this repository and intended for review:

- `README.md` — project front door
- `LICENSE` — source-available terms
- `docs/starlab.md` — canonical public ledger
- `docs/starlab-vision.md` — moonshot thesis
- `docs/bicetb.md` — acquisition/diligence discipline
- Governance docs added in M00: `docs/public_private_boundary.md`, `docs/replay_data_provenance.md`, `docs/rights_register.md`, `docs/branding_and_naming.md`, `docs/deployment/*`
- Future: public artifact schemas, benchmark philosophy, selected evidence reports (when published under explicit governance)

## Protected surfaces (current)

Treated as sensitive or reserved until explicitly promoted:

- **`docs/company_secrets/**` — not committed** (entire tree is **gitignored**; milestone plans, prompts, manuals, and audits are **local / operator** copies only — a default `git clone` does **not** include them)
- Future: core runtime, SC2 adapters, stabilization internals, ingestion pipelines, private corpora, labels, weights, proprietary evaluation internals

## Current repo mapping

| Area | Posture |
|------|---------|
| Docs under `docs/` (non-secrets) | Public |
| `docs/company_secrets/**` | **Private** — must remain **untracked**; keep milestone notes, prompts, and operator evidence **locally** (or in separate private storage) — **not** public git contents |
| `frontend/`, `backend/`, `ops/` | Placeholder roots; future code subject to same boundary rules |

## Promoting an internal surface to public

Requires:

1. Rights/provenance check (`docs/rights_register.md`)
2. Update to `docs/public_private_boundary.md` and `docs/starlab.md`
3. Milestone governance if the change affects contracts, benchmarks, or deployment posture

## Demos and public evidence

No public demo site or hosted deployment is implied until:

- deployment posture and rights are explicit, and
- `docs/starlab.md` records the milestone that authorizes the surface.

## Who decides boundary changes

The project owner (Michael Cahill) approves boundary changes; significant changes are recorded in `docs/starlab.md` and, where applicable, milestone closeouts.
