"""M51 governed post-bootstrap phase orchestration."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from starlab.training.execute_full_local_training_campaign import main as execute_campaign_main
from starlab.training.full_local_training_campaign_io import emit_full_local_training_campaign
from starlab.training.full_local_training_campaign_models import default_campaign_protocol_v1

from tests.test_m49_full_local_training_campaign import (
    M26_FIX,
    M28_FIX,
    MATCH_FAKE,
    REPO_ROOT,
    _build_m43_run_dir,
)


def _minimal_protocol_one_bootstrap_episode() -> dict[str, object]:
    base = default_campaign_protocol_v1()
    raw_phases = base.get("phases", [])
    phases = list(raw_phases) if isinstance(raw_phases, list) else []
    # Replace bootstrap tranches with a single one-episode phase for CI speed.
    slim: list[dict[str, object]] = []
    for p in phases:
        if not isinstance(p, dict):
            continue
        if p.get("kind") == "bootstrap_episodes":
            if p.get("phase") == "shakedown":
                slim.append(
                    {
                        "phase": "m51_ci_bootstrap",
                        "kind": "bootstrap_episodes",
                        "episode_budget": 1,
                        "description": "single fixture episode for M51 CI",
                    }
                )
            continue
        slim.append(p)
    out = dict(base)
    out["phases"] = slim
    return out


def test_m51_post_bootstrap_protocol_fixture_pipeline(tmp_path: Path) -> None:
    m43_dir, bundle = _build_m43_run_dir(tmp_path)
    shutil.copy(MATCH_FAKE, tmp_path / "match.json")
    bench = M28_FIX / "benchmark_contract_m28.json"
    out = tmp_path / "campaign"
    ds = M26_FIX / "replay_training_dataset.json"
    emit_full_local_training_campaign(
        benchmark_contract_path=bench,
        bundle_dirs=[bundle],
        campaign_id="m51_pb",
        campaign_protocol=_minimal_protocol_one_bootstrap_episode(),
        dataset_path=ds,
        hierarchical_training_run_dir=m43_dir,
        match_config_path=tmp_path / "match.json",
        output_dir=out,
        planned_weighted_refit=True,
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
            "m51_exec_pb",
            "--skip-execution-preflight",
            "--post-bootstrap-protocol-phases",
            "--requested-visibility-mode",
            "minimized",
        ],
    )
    assert code == 0
    ed = out / "campaign_runs" / "m51_exec_pb"
    run_path = ed / "hidden_rollout_campaign_run.json"
    assert run_path.is_file()
    sealed = json.loads(run_path.read_text(encoding="utf-8"))
    assert sealed.get("post_bootstrap_protocol_phases_enabled") is True
    receipts = sealed.get("phase_receipts")
    assert isinstance(receipts, list)
    assert len(receipts) >= 5
    names = {r.get("phase_name") for r in receipts if isinstance(r, dict)}
    assert "optional_weighted_refit" in names
    assert "post_refit_m42_comparison" in names
    assert "watchable_m44_validation" in names

    def _is_m42_phase(r: object) -> bool:
        return isinstance(r, dict) and r.get("phase_name") == "post_refit_m42_comparison"

    m42_rec = next(r for r in receipts if _is_m42_phase(r))
    assert m42_rec.get("executed") is False
    assert "candidate_not_m41_comparison_compatible" in (m42_rec.get("reason_codes") or [])

    refit_dir = ed / "phases" / "optional_weighted_refit"
    assert (refit_dir / "phase_receipt.json").is_file()
    joblib_p = refit_dir / "updated_policy" / "rl_bootstrap_candidate_bundle.joblib"
    assert joblib_p.is_file()

    w44 = ed / "phases" / "watchable_m44_validation"
    assert (w44 / "phase_receipt.json").is_file()
    assert (w44 / "local_live_play_validation_run.json").is_file()


def test_m51_module_help_lists_post_bootstrap_flag() -> None:
    import subprocess
    import sys

    r = subprocess.run(
        [sys.executable, "-m", "starlab.training.execute_full_local_training_campaign", "--help"],
        check=False,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert r.returncode == 0
    out = (r.stdout + r.stderr).lower()
    assert "post-bootstrap" in out
