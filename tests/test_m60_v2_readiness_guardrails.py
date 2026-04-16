"""M60 — architectural guardrails for v2 readiness audit hardening."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

from starlab.training.execute_full_local_training_campaign import main as execute_campaign_main
from starlab.training.full_local_training_campaign_io import emit_full_local_training_campaign

from tests.test_m49_full_local_training_campaign import (
    M28_FIX,
    MATCH_FAKE,
    REPO_ROOT,
    _build_m43_run_dir,
)


def test_m60_evaluation_imports_state_only_via_m14_bundle_loader() -> None:
    """Preserve M35 loader boundary: evaluation must not spread direct state imports."""
    eval_dir = REPO_ROOT / "starlab" / "evaluation"
    offenders: list[str] = []
    for path in sorted(eval_dir.rglob("*.py")):
        if path.name == "m14_bundle_loader.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("starlab.state"):
                        offenders.append(f"{path.relative_to(REPO_ROOT)}: import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("starlab.state"):
                    offenders.append(f"{path.relative_to(REPO_ROOT)}: from {node.module}")
    assert offenders == [], f"unexpected starlab.state imports: {offenders}"


def test_m60_campaign_executor_private_module_importable() -> None:
    spec = importlib.util.find_spec("starlab.training._full_local_training_campaign_execution")
    assert spec is not None
    mod = importlib.import_module("starlab.training._full_local_training_campaign_execution")
    assert callable(getattr(mod, "execute_m50_bootstrap_only"))
    assert callable(getattr(mod, "execute_m51_protocol_phases"))


def test_m60_execute_module_entrypoint_unchanged() -> None:
    assert callable(execute_campaign_main)


def test_m60_m50_fixture_smoke_regression(tmp_path: Path) -> None:
    """End-to-end: M50 bootstrap-only path still produces sealed campaign run JSON."""
    import shutil

    m43_dir, _bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        campaign_id="m60_guard",
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=False,
        runtime_mode="fixture_stub_ci",
        training_program_contract_path=None,
    )
    code = execute_campaign_main(
        [
            "--campaign-contract",
            str(out / "full_local_training_campaign_contract.json"),
            "--campaign-root",
            str(out),
            "--execution-id",
            "m60_e2e_smoke",
            "--skip-execution-preflight",
            "--max-bootstrap-phases",
            "1",
            "--requested-visibility-mode",
            "minimized",
        ],
    )
    assert code == 0
    run_json = out / "campaign_runs" / "m60_e2e_smoke" / "hidden_rollout_campaign_run.json"
    assert run_json.is_file()
    text = run_json.read_text(encoding="utf-8")
    assert '"execution_status"' in text
    assert '"phase_results"' in text
