"""Helpers for running a module as ``__main__`` in tests (see ``runpy.run_module``).

``runpy`` can emit a benign ``RuntimeWarning`` when a submodule is already
loaded in the same process (common when tests import ``starlab`` packages first).
Suppressing that warning locally keeps CI warning counts honest without changing
product entry points.
"""

from __future__ import annotations

import runpy
import warnings
from typing import Any


def run_module_as_main(module_name: str) -> Any:
    """Run *module_name* as ``__main__`` (same contract as ``runpy.run_module``)."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning, module="runpy")
        return runpy.run_module(module_name, run_name="__main__")
