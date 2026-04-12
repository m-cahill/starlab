"""Build and write replay-imitation training run JSON artifacts (M41)."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from starlab.imitation.replay_imitation_training_models import (
    REPLAY_IMITATION_TRAINING_RUN_FILENAME,
    REPLAY_IMITATION_TRAINING_RUN_REPORT_FILENAME,
    REPLAY_IMITATION_TRAINING_RUN_REPORT_VERSION,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def compute_deterministic_run_id(*, identity_payload: dict[str, Any]) -> str:
    """64-char hex run id from canonical JSON of the identity payload (no timestamp)."""

    return sha256_hex_of_canonical_json(identity_payload)


def sha256_hex_file(path: Path) -> str:
    h = hashlib.sha256()
    data = path.read_bytes()
    h.update(data)
    return h.hexdigest()


def write_replay_imitation_training_artifacts(
    *,
    run_body: dict[str, Any],
    report_body: dict[str, Any],
    output_dir: Path,
) -> tuple[Path, Path]:
    """Write run + report JSON; ``run_body`` must already include ``training_run_sha256``."""

    output_dir.mkdir(parents=True, exist_ok=True)
    run_path = output_dir / REPLAY_IMITATION_TRAINING_RUN_FILENAME
    rep_path = output_dir / REPLAY_IMITATION_TRAINING_RUN_REPORT_FILENAME
    run_path.write_text(canonical_json_dumps(run_body), encoding="utf-8")
    rep_path.write_text(canonical_json_dumps(report_body), encoding="utf-8")
    return run_path, rep_path


def seal_training_run_body(body_without_hash: dict[str, Any]) -> dict[str, Any]:
    """Attach ``training_run_sha256`` over the object without that field."""

    digest = sha256_hex_of_canonical_json(body_without_hash)
    return {**body_without_hash, "training_run_sha256": digest}


def minimal_report_from_run(run: dict[str, Any]) -> dict[str, Any]:
    """Compact report JSON linked to the run digest."""

    return {
        "report_version": REPLAY_IMITATION_TRAINING_RUN_REPORT_VERSION,
        "training_run_sha256": run["training_run_sha256"],
        "run_id": run["run_id"],
        "training_program_contract_sha256": run["training_program_contract_sha256"],
        "summary": {
            "model_family": run["model_family"],
            "dataset_sha256": run["source_dataset"]["dataset_sha256"],
            "split_metrics": run["split_metrics"],
            "example_counts_by_split": run["example_counts_by_split"],
        },
        "feature_schema_summary": {
            "encoding_policy_id": run["feature_schema"]["encoding_policy_id"],
            "feature_count": len(run["feature_schema"]["ordered_feature_names"]),
            "label_count": len(run["feature_schema"]["label_vocabulary"]),
        },
        "warnings": run.get("warnings", []),
        "caveats": run.get("caveats", []),
        "non_claims": run.get("non_claims", []),
        "provenance": {
            "training_program_contract_version": run["training_program_contract_version"],
            "weights_emitted": run.get("weights_sidecar") is not None,
        },
    }
