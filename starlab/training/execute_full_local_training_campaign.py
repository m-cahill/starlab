"""M50: governed full local campaign executor (M49 contract + M45 orchestration)."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import threading
import uuid
from pathlib import Path
from typing import Any, cast

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.local_live_play_validation_models import RuntimeMode
from starlab.training.campaign_execution_io import (
    HIDDEN_ROLLOUT_CAMPAIGN_RUN_FILENAME,
    STOP_REQUEST_FILENAME,
    build_hidden_rollout_campaign_run_report,
    seal_hidden_rollout_campaign_run_body,
    update_heartbeat,
    write_execution_manifest,
    write_hidden_rollout_campaign_run_artifacts,
    write_initial_heartbeat,
    write_resume_state,
)
from starlab.training.campaign_execution_io import (
    execution_dir as execution_dir_path,
)
from starlab.training.campaign_execution_lock import (
    release_lock,
    try_acquire_campaign_output_lock,
    try_acquire_execution_tree_lock,
)
from starlab.training.campaign_execution_preflight import run_campaign_execution_preflight
from starlab.training.full_local_training_campaign_models import NON_CLAIMS_V1
from starlab.training.industrial_hidden_rollout_models import (
    HIDDEN_ROLLOUT_CAMPAIGN_RUN_VERSION,
    resolve_visibility_posture_v1,
)
from starlab.training.self_play_rl_bootstrap_pipeline import run_self_play_rl_bootstrap


def _load_contract(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = "campaign contract must be a JSON object"
        raise ValueError(msg)
    return raw


def _execution_tree_state(edir: Path) -> str:
    """Return 'absent', 'complete', or 'partial'."""

    if not edir.is_dir():
        return "absent"
    if (edir / HIDDEN_ROLLOUT_CAMPAIGN_RUN_FILENAME).is_file():
        return "complete"
    if any(edir.iterdir()):
        return "partial"
    return "absent"


def _bootstrap_phases(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    phases = protocol.get("phases")
    if not isinstance(phases, list):
        return []
    out: list[dict[str, Any]] = []
    for p in phases:
        if not isinstance(p, dict):
            continue
        if str(p.get("kind")) == "bootstrap_episodes":
            out.append(p)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.training.execute_full_local_training_campaign",
        description=(
            "M50: execute governed bootstrap phases from an M49 campaign contract (M45 episodes)."
        ),
    )
    parser.add_argument(
        "--campaign-contract",
        required=True,
        type=Path,
        help="Path to full_local_training_campaign_contract.json",
    )
    parser.add_argument(
        "--campaign-root",
        type=Path,
        default=None,
        help="M49 campaign root (default: parent of --campaign-contract)",
    )
    parser.add_argument(
        "--execution-id",
        type=str,
        default=None,
        help="Execution id (default: random uuid)",
    )
    parser.add_argument(
        "--requested-visibility-mode",
        choices=("hidden", "minimized", "visible_fallback", "unsupported"),
        default="hidden",
        help="Requested visibility posture (resolved honestly in artifacts).",
    )
    parser.add_argument(
        "--allow-resume",
        action="store_true",
        help="Allow reusing execution_id when a partial tree exists (operator-authorized).",
    )
    parser.add_argument(
        "--skip-execution-preflight",
        action="store_true",
        help="Skip extended execution preflight (tests only).",
    )
    parser.add_argument(
        "--heartbeat-interval-s",
        type=float,
        default=30.0,
        help="Background heartbeat refresh interval while episodes run.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Base seed for bootstrap phases (per-phase offset applied).",
    )
    parser.add_argument(
        "--max-bootstrap-phases",
        type=int,
        default=None,
        metavar="N",
        help="Run only the first N bootstrap_episodes phases (default: all).",
    )
    args = parser.parse_args(argv)

    contract_path = args.campaign_contract.resolve()
    campaign_root = args.campaign_root.resolve() if args.campaign_root else contract_path.parent
    execution_id = args.execution_id or str(uuid.uuid4())
    edir = execution_dir_path(campaign_root, execution_id)

    try:
        contract = _load_contract(contract_path)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        sys.stderr.write(f"campaign contract: {e}\n")
        return 1

    state = _execution_tree_state(edir)
    if state == "complete":
        sys.stderr.write(
            f"execution tree already complete: {edir}\nchoose a new --execution-id.\n",
        )
        return 2
    if state == "partial" and not args.allow_resume:
        sys.stderr.write(
            f"partial execution tree exists: {edir}\n"
            f"quarantine/review, then re-run with --allow-resume if appropriate.\n",
        )
        return 3
    if state == "partial" and args.allow_resume:
        try:
            shutil.rmtree(edir)
        except OSError as e:
            sys.stderr.write(f"could not clear partial tree: {e}\n")
            return 1

    if not args.skip_execution_preflight:
        ok, receipt = run_campaign_execution_preflight(
            campaign_root=campaign_root,
            contract_path=contract_path,
            requested_visibility_mode=args.requested_visibility_mode,
        )
        receipt_path = campaign_root / "campaign_execution_preflight_receipt.json"
        receipt_path.write_text(canonical_json_dumps(receipt), encoding="utf-8")
        if not ok:
            sys.stderr.write(
                "execution preflight failed; see campaign_execution_preflight_receipt.json\n"
            )
            return 4

    capability = resolve_visibility_posture_v1(requested=args.requested_visibility_mode)

    ok_lock, out_lock_path, msg = try_acquire_campaign_output_lock(
        campaign_root=campaign_root,
        command="execute_full_local_training_campaign",
        execution_id=execution_id,
    )
    if not ok_lock:
        sys.stderr.write(f"campaign output lock: {msg}\n")
        return 5

    ok_ex, ex_lock_path, msg_ex = try_acquire_execution_tree_lock(
        command="execute_full_local_training_campaign",
        execution_dir=edir,
        execution_id=execution_id,
    )
    if not ok_ex:
        release_lock(out_lock_path)
        sys.stderr.write(f"execution tree lock: {msg_ex}\n")
        return 5

    campaign_sha256 = str(contract.get("campaign_sha256", ""))
    protocol = contract.get("campaign_protocol")
    if not isinstance(protocol, dict):
        release_lock(ex_lock_path)
        release_lock(out_lock_path)
        sys.stderr.write("campaign_protocol missing\n")
        return 1

    phases = _bootstrap_phases(protocol)
    if args.max_bootstrap_phases is not None:
        n = max(0, int(args.max_bootstrap_phases))
        phases = phases[:n]
    phase_names = [str(p.get("phase", "unknown")) for p in phases]

    m45 = contract.get("m45_planned_bootstrap")
    m43 = contract.get("m43_candidate")
    if not isinstance(m45, dict) or not isinstance(m43, dict):
        release_lock(ex_lock_path)
        release_lock(out_lock_path)
        sys.stderr.write("m45_planned_bootstrap / m43_candidate missing\n")
        return 1

    rt = cast(RuntimeMode, str(m45["runtime_mode"]))
    hr_dir = Path(str(m43["hierarchical_training_run_dir"]))
    match_cfg = Path(str(m45["match_config_path"]))
    m26 = contract.get("m26_replay_training_dataset")
    bundles = contract.get("m14_replay_bundle_directories")
    dataset_path = Path(str(m26["resolved_path"])) if isinstance(m26, dict) else None
    bundle_dirs: list[Path] | None = None
    if isinstance(bundles, list):
        bundle_dirs = [Path(str(b["resolved_path"])) for b in bundles if isinstance(b, dict)]

    write_execution_manifest(
        campaign_id=str(contract["campaign_id"]),
        campaign_sha256=campaign_sha256,
        capability=capability,
        execution_dir=edir,
        execution_id=execution_id,
        phases_planned=phase_names,
    )
    hb_path = write_initial_heartbeat(
        campaign_sha256=campaign_sha256,
        execution_dir=edir,
        execution_id=execution_id,
    )
    write_resume_state(
        campaign_sha256=campaign_sha256,
        detail="execution started",
        execution_dir=edir,
        execution_id=execution_id,
        phase=None,
        status="running",
    )

    stop_event = threading.Event()

    def _refresh_heartbeat() -> None:
        while not stop_event.wait(timeout=args.heartbeat_interval_s):
            try:
                update_heartbeat(
                    episode_index=None,
                    heartbeat_path=hb_path,
                    last_phase=None,
                )
            except OSError:
                break

    hb_thread = threading.Thread(target=_refresh_heartbeat, daemon=True)
    hb_thread.start()

    phase_results: list[dict[str, Any]] = []
    exit_code = 0

    try:
        for idx, phase in enumerate(phases):
            phase_name = str(phase.get("phase", f"phase_{idx}"))
            stop_p = edir / STOP_REQUEST_FILENAME
            if stop_p.is_file():
                write_resume_state(
                    campaign_sha256=campaign_sha256,
                    detail="stop request file present",
                    execution_dir=edir,
                    execution_id=execution_id,
                    phase=phase_name,
                    status="stopped_graceful",
                )
                exit_code = 6
                break

            budget = int(phase.get("episode_budget", 0))
            if budget < 1:
                continue

            phase_out = edir / "phases" / phase_name
            phase_out.mkdir(parents=True, exist_ok=True)
            phase_seed = int(args.seed) + idx * 10_000

            def _on_episode(ep: int, _row: dict[str, Any]) -> None:
                update_heartbeat(
                    episode_index=ep,
                    heartbeat_path=hb_path,
                    last_phase=phase_name,
                )

            try:
                run_self_play_rl_bootstrap(
                    bundle_dirs=bundle_dirs,
                    dataset_path=dataset_path,
                    emit_updated_bundle=False,
                    episodes=budget,
                    hierarchical_training_run_dir=hr_dir,
                    match_config_path=match_cfg,
                    mirror_self_play=False,
                    on_episode_complete=_on_episode,
                    output_dir=phase_out,
                    runtime_mode=rt,
                    seed=phase_seed,
                    weights_path=None,
                )
            except (OSError, ValueError, RuntimeError) as e:
                write_resume_state(
                    campaign_sha256=campaign_sha256,
                    detail=str(e),
                    execution_dir=edir,
                    execution_id=execution_id,
                    phase=phase_name,
                    status="failed",
                )
                exit_code = 7
                phase_results.append({"error": str(e), "phase": phase_name, "status": "failed"})
                break

            phase_results.append({"phase": phase_name, "episodes": budget, "status": "ok"})

        status = "complete" if exit_code == 0 else "failed_or_partial"
        non_claims = sorted(
            set(NON_CLAIMS_V1).union(
                {
                    "m50_campaign_execution_not_automatic_proof_of_learning",
                    "m50_hidden_rollout_not_true_headless_unless_resolved",
                }
            )
        )
        pre_body: dict[str, Any] = {
            "campaign_sha256": campaign_sha256,
            "execution_id": execution_id,
            "execution_status": status,
            "hidden_rollout_capability": dict(capability),
            "non_claims": non_claims,
            "phase_results": phase_results,
            "run_version": HIDDEN_ROLLOUT_CAMPAIGN_RUN_VERSION,
        }
        if exit_code == 0:
            pre_body["planned_weighted_refit_executed"] = False
            pre_body["planned_weighted_refit_note"] = (
                "M50 executor runs bootstrap_episodes phases only; "
                "refit/compare/M44 are out of scope."
            )
        run = seal_hidden_rollout_campaign_run_body(pre_body)
        report = build_hidden_rollout_campaign_run_report(run)
        write_hidden_rollout_campaign_run_artifacts(
            execution_dir=edir,
            report_body=report,
            run_body=run,
        )
        if exit_code == 0:
            write_resume_state(
                campaign_sha256=campaign_sha256,
                detail="execution finished",
                execution_dir=edir,
                execution_id=execution_id,
                phase=None,
                status="complete",
            )
    finally:
        stop_event.set()
        hb_thread.join(timeout=0.5)
        release_lock(ex_lock_path)
        release_lock(out_lock_path)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
