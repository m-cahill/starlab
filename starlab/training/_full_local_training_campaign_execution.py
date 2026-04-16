"""Private helpers for M50/M51 governed campaign execution (split from the executor CLI)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps
from starlab.sc2.local_live_play_validation_harness import run_local_live_play_validation
from starlab.sc2.local_live_play_validation_models import RuntimeMode
from starlab.sc2.match_config import match_config_from_mapping, match_config_to_mapping
from starlab.training.campaign_execution_io import (
    HIDDEN_ROLLOUT_CAMPAIGN_RUN_FILENAME,
    STOP_REQUEST_FILENAME,
    update_heartbeat,
    write_resume_state,
)
from starlab.training.campaign_phase_receipt import build_phase_receipt, write_phase_receipt
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


def execute_m50_bootstrap_only(
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


def execute_m51_protocol_phases(
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

    _ = m45

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


__all__ = [
    "_bootstrap_phases",
    "_execution_tree_state",
    "_load_contract",
    "_protocol_phases_in_order",
    "execute_m50_bootstrap_only",
    "execute_m51_protocol_phases",
]
