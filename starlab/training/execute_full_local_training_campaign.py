"""M50/M51: governed full local campaign executor (M49 contract + M45 orchestration)."""

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
from starlab.sc2.local_live_play_validation_harness import run_local_live_play_validation
from starlab.sc2.local_live_play_validation_models import RuntimeMode
from starlab.sc2.match_config import match_config_from_mapping, match_config_to_mapping
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
from starlab.training.campaign_phase_receipt import (
    build_phase_receipt,
    write_phase_receipt,
)
from starlab.training.full_local_training_campaign_models import NON_CLAIMS_V1
from starlab.training.industrial_hidden_rollout_models import (
    HIDDEN_ROLLOUT_CAMPAIGN_RUN_VERSION,
    resolve_visibility_posture_v1,
)
from starlab.training.self_play_rl_bootstrap_models import (
    UPDATED_BUNDLE_BASENAME,
    UPDATED_POLICY_SUBDIR,
)
from starlab.training.self_play_rl_bootstrap_pipeline import (
    aggregate_bootstrap_pseudo_label_rows_from_completed_phase_dirs,
    run_self_play_rl_bootstrap,
    run_standalone_weighted_refit_from_aggregated_rows,
)


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


def _protocol_phases_in_order(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    phases = protocol.get("phases")
    if not isinstance(phases, list):
        return []
    return [p for p in phases if isinstance(p, dict)]


def _stop_requested(edir: Path) -> bool:
    return (edir / STOP_REQUEST_FILENAME).is_file()


def _refit_output_joblib_path(phase_out: Path) -> Path:
    return phase_out / UPDATED_POLICY_SUBDIR / UPDATED_BUNDLE_BASENAME


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m starlab.training.execute_full_local_training_campaign",
        description=(
            "M50/M51: execute governed bootstrap phases from an M49 campaign contract "
            "(M45 episodes); optional M51 post-bootstrap protocol phases."
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
    parser.add_argument(
        "--post-bootstrap-protocol-phases",
        action="store_true",
        help=(
            "M51: after bootstrap phases, execute optional weighted refit, M42 comparison step, "
            "and watchable M44 per M49 protocol order (fixture/eligibility rules apply)."
        ),
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
    dataset_path: Path | None = Path(str(m26["resolved_path"])) if isinstance(m26, dict) else None
    bundle_dirs: list[Path] | None = None
    if isinstance(bundles, list):
        bundle_dirs = [Path(str(b["resolved_path"])) for b in bundles if isinstance(b, dict)]

    planned_refit = bool(m45.get("planned_weighted_refit"))

    if args.post_bootstrap_protocol_phases:
        proto = _protocol_phases_in_order(protocol)
        phases_planned = [str(p.get("phase", "unknown")) for p in proto]
    else:
        phases = _bootstrap_phases(protocol)
        if args.max_bootstrap_phases is not None:
            n = max(0, int(args.max_bootstrap_phases))
            phases = phases[:n]
        phases_planned = [str(p.get("phase", "unknown")) for p in phases]

    write_execution_manifest(
        campaign_id=str(contract["campaign_id"]),
        campaign_sha256=campaign_sha256,
        capability=capability,
        execution_dir=edir,
        execution_id=execution_id,
        phases_planned=phases_planned,
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
    phase_receipt_summaries: list[dict[str, Any]] = []
    planned_weighted_refit_executed = False
    refit_joblib_path: Path | None = None

    try:
        if args.post_bootstrap_protocol_phases:
            (
                exit_code,
                phase_results,
                phase_receipt_summaries,
                planned_weighted_refit_executed,
                refit_joblib_path,
            ) = _execute_m51_protocol_phases(
                args=args,
                bundle_dirs=bundle_dirs,
                campaign_sha256=campaign_sha256,
                dataset_path=dataset_path,
                edir=edir,
                execution_id=execution_id,
                hb_path=hb_path,
                hr_dir=hr_dir,
                match_cfg=match_cfg,
                m45=m45,
                planned_refit=planned_refit,
                protocol=protocol,
                rt=rt,
            )
        else:
            phases = _bootstrap_phases(protocol)
            if args.max_bootstrap_phases is not None:
                n = max(0, int(args.max_bootstrap_phases))
                phases = phases[:n]
            exit_code, phase_results = _execute_m50_bootstrap_only(
                args=args,
                bundle_dirs=bundle_dirs,
                campaign_sha256=campaign_sha256,
                dataset_path=dataset_path,
                edir=edir,
                execution_id=execution_id,
                hb_path=hb_path,
                hr_dir=hr_dir,
                match_cfg=match_cfg,
                phases=phases,
                rt=rt,
            )

        status = "complete" if exit_code == 0 else "failed_or_partial"
        non_claims = sorted(
            set(NON_CLAIMS_V1).union(
                {
                    "m50_campaign_execution_not_automatic_proof_of_learning",
                    "m50_hidden_rollout_not_true_headless_unless_resolved",
                }
            )
        )
        if args.post_bootstrap_protocol_phases:
            non_claims = sorted(
                non_claims
                + [
                    "m51_orchestration_only_not_m42_semantics_extension",
                    "m51_watchable_m44_not_proof_of_benchmark_strength",
                    "m51_post_refit_m42_skipped_without_m41_candidates_by_default",
                ]
            )

        pre_body: dict[str, Any] = {
            "campaign_sha256": campaign_sha256,
            "execution_id": execution_id,
            "execution_status": status,
            "hidden_rollout_capability": dict(capability),
            "non_claims": non_claims,
            "phase_results": phase_results,
            "post_bootstrap_protocol_phases_enabled": bool(args.post_bootstrap_protocol_phases),
            "run_version": HIDDEN_ROLLOUT_CAMPAIGN_RUN_VERSION,
        }
        if phase_receipt_summaries:
            pre_body["phase_receipts"] = phase_receipt_summaries

        if exit_code == 0:
            if args.post_bootstrap_protocol_phases:
                pre_body["planned_weighted_refit_executed"] = planned_weighted_refit_executed
                pre_body["planned_weighted_refit_note"] = (
                    "M51 post-bootstrap protocol: refit/compare/watchable phases recorded in "
                    "phase receipts; M42 remains M27/M41-only unless contract adds M41 candidates "
                    "(future milestone)."
                )
            else:
                pre_body["planned_weighted_refit_executed"] = False
                pre_body["planned_weighted_refit_note"] = (
                    "Default executor path runs bootstrap_episodes phases only; "
                    "use --post-bootstrap-protocol-phases for M51 refit/compare/watchable "
                    "orchestration."
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


def _execute_m50_bootstrap_only(
    *,
    args: argparse.Namespace,
    bundle_dirs: list[Path] | None,
    campaign_sha256: str,
    dataset_path: Path | None,
    edir: Path,
    execution_id: str,
    hb_path: Path,
    hr_dir: Path,
    match_cfg: Path,
    phases: list[dict[str, Any]],
    rt: RuntimeMode,
) -> tuple[int, list[dict[str, Any]]]:
    phase_results: list[dict[str, Any]] = []
    exit_code = 0
    for idx, phase in enumerate(phases):
        phase_name = str(phase.get("phase", f"phase_{idx}"))
        if _stop_requested(edir):
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
    return exit_code, phase_results


def _execute_m51_protocol_phases(
    *,
    args: argparse.Namespace,
    bundle_dirs: list[Path] | None,
    campaign_sha256: str,
    dataset_path: Path | None,
    edir: Path,
    execution_id: str,
    hb_path: Path,
    hr_dir: Path,
    match_cfg: Path,
    m45: dict[str, Any],
    planned_refit: bool,
    protocol: dict[str, Any],
    rt: RuntimeMode,
) -> tuple[
    int,
    list[dict[str, Any]],
    list[dict[str, Any]],
    bool,
    Path | None,
]:
    phase_results: list[dict[str, Any]] = []
    receipt_list: list[dict[str, Any]] = []
    exit_code = 0
    completed_bootstrap_phase_dirs: list[Path] = []
    planned_weighted_refit_executed = False
    refit_joblib_path: Path | None = None

    proto_phases = _protocol_phases_in_order(protocol)
    bootstrap_slot = 0
    max_boot = args.max_bootstrap_phases

    for order_idx, phase in enumerate(proto_phases):
        if exit_code != 0:
            break
        phase_name = str(phase.get("phase", f"phase_{order_idx}"))
        kind = str(phase.get("kind", ""))

        if _stop_requested(edir):
            write_resume_state(
                campaign_sha256=campaign_sha256,
                detail="stop request file present",
                execution_dir=edir,
                execution_id=execution_id,
                phase=phase_name,
                status="stopped_graceful",
            )
            exit_code = 6
            rec = build_phase_receipt(
                eligible=False,
                executed=False,
                final_status="skipped",
                input_artifact_refs={},
                output_artifact_refs={},
                phase_kind=kind,
                phase_name=phase_name,
                phase_order_index=order_idx,
                reason_codes=["stop_request_before_phase"],
                requested=True,
                resume_posture="quarantine_first",
                stop_boundary_reached=True,
                warnings=[],
            )
            pdir = edir / "phases" / phase_name
            write_phase_receipt(phase_output_dir=pdir, receipt=rec)
            receipt_list.append(rec)
            break

        if kind == "gate":
            rec = build_phase_receipt(
                eligible=False,
                executed=False,
                final_status="skipped",
                input_artifact_refs={},
                output_artifact_refs={},
                phase_kind=kind,
                phase_name=phase_name,
                phase_order_index=order_idx,
                reason_codes=["gate_phase_charter_only_not_executed_by_executor"],
                requested=True,
                resume_posture="not_applicable",
                stop_boundary_reached=False,
                warnings=[],
            )
            pdir = edir / "phases" / phase_name
            write_phase_receipt(phase_output_dir=pdir, receipt=rec)
            receipt_list.append(rec)
            continue

        if kind == "bootstrap_episodes":
            skip_max = max_boot is not None and bootstrap_slot >= int(max_boot)
            budget = int(phase.get("episode_budget", 0))
            if skip_max:
                bootstrap_slot += 1
                rec = build_phase_receipt(
                    eligible=False,
                    executed=False,
                    final_status="skipped",
                    input_artifact_refs={},
                    output_artifact_refs={},
                    phase_kind=kind,
                    phase_name=phase_name,
                    phase_order_index=order_idx,
                    reason_codes=["max_bootstrap_phases_limit"],
                    requested=True,
                    resume_posture="not_applicable",
                    stop_boundary_reached=False,
                    warnings=[],
                )
                pdir = edir / "phases" / phase_name
                write_phase_receipt(phase_output_dir=pdir, receipt=rec)
                receipt_list.append(rec)
                continue
            if budget < 1:
                rec = build_phase_receipt(
                    eligible=False,
                    executed=False,
                    final_status="skipped",
                    input_artifact_refs={},
                    output_artifact_refs={},
                    phase_kind=kind,
                    phase_name=phase_name,
                    phase_order_index=order_idx,
                    reason_codes=["zero_episode_budget"],
                    requested=True,
                    resume_posture="not_applicable",
                    stop_boundary_reached=False,
                    warnings=[],
                )
                pdir = edir / "phases" / phase_name
                write_phase_receipt(phase_output_dir=pdir, receipt=rec)
                receipt_list.append(rec)
                bootstrap_slot += 1
                continue

            phase_out = edir / "phases" / phase_name
            phase_out.mkdir(parents=True, exist_ok=True)
            phase_seed = int(args.seed) + bootstrap_slot * 10_000

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
                rec = build_phase_receipt(
                    eligible=True,
                    executed=True,
                    final_status="failed",
                    input_artifact_refs={"bootstrap_phase_output_dir": str(phase_out.resolve())},
                    output_artifact_refs={},
                    phase_kind=kind,
                    phase_name=phase_name,
                    phase_order_index=order_idx,
                    reason_codes=["bootstrap_phase_exception"],
                    requested=True,
                    resume_posture="quarantine_first",
                    stop_boundary_reached=False,
                    warnings=[str(e)],
                )
                write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
                receipt_list.append(rec)
                break

            completed_bootstrap_phase_dirs.append(phase_out)
            phase_results.append({"episodes": budget, "phase": phase_name, "status": "ok"})
            bootstrap_slot += 1
            rec = build_phase_receipt(
                eligible=True,
                executed=True,
                final_status="completed",
                input_artifact_refs={
                    "hierarchical_training_run_dir": str(hr_dir.resolve()),
                    "match_config_path": str(match_cfg.resolve()),
                },
                output_artifact_refs={
                    "bootstrap_dataset_json": str((phase_out / "bootstrap_dataset.json").resolve()),
                    "self_play_rl_bootstrap_run_json": str(
                        (phase_out / "self_play_rl_bootstrap_run.json").resolve()
                    ),
                },
                phase_kind=kind,
                phase_name=phase_name,
                phase_order_index=order_idx,
                reason_codes=[],
                requested=True,
                resume_posture="not_applicable",
                stop_boundary_reached=False,
                warnings=[],
            )
            write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
            receipt_list.append(rec)
            continue

        if kind == "optional" and phase_name == "optional_weighted_refit":
            phase_out = edir / "phases" / phase_name
            phase_out.mkdir(parents=True, exist_ok=True)
            requested = True
            prereq_refit = planned_refit
            prereq_ds = dataset_path is not None and dataset_path.is_file()
            prereq_bundles = bool(bundle_dirs)
            prereq_boot = bool(completed_bootstrap_phase_dirs)
            eligible = prereq_refit and prereq_ds and prereq_bundles and prereq_boot

            if not eligible:
                codes = []
                if not prereq_refit:
                    codes.append("planned_weighted_refit_false_in_contract")
                if not prereq_ds:
                    codes.append("missing_m26_replay_training_dataset")
                if not prereq_bundles:
                    codes.append("missing_m14_replay_bundle_directories")
                if not prereq_boot:
                    codes.append("no_completed_bootstrap_phases")
                rec = build_phase_receipt(
                    eligible=False,
                    executed=False,
                    final_status="skipped",
                    input_artifact_refs={
                        "completed_bootstrap_phase_dirs": [
                            str(p.resolve()) for p in completed_bootstrap_phase_dirs
                        ],
                    },
                    output_artifact_refs={},
                    phase_kind=kind,
                    phase_name=phase_name,
                    phase_order_index=order_idx,
                    reason_codes=codes,
                    requested=requested,
                    resume_posture="not_applicable",
                    stop_boundary_reached=False,
                    warnings=[],
                )
                write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
                receipt_list.append(rec)
                continue

            try:
                agg_fn = aggregate_bootstrap_pseudo_label_rows_from_completed_phase_dirs
                bx, bd, bc, bw, agg_meta = agg_fn(completed_bootstrap_phase_dirs)
            except (OSError, ValueError) as e:
                rec = build_phase_receipt(
                    eligible=True,
                    executed=False,
                    final_status="failed",
                    input_artifact_refs={
                        "completed_bootstrap_phase_dirs": [
                            str(p.resolve()) for p in completed_bootstrap_phase_dirs
                        ],
                    },
                    output_artifact_refs={},
                    phase_kind=kind,
                    phase_name=phase_name,
                    phase_order_index=order_idx,
                    reason_codes=["aggregation_failed"],
                    requested=requested,
                    resume_posture="quarantine_first",
                    stop_boundary_reached=False,
                    warnings=[str(e)],
                )
                write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
                receipt_list.append(rec)
                exit_code = 7
                phase_results.append(
                    {"error": str(e), "phase": phase_name, "status": "aggregation_failed"}
                )
                break

            if not bx:
                rec = build_phase_receipt(
                    eligible=True,
                    executed=False,
                    final_status="skipped",
                    input_artifact_refs={"aggregation_metadata": agg_meta},
                    output_artifact_refs={},
                    phase_kind=kind,
                    phase_name=phase_name,
                    phase_order_index=order_idx,
                    reason_codes=["zero_bootstrap_pseudo_label_rows"],
                    requested=requested,
                    resume_posture="not_applicable",
                    stop_boundary_reached=False,
                    warnings=[],
                )
                write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
                receipt_list.append(rec)
                continue

            refit_seed = int(args.seed) + 900_000
            assert dataset_path is not None and bundle_dirs is not None
            try:
                out_refs = run_standalone_weighted_refit_from_aggregated_rows(
                    bootstrap_coarse=bc,
                    bootstrap_delegate=bd,
                    bootstrap_w=bw,
                    bootstrap_xd=bx,
                    bundle_dirs=bundle_dirs,
                    dataset_path=dataset_path,
                    hierarchical_training_run_dir=hr_dir,
                    output_dir=phase_out,
                    seed=refit_seed,
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
                rec = build_phase_receipt(
                    eligible=True,
                    executed=True,
                    final_status="failed",
                    input_artifact_refs={"aggregation_metadata": agg_meta},
                    output_artifact_refs={},
                    phase_kind=kind,
                    phase_name=phase_name,
                    phase_order_index=order_idx,
                    reason_codes=["weighted_refit_failed"],
                    requested=requested,
                    resume_posture="quarantine_first",
                    stop_boundary_reached=False,
                    warnings=[str(e)],
                )
                write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
                receipt_list.append(rec)
                break

            planned_weighted_refit_executed = True
            refit_joblib_path = _refit_output_joblib_path(phase_out)
            phase_results.append({"phase": phase_name, "status": "ok"})
            out_artifact_refs = dict(out_refs)
            out_artifact_refs["updated_bundle_absolute_path"] = str(refit_joblib_path.resolve())
            rec = build_phase_receipt(
                eligible=True,
                executed=True,
                final_status="completed",
                input_artifact_refs={
                    "aggregation_metadata": agg_meta,
                    "m26_replay_training_dataset": str(dataset_path.resolve()),
                },
                output_artifact_refs=out_artifact_refs,
                phase_kind=kind,
                phase_name=phase_name,
                phase_order_index=order_idx,
                reason_codes=[],
                requested=requested,
                resume_posture="not_applicable",
                stop_boundary_reached=False,
                warnings=[],
            )
            write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
            receipt_list.append(rec)
            continue

        if kind == "offline" and phase_name == "post_refit_m42_comparison":
            phase_out = edir / "phases" / phase_name
            phase_out.mkdir(parents=True, exist_ok=True)
            requested = True
            # M51: honest skip — M42 compares M27 vs M41 only; refit bundle is not an M41 candidate.
            rec = build_phase_receipt(
                eligible=False,
                executed=False,
                final_status="skipped",
                input_artifact_refs={},
                output_artifact_refs={},
                phase_kind=kind,
                phase_name=phase_name,
                phase_order_index=order_idx,
                reason_codes=["candidate_not_m41_comparison_compatible"],
                requested=requested,
                resume_posture="not_applicable",
                stop_boundary_reached=False,
                warnings=[],
            )
            write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
            receipt_list.append(rec)
            continue

        if kind == "operator_review" and phase_name == "watchable_m44_validation":
            phase_out = edir / "phases" / phase_name
            phase_out.mkdir(parents=True, exist_ok=True)
            requested = True
            if refit_joblib_path is None or not refit_joblib_path.is_file():
                codes = ["watchable_m44_requires_successful_refit_bundle"]
                if refit_joblib_path is not None:
                    codes.append("refit_output_joblib_missing")
                rec = build_phase_receipt(
                    eligible=False,
                    executed=False,
                    final_status="skipped",
                    input_artifact_refs={},
                    output_artifact_refs={},
                    phase_kind=kind,
                    phase_name=phase_name,
                    phase_order_index=order_idx,
                    reason_codes=codes,
                    requested=requested,
                    resume_posture="not_applicable",
                    stop_boundary_reached=False,
                    warnings=[],
                )
                write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
                receipt_list.append(rec)
                continue

            mraw = json.loads(match_cfg.read_text(encoding="utf-8"))
            if not isinstance(mraw, dict):
                msg = "match config root must be an object"
                raise ValueError(msg)
            watch_seed = int(args.seed) + 950_000
            mraw["seed"] = watch_seed
            watch_match = phase_out / "watchable_match_config.json"
            cfg = match_config_from_mapping(mraw)
            watch_match.write_text(
                canonical_json_dumps(match_config_to_mapping(cfg)),
                encoding="utf-8",
            )

            try:
                run_local_live_play_validation(
                    enforce_weights_sidecar_sha256=False,
                    hierarchical_training_run_dir=hr_dir,
                    match_config_path=watch_match,
                    output_dir=phase_out,
                    runtime_mode=rt,
                    weights_path=refit_joblib_path,
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
                rec = build_phase_receipt(
                    eligible=True,
                    executed=True,
                    final_status="failed",
                    input_artifact_refs={"weights_path": str(refit_joblib_path.resolve())},
                    output_artifact_refs={},
                    phase_kind=kind,
                    phase_name=phase_name,
                    phase_order_index=order_idx,
                    reason_codes=["watchable_m44_validation_failed"],
                    requested=requested,
                    resume_posture="quarantine_first",
                    stop_boundary_reached=False,
                    warnings=[str(e)],
                )
                write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
                receipt_list.append(rec)
                break

            phase_results.append({"phase": phase_name, "status": "ok"})
            rec = build_phase_receipt(
                eligible=True,
                executed=True,
                final_status="completed",
                input_artifact_refs={
                    "refit_joblib_path": str(refit_joblib_path.resolve()),
                    "watchable_match_config": str(watch_match.resolve()),
                },
                output_artifact_refs={
                    "local_live_play_validation_run": str(
                        (phase_out / "local_live_play_validation_run.json").resolve()
                    ),
                },
                phase_kind=kind,
                phase_name=phase_name,
                phase_order_index=order_idx,
                reason_codes=[],
                requested=requested,
                resume_posture="not_applicable",
                stop_boundary_reached=False,
                warnings=[],
            )
            write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
            receipt_list.append(rec)
            continue

        # Unknown / future phase kinds: explicit skip receipt
        phase_out = edir / "phases" / phase_name
        phase_out.mkdir(parents=True, exist_ok=True)
        rec = build_phase_receipt(
            eligible=False,
            executed=False,
            final_status="skipped",
            input_artifact_refs={},
            output_artifact_refs={},
            phase_kind=kind,
            phase_name=phase_name,
            phase_order_index=order_idx,
            reason_codes=["phase_kind_not_executed_in_m51"],
            requested=True,
            resume_posture="not_applicable",
            stop_boundary_reached=False,
            warnings=[],
        )
        write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
        receipt_list.append(rec)

    return (
        exit_code,
        phase_results,
        receipt_list,
        planned_weighted_refit_executed,
        refit_joblib_path,
    )


if __name__ == "__main__":
    raise SystemExit(main())
