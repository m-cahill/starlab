"""Replay parse orchestration, linkage checks, and artifact emission (M08)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from starlab.replays.parser_interfaces import (
    AdapterFailure,
    AdapterSuccess,
    RawEventStreams,
    RawParseSections,
    ReplayParserAdapter,
)
from starlab.replays.parser_models import (
    NORMALIZATION_PROFILE_V1,
    PARSE_CHECK_IDS,
    PARSER_CONTRACT_VERSION,
    POLICY_VERSION,
    RAW_EVENT_STREAMS_SCHEMA_VERSION,
    RAW_PARSE_SCHEMA_VERSION_V1,
    RAW_PARSE_SCHEMA_VERSION_V2,
    RECEIPT_SCHEMA_VERSION,
    REPORT_SCHEMA_VERSION,
    CheckResult,
    CheckSeverity,
    ParseStatus,
)
from starlab.replays.parser_normalization import NormalizationError, normalize_value
from starlab.replays.s2protocol_adapter import default_adapter
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json
from starlab.runs.replay_binding import load_replay_binding


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_replay_opaque(replay_path: Path) -> tuple[str | None, int | None, str | None]:
    """Return ``(sha256_hex, size_bytes, read_error)``."""

    try:
        data = replay_path.read_bytes()
    except OSError as exc:
        return None, None, str(exc)
    return hashlib.sha256(data).hexdigest(), len(data), None


def load_optional_json(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(raw, dict):
        return None, "JSON root must be an object"
    return raw, None


def _status_from_adapter_failure(kind: str) -> ParseStatus:
    if kind == "unsupported_protocol":
        return "unsupported_protocol"
    if kind == "parser_unavailable":
        return "parser_unavailable"
    return "parse_failed"


def finalize_checks(checks: list[CheckResult]) -> list[CheckResult]:
    """Emit checks in ``PARSE_CHECK_IDS`` order; fill gaps with ``not_evaluated``."""

    by_id = {c.check_id: c for c in checks}
    out: list[CheckResult] = []
    for cid in PARSE_CHECK_IDS:
        out.append(
            by_id.get(cid)
            or CheckResult(
                check_id=cid,
                detail=None,
                severity="required",
                status="not_evaluated",
            ),
        )
    return out


def _merge_checks(
    *,
    base: list[CheckResult],
    overrides: dict[str, tuple[str, CheckSeverity, str | None]],
) -> list[CheckResult]:
    out: list[CheckResult] = []
    for cid in PARSE_CHECK_IDS:
        if cid in overrides:
            st, sev, det = overrides[cid]
            out.append(CheckResult(check_id=cid, detail=det, severity=sev, status=st))  # type: ignore[arg-type]
        else:
            found = next((c for c in base if c.check_id == cid), None)
            if found is None:
                out.append(
                    CheckResult(
                        check_id=cid,
                        detail=None,
                        severity="required",
                        status="not_evaluated",
                    ),
                )
            else:
                out.append(found)
    return out


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

    raw_parse: dict[str, Any] = {
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
        raw_parse["raw_event_streams"] = raw_streams_norm

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


def load_optional_replay_binding(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return load_replay_binding(path), None
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        return None, str(exc)


def _normalize_raw_sections(raw: RawParseSections) -> dict[str, Any]:
    """Normalize raw section dicts to JSON-safe trees."""

    sections: dict[str, Any] = {}
    for key, val in (
        ("header", raw.header),
        ("details", raw.details),
        ("init_data", raw.init_data),
        ("attribute_events", raw.attribute_events),
    ):
        if val is None:
            sections[key] = None
        else:
            sections[key] = normalize_value(val)
    return sections


def _build_raw_parse_empty(
    *,
    adapter: ReplayParserAdapter,
    replay_sha256: str | None,
) -> dict[str, Any]:
    return {
        "event_streams_available": {
            "attribute_events_available": False,
            "game_events_available": False,
            "message_events_available": False,
            "tracker_events_available": False,
        },
        "normalization_profile": NORMALIZATION_PROFILE_V1,
        "parser_family": adapter.parser_family(),
        "parser_version": adapter.parser_version(),
        "protocol_context": None,
        "raw_sections": {
            "attribute_events": None,
            "details": None,
            "header": None,
            "init_data": None,
        },
        "replay_content_sha256": replay_sha256,
        "schema_version": RAW_PARSE_SCHEMA_VERSION_V1,
    }


def _normalize_raw_event_streams(streams: RawEventStreams) -> dict[str, Any]:
    """Lower decoded event lists to JSON-safe trees (M10-owned payload area)."""

    out: dict[str, Any] = {"raw_event_streams_schema": RAW_EVENT_STREAMS_SCHEMA_VERSION}
    for key, val in (
        ("game_events", streams.game_events),
        ("message_events", streams.message_events),
        ("tracker_events", streams.tracker_events),
    ):
        if val is None:
            out[key] = None
        else:
            out[key] = normalize_value(val)
    return out


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


def write_parse_artifacts(
    *,
    output_dir: Path,
    receipt: dict[str, Any],
    report: dict[str, Any],
    raw_parse: dict[str, Any],
) -> tuple[Path, Path, Path]:
    """Write deterministic JSON files with trailing newlines."""

    output_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = output_dir / "replay_parse_receipt.json"
    report_path = output_dir / "replay_parse_report.json"
    raw_path = output_dir / "replay_raw_parse.json"
    receipt_path.write_text(canonical_json_dumps(receipt), encoding="utf-8")
    report_path.write_text(canonical_json_dumps(report), encoding="utf-8")
    raw_path.write_text(canonical_json_dumps(raw_parse), encoding="utf-8")
    return receipt_path, report_path, raw_path


def exit_code_for_parse_status(status: ParseStatus) -> int:
    """CLI exit code mapping for ``parse_status``."""

    if status == "parsed":
        return 0
    if status == "unsupported_protocol":
        return 2
    if status == "parser_unavailable":
        return 3
    if status == "parse_failed":
        return 4
    if status == "input_contract_failed":
        return 5
    msg = f"unknown parse status: {status!r}"
    raise ValueError(msg)
