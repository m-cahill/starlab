"""Logical path identity for sealed PX2 self-play artifacts (PX2-M03 slice 6).

Absolute machine paths remain in JSON for operators; sealed hashes use stable logical keys.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

PREFLIGHT_SEAL_VERSION: Final[str] = "px2_m03_slice6_logical_v1"


def corpus_root_logical_posix(corpus_root: Path) -> str:
    """Stable logical corpus ref when under STARLAB ``tests/fixtures/`` lineage."""

    p = corpus_root.resolve().as_posix().replace("\\", "/")
    key = "/fixtures/"
    if key in p:
        idx = p.index(key)
        return ("tests" + p[idx:]).replace("//", "/")
    return f"corpus_logical:{corpus_root.name}"


def output_dir_logical_posix(output_dir: Path, run_id: str) -> str:
    """Stable run output root: ``runs/<run_id>/`` when directory layout matches."""

    op = output_dir.resolve()
    parts = tuple(op.parts)
    if len(parts) >= 2 and parts[-2] == "runs" and parts[-1] == run_id:
        return f"runs/{run_id}/"
    if op.name == run_id:
        return f"runs/{run_id}/"
    return f"output_dir_logical:{run_id}"


def weights_path_logical_posix(weights_path: Path | None) -> str | None:
    """Basename-only logical identity for weight files (cross-machine stable)."""

    if weights_path is None:
        return None
    return Path(weights_path).name


def build_preflight_seal_basis(
    *,
    contract_id: str,
    run_id: str,
    corpus_root: Path,
    output_dir: Path,
    init_only: bool,
    weights_path: Path | None,
    weight_bundle_ref: str | None,
    torch_seed: int,
    device_intent: str,
    map_location: str,
    preflight_ok: bool,
    checks: list[dict[str, Any]],
    non_claims: list[str],
) -> dict[str, Any]:
    """Exact dict hashed as ``preflight_sha256`` (canonical JSON, no absolute paths)."""

    return {
        "contract_id": contract_id,
        "preflight_seal_version": PREFLIGHT_SEAL_VERSION,
        "run_id": run_id,
        "corpus_root_logical": corpus_root_logical_posix(corpus_root),
        "output_dir_logical": output_dir_logical_posix(output_dir, run_id),
        "weights_path_logical": weights_path_logical_posix(weights_path),
        "init_only": init_only,
        "weight_bundle_ref": weight_bundle_ref.strip() if weight_bundle_ref else None,
        "torch_seed": torch_seed,
        "device_intent": device_intent,
        "map_location": map_location,
        "preflight_ok": preflight_ok,
        "preflight_checks_stable": [
            {"check_id": c["check_id"], "status": c["status"]} for c in checks
        ],
        "non_claims": non_claims,
    }
