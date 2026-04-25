# Contributing

## Local Python setup

Use Python **3.11** and a **virtual environment** so tooling matches CI:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -e ".[dev]"
```

Optional — Blizzard **`s2protocol`** replay decode for local runs of `python -m starlab.replays.parse_replay` with a real `.SC2Replay` (CI stays fixture-driven without this extra):

```bash
pip install -e ".[dev,replay-parser]"
```

Then run `ruff check starlab tests`, `mypy starlab tests`, `pytest`, and `python -m pip_audit` as needed.

STARLAB is milestone-driven. Until broader contribution is opened:

- **Traceability:** commits should be attributable; no anonymous core changes.
- **No ambiguous-origin code:** do not paste snippets from forums or Stack Overflow without clear license handling (see `docs/rights_register.md`).
- **Milestone scope:** work aligns with an active milestone plan maintained **locally** under `docs/company_secrets/milestones/` (private tree; gitignored; not present in a default clone — see `docs/public_private_boundary.md`).
- **Documentation:** meaningful project changes update `docs/starlab.md` when they affect governance, contracts, or claims.

Licensing is **source-available** (`LICENSE`); evaluation and verification use only unless terms change. Do not contribute with the expectation of permissive OSS redistribution.

For security-sensitive reports, see `SECURITY.md`.
