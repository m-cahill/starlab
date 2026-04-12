"""Read/write M44 local live-play validation JSON artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.sc2.local_live_play_validation_models import (
    LOCAL_LIVE_PLAY_VALIDATION_RUN_FILENAME,
    LOCAL_LIVE_PLAY_VALIDATION_RUN_REPORT_FILENAME,
    LOCAL_LIVE_PLAY_VALIDATION_RUN_REPORT_VERSION,
)


def load_json_object(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        msg = f"{path.name} root must be a JSON object"
        raise ValueError(msg)
    return data


def sha256_hex_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def write_validation_artifacts(
    *,
    run_body: dict[str, Any],
    report_body: dict[str, Any],
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write run + report JSON under ``output_dir``."""

    output_dir.mkdir(parents=True, exist_ok=True)
    run_path = output_dir / LOCAL_LIVE_PLAY_VALIDATION_RUN_FILENAME
    rep_path = output_dir / LOCAL_LIVE_PLAY_VALIDATION_RUN_REPORT_FILENAME
    run_path.write_text(canonical_json_dumps(run_body), encoding="utf-8")
    rep_path.write_text(canonical_json_dumps(report_body), encoding="utf-8")
    return run_path, rep_path


def seal_validation_run_body(body_without_hash: dict[str, Any]) -> dict[str, Any]:
    """Attach ``validation_run_sha256`` over the object without that field."""

    digest = sha256_hex_of_canonical_json(body_without_hash)
    return {**body_without_hash, "validation_run_sha256": digest}


def minimal_report_from_run(run: dict[str, Any]) -> dict[str, Any]:
    """Compact report JSON linked to the run digest."""

    return {
        "report_version": LOCAL_LIVE_PLAY_VALIDATION_RUN_REPORT_VERSION,
        "validation_run_sha256": run["validation_run_sha256"],
        "run_id": run["run_id"],
        "runtime_mode": run["runtime_mode"],
        "candidate": {
            "hierarchical_training_run_sha256": run["candidate"][
                "hierarchical_training_run_sha256"
            ],
            "training_run_id": run["candidate"]["training_run_id"],
        },
        "replay_binding_id": run["replay_binding"]["replay_binding_id"],
        "replay_content_sha256": run["replay_binding"]["replay_content_sha256"],
        "semantic_live_action_adapter_policy_id": run["semantic_live_action_adapter_policy_id"],
        "warnings": run.get("warnings", []),
        "caveats": run.get("caveats", []),
        "non_claims": run.get("non_claims", []),
        "optional_media": run.get("optional_media_registration"),
    }
