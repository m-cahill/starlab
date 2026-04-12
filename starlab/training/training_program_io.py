"""Write agent training program contract artifacts (deterministic JSON)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.training.training_program_models import (
    AGENT_TRAINING_PROGRAM_CONTRACT_REPORT_VERSION,
    AGENT_TRAINING_PROGRAM_CONTRACT_VERSION,
    CONTRACT_FILENAME,
    REPORT_FILENAME,
    TRAINING_PHASE_VERSION,
    allowed_upstreams_v1,
    canonical_evaluation_entrypoints_v1,
    ci_policy_v1,
    future_required_artifacts_v1,
    local_training_policy_v1,
    milestone_sequence_v1,
    non_claims_v1,
    rights_and_provenance_reminders_v1,
)


def build_agent_training_program_contract() -> dict[str, Any]:
    seq = milestone_sequence_v1()
    body: dict[str, Any] = {
        "program_version": AGENT_TRAINING_PROGRAM_CONTRACT_VERSION,
        "training_phase_version": TRAINING_PHASE_VERSION,
        "milestone_sequence": [dict(row) for row in seq],
        "allowed_upstreams": allowed_upstreams_v1(),
        "canonical_evaluation_entrypoints": list(canonical_evaluation_entrypoints_v1()),
        "future_required_artifacts": future_required_artifacts_v1(),
        "ci_policy": ci_policy_v1(),
        "local_training_policy": local_training_policy_v1(),
        "non_claims": list(non_claims_v1()),
        "rights_and_provenance_reminders": list(rights_and_provenance_reminders_v1()),
    }
    digest = sha256_hex_of_canonical_json(body)
    body["contract_sha256"] = digest
    return body


def build_agent_training_program_contract_report(contract: dict[str, Any]) -> dict[str, Any]:
    seq = contract["milestone_sequence"]
    summary_ms = [f"{row['milestone']}: {row['title']}" for row in seq]
    return {
        "report_version": AGENT_TRAINING_PROGRAM_CONTRACT_REPORT_VERSION,
        "contract_sha256": contract["contract_sha256"],
        "program_version": contract["program_version"],
        "training_phase_version": contract["training_phase_version"],
        "summary": {
            "milestone_titles": summary_ms,
            "arc": "M40–M45 governed agent training track (Phase VI recharter post-M39).",
            "ci_posture": "No GPU training or live SC2 in CI; contract validation and tests only.",
            "local_posture": contract["local_training_policy"],
        },
        "non_claims": contract["non_claims"],
    }


def write_agent_training_program_contract(output_dir: Path) -> tuple[Path, Path]:
    """Emit contract + report JSON under output_dir (e.g. out/training_program)."""

    output_dir.mkdir(parents=True, exist_ok=True)
    contract = build_agent_training_program_contract()
    report = build_agent_training_program_contract_report(contract)

    c_path = output_dir / CONTRACT_FILENAME
    r_path = output_dir / REPORT_FILENAME
    c_path.write_text(canonical_json_dumps(contract), encoding="utf-8")
    r_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    return c_path, r_path
