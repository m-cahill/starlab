"""Load timeline + M11 build-order/economy + optional lineage / raw parse; emit M12 artifacts."""

# ruff: noqa: I001
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starlab.replays.combat_scouting_visibility_extraction import (
    extract_combat_scouting_visibility_envelope,
    validate_build_order_economy_contract,
    validate_timeline_contract,
)
from starlab.replays.combat_scouting_visibility_models import (
    COMBAT_SCOUTING_VISIBILITY_CONTRACT_VERSION as _M12CV,
    COMBAT_SCOUTING_VISIBILITY_PROFILE as _M12P,
    COMBAT_SCOUTING_VISIBILITY_REPORT_SCHEMA_VERSION as _M12R,
    COMBAT_SCOUTING_VISIBILITY_SCHEMA_VERSION as _M12S,
    CombatScoutingVisibilityCheckResult,
    ExtractionStatus,
    RunStatus,
    finalize_combat_scouting_visibility_checks,
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


def exit_code_for_combat_scouting_visibility_run(status: str) -> int:
    if status == "completed":
        return 0
    if status == "source_contract_failed":
        return 5
    if status == "extraction_failed":
        return 4
    msg = f"unknown combat/scouting/visibility run status: {status!r}"
    raise ValueError(msg)


def _counts_surfaces(
    combat_windows: list[dict[str, Any]],
    scouting_observations: list[dict[str, Any]],
    visibility_windows: list[dict[str, Any]],
) -> dict[str, int]:
    return {
        "combat_windows": len(combat_windows),
        "scouting_observations": len(scouting_observations),
        "visibility_windows": len(visibility_windows),
    }


def _counts_by_player(
    combat_windows: list[dict[str, Any]],
    scouting_observations: list[dict[str, Any]],
    visibility_windows: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    acc: dict[str, dict[str, int]] = {}
    for w in combat_windows:
        for p in w.get("players_involved", []):
            pk = str(p)
            acc.setdefault(
                pk, {"combat_windows": 0, "scouting_observations": 0, "visibility_windows": 0}
            )
            acc[pk]["combat_windows"] = acc[pk].get("combat_windows", 0) + 1
    for o in scouting_observations:
        sp = o.get("subject_player_index")
        if isinstance(sp, int) and not isinstance(sp, bool):
            pk = str(sp)
            acc.setdefault(
                pk, {"combat_windows": 0, "scouting_observations": 0, "visibility_windows": 0}
            )
            acc[pk]["scouting_observations"] = acc[pk].get("scouting_observations", 0) + 1
    for v in visibility_windows:
        sp = v.get("subject_player_index")
        if isinstance(sp, int) and not isinstance(sp, bool):
            pk = str(sp)
            acc.setdefault(
                pk, {"combat_windows": 0, "scouting_observations": 0, "visibility_windows": 0}
            )
            acc[pk]["visibility_windows"] = acc[pk].get("visibility_windows", 0) + 1
    return dict(sorted(acc.items()))


def _counts_by_role(
    combat_windows: list[dict[str, Any]],
    scouting_observations: list[dict[str, Any]],
    visibility_windows: list[dict[str, Any]],
) -> dict[str, int]:
    out: dict[str, int] = {}
    for w in combat_windows:
        lbr = w.get("losses_by_role")
        if isinstance(lbr, dict):
            for k, v in lbr.items():
                if isinstance(k, str) and isinstance(v, int):
                    out[k] = out.get(k, 0) + v
    for o in scouting_observations:
        er = o.get("entity_role")
        if isinstance(er, str):
            out[er] = out.get(er, 0) + 1
    for v in visibility_windows:
        er = v.get("entity_role")
        if isinstance(er, str):
            out[er] = out.get(er, 0) + 1
    return dict(sorted(out.items()))


def run_combat_scouting_visibility_extraction(
    *,
    timeline: dict[str, Any],
    source_timeline_sha256: str,
    build_order_economy: dict[str, Any],
    source_build_order_economy_sha256: str,
    raw_parse: dict[str, Any] | None,
    source_raw_parse_sha256: str | None,
    timeline_report: dict[str, Any] | None,
    build_order_economy_report: dict[str, Any] | None,
    metadata: dict[str, Any] | None,
    metadata_report: dict[str, Any] | None,
) -> tuple[RunStatus, dict[str, Any], dict[str, Any]]:
    """Return ``(run_status, artifact, report)`` including finalized ``check_results``."""

    checks: list[CombatScoutingVisibilityCheckResult] = []

    ok_tl, err_tl = validate_timeline_contract(timeline)
    checks.append(
        CombatScoutingVisibilityCheckResult(
            check_id="timeline_schema_valid",
            detail=None if ok_tl else err_tl,
            severity="required",
            status="pass" if ok_tl else "fail",
        ),
    )

    ok_boe, err_boe = validate_build_order_economy_contract(build_order_economy)
    checks.append(
        CombatScoutingVisibilityCheckResult(
            check_id="build_order_economy_schema_valid",
            detail=None if ok_boe else err_boe,
            severity="required",
            status="pass" if ok_boe else "fail",
        ),
    )

    boe_tl = build_order_economy.get("source_timeline_sha256")
    hash_match = isinstance(boe_tl, str) and boe_tl.lower() == source_timeline_sha256.lower()
    checks.append(
        CombatScoutingVisibilityCheckResult(
            check_id="timeline_boe_hash_consistent",
            detail=None
            if hash_match
            else (
                "build_order_economy.source_timeline_sha256 does not match canonical timeline hash"
            ),
            severity="required",
            status="pass" if hash_match else "fail",
        ),
    )

    rhash = timeline.get("replay_content_sha256")
    hash_ok = _is_hex_sha256(rhash)
    checks.append(
        CombatScoutingVisibilityCheckResult(
            check_id="replay_hash_present",
            detail=None if hash_ok else "replay_content_sha256 missing or not 64-hex",
            severity="required",
            status="pass" if hash_ok else "fail",
        ),
    )

    checks.append(
        CombatScoutingVisibilityCheckResult(
            check_id="source_timeline_sha256_computed",
            detail=None,
            severity="required",
            status="pass",
        ),
    )

    checks.append(
        CombatScoutingVisibilityCheckResult(
            check_id="source_build_order_economy_sha256_computed",
            detail=None,
            severity="required",
            status="pass",
        ),
    )

    raw_match_ok = True
    detail_raw: str | None = None
    if raw_parse is not None:
        t_sr = timeline.get("source_raw_parse_sha256")
        if isinstance(t_sr, str) and t_sr:
            if not isinstance(source_raw_parse_sha256, str):
                raw_match_ok = False
                detail_raw = "source_raw_parse_sha256 unavailable for comparison"
            elif t_sr.lower() != source_raw_parse_sha256.lower():
                raw_match_ok = False
                detail_raw = "timeline source_raw_parse_sha256 mismatch vs supplemental raw parse"
    checks.append(
        CombatScoutingVisibilityCheckResult(
            check_id="source_raw_parse_identity_match",
            detail=detail_raw,
            severity="warning",
            status="pass" if raw_match_ok else "warn" if raw_parse is not None else "not_evaluated",
        ),
    )

    contract_failed = not ok_tl or not ok_boe or not hash_match or not hash_ok

    source_tr_sha = (
        sha256_hex_of_canonical_json(timeline_report) if timeline_report is not None else None
    )
    source_boe_rep_sha = (
        sha256_hex_of_canonical_json(build_order_economy_report)
        if build_order_economy_report is not None
        else None
    )
    source_meta_sha = sha256_hex_of_canonical_json(metadata) if metadata is not None else None
    source_meta_rep_sha = (
        sha256_hex_of_canonical_json(metadata_report) if metadata_report is not None else None
    )

    if contract_failed:
        empty: dict[str, Any] = {
            "combat_scouting_visibility_contract_version": _M12CV,
            "combat_scouting_visibility_profile": _M12P,
            "schema_version": _M12S,
            "replay_content_sha256": rhash if isinstance(rhash, str) else None,
            "source_timeline_sha256": source_timeline_sha256,
            "source_build_order_economy_sha256": source_build_order_economy_sha256,
            "source_timeline_report_sha256": source_tr_sha,
            "source_build_order_economy_report_sha256": source_boe_rep_sha,
            "source_metadata_sha256": source_meta_sha,
            "source_metadata_report_sha256": source_meta_rep_sha,
            "source_raw_parse_sha256": source_raw_parse_sha256,
            "classification_profile": {},
            "combat_window_model": "",
            "combat_window_gap_loops": 0,
            "combat_windows": [],
            "ordering_policy": "",
            "scouting_model": "",
            "scouting_observations": [],
            "visibility_model": "",
            "visibility_windows": [],
        }
        checks.append(
            CombatScoutingVisibilityCheckResult(
                check_id="combat_scouting_visibility_emitted",
                detail="empty envelope due to contract failure",
                severity="required",
                status="fail",
            ),
        )
        ordered = finalize_combat_scouting_visibility_checks(checks)
        report_out: dict[str, Any] = {
            "check_results": [c.to_mapping() for c in ordered],
            "combat_scouting_visibility_contract_version": _M12CV,
            "combat_scouting_visibility_profile": _M12P,
            "counts_by_player": {},
            "counts_by_role": {},
            "counts_by_surface": {},
            "extraction_status": "failed",
            "reason_codes": ["source_contract_failed"],
            "schema_version": _M12R,
            "unclassified_entity_names": [],
            "unsupported_signal_kinds": [],
            "warnings": [],
        }
        return "source_contract_failed", empty, report_out

    body, partial = extract_combat_scouting_visibility_envelope(
        build_order_economy=build_order_economy,
        raw_parse=raw_parse,
        source_build_order_economy_report_sha256=source_boe_rep_sha,
        source_build_order_economy_sha256=source_build_order_economy_sha256,
        source_metadata_report_sha256=source_meta_rep_sha,
        source_metadata_sha256=source_meta_sha,
        source_raw_parse_sha256=source_raw_parse_sha256,
        source_timeline_report_sha256=source_tr_sha,
        source_timeline_sha256=source_timeline_sha256,
        timeline=timeline,
    )

    cw = body.get("combat_windows")
    so = body.get("scouting_observations")
    vw = body.get("visibility_windows")
    if not isinstance(cw, list):
        cw = []
    if not isinstance(so, list):
        so = []
    if not isinstance(vw, list):
        vw = []

    extraction_status: ExtractionStatus = "ok"
    warns = partial.get("warnings", [])
    if not isinstance(warns, list):
        warns = []
    if warns or not raw_match_ok or partial.get("unclassified_entity_names"):
        extraction_status = "partial"

    checks.append(
        CombatScoutingVisibilityCheckResult(
            check_id="combat_scouting_visibility_emitted",
            detail=None,
            severity="required",
            status="pass",
        ),
    )
    ordered = finalize_combat_scouting_visibility_checks(checks)

    reason_codes: list[str] = []
    if not raw_match_ok:
        reason_codes.append("supplemental_raw_parse_hash_mismatch")

    report_out = {
        **partial,
        "check_results": [c.to_mapping() for c in ordered],
        "combat_scouting_visibility_contract_version": _M12CV,
        "combat_scouting_visibility_profile": _M12P,
        "counts_by_player": _counts_by_player(cw, so, vw),
        "counts_by_role": _counts_by_role(cw, so, vw),
        "counts_by_surface": _counts_surfaces(cw, so, vw),
        "extraction_status": extraction_status,
        "reason_codes": reason_codes,
        "schema_version": _M12R,
    }
    return "completed", body, report_out


def write_combat_scouting_visibility_artifacts(
    *,
    output_dir: Path,
    artifact: dict[str, Any],
    report: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ap = output_dir / "replay_combat_scouting_visibility.json"
    rp = output_dir / "replay_combat_scouting_visibility_report.json"
    ap.write_text(canonical_json_dumps(artifact), encoding="utf-8")
    rp.write_text(canonical_json_dumps(report), encoding="utf-8")
    return ap, rp


def extract_combat_scouting_visibility_from_paths(
    *,
    timeline_path: Path,
    build_order_economy_path: Path,
    output_dir: Path,
    raw_parse_path: Path | None,
    timeline_report_path: Path | None,
    build_order_economy_report_path: Path | None,
    metadata_path: Path | None,
    metadata_report_path: Path | None,
) -> tuple[RunStatus, dict[str, Any], dict[str, Any]]:
    timeline, terr = load_json_object(timeline_path)
    if timeline is None:
        artifact = {
            "combat_scouting_visibility_contract_version": _M12CV,
            "combat_scouting_visibility_profile": _M12P,
            "schema_version": _M12S,
            "combat_windows": [],
            "scouting_observations": [],
            "visibility_windows": [],
        }
        report: dict[str, Any] = {
            "check_results": [
                c.to_mapping()
                for c in finalize_combat_scouting_visibility_checks(
                    [
                        CombatScoutingVisibilityCheckResult(
                            check_id="timeline_schema_valid",
                            detail=str(terr),
                            severity="required",
                            status="fail",
                        ),
                    ],
                )
            ],
            "combat_scouting_visibility_contract_version": _M12CV,
            "combat_scouting_visibility_profile": _M12P,
            "extraction_status": "failed",
            "reason_codes": ["timeline_load_failed"],
            "schema_version": _M12R,
            "warnings": [f"failed to load timeline: {terr}"],
        }
        write_combat_scouting_visibility_artifacts(
            artifact=artifact, output_dir=output_dir, report=report
        )
        return "extraction_failed", artifact, report

    boe, boerr = load_json_object(build_order_economy_path)
    if boe is None:
        sha_t = sha256_hex_of_canonical_json(timeline)
        artifact = {
            "combat_scouting_visibility_contract_version": _M12CV,
            "combat_scouting_visibility_profile": _M12P,
            "schema_version": _M12S,
            "source_timeline_sha256": sha_t,
            "combat_windows": [],
            "scouting_observations": [],
            "visibility_windows": [],
        }
        report = {
            "check_results": [
                c.to_mapping()
                for c in finalize_combat_scouting_visibility_checks(
                    [
                        CombatScoutingVisibilityCheckResult(
                            check_id="build_order_economy_schema_valid",
                            detail=str(boerr),
                            severity="required",
                            status="fail",
                        ),
                    ],
                )
            ],
            "combat_scouting_visibility_contract_version": _M12CV,
            "combat_scouting_visibility_profile": _M12P,
            "extraction_status": "failed",
            "reason_codes": ["build_order_economy_load_failed"],
            "schema_version": _M12R,
            "warnings": [f"failed to load build_order_economy: {boerr}"],
        }
        write_combat_scouting_visibility_artifacts(
            artifact=artifact, output_dir=output_dir, report=report
        )
        return "extraction_failed", artifact, report

    source_timeline_sha256 = sha256_hex_of_canonical_json(timeline)
    source_build_order_economy_sha256 = sha256_hex_of_canonical_json(boe)

    def _load_opt(p: Path | None) -> dict[str, Any] | None:
        if p is None:
            return None
        d, e = load_json_object(p)
        if e is not None:
            raise ValueError(e)
        return d

    try:
        raw_parse = _load_opt(raw_parse_path)
        timeline_report = _load_opt(timeline_report_path)
        build_order_economy_report = _load_opt(build_order_economy_report_path)
        metadata = _load_opt(metadata_path)
        metadata_report = _load_opt(metadata_report_path)
    except ValueError as exc:
        sha_t = sha256_hex_of_canonical_json(timeline)
        artifact_err = {
            "combat_scouting_visibility_contract_version": _M12CV,
            "combat_scouting_visibility_profile": _M12P,
            "schema_version": _M12S,
            "source_timeline_sha256": sha_t,
            "source_build_order_economy_sha256": source_build_order_economy_sha256,
            "combat_windows": [],
            "scouting_observations": [],
            "visibility_windows": [],
        }
        report_err = {
            "check_results": [
                c.to_mapping()
                for c in finalize_combat_scouting_visibility_checks(
                    [
                        CombatScoutingVisibilityCheckResult(
                            check_id="source_raw_parse_identity_match",
                            detail=str(exc),
                            severity="required",
                            status="fail",
                        ),
                    ],
                )
            ],
            "combat_scouting_visibility_contract_version": _M12CV,
            "combat_scouting_visibility_profile": _M12P,
            "extraction_status": "failed",
            "reason_codes": ["lineage_load_failed"],
            "schema_version": _M12R,
            "warnings": [str(exc)],
        }
        write_combat_scouting_visibility_artifacts(
            artifact=artifact_err,
            output_dir=output_dir,
            report=report_err,
        )
        return "extraction_failed", artifact_err, report_err

    source_raw_parse_sha256 = (
        sha256_hex_of_canonical_json(raw_parse) if raw_parse is not None else None
    )

    status, body, report_out = run_combat_scouting_visibility_extraction(
        build_order_economy=boe,
        build_order_economy_report=build_order_economy_report,
        metadata=metadata,
        metadata_report=metadata_report,
        raw_parse=raw_parse,
        source_build_order_economy_sha256=source_build_order_economy_sha256,
        source_raw_parse_sha256=source_raw_parse_sha256,
        source_timeline_sha256=source_timeline_sha256,
        timeline=timeline,
        timeline_report=timeline_report,
    )
    write_combat_scouting_visibility_artifacts(
        artifact=body, output_dir=output_dir, report=report_out
    )
    return status, body, report_out
