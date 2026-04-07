"""Load M08 artifacts, verify linkage, emit metadata + report (M09)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.replays.metadata_extraction import (
    RAW_PARSE_SCHEMA_EXPECTED,
    build_metadata_envelope,
    core_metadata_ok,
    player_rows_complete,
    required_sections_non_null,
)
from starlab.replays.metadata_models import (
    METADATA_CONTRACT_VERSION,
    METADATA_PROFILE,
    METADATA_REPORT_SCHEMA_VERSION,
    METADATA_SCHEMA_VERSION,
    ExtractionStatus,
    MetadataCheckResult,
    finalize_metadata_checks,
)
from starlab.runs.json_util import canonical_json_dumps, sha256_hex_of_canonical_json


def _is_hex_sha256(v: Any) -> bool:
    if not isinstance(v, str) or len(v) != 64:
        return False
    try:
        int(v, 16)
    except ValueError:
        return False
    return True


def load_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(raw, dict):
        return None, "JSON root must be an object"
    return raw, None


def exit_code_for_extraction_status(status: ExtractionStatus) -> int:
    if status in ("extracted", "partial"):
        return 0
    if status == "source_contract_failed":
        return 5
    if status == "extraction_failed":
        return 4
    msg = f"unknown extraction status: {status!r}"
    raise ValueError(msg)


def _emit_load_failure(
    *,
    advisory: str,
    output_dir: Path,
    raw_parse: dict[str, Any],
    reason_codes: list[str],
    source_sha: str,
) -> tuple[ExtractionStatus, dict[str, Any], dict[str, Any]]:
    """Receipt/report JSON unreadable — emit minimal artifacts and ``extraction_failed``."""

    meta = _empty_metadata_envelope(source_sha=source_sha)
    rh = raw_parse.get("replay_content_sha256")
    if isinstance(rh, str):
        meta["replay_content_sha256"] = rh
    chk = [
        MetadataCheckResult(
            check_id="raw_parse_schema_valid",
            detail=None,
            severity="required",
            status="pass"
            if raw_parse.get("schema_version") == RAW_PARSE_SCHEMA_EXPECTED
            else "fail",
        ),
        MetadataCheckResult(
            check_id="replay_hash_present",
            detail=None,
            severity="required",
            status="pass" if _is_hex_sha256(rh) else "fail",
        ),
        MetadataCheckResult(
            check_id="source_raw_parse_sha256_computed",
            detail=None,
            severity="required",
            status="pass",
        ),
        MetadataCheckResult(
            check_id="parse_receipt_hash_match",
            detail=None,
            severity="warning",
            status="not_evaluated",
        ),
        MetadataCheckResult(
            check_id="parse_report_status_parsed",
            detail=None,
            severity="warning",
            status="not_evaluated",
        ),
    ]
    rep = _build_report(
        advisory_notes=[advisory],
        checks=chk,
        extraction_status="extraction_failed",
        reason_codes=reason_codes,
        replay_sha=rh if isinstance(rh, str) else None,
        source_sha=source_sha,
    )
    write_metadata_artifacts(output_dir=output_dir, metadata=meta, report=rep)
    return "extraction_failed", meta, rep


def _empty_metadata_envelope(*, source_sha: str) -> dict[str, Any]:
    return {
        "metadata": {
            "game": {
                "event_streams_available": {
                    "attribute_events_available": False,
                    "game_events_available": False,
                    "message_events_available": False,
                    "tracker_events_available": False,
                },
                "game_length_loops": None,
                "player_count": 0,
            },
            "map": {"map_name": None},
            "players": [],
            "protocol": {"base_build": 0, "data_build": 0, "data_version": None},
        },
        "metadata_contract_version": METADATA_CONTRACT_VERSION,
        "metadata_profile": METADATA_PROFILE,
        "parser_family": "unknown",
        "parser_version": "unknown",
        "replay_content_sha256": None,
        "schema_version": METADATA_SCHEMA_VERSION,
        "source_raw_parse_sha256": source_sha,
        "source_sections_present": [],
    }


def run_metadata_extraction(
    *,
    raw_parse: dict[str, Any],
    source_raw_parse_sha256: str,
    parse_receipt: dict[str, Any] | None,
    parse_report: dict[str, Any] | None,
) -> tuple[ExtractionStatus, dict[str, Any], dict[str, Any]]:
    """Return ``(status, metadata_envelope, report)``."""

    reason_codes: list[str] = []
    advisory: list[str] = []
    checks: list[MetadataCheckResult] = []

    # --- raw_parse_schema_valid
    schema_ok = (
        isinstance(raw_parse.get("schema_version"), str)
        and raw_parse.get(
            "schema_version",
        )
        == RAW_PARSE_SCHEMA_EXPECTED
    )
    if not schema_ok:
        reason_codes.append("raw_parse_schema_invalid")
        checks.append(
            MetadataCheckResult(
                check_id="raw_parse_schema_valid",
                detail="schema_version must be starlab.replay_raw_parse.v1",
                severity="required",
                status="fail",
            ),
        )
    else:
        checks.append(
            MetadataCheckResult(
                check_id="raw_parse_schema_valid",
                detail=None,
                severity="required",
                status="pass",
            ),
        )

    # --- replay_hash_present
    rhash = raw_parse.get("replay_content_sha256")
    hash_ok = _is_hex_sha256(rhash)
    if not hash_ok:
        reason_codes.append("replay_hash_missing_or_invalid")
        checks.append(
            MetadataCheckResult(
                check_id="replay_hash_present",
                detail="replay_content_sha256 must be a 64-char hex string",
                severity="required",
                status="fail",
            ),
        )
    else:
        checks.append(
            MetadataCheckResult(
                check_id="replay_hash_present",
                detail=None,
                severity="required",
                status="pass",
            ),
        )

    # --- source_raw_parse_sha256_computed
    checks.append(
        MetadataCheckResult(
            check_id="source_raw_parse_sha256_computed",
            detail=None,
            severity="required",
            status="pass",
        ),
    )

    # --- parse_receipt_hash_match
    if parse_receipt is None:
        checks.append(
            MetadataCheckResult(
                check_id="parse_receipt_hash_match",
                detail=None,
                severity="warning",
                status="not_evaluated",
            ),
        )
    else:
        cr = parse_receipt.get("replay_content_sha256")
        rr = parse_receipt.get("raw_parse_sha256")
        receipt_ok = (
            isinstance(cr, str)
            and isinstance(rhash, str)
            and cr.lower() == rhash.lower()
            and isinstance(rr, str)
            and rr.lower() == source_raw_parse_sha256.lower()
        )
        if not receipt_ok:
            reason_codes.append("parse_receipt_hash_mismatch")
            advisory.append("receipt replay hash or raw_parse_sha256 mismatch")
            checks.append(
                MetadataCheckResult(
                    check_id="parse_receipt_hash_match",
                    detail="receipt linkage failed",
                    severity="required",
                    status="fail",
                ),
            )
        else:
            checks.append(
                MetadataCheckResult(
                    check_id="parse_receipt_hash_match",
                    detail=None,
                    severity="required",
                    status="pass",
                ),
            )

    # --- parse_report_status_parsed
    if parse_report is None:
        checks.append(
            MetadataCheckResult(
                check_id="parse_report_status_parsed",
                detail=None,
                severity="warning",
                status="not_evaluated",
            ),
        )
    else:
        pr = parse_report.get("replay_content_sha256")
        st = parse_report.get("parse_status")
        report_hash_ok = (
            isinstance(pr, str) and isinstance(rhash, str) and pr.lower() == rhash.lower()
        )
        if not report_hash_ok:
            reason_codes.append("parse_report_replay_hash_mismatch")
            checks.append(
                MetadataCheckResult(
                    check_id="parse_report_status_parsed",
                    detail="replay_content_sha256 mismatch with parse report",
                    severity="required",
                    status="fail",
                ),
            )
        elif st != "parsed":
            reason_codes.append("parse_report_not_parsed")
            checks.append(
                MetadataCheckResult(
                    check_id="parse_report_status_parsed",
                    detail=f"parse_status is {st!r}, expected parsed",
                    severity="required",
                    status="fail",
                ),
            )
        else:
            checks.append(
                MetadataCheckResult(
                    check_id="parse_report_status_parsed",
                    detail=None,
                    severity="required",
                    status="pass",
                ),
            )

    contract_failed = any(
        c.check_id in ("parse_receipt_hash_match", "parse_report_status_parsed")
        and c.status == "fail"
        and c.severity == "required"
        for c in checks
    )

    if not schema_ok or not hash_ok:
        contract_failed = True

    if contract_failed:
        meta = _empty_metadata_envelope(source_sha=source_raw_parse_sha256)
        if isinstance(rhash, str):
            meta["replay_content_sha256"] = rhash
        report_out = _build_report(
            advisory_notes=advisory,
            checks=checks,
            extraction_status="source_contract_failed",
            reason_codes=reason_codes,
            replay_sha=rhash if isinstance(rhash, str) else None,
            source_sha=source_raw_parse_sha256,
        )
        return "source_contract_failed", meta, report_out

    # --- extract metadata body
    try:
        meta_env, ambiguous = build_metadata_envelope(
            raw=raw_parse,
            source_raw_parse_sha256=source_raw_parse_sha256,
        )
    except Exception as exc:  # noqa: BLE001 — boundary: surface as extraction_failed
        reason_codes.append("metadata_build_failed")
        advisory.append(str(exc))
        meta = _empty_metadata_envelope(source_sha=source_raw_parse_sha256)
        if isinstance(rhash, str):
            meta["replay_content_sha256"] = rhash
        checks.append(
            MetadataCheckResult(
                check_id="required_sections_present",
                detail=None,
                severity="required",
                status="not_evaluated",
            ),
        )
        checks.append(
            MetadataCheckResult(
                check_id="core_metadata_extracted",
                detail=None,
                severity="required",
                status="fail",
            ),
        )
        checks.append(
            MetadataCheckResult(
                check_id="player_metadata_extracted",
                detail=None,
                severity="warning",
                status="not_evaluated",
            ),
        )
        checks.append(
            MetadataCheckResult(
                check_id="metadata_emitted",
                detail=None,
                severity="required",
                status="pass",
            ),
        )
        report_out = _build_report(
            advisory_notes=advisory,
            checks=checks,
            extraction_status="extraction_failed",
            reason_codes=reason_codes,
            replay_sha=rhash if isinstance(rhash, str) else None,
            source_sha=source_raw_parse_sha256,
        )
        return "extraction_failed", meta, report_out

    inner = meta_env.get("metadata")
    assert isinstance(inner, dict)

    # --- required_sections_present
    if required_sections_non_null(raw_parse):
        checks.append(
            MetadataCheckResult(
                check_id="required_sections_present",
                detail=None,
                severity="required",
                status="pass",
            ),
        )
        req_ok = True
    else:
        checks.append(
            MetadataCheckResult(
                check_id="required_sections_present",
                detail="header, details, or init_data missing",
                severity="required",
                status="fail",
            ),
        )
        req_ok = False

    # --- core_metadata_extracted
    if core_metadata_ok(inner):
        checks.append(
            MetadataCheckResult(
                check_id="core_metadata_extracted",
                detail=None,
                severity="required",
                status="pass",
            ),
        )
        core_ok = True
    else:
        checks.append(
            MetadataCheckResult(
                check_id="core_metadata_extracted",
                detail=None,
                severity="required",
                status="fail",
            ),
        )
        core_ok = False

    players = inner.get("players")
    pl_ok = isinstance(players, list) and player_rows_complete(players)
    if pl_ok and not ambiguous:
        checks.append(
            MetadataCheckResult(
                check_id="player_metadata_extracted",
                detail=None,
                severity="warning",
                status="pass",
            ),
        )
    elif not pl_ok:
        reason_codes.append("player_metadata_incomplete")
        checks.append(
            MetadataCheckResult(
                check_id="player_metadata_extracted",
                detail="player list malformed",
                severity="warning",
                status="fail",
            ),
        )
    else:
        reason_codes.append("player_metadata_ambiguous")
        checks.append(
            MetadataCheckResult(
                check_id="player_metadata_extracted",
                detail="unmapped player control/race value",
                severity="warning",
                status="warn",
            ),
        )

    checks.append(
        MetadataCheckResult(
            check_id="metadata_emitted",
            detail=None,
            severity="required",
            status="pass",
        ),
    )

    # --- status rollup
    player_extracted_ok = (
        pl_ok
        and not ambiguous
        and not any(
            c.check_id == "player_metadata_extracted" and c.status == "fail" for c in checks
        )
    )
    if req_ok and core_ok and player_extracted_ok:
        status: ExtractionStatus = "extracted"
    else:
        status = "partial"

    report_out = _build_report(
        advisory_notes=advisory,
        checks=checks,
        extraction_status=status,
        reason_codes=reason_codes,
        replay_sha=rhash if isinstance(rhash, str) else None,
        source_sha=source_raw_parse_sha256,
    )
    return status, meta_env, report_out


def _build_report(
    *,
    advisory_notes: list[str],
    checks: list[MetadataCheckResult],
    extraction_status: ExtractionStatus,
    reason_codes: list[str],
    replay_sha: str | None,
    source_sha: str,
) -> dict[str, Any]:
    ordered = finalize_metadata_checks(checks)
    return {
        "advisory_notes": sorted(set(advisory_notes)),
        "check_results": [c.to_mapping() for c in ordered],
        "extraction_status": extraction_status,
        "metadata_contract_version": METADATA_CONTRACT_VERSION,
        "reason_codes": sorted(set(reason_codes)),
        "replay_content_sha256": replay_sha,
        "schema_version": METADATA_REPORT_SCHEMA_VERSION,
        "source_raw_parse_sha256": source_sha,
    }


def write_metadata_artifacts(
    *,
    output_dir: Path,
    metadata: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    mp = output_dir / "replay_metadata.json"
    rp = output_dir / "replay_metadata_report.json"
    mp.write_text(canonical_json_dumps(metadata), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    return mp, rp


def extract_from_paths(
    *,
    raw_parse_path: Path,
    output_dir: Path,
    parse_receipt_path: Path | None,
    parse_report_path: Path | None,
) -> tuple[ExtractionStatus, dict[str, Any], dict[str, Any]]:
    """Load files, run pipeline, write artifacts; return status and bodies."""

    raw, err = load_json_object(raw_parse_path)
    if raw is None:
        meta = _empty_metadata_envelope(source_sha="")
        chk = [
            MetadataCheckResult(
                check_id="raw_parse_schema_valid",
                detail=str(err),
                severity="required",
                status="fail",
            ),
        ]
        rep = _build_report(
            advisory_notes=[f"failed to load raw parse: {err}"],
            checks=chk,
            extraction_status="extraction_failed",
            reason_codes=["raw_parse_load_failed"],
            replay_sha=None,
            source_sha="",
        )
        write_metadata_artifacts(output_dir=output_dir, metadata=meta, report=rep)
        return "extraction_failed", meta, rep

    source_sha = sha256_hex_of_canonical_json(raw)
    receipt: dict[str, Any] | None = None
    report: dict[str, Any] | None = None
    if parse_receipt_path is not None:
        receipt, rerr = load_json_object(parse_receipt_path)
        if rerr is not None:
            return _emit_load_failure(
                advisory=f"failed to load parse receipt: {rerr}",
                output_dir=output_dir,
                raw_parse=raw,
                reason_codes=["parse_receipt_load_failed"],
                source_sha=source_sha,
            )

    if parse_report_path is not None:
        report, perr = load_json_object(parse_report_path)
        if perr is not None:
            return _emit_load_failure(
                advisory=f"failed to load parse report: {perr}",
                output_dir=output_dir,
                raw_parse=raw,
                reason_codes=["parse_report_load_failed"],
                source_sha=source_sha,
            )

    status, meta, rep = run_metadata_extraction(
        parse_receipt=receipt,
        parse_report=report,
        raw_parse=raw,
        source_raw_parse_sha256=source_sha,
    )
    write_metadata_artifacts(output_dir=output_dir, metadata=meta, report=rep)
    return status, meta, rep
