# Deployment posture (preparatory only)

## Purpose

Record **future** hosting intent for STARLAB without implying live deployments, production readiness, or rights-cleared public distribution.

> **Deployment readiness is not deployment.**  
> M00 establishes conventions and governance only. Netlify and Render are **targets**, not active environments.

## Future target split

| Surface | Future host | Notes |
|---------|-------------|--------|
| Frontend web app | **Netlify** | Site root should map to `frontend/` when code exists |
| Static docs / evidence (optional) | **Netlify** | May share a site or a separate docs site; TBD |
| Backend APIs / services | **Render** | Blueprint (`render.yaml`) as source of truth when services exist |

## Monorepo convention (adopted in M00)

- `frontend/` — future UI
- `backend/` — future services
- `ops/` — IaC snippets, non-secret config templates
- `docs/` — repository documentation (may be mirrored to a static site later)

## Netlify convention (when frontend exists)

- Keep **site-specific** config **with** the site (e.g. under `frontend/`).
- Use deploy contexts: at least `production`, `deploy-preview`, and any future `staging` / branch contexts per Netlify docs.
- **Environment variables** are managed in the provider; never commit secrets.
- For monorepos: set base directory / publish directory to match `frontend/` when applicable.

## Render convention (when backend exists)

- **Render Blueprint** (`render.yaml`) becomes the single source of truth for deployable backend resources.
- Validate Blueprint **in CI** once a real `render.yaml` exists.
- Secrets live in Render environment groups or provider UI, not the repo.

## Secret policy

Reserved prefixes:

- `STARLAB_*` — application configuration
- `NETLIFY_*` — only when supplied by Netlify
- `RENDER_*` — only when supplied by Render

Do not commit `.env` files with secrets. Example files may use `.env.example` without secrets.

## Non-operative examples

Example files under `frontend/` and `ops/render/` (if present) are **templates only**; they do not imply active sites or services.
