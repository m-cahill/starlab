# M00 — Governance Bootstrap, Ledger Hardening, and Deployment Posture Seeding

## Objective

Make STARLAB safe to start: clear source of truth, governance and milestone machinery, explicit rights/provenance posture, minimal truthful CI, and documented future deployment intent (Netlify / Render) without live deploys.

## Constraints

Docs-first and governance-first. No SC2 runtime code, no environment-stability claims, no replay/benchmark/agent capability claims, no secrets in repo, no public hosted deployments in M00.

## Workstreams

- **A** — Harden `docs/starlab.md` (untrusted boundary, change control, proved/not proved, assumed/owned, deployment posture, resolve open decisions).
- **B** — Governance docs: public/private boundary, replay provenance, rights register, branding, CONTRIBUTING, SECURITY.
- **C** — Deployment docs (`docs/deployment/`), `frontend/`, `backend/`, `ops/` placeholders, non-operative examples.
- **D** — Python 3.11 tooling: Ruff, Mypy, Pytest, pip-audit, Gitleaks, CycloneDX SBOM, GitHub Actions CI.
- **E** — Milestone artifacts under `docs/company_secrets/milestones/M00/`; seed M01 stubs at closeout.

## Success

Ledger updated; OD-002/003/004/006 resolved or conditionally resolved; rights register and boundary docs exist; CI green on governance smoke tests; no runtime overclaim.
