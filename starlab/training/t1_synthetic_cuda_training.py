"""Bounded T1 synthetic CUDA PyTorch training phase (governed M50 extension).

Not gameplay, benchmark, or strong-agent evidence — wiring for honest checkpoint artifacts only.
"""

from __future__ import annotations

import argparse
import os
import time
from pathlib import Path
from typing import Any

from starlab.training.campaign_execution_io import update_heartbeat, write_resume_state
from starlab.training.campaign_phase_receipt import build_phase_receipt, write_phase_receipt

PHASE_KIND_T1_SYNTHETIC_CUDA: str = "t1_synthetic_cuda_training"

_ENV_MIN_WALL_OVERRIDE: str = "STARLAB_T1_SYNTHETIC_CUDA_MIN_WALL_SECONDS"


def _campaign_wall_clock_elapsed_s(args: argparse.Namespace) -> float:
    start = getattr(args, "_campaign_wall_clock_start_monotonic", None)
    if start is None:
        return 0.0
    return time.monotonic() - float(start)


def _max_campaign_wall_seconds(args: argparse.Namespace) -> float | None:
    mins = getattr(args, "max_wall_clock_minutes", None)
    if mins is None:
        return None
    return float(mins) * 60.0


def _effective_min_wall_seconds(phase: dict[str, Any]) -> int:
    raw = phase.get("min_wall_seconds", 300)
    try:
        n = int(raw)
    except (TypeError, ValueError):
        n = 300
    n = max(1, n)
    env_raw = os.environ.get(_ENV_MIN_WALL_OVERRIDE, "").strip()
    if env_raw:
        try:
            env_n = int(env_raw)
            if env_n > 0:
                n = env_n
        except ValueError:
            pass
    return n


def _steps_per_tick(phase: dict[str, Any]) -> int:
    raw = phase.get("steps_per_tick", 400)
    try:
        n = int(raw)
    except (TypeError, ValueError):
        n = 400
    return max(1, min(n, 50_000))


def _checkpoint_interval_s(phase: dict[str, Any]) -> int:
    raw = phase.get("checkpoint_interval_wall_seconds", 120)
    try:
        n = int(raw)
    except (TypeError, ValueError):
        n = 120
    return max(30, min(n, 3600))


