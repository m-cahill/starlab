"""Receipt and report JSON construction for replay parse pipeline (M08 / M35)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.replays.parser_interfaces import ReplayParserAdapter
from starlab.replays.parser_io_checks import finalize_checks
from starlab.replays.parser_models import (
    PARSER_CONTRACT_VERSION,
    POLICY_VERSION,
    RECEIPT_SCHEMA_VERSION,
    REPORT_SCHEMA_VERSION,
    CheckResult,
    ParseStatus,
)


def _build_receipt(
    *,
    adapter: ReplayParserAdapter,
    parse_input_artifacts: dict[str, str | None],
    raw_parse_sha256: str | None,
    replay_path: Path,
    replay_sha256: str | None,
) -> dict[str, Any]:
    return {
        "observed_filename": replay_path.name,
        "parse_input_artifacts": parse_input_artifacts,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "parser_family": adapter.parser_family(),
        "parser_version": adapter.parser_version(),
        "policy_version": POLICY_VERSION,
        "raw_parse_sha256": raw_parse_sha256,
        "replay_content_sha256": replay_sha256,
        "schema_version": RECEIPT_SCHEMA_VERSION,
    }


def _build_report(
    *,
    adapter: ReplayParserAdapter,
    advisory_notes: list[str],
    checks: list[CheckResult],
    reason_codes: list[str],
    replay_sha256: str | None,
    status: ParseStatus,
) -> dict[str, Any]:
    ordered = finalize_checks(checks)
    return {
        "advisory_notes": sorted(set(advisory_notes)),
        "check_results": [c.to_mapping() for c in ordered],
        "parser_family": adapter.parser_family(),
        "parser_version": adapter.parser_version(),
        "parse_status": status,
        "reason_codes": sorted(set(reason_codes)),
        "replay_content_sha256": replay_sha256,
        "schema_version": REPORT_SCHEMA_VERSION,
    }


__all__ = [
    "_build_receipt",
    "_build_report",
]
