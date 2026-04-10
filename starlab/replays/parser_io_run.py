"""Core ``run_replay_parse`` pipeline (M08 / M35 decomposition)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from starlab.replays.parser_interfaces import AdapterFailure, AdapterSuccess, ReplayParserAdapter
from starlab.replays.parser_io_checks import (
    _merge_checks,
    _sha256_file,
    _status_from_adapter_failure,
    load_optional_json,
    load_optional_replay_binding,
    read_replay_opaque,
)
from starlab.replays.parser_io_raw_parse import (
    _build_raw_parse_empty,
    _normalize_raw_event_streams,
    _normalize_raw_sections,
)
from starlab.replays.parser_io_receipt_report import _build_receipt, _build_report
from starlab.replays.parser_models import (
    NORMALIZATION_PROFILE_V1,
    RAW_PARSE_SCHEMA_VERSION_V1,
    RAW_PARSE_SCHEMA_VERSION_V2,
    CheckResult,
    CheckSeverity,
    ParseStatus,
)
from starlab.replays.parser_normalization import NormalizationError, normalize_value
from starlab.replays.s2protocol_adapter import default_adapter
from starlab.runs.json_util import sha256_hex_of_canonical_json


def run_replay_parse(
    *,
    replay_path: Path,
    intake_receipt_path: Path | None,
    intake_report_path: Path | None,
    replay_binding_path: Path | None,
    adapter: ReplayParserAdapter | None = None,
) -> tuple[ParseStatus, dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Execute parse pipeline and return ``(status, receipt, report, raw_parse)``."""

    adapter = adapter or default_adapter()
    checks: list[CheckResult] = []
    reason_codes: list[str] = []
    advisory: list[str] = []

    replay_sha256: str | None = None
    replay_read_err: str | None = None

    digest, _size, rerr = read_replay_opaque(replay_path)
    if rerr is not None:
        checks.append(
            CheckResult(
                check_id="replay_file_readable",
                detail=rerr,
                severity="required",
                status="fail",
            ),
        )
        replay_read_err = rerr
    else:
        checks.append(
            CheckResult(
                check_id="replay_file_readable",
                detail=None,
                severity="required",
                status="pass",
            ),
        )
        replay_sha256 = digest

    if replay_sha256 is not None:
        checks.append(
            CheckResult(
                check_id="replay_sha256_computed",
                detail=None,
                severity="required",
                status="pass",
            ),
        )
    else:
        checks.append(
            CheckResult(
                check_id="replay_sha256_computed",
                detail=replay_read_err,
                severity="required",
                status="fail",
            ),
        )

    # Dependency / adapter
    deps_ok = adapter.dependency_available()
    checks.append(
        CheckResult(
            check_id="parser_dependency_available",
            detail=None,
            severity="required",
            status="pass" if deps_ok else "fail",
        ),
    )
    checks.append(
        CheckResult(
            check_id="parser_adapter_selected",
            detail=adapter.parser_family(),
            severity="required",
            status="pass",
        ),
    )

    intake_receipt, ir_err = load_optional_json(intake_receipt_path)
    intake_report, _irpt_err = load_optional_json(intake_report_path)
    binding: dict[str, Any] | None
    bind_err: str | None
    if replay_binding_path is None:
        binding, bind_err = None, None
    else:
        binding, bind_err = load_optional_replay_binding(replay_binding_path)

    parse_input_artifacts: dict[str, str | None] = {}
    if intake_receipt_path is not None:
        try:
            parse_input_artifacts["replay_intake_receipt.json"] = _sha256_file(intake_receipt_path)
        except OSError:
            parse_input_artifacts["replay_intake_receipt.json"] = None
    else:
        parse_input_artifacts["replay_intake_receipt.json"] = None

    if intake_report_path is not None:
        try:
            parse_input_artifacts["replay_intake_report.json"] = _sha256_file(intake_report_path)
        except OSError:
            parse_input_artifacts["replay_intake_report.json"] = None
    else:
        parse_input_artifacts["replay_intake_report.json"] = None

    if replay_binding_path is not None:
        try:
            parse_input_artifacts["replay_binding.json"] = _sha256_file(replay_binding_path)
        except OSError:
            parse_input_artifacts["replay_binding.json"] = None
    else:
        parse_input_artifacts["replay_binding.json"] = None

    if intake_report is not None:
        _ = intake_report  # advisory context only (M08 plan)

    intake_hash_ok = True
    if intake_receipt_path is not None:
        if ir_err is not None:
            intake_hash_ok = False
            reason_codes.append("intake_receipt_invalid")
            advisory.append(f"intake receipt load failed: {ir_err}")
        elif intake_receipt is not None:
            expected = intake_receipt.get("replay_content_sha256")
            if not isinstance(expected, str) or len(expected) != 64:
                intake_hash_ok = False
                reason_codes.append("intake_receipt_missing_hash")
            elif replay_sha256 is not None and expected.lower() != replay_sha256.lower():
                intake_hash_ok = False
                reason_codes.append("intake_receipt_hash_mismatch")
        checks.append(
            CheckResult(
                check_id="intake_receipt_hash_match",
                detail=None,
                severity="required",
                status="pass"
                if intake_hash_ok and intake_receipt_path is not None and ir_err is None
                else ("not_evaluated" if intake_receipt_path is None else "fail"),
            ),
        )
    else:
        checks.append(
            CheckResult(
                check_id="intake_receipt_hash_match",
                detail=None,
                severity="warning",
                status="not_evaluated",
            ),
        )

    binding_hash_ok = True
    if replay_binding_path is not None:
        if bind_err is not None:
            binding_hash_ok = False
            reason_codes.append("replay_binding_invalid")
            advisory.append(f"replay binding load failed: {bind_err}")
        elif binding is not None:
            expected = binding.get("replay_content_sha256")
            if not isinstance(expected, str) or len(expected) != 64:
                binding_hash_ok = False
                reason_codes.append("replay_binding_missing_hash")
            elif replay_sha256 is not None and expected.lower() != replay_sha256.lower():
                binding_hash_ok = False
                reason_codes.append("binding_hash_mismatch")
        checks.append(
            CheckResult(
                check_id="binding_hash_match",
                detail=None,
                severity="required",
                status="pass"
                if binding_hash_ok and replay_binding_path is not None and bind_err is None
                else ("not_evaluated" if replay_binding_path is None else "fail"),
            ),
        )
    else:
        checks.append(
            CheckResult(
                check_id="binding_hash_match",
                detail=None,
                severity="warning",
                status="not_evaluated",
            ),
        )

    contract_failed = not intake_hash_ok or not binding_hash_ok or replay_sha256 is None

    if contract_failed:
        status: ParseStatus = "input_contract_failed"
        overrides: dict[str, tuple[str, CheckSeverity, str | None]] = {
            "parse_attempted": (
                "not_evaluated",
                "required",
                "skipped due to input contract failure",
            ),
            "raw_sections_normalized": ("not_evaluated", "required", None),
            "raw_parse_emitted": ("pass", "required", "empty envelope emitted"),
        }
        checks = _merge_checks(base=checks, overrides=overrides)
        raw_parse = _build_raw_parse_empty(
            adapter=adapter,
            replay_sha256=replay_sha256,
        )
        receipt = _build_receipt(
            adapter=adapter,
            parse_input_artifacts=parse_input_artifacts,
            raw_parse_sha256=sha256_hex_of_canonical_json(raw_parse),
            replay_path=replay_path,
            replay_sha256=replay_sha256,
        )
        report = _build_report(
            adapter=adapter,
            advisory_notes=sorted(advisory),
            checks=checks,
            reason_codes=sorted(set(reason_codes)),
            replay_sha256=replay_sha256,
            status=status,
        )
        return status, receipt, report, raw_parse

    if not adapter.dependency_available():
        reason_codes.append("parser_unavailable")
        advisory.append(
            "replay parser dependencies not importable; "
            "install optional extra starlab[replay-parser]",
        )
        checks.append(
            CheckResult(
                check_id="parse_attempted",
                detail=None,
                severity="required",
                status="not_evaluated",
            ),
        )
        checks.append(
            CheckResult(
                check_id="raw_sections_normalized",
                detail=None,
                severity="required",
                status="fail",
            ),
        )
        checks.append(
            CheckResult(
                check_id="raw_parse_emitted",
                detail=None,
                severity="required",
                status="pass",
            ),
        )
        status = "parser_unavailable"
        raw_parse = _build_raw_parse_empty(
            adapter=adapter,
            replay_sha256=replay_sha256,
        )
        receipt = _build_receipt(
            adapter=adapter,
            parse_input_artifacts=parse_input_artifacts,
            raw_parse_sha256=sha256_hex_of_canonical_json(raw_parse),
            replay_path=replay_path,
            replay_sha256=replay_sha256,
        )
        report = _build_report(
            adapter=adapter,
            advisory_notes=sorted(advisory),
            checks=checks,
            reason_codes=sorted(set(reason_codes)),
            replay_sha256=replay_sha256,
            status=status,
        )
        return status, receipt, report, raw_parse

    # Parse attempt
    checks.append(
        CheckResult(
            check_id="parse_attempted",
            detail=None,
            severity="required",
            status="pass",
        ),
    )

    outcome = adapter.parse_replay_file(replay_path)

    if isinstance(outcome, AdapterFailure):
        status = _status_from_adapter_failure(outcome.kind)
        reason_codes.append(outcome.kind)
        advisory.append(outcome.message)
        checks.append(
            CheckResult(
                check_id="raw_sections_normalized",
                detail=None,
                severity="required",
                status="fail",
            ),
        )
        checks.append(
            CheckResult(
                check_id="raw_parse_emitted",
                detail=None,
                severity="required",
                status="pass",
            ),
        )
        raw_parse = _build_raw_parse_empty(
            adapter=adapter,
            replay_sha256=replay_sha256,
        )
        receipt = _build_receipt(
            adapter=adapter,
            parse_input_artifacts=parse_input_artifacts,
            raw_parse_sha256=sha256_hex_of_canonical_json(raw_parse),
            replay_path=replay_path,
            replay_sha256=replay_sha256,
        )
        report = _build_report(
            adapter=adapter,
            advisory_notes=sorted(advisory),
            checks=checks,
            reason_codes=sorted(set(reason_codes)),
            replay_sha256=replay_sha256,
            status=status,
        )
        return status, receipt, report, raw_parse

    assert isinstance(outcome, AdapterSuccess)
    try:
        raw_sections_norm = _normalize_raw_sections(outcome.raw_sections)
        event_avail = {
            "attribute_events_available": outcome.availability.attribute_events_available,
            "game_events_available": outcome.availability.game_events_available,
            "message_events_available": outcome.availability.message_events_available,
            "tracker_events_available": outcome.availability.tracker_events_available,
        }
        protocol_ctx = normalize_value(outcome.protocol_context)
        raw_streams_norm: dict[str, Any] | None = None
        schema_ver = RAW_PARSE_SCHEMA_VERSION_V1
        if outcome.raw_event_streams is not None:
            raw_streams_norm = _normalize_raw_event_streams(outcome.raw_event_streams)
            schema_ver = RAW_PARSE_SCHEMA_VERSION_V2
    except NormalizationError as exc:
        status = "parse_failed"
        reason_codes.append("normalization_failed")
        advisory.append(str(exc))
        checks.append(
            CheckResult(
                check_id="raw_sections_normalized",
                detail=str(exc),
                severity="required",
                status="fail",
            ),
        )
        checks.append(
            CheckResult(
                check_id="raw_parse_emitted",
                detail=None,
                severity="required",
                status="pass",
            ),
        )
        raw_parse = _build_raw_parse_empty(
            adapter=adapter,
            replay_sha256=replay_sha256,
        )
        receipt = _build_receipt(
            adapter=adapter,
            parse_input_artifacts=parse_input_artifacts,
            raw_parse_sha256=sha256_hex_of_canonical_json(raw_parse),
            replay_path=replay_path,
            replay_sha256=replay_sha256,
        )
        report = _build_report(
            adapter=adapter,
            advisory_notes=sorted(advisory),
            checks=checks,
            reason_codes=sorted(set(reason_codes)),
            replay_sha256=replay_sha256,
            status=status,
        )
        return status, receipt, report, raw_parse

    parsed_raw: dict[str, Any] = {
        "event_streams_available": event_avail,
        "normalization_profile": NORMALIZATION_PROFILE_V1,
        "parser_family": adapter.parser_family(),
        "parser_version": adapter.parser_version(),
        "protocol_context": protocol_ctx,
        "raw_sections": raw_sections_norm,
        "replay_content_sha256": replay_sha256,
        "schema_version": schema_ver,
    }
    if raw_streams_norm is not None:
        parsed_raw["raw_event_streams"] = raw_streams_norm

    checks.append(
        CheckResult(
            check_id="raw_sections_normalized",
            detail=None,
            severity="required",
            status="pass",
        ),
    )
    checks.append(
        CheckResult(
            check_id="raw_parse_emitted",
            detail=None,
            severity="required",
            status="pass",
        ),
    )

    status = "parsed"
    receipt = _build_receipt(
        adapter=adapter,
        parse_input_artifacts=parse_input_artifacts,
        raw_parse_sha256=sha256_hex_of_canonical_json(parsed_raw),
        replay_path=replay_path,
        replay_sha256=replay_sha256,
    )
    report = _build_report(
        adapter=adapter,
        advisory_notes=sorted(advisory),
        checks=checks,
        reason_codes=sorted(set(reason_codes)),
        replay_sha256=replay_sha256,
        status=status,
    )
    return status, receipt, report, parsed_raw


__all__ = ["run_replay_parse"]
