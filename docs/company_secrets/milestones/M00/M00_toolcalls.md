# M00 toolcalls log

Workstream-level log (not per-file). Timestamps UTC where noted.

---

## Workstream A — Ledger hardening (`docs/starlab.md`)

- **Purpose:** Untrusted boundary rule, change control, proved/not-proved, assumed/owned, deployment posture, “deployment readiness is not deployment”; resolve OD-002, OD-003 (conditional), OD-004, OD-006; milestone table + closeout ledger + changelog.
- **Files:** `docs/starlab.md`
- **Status:** complete

---

## Workstream B — Governance documents

- **Purpose:** Public/private boundary, replay provenance, rights register, branding, CONTRIBUTING, SECURITY.
- **Files:** `docs/public_private_boundary.md`, `docs/replay_data_provenance.md`, `docs/rights_register.md`, `docs/branding_and_naming.md`, `CONTRIBUTING.md`, `SECURITY.md`
- **Status:** complete

---

## Workstream C — Deployment posture + repo placeholders

- **Purpose:** `docs/deployment/deployment_posture.md`, `docs/deployment/env_matrix.md`, `frontend/README.md`, `backend/README.md`, `ops/README.md`, `frontend/netlify.toml.example`, `ops/render/render.yaml.example`
- **Status:** complete

---

## Workstream D — CI and tooling

- **Purpose:** `pyproject.toml`, `starlab/`, `tests/`, `.github/workflows/ci.yml`, `.editorconfig`, `.pre-commit-config.yaml`, `.gitignore` (narrowed `company_secrets` ignore list).
- **Commands (local venv):** `python -m pip install --upgrade pip setuptools`, `pip install -e ".[dev]"`, `ruff check`, `ruff format --check`, `mypy starlab tests`, `pytest`, `python -m pip_audit`, `cyclonedx-py environment -o sbom.json`
- **Status:** complete

---

## Workstream E — Milestone machinery

- **Purpose:** `M00_plan.md`, this file, `M00_summary.md` / `M00_audit.md` stubs, `M01_plan.md` / `M01_toolcalls.md` stubs.
- **Status:** complete
