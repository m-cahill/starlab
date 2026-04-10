# Field-test checklist

Use this for diligence or on-site validation of a **fixture-only** STARLAB checkout.

## Environment

- [ ] Python 3.11 available (`python --version`).
- [ ] Repository cloned from canonical remote.
- [ ] `pip install -e ".[dev]"` succeeds.

## Quality

- [ ] `ruff check starlab tests` passes.
- [ ] `ruff format --check starlab tests` passes.
- [ ] `mypy starlab tests` passes.
- [ ] `pytest -q` passes (full suite).
- [ ] `pytest -q -m smoke` passes (fast lane).

## Representative product path (fixtures)

- [ ] Run M31 explorer emit on bundled fixtures (see `docs/getting_started_clone_to_run.md`).
- [ ] Confirm output JSON files exist and are non-empty.
- [ ] Confirm no raw `.SC2Replay` bytes are required for this path.
- [ ] (Optional diligence) Record session using `docs/diligence/field_test_session_template.md`.
- [ ] (CI) Confirm **`fieldtest-output`** artifact contains `replay_explorer_surface.json` and `replay_explorer_surface_report.json` when validating a green **`CI`** workflow — see `docs/runtime/ci_tiering_field_test_readiness_v1.md`.

## Governance

- [ ] `docs/starlab.md` milestone table matches expected program arc (see ledger §7).
- [ ] `docs/audit/DeferredIssuesRegistry.md` reviewed for open corrective items.

## Explicit non-claims

Field-testing this checklist does **not** prove benchmark integrity, live SC2 correctness, or flagship proof-pack completion.
