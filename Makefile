# STARLAB developer / operator surface (POSIX make; Git Bash on Windows OK).
PY ?= python
PIP ?= $(PY) -m pip

.PHONY: install-dev smoke test coverage lint typecheck audit fieldtest

install-dev:
	$(PIP) install --upgrade pip setuptools
	$(PIP) install -e ".[dev]"

lint:
	ruff check starlab tests

typecheck:
	mypy starlab tests

test:
	pytest -q

coverage:
	pytest -q --cov=starlab --cov-report=term-missing:skip-covered --cov-report=xml

smoke:
	pytest -q -m smoke

audit:
	$(PY) -m pip_audit

# Fast fixture-backed subset (~25–30 tests; no live SC2).
# Field test: M31 explorer CLI on checked-in fixtures (deterministic).
fieldtest: install-dev
	$(PY) -m starlab.explorer.emit_replay_explorer_surface \
		--bundle-dir tests/fixtures/m31/bundle \
		--agent-path tests/fixtures/m30/replay_hierarchical_imitation_agent.json \
		--output-dir out/fieldtest
