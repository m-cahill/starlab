"""Operator-local execution preflight receipts (PX2-M03 slice 3)."""

from __future__ import annotations

import platform
import sys
from pathlib import Path
from pickle import UnpicklingError
from typing import Any, Final

import torch

from starlab.runs.json_util import sha256_hex_of_canonical_json
from starlab.sc2.px2.self_play.weight_loading import load_policy_from_weights_file

PX2_SELF_PLAY_EXECUTION_PREFLIGHT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_execution_preflight.v1"
)
PX2_SELF_PLAY_EXECUTION_PREFLIGHT_REPORT_CONTRACT_ID: Final[str] = (
    "starlab.px2.self_play_execution_preflight_report.v1"
)


def _seal_preflight_body(body_without_seal: dict[str, Any]) -> str:
    return sha256_hex_of_canonical_json(body_without_seal)


def run_execution_preflight(
    *,
    corpus_root: Path,
    output_dir: Path,
    init_only: bool,
    weights_path: Path | None,
    weight_bundle_ref: str | None,
    torch_seed: int,
    run_id: str,
    device_intent: str = "cpu",
    map_location: str = "cpu",
) -> tuple[bool, dict[str, Any], dict[str, Any], list[str]]:
    """Validate operator-local inputs; return preflight JSON, report, and error codes.

    Emits **readiness** only — **not** campaign success, **not** industrial proof.
    """

    errors: list[str] = []
    checks: list[dict[str, Any]] = []

    cr = corpus_root.resolve()
    if cr.is_dir():
        checks.append({"check_id": "corpus_root_exists", "status": "ok", "detail": cr.as_posix()})
    else:
        errors.append("corpus_root_not_found")
        checks.append({"check_id": "corpus_root_exists", "status": "fail", "detail": cr.as_posix()})

    out = output_dir.resolve()
    try:
        out.mkdir(parents=True, exist_ok=True)
        probe = out / ".px2_preflight_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        checks.append({"check_id": "output_dir_writable", "status": "ok", "detail": out.as_posix()})
    except OSError as exc:
        errors.append("output_dir_not_writable")
        checks.append({"check_id": "output_dir_writable", "status": "fail", "detail": str(exc)})

    if init_only:
        checks.append({"check_id": "policy_weight_mode", "status": "ok", "detail": "init_only"})
        if weights_path is not None:
            errors.append("weights_path_forbidden_when_init_only")
            checks.append(
                {
                    "check_id": "init_only_no_weights_path",
                    "status": "fail",
                    "detail": "weights_path must be omitted when init_only=True",
                }
            )
    elif weights_path is None:
        errors.append("weights_path_required_when_not_init_only")
        checks.append(
            {
                "check_id": "weights_source",
                "status": "fail",
                "detail": "slice 3 requires a weights file path when init_only=False",
            }
        )
    else:
        wp = weights_path.resolve()
        if not wp.is_file():
            errors.append("weights_file_missing")
            checks.append(
                {"check_id": "weights_file_exists", "status": "fail", "detail": wp.as_posix()},
            )
        else:
            checks.append(
                {"check_id": "weights_file_exists", "status": "ok", "detail": wp.as_posix()},
            )
            try:
                load_policy_from_weights_file(weights_path=wp, map_location=map_location)
                checks.append(
                    {"check_id": "weights_loadable", "status": "ok", "detail": "state_dict"},
                )
            except (OSError, ValueError, RuntimeError, UnpicklingError) as exc:
                errors.append("weights_load_failed")
                checks.append(
                    {"check_id": "weights_loadable", "status": "fail", "detail": str(exc)},
                )

    body: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_EXECUTION_PREFLIGHT_CONTRACT_ID,
        "run_id": run_id,
        "corpus_root": cr.as_posix(),
        "output_dir": out.as_posix(),
        "init_only": init_only,
        "weights_path": weights_path.resolve().as_posix() if weights_path else None,
        "weight_bundle_ref": weight_bundle_ref.strip() if weight_bundle_ref else None,
        "torch_seed": torch_seed,
        "device_intent": device_intent,
        "map_location": map_location,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "torch_version": torch.__version__,
        "preflight_checks": checks,
        "preflight_ok": len(errors) == 0,
        "non_claims": [
            "Operator-local execution preflight — not campaign success evidence.",
            "Not Blackwell-scale or industrial completion proof.",
        ],
    }
    seal = _seal_preflight_body({k: v for k, v in body.items() if k != "preflight_sha256"})
    preflight = dict(body)
    preflight["preflight_sha256"] = seal

    report: dict[str, Any] = {
        "contract_id": PX2_SELF_PLAY_EXECUTION_PREFLIGHT_REPORT_CONTRACT_ID,
        "preflight_sha256": seal,
        "run_id": run_id,
        "summary": {
            "preflight_ok": preflight["preflight_ok"],
            "error_codes": errors,
        },
        "non_claims": body["non_claims"],
    }
    ok = len(errors) == 0
    return ok, preflight, report, errors
