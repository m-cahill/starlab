"""Regression tests for ``tests.runpy_helpers`` (runpy warning noise in CI)."""

from __future__ import annotations

import sys
import warnings

import pytest

from tests.runpy_helpers import run_module_as_main


def test_run_module_as_main_does_not_emit_sys_modules_runtime_warning(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``runpy.run_module`` warns when submodules are pre-imported; helper filters it."""
    monkeypatch.setattr(sys, "argv", ["emit_learned_agent_evaluation", "--help"])
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        with pytest.raises(SystemExit) as exc:
            run_module_as_main("starlab.evaluation.emit_learned_agent_evaluation")
        assert exc.value.code == 0
    assert not any("sys.modules" in str(w.message) for w in rec)