def run_t1_synthetic_cuda_training_phase(
    *,
    phase: dict[str, Any],
    phase_order_index: int,
    args: argparse.Namespace,
    campaign_sha256: str,
    execution_id: str,
    edir: Path,
    hb_path: Path,
) -> tuple[int, dict[str, Any]]:
    """Execute one synthetic CUDA training phase under ``edir/phases/<phase_name>``."""

    phase_name = str(phase.get("phase", "t1_synthetic_cuda"))
    phase_out = edir / "phases" / phase_name
    phase_out.mkdir(parents=True, exist_ok=True)

    try:
        import torch
    except ImportError as e:
        rec = build_phase_receipt(
            phase_name=phase_name,
            phase_order_index=phase_order_index,
            phase_kind=PHASE_KIND_T1_SYNTHETIC_CUDA,
            requested=True,
            eligible=True,
            executed=False,
            final_status="failed",
            reason_codes=["torch_import_failed"],
            warnings=[str(e)],
            input_artifact_refs={"run_tier": str(getattr(args, "run_tier", "") or "")},
            output_artifact_refs={},
            resume_posture="not_applicable",
            stop_boundary_reached=False,
        )
        write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
        return 7, {"phase": phase_name, "status": "failed", "error": "torch_import_failed"}

    if not torch.cuda.is_available():
        rec = build_phase_receipt(
            phase_name=phase_name,
            phase_order_index=phase_order_index,
            phase_kind=PHASE_KIND_T1_SYNTHETIC_CUDA,
            requested=True,
            eligible=True,
            executed=False,
            final_status="failed",
            reason_codes=["cuda_not_available"],
            warnings=[],
            input_artifact_refs={"run_tier": str(getattr(args, "run_tier", "") or "")},
            output_artifact_refs={},
            resume_posture="not_applicable",
            stop_boundary_reached=False,
        )
        write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
        return 7, {"phase": phase_name, "status": "failed", "error": "cuda_not_available"}

    min_wall = _effective_min_wall_seconds(phase)
    steps_tick = _steps_per_tick(phase)
    ck_interval = _checkpoint_interval_s(phase)
    max_campaign = _max_campaign_wall_seconds(args)

    device = torch.device("cuda")
    torch.manual_seed(42)
    torch.cuda.manual_seed_all(42)

    model = torch.nn.Sequential(
        torch.nn.Linear(512, 256),
        torch.nn.ReLU(),
        torch.nn.Linear(256, 128),
    )
    model = model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    x = torch.randn(256, 512, device=device)
    y = torch.randn(256, 128, device=device)

    ck_path = phase_out / "t1_synthetic_cuda_checkpoint.pt"
    t_phase0 = time.monotonic()
    last_ck = t_phase0
    total_steps = 0
    stop_boundary = False

    try:
        while True:
            if max_campaign is not None and _campaign_wall_clock_elapsed_s(args) >= max_campaign:
                stop_boundary = True
                break
            elapsed_phase = time.monotonic() - t_phase0
            if elapsed_phase >= float(min_wall):
                break

            for _ in range(steps_tick):
                opt.zero_grad()
                loss = torch.nn.functional.mse_loss(model(x), y)
                loss.backward()  # type: ignore[no-untyped-call]
                opt.step()
                total_steps += 1

            update_heartbeat(
                episode_index=None,
                heartbeat_path=hb_path,
                last_phase=phase_name,
            )

            now = time.monotonic()
            if now - last_ck >= float(ck_interval):
                torch.save(
                    {
                        "model_state_dict": model.state_dict(),
                        "step": total_steps,
                        "phase": phase_name,
                        "trainer_kind": "t1_synthetic_cuda_mlp",
                    },
                    ck_path,
                )
                last_ck = now

        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "step": total_steps,
                "phase": phase_name,
                "trainer_kind": "t1_synthetic_cuda_mlp",
            },
            ck_path,
        )
    except RuntimeError as e:
        write_resume_state(
            campaign_sha256=campaign_sha256,
            detail=str(e),
            execution_dir=edir,
            execution_id=execution_id,
            phase=phase_name,
            status="failed",
        )
        rec = build_phase_receipt(
            phase_name=phase_name,
            phase_order_index=phase_order_index,
            phase_kind=PHASE_KIND_T1_SYNTHETIC_CUDA,
            requested=True,
            eligible=True,
            executed=True,
            final_status="failed",
            reason_codes=["synthetic_cuda_runtime_error"],
            warnings=[str(e)],
            input_artifact_refs={"run_tier": str(getattr(args, "run_tier", "") or "")},
            output_artifact_refs={},
            resume_posture="not_applicable",
            stop_boundary_reached=stop_boundary,
        )
        write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
        return 7, {"phase": phase_name, "status": "failed", "error": str(e)}

    if stop_boundary and (time.monotonic() - t_phase0) < float(min_wall):
        rec = build_phase_receipt(
            phase_name=phase_name,
            phase_order_index=phase_order_index,
            phase_kind=PHASE_KIND_T1_SYNTHETIC_CUDA,
            requested=True,
            eligible=True,
            executed=True,
            final_status="failed",
            reason_codes=["max_wall_clock_minutes_exceeded_before_min_synthetic_training"],
            warnings=[],
            input_artifact_refs={
                "run_tier": str(getattr(args, "run_tier", "") or ""),
                "min_wall_seconds_configured": min_wall,
            },
            output_artifact_refs={"checkpoint_path": str(ck_path.resolve())}
            if ck_path.is_file()
            else {},
            resume_posture="not_applicable",
            stop_boundary_reached=True,
        )
        write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
        return 8, {
            "phase": phase_name,
            "status": "wall_clock_budget_exceeded",
            "steps": total_steps,
        }

    rec = build_phase_receipt(
        phase_name=phase_name,
        phase_order_index=phase_order_index,
        phase_kind=PHASE_KIND_T1_SYNTHETIC_CUDA,
        requested=True,
        eligible=True,
        executed=True,
        final_status="completed",
        reason_codes=[],
        warnings=[],
        input_artifact_refs={
            "run_tier": str(getattr(args, "run_tier", "") or ""),
            "min_wall_seconds": min_wall,
            "steps_per_tick": steps_tick,
        },
        output_artifact_refs={
            "checkpoint_path": str(ck_path.resolve()),
            "trainer_module": "starlab.training.t1_synthetic_cuda_training",
        },
        resume_posture="not_applicable",
        stop_boundary_reached=False,
    )
    write_phase_receipt(phase_output_dir=phase_out, receipt=rec)
    return 0, {
        "phase": phase_name,
        "status": "ok",
        "steps": total_steps,
        "wall_seconds_observed": time.monotonic() - t_phase0,
    }


def t1_synthetic_cuda_phases_in_order(protocol: dict[str, Any]) -> list[dict[str, Any]]:
    phases = protocol.get("phases")
    if not isinstance(phases, list):
        return []
    return [
        p
        for p in phases
        if isinstance(p, dict) and str(p.get("kind")) == PHASE_KIND_T1_SYNTHETIC_CUDA
    ]


def execute_t1_synthetic_cuda_phases_after_bootstrap(
    *,
    args: argparse.Namespace,
    protocol: dict[str, Any],
    campaign_sha256: str,
    execution_id: str,
    edir: Path,
    hb_path: Path,
    phase_results: list[dict[str, Any]],
) -> tuple[int, list[dict[str, Any]]]:
    """Run synthetic CUDA phases when ``run_tier`` is T1_30_MIN and the protocol lists them."""

    if str(getattr(args, "run_tier", "") or "") != "T1_30_MIN":
        return 0, []
    extra: list[dict[str, Any]] = []
    to_run = t1_synthetic_cuda_phases_in_order(protocol)
    if not to_run:
        return 0, []
    exit_code = 0
    base_idx = len(phase_results)
    for i, phase in enumerate(to_run):
        code, pr = run_t1_synthetic_cuda_training_phase(
            phase=phase,
            phase_order_index=base_idx + i,
            args=args,
            campaign_sha256=campaign_sha256,
            execution_id=execution_id,
            edir=edir,
            hb_path=hb_path,
        )
        extra.append(pr)
        if code != 0:
            exit_code = code
            break
    return exit_code, extra
